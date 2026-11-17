"""studio 데이터셋 시험: 레시피 기본값·덮어쓰기, 레시피 검사, 작업, 등록."""
import argparse
import json
import sys
import time

import pytest

from docgen.bench import build as BUILD
from studio import bank_data as BD


def _args(**kw):
    a = argparse.Namespace(types="all", per_doc=1, fields_per_doc=6, max_keys=40, scale=2.0, start=0, split="test")
    for k, v in kw.items():
        setattr(a, k, v)
    return a


def test_empty_recipe_keeps_defaults(tmp_path):
    f = tmp_path / "r.json"
    f.write_text("{}", encoding="utf-8")
    a = _args()
    rc = BUILD.load_recipe(f, a)
    assert (a.types, a.per_doc, a.split) == ("all", 1, "test")
    assert rc["rules"] == {"conditions": None, "exclude": [], "nulls": {}}
    assert rc["exclude"] == set() and rc["reviewed_only"] is False


def test_recipe_overrides(tmp_path):
    f = tmp_path / "r.json"
    f.write_text(json.dumps({"split": "train", "types": ["resident_id_card", "hf169"], "per_doc": 3, "conditions": {"clean": 1.0},
                             "exclude": ["hf001"], "nulls": {"blank": 0.2}, "page_view": 0.3, "reviewed_only": True}), encoding="utf-8")
    a = _args()
    rc = BUILD.load_recipe(f, a)
    assert a.split == "train" and a.types == "resident_id_card,hf169" and a.per_doc == 3
    assert rc["rules"] == {"conditions": [("clean", 1.0)], "exclude": ["hf001"], "nulls": {"blank": 0.2}, "page_view": 0.3}
    assert rc["reviewed_only"] is True
    for bad in ({"nope": 1}, {"scenarios": ["mortgage"]}, {"conditions": {"clean": 0.5}}, {"page_view": 2}, {"nulls": {"x": 0.1}}):
        g = tmp_path / "bad.json"
        g.write_text(json.dumps(bad), encoding="utf-8")
        with pytest.raises(SystemExit):
            BUILD.load_recipe(g, _args())


def test_pick_condition_default_unchanged():
    keys = [f"k{i}" for i in range(200)]
    assert [BUILD.pick_condition(k) for k in keys] == [BUILD.pick_condition(k, BUILD.CONDITIONS) for k in keys]


def test_validate_recipe():
    BD.validate_recipe(BD.TEMPLATES["bank-try"])
    with pytest.raises(ValueError):
        BD.validate_recipe({"types": ["no_such_form"]})
    with pytest.raises(ValueError):
        BD.validate_recipe({"conditions": {"clean": 0.5}})
    with pytest.raises(ValueError):
        BD.validate_recipe({"cases": {"nope": {"enabled": False}}})
    with pytest.raises(ValueError):
        BD.validate_recipe({"custom_bundles": [{"scenario": "nope"}]})


def _bench(tmp_path, name, split, split_counts=None):
    root = tmp_path / name
    (root / "tasks").mkdir(parents=True)
    (root / "tasks" / "classify.jsonl").write_text('{"id": "c", "task": "classify", "answer": "x"}\n', encoding="utf-8")
    meta = {"version": "1.2", "split": split, "counts": {"classify": 1}}
    if split_counts:
        meta.update(kind="ocr", split_counts=split_counts, counts={"crop_ocr": 1})
        (root / "tasks" / "classify.jsonl").rename(root / "tasks" / "crop_ocr.jsonl")
    (root / "meta.json").write_text(json.dumps(meta), encoding="utf-8")
    return root


def test_jobs_run_and_on_done(tmp_path):
    from studio.jobs import Jobs

    jobs = Jobs(tmp_path, tmp_path)
    j = jobs.start("t", "시험", [sys.executable, "-c", "import sys; print('1/2'); print('2/2')"], on_done=lambda job: {"ok": 1})
    for _ in range(300):
        if jobs.get(j["id"])["status"] != "running":
            break
        time.sleep(0.1)
    got = jobs.get(j["id"])
    assert got["status"] == "done" and got["result"] == {"ok": 1} and "2/2" in got["log_tail"]


