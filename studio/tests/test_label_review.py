"""9단계 시험: 결과 폴더 검사·가져오기(studio/results.py) → 라벨 검수(studio/label_review.py) → 표준 라벨 v1 폴더 → 검수 전 점수.
브라우저·사내 OCR 없이 (흰 쪽 그림 + 사내 OCR 형식 JSON + 추론 결과를 직접 만든다)."""
import json

import pytest
from PIL import Image

from docgen import ocr_export as X
from studio import importer as IM
from studio import label_review as LR
from studio import results as RS

W, H = 1000, 1400
DOCS = {"A001": {"employee.name": "김하나", "company.name": "주식회사 한빛", "employment.position": "대리"},
        "A002": {"employee.name": "이두리", "company.name": "주식회사 다솜", "employment.position": "과장"}}
BOX = {"employee.name": [300, 200, 420, 230], "company.name": [300, 300, 520, 330], "employment.position": [300, 400, 380, 430]}
LABEL = {"employee.name": "성명", "company.name": "회사명", "employment.position": "직위"}


@pytest.fixture
def folder(tmp_path):
    root = tmp_path / "res"
    for doc, vals in DOCS.items():
        img = root / "images" / doc / "page_1.png"
        img.parent.mkdir(parents=True)
        Image.new("RGB", (W, H), "white").save(img)
        words = [("재 직 증 명 서", [400, 80, 600, 120])] + [(LABEL[k], [150, b[1], 250, b[3]]) for k, b in BOX.items()] + \
            [(v, BOX[k]) for k, v in vals.items()]
        oj = root / "ocr" / doc / "page_1.json"
        oj.parent.mkdir(parents=True)
        oj.write_text(json.dumps(X.page_document([X.item(t, b, 0.99, i) for i, (t, b) in enumerate(words)], "page_1.png"),
                                 ensure_ascii=False), encoding="utf-8")
        items = []
        for k, v in vals.items():
            b = BOX[k]
            items.append({"key": "emp_name" if k == "employee.name" else k, "label": LABEL[k],
                          "value": v + "X" if (doc, k) == ("A002", "company.name") else v,   # 틀린 추론 하나
                          "bbox_2d": [b[0], b[1] * 1000 // H, b[2], b[3] * 1000 // H], "page": 1})
        (root / "pred").mkdir(exist_ok=True)
        (root / "pred" / f"{doc}.json").write_text(json.dumps({"items": items}, ensure_ascii=False), encoding="utf-8")
    (root / "meta.json").write_text(json.dumps({"format": "studio-results/1", "name": "시험", "real_data": True, "model": "m1",
                                                "document_regex": "^(?P<document_id>[^/]+)/page_\\d+\\.png$"}), encoding="utf-8")
    (root / "bundles.jsonl").write_text(json.dumps({"bundle_id": "b1", "scenario": "credit_loan", "documents": ["A001", "A002"]}) + "\n",
                                        encoding="utf-8")
    return root


def test_check_reports_problems(folder, tmp_path):
    ok = RS.check(str(folder))
    assert ok["ok"] and ok["summary"] == {"documents": 2, "pages": 2, "with_pred": 2, "bundles": 1}
    (folder / "pred" / "A001.json").write_text('{"items": [{"value": 1, "bbox_2d": [0, 0, 2000, 5]}]}', encoding="utf-8")
    bad = RS.check(str(folder))
    assert not bad["ok"] and any("key" in e for e in bad["errors"]) and any("bbox_2d" in e for e in bad["errors"])
    assert not RS.check(str(tmp_path / "none"))["ok"]
    assert RS.flatten({"a": {"b": 1}, "c": [{"d": 2}]}) == [{"key": "a.b", "value": 1}, {"key": "c.0.d", "value": 2}]


@pytest.fixture
def batch(folder, tmp_path):
    ws = tmp_path / "ws"
    b = RS.create_batch(ws, "res1", str(folder), {"cache_dir": str(tmp_path / "cache")})
    assert b["source"]["kind"] == "results" and b["results"]["model"] == "m1" and b["ocr"]["revision"].startswith("saved-ocr")
    bdir = ws / "imports" / "res1"
    IM.run_ocr(bdir)   # 저장된 OCR 만 쓴다 (사내 OCR 을 부르지 않음)
    fx = IM.run_group(bdir)
    assert len(fx["formats"]) == 1 and len(fx["formats"][0]["docs"]) == 2
    return bdir, fx["formats"][0]["id"]


def test_review_flow_to_v1_and_score(batch, tmp_path):
    from studio import labeled_data as L

    bdir, fid = batch
    real = tmp_path / "real"
    ov = LR.overview(bdir, real)
    assert ov["formats"][0]["doc_type"] is None and ov["formats"][0]["with_pred"] == 2
    d = LR.load_doc(bdir, real, "A001")
    assert {f["key"] for f in d["fields"]} == {"emp_name", "company.name", "employment.position"}
    assert d["fields"][0]["bbox"][0] == pytest.approx(300, abs=1) and d["fields"][0]["page"] == 0   # 0~1000 → 픽셀, 쪽 0부터
    with pytest.raises(ValueError, match="서식이 정해지지"):
        LR.save_doc(bdir, real, "A001", d["fields"], True, "t")
    IM.set_decision(bdir, fid, {"kind": "existing", "form_id": "employment_certificate"})
    km = LR.keymap_view(bdir, real, fid)
    assert {k["key"]: k["mapped"] for k in km["model_keys"]}["emp_name"] is None and any(s["key"] == "employee.name" for s in km["standard"])
    LR.save_keymap(bdir, real, fid, {"emp_name": "employee.name"})
    assert LR.overview(bdir, real)["formats"][0]["n_unmapped"] == 0
    for doc in DOCS:
        d = LR.load_doc(bdir, real, doc)
        assert "employee.name" in {f["key"] for f in d["fields"]}
        fields = d["fields"]
        if doc == "A002":
            for f in fields:
                if f["key"] == "company.name":
                    f["value"], f["state"] = "주식회사 다솜", "edited"   # 틀린 추론을 고친다
        st = LR.save_doc(bdir, real, doc, fields, True, "tester")
        assert st["status"] == "done"
    rt = LR.root(real, "res1")
    lab = json.loads((rt / "labels" / "A002.json").read_text(encoding="utf-8"))
    assert lab["doc_type"] == "employment_certificate" and lab["images"] == ["images/A002_p1.png"]
    assert {f["key"]: f["value"] for f in lab["fields"]}["company.name"] == "주식회사 다솜"
    rv = json.loads((rt / "review" / "A002.json").read_text(encoding="utf-8"))
    assert {f["key"]: f["state"] for f in rv["fields"]} == {"employee.name": "confirmed", "company.name": "edited", "employment.position": "confirmed"}
    assert next(f for f in rv["fields"] if f["key"] == "company.name")["original"]["value"] == "주식회사 다솜X"   # 원래 추론 보관
    # 검수 전 점수: 6칸 중 1칸 값이 틀림 → 값 점수 1 미만, 위치는 모두 맞음
    sc = LR.score(bdir, real)
    kie = sc["tasks"]["kie"]
    assert sc["documents"] == 2 and sc["model"] == "m1" and kie["n"] == 2
    assert 0.5 < kie["metrics"]["f1"] < 1 and kie["metrics"]["loc_f1"] == pytest.approx(1.0) and kie["main"] == "vl_f1"
    # 같은 자리 모아 보기·의심 먼저
    kv = LR.key_view(bdir, real, fid, "company.name")
    assert [r["field"]["value"] for r in kv] == ["주식회사 한빛", "주식회사 다솜"]
    sus = LR.suspicious(bdir, real, fid)
    assert {s["doc"] for s in sus} == set(DOCS) and all(not s["not_in_ocr"] for s in sus)
    # 업무 묶음: 결과 폴더의 묶음을 이어 받아 고쳐 저장 → v1 폴더 그대로 검사 통과
    bd = LR.bundles(bdir, real)
    assert bd["bundles"][0]["bundle_id"] == "b1"
    with pytest.raises(ValueError, match="시나리오"):
        LR.save_bundles(bdir, real, [{"bundle_id": "b1", "documents": ["A001"]}])
    with pytest.raises(ValueError, match="같은 서식"):
        LR.save_bundles(bdir, real, [{"bundle_id": "b1", "scenario": "personal_credit_loan", "documents": ["A001", "A002"]}])
    with pytest.raises(ValueError, match="등록되지 않은 시나리오"):
        LR.save_bundles(bdir, real, [{"bundle_id": "b1", "scenario": "nope", "documents": ["A001"]}])
    assert LR.save_bundles(bdir, real, [{"bundle_id": "b1", "scenario": "personal_credit_loan", "documents": ["A001"], "not_customer": []},
                                        {"bundle_id": "b2", "scenario": "jeonse_loan", "documents": ["A002"]}]) == 2
    chk = L.inspect(str(rt))
    assert not chk["errors"], chk["errors"][:5]
    assert chk["summary"]["documents"] == 2
    # 확인을 풀면 v1 폴더에서 빠진다
    LR.save_doc(bdir, real, "A002", rv["fields"], False, "tester")
    assert not (rt / "labels" / "A002.json").exists()


def test_save_doc_validates(batch, tmp_path):
    bdir, fid = batch
    real = tmp_path / "real"
    d = LR.load_doc(bdir, real, "A001")
    f = dict(d["fields"][0])
    with pytest.raises(ValueError, match="같은 키"):
        LR.save_doc(bdir, real, "A001", d["fields"] + [f], False, "t")
    with pytest.raises(ValueError, match="쪽 번호"):
        LR.save_doc(bdir, real, "A001", [{**f, "page": 3}], False, "t")
    g = {**f, "bbox": [900, 900, 5000, -20]}
    LR.save_doc(bdir, real, "A001", [g], False, "t")
    saved = LR.load_doc(bdir, real, "A001")["fields"][0]["bbox"]
    assert saved[2] <= W and saved[1] >= 0   # 쪽 밖 좌표는 쪽 안으로


def test_autolabel_fills_pred_for_review(batch, tmp_path):
    """내부 openai 방식 모델(시험용 가짜 서버)로 먼저 채우면 그 답이 라벨 검수의 출발점이 된다."""
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    from studio import analyzers as AZ

    seen = []

    class Fake(BaseHTTPRequestHandler):
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            seen.append(body)
            ans = '```json\n[{"key": "employee.name", "value": "모델이 읽은 이름", "bbox_2d": [300, 142, 420, 164], "page": 1}]\n```'
            out = json.dumps({"choices": [{"message": {"content": ans}}]}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(out)

        def log_message(self, *a):
            pass

    srv = ThreadingHTTPServer(("127.0.0.1", 0), Fake)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    cfg = {"providers": {"local": {"kind": "openai", "base_url": f"http://127.0.0.1:{srv.server_port}/v1", "model": "m", "external": False},
                         "ext": {"kind": "openai", "base_url": "http://x/v1", "external": True}}}
    bdir, fid = batch
    real = tmp_path / "real"
    b = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    b["results"]["pred"] = {}   # 결과 폴더 추론이 없는 묶음처럼
    (bdir / "batch.json").write_text(json.dumps(b, ensure_ascii=False), encoding="utf-8")
    keys = [{"key": "employee.name", "label": "성명"}]
    docs = [{"doc": d, "pages": [r["image"] for r in IM._jsonl(bdir / "pages.jsonl") if r["doc"] == d]} for d in DOCS]
    with pytest.raises(ValueError, match="내부 분석기"):
        AZ.create_autolabel(tmp_path / "ws", cfg, "ext", bdir, fid, docs, keys)
    with pytest.raises(ValueError, match="표준 키"):
        AZ.create_autolabel(tmp_path / "ws", cfg, "local", bdir, fid, docs, [])
    d = AZ.create_autolabel(tmp_path / "ws", cfg, "local", bdir, fid, docs, keys)
    try:
        AZ.run_autolabel(d, cfg)
    finally:
        srv.shutdown()
    assert len(seen) == 2 and seen[0]["messages"][0]["content"][-1]["text"].startswith("이 문서에서 아래 항목의 값과 위치")
    assert AZ.validate_autolabel(d)["ok"]
    ld = LR.load_doc(bdir, real, "A001")
    assert ld["has_pred"] and ld["fields"][0]["value"] == "모델이 읽은 이름" and ld["fields"][0]["page"] == 0
    AZ.run_autolabel(d, cfg)   # 다시 돌려도 이미 채운 문서는 건너뛴다 (서버가 꺼져 있어도 실패 없음)
    assert json.loads((d / "output" / "summary.json").read_text(encoding="utf-8"))["skipped"] == 2
