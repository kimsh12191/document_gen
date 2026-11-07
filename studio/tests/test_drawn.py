"""새 서식 추가 › 그림 위에 그려서 만들기 (studio/drawn.py): 그림 → 빈 overlay 서식 → 칸·표 행 추가 → 키. 브라우저·OCR 없이."""
import io
import json

import pytest
from PIL import Image

from docgen import formdir
from docgen import realform as RF
from studio import drawn, editor


def png(w=1240, h=1754) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (w, h), "white").save(buf, "PNG")
    return buf.getvalue()


@pytest.fixture
def roots(tmp_path, monkeypatch):
    monkeypatch.setattr(formdir, "NEW_FORMS", tmp_path / "public_forms")
    priv = tmp_path / "private"
    monkeypatch.setenv("DOCGEN_PRIVATE_FORMS", str(priv))
    yield tmp_path / "public_forms", priv
    from docgen.registry import REGISTRY

    for k in [k for k in REGISTRY if k.startswith("img_drawn_")]:   # 다른 시험의 서식 목록에 남기지 않는다
        del REGISTRY[k]


def test_create_checks(roots):
    pub, priv = roots
    with pytest.raises(ValueError, match="img_"):
        drawn.create([("a.png", png())], "payslip", "급여", False, None)
    with pytest.raises(ValueError, match="이름"):
        drawn.create([("a.png", png())], "img_drawn_a", " ", False, None)
    with pytest.raises(ValueError, match="private_forms_dir"):   # 실서류 견본은 저장소에 만들지 않는다
        drawn.create([("a.png", png())], "img_drawn_a", "급여", True, None)
    with pytest.raises(ValueError, match="PDF"):
        drawn.create([("a.txt", b"x")], "img_drawn_a", "급여", False, None)
    assert not (pub / "img_drawn_a").exists() and not (priv / "img_drawn_a").exists()   # 실패하면 폴더를 남기지 않는다


def test_create_pages_a4_and_register(roots):
    pub, priv = roots
    import pymupdf

    pdf = pymupdf.open()
    for _ in range(2):
        pdf.new_page(width=595, height=842)
    res = drawn.create([("small.png", png(620, 877)), ("more.pdf", pdf.tobytes())], "img_drawn_b", "거래 확인서", True, str(priv))
    assert res["private"] and res["pages"] == 3 and not pub.exists()
    lay = json.loads((priv / "img_drawn_b" / "layout.json").read_text(encoding="utf-8"))
    assert lay["origin"] == "drawn" and lay["texts"] == [] and lay["items"] == []
    for pg in lay["pages"]:   # 그림 해상도와 상관없이 긴 변 = A4
        assert max(pg["width"], pg["height"]) == pytest.approx(842, abs=0.5)
    assert (priv / "img_drawn_b" / "look" / "page_2.png").exists() and (priv / "img_drawn_b" / "fields.json").exists()
    from docgen.registry import load_all

    assert load_all()["img_drawn_b"].name == "거래 확인서"   # 분류 정답 = 서식 이름
    with pytest.raises(ValueError, match="이미 있는"):
        drawn.create([("a.png", png())], "img_drawn_b", "다시", True, str(priv))


def test_drawn_cells_keys_and_table_rows(roots):
    _, priv = roots
    drawn.create([("a.png", png())], "img_drawn_c", "거래 확인서", True, str(priv))
    add = [{"t": "text", "page": 0, "label": "성명", "rect": [100, 100, 300, 120]},
           {"t": "text", "page": 0, "label": "연락처", "rect": [100, 130, 300, 150], "key": "customer.phone"}]
    for r in range(3):   # 편집기의 "표의 반복 행" + "이 행 복제" 가 보내는 꼴
        for lab, x0 in (("거래일", 60), ("금액", 300)):
            add.append({"t": "text", "page": 0, "label": lab, "rect": [x0, 300 + r * 20, x0 + 200, 318 + r * 20], "row": True, "group": "거래"})
    editor.save("img_drawn_c", {"add": add}, "test")
    keys = [k for c in RF.layout_keys("img_drawn_c").values() for k in c["keys"]]
    assert keys[:2] == ["customer.name", "customer.phone"]   # 항목명만으로 공통 키, 직접 적은 키는 그대로
    assert "거래_목록.2.금액" in keys and "거래_목록.0.거래일" in keys   # 표 행 칸 (행 번호가 든 키 = 표 과제)


def test_ocr_set_skips_drawn(roots, monkeypatch):
    from docgen import ocr_set

    _, priv = roots
    drawn.create([("a.png", png())], "img_drawn_d", "확인서", True, str(priv))
    monkeypatch.setattr(ocr_set, "_reviewed", lambda: {"img_drawn_d"})
    assert "img_drawn_d" not in ocr_set.select_ids({"types": "imported"})
    with pytest.raises(SystemExit, match="배경 글자"):
        ocr_set.select_ids({"types": ["img_drawn_d"]})
