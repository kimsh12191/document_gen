"""표 과제 (table·table_read·table_find·table_qa)와 빈 답 배우기 (없는 키·열, 빈 칸 비우기, 가림).
표의 정의: 항목 묶음은 서식이 정하고 행 수가 서류마다 다른 것 (guide/reference/benchmark.md "표의 정의"). 표 칸은 kie 가 묻지 않는다."""
import json
from pathlib import Path

import pytest
from PIL import Image

from docgen.bench import absent as AB
from docgen.bench import build as B
from docgen.bench import tasks as T
from docgen.bench.evaluate import SCORERS, _align_rows
from docgen.bench.runner import oracle_output


def f(key, value, x=0, y=0, page=0, label=None, typ="text", **kw):
    return {"key": key, "value": value, "type": typ, "label": label or key.split(".")[-1], "bbox": [x, y, x + 50, y + 10],
            "page": page, **kw}


def doc(fields, q=None, group="income", tables=None, sizes=((1000, 1000), (1000, 1000))):
    r = {"doc_id": "t_doc", "name": "시험 서류", "group": group, "condition": "clean", "writing": "print", "images": ["a.png"],
         "sizes": list(sizes), "fields": fields, "raw_keys": [x["key"] for x in fields], "visible": {x["key"] for x in fields},
         "tables": tables or []}
    d = T.Doc(r, "images/t_doc_1", Path("."), 0, 40)
    d.q = q
    return d


def test_table_cell():
    assert T.table_cell("rows.3.kind") == ("rows", 3, "kind")
    assert T.table_cell("special_terms.2") == ("special_terms", 2, "value")
    assert T.table_cell("a.b.0.c.d") == ("a.b", 0, "c.d")
    assert T.table_cell("items.0.specs.1.no") == ("", -1, "")   # 겹친 목록
    assert T.table_cell("applicant.name") is None and T.table_cell("0.x") is None


def test_doc_tables_order_columns_empty_rows_and_kie_split():
    fields = [f("bank", "국민은행", 0, 0),
              f("rows.0.end", "2012-07-01", 600, 300), f("rows.0.kind", "직장가입자", 100, 300),   # 위치가 아래인 행이 0번
              f("rows.1.kind", "지역세대원", 100, 200), f("rows.1.start", "2022-07-30", 400, 200),
              f("rows.2.kind", None, 100, 400),   # 다 빈 행
              f("rows.0.start", "2010-01-01", 400, 300),
              f("items.0.specs.1.no", "1", 0, 500),   # 겹친 목록: 어디서도 안 묻는다
              f("pick.0", "SMS", 0, 600), {"key": "pick", "value": None, "type": "checkbox_multi", "label": "수신", "group": True},
              f("seal.issuer", "인", 0, 700, typ="seal")]
    d = doc(fields)
    t = d.tables["rows"]
    assert [c for c, _ in t["columns"]] == ["kind", "start", "end"]   # 왼쪽부터
    assert [r["kind"]["value"] for r in t["rows"]] == ["지역세대원", "직장가입자"]   # 위에서부터, 다 빈 행 뺌
    assert set(d.tables) == {"rows"}   # 복수 선택 묶음(pick)은 표가 아님
    assert {"rows.2.kind", "items.0.specs.1.no"} <= d.table_keys and "bank" not in d.table_keys
    kie = T.kie.make(d)[0]
    asked = {a["key"] for a in kie["answer"] if kie["eval"]["fields"][a["key"]].get("kind") != "absent"}
    assert "bank" in asked and not any(k.startswith(("rows.", "items.")) for k in asked)   # 표 칸·겹친 목록은 kie 가 안 묻는다
    d2 = doc(fields, q={"table": {"rows": {"ask": False}}})   # 정해진 격자 → kie
    assert d2.tables == {} and "rows.0.kind" in {a["key"] for a in T.kie.make(d2)[0]["answer"]}


