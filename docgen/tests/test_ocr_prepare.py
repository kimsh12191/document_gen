"""OCR 문항 만들기(docgen/bench/ocr_*): 사내 OCR 응답 읽기·나누기·채점/보상·쪽 그림 변형·과제 만들기·준비 전체 (studio/DESIGN.md 17절).
옛 1부 ocr/tests/test_pipeline.py 에서 옮김 (학습·답 내기·골라 뽑기 시험은 train/tests)."""
import json
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageDraw

from docgen.bench.ocr_augment import make_view
from docgen.bench.ocr_data import assign_splits, canonical_image, dumps, parse_ocr, read_json, read_jsonl, scan, write_json, write_jsonl
from docgen.bench.ocr_metrics import answer_for, evaluate, iou, numbers, parse_boxes, reward
from docgen.bench.ocr_prepare import prepare
from docgen.bench.ocr_tasks import MARKERS, build_view, grounding_tasks, marked_tasks, region_tasks, relation_tasks, spotting_tasks
from docgen.tests.ocr_fixture import create_demo, ocr_from_file


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
        raw = read_json(Path(__file__).parent / "data" / "ocr-response.json")
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


def box(x1, y1, x2, y2, label=""):
    return {"bbox_2d": [x1, y1, x2, y2], "label": label}


class MetricTests(unittest.TestCase):
    def test_box_list_format(self):
        self.assertEqual(parse_boxes('[{"bbox_2d":[0,0,20,20],"label":"A"}]'), [box(0, 0, 20, 20, "A")])
        self.assertEqual(parse_boxes('```json\n[{"bbox_2d":[0,0,20,20]}]\n```'), [box(0, 0, 20, 20)])
        self.assertEqual(parse_boxes("[]"), [])
        for bad in ['[{"bbox_2d":[true,0,20,20]}]', '[{"bbox_2d":[0,0,NaN,20]}]', '[{"bbox_2d":[0,0,1001,20]}]',
                    '[{"bbox_2d":[1,1,1,4]}]', '[{"bbox":[0,0,20,20]}]', 'not json', '[{"bbox_2d":[0,0,20,20],"label":3}]']:
            self.assertIsNone(parse_boxes(bad))

    def test_numeric_tokens_do_not_collapse(self):
        self.assertNotEqual(numbers("12 34"), numbers("1234"))
        self.assertNotEqual(numbers("123.45"), numbers("123,45"))
        self.assertLess(reward("USD 123.4O", "bbox_ocr", {"text": "USD 123.40"}), 1)
        self.assertEqual(reward("한글", "crop_ocr", {"text": "한글"}), 1)

    def test_box_reward_soft_f1(self):
        gold = {"boxes": [box(100, 100, 300, 130, "USD 12"), box(600, 100, 800, 130, "USD 12")]}
        exact = reward(answer_for("grounding", gold), "grounding", gold)
        self.assertEqual(exact, 1)
        one = reward(dumps([box(100, 100, 300, 130)]), "grounding", gold)
        extra = reward(dumps([box(100, 100, 300, 130), box(600, 100, 800, 130), box(0, 0, 50, 50)]), "grounding", gold)
        self.assertAlmostEqual(one, 2 / 3)
        self.assertAlmostEqual(extra, 0.8)
        # IoU above 0.8 is not pushed further toward the teacher's exact box edges.
        loose = reward(dumps([box(100, 100, 300, 136), box(600, 100, 800, 130)]), "grounding", gold)
        self.assertEqual(loose, 1)
        self.assertEqual(reward(dumps([box(0, 0, 1000, 1000)]), "grounding", {"boxes": [box(100, 100, 300, 130)]}) < 0.1, True)
        self.assertEqual(reward("not json", "grounding", gold), 0)
        self.assertEqual(reward("[]", "grounding", {"boxes": []}), 1)
        self.assertEqual(reward(dumps([box(1, 1, 5, 5)]), "grounding", {"boxes": []}), 0)
        spot = {"boxes": [box(10, 10, 100, 40, "성명")]}
        self.assertEqual(reward(dumps([box(10, 10, 100, 40, "성명")]), "spotting", spot), 1)
        self.assertAlmostEqual(reward(dumps([box(10, 10, 100, 40, "성멍")]), "spotting", spot), 0.75)

    def test_box_metrics(self):
        rows = [{"id": "a", "task": "spotting", "view": "clean", "target": dumps({"boxes": [box(0, 0, 100, 100, "A"), box(200, 0, 300, 100, "B")]})},
                {"id": "b", "task": "grounding", "view": "aug", "target": dumps({"boxes": []})},
                {"id": "c", "task": "grounding", "view": "aug", "target": dumps({"boxes": [box(0, 0, 100, 100, "A")]})}]
        preds = {"a": dumps([box(0, 0, 100, 100, "A"), box(200, 0, 300, 100, "X")]), "b": "[]", "c": dumps([box(0, 0, 100, 100, "A"), box(500, 500, 600, 600, "A")])}
        result = evaluate(rows, preds)
        spot, ground = result["tasks"]["spotting"], result["tasks"]["grounding"]
        self.assertEqual(spot["f1_iou50"], 1)
        self.assertEqual(spot["e2e_f1"], 0.5)
        self.assertEqual(ground["negative_accuracy"], 1)
        self.assertEqual(ground["precision_iou50"], 0.5)
        self.assertEqual(ground["recall_iou50"], 1)
        self.assertEqual(set(result["breakdown"]["view"]), {"clean", "aug"})

