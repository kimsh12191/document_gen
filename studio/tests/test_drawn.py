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


def test_generator_catalog_sources_are_saveable():
    """생성 방법 고르기의 모든 항목은 저장 검사(editor._check_source)를 통과하고, 빈 칸 말고는 예시 값이 있다."""
    from studio import generators as G

    cat = G.catalog()
    items = [i for g in cat["groups"] for i in g["items"]]
    assert len({i["source"] for i in items}) == len(items)   # 같은 생성 방법이 두 번 나오지 않는다
    for i in items:
        editor._check_source(i["source"], i["name"])
        assert i["examples"] or i["source"] == "rule:empty", i
    assert any(i["source"].startswith("rule:") and i["source"][5:] in __import__("docgen.keyrules", fromlist=["x"]).load()["kinds"] for i in items)
    assert cat["howto"]


def test_auto_example_warns_empty(roots):
    _, priv = roots
    drawn.create([("a.png", png())], "img_drawn_e", "확인서", True, str(priv))
    add = [{"t": "text", "page": 0, "label": "성명", "rect": [100, 100, 300, 120]},
           {"t": "text", "page": 0, "label": "적요", "rect": [100, 130, 300, 150]},
           {"t": "text", "page": 0, "label": "적요", "rect": [100, 160, 300, 180], "source": "rule:choice", "choices": ["이체"]}]
    v = editor.save("img_drawn_e", {"add": add}, "test")
    got = {(i["label"], i.get("source")): i for i in v["items"]}
    assert got[("성명", None)]["auto_example"]                         # 자동 → 고객 이름
    assert got[("적요", None)]["auto_example"] is None                 # 자동 → 빈 칸 (화면이 경고)
    assert "auto_example" not in got[("적요", "rule:choice")]          # 고른 칸은 예시 계산 안 함


def test_format_pattern_fill_and_usergen(roots):
    """표기(fmt)·틀(pattern)·표 채움(fill)·코드 생성기(rule:<함수>)가 그린 서식 값에 들어간다."""
    import random

    from docgen.entities import make_profile

    _, priv = roots
    drawn.create([("a.png", png())], "img_drawn_f", "확인서", True, str(priv))
    add = [{"t": "text", "page": 0, "label": "생년월일", "rect": [100, 100, 300, 120], "fmt": "date.yyyymmdd"},
           {"t": "text", "page": 0, "label": "관리번호", "rect": [100, 130, 300, 150], "source": "rule:pattern", "pattern": "HN-####-{A|B}"},
           {"t": "text", "page": 0, "label": "카드", "rect": [100, 160, 300, 180], "source": "rule:card_masked"}]
    for r in range(4):
        for lab, x0, k in (("거래일", 60, "date"), ("금액", 300, "amount")):
            add.append({"t": "text", "page": 0, "label": lab, "rect": [x0, 300 + r * 20, x0 + 200, 318 + r * 20], "row": True, "group": "거래",
                        "key": f"deals.{{i}}.{k}", "fill": "full", **({"fmt": "amount.won"} if k == "amount" else {})})
    editor.save("img_drawn_f", {"add": add}, "test")
    with pytest.raises(ValueError, match="표기"):
        editor.validate("img_drawn_f", {"add": [{**add[0], "fmt": "nope"}]})
    with pytest.raises(ValueError, match="틀"):
        editor.validate("img_drawn_f", {"add": [{**add[1], "pattern": ""}]})
    for seed in range(3):
        d = RF.build_form("img_drawn_f", make_profile(seed), random.Random(seed))
        v = {i["key"]: i["value"] for i in d["items"] if i.get("key")}
        assert v["customer.birth"].isdigit() and len(v["customer.birth"]) == 8
        assert __import__("re").fullmatch(r"HN-\d{4}-[AB]", v["관리번호"])
        assert "**-****-" in v["카드"]
        amounts = [v[f"deals.{i}.amount"] for i in range(4)]
        assert all(a and a.endswith("원") for a in amounts)   # fill full: 모든 행, 표기 원