def test_table_item_and_oracle(monkeypatch):
    monkeypatch.setattr(T.table, "ABSENT_RATE", 0)
    fields = [f("rows.0.kind", "직장가입자", 100, 300, label="가입자구분"), f("rows.0.start", "2010-01-01", 400, 300, label="취득일"),
              f("rows.1.kind", "지역세대원", 100, 200, label="가입자구분"),
              f("rows.1.memo", "첫 줄\n둘째 줄", 700, 200, label="비고")]
    d = doc(fields, q={"table": {"rows": {"title": "자격 내역"}}})
    it = T.table.make(d)[0]
    a = it["answer"]
    assert a["columns"] == ["kind", "start", "memo"]
    assert a["rows"] == [["지역세대원", None, "첫 줄 둘째 줄"], ["직장가입자", "2010-01-01", None]]   # 줄바꿈은 공백
    assert a["row_boxes"][0] == {"bbox_2d": [100, 200, 750, 210], "page": 1}
    assert "- kind: 가입자구분" in it["prompt"] and it["meta"]["n_rows"] == 2
    assert SCORERS["table"](it, oracle_output(it))["metrics"]["cell_f1"] == 1


def test_long_and_multi_page_tables_are_asked_whole():
    """행을 잘라 묻지 않는다: 45행·2쪽 표도 모든 행, 범위 말 없음 (한 쪽만은 view "page" 문항)."""
    rows = [f(f"rows.{i}.v", f"값{i}", 100, 10 + i, page=0 if i < 20 else 1) for i in range(45)]
    d = doc(rows)
    scope, chosen, text = T.table.choose_scope(d, d.tables["rows"]["rows"])
    assert scope == "all" and len(chosen) == 45 and text == ""
    it = next(x for x in T.table.make(d))
    assert len(it["answer"]["rows"]) == 45 and "쪽에 있는 행만" not in it["prompt"] and "행까지만" not in it["prompt"]


def test_absent_column_and_keys(monkeypatch):
    monkeypatch.setattr(AB, "pools", lambda group: ([("other", "loan.rate", "금리", "percent"), ("other", "x.memo", "가입자구분", "text")],
                                                    [("other", "fee", "수수료", "amount"), ("other", "kind", "구분", "text")]))
    fields = [f("rows.0.kind", "직장가입자", 100, 300, label="가입자구분"), f("bank", "국민은행")]
    d = doc(fields)
    keys = AB.absent_keys(d, 3)
    assert [k["key"] for k in keys] == ["loan.rate"]   # 항목명이 서류에 있는 칸(가입자구분)은 뺀다
    col = AB.absent_column(d, "rows", T.table.columns(d, d.tables["rows"]))
    assert col["key"] == "fee"   # 표에 이미 있는 열 키(kind)는 뺀다
    monkeypatch.setattr(T.table, "ABSENT_RATE", 1)
    it = T.table.make(doc(fields))[0]
    assert it["eval"]["absent"] == ["fee"] and all(r[it["answer"]["columns"].index("fee")] is None for r in it["answer"]["rows"])
    filled = json.dumps({**it["answer"], "rows": [[v if c != "fee" else "1,000" for c, v in zip(it["answer"]["columns"], r)]
                                                  for r in it["answer"]["rows"]]}, ensure_ascii=False)
    m = SCORERS["table"](it, filled)["metrics"]
    assert m["absent_null"] == 0 and m["cell_precision"] < 1   # 없는 열을 채우면 틀림
    monkeypatch.setattr(T.kie, "ABSENT_RATE", 1)
    kie = T.kie.make(doc(fields))[0]
    assert kie["eval"]["absent"] == ["loan.rate"] and {"key": "loan.rate", "value": None} in kie["answer"]
    assert "- loan.rate: 금리" in kie["prompt"]


def _item(rows, cols=("kind", "start"), boxes=None):
    return {"task": "table", "answer": {"columns": list(cols), "rows": rows, "row_boxes": boxes or [{}] * len(rows)},
            "eval": {"fields": {c: {"type": "date" if c == "start" else "text", "kind": "text"} for c in cols}}}


