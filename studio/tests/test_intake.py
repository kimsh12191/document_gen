"""④ 서류 넣기 ❶ (studio/intake.py): 폴더 읽기 규칙, 업무·건 구분, 묶음 만들기 → OCR(저장된 것) → 묶기 → 정확도."""
import json
from pathlib import Path

import pytest
from PIL import Image

from studio import importer as IM
from studio import intake as IN
from studio import intake_testset as T


def _img(p: Path):
    p.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (60, 80), "white").save(p)


def test_find_docs_rules(tmp_path):
    im = tmp_path / "images"
    _img(im / "loan" / "A01" / "id" / "p1.png")
    _img(im / "loan" / "A01" / "id" / "p2.png")
    _img(im / "loan" / "A01" / "scan_0001.png")      # 쪽 번호꼴이 아닌 이미지 = 서류 한 장
    _img(im / "loose.jpg")
    _img(im / "pages" / "page_10.png")
    _img(im / "pages" / "page_2.png")
    import pymupdf

    doc = pymupdf.open()
    doc.new_page()
    doc.new_page()
    (im / "loan" / "A02").mkdir(parents=True)
    doc.save(im / "loan" / "A02" / "contract.pdf")
    docs = {d["id"]: d for d in IN.find_docs(im)}
    assert set(docs) == {"loan/A01/id", "loan/A01/scan_0001", "loose", "pages", "loan/A02/contract"}
    assert [f.name for f in docs["loan/A01/id"]["files"]] == ["p1.png", "p2.png"]
    assert [f.name for f in docs["pages"]["files"]] == ["page_2.png", "page_10.png"]   # 쪽 번호 순서
    assert docs["loan/A02/contract"]["kind"] == "pdf"
    assert IN._rel_parts("loan/A01/id") == ("loan", "A01")
    assert IN._rel_parts("A01/id") == (None, "A01")
    assert IN._rel_parts("id") == (None, None)

    res = IN.check(str(tmp_path))
    assert res["ok"], res["errors"]
    assert res["summary"]["documents"] == 5 and res["summary"]["pages"] == 8 and res["summary"]["pdf"] == 1
    assert res["summary"]["structure"] == "일부만 구분"


def test_cases_csv_overrides_folders(tmp_path):
    _img(tmp_path / "x1.png")
    _img(tmp_path / "x2.png")
    (tmp_path / "cases.csv").write_text("path,case,scenario\nx1.png,K1,mortgage\nx2,K1,mortgage\n", encoding="utf-8")
    res = IN.check(str(tmp_path))
    assert [(d["scenario"], d["case"]) for d in res["docs"]] == [("mortgage", "K1")] * 2
    assert res["summary"]["structure"] == "업무/건/서류" and res["summary"]["cases"] == 1


@pytest.fixture(scope="module")
def testset(tmp_path_factory):
    out = tmp_path_factory.mktemp("set")
    T.build(out, ["fx_remittance", "account_opening"], 2, [], scale=1.0, conditions=(("clean", 1.0),), missing=0.0,
            external=T.EXTERNAL, log=lambda *a: None)
    for name in ("structured", "flat"):
        (out / name / "meta.json").unlink()     # meta.json 없이도 된다
    return out


@pytest.mark.parametrize("name,structure", [("structured", "업무/건/서류"), ("flat", "구분 없음")])
def test_batch_ocr_group_score(testset, tmp_path, name, structure):
    res = IN.check(str(testset / name))
    assert res["ok"], res["errors"]
    assert res["summary"]["structure"] == structure and res["summary"]["with_ocr"] == res["summary"]["pages"]
    b = IN.create_batch(tmp_path, name, str(testset / name), None)
    d = tmp_path / "imports" / b["name"]
    assert b["ocr"]["revision"].startswith("saved-ocr:")          # 모든 쪽에 OCR 이 있으면 사내 OCR 을 부르지 않는다
    IM.run_ocr(d)
    IM.run_group(d)
    s = IN.score(d, testset / "truth.json")
    assert s["documents"] == res["summary"]["documents"]
    assert s["purity"] >= 0.9, s["rows"][:3]                       # 영문 서류끼리 한 포맷으로 뭉치지 않는다
    ov = IN.overview(d)
    assert sum(f["n_docs"] for f in ov["formats"]) == s["documents"]
    assert json.loads((d / "batch.json").read_text(encoding="utf-8"))["results"]["pred"]   # ⑤ 라벨 검수가 쓰는 추출 결과 위치


