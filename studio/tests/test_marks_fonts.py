"""표시 요소: 경로로 글꼴 등록 (studio/marks_admin.add_font) → 렌더러 @font-face·serve 까지."""
import shutil

import pytest

from docgen import marks as M
from docgen import realform as RF
from studio import marks_admin as MA

SRC = M.FONTS_DIR / "NanumPen.woff2"


@pytest.fixture
def tmp_marks(tmp_path, monkeypatch):
    fonts = tmp_path / "fonts"
    fonts.mkdir()
    for f in M.FONTS_DIR.glob("*.woff2"):   # 기본 손글씨 글꼴
        shutil.copy(f, fonts / f.name)
    monkeypatch.setattr(M, "FONTS_DIR", fonts)
    monkeypatch.setattr(RF, "FONTS", fonts)
    monkeypatch.setattr(M, "POOLS_DIR", tmp_path / "marks")
    monkeypatch.setattr(M, "POOLS", tmp_path / "marks" / "pools.json")
    return tmp_path


def test_add_folder_registers_every_font_file(tmp_marks):
    src = tmp_marks / "내 글꼴"
    (src / "sub").mkdir(parents=True)
    shutil.copy(SRC, src / "My Hand-1.woff2")
    shutil.copy(SRC, src / "sub" / "손글씨.ttf")
    (src / "readme.txt").write_text("x")

    r = MA.add_font("hand_fonts", str(src), 1.2)
    assert sorted(r["added"]) == ["My Hand-1.woff2", "손글씨.ttf"]
    items = {it["name"]: it for it in M.pools()["hand_fonts"] if it.get("font_file")}
    assert items["My Hand-1.woff2"]["id"] == "MyHand1" and items["My Hand-1.woff2"]["scale"] == 1.2
    ttf = items["손글씨.ttf"]["font_file"]
    assert ttf.startswith("Font") and ttf.endswith(".ttf") and (M.FONTS_DIR / ttf).exists()

    # 같은 폴더를 다시 넣으면 건너뛴다
    assert MA.add_font("hand_fonts", str(src))["skipped"] == ["My Hand-1.woff2", "손글씨.ttf"]

    # 렌더러가 @font-face 로 걸고 파일을 넘겨 준다
    faces = {f["family"]: f["file"] for f in M.font_faces(M.pools())}
    assert faces["MyHand1"] == "MyHand1.woff2" and faces["NanumPen"] == "NanumPen.woff2"
    data, mime = RF.serve(f"{RF.HOST}fonts/{ttf}")
    assert mime == "font/ttf" and data == SRC.read_bytes()


def test_print_font_from_file_and_delete(tmp_marks):
    src = tmp_marks / "Gulim.otf"
    shutil.copy(SRC, src)
    MA.add_font("print_fonts", str(src))
    it = next(x for x in M.pools()["print_fonts"] if x.get("font_file"))
    assert it["id"] == "'Gulim'" and it["font_file"] == "Gulim.otf"
    assert {"family": "Gulim", "file": "Gulim.otf"} in M.font_faces(M.pools())
    assert next(x for x in MA.view()["pools"]["print_fonts"] if x["id"] == "'Gulim'")["face"] == "/fonts/Gulim.otf"

    MA.delete_item("print_fonts", "'Gulim'")
    assert not (M.FONTS_DIR / "Gulim.otf").exists()


def test_name_clash_with_different_file_gets_suffix(tmp_marks):
    (M.FONTS_DIR / "Pen.ttf").write_bytes(b"other")
    src = tmp_marks / "Pen.ttf"
    shutil.copy(SRC, src)
    MA.add_font("hand_fonts", str(src))
    assert any(x.get("font_file") == "Pen2.ttf" for x in M.pools()["hand_fonts"])


def test_name_without_path_keeps_old_behaviour(tmp_marks):
    MA.add_font("print_fonts", "'Malgun Gothic'")
    assert any(x["id"] == "'Malgun Gothic'" and "font_file" not in x for x in M.pools()["print_fonts"])
    (tmp_marks / "empty").mkdir()
    (tmp_marks / "empty" / "a.txt").write_text("x")
    with pytest.raises(ValueError, match="글꼴 파일"):
        MA.add_font("hand_fonts", str(tmp_marks / "empty"))   # 글꼴 파일이 없는 폴더