def test_table_scoring_rows_missing_extra_and_shapes():
    it = _item([["A", "2020-01-01"], ["B", "2021-02-02"], ["C", None]],
               boxes=[{"bbox_2d": [0, 0, 100, 10], "page": 1}, {"bbox_2d": [0, 10, 100, 20], "page": 1}, {}])
    s = SCORERS["table"]
    assert s(it, oracle_output(it))["metrics"]["cell_f1"] == 1
    miss = s(it, json.dumps({"columns": ["kind", "start"], "rows": [["A", "2020.01.01"], ["C", None]]}))["metrics"]
    assert miss["cell_precision"] == 1 and miss["cell_recall"] == pytest.approx(3 / 5) and miss["count_acc"] == 0
    assert miss["row_exact"] == pytest.approx(2 / 3)   # 빠진 B 행만 틀림 (날짜 표기 차이는 같음)
    extra = s(it, json.dumps({"rows": [["A", "2020-01-01"], ["X", "1999-01-01"], ["B", "2021-02-02"], ["C", None]],
                              "columns": ["kind", "start"]}))["metrics"]
    assert extra["cell_recall"] == 1 and extra["cell_precision"] < 1
    swapped = s(it, json.dumps({"columns": ["start", "kind"], "rows": [["2020-01-01", "A"], ["2021-02-02", "B"], [None, "C"]]}))
    assert swapped["metrics"]["cell_f1"] == 1   # 열 이름으로 맞춘다
    objects = s(it, json.dumps([{"kind": "A", "start": "2020-01-01"}, {"kind": "B", "start": "2021-02-02"}, {"kind": "C"}]))
    assert objects["metrics"]["cell_f1"] == 1   # 행마다 객체로 답해도 읽는다
    halluc = s(it, json.dumps({"columns": ["kind", "start"], "rows": [["A", "2020-01-01"], ["B", "2021-02-02"], ["C", "2022-01-01"]]}))
    assert halluc["metrics"]["cell_precision"] < 1 and halluc["metrics"]["row_exact"] == pytest.approx(2 / 3)   # 빈 칸에 지어낸 값
    assert s(it, "표가 없습니다")["parse_fail"]
    loc = s(it, json.dumps({**it["answer"], "row_boxes": [{"bbox_2d": [0, 0, 100, 10], "page": 1}, {"bbox_2d": [0, 50, 100, 60], "page": 1}]}))
    assert loc["metrics"]["loc_f1"] == pytest.approx(0.5)


def test_align_rows_keeps_order():
    g, p = [["A"], ["B"], ["C"]], [["B"], ["C"], ["A"]]
    pairs = _align_rows(g, p, lambda i, j, c: g[i][c] == p[j][c])
    assert pairs == [(1, 0), (2, 1)]   # 순서를 거스르는 짝(A)은 짓지 않는다


def test_table_read_transcribe_spans_and_scoring():
    cell = lambda text, keys=(), rs=1, cs=1, th=False, y=0: {"text": text, "rs": rs, "cs": cs, "th": th, "keys": list(keys),
                                                             "bbox": [0, y, 100, y + 10]}
    dom = {"page": 0, "bbox": [0, 0, 500, 100], "rows": [
        {"cells": [cell("번호", th=True, rs=2), cell("기간", th=True, cs=2), cell("금액", th=True, rs=2)]},
        {"cells": [cell("시작", th=True), cell("끝", th=True)]},
        {"cells": [cell("1", y=20), cell("2020", ["rows.0.start"], y=20), cell("2021", ["rows.0.end"], y=20),
                   cell("100", ["rows.0.amt"], rs=2, y=20)]},
        {"cells": [cell("2", y=30), cell("2022", ["rows.1.start"], y=30), cell("", ["rows.1.end"], y=30)]},
        {"cells": [cell("합계", cs=3, y=40), cell("200", y=40)]}]}
    x = T.table_read.transcribe(dom, {"rows"})
    assert x["columns"] == ["번호", "기간 > 시작", "기간 > 끝", "금액"]
    assert x["rows"] == [["1", "2020", "2021", "100"], ["2", "2022", None, "100"], ["합계", None, None, "200"]]   # rowspan 반복, colspan 첫 열
    mixed = json.loads(json.dumps(dom))
    mixed["rows"][4]["cells"][1]["keys"] = ["total"]
    assert T.table_read.transcribe(mixed, {"rows"}) is None   # 표 칸이 아닌 값이 섞인 표
    item = {"task": "table_read", "answer": {"columns": x["columns"], "rows": x["rows"], "row_boxes": [{}] * 3}}
    s = SCORERS["table_read"]
    assert s(item, oracle_output(item))["metrics"]["cell_f1"] == 1
    renamed = json.dumps({"columns": ["No.", "기간>시작", "기간 > 끝", "금 액"], "rows": x["rows"]}, ensure_ascii=False)
    m = s(item, renamed)["metrics"]
    assert m["cell_f1"] == 1 and m["header_f1"] == 1   # 머리글 글자가 조금 달라도 (비슷한 글자 → 자리)


