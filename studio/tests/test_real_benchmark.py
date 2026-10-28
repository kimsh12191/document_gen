"""실문서의 사용자 정의 키 → 추론 → 검수 → 고정 평가 세트 (OCR/VLM 서버 없이)."""
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi import HTTPException
from PIL import Image

from docgen.bench.runner import oracle_output
from studio import api_real_benchmark as API, datasets as DS, importer as IM, real_benchmark as RB


@pytest.fixture
def work(tmp_path):
    ws, real = tmp_path / "workspace", tmp_path / "real"
    src = tmp_path / "images"
    src.mkdir()
    for n in ("a.png", "b.png"):
        Image.new("RGB", (1000, 1400), "white").save(src / n)
    batch = IM.create_batch(ws, "실문서", str(src))
    d = ws / "imports" / batch["name"]
    rows = IM._jsonl(d / "pages.jsonl")
    for row in rows:
        row.update(width=1000, height=1400, image=row["source"])
    IM._write_jsonl(d / "pages.jsonl", rows)
    RB.write(d / "formats.json", {"formats": [{"id": "f1", "name": "새 신청서", "pages": [r["id"] for r in rows],
              "docs": {r["doc"]: [r["id"]] for r in rows}}], "fixed": {}})
    RB.initialize(d)
    RB.save_schema(d, "f1", "사용자 신청서", [{"key": "applicant", "label": "신청인 성명", "type": "text"},
                   {"key": "signed", "label": "신청인 서명", "type": "signature"}])
    return d, real, DS.Registry(ws)


def prediction(d, doc="a.png"):
    RB.write(RB.prediction_path(d, doc), {"model": "sft-1", "raw": "original response", "prompt": "original prompt",
             "items": [{"key": "applicant", "value": "잘못 읽음", "bbox_2d": [100, 100, 300, 200], "page": 1},
                       {"key": "signed", "value": False}]})


def test_custom_schema_review_and_immutable_benchmark(work):
    d, real, reg = work
    prediction(d)
    doc = RB.load_document(d, real, "a.png")
    assert doc["standard"][1]["type"] == "signature"
    assert doc["fields"][0]["bbox"] == [100, 140, 300, 280]
    doc["fields"][0]["value"] = "김하나"
    RB.save_document(d, real, "a.png", doc["fields"], True, "tester")
    result = RB.finalize(d, real, reg, "실문서 평가", "v1", classify=True)
    root = Path(result["path"])
    assert result["frozen"] and result["gt"] == "reviewed" and result["real_data"]
    assert result["counts"] == {"classify": 1, "kie": 1, "marks": 1}
    items = [json.loads(line) for p in (root / "tasks").glob("*.jsonl") for line in p.read_text(encoding="utf-8").splitlines()]
    score = DS.score(result, {it["id"]: oracle_output(it) for it in items})
    assert score["tasks"]["kie"]["metrics"]["vl_f1"] == 1
    assert score["tasks"]["marks"]["metrics"]["vl_f1"] == 1
    prov = RB.read(next((root / "input/provenance").glob("*.json")))
    assert prov["prediction"]["raw"] == "original response"
    assert prov["review"]["fields"][0]["original"]["value"] == "잘못 읽음"
    assert prov["review"]["fields"][0]["value"] == "김하나"
    frozen = (root / "tasks/kie.jsonl").read_bytes()
    doc["fields"][0]["value"] = "이두리"
    RB.save_document(d, real, "a.png", doc["fields"], False, "tester")
    assert (root / "tasks/kie.jsonl").read_bytes() == frozen
    assert RB.summary(d, real)["done"] == 0
    with pytest.raises(ValueError, match="새 버전"):
        RB.finalize(d, real, reg, "실문서 평가", "v1")


def test_missing_keys_boxes_and_schema_changes(work):
    d, real, _ = work
    with pytest.raises(ValueError, match="모든 항목"):
        RB.save_document(d, real, "a.png", [], True, "tester")
    prediction(d)
    fields = RB.load_document(d, real, "a.png")["fields"]
    fields[0]["bbox"] = None
    with pytest.raises(ValueError, match="위치를"):
        RB.save_document(d, real, "a.png", fields, True, "tester")
    fields[0]["page"] = -1
    with pytest.raises(ValueError, match="쪽 번호"):
        RB.save_document(d, real, "a.png", fields, False, "tester")
    with pytest.raises(ValueError, match="이미 추론"):
        RB.save_schema(d, "f1", "변경", [{"key": "x", "label": "다른 값"}])


