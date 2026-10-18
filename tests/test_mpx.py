"""research/multipage/mpx: 쪽 나누기·상태·병합·채점이 맞는지 (렌더링 없이 손으로 만든 정답으로)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "multipage"))

from mpx.pages import (build_state, doc_content, flatten, merge_pages, nest, page_answer, page_prompt,  # noqa: E402
                       page_views, run_pagewise, split_key)
from mpx.run import normalize_documents, oracle_documents  # noqa: E402
from mpx.score import balance_chain, score_bundle, summarize  # noqa: E402
from mpx.sft import corrupt  # noqa: E402


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


def test_state_kinds_and_prompt():
    views = page_views(statement())
    doc = merge_pages([page_answer(statement(), views, 0)])[0]
    assert build_state(doc, "none") is None
    assert build_state(doc, "doc") == {"document": {"type": "bank_statement", "name": "거래내역확인서", "pages_read": 1}}
    tail = build_state(doc, "tail")
    assert tail["lists"]["rows"]["count"] == 3 and tail["lists"]["rows"]["last"]["balance"] == "930,000"
    ctx = build_state(doc, "context")
    assert ctx["context"] == {"holder": "홍길동", "account_no": "123-45-678901", "opening_balance": "1,000,000"}
    assert "앞 쪽까지 정리한 내용: 없음" in page_prompt(None)
    noisy = corrupt(tail, __import__("random").Random(0))
    assert noisy != tail and tail["lists"]["rows"]["count"] == 3  # 원본은 그대로


def test_run_pagewise_passes_state_from_previous_answers():
    st = statement()
    views = page_views(st)
    prompts = []

    def answer(i, prompt):
        prompts.append(prompt)
        return "", page_answer(st, views, i)

    _, docs, states = run_pagewise(answer, 2, "tail")
    assert states[0] is None and states[1]["lists"]["rows"]["count"] == 3
    assert '"count": 3' in prompts[1] and "없음" in prompts[0]
    assert len(docs) == 1 and len(docs[0]["lists"]["rows"]) == 6


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
