"""Banking-task stage: data preparation from docgen folders, reward, mining, report.
Needs the docgen code (scorers): DOCGEN_ROOT=<folder with docgen/>; skipped without it."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from bank_ocr.data import read_json, read_jsonl, write_json

DOCGEN = os.environ.get("DOCGEN_ROOT")
if DOCGEN and DOCGEN not in sys.path:
    sys.path.insert(0, DOCGEN)


def _item(task, key, **kw):
    """Benchmark-format item (docgen) with a valid answer for its scorer."""
    base = {"cross_check": {"answer": {"consistent": False, "issues": [
                {"document": "대출거래신청서", "field": "성명", "value": "김나무", "expected": "김나우"}]},
                            "eval": {"documents": ["대출거래신청서", "주민등록증"]}, "meta": {"category": "typo"}},
            "review": {"answer": "75.5", "eval": {"answer_type": "number", "tol": 0.05}, "meta": {"skill": "계산(비율)"}},
            "doc_check": {"answer": {"missing": ["재직증명서"], "not_required": [], "not_customer": []},
                          "eval": {"required": ["주민등록증", "재직증명서"], "names": ["주민등록증", "재직증명서"]},
                          "meta": {"n_missing": 1}},
            "kie": {"answer": {"name": "김나우"}, "eval": {"fields": {"name": {"type": "text", "norm": "김나우"}}},
                    "meta": {"group": "bank_form"}}}[task]
    return {"id": f"{task}/{key}/x" if task in ("cross_check", "review") else f"{task}/{key}", "task": task,
            "prompt": f"{task} 질문", **base, **kw}


def _docgen_folder(root: Path, split, keys, n_images=2, size=(1600, 2260)):
    """A docgen `bench build` output folder with a few items per customer bundle."""
    (root / "tasks").mkdir(parents=True)
    (root / "swift").mkdir()
    (root / "images").mkdir()
    meta = {"version": "1.1", "settings": {}, "counts": {}}
    if split:
        meta["split"] = split
    write_json(root / "meta.json", meta)
    from bank_task.score import oracle

    def swift_record(it):  # what `docgen.bench build --split train` writes to swift/ (without importing its renderer)
        return {"id": it["id"], "task": it["task"], "images": it["images"],
                "messages": [{"role": "user", "content": "<image>" * len(it["images"]) + it["prompt"]},
                             {"role": "assistant", "content": oracle(it)}]}
    items = {}
    for key in keys:
        imgs = []
        for i in range(n_images):
            p = root / "images" / f"{key}_{i}.jpg"
            Image.new("RGB", size, (250, 250, 250)).save(p)
            imgs.append(f"images/{key}_{i}.jpg")
        for task in ("cross_check", "review", "doc_check", "kie"):
            it = _item(task, key, images=imgs if task != "kie" else imgs[:1])
            items.setdefault(task, []).append(it)
    swift = []
    for task, rows in items.items():
        with open(root / "tasks" / f"{task}.jsonl", "w", encoding="utf-8") as f:
            for it in rows:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")
                swift.append(swift_record(it))
    with open(root / "swift" / "all.jsonl", "w", encoding="utf-8") as f:
        for r in swift:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return items


@unittest.skipUnless(DOCGEN, "set DOCGEN_ROOT to the docgen code folder")
class BankTaskTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        model = self.root / "model"
        model.mkdir()
        write_json(model / "config.json", {"vision_config": {"patch_size": 16, "spatial_merge_size": 2}})
        self.model = str(model)

    def tearDown(self):
        self.tmp.cleanup()

    def data_cfg(self, **kw):
        return {"train": [str(self.root / "train")], "benchmark": str(self.root / "bench"),
                "output_dir": str(self.root / "prep"), "val_count": 2, "grpo_holdout": 0.3, "workers": 1, **kw}

    def test_reward_matches_benchmark_scoring_with_partial_credit(self):
        from bank_task.score import oracle, reward
        cc = _item("cross_check", "b1")
        self.assertEqual(reward(oracle(cc), cc), 1.0)
        # says inconsistent but points at the wrong document: half credit
        self.assertEqual(reward('{"consistent": false, "issues": [{"document": "주민등록증", "field": "주소"}]}', cc), 0.5)
        self.assertEqual(reward('{"consistent": true, "issues": []}', cc), 0.0)
        self.assertEqual(reward("모르겠습니다", cc), 0.0)
        self.assertEqual(reward(None, cc), 0.0)
        dc = _item("doc_check", "b1")
        self.assertEqual(reward(oracle(dc), dc), 1.0)
        partial = reward('{"missing": ["재직증명서", "주민등록증"], "not_required": [], "not_customer": []}', dc)
        self.assertTrue(0 < partial < 1)
        rv = _item("review", "b1")
        self.assertEqual(reward("75.5%", rv), 1.0)
        self.assertEqual(reward("80", rv), 0.0)

    def test_prepare_splits_budgets_and_formats(self):
        from bank_task.prepare import prepare
        train_keys = [f"mortgage_{20000000 + i}" for i in range(12)]
        _docgen_folder(self.root / "train", "train", train_keys, n_images=5)
        _docgen_folder(self.root / "bench", None, ["mortgage_2000000", "mortgage_2000001"], n_images=5)
        result = prepare(self.data_cfg(max_image_tokens_per_sample=6000), self.model)
        prep = self.root / "prep"
        done = read_json(prep / "DONE.json")
        self.assertEqual(done["max_image_tokens_per_image"], 3600)
        self.assertEqual(result["benchmark_by_task"], {"cross_check": 2, "doc_check": 2, "kie": 2, "review": 2})

        def tokens(p):
            with Image.open(p) as im:
                return -(-im.size[0] // 32) * -(-im.size[1] // 32)

        sft, grpo, bench = (read_jsonl(prep / f) for f in ("train_sft.jsonl", "train_grpo.jsonl", "benchmark_tasks.jsonl"))
        for rows in (sft, grpo, bench):
            for r in rows:
                self.assertEqual(sum(m["content"].count("<image>") for m in r["messages"]), len(r["images"]))
                self.assertLessEqual(sum(tokens(p) for p in r["images"]), 6000)  # 5 pages share the budget
        self.assertTrue(all(p.endswith(".png") for r in bench + grpo for p in r["images"]))
        # GRPO customers are held out of SFT; the single-image kie keeps full size (1600x2260 fits 3600 tokens)
        from bank_task.prepare import group_key
        grpo_keys = {group_key(r["id"]) for r in grpo}
        self.assertTrue(grpo_keys)
        sft_text = json.dumps(sft, ensure_ascii=False)
        self.assertTrue(all(r["split"] == "train" and json.loads(r["bench_item"])["task"] == r["task"] for r in grpo))
        kie = next(r for r in bench if r["task"] == "kie")
        self.assertEqual(tokens(kie["images"][0]), 50 * 71)
        # packing: kie/cross_check/review/doc_check of one customer do not share image lists except
        # cross_check and review (same 5 pages) -> packed into one conversation
        self.assertTrue(any(len(r["messages"]) == 4 for r in sft))
        self.assertTrue(all(k not in sft_text for k in grpo_keys))
        items = read_jsonl(prep / "benchmark_items.jsonl")
        self.assertTrue(all("images" not in it and "prompt" not in it for it in items))

    def test_prepare_refuses_leaks(self):
        from bank_task.prepare import prepare
        _docgen_folder(self.root / "train", None, ["mortgage_1"], n_images=1)  # a test set listed as training data
        _docgen_folder(self.root / "bench", None, ["mortgage_2"], n_images=1)
        with self.assertRaisesRegex(ValueError, "test set is listed under train"):
            prepare(self.data_cfg(), self.model)
        same = self.root / "same"
        _docgen_folder(same, "train", ["mortgage_2"], n_images=1)  # same customer as the benchmark
        with self.assertRaisesRegex(ValueError, "share a customer"):
            prepare(self.data_cfg(train=[str(same)]), self.model)

    def test_quotas_follow_mix_and_refill(self):
        from bank_task.prepare import quotas
        take = quotas({"a": 100, "b": 5, "c": 100}, {"a": 0.5, "b": 0.5}, 40)
        self.assertEqual(take, {"a": 35, "b": 5})  # b runs short, a takes the rest; c is not in the mix
        self.assertEqual(sum(quotas({"a": 3, "b": 4}, None, 100).values()), 7)

    def test_mine_and_report(self):
        from bank_task.report import build
        from bank_task.score import mine, oracle, score
        items = [_item("cross_check", f"b{i}") for i in range(10)]
        rows = [{"id": it["id"], "split": "train", "task": it["task"], "bench_item": json.dumps(it)} for it in items]
        preds = {it["id"]: oracle(it) if i < 6 else "틀림" for i, it in enumerate(items)}
        chosen, info = mine(rows, preds, count=4, seed=0, hard_fraction=0.5)
        self.assertEqual((len(chosen), info["hard_available"], info["hard_selected"]), (4, 4, len([r for r in chosen if preds[r["id"]] == "틀림"])))
        self.assertGreaterEqual(info["hard_selected"], 2)
        reports = []
        for name, role, good in (("출발", "start", 3), ("SFT", "sft", 8)):
            res = score(items, {it["id"]: oracle(it) if i < good else "x" for i, it in enumerate(items)})
            path = self.root / f"{role}.json"
            write_json(path, {"label": name, "role": role, **res})
            reports.append(path)
        build(reports, self.root / "out" / "benchmark.csv")
        md = (self.root / "out" / "benchmark.md").read_text(encoding="utf-8")
        self.assertIn("| SFT | 80.0 |", md)
        self.assertIn("+50.0", md)
        other = score(items[:5], {})
        write_json(self.root / "other.json", {"label": "다른 세트", **other})
        with self.assertRaisesRegex(ValueError, "different benchmark"):
            build(reports + [self.root / "other.json"], self.root / "out" / "x.csv")


if __name__ == "__main__":
    unittest.main()
