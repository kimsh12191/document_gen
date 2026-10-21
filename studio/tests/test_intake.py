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