class AugmentTests(unittest.TestCase):
    def test_boxes_follow_geometric_augmentation(self):
        boxes = [[40 + gx * 300, 40 + gy * 140, 240 + gx * 300, 90 + gy * 140] for gx in range(6) for gy in range(18)]
        page = Image.new("RGB", (1900, 2600), "white")
        draw = ImageDraw.Draw(page)
        for b in boxes:
            draw.rectangle(b, fill="black")
        items = [{"text": str(i), "confidence": 1, "order": i, "line_num": None, "usable": True} for i in range(len(boxes))]
        aug = {"crop_probability": 1, "rotate_probability": 1, "pad_probability": 1, "photometric_ops": [0, 0]}
        checked = 0
        for seed in range(6):
            im, envelopes, fractions, ops = make_view(page, boxes, random.Random(seed), [1150, 800], aug)
            self.assertLessEqual(max(im.size), 1150)
            self.assertLessEqual(min(im.size), 800)
            view = build_view("v.png", im.size, items, envelopes, fractions, "aug", ops, "v")
            dark = im.convert("L").point(lambda v: 255 if v < 40 else 0)
            for item in view["items"]:
                if item["cut"]:
                    self.assertFalse(item["usable"])
                    continue
                x1, y1, x2, y2 = item["px"]
                area = (max(0, int(x1) - 8), max(0, int(y1) - 8), min(im.width, int(x2) + 8), min(im.height, int(y2) + 8))
                found = dark.crop(area).getbbox()
                self.assertIsNotNone(found, ops)
                actual = [found[0] + area[0], found[1] + area[1], found[2] + area[0], found[3] + area[1]]
                self.assertGreater(iou(actual, item["px"]), 0.85, ops)
                checked += 1
        self.assertGreater(checked, 100)

    def test_clean_view_fits_input_size(self):
        im, envelopes, fractions, ops = make_view(Image.new("RGB", (2480, 3508)), [[0, 0, 2480, 3508]], random.Random(0), [2300, 1600])
        self.assertEqual(im.size, (1600, 2263))
        self.assertEqual(fractions, [1.0])
        self.assertEqual([round(v) for v in envelopes[0]], [0, 0, 1600, 2263])