def test_judge_decide_and_draft(testset, tmp_path, monkeypatch):
    """❷: 기존 서식 지문과 맞는 모양은 '기존 서식', 아닌 것은 '새 서식'. 결정 저장, 새 서식 초안(값 칸·지운 배경)."""
    from studio import intake_judge as IJ

    b = IN.create_batch(tmp_path, "j", str(testset / "structured"), None)
    d = tmp_path / "imports" / b["name"]
    IM.run_ocr(d)
    IM.run_group(d)
    truth = json.loads((testset / "truth.json").read_text(encoding="utf-8"))["documents"]
    rows = {r["id"]: r for r in IM._jsonl(d / "pages.jsonl")}
    fx = json.loads((d / "formats.json").read_text(encoding="utf-8"))
    form_of = lambda f: max({truth[x]["form"] for x in f["docs"]}, key=lambda k: sum(truth[x]["form"] == k for x in f["docs"]))  # noqa: E731
    known = next(f for f in fx["formats"] if form_of(f) == "employment_certificate")
    # 지문: 재직증명서 하나만 '기존 서식'으로 (나머지 모양은 맞는 지문이 없다)
    tokens = rows[next(iter(known["docs"].values()))[0]]["fp"]["tokens"]
    monkeypatch.setattr(IM, "load_form_prints", lambda: {"employment_certificate": {"name": "재직증명서", "tokens": tokens}})
    j = {x["id"]: x for x in IJ.judge(d)}
    assert j[known["id"]]["suggest"]["kind"] == "existing" and j[known["id"]]["suggest"]["form_id"] == "employment_certificate"
    other = next(f for f in fx["formats"] if form_of(f) == "commercial_invoice")
    assert j[other["id"]]["suggest"]["kind"] == "new" and j[other["id"]]["keys"]
    assert any(k["common"] == "foreign.name" for k in j[other["id"]]["keys"])          # shipper.name → 외국 상대 이름
    IJ.decide(d, {other["id"]: {"kind": "new", "name": "상업송장(새)", "uses": {"template": True, "raw": True},
                                "keymap": {"invoice_no": None}}})
    saved = next(x for x in IJ.judge(d) if x["id"] == other["id"])["decision"]
    assert saved["name"] == "상업송장(새)" and saved["uses"] == {"template": True, "raw": True} and saved["keymap"] == {"invoice_no": None}
    with pytest.raises(ValueError):
        IJ.decide(d, {other["id"]: {"kind": "existing", "form_id": "no_such_form"}})
    dr = IJ.draft(d, other["id"])
    assert dr["regions"] and dr["images"] and (d / "drafts" / dr["images"][0]["name"]).is_file()
    # 지운 자리는 한 색으로 칠해진다 (원래 값 글자가 남지 않음)
    from PIL import Image

    img = Image.open(d / "drafts" / dr["images"][0]["name"]).convert("L")
    g = next(x for x in dr["regions"] if x["page"] == 0 and x["rect"][2] - x["rect"][0] > 20)
    x0, y0, x1, y1 = (int(v) for v in g["rect"])
    lo, hi = img.crop((x0 + 2, y0 + 2, x1 - 2, y1 - 2)).getextrema()
    assert lo == hi


@pytest.fixture(scope="module")
def clean_set(tmp_path_factory):
    """추출 오류를 넣지 않은 시험 폴더 (원본 데이터로 내보내기 채점용). 키 이름 바꾸기(name·rrn …)는 그대로 섞인다."""
    out = tmp_path_factory.mktemp("clean")
    T.build(out, ["fx_remittance", "account_opening"], 2, [], scale=1.0, conditions=(("clean", 1.0),), missing=0.0, no_pred=0.0,
            p_wrong=0.0, p_drop=0.0, external=T.EXTERNAL, log=lambda *a: None)
    return out