def test_model_failure_retry_and_original_response(work, tmp_path):
    d, real, _ = work
    schema = RB.work(d)["schemas"]["f1"]
    request = {"batch_dir": str(d), "provider": "m1", "provider_config": {"model": "bank-sft", "base_url": "http://vlm/v1"},
               "documents": [{"doc": "a.png", "images": [str(tmp_path / "images/a.png")], "schema": schema}],
               "result_path": str(tmp_path / "result.json")}

    class Reply:
        def __init__(self, content): self.content = content
        def __enter__(self): return self
        def __exit__(self, *_): pass
        def read(self): return json.dumps({"choices": [{"message": {"content": self.content}, "finish_reason": "stop"}]}).encode()

    with patch("urllib.request.urlopen", return_value=Reply("not valid json")):
        assert RB.run_inference(request)["failed"] == 1
    assert not RB.prediction_path(d, "a.png").exists()
    answer = json.dumps([{"key": "applicant", "value": "김하나", "page": 1, "bbox_2d": [100, 100, 300, 200]},
                         {"key": "signed", "value": False}], ensure_ascii=False)
    with patch("urllib.request.urlopen", return_value=Reply(answer)) as call:
        assert RB.run_inference(request)["completed"] == 1
        body = json.loads(call.call_args.args[0].data)
        assert "data:image/png;base64," in body["messages"][0]["content"][0]["image_url"]["url"]
    assert RB.prediction(d, "a.png")["raw"] == answer
    with patch("urllib.request.urlopen", side_effect=AssertionError("성공 문서는 재호출하지 않는다")):
        assert RB.run_inference(request)["skipped"] == 1
    assert RB.load_document(d, real, "a.png")["fields"][1]["type"] == "signature"


def test_api_connections_custom_review_and_busy_lock(work):
    d, real, reg = work
    class Jobs:
        running = False
        def list(self):
            return [{"id": "j1", "status": "running", "info": {"real_benchmark": d.name}}] if self.running else []
        def get(self, _): return self.list()[0]
    jobs = Jobs()
    def guard(fn, *args, **kw):
        try: return fn(*args, **kw)
        except ValueError as e: raise HTTPException(400, str(e))
        except KeyError as e: raise HTTPException(404, str(e))
    router = API.make_router(reg, jobs, guard, {"providers": {}, "ocr": {}}, real)
    endpoints = {(method, route.path): route.endpoint for route in router.routes for method in route.methods}
    prefix = "/api/real-bench"
    assert endpoints["GET", prefix]()["works"][0]["name"] == d.name
    body = {"ocr": {"base_url": "http://ocr:30107", "revision": "r1"},
            "providers": {"m1": {"base_url": "http://vlm/v1", "model": "bank-sft"}}}
    save = endpoints["PUT", prefix + "/connections"]
    assert save(save.__annotations__["req"](**body))["providers"]["m1"]["model"] == "bank-sft"
    assert RB.connection_config(reg.ws, {})["providers"]["m1"]["external"] is False
    assert endpoints["GET", prefix + "/{name}/doc"](d.name, "a.png")["doc"] == "a.png"
    grouping = endpoints["POST", prefix + "/{name}/grouping"]
    with pytest.raises(HTTPException) as ex:
        grouping(d.name, grouping.__annotations__["req"](action="split", documents=["a.png"]))
    assert ex.value.status_code == 400
    jobs.running = True
    review = endpoints["PUT", prefix + "/{name}/doc"]
    with pytest.raises(HTTPException) as ex:
        review(d.name, "a.png", review.__annotations__["req"](fields=[], done=False))
    assert ex.value.status_code == 409


def test_ocr_adapter_uses_explicit_address(tmp_path):
    from studio import internal_ocr_adapter as adapter
    image = tmp_path / "image.png"
    image.write_bytes(b"image")
    with patch.object(adapter, "urlopen") as post:
        post.return_value.__enter__.return_value.read.return_value = b'{"success":"Y"}'
        assert adapter.ocr_from_file(str(image), base_url="http://new-ocr:30107/") == {"success": "Y"}
        assert post.call_args.args[0].full_url == "http://new-ocr:30107/ocr"
        assert b'name="file"' in post.call_args.args[0].data


@pytest.mark.parametrize("answer", [
    "not JSON", "[]", '[{"key":"applicant","value":"a"}]',
    '[{"key":"applicant","value":{}},{"key":"signed","value":false}]',
    '[{"key":"applicant","value":"a","bbox_2d":[0,0,1100,10],"page":1},{"key":"signed","value":false}]',
    '[{"key":"applicant","value":"a"},{"key":"signed","value":"false"}]',
])
def test_invalid_inference_is_not_a_success(work, answer):
    d, _, _ = work
    with pytest.raises(ValueError):
        RB.parse_items(answer, RB.work(d)["schemas"]["f1"], 1)


def test_prediction_paths_do_not_collide(work):
    d, _, _ = work
    assert RB.prediction_path(d, "a/b.png") != RB.prediction_path(d, "a_b.png")


