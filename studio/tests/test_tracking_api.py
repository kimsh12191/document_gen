"""실제 데이터셋으로 구성·필터·채점 API 계약을 확인한다. 사용자 등록부는 사용하지 않는다."""
import json

import pytest
from fastapi import HTTPException

from docgen.bench.runner import oracle_output
from studio import api_datasets, datasets as DS


@pytest.fixture
def tracking_api(tmp_path):
    root = tmp_path / "benchmark"
    (root / "tasks").mkdir(parents=True)
    rows = [
        {"id": "ocr-train", "task": "crop_ocr", "answer": {"text": "abc"}, "meta": {"split": "train"}},
        {"id": "ocr-test", "task": "crop_ocr", "answer": {"text": "abc"}, "meta": {"split": "benchmark", "doc_type": "employment_certificate"}},
        *[{"id": f"review-{s}", "task": "review", "answer": "예", "eval": {"answer_type": "yesno", "tol": 0},
           "meta": {"split": "benchmark", "scenario": s, "skill": "test"}} for s in ("mortgage", "jeonse_loan")],
        {"id": "kie", "task": "kie", "answer": {"name": "Alice"}, "eval": {"fields": {"name": {"type": "text", "kind": "name"}}},
         "meta": {"split": "benchmark", "group": "income", "condition": "clean"}},
    ]
    for task in {r["task"] for r in rows}:
        (root / "tasks" / f"{task}.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows if r["task"] == task), encoding="utf-8")
    (root / "meta.json").write_text(json.dumps({"version": "3.0", "split": "mixed", "counts": {"crop_ocr": 2, "review": 2, "kie": 1}}), encoding="utf-8")
    reg = DS.Registry(tmp_path / "workspace")
    ds = reg.register(str(root))
    router = api_datasets.make_router(reg, lambda fn, *a, **kw: fn(*a, **kw))
    endpoints = {(method, route.path): route.endpoint for route in router.routes for method in route.methods}
    result = DS.score(ds, {r["id"]: oracle_output(r) for r in rows})
    path = reg.ws / "scores" / ds["id"]
    path.mkdir(parents=True)
    (path / "model.json").write_text(json.dumps({"pid": "model", "label": "model", **result}), encoding="utf-8")
    (path / "legacy.json").write_text(json.dumps({"pid": "legacy", "tasks": {}}), encoding="utf-8")
    return endpoints, ds


def test_composition_filters_and_evaluation_scope(tracking_api):
    api, ds = tracking_api
    summary = api["GET", "/api/datasets/{ds_id}/composition"](ds["id"])
    assert summary["all"]["n"] == 5 and summary["evaluation"]["n"] == 4
    assert summary["evaluation"]["field_kind_counts"] == {"name": 1}
    lookup = api["GET", "/api/datasets/{ds_id}/items"]
    assert lookup(ds["id"], task="crop_ocr", evaluation_only=True)["total"] == 1
    rows = lookup(ds["id"], scenario="mortgage", task_group="work", label_format="scalar")["items"]
    assert [r["id"] for r in rows] == ["review-mortgage"]


def test_breakdowns_and_legacy_scores(tracking_api):
    api, ds = tracking_api
    lookup = api["GET", "/api/datasets/{ds_id}/breakdowns"]
    data = lookup(ds["id"], "model")
    assert data["available"]
    assert data["breakdowns"]["task_group"]["work"]["n"] == 2
    assert data["tasks"]["kie"]["slices"]["kind"]["name"] == {"n": 1, "acc": 1.0}
    assert not lookup(ds["id"], "legacy")["available"]
    with pytest.raises(HTTPException) as exc:
        lookup(ds["id"], "../model")
    assert exc.value.status_code == 404