def test_overlay_adjust_script(roots):
    """그린 서식도 서식 폴더 generate.py 의 adjust 로 칸끼리 관계를 맞춘다 (합계 = 행의 합). 견본은 formdir adjust --new."""
    import random

    from docgen import formdir as FD
    from docgen.entities import make_profile
    from docgen.formkit import to_amount

    _, priv = roots
    drawn.create([("a.png", png())], "img_drawn_g", "확인서", True, str(priv))
    add = [{"t": "text", "page": 0, "label": "합계", "rect": [100, 100, 300, 120], "key": "total"}]
    for r in range(3):
        add.append({"t": "text", "page": 0, "label": "금액", "rect": [60, 300 + r * 20, 260, 318 + r * 20], "row": True, "key": "deals.{i}.amount"})
    editor.save("img_drawn_g", {"add": add}, "test")
    assert FD.main(["adjust", "img_drawn_g", "--new"]) == 0
    sk = (priv / "img_drawn_g" / "generate.py").read_text(encoding="utf-8")
    assert 'rows(d, "deals")' in sk and "# total = " in sk
    assert FD.main(["adjust", "img_drawn_g", "--new"]) == 1   # 덮어쓰지 않는다
    (priv / "img_drawn_g" / "generate.py").write_text(
        "from docgen.formkit import rows, to_amount, amount_like\n\n\ndef adjust(d, p, rng):\n"
        "    d['total'] = amount_like(sum(to_amount(r.get('amount')) or 0 for r in rows(d, 'deals')), '1,000')\n    return d\n",
        encoding="utf-8")
    for seed in range(4):
        d = RF.build_form("img_drawn_g", make_profile(seed), random.Random(seed))
        v = {i["key"]: i["value"] for i in d["items"] if i.get("key")}
        rows = [to_amount(v.get(f"deals.{i}.amount")) or 0 for i in range(3)]
        rows += [to_amount(c["value"]) or 0 for g in d["extra_rows"] for r in g["rows"] for c in r["cells"]]
        assert to_amount(v["total"]) == sum(rows)


def test_nest_flatten_roundtrip():
    f = {"customer.name": "a", "deals.0.amount": "1", "deals.1.amount": "2", "deals.0.date": "x", "date": "d", "date.x": "q"}
    n = RF.nest(f)
    assert n["deals"][1] == {"amount": "2"} and n["customer"] == {"name": "a"} and n["date.x"] == "q"
    assert RF.flatten(n) == f


def test_read_texts_with_fake_ocr(roots, monkeypatch):
    """배경 글자를 사내 OCR(가짜)로 읽어 layout.json texts 에 → 합성 OCR 세트에서 빠지지 않는다."""
    from docgen import ocr_set
    from docgen.bench import ocr_data
    from docgen.ocr_export import item, page_document

    _, priv = roots
    drawn.create([("a.png", png())], "img_drawn_h", "확인서", True, str(priv))
    with pytest.raises(ValueError, match="OCR 설정"):
        drawn.read_texts("img_drawn_h", None)
    fake = lambda path: page_document([item("거래 확인서", [500, 100, 800, 150], 0.99), item("성명", [100, 300, 180, 340], 0.98, 1)], "p.png")  # noqa: E731
    monkeypatch.setattr(ocr_data, "load_callable", lambda spec: fake)
    cfg = {"callable": "x:y", "revision": "test", "cache_dir": str(priv.parent / "ocr_cache")}
    res = drawn.read_texts("img_drawn_h", cfg)
    assert res["texts"] == 2
    lay = json.loads((priv / "img_drawn_h" / "layout.json").read_text(encoding="utf-8"))
    assert {t["text"] for t in lay["texts"]} == {"거래 확인서", "성명"} and lay["texts_from"]["revision"] == "test"
    with pytest.raises(ValueError, match="이미 배경 글자"):
        drawn.read_texts("img_drawn_h", cfg)
    assert not ocr_set._drawn_without_texts("img_drawn_h")


def test_no_erase_warning_for_real_sample(roots):
    _, priv = roots
    drawn.create([("a.png", png())], "img_drawn_i", "확인서", True, str(priv))
    assert "no_erase" in [c["code"] for c in editor.checks("img_drawn_i")]
    editor.save("img_drawn_i", {"erase": [{"page": 0, "rect": [10, 10, 50, 50]}]}, "test")
    assert "no_erase" not in [c["code"] for c in editor.checks("img_drawn_i")]


def test_usergen_errors(tmp_path, monkeypatch):
    from docgen import usergen

    bad = tmp_path / "generators.py"
    monkeypatch.setattr(usergen, "path", lambda: bad)
    bad.write_text("from docgen.usergen import generator\n\n@generator('x')\ndef date(p, rng, item, row):\n    return '1'\n", encoding="utf-8")
    assert "이미 있는 값 종류" in usergen.error()
    bad.write_text("from docgen.usergen import generator\n\nraise RuntimeError('boom')\n", encoding="utf-8")
    import os
    os.utime(bad, ns=(1, 2))   # 다시 읽게
    assert "3번째 줄" in usergen.error()


def test_formdir_check_and_paths_know_drawn_extras(roots):
    """서식 검사가 직접 만든 생성기(rule:<함수>)를 모르는 값 종류로 잡지 않고, 파일 목록에 칸끼리 관계 generate.py 가 나온다."""
    from docgen import formdir as FD

    _, priv = roots
    drawn.create([("a.png", png())], "img_drawn_j", "확인서", True, str(priv))
    editor.save("img_drawn_j", {"add": [{"t": "text", "page": 0, "label": "카드", "rect": [100, 100, 300, 120], "source": "rule:card_masked"}]}, "test")
    res = FD.check_form("img_drawn_j")
    assert not [x for x in res["problems"] if "card_masked" in x], res["problems"]
    assert "칸끼리 관계 (generate.py)" in [r for r, _ in FD.describe("img_drawn_j")]
