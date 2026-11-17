"""새 서식 추가 › 그림 위에 그려서 만들기 (studio/drawn.py): 그림 → 빈 overlay 서식 → 칸·표 행 추가 → 키. 브라우저·OCR 없이."""
import io
import json
import re

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
    assert keys[:2] == ["성명", "customer.phone"]   # 키를 안 적으면 키 설명 그대로 (공통 키 규칙 없음), 직접 적은 키는 그대로
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
    add = [{"t": "text", "page": 0, "label": "성명", "rect": [100, 100, 300, 120], "key": "customer.name"},
           {"t": "text", "page": 0, "label": "적요", "rect": [100, 130, 300, 150]},
           {"t": "text", "page": 0, "label": "적요", "rect": [100, 160, 300, 180], "source": "rule:choice", "choices": ["이체"]}]
    v = editor.save("img_drawn_e", {"add": add}, "test")
    got = {(i["label"], i.get("source")): i for i in v["items"]}
    assert got[("성명", None)]["auto_example"]                         # 고객 정보 키 + 자동 → 고객 이름
    assert got[("적요", None)]["auto_example"] is None                 # 자동 → 빈 칸 (화면이 경고)
    assert "auto_example" not in got[("적요", "rule:choice")]          # 고른 칸은 예시 계산 안 함


def test_format_pattern_fill_and_usergen(roots):
    """표기(fmt)·틀(pattern)·표 채움(fill)·코드 생성기(rule:<함수>)가 그린 서식 값에 들어간다."""
    import random

    from docgen.entities import make_profile

    _, priv = roots
    drawn.create([("a.png", png())], "img_drawn_f", "확인서", True, str(priv))
    add = [{"t": "text", "page": 0, "label": "생년월일", "rect": [100, 100, 300, 120], "key": "customer.birth", "fmt": "date.yyyymmdd"},
           {"t": "text", "page": 0, "label": "관리번호", "rect": [100, 130, 300, 150], "source": "rule:pattern", "pattern": "HN-####-{A|B}"},
           {"t": "text", "page": 0, "label": "카드", "rect": [100, 160, 300, 180], "source": "rule:card_masked"}]
    for r in range(4):
        for lab, x0, k in (("거래일", 60, "date"), ("금액", 300, "amount")):
            add.append({"t": "text", "page": 0, "label": lab, "rect": [x0, 300 + r * 20, x0 + 200, 318 + r * 20], "row": True, "group": "거래",
                        "key": f"deals.{{i}}.{k}", "kind": k, "fill": "full", **({"fmt": "amount.won"} if k == "amount" else {})})
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


def test_date_cell_parts_source_and_key(roots):
    """날짜 칸(년·월·일): 세 칸이 다 있어야 저장, 생성 방법이 없으면 서류 날짜, 있으면 그 날짜 (생년월일 등), 키를 정하면 그 키."""
    import random

    from docgen.entities import make_profile

    _, priv = roots
    drawn.create([("a.png", png())], "img_drawn_k", "신청서", True, str(priv))
    with pytest.raises(ValueError, match="년·월·일"):
        editor.validate("img_drawn_k", {"add": [{"t": "date", "page": 0, "label": "신청일", "parts": {"y": [10, 10, 40, 20]}}]})
    parts = lambda y: {"y": [100, y, 140, y + 15], "m": [150, y, 170, y + 15], "d": [180, y, 200, y + 15]}  # noqa: E731
    editor.save("img_drawn_k", {"add": [
        {"t": "date", "page": 0, "label": "신청일", "parts": parts(100), "key": "apply_date"},
        {"t": "date", "page": 0, "label": "생년월일", "parts": parts(140), "source": "profile.person.birth", "yy": True, "key": "customer.birth"}]}, "test")
    p = make_profile(3)
    d = RF.build_form("img_drawn_k", p, random.Random(3))
    hid = {i["key"]: i["value"] for i in d["items"] if i["t"] == "hidden"}
    i0 = p.issue_date
    assert hid["apply_date"] == f"{i0.year}년 {i0.month}월 {i0.day}일"
    b = p.person.birth
    assert hid["customer.birth"] == f"{b.year}년 {b.month}월 {b.day}일"
    vis = [i["value"] for i in d["items"] if i["t"] == "text" and i["key"] is None]
    assert f"{b.year % 100:02d}" in vis   # 연도 2자리