def test_raw_export_scores_full_on_generated_truth(clean_set, tmp_path):
    """원본 데이터로: 모양마다 진짜 서식으로 정하고 내보내면, 생성 정답으로 채점해 서식·항목(키·값·쪽·위치)이 다 맞고 건이 양쪽에 새지 않는다.
    v1 검사를 통과하고, 의사정답(gt pseudo)·추출 모델이 meta 에 남는다. 외부 문서(새 서식, 등록 전)는 빠진다."""
    from collections import Counter

    from studio import intake_judge as IJ
    from studio import intake_raw as IR
    from studio.labeled_data import inspect

    b = IN.create_batch(tmp_path, "raw", str(clean_set / "structured"), None)
    d = tmp_path / "imports" / b["name"]
    IM.run_ocr(d)
    IM.run_group(d)
    truth = json.loads((clean_set / "truth.json").read_text(encoding="utf-8"))["documents"]
    fx = json.loads((d / "formats.json").read_text(encoding="utf-8"))
    dec = {}
    for f in fx["formats"]:
        top = Counter(truth[x]["form"] for x in f["docs"]).most_common(1)[0][0]
        ext = any(truth[x].get("external") for x in f["docs"])
        dec[f["id"]] = {"kind": "new", "uses": {"raw": True}} if ext else {"kind": "existing", "form_id": top, "uses": {"raw": True}}
    IJ.decide(d, dec)
    pv = IR.preview(d)
    assert pv["unknown_case"] == 0 and pv["cases"]["test"] >= 2 and pv["not_ready"].get("새 서식 등록 전")
    r = IR.export(d, tmp_path / "real")
    assert set(r["splits"]) == {"train", "test"} and r["skipped"]["새 서식 등록 전"] == sum(t.get("external", False) for t in truth.values())
    s = IR.score(tmp_path / "real", b["name"], clean_set)
    assert s["leaked_cases"] == 0 and s["documents"] == sum(not t.get("external") for t in truth.values())
    assert all(w["doc_type"] != w["form"] for w in s["wrong"]), s["wrong"][:3]   # 틀린 것은 묶기에서 섞인 서류뿐
    assert s["form_acc"] >= 0.9
    for sp, x in r["splits"].items():
        c = inspect(x["path"])
        assert c["ok"], c["errors"][:3]
        assert c["meta"]["gt"] == "pseudo" and c["meta"]["model"] == "intake-testset" and c["meta"]["split"] == sp
    # 평가 쪽 건의 서류는 새 서식 초안의 견본으로 쓰지 않는다
    held = IR.test_docs(d)
    assert held and held < set(truth)


def test_raw_v1_fields_and_self_scoring_guard():
    from studio import datasets as DS
    from studio import intake_raw as IR

    km = IR.KeyMapper("account_opening_application", {})
    assert [km(k) for k in ("name", "rrn", "phone", "customer.name")] == ["customer.name", "customer.rrn", "customer.mobile", "customer.name"]
    items = [{"key": "agree", "type": "checkbox", "value": "예", "bbox_2d": [10, 10, 20, 20], "page": 1},
             {"key": "agree", "type": "checkbox", "value": "아니오", "bbox_2d": [30, 10, 40, 20], "page": 1},
             {"key": "seal.bank", "type": "seal", "value": True, "bbox_2d": [500, 500, 600, 600], "page": 1},
             {"key": "memo", "value": "", "page": 1}]
    fields, _ = IR.v1_fields(items, [(1000, 2000)], IR.KeyMapper("no_such_form", {}))
    by = {f["key"]: f for f in fields}
    assert by["agree"]["type"] == "checkbox_multi" and by["agree"]["value"] is None and [o["text"] for o in by["agree"]["options"]] == ["예", "아니오"]
    assert by["agree"]["options"][1]["box_bbox"] == [30.0, 20.0, 40.0, 40.0]
    assert by["seal.bank"] == {"key": "seal.bank", "label": "bank", "type": "seal", "value": None, "present": True, "page": 0,
                               "bbox": [500.0, 1000.0, 600.0, 1200.0]}
    assert by["memo"]["value"] is None and "bbox" not in by["memo"]
    ds = {"gt": "pseudo", "pseudo_model": "m1"}
    assert DS.self_scoring(ds, {"label": "a", "run": "b", "meta": {"model": "m1"}})
    assert DS.self_scoring(ds, {"label": "m1", "run": "b", "meta": None})
    assert DS.self_scoring(ds, {"label": "m2", "run": "b", "meta": {"model": "m2"}}) is None
    assert DS.self_scoring({**ds, "gt": "reviewed"}, {"label": "m1", "run": "b", "meta": None}) is None