def test_table_find_and_qa_scoring():
    gold = [{"columns": ["가입자구분", "자격취득일"], "bbox_2d": [100, 100, 900, 500], "page": 1, "n_rows": 4}]
    it = {"task": "table_find", "answer": gold}
    s = SCORERS["table_find"]
    assert s(it, oracle_output(it))["metrics"] == {"f1_iou50": 1, "count_acc": 1, "rows_acc": 1, "header_f1": 1}
    m = s(it, json.dumps([{"bbox_2d": [110, 90, 890, 520], "page": 1, "n_rows": 5}]))["metrics"]
    assert m["f1_iou50"] == 1 and m["rows_acc"] == 0
    assert s({"task": "table_find", "answer": []}, "[]")["metrics"]["f1_iou50"] == 1
    q = SCORERS["table_qa"]
    num = {"answer": 14, "eval": {"answer_type": "number"}}
    assert q(num, "14")["metrics"]["acc"] == 1 and q(num, "14개")["metrics"]["acc"] == 1 and q(num, "13")["metrics"]["acc"] == 0
    val = {"answer": "2022-07-30", "eval": {"answer_type": "value", "type": "date", "key": "start"}}
    assert q(val, "2022.07.30")["metrics"]["acc"] == 1
    empty = {"answer": None, "eval": {"answer_type": "value", "type": "text", "key": "end"}}
    assert q(empty, "null")["metrics"]["acc"] == 1 and q(empty, "2022-01-01")["metrics"]["acc"] == 0


def test_table_qa_questions_have_right_answers():
    fields = [f("rows.0.kind", "직장가입자", 100, 100, label="가입자구분"), f("rows.0.amt", "1,000", 400, 100, label="금액", typ="amount"),
              f("rows.1.kind", "지역세대원", 100, 200, label="가입자구분"), f("rows.1.amt", "2,500", 400, 200, label="금액", typ="amount"),
              f("rows.2.kind", "직장가입자", 100, 300, label="가입자구분"), f("rows.2.amt", None, 400, 300, label="금액", typ="amount")]
    d = doc(fields)
    t = d.tables["rows"]
    qs = {k: (text, ans) for k, text, ans, *_ in T.table_qa._questions(d, T.table.columns(d, t), t["rows"])}
    assert qs["count"][1] == 3 and qs["sum"][1] == 3500
    assert "'가입자구분' 칸이" in qs["count_if"][0]
    assert qs["count_if"][1] == (2 if "'직장가입자'" in qs["count_if"][0] else 1)
    assert qs["last"][1] in ("직장가입자", None)


def test_blank_optional_fields_in_render():
    from docgen.entities import make_profile
    from docgen.registry import load_all
    from docgen.render import render

    spec = load_all()["health_insurance_qualification"]
    p = make_profile(5)
    p.extra["blank_optional"] = 1.0
    _, raw, data = render(spec, p, 5)
    vals = {x["key"]: x["value"] for x in raw}
    assert vals["purpose"] is None and vals["issue_no"] is None and vals["person.name"]   # 용도·발급번호만 비움
    _, raw, data = render(spec, make_profile(5), 5)
    assert {x["key"]: x["value"] for x in raw}["purpose"]   # 기본(미리보기·카드)은 그대로
    starts = [r["start"] for r in data["rows"]]
    assert starts == sorted(starts, key=lambda s: s.replace(".", "-"), reverse=True)   # 실서류처럼 최근 이력이 위


