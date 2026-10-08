import copy
import importlib.util
import json
import contextlib
import io
import runpy
import sys
import types
from pathlib import Path
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import unittest
from unittest.mock import patch

from PIL import Image

from bank_ocr.cli import mine
from bank_ocr.data import assign_splits, canonical_image, dumps, parse_ocr, read_json, read_jsonl, scan, write_json, write_jsonl
from bank_ocr.inference import index_predictions, predict
from bank_ocr.metrics import evaluate, numbers, parse_box, reward
from bank_ocr.pipeline import prepare
from demo import create_demo, ocr_from_file


MAPPING = {"items_path": "data.basicData", "success_key": "success", "success_value": "Y"}


class DataTests(unittest.TestCase):
    def test_integer_normalized_boxes_preserve_small_regions(self):
        mapping = {**MAPPING, "box_format": "xyxy"}
        boxes = [[583.836, 224.42364, 746.924, 271.56276],
                 [0.1, 0.1, 0.2, 0.2], [2399.8, 3599.8, 2399.9, 3599.9]]
        raw = {"success": "Y", "data": {"basicData": [
            {"text": "text", "confidence": 1, "bounding": box} for box in boxes
        ]}}
        result = parse_ocr(raw, 2400, 3600, mapping)
        self.assertEqual([r["bbox_norm"] for r in result],
                         [[243, 62, 311, 75], [0, 0, 1, 1], [999, 999, 1000, 1000]])
        self.assertEqual([r["bbox"] for r in result], boxes)
        self.assertTrue(all(type(v) is int for r in result for v in r["bbox_norm"]))

    def test_screenshot_schema_nested_basic_data(self):
        raw = read_json(Path(__file__).parents[1] / "examples" / "ocr-response.json")
        result = parse_ocr(raw, 2000, 1000, MAPPING)
        self.assertEqual(result[0]["bbox"], [140, 46, 224, 76])
        self.assertEqual(result[0]["bbox_norm"], [70, 46, 112, 76])
        self.assertEqual(result[1]["text"], "01/30")

    def test_failed_response_and_malformed_box_rejected(self):
        raw = ocr_from_file("page.png")
        raw["success"] = "N"
        with self.assertRaises(ValueError):
            parse_ocr(raw, 400, 200, MAPPING)
        raw["success"] = "Y"
        raw["data"]["basicData"][0][0]["bounding"]["vertices"][0]["x"] = -1
        with self.assertRaises(ValueError):
            parse_ocr(raw, 400, 200, MAPPING)

    def test_empty_success_page_allowed(self):
        self.assertEqual(parse_ocr({"success": "Y", "data": {"basicData": [[]]}}, 400, 200, MAPPING), [])

    def test_document_leakage_rejected(self):
        rows = [{"document_id": "same", "page_id": str(i), "image": "a.png", "split": s} for i, s in enumerate(["train", "benchmark"])]
        with self.assertRaisesRegex(ValueError, "Document leakage"):
            assign_splits(rows, 42, 0.1)

    def test_validation_is_stable_and_document_level(self):
        rows = [{"document_id": f"d{d}", "page_id": f"p{p}", "image": "x", "split": "train"} for d in range(10) for p in range(3)]
        a, b = assign_splits(rows, 42, 0.2), assign_splits(list(reversed(rows)), 42, 0.2)
        self.assertEqual({(r["document_id"], r["split"]) for r in a}, {(r["document_id"], r["split"]) for r in b})
        self.assertEqual(len({(r["document_id"], r["split"]) for r in a}), 10)

    def test_exif_orientation(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "exif.jpg"
            im = Image.new("RGB", (100, 200))
            exif = Image.Exif()
            exif[274] = 6
            im.save(path, exif=exif)
            with canonical_image(path) as actual:
                self.assertEqual(actual.size, (200, 100))

    def test_scan_requires_explicit_document_grouping(self):
        with tempfile.TemporaryDirectory() as d:
            Image.new("RGB", (10, 10)).save(Path(d) / "doc1_p01.png")
            Image.new("RGB", (10, 10)).save(Path(d) / "doc1_p02.png")
            rows = scan(d, "train", r"(?P<document_id>doc\d+)_p\d+")
            self.assertEqual({r["document_id"] for r in rows}, {"doc1"})
            with self.assertRaises(ValueError):
                scan(d, "train")


class MetricTests(unittest.TestCase):
    def test_strict_box_format(self):
        for bad in ['{"bbox":[true,0,20,20]}', '{"bbox":[0,0,NaN,20]}', '{"bbox":[0,0,1001,20]}',
                    '```json\n{"bbox":[0,0,20,20]}\n```', '{"bbox":[1,1,1,4]}']:
            self.assertIsNone(parse_box(bad))

    def test_numeric_tokens_do_not_collapse(self):
        self.assertNotEqual(numbers("12 34"), numbers("1234"))
        self.assertNotEqual(numbers("123.45"), numbers("123,45"))
        self.assertLess(reward("USD 123.4O", "ocr", "USD 123.40"), 1)
        self.assertEqual(reward("한글", "ocr", "한글"), 1)

    def test_cycle_reward_and_full_page_penalty(self):
        items = [{"text": "USD 12", "bbox": [100, 100, 300, 130]}, {"text": "EXTRA", "bbox": [600, 100, 800, 130]}]
        exact = reward('{"bbox":[100,100,300,130]}', "grounding", "USD 12", items[0]["bbox"], items)
        full = reward('{"bbox":[0,0,1000,1000]}', "grounding", "USD 12", items[0]["bbox"], items)
        self.assertEqual(exact, 1)
        self.assertLess(full, exact)
        self.assertEqual(reward("not json", "grounding", "USD 12", items[0]["bbox"], items), 0)

    def test_swift_plugin_batch_contract(self):
        # Only the public registry is stubbed; actual GPU/SWIFT integration remains untested.
        swift = types.ModuleType("swift")
        registry = types.ModuleType("swift.rewards")
        registry.ORM, registry.orms = object, {}
        with patch.dict(sys.modules, {"swift": swift, "swift.rewards": registry}):
            runpy.run_path(str(Path(__file__).parents[1] / "bank_ocr_reward.py"))
        plugin = registry.orms["bank_ocr_cycle"]()
        scores = plugin(["ABC", '{"bbox":[10,20,30,40]}'], ["bbox_ocr", "grounding"], ["ABC", "42"],
                        [[0, 0, 10, 10], [10, 20, 30, 40]], [[], [{"text": "42", "bbox": [10, 20, 30, 40]}]])
        self.assertEqual(scores, [1, 1])
        with self.assertRaises(ValueError):
            plugin(["ABC"], [], [], [], [])


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.config = create_demo(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_prepare_cache_sft_grpo_and_metrics(self):
        summary = prepare(self.config)
        out = self.root / "prepared"
        self.assertEqual(summary["page_counts"], {"train": 2, "val": 1, "benchmark": 1})
        self.assertEqual(summary["benchmark_examples"], 7)  # 3 crop + 3 bbox + 1 unique grounding
        rows = read_jsonl(out / "benchmark_tasks.jsonl")
        self.assertEqual([r["target_text"] for r in rows if r["task"] == "grounding"], ["USD 123.45"])
        for r in read_jsonl(out / "train_grpo.jsonl"):
            self.assertEqual(len(r["messages"]), 1)
            self.assertEqual(r["split"], "train")
        for r in read_jsonl(out / "train_sft.jsonl"):
            self.assertEqual(r["messages"][-1]["role"], "assistant")
        oracle = {r["id"]: dumps({"bbox": r["target_bbox"]}) if r["task"] == "grounding" else r["target_text"] for r in rows}
        metrics = evaluate(rows, oracle)
        self.assertEqual(metrics["tasks"]["crop_ocr"]["cer"], 0)
        self.assertEqual(metrics["tasks"]["grounding"]["cycle_em"], 1)
        with self.assertRaises(ValueError):
            evaluate(rows, {})
        with self.assertRaisesRegex(ValueError, "Output already exists"):
            prepare(self.config)
        cfg = read_json(self.config)
        cfg["output_dir"] = "prepared2"
        write_json(self.config, cfg)
        with patch("demo.ocr_from_file", side_effect=AssertionError("Cache should be reused")):
            prepare(self.config)

    def test_duplicate_pixels_fail_before_ocr(self):
        manifest = read_jsonl(self.root / "manifest.jsonl")
        manifest[-1]["image"] = manifest[0]["image"]
        write_jsonl(self.root / "manifest.jsonl", manifest)
        with patch("demo.ocr_from_file", side_effect=AssertionError("No OCR during preflight")):
            with self.assertRaisesRegex(ValueError, "Duplicate image leakage"):
                prepare(self.config)

    def test_failure_does_not_poison_cache(self):
        with patch("demo.ocr_from_file", return_value={"success": "N"}):
            with self.assertRaises(ValueError):
                prepare(self.config)
        self.assertEqual(list((self.root / "cache" / "ocr").glob("*.json")), [])
        prepare(self.config)

    def test_mining_rejects_benchmark(self):
        prepare(self.config)
        with self.assertRaisesRegex(ValueError, "TRAIN only"):
            mine(self.root / "prepared" / "benchmark_tasks.jsonl", "unused", "unused", 10, 42, 0.7)

    def test_mining_valid_train_no_duplicate_examples(self):
        prepare(self.config)
        tasks = self.root / "prepared" / "train_grpo.jsonl"
        rows = read_jsonl(tasks)
        predictions = self.root / "train-preds.jsonl"
        write_jsonl(predictions, [{"id": r["id"], "prediction": "WRONG"} for r in rows])
        output = self.root / "mined.jsonl"
        result = mine(tasks, predictions, output, 1000, 42, 0.7)
        self.assertEqual(result["selected"], len(rows))
        self.assertEqual(len({r["id"] for r in read_jsonl(output)}), len(rows))

    def test_train_launch_dry_runs(self):
        prepare(self.config)
        model, adapter = self.root / "fake-model", self.root / "fake-adapter"
        model.mkdir()
        adapter.mkdir()
        launcher = str(Path(__file__).parents[1] / "train.py")
        for stage in ["sft", "grpo"]:
            argv = [launcher, stage, "--model", str(model), "--data", str(self.root / "prepared"),
                    "--output", str(self.root / "runs"), "--max-steps", "5"]
            if stage == "grpo":
                argv += ["--adapter", str(adapter)]
            capture = io.StringIO()
            with patch.object(sys, "argv", argv), contextlib.redirect_stdout(capture):
                runpy.run_path(launcher, run_name="__main__")
            self.assertIn("NPROC_PER_NODE=4", capture.getvalue())
            self.assertIn("--freeze_vit false", capture.getvalue())
            if stage == "grpo":
                self.assertIn("--use_vllm false", capture.getvalue())
                self.assertIn("--remove_unused_columns false", capture.getvalue())

    def test_inference_no_target_leak_and_resume(self):
        prepare(self.config)
        tasks = self.root / "prepared" / "benchmark_tasks.jsonl"
        seen = []
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                seen.append(payload)
                body = dumps({"choices": [{"message": {"content": "test prediction"}, "finish_reason": "stop"}]}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            def log_message(self, *args):
                pass
        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            endpoint = f"http://127.0.0.1:{server.server_port}/v1"
            output = self.root / "predictions.jsonl"
            predict(tasks, output, endpoint, "bank-ocr", "base-v1")
            n = len(seen)
            predict(tasks, output, endpoint, "bank-ocr", "base-v1")
            self.assertEqual(len(seen), n)
            for request in seen:
                self.assertNotIn("target_text", request)
                self.assertNotIn("ocr_items", request)
                self.assertEqual(len(request["messages"]), 1)
            self.assertNotIn("USD 123.45", seen[0]["messages"][0]["content"][0]["text"])
            with self.assertRaisesRegex(ValueError, "changed"):
                predict(tasks, output, endpoint, "bank-ocr", "sft-v1")
            with self.assertRaisesRegex(ValueError, "changed"):
                predict(tasks, output, endpoint, "bank-ocr", "base-v1", temperature=0.5)
            with self.assertRaisesRegex(ValueError, "changed"):
                predict(tasks, output, endpoint, "bank-ocr", "base-v1", request_options={"top_p": 0.9})
            configured_output = self.root / "configured.jsonl"
            predict(tasks, configured_output, endpoint, "bank-ocr", "sft-configured", max_tokens=128,
                    temperature=0.5, enable_thinking=True, request_options={"top_p": 0.9})
            self.assertEqual(seen[-1]["temperature"], 0.5)
            self.assertEqual(seen[-1]["max_tokens"], 128)
            self.assertEqual(seen[-1]["top_p"], 0.9)
            self.assertTrue(seen[-1]["chat_template_kwargs"]["enable_thinking"])
            self.assertEqual(read_json(str(configured_output) + ".meta.json")["request_options"], {"top_p": 0.9})
            with self.assertRaisesRegex(ValueError, "reserved"):
                predict(tasks, self.root / "bad.jsonl", endpoint, "bank-ocr", "bad",
                        request_options={"messages": []})
            self.assertEqual(len(index_predictions(output)), n)
        finally:
            server.shutdown()
            thread.join()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