def _decide_by_truth(d, truth, template_new=()):
    """❷를 사람이 고친 것처럼: 모양마다 다수 진짜 서식, 외부 문서 모양은 새 서식(template_new 에 든 모양만 '서식으로')."""
    from collections import Counter

    from studio import intake_judge as IJ

    fx = json.loads((d / "formats.json").read_text(encoding="utf-8"))
    by = {**truth, **{v["flat"]: v for v in truth.values()}}
    dec = {}
    for f in fx["formats"]:
        top = Counter(by[x]["form"] for x in f["docs"]).most_common(1)[0][0]
        if any(by[x].get("external") for x in f["docs"]):
            dec[f["id"]] = {"kind": "new", "name": top, "uses": {"raw": True, "template": f["id"] in template_new}}
        else:
            dec[f["id"]] = {"kind": "existing", "form_id": top, "uses": {"raw": True}}
    IJ.decide(d, dec)
    return fx


@pytest.mark.parametrize("name", ["structured", "flat"])
def test_cases_infer(testset, tmp_path, name):
    """❸ 건·업무: 구분 있는 벌은 폴더 기준이 기본이고 정답과 같다. 구분 없는 벌은 자동(고객 식별값)으로 묶어 '확실'한 것은 틀리지 않는다."""
    from studio import intake_cases as IC

    b = IN.create_batch(tmp_path, name, str(testset / name), None)
    d = tmp_path / "imports" / b["name"]
    IM.run_ocr(d)
    IM.run_group(d)
    truth = json.loads((testset / "truth.json").read_text(encoding="utf-8"))["documents"]
    _decide_by_truth(d, truth)
    bs = IC.bases(d)
    assert bs["default"]["case"]["kind"] == ("folder" if name == "structured" else "auto")
    IC.infer(d)
    s = IC.score(d, testset / "truth.json")
    if name == "structured":
        assert s["pair_precision"] == s["pair_recall"] == s["exact_cases"] == s["task_acc"] == 1.0
    else:
        assert s["sure_wrong"] == 0 and s["pair_precision"] >= 0.95
        assert s["without_external"]["pair_recall"] >= 0.7 and s["without_external"]["task_acc"] >= 0.8
    batch = json.loads((d / "batch.json").read_text(encoding="utf-8"))
    # 사람이 고치기: 건 둘 합치기 → 확실
    c1, c2 = list(batch["cases"]["cases"])[:2]
    IC.edit(d, {"merge": [[c1, c2]], "task": {c1: "fx_remittance"}})
    batch = json.loads((d / "batch.json").read_text(encoding="utf-8"))
    assert c2 not in batch["cases"]["cases"] and batch["cases"]["cases"][c1]["sure"] and batch["cases"]["cases"][c1]["scenario"] == "fx_remittance"
    assert all(batch["case_guess"][x]["case"] == c1 for x in batch["cases"]["cases"][c1]["docs"])


def test_case_grouping_rules():
    """기준 값은 무조건 한 건, 자동은 주민번호·휴대전화·생년월일+이름이 확실, 생년월일이 두 글자 이상 다른 고객은 합치지 않는다."""
    from collections import defaultdict

    from studio import intake_cases as IC

    def ident(**kw):
        t = defaultdict(set)
        for k, v in kw.items():
            t[k] |= set(v)
        return t

    ids = {"a": ident(name=["홍길동"], rrn7=["900101-1"], cust7=["900101-1"]),
           "b": ident(name=["홍길동"], rrn7=["900101-1"]),                   # 생년월일+이름 → a 와 확실
           "c": ident(name=["홍길동"], rrn7=["850505-2"], cust7=["850505-2"]),  # 동명이인 (생년월일 다름)
           "d": ident(mobile=["01012345678"]), "e": ident(mobile=["01012345678"], name=["김철수"]),
           "f": ident(), "g": ident(), "h": ident(name=["홍길동"], rrn7=["900101-7"], cust7=["900101-7"])}  # 한 글자 다름 = 추출 오류
    got = IC.group_cases(list(ids), ids, {"f": "R1", "g": "R1"})
    case = {k: v["case"] for k, v in got.items()}
    assert case["a"] == case["b"] == case["h"] and got["b"]["sure"]
    assert case["c"] != case["a"]
    assert case["d"] == case["e"] and got["d"]["sure"]
    assert case["f"] == case["g"] and got["f"]["why"] == ["기준"]
    assert IC._prefix("x/20261021-00123_신분증") == "20261021-00123" and IC._prefix("doc_6343") == "doc"


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    """시나리오 파일·키 사전·이미지 서식 폴더를 임시 사본으로 (저장소 파일을 바꾸지 않는다). 끝나면 원래 시나리오를 다시 읽고 만든 서식을 지운다."""
    import shutil as sh

    from docgen import dictionary as DIC
    from docgen import realform as RF
    from docgen import registry as R

    sc = tmp_path / "scenarios.json"
    sh.copyfile(R.SCENARIOS_JSON, sc)
    dd = tmp_path / "dictionary"
    sh.copytree(DIC.DIR, dd)
    monkeypatch.setattr(R, "SCENARIOS_JSON", sc)
    monkeypatch.setattr(DIC, "DIR", dd)
    DIC._cache.clear()
    monkeypatch.setattr(RF, "IMAGE_FORMS", tmp_path / "images")
    before = set(R.REGISTRY)
    yield sc
    monkeypatch.undo()
    DIC._cache.clear()
    R.load_scenarios()
    for k in set(R.REGISTRY) - before:
        del R.REGISTRY[k]