def test_mask_fields_blacks_out_and_nulls(tmp_path):
    img = tmp_path / "p.png"
    Image.new("RGB", (400, 300), "white").save(img)
    fields = [f("customer.name", "홍길동", 100, 100, label="성명"), f("bank", "국민은행", 10, 10, label="은행명"),
              f("memo", "생활비로 3천", 10, 200, label="비고")]
    keys = B.mask_fields(fields, [img], "k1", {"_freetext": {"생활비로 3천": {}}})
    assert keys and "memo" not in keys
    masked = [x for x in fields if x.get("masked")]
    assert all(x["value"] is None for x in masked)
    x0, y0, x1, y1 = masked[0]["bbox"]
    assert Image.open(img).getpixel((int(x0) + 5, int(y0) + 5)) == (0, 0, 0)
    Image.new("RGB", (400, 300), "white").save(img)   # 같은 칸이 두 곳에 찍혔으면 두 곳 모두 가린다
    fields = [f("customer.name", "홍길동", 100, 100, label="성명")]
    anchors = [{"target": "field", "key": "customer.name", "page": 0, "bbox": [100, 100, 150, 110]},
               {"target": "field", "key": "customer.name", "page": 0, "bbox": [300, 250, 350, 260]}]
    assert B.mask_fields(fields, [img], "k2", {}, anchors) == ["customer.name"]
    assert Image.open(img).getpixel((320, 255)) == (0, 0, 0) and Image.open(img).getpixel((120, 105)) == (0, 0, 0)


def test_build_settings_have_nulls():
    assert B.NULLS == {"blank": 0.3, "mask": 0.1} and B.VERSION == "5.1"
    p = B.single_profile(1_000_000, {"blank": 0.5}, "a")
    assert p.extra["blank_optional"] == 0.5 and "blank_optional" not in B.single_profile(1, None, "a").extra
    # 같은 순번이라도 서식마다 다른 고객
    assert B.single_profile(1_000_000, None, "a").person.name != B.single_profile(1_000_000, None, "b").person.name or \
        B.single_profile(1_000_000, None, "a").person.rrn != B.single_profile(1_000_000, None, "b").person.rrn


def test_real_render_gives_every_table_task_and_oracle_scores_full(tmp_path):
    """그림을 실제로 그려: 건강보험 자격득실확인서 한 건 → 표 과제 넷이 나오고, 정답을 답으로 넣으면 모두 만점."""
    pytest.importorskip("playwright")
    from docgen.entities import make_profile

    b = B.Builder(tmp_path, 1.0)
    try:
        r = b.render_doc("health_insurance_qualification", make_profile(1_000_002), 1_000_002, "images/h", "clean", single=True)
        recs = T.make_single(r, "images/h", tmp_path, 2, 40)
    finally:
        b.close()
    tasks = {x["task"] for x in recs}
    assert {"table", "table_read", "table_find", "table_qa"} <= tasks
    assert not any(k.startswith("rows.") for x in recs if x["task"] == "kie" for k in x["eval"]["fields"])
    for x in recs:
        if x["task"].startswith("table"):
            m = SCORERS[x["task"]](x, oracle_output(x))["metrics"]
            assert m[{"table": "cell_f1", "table_read": "cell_f1", "table_find": "f1_iou50", "table_qa": "acc"}[x["task"]]] == 1, x["id"]
    read = next(x for x in recs if x["task"] == "table_read")
    assert read["answer"]["columns"][:2] == ["번호", "가입자구분"] and read["answer"]["rows"][0][0] == "1"


