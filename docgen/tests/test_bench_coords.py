"""평가 세트 2.0 좌표 시험: 옮겨 온 좌표 함수가 OCR 과제(docgen/bench/ocr_*)와 같은 값을 내는지, kie·marks 의 값·위치·값+위치 점수."""
import json
import random
import sys
from pathlib import Path

import pytest

from docgen.bench import evaluate as E
from docgen.bench import metrics as M

from docgen.bench import ocr_data as OD  # noqa: E402
from docgen.bench import ocr_metrics as OM  # noqa: E402


def test_ported_functions_match_ocr_tasks():
    rng = random.Random(7)
    for _ in range(2000):
        w, h = rng.randint(50, 3000), rng.randint(50, 3000)
        x0, y0 = rng.uniform(0, w - 1), rng.uniform(0, h - 1)
        box = [x0, y0, rng.uniform(x0 + 0.01, w), rng.uniform(y0 + 0.01, h)]
        assert M.normalize_box(box, w, h) == OD.normalize_box(box, w, h)
        a = M.normalize_box(box, w, h)
        b = [max(0, a[0] - rng.randint(0, 30)), a[1], min(1000, a[2] + rng.randint(0, 30)), a[3]]
        assert M.iou(a, b) == OM.iou(a, b)
        assert M.valid_box(b) == OM.valid_box(b)
    preds = [{"bbox_2d": [rng.randint(0, 500), rng.randint(0, 500), 600 + rng.randint(0, 300), 600 + rng.randint(0, 300)]} for _ in range(8)]
    gts = [{"bbox_2d": [rng.randint(0, 500), rng.randint(0, 500), 600 + rng.randint(0, 300), 600 + rng.randint(0, 300)]} for _ in range(6)]
    acc = lambda p, g, v: v >= 0.3  # noqa: E731
    assert M.match(preds, gts, acc) == OM.match(preds, gts, acc)


def test_normalize_box_clips_outside():
    assert M.normalize_box([-5, -5, 50, 50], 100, 100) == [0, 0, 500, 500]


def _kie():
    return {"id": "kie/x", "task": "kie", "images": ["a.jpg"], "meta": {},
            "answer": [{"key": "name", "value": "김나우", "bbox_2d": [100, 100, 300, 140], "page": 1},
                       {"key": "amount", "value": "56,000,000", "bbox_2d": [100, 200, 300, 240], "page": 1},
                       {"key": "memo", "value": None}],
            "eval": {"fields": {"name": {"type": "text"}, "amount": {"type": "amount", "norm": 56000000}, "memo": {"type": "text"}}}}


def test_kie_value_location_scores():
    it = _kie()
    perfect = json.dumps(it["answer"], ensure_ascii=False)
    m = E.s_kie(it, perfect)["metrics"]
    assert m["f1"] == m["loc_f1"] == m["vl_f1"] == 1.0
    moved = [dict(a) for a in it["answer"]]
    moved[0]["bbox_2d"] = [600, 600, 800, 640]
    m = E.s_kie(it, json.dumps(moved, ensure_ascii=False))["metrics"]
    assert m["f1"] == 1.0 and m["loc_f1"] == m["vl_f1"] == 0.5
    wrong_page = [dict(a) for a in it["answer"]]
    wrong_page[1]["page"] = 2
    assert E.s_kie(it, json.dumps(wrong_page, ensure_ascii=False))["metrics"]["loc_f1"] == 0.5
    values_only = '{"name": "김나우", "amount": "56000000원", "memo": null}'   # 위치를 못 내는 모델도 값 점수는 받는다
    m = E.s_kie(it, values_only)["metrics"]
    assert m["f1"] == 1.0 and m["loc_f1"] == 0.0 and m["vl_f1"] == 0.0
    wrong_value = [dict(a) for a in it["answer"]]
    wrong_value[0]["value"] = "김나무"
    m = E.s_kie(it, json.dumps(wrong_value, ensure_ascii=False))["metrics"]
    assert m["loc_f1"] == 1.0 and m["vl_f1"] == 0.5


