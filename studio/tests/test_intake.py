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