class TaskTests(unittest.TestCase):
    PAGE = {"document_id": "d", "page_id": "p", "split": "train"}

    def view(self, words):
        items = [{"text": t, "confidence": c, "order": n, "line_num": line, "usable": c >= 0.95}
                 for n, (t, _, c, line) in enumerate(words)]
        envelopes = [b for _, b, _, _ in words]
        return build_view("v.png", (1000, 1000), items, envelopes, [1.0] * len(words), "clean", [], "v")

    def test_grounding_lists_all_occurrences_and_negatives(self):
        view = self.view([("DATE", [10, 10, 60, 30], 0.99, 0), ("DATE", [500, 10, 560, 30], 0.99, 0), ("LOW", [10, 100, 60, 120], 0.5, 1)])
        rows = grounding_tasks(view, self.PAGE, random.Random(0), 5, 0.5, ["ABSENT"])
        targets = {json.loads(r["target"])["boxes"].__len__() for r in rows}
        self.assertEqual(targets, {2, 0})  # DATE twice, a negative; LOW is never a query
        self.assertFalse(any('"LOW"' in r["messages"][0]["content"] for r in rows))

    def test_region_rejects_untrusted_words(self):
        clean = self.view([("A", [10, 10, 60, 30], 0.99, 0), ("B", [70, 10, 120, 30], 0.99, 0), ("C", [10, 40, 60, 60], 0.99, 1)])
        rows = region_tasks(clean, self.PAGE, random.Random(0), 3)
        self.assertTrue(rows)
        texts = {json.loads(r["target"])["text"] for r in rows}
        self.assertIn("A B\nC", texts)
        # Reading order follows geometry, not the OCR's output order.
        shuffled = self.view([("C", [10, 40, 60, 60], 0.99, 1), ("B", [70, 10, 120, 30], 0.99, 0), ("A", [10, 12, 60, 31], 0.99, 0)])
        self.assertIn("A B\nC", {json.loads(r["target"])["text"] for r in region_tasks(shuffled, self.PAGE, random.Random(0), 3)})
        noisy = self.view([("A", [10, 10, 60, 30], 0.99, 0), ("B", [70, 10, 120, 30], 0.3, 0)])
        self.assertEqual(region_tasks(noisy, self.PAGE, random.Random(0), 3), [])

    def test_prompts_are_fully_formatted(self):
        view = self.view([("A", [10, 10, 60, 30], 0.99, 0), ("B", [70, 10, 120, 30], 0.99, 0)])
        im = Image.new("RGB", (1000, 1000), "white")
        with tempfile.TemporaryDirectory() as d:
            rows = spotting_tasks(view, self.PAGE, random.Random(0), 2, im, Path(d), 40)
        self.assertTrue(rows)
        for r in rows:
            self.assertNotIn("{{", r["messages"][0]["content"])

    def test_spotting_masks_untrusted_words(self):
        view = self.view([("A", [10, 10, 60, 30], 0.99, 0), ("LOW", [70, 10, 120, 30], 0.3, 0)])
        im = Image.new("RGB", (1000, 1000), "white")
        for x in range(74, 118, 8):  # stroke-like marks, a minority of the word box like real text
            ImageDraw.Draw(im).line([x, 13, x + 3, 27], fill="black", width=2)
        with tempfile.TemporaryDirectory() as d:
            rows = spotting_tasks(view, self.PAGE, random.Random(0), 1, im, Path(d), 40)
            self.assertEqual(len(rows), 1)
            self.assertEqual([b["label"] for b in json.loads(rows[0]["target"])["boxes"]], ["A"])
            self.assertEqual(rows[0]["masked_words"], 1)
            with Image.open(rows[0]["images"][0]) as tile:
                self.assertEqual(tile.convert("L").getextrema(), (255, 255))  # the untrusted word is gone

    def test_marked_boxes_are_drawn_where_the_answer_says(self):
        words = [("성명", [100, 100, 200, 130], 0.99, 0), ("홍길동", [400, 100, 520, 130], 0.99, 0),
                 ("주소", [100, 400, 200, 430], 0.99, 1), ("LOW", [400, 400, 500, 430], 0.3, 1),
                 ("붙은", [600, 100, 700, 130], 0.99, 0), ("단어", [702, 100, 800, 130], 0.99, 0)]
        view = self.view(words)
        im = Image.new("RGB", (1000, 1000), "white")
        with tempfile.TemporaryDirectory() as d:
            rows = marked_tasks(view, self.PAGE, random.Random(0), 3, 3, im, Path(d))
            self.assertEqual(sorted(r["task"] for r in rows), ["marked_box"] * 3 + ["marked_ocr"] * 3)
            with Image.open(rows[0]["images"][0]) as marked:
                marked = marked.convert("RGB")
            colours = {c: rgb for c, _, rgb in MARKERS}
            for r in rows:
                self.assertNotIn("{", r["messages"][0]["content"].replace("[{", "").replace('{"bbox_2d"', ""))
                if r["task"] != "marked_box":
                    continue
                entry = json.loads(r["target"])["boxes"][0]
                # LOW (untrusted) and words whose box would touch a neighbour are never marked.
                self.assertIn(entry["label"], {"성명", "홍길동", "주소"})
                prompt = r["messages"][0]["content"]
                colour = next(en for en, ko, _ in MARKERS if f" {en} box" in prompt or f"{ko} 박스" in prompt)
                x1, y1, x2, y2 = entry["bbox_2d"]
                self.assertEqual(marked.getpixel((x1, (y1 + y2) // 2)), colours[colour])
                self.assertEqual(marked.getpixel(((x1 + x2) // 2, y2 - 1)), colours[colour])
                self.assertEqual(marked.getpixel(((x1 + x2) // 2, (y1 + y2) // 2)), (255, 255, 255))  # word not covered

    def test_relation_requires_unambiguous_trusted_neighbour(self):
        view = self.view([("성명", [10, 10, 60, 30], 0.99, 0), ("홍길동", [80, 10, 160, 30], 0.99, 0)])
        rows = relation_tasks(view, self.PAGE, random.Random(0), 20)
        answers = {(r["messages"][0]["content"], json.loads(r["target"])["boxes"][0]["label"]) for r in rows}
        self.assertTrue(any(label == "홍길동" for _, label in answers))
        low = self.view([("성명", [10, 10, 60, 30], 0.99, 0), ("홍길동", [80, 10, 160, 30], 0.4, 0)])
        self.assertEqual(relation_tasks(low, self.PAGE, random.Random(0), 20), [])


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
        self.assertEqual(summary["benchmark_view_counts"].keys(), {"clean", "aug"})
        rows = read_jsonl(out / "benchmark_tasks.jsonl")
        self.assertEqual(len({r["id"] for r in rows}), len(rows))
        clean_grounding = [json.loads(r["target"]) for r in rows if r["task"] == "grounding" and r["view"] == "clean"]
        self.assertIn(2, [len(t["boxes"]) for t in clean_grounding])  # "DATE" appears twice
        for image in {i for r in rows for i in r["images"]}:
            with Image.open(image) as im:
                self.assertLessEqual(max(im.size), 2300)
        for r in read_jsonl(out / "train_grpo.jsonl"):
            self.assertEqual(len(r["messages"]), 1)
            self.assertEqual(r["split"], "train")
            self.assertIn(r["task"], ("grounding", "spotting", "relation"))
        sft_rows = read_jsonl(out / "train_sft.jsonl")
        for r in sft_rows:
            self.assertEqual(r["messages"][-1]["role"], "assistant")
        self.assertEqual(sum(len(r["messages"]) // 2 for r in sft_rows), summary["sft_examples"])
        self.assertLess(summary["sft_samples"], summary["sft_examples"])
        oracle = {r["id"]: answer_for(r["task"], r["target"]) for r in rows}
        metrics = evaluate(rows, oracle)
        self.assertEqual(metrics["tasks"]["crop_ocr"]["cer"], 0)
        self.assertEqual(metrics["tasks"]["grounding"]["f1_iou50"], 1)
        self.assertEqual(metrics["tasks"]["spotting"]["e2e_f1"], 1)
        with self.assertRaises(ValueError):
            evaluate(rows, {})
        with self.assertRaisesRegex(ValueError, "Output already exists"):
            prepare(self.config)
        cfg = read_json(self.config)
        cfg["output_dir"] = "prepared2"
        write_json(self.config, cfg)
        with patch("docgen.tests.ocr_fixture.ocr_from_file", side_effect=AssertionError("Cache should be reused")):
            prepare(self.config)
        # 과제 형식 (docgen-tasks/1): 같은 문항이 tasks/<과제>.jsonl 에, 정답은 target 을 푼 것, 그림은 준비 폴더 기준 상대 경로
        meta = read_json(out / "meta.json")
        self.assertEqual(meta["format"], "docgen-tasks/1")
        self.assertEqual(sum(meta["counts"].values()), sum(meta["split_counts"].values()))
        items = {i["id"]: i for t in meta["counts"] for i in read_jsonl(out / "tasks" / f"{t}.jsonl")}
        for r in rows:
            it = items[r["id"]]
            self.assertEqual(it["answer"], json.loads(r["target"]))
            self.assertEqual(it["meta"]["split"], "benchmark")
            self.assertTrue((out / it["images"][0]).is_file() and not Path(it["images"][0]).is_absolute())
            self.assertNotIn("<image>", it["prompt"])
        key = lambda r: (r["id"], r["target"], r["messages"][0]["content"], r["view_ops"])
        self.assertEqual([key(r) for r in read_jsonl(self.root / "prepared2" / "benchmark_tasks.jsonl")], [key(r) for r in rows])

    def test_saved_ocr_json_skips_the_adapter(self):
        ocr_dir = self.root / "ocr"
        ocr_dir.mkdir()
        for idx in range(4):
            write_json(ocr_dir / f"document_{idx}.json", ocr_from_file(f"document_{idx}.png"))
        rows = scan(self.root, "train", single_page=True, ocr_dir=ocr_dir)
        self.assertTrue(all(r["ocr_json"].endswith(".json") for r in rows))
        write_jsonl(self.root / "manifest.jsonl", rows)
        cfg = read_json(self.config)
        cfg.update(benchmark_fraction=0.25, ocr_callable="no_such_module:never_called")
        write_json(self.config, cfg)
        summary = prepare(self.config)
        self.assertEqual(summary["page_counts"], {"train": 2, "val": 1, "benchmark": 1})
        with self.assertRaisesRegex(ValueError, "No saved OCR JSON"):
            scan(self.root, "train", single_page=True, ocr_dir=self.root / "prepared")

    def test_obsolete_config_key_rejected(self):
        cfg = read_json(self.config)
        cfg["train_regions_per_page"] = 0
        write_json(self.config, cfg)
        with self.assertRaisesRegex(ValueError, "tasks_per_view"):
            prepare(self.config)

    def test_duplicate_pixels_fail_before_ocr(self):
        manifest = read_jsonl(self.root / "manifest.jsonl")
        manifest[-1]["image"] = manifest[0]["image"]
        write_jsonl(self.root / "manifest.jsonl", manifest)
        with patch("docgen.tests.ocr_fixture.ocr_from_file", side_effect=AssertionError("No OCR during preflight")):
            with self.assertRaisesRegex(ValueError, "Duplicate image leakage"):
                prepare(self.config)

    def test_failure_does_not_poison_cache(self):
        with patch("docgen.tests.ocr_fixture.ocr_from_file", return_value={"success": "N"}):
            with self.assertRaises(ValueError):
                prepare(self.config)
        self.assertEqual(list((self.root / "cache" / "ocr").glob("*.json")), [])
        prepare(self.config)

if __name__ == "__main__":
    unittest.main()