def test_marks_value_location_scores():
    it = {"id": "marks/x", "task": "marks", "images": ["a.jpg"], "meta": {},
          "answer": [{"key": "rate", "value": "변동", "bbox_2d": [10, 10, 20, 20], "page": 1},
                     {"key": "multi", "value": "A", "bbox_2d": [30, 10, 40, 20], "page": 1},
                     {"key": "multi", "value": "C", "bbox_2d": [50, 10, 60, 20], "page": 1},
                     {"key": "seal.a", "value": True, "bbox_2d": [700, 700, 800, 800], "page": 1},
                     {"key": "sign.b", "value": False}],
          "eval": {"types": {"rate": "checkbox", "multi": "checkbox_multi", "seal.a": "seal", "sign.b": "signature"}}}
    m = E.s_marks(it, json.dumps(it["answer"], ensure_ascii=False))["metrics"]
    assert m["acc"] == m["loc_f1"] == m["vl_f1"] == 1.0
    vo = '{"rate": "변동", "multi": ["C", "A"], "seal.a": "예", "sign.b": false}'
    m = E.s_marks(it, vo)["metrics"]
    assert m["acc"] == 1.0 and m["vl_f1"] == 0.0


def test_main_metric_by_version():
    assert E.main_metric("kie", {"f1": 1, "vl_f1": 1}) == "vl_f1"
    assert E.main_metric("kie", {"f1": 1}) == "f1"   # 1.x 세트
    assert E.main_metric("marks", {"acc": 1}) == "acc"
    old = {"id": "kie/o", "task": "kie", "images": [], "meta": {}, "answer": {"a": "x"}, "eval": {"fields": {"a": {"type": "text"}}}}
    assert E.score_task("kie", [old], {"kie/o": '{"a": "x"}'})["main"] == "f1"


def test_swift_marks_record_matches_eval_shape():
    from docgen.swift import build_records

    label = {"id": "x", "doc_name": "서류", "gt": {}, "fields": [
        {"key": "rate", "type": "checkbox", "value": "변동", "page": 0,
         "options": [{"text": "고정", "checked": False, "box_bbox": [0, 0, 10, 10]}, {"text": "변동", "checked": True, "box_bbox": [20, 0, 30, 10]}]},
        {"key": "seal.a", "type": "seal", "value": "김", "present": True, "page": 0, "bbox": [50, 50, 90, 90]},
        {"key": "sign.b", "type": "signature", "value": None, "present": False, "page": 0, "bbox": [0, 80, 10, 90]},
        {"key": "name", "type": "text", "value": "김", "page": 0, "bbox": [0, 20, 40, 30], "label": "성명"}]}
    recs = {r["task"]: r for r in build_records(label, ["a.png"], [(100, 100)], random.Random(0), ("grounding", "marks"))}
    marks = json.loads(recs["marks"]["messages"][1]["content"])
    assert marks == [{"key": "rate", "value": "변동", "bbox_2d": [200, 0, 300, 100], "page": 1},
                     {"key": "seal.a", "value": True, "bbox_2d": [500, 500, 900, 900], "page": 1},
                     {"key": "sign.b", "value": False}]
    ground = json.loads(recs["grounding"]["messages"][1]["content"])
    assert ground == [{"key": "name", "label": "성명", "value": "김", "bbox_2d": [0, 200, 400, 300], "page": 1}]


@pytest.mark.parametrize("seed", range(4))
def test_health_insurance_installment_follows_switch(seed, monkeypatch):
    """2.0 에서 고친 것: 정산 분할납부는 special 스위치를 따른다 (끄면 '정산 분할' 비고가 없다)."""
    from docgen.entities import make_profile
    from docgen.registry import load_all

    monkeypatch.setenv("DOCGEN_SPECIAL", "none")
    d = load_all()["health_insurance_payment"].generate(make_profile(seed), random.Random(seed))
    assert not any("정산 분할" in str(r.get("note") or "") for r in d["rows"])