def test_dup_key_warning(roots):
    _, priv = roots
    drawn.create([("a.png", png())], "img_drawn_l", "신청서", True, str(priv))
    editor.save("img_drawn_l", {"add": [{"t": "text", "page": 0, "label": "성명", "rect": [100, 100, 300, 120]},
                                        {"t": "text", "page": 0, "label": "성명", "rect": [100, 200, 300, 220]}],
                                "erase": [{"page": 0, "rect": [1, 1, 5, 5]}]}, "test")
    w = [c for c in editor.checks("img_drawn_l") if c["code"] == "dup_key"]
    assert w and "성명2" in w[0]["text"]
    drawn.create([("a.png", png())], "img_drawn_m", "신청서", True, str(priv))   # 뒤 칸에 역할 키를 주면 경고 없음
    editor.save("img_drawn_m", {"add": [{"t": "text", "page": 0, "label": "성명", "rect": [100, 100, 300, 120]},
                                        {"t": "text", "page": 0, "label": "성명", "rect": [100, 200, 300, 220], "key": "applicant.name"}],
                                "erase": [{"page": 0, "rect": [1, 1, 5, 5]}]}, "test")
    assert not [c for c in editor.checks("img_drawn_m") if c["code"] == "dup_key"]


def test_floats_per_form_and_global(roots, tmp_path, monkeypatch):
    """자유 위치 도장·번호 (docgen/floats.py): 서식의 float 칸 + 모든 서식 설정. 도장 글자 정답 켜기·끄기, 안 나온 도장은 '없음'."""
    import random

    from docgen import marks as M
    from docgen.entities import make_profile

    _, priv = roots
    drawn.create([("a.png", png())], "img_drawn_n", "신청서", True, str(priv))
    with pytest.raises(ValueError, match="자유 위치 종류"):
        editor.validate("img_drawn_n", {"add": [{"t": "float", "page": 0, "rect": [10, 10, 200, 200], "preset": "nope"}]})
    with pytest.raises(ValueError, match="도장 글자"):
        editor.validate("img_drawn_n", {"add": [{"t": "float", "page": 0, "rect": [10, 10, 200, 200], "preset": "stamp"}]})
    area = [300, 300, 560, 500]
    editor.save("img_drawn_n", {"add": [
        {"t": "text", "page": 0, "label": "성명", "rect": [100, 100, 300, 120]},
        {"t": "float", "page": 0, "rect": area, "label": "접수인", "preset": "received", "p": 1},
        {"t": "float", "page": 0, "rect": area, "label": "원본대조필", "preset": "certified", "p": 0},
        {"t": "float", "page": 0, "rect": [50, 20, 400, 80], "label": "문서번호", "preset": "ref_no", "p": 1, "pattern": "HN-####"},
        {"t": "float", "page": 0, "rect": area, "label": "확인", "preset": "confirm", "p": 1, "answer": True}],
        "erase": [{"page": 0, "rect": [1, 1, 5, 5]}]}, "test")
    settings = tmp_path / "marks.json"
    settings.write_text(json.dumps({"floats": [{"preset": "dated", "p": 1, "area": "bottom"}]}), encoding="utf-8")
    monkeypatch.setattr(M, "SETTINGS", settings)
    p = make_profile(5)
    d = RF.build_form("img_drawn_n", p, random.Random(5))
    marks = {i["key"]: i for i in d["items"] if i["t"] == "mark"}
    vals = {i["key"]: i["value"] for i in d["items"] if i["t"] in ("text", "hidden") and i.get("key")}
    assert marks["stamp_received"]["seal"] and p.bank_branch in marks["stamp_received"]["name"]
    assert "stamp_received" in vals and vals["stamp_received"].startswith("접 수")          # 정답에 글자 (기본 켬)
    assert not marks["stamp_certified"]["seal"] and "stamp_certified" not in vals           # p=0 → 찍히지 않음 ('없음')
    assert re.fullmatch(r"HN-\d{4}", vals["ref_no"])
    assert vals["stamp_confirm"] == "확 인"                                                  # 기본은 끔, 켠 것만 정답
    assert marks["stamp_dated"]["seal"] and vals["stamp_dated"].startswith(p.bank)           # 모든 서식 설정
    st = marks["stamp_received"]
    x0, y0, x1, y1 = [v / RF.PX for v in st["rect"]]
    assert area[0] - 1 <= x0 and x1 <= area[2] + 1 and area[1] - 1 <= y0 and y1 <= area[3] + 1   # 영역 안
    d2 = RF.build_form("img_drawn_n", make_profile(5), random.Random(5))
    assert d2["items"] == d["items"]   # 같은 seed → 같은 자리