def test_table_audit_lists_what_a_person_decides():
    from docgen.bench import table_audit as TA

    r = TA.audit_form(("health_insurance_qualification", 4))
    t = r["tables"]["rows"]
    assert t["order"] == "desc" and t["min"] >= 1 and set(t["columns"]) >= {"kind", "start", "end"}   # 최신순으로 고쳤음
    md = TA.markdown([r, {"id": "x", "name": "이름[필수](용)", "group": "g", "tables": {}, "numbered": ["aN.b"], "nested": []}], 4)
    assert "표가 있는 서식 1종" in md and "이름\\[필수\\](용)" in md   # 서식 이름의 [ ] 는 링크로 읽히지 않게


def two_pages(tmp_path):
    """2쪽 서류: 1쪽에 이름·표 첫 행, 2쪽에 표 둘째 행·주소."""
    for n in ("p1.png", "p2.png"):
        Image.new("RGB", (1000, 1000), "white").save(tmp_path / n)
    fields = [f("name", "홍길동", 10, 10, 0, "성명"), f("rows.0.kind", "직장", 10, 100, 0, "구분"), f("rows.0.start", "2020-01-01", 200, 100, 0, "취득일"),
              f("rows.1.kind", "지역", 10, 100, 1, "구분"), f("rows.1.start", "2021-01-01", 200, 100, 1, "취득일"), f("addr", "서울", 10, 500, 1, "주소")]
    return {"doc_id": "t_doc", "name": "시험 서류", "group": "income", "condition": "clean", "writing": "print",
            "images": ["p1.png", "p2.png"], "sizes": [(1000, 1000), (1000, 1000)], "fields": fields,
            "raw_keys": [x["key"] for x in fields], "visible": {x["key"] for x in fields}, "tables": []}


def test_multi_page_doc_is_asked_whole_or_one_page_only(tmp_path):
    """여러 쪽 서류: view "all" 은 모든 쪽 이미지·모든 쪽 정답, view "page" 는 한 쪽 이미지·그 쪽 정답만 (위치의 쪽은 1)."""
    r = two_pages(tmp_path)
    whole = T.make_single(r, "images/t_doc_1", tmp_path, 0, 40, page_rate=0)
    assert whole and all(x["images"] == ["p1.png", "p2.png"] and x["meta"]["view"] == "all" for x in whole)
    kie = next(x for x in whole if x["task"] == "kie")
    assert {"name", "addr"} <= {a["key"] for a in kie["answer"]}
    table = next(x for x in whole if x["task"] == "table")
    assert len(table["answer"]["rows"]) == 2

    one = T.make_single(r, "images/t_doc_1", tmp_path, 0, 40, page_rate=1)
    page = one[0]["meta"]["page"]
    assert all(x["images"] == [f"p{page}.png"] and x["meta"]["view"] == "page" and x["meta"]["n_pages"] == 1
               and x["meta"]["n_pages_doc"] == 2 and f"t_doc_1_p{page}" in x["id"] for x in one)
    keys = {a["key"] for x in one if x["task"] == "kie" for a in x["answer"] if a.get("value") is not None}
    assert keys <= ({"name"} if page == 1 else {"addr"})
    table = next(x for x in one if x["task"] == "table")
    assert table["answer"]["rows"] == [["직장", "2020-01-01"] if page == 1 else ["지역", "2021-01-01"]] or table["eval"].get("absent")
    boxes = [b for x in one if x["task"] in ("kie", "table") for b in (x["answer"] if x["task"] == "kie" else x["answer"]["row_boxes"])]
    assert all(b.get("page", 1) == 1 for b in boxes)


def test_one_page_doc_is_always_whole_and_page_view_needs_a_build(tmp_path):
    r = two_pages(tmp_path)
    r = {**r, "images": ["p1.png"], "sizes": [(1000, 1000)], "fields": [x for x in r["fields"] if x["page"] == 0]}
    r["raw_keys"] = [x["key"] for x in r["fields"]]
    assert all(x["meta"]["view"] == "all" for x in T.make_single(r, "images/t_doc_1", tmp_path, 0, 40, page_rate=1))
    assert B.Builder.page_view == 0.0 and T.PAGE_VIEW == 0.5   # 카드·미리보기는 모든 쪽, bench build 만 레시피 page_view (기본 0.5)