def test_key_catalog_contains_roles_and_no_example_values(work):
    from studio import key_suggestions as KS
    _, _, reg = work
    rows = KS.catalog(reg.ws)
    by_key = {r["key"]: r for r in rows}
    assert by_key["customer.name"]["who"] == "고객 본인"
    assert by_key["agent.name"]["who"] == "대리인"
    chosen = KS.candidates(rows, ["성명", "대리인 성명"])
    assert {r["key"] for r in rows if r["scope"] == "common"} <= {r["key"] for r in chosen}
    assert all("example" not in r for r in rows)
    assert KS.field_type("rrn") == "text"


def test_key_suggestion_existing_new_and_read_only(work, monkeypatch, tmp_path):
    from studio import key_suggestions as KS
    d, _, reg = work
    before = (d / "real_benchmark.json").read_bytes()
    request = KS.prepare(reg.ws, d, "f1", "m1", {"model": "m1", "base_url": "http://vlm/v1"},
                         [{"key": "", "label": "신청인 성명"}, {"key": "", "label": "특별 심사 코드"}])
    request["result_path"] = str(tmp_path / "suggestions.json")
    answer = [{"request_index": 0, "document_label": "성명", "label": "신청인 성명", "key": "customer.name", "type": "text",
               "source": "existing", "reason": "신청인 구역의 성명이므로 고객 본인"},
              {"request_index": 1, "document_label": "심사코드", "label": "특별 심사 코드", "key": "special_review_code", "type": "text",
               "source": "new", "reason": "동일한 의미의 후보가 없음"}]
    def completion(provider, images, prompt):
        assert len(images) == 1
        assert "customer.name" in prompt and "agent.name" in prompt and "누구의" in prompt
        assert "신청인 성명" in prompt and "값을 추출하거나" in prompt
        return json.dumps(answer, ensure_ascii=False)
    monkeypatch.setattr(RB, "vlm_completion", completion)
    result = KS.run(request)
    assert [s["source"] for s in result["suggestions"]] == ["existing", "new"]
    assert result["suggestions"][0]["requested_label"] == "신청인 성명"
    assert result["candidate_count"] < result["catalog_total"]
    assert (d / "real_benchmark.json").read_bytes() == before  # 제안만으로 항목 정의를 확정하지 않는다.
    assert not RB.prediction_path(d, "a.png").exists()
    for bad in ([answer[0]], [{**answer[0], "key": "not_in_catalog"}, answer[1]],
                [{**answer[0], "request_index": 1}, answer[1]]):
        with pytest.raises(ValueError):
            KS.parse(json.dumps(bad), request)
    discovered = KS.parse(json.dumps([{**row, "request_index": None} for row in answer]), {**request, "requested_fields": []})
    assert len(discovered) == 2 and discovered[0]["requested_label"] is None
    monkeypatch.setattr(RB, "vlm_completion", lambda *a: "malformed proposal")
    with pytest.raises(ValueError):
        KS.run(request)
    failed = RB.read(Path(request["result_path"]))
    assert failed["raw"] == "malformed proposal" and "error" in failed and "suggestions" not in failed


def test_key_suggestion_api_job_and_ownership(work, monkeypatch):
    from studio import key_suggestions as KS
    d, real, reg = work
    class Jobs:
        def __init__(self): self.jobs = {}
        def list(self): return list(self.jobs.values())
        def get(self, jid): return self.jobs[jid]
        def start(self, kind, title, cmd, done, info):
            j = {"id": "j1", "status": "running", "info": info, "kind": kind}
            self.jobs[j["id"]] = j
            self.request = RB.read(Path(cmd[-1]))
            return j
    def guard(fn, *a, **kw):
        try: return fn(*a, **kw)
        except ValueError as e: raise HTTPException(400, str(e))
        except KeyError as e: raise HTTPException(404, str(e))
    jobs = Jobs()
    router = API.make_router(reg, jobs, guard, {"providers": {"m1": {"kind": "openai", "external": False,
                              "model": "m1", "base_url": "http://vlm/v1"}}}, real)
    routes = {(method, route.path): route.endpoint for route in router.routes for method in route.methods}
    start = routes["POST", "/api/real-bench/{name}/schemas/{fid}/suggest-keys"]
    result = start(d.name, "f1", start.__annotations__["req"](provider="m1", fields=[{"label": "신청인 성명"}]))
    lookup = routes["GET", "/api/real-bench/{name}/key-suggestions/{job_id}"]
    assert lookup(d.name, result["job"])["status"] == "running"
    assert RB.work(d)["key_suggestions"]["f1"] == "j1"
    RB.write(Path(jobs.request["result_path"]), {"suggestions": [{"key": "customer.name"}], "raw": "private response", "prompt": "private question"})
    jobs.jobs["j1"]["status"] = "done"
    shown = lookup(d.name, "j1")
    assert shown["suggestions"][0]["key"] == "customer.name" and "raw" not in shown and "prompt" not in shown
    jobs.jobs["j1"]["info"]["real_benchmark"] = "other"
    with pytest.raises(HTTPException) as ex:
        lookup(d.name, "j1")
    assert ex.value.status_code == 404