def test_floats_global_settings_saved(tmp_path, monkeypatch):
    from docgen import marks as M
    from studio import marks_admin

    monkeypatch.setattr(M, "SETTINGS", tmp_path / "marks.json")
    view = marks_admin.save_settings({**M.DEFAULTS, "floats": [{"preset": "certified", "p": 0.2, "area": "top_right", "answer": False}]})
    assert view["settings"]["floats"][0]["preset"] == "certified" and len(view["floats"]["presets"]) == len(__import__("docgen.floats", fromlist=["x"]).PRESETS)
    with pytest.raises(ValueError, match="영역"):
        marks_admin.save_settings({**M.DEFAULTS, "floats": [{"preset": "certified", "p": 0.2, "area": "middle"}]})
    marks_admin.save_settings(M.DEFAULTS)
    assert not (tmp_path / "marks.json").exists()   # 기본값이면 파일 없음


def test_floats_on_html_forms(tmp_path, monkeypatch):
    """html 서식: 모든 서식 설정의 자유 위치 도장·번호를 정답에 기록하고, 쪽 나눔 뒤 브라우저가 자리를 고른다 (값 칸은 피함)."""
    from docgen import marks as M
    from docgen.entities import make_profile
    from docgen.registry import load_all
    from docgen.render import render

    settings = tmp_path / "marks.json"
    settings.write_text(json.dumps({"floats": [{"preset": "received", "p": 1}, {"preset": "certified", "p": 0},
                                               {"preset": "ref_no", "p": 1, "area": "top"}]}), encoding="utf-8")
    monkeypatch.setattr(M, "SETTINGS", settings)
    spec = load_all()["employment_certificate"]
    html, fields, _ = render(spec, make_profile(2), 2)
    f = {x["key"]: x for x in fields}
    assert f["seal.stamp_received"]["present"] and f["stamp_received"]["value"].startswith("접 수")
    assert not f["seal.stamp_certified"]["present"] and f["ref_no"]["value"].startswith("Ref. No.")
    assert 'id="dg-floats"' in html
    pytest.importorskip("playwright")
    from docgen.image import ImageRenderer

    try:
        r = ImageRenderer(scale=1.0).__enter__()
    except Exception:  # noqa: BLE001
        pytest.skip("브라우저 없음")
    try:
        info = r.render(html, tmp_path / "a.png")
    finally:
        r.__exit__(None, None, None)
    boxes = {x["key"]: x["bbox"] for x in info["fields"]}
    marks = {x["key"]: x["bbox"] for x in info["marks"]}
    assert "seal.stamp_received" in marks and "ref_no" in boxes
    sb = boxes["stamp_received"]
    assert sb[2] - sb[0] > 30   # 도장 글자 정답 칸이 도장 자리를 덮음
    rn = boxes["ref_no"]
    for k, b in boxes.items():   # 번호가 값 칸을 덮지 않음
        if k in ("ref_no", "stamp_received"):
            continue
        ix = max(0, min(rn[2], b[2]) - max(rn[0], b[0]))
        iy = max(0, min(rn[3], b[3]) - max(rn[1], b[1]))
        assert ix * iy <= 0.25 * max(1, min((rn[2] - rn[0]) * (rn[3] - rn[1]), (b[2] - b[0]) * (b[3] - b[1]))), k


def test_formdir_check_overlay_script(roots):
    """서식 검사가 그린 서식의 generate.py 오류(몇 번째 줄)·같은 seed 두 번 다름·새 키를 문제로 보인다 (guide/studio/generators.md)."""
    from docgen import formdir as FD

    _, priv = roots
    drawn.create([("a.png", png())], "img_drawn_o", "신청서", True, str(priv))
    editor.save("img_drawn_o", {"add": [{"t": "text", "page": 0, "label": "성명", "rect": [100, 100, 300, 120], "key": "customer.name"}],
                                "erase": [{"page": 0, "rect": [1, 1, 5, 5]}]}, "test")
    script = priv / "img_drawn_o" / "generate.py"
    script.write_text("def adjust(d, p, rng):\n    x = d['nope']\n    return d\n", encoding="utf-8")
    assert any("2번째 줄" in x for x in FD.check_form("img_drawn_o")["problems"])
    script.write_text("import random\ndef adjust(d, p, rng):\n    d['customer']['name'] = str(random.random())\n    d['brand_new'] = 'x'\n    return d\n",
                      encoding="utf-8")
    probs = FD.check_form("img_drawn_o")["problems"]
    assert any("같은 seed" in x for x in probs) and any("brand_new" in x for x in probs)
    script.write_text("def adjust(d, p, rng):\n    return d\n", encoding="utf-8")
    assert not FD.check_form("img_drawn_o")["problems"]
