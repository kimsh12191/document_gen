"""mpx: 쪽 나누기·병합·채점·행 결과 분류·통제 실험이 맞는지 (렌더링 없이 손으로 만든 정답으로)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mpx.pages import (doc_content, flatten, merge_pages, nest, page_answer, page_prompt, page_views,  # noqa: E402
                       run_pagewise, schema_hint, split_key)
from mpx.run import normalize_documents, oracle_documents  # noqa: E402
from mpx.score import balance_chain, score_bundle, summarize  # noqa: E402


def _f(key, value, page, typ="text"):
    return {"key": key, "value": value, "page": page, "type": typ}


def statement(sid="bank_statement_0000001"):
    """2쪽 거래내역: 0~2행은 1쪽, 3~5행은 2쪽. 잔액이 이어진다."""
    fields = [_f("holder", "홍길동", 0), _f("account_no", "123-45-678901", 0, "account_no"),
              _f("opening_balance", "1,000,000", 0, "amount"), _f("seal.issuer", None, 1, "seal")]
    fields[-1]["present"] = True
    bal = 1_000_000
    for i, (out, inn) in enumerate([(100_000, 0), (0, 50_000), (20_000, 0), (0, 300_000), (5_000, 0), (70_000, 0)]):
        bal = bal - out + inn
        page = 0 if i < 3 else 1
        fields += [_f(f"rows.{i}.datetime", f"2025.10.0{i + 1} 10:00:00", page, "datetime"),
                   _f(f"rows.{i}.out", f"{out:,}", page, "amount"), _f(f"rows.{i}.in", f"{inn:,}", page, "amount"),
                   _f(f"rows.{i}.balance", f"{bal:,}", page, "amount")]
    return {"id": sid, "doc_type": "bank_statement", "doc_name": "거래내역확인서", "pages": [{}, {}], "fields": fields}


def idcard(sid="resident_id_card_0000001"):
    return {"id": sid, "doc_type": "resident_id_card", "doc_name": "주민등록증", "pages": [{}],
            "fields": [_f("name", "홍길동", 0), _f("rrn", "900101-1234567", 0, "rrn")]}


def bundle_of(*labels):
    pages = [{"image": f"{lb['id']}_{k}.png", "doc": lb["id"], "page": k} for lb in labels for k in range(len(lb["pages"]))]
    return {"id": "bundle_x", "docs": [lb["id"] for lb in labels], "pages": pages}, {lb["id"]: lb for lb in labels}


def test_keys_roundtrip():
    assert split_key("gapgu.3.holders.1.name") == ("gapgu", 3, "holders.1.name")
    assert split_key("summary.owners.0.name") == ("summary.owners", 0, "name")
    assert split_key("holder") == (None, None, "holder")
    obj = {"a": {"b": "1"}, "c": [{"d": "2", "e": [{"f": "3"}]}]}
    assert nest(flatten(obj)) == obj


def test_page_views_split_rows_by_page():
    views = page_views(statement())
    assert [len(v["lists"]["rows"]) for v in views] == [3, 3]
    assert "holder" in views[0]["fields"] and "seal.issuer" in views[1]["fields"]
    ans = page_answer(statement(), views, 1)
    assert ans["document"] == {"type": "bank_statement", "name": "거래내역확인서", "page": 2, "continues": True}
    assert ans["lists"]["rows"][0]["balance"] == "1,230,000"


def test_merge_pages_rebuilds_documents():
    st, card = statement(), idcard()
    b, labels = bundle_of(card, st)
    answers = [page_answer(labels[p["doc"]], page_views(labels[p["doc"]]), p["page"]) for p in b["pages"]]
    docs = merge_pages(answers)
    assert [d["type"] for d in docs] == ["resident_id_card", "bank_statement"]
    assert docs[1]["pages"] == [2, 3]
    assert docs[1]["lists"] == doc_content(page_views(st))["lists"]


def test_prompt_hint_lists_columns_of_target_types():
    st = {**statement(), "target": True}
    hint = schema_hint([st, idcard()])
    assert "bank_statement" in hint and "rows[datetime, out, in, balance]" in hint
    assert "resident_id_card" not in hint  # 목록 없는 서류·대상 아닌 서류는 빼고
    assert page_prompt(hint).endswith(hint)


def test_run_pagewise_merges_pages_and_records_row_pages():
    st = statement()
    views = page_views(st)

    def answer(i, prompt):
        return "", page_answer(st, views, i)

    raws, docs = run_pagewise(answer, 2)
    assert len(raws) == 2 and len(docs) == 1 and len(docs[0]["lists"]["rows"]) == 6
    assert docs[0]["row_pages"]["rows"] == [1, 1, 1, 2, 2, 2]


def _score(labels_bundle, docs):
    b, labels = labels_bundle
    return summarize([score_bundle(b, labels, docs)])["all"]


def test_oracle_scores_perfect_and_checks_hold():
    lb = bundle_of(idcard(), statement())
    s = _score(lb, oracle_documents(*lb))
    for k in ("doc_pages_exact", "page_assign_acc", "field_f1", "row_f1", "boundary_row_recall", "cont_row_recall",
              "check_balance_chain"):
        assert s[k] == 1.0, k
    assert s["row_dropped"] == 0.0


def test_dropped_boundary_row_and_duplicate_are_caught():
    lb = bundle_of(statement())
    docs = oracle_documents(*lb)
    rows = docs[0]["lists"]["rows"]
    docs[0]["lists"]["rows"] = rows[:2] + rows[3:] + [rows[-1]]  # 1쪽 마지막 행을 빠뜨리고 마지막 행을 겹침
    s = _score(lb, docs)
    assert s["row_dropped"] == 1 / 6
    assert s["boundary_row_recall"] == 1 / 2  # 경계 행은 1쪽 끝 행과 2쪽 첫 행. 그중 1쪽 끝 행이 빠짐
    assert s["row_dup"] > 0
    assert s["check_balance_chain"] < 1.0  # 빠진 행 때문에 잔액이 안 이어짐


def test_split_documents_lower_segmentation():
    lb = bundle_of(statement())
    docs = oracle_documents(*lb)
    whole = docs[0]
    first = {**whole, "pages": [1], "lists": {"rows": whole["lists"]["rows"][:3]}}
    second = {**whole, "pages": [2], "fields": {}, "lists": {"rows": whole["lists"]["rows"][3:]}}
    s = _score(lb, [first, second])
    assert s["doc_pages_exact"] == 0.0
    assert s["row_recall"] == 0.5 and s["cont_row_recall"] == 0.0  # 첫 쪽을 가진 조각과 짝지어지고, 2쪽 행들은 떨어져 나감


def test_balance_chain_reads_amount_strings():
    assert balance_chain({"opening_balance": "100"}, [{"out": "10", "in": "", "balance": "90"},
                                                       {"out": "", "in": "5", "balance": "95"}]) == (2, 2)


def test_normalize_documents_is_robust():
    assert normalize_documents(None) == []
    assert normalize_documents({"documents": "x"}) == []
    docs = normalize_documents({"documents": [{"type": "a", "pages": [1, "2", "x"], "fields": [], "lists": {"r": [{}], "s": 1}}]})
    assert docs == [{"type": "a", "name": None, "pages": [1, 2], "fields": {}, "lists": {"r": [{}]}}]


# ---------------------------------------------------------------------------
# 1단계 관찰: 잘린 답 살리기, 행 결과 분류, 회귀 / 2단계 통제 실험
# ---------------------------------------------------------------------------

from mpx.analyze import logistic  # noqa: E402
from mpx.parse import parse_output  # noqa: E402
from mpx.rows import classify_bundle, classify_lists, row_records  # noqa: E402


def test_parse_output_recovers_truncated_answer():
    obj, cut = parse_output('{"documents": [{"lists": {"rows": [{"a": "1"}, {"a": "2"}, {"a": "3')
    assert cut and obj == {"documents": [{"lists": {"rows": [{"a": "1"}, {"a": "2"}]}}]}
    assert parse_output('{"a": 1}') == ({"a": 1}, False)
    assert parse_output("모름") == (None, False)


def _rows(n):
    return [{"date": (f"2025.01.{i:02d}", "date", None), "amount": (f"{i}00", "text", None)} for i in range(1, n + 1)]


def _plain(rows):
    return [{k: v[0] for k, v in r.items()} for r in rows]


def test_classify_lists_separates_skip_misread_and_cut():
    g = _rows(6)
    p = _plain(g)
    pred = [p[0], {"date": "#", "amount": "#"}, p[3], p[4]]  # 2행 잘못 읽음, 3행 건너뜀, 6행 끝에서 없음
    res = classify_lists({"rows": g}, {"rows": pred}, truncated=False)["rows"]
    assert [e["outcome"] for e in res] == ["exact", "misread", "skipped", "exact", "exact", "cut_stop"]
    res = classify_lists({"rows": g}, {"rows": pred}, truncated=True)["rows"]
    assert res[-1]["outcome"] == "cut_length"
    moved = classify_lists({"rows": g}, {"rows": p[:2] + p[3:], "other": [p[2]]}, truncated=False)["rows"]
    assert moved[2]["outcome"] == "misplaced"


def test_classify_bundle_allatonce_and_pagewise():
    lb = bundle_of(statement(), idcard())
    b, labels = lb
    docs = oracle_documents(*lb)
    rows = docs[0]["lists"]["rows"]
    docs[0]["lists"]["rows"] = rows[:1] + rows[2:4]  # 2행 건너뜀, 5·6행은 끝에서 없음
    pred = {"method": "allatonce", "docs": docs, "truncated": [True]}
    out = [e["outcome"] for e in classify_bundle(b, labels, pred)[(0, "rows")]]
    assert out == ["exact", "skipped", "exact", "exact", "skipped", "skipped"]  # 뒤에 주민등록증 출력이 이어짐
    pred = {"method": "allatonce", "docs": docs[:1], "truncated": [True]}
    out = [e["outcome"] for e in classify_bundle(b, labels, pred)[(0, "rows")]]
    assert out[-2:] == ["cut_length", "cut_length"]
    pred = {"method": "allatonce", "docs": docs[1:], "truncated": [False]}
    assert {e["outcome"] for e in classify_bundle(b, labels, pred)[(0, "rows")]} == {"doc_missing"}

    st = {**statement(), "target": True}
    views = page_views(st)
    answers = [page_answer(st, views, 0), page_answer(st, views, 1)]
    answers[1]["lists"]["rows"] = answers[1]["lists"]["rows"][:1]  # 2쪽 답이 첫 행 뒤에서 잘림
    b1, labels1 = bundle_of(st)
    pred = {"method": "pagewise", "docs": merge_pages(answers), "truncated": [False, True]}
    out = [e["outcome"] for e in classify_bundle(b1, labels1, pred)[(0, "rows")]]
    assert out == ["exact"] * 4 + ["cut_length", "cut_length"]
    recs = row_records(b1, labels1, pred, "pw")
    assert [r["dropped"] for r in recs] == [False] * 4 + [True, True]
    assert [r["boundary"] for r in recs] == [False, False, True, True, False, False]
    assert recs[4]["rows_before"] == 1 and recs[4]["n_images"] == 1


def test_logistic_ranks_the_real_signal_first():
    import random as _r

    rng = _r.Random(0)
    rows = []
    for _ in range(400):
        x, noise = rng.gauss(0, 1), rng.gauss(0, 1)
        rows.append({"x": x, "noise": noise, "y": rng.random() < 1 / (1 + 2.718 ** (-(2 * x - 1)))})
    reg = logistic(rows, lambda r: r["y"], ["noise", "x"])
    assert reg[0]["feature"] == "x" and reg[0]["coef"] > 1


def test_probe_oracle_and_simulated(tmp_path):
    import json as _j

    from mpx import probe

    st, card = statement(), idcard()
    st["rep"] = f"{st['id']}_rep"
    rep = {**statement(), "id": st["rep"]}
    for lb in (st, card, rep):
        lb.update(target=lb is st, images=[f"images/{lb['id']}_p{k + 1}.png" for k in range(len(lb["pages"]))],
                  pages=[{"width": 1000, "height": 1400}] * len(lb["pages"]), n_pages=len(lb["pages"]))
        (tmp_path / "labels").mkdir(exist_ok=True)
        (tmp_path / "labels" / f"{lb['id']}.json").write_text(_j.dumps(lb, ensure_ascii=False), encoding="utf-8")
    b, _ = bundle_of(card, st)
    (tmp_path / "bundles.jsonl").write_text(_j.dumps(b) + "\n", encoding="utf-8")
    md = probe.run_all(tmp_path, tmp_path / "oracle", None, max_items=2, workers=1)
    rows = [_j.loads(x) for x in (tmp_path / "oracle" / "rows.jsonl").read_text().splitlines()]
    assert {r["kind"] for r in rows} == {"resolution", "scope", "images", "repeat", "penalty"}
    items = [_j.loads(x) for x in (tmp_path / "oracle" / "items.jsonl").read_text().splitlines()]
    assert {i["sampling"]["repetition_penalty"] for i in items if i["kind"] == "penalty"} == {1.0, 1.05, 1.1}
    assert all(r["outcome"] == "exact" for r in rows) and "A 해상도" in md
    probe.run_all(tmp_path, tmp_path / "sim", None, max_items=2, workers=1, simulate=0.5)
    rows = [_j.loads(x) for x in (tmp_path / "sim" / "rows.jsonl").read_text().splitlines()]
    assert any(r["outcome"] != "exact" for r in rows)


def test_repeat_twin_makes_runs_of_same_text():
    import random as _r

    from docgen.entities import make_profile
    from docgen.registry import load_all
    from docgen.render import render
    from mpx.gen import _repeat_rows
    from mpx.rows import same_text_prev

    html, raw, _ = render(load_all()["bank_statement"], make_profile(5), 5)
    new_html, new_raw = _repeat_rows(html, raw, ("type", "memo"), _r.Random(2))
    val = {x["key"]: x["value"] for x in new_raw}
    n = 1 + max(int(k.split(".")[1]) for k in val if k.startswith("rows."))
    rows = [{c: (val[f"rows.{i}.{c}"], "text", None) for c in ("type", "memo")} |
            {"out": (val[f"rows.{i}.out"], "amount", None)} for i in range(n)]
    same = sum(same_text_prev(rows, i) for i in range(n))
    assert 0 < same < n and new_html != html
    assert [x["value"] for x in new_raw if x["key"].endswith(".out")] == [x["value"] for x in raw if x["key"].endswith(".out")]