def test_plan_and_apply(clean_set, tmp_path, sandbox):
    """❸ 반영: 시나리오에서 뺀 서류는 '필수 추가'로 제안되고, 반영하면 시나리오에 돌아온다. '서식으로'를 켠 새 양식은 overlay 서식으로
    등록되어(지운 자리 + 값 칸) 원본 데이터로도 내보내진다. 구분 있는 벌과 없는 벌(모양 = 진짜 서식)의 변경안이 같다."""
    from docgen import registry as R
    from studio import intake_cases as IC
    from studio import intake_plan as IP

    data = json.loads(sandbox.read_text(encoding="utf-8"))
    for s in data["scenarios"]:
        if s["id"] == "account_opening":
            s["docs"].remove("employment_certificate")
    sandbox.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    R.load_scenarios()
    truth = json.loads((clean_set / "truth.json").read_text(encoding="utf-8"))["documents"]
    plans = {}
    for name in ("structured", "flat"):
        b = IN.create_batch(tmp_path, name, str(clean_set / name), None)
        d = tmp_path / "imports" / b["name"]
        IM.run_ocr(d)
        IM.run_group(d)
        fx = _decide_by_truth(d, truth)
        IC.infer(d)
        plans[name] = (d, fx, IP.proposals(d))
    d, fx, p = plans["structured"]
    ch = {c["id"]: c for t in p["tasks"] for c in t["changes"]}
    assert "account_opening:add_required:employment_certificate" in ch
    assert any(c["kind"] == "compare" for c in ch.values())
    # 새 서식 하나를 '서식으로' (추출 결과에 위치가 있는 외부 문서 모양)
    batch = json.loads((d / "batch.json").read_text(encoding="utf-8"))
    by = {f["id"]: f for f in fx["formats"]}
    ext = next(f for f in fx["formats"] if all(truth[x].get("external") for x in f["docs"])
               and any(it.get("bbox_2d") for x in f["docs"] for it in IC._pred_items(batch, x)))
    _decide_by_truth(d, truth, template_new={ext["id"]})
    out = IP.apply(d, tmp_path / "real", None, selected=["account_opening:add_required:employment_certificate"])
    assert out["scenarios"]["applied"] == ["account_opening:add_required:employment_certificate"]
    assert "employment_certificate" in R.SCENARIOS["account_opening"][1]
    [form] = out["forms"]
    assert form["format"] == ext["id"] and form["form_id"] in R.REGISTRY and form["slots"] >= 1 and form["erase"] >= 1
    ov = json.loads((Path(form["dir"]) / "overrides.json").read_text(encoding="utf-8"))
    assert ov["erase"] and ov["add"][0]["key"]
    exported = json.loads((Path(out["raw"]["root"]) / "export.json").read_text(encoding="utf-8"))["documents"]
    assert {v["doc_type"] for v in exported.values()} >= {form["form_id"]}
    assert len(by[ext["id"]]["docs"]) == sum(v["doc_type"] == form["form_id"] for v in exported.values())
