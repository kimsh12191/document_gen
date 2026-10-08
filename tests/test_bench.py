"""벤치마크 채점기·변조 함수 검사 (렌더링 없이)."""
import json
import random

from docgen.bench import evaluate as E
from docgen.bench import perturb
from docgen.bench.metrics import cer, parse_json, substring_distance, to_number, value_match
from docgen.bench.rules import Bundle, _age, _birth_from_rrn, questions


def test_parse_json_tolerates_fences_and_prose():
    assert parse_json('```json\n{"a": 1}\n```') == {"a": 1}
    assert parse_json('결과는 다음과 같습니다: {"a": [1, 2]} 입니다') == {"a": [1, 2]}
    assert parse_json("모름") is None


def test_value_match_normalizes_by_type():
    assert value_match("2025-09-20", "2025년 9월 20일", "date", "2025-09-20")
    assert value_match("500000000", "금 오억원정 (₩500,000,000)", "amount", 500000000)
    assert value_match("327,000,000원", "327,000,000", "amount", 327000000)
    assert value_match("01012345678", "010-1234-5678", "phone", "01012345678")
    assert value_match("김 나우", "김나우", "text", "김나우")
    assert value_match(None, None) and value_match("null", None)
    assert not value_match("327,000,001", "327,000,000", "amount", 327000000)
    assert not value_match("2025-09-21", "2025년 9월 20일", "date", "2025-09-20")
    assert not value_match("", "김나우", "text", "김나우")
    assert not value_match("김나우", None)
    assert value_match("해당없음", "해당없음") and value_match("-", "-") and not value_match(None, "없음")


def test_numbers_and_distances():
    assert to_number("금 이억일천사백만원정") == 214000000
    assert to_number("3억 2천만원") == 320000000
    assert to_number("120.5%") == 120.5
    assert cer("가나다라", "가나다라") == 0 and cer("가나라", "가나다라") == 0.25
    assert substring_distance("홍길동", "성명:홍길둥주소") == 1


def _item(task, answer, **kw):
    return {"id": f"{task}/x", "task": task, "answer": answer, "meta": {}, **kw}


def test_scorers_right_wrong_and_empty():
    kie = _item("kie", {"name": "김나우", "loan.amount": "56,000,000", "memo": None},
                eval={"fields": {"name": {"type": "text", "norm": "김나우"},
                                 "loan.amount": {"type": "amount", "norm": 56000000},
                                 "memo": {"type": "text", "norm": None}}})
    # 중첩 JSON·다른 금액 표기도 정답
    r = E.s_kie(kie, '{"name": "김나우", "loan": {"amount": "56000000원"}, "memo": null}')
    assert r["metrics"]["field_acc"] == 1 and r["metrics"]["f1"] == 1
    r = E.s_kie(kie, '{"name": "김나무", "loan.amount": "56,000,000", "memo": "없음"}')
    assert abs(r["metrics"]["field_acc"] - 2 / 3) < 1e-9
    r = E.s_kie(kie, None)
    assert r["metrics"]["f1"] == 0 and r["parse_fail"]

    marks = _item("marks", {"rate": "변동", "seal.a": True, "multi": ["A", "C"]},
                  eval={"types": {"rate": "checkbox", "seal.a": "seal", "multi": "checkbox_multi"}})
    assert E.s_marks(marks, '{"rate": "변동", "seal.a": "예", "multi": ["C", "A"]}')["metrics"]["acc"] == 1
    assert E.s_marks(marks, '{"rate": "고정", "seal.a": false, "multi": ["A"]}')["metrics"]["acc"] == 0

    dc = _item("doc_check", {"missing": ["주민등록증", "재직증명서"], "not_required": ["여권"], "not_customer": ["재직증명서"]},
               eval={"required": ["주민등록증", "재직증명서", "소득금액증명원"],
                     "names": ["주민등록증", "재직증명서", "소득금액증명원", "여권"]})
    full = '{"missing": ["주민등록증", "재직증명서"], "not_required": ["여권"], "not_customer": ["재직증명서"]}'
    assert E.s_doc_check(dc, full)["metrics"]["exact"] == 1
    r = E.s_doc_check(dc, '{"missing": ["주민등록증"], "not_required": ["여권"], "not_customer": []}')["metrics"]
    assert r["exact"] == 0 and r["not_required_exact"] == 1 and r["not_customer_exact"] == 0
    assert E.s_doc_check(dc, '{"missing": ["주민등록증", "재직증명서"]}')["metrics"]["exact"] == 0

    cc = _item("cross_check", {"consistent": False, "issues": [{"document": "대출거래신청서", "field": "성명",
                                                               "value": "김나무", "expected": "김나우"}]},
               eval={"documents": ["대출거래신청서", "주민등록증"]})
    hit = '{"consistent": false, "issues": [{"document": "대출거래신청서", "field": "성명", "value": "김나무"}]}'
    wrong_doc = '{"consistent": false, "issues": [{"document": "주민등록증", "field": "성명", "value": "김나우"}]}'
    assert E.s_cross_check(cc, hit)["metrics"]["score"] == 1
    assert E.s_cross_check(cc, wrong_doc)["metrics"]["score"] == 0
    assert E.s_cross_check(cc, '{"consistent": true, "issues": []}')["metrics"]["detect"] == 0
    # 관계 불일치는 짝 서류(alt_documents)를 짚거나 원래 값(expected)을 말해도 맞다
    rel = _item("cross_check", {"consistent": False, "issues": [{"document": "등기사항전부증명서", "field": "소유자",
                                                                "value": "추규태", "expected": "신수유",
                                                                "alt_documents": ["주택임대차표준계약서"]}]},
                eval={"documents": ["주택임대차표준계약서", "등기사항전부증명서"]})
    alt = '{"consistent": false, "issues": [{"document": "주택임대차표준계약서", "field": "임대인", "value": "신수유"}]}'
    assert E.s_cross_check(rel, alt)["metrics"]["score"] == 1
    clean = _item("cross_check", {"consistent": True, "issues": []}, eval={"documents": ["주민등록증"]})
    assert E.s_cross_check(clean, '{"consistent": true, "issues": []}')["metrics"]["score"] == 1
    assert E.s_cross_check(clean, hit)["metrics"]["false_alarm"] == 1

    rv = _item("review", 120.1, eval={"answer_type": "number", "tol": 0.1})
    assert E.s_review(rv, "120.1%")["metrics"]["acc"] == 1 and E.s_review(rv, "답: 120.0")["metrics"]["acc"] == 1
    assert E.s_review(rv, "119.9")["metrics"]["acc"] == 0
    yn = _item("review", "아니오", eval={"answer_type": "yesno", "tol": 0})
    assert E.s_review(yn, "아니오.")["metrics"]["acc"] == 1 and E.s_review(yn, "예")["metrics"]["acc"] == 0

    assert E.s_ocr_page(_item("ocr_page", ["김나우", "010-1234-5678"]), "성명 김나우\n전화 010-1234-5678")["metrics"]["recall"] == 1
    assert E.s_ocr_field(_item("ocr_field", "김나우"), "김 나 우")["metrics"]["exact"] == 1


def test_mutate_changes_value_and_keeps_format():
    rng = random.Random(0)
    for f in [{"value": "김나우", "label": "성명", "type": "text"},
              {"value": "830424-1621292", "label": "주민등록번호", "type": "rrn"},
              {"value": "327,000,000", "label": "대출신청금액", "type": "amount", "norm": 327000000},
              {"value": "2025년 9월 20일", "label": "생년월일", "type": "date", "norm": "2025-09-20"},
              {"value": "서울특별시 강남구 테헤란로 152", "label": "주소", "type": "text"}]:
        for _ in range(20):
            new = perturb.mutate(f, rng)
            assert new and new != f["value"] and len(new) == len(f["value"]), (f, new)
    assert perturb.shift_date("2025.02.02", "2025-02-02", -120) == "2024.10.05"
    assert perturb.shift_date("2025년 9월 20일", "2025-09-20", -120) == "2025년 5월 23일"


def test_apply_replaces_only_that_field():
    html = '<span class="fv" data-field="a.name">김나우</span> <span class="fv" data-field="b.name">김나우</span>'
    out = perturb.apply(html, "a.name", "김나우", "김나무")
    assert out == '<span class="fv" data-field="a.name">김나무</span> <span class="fv" data-field="b.name">김나우</span>'
    assert perturb.apply(html, "c", "x", "y") is None


def test_rules_compute_answers():
    def fl(key, value, norm, typ):
        return {"key": key, "label": key, "value": value, "norm": norm, "type": typ}

    B = Bundle("mortgage", {
        "loan_application": {"name": "대출거래신청서", "fields": [
            fl("loan.amount", "300,000,000", 300000000, "amount"), fl("apply_date", "2025년 9월 20일", "2025-09-20", "date"),
            fl("workplace.hire_date", "2015.09.21", "2015-09-21", "date")]},
        "sales_contract": {"name": "부동산 매매계약서", "fields": [
            fl("payment.price", "금 오억원정 (₩500,000,000)", 500000000, "amount"),
            fl("payment.down", "금 오천만원정 (₩50,000,000)", 50000000, "amount")]},
        "resident_id_card": {"name": "주민등록증", "fields": [fl("rrn", "850921-1234567", "850921-1234567", "rrn")]},
    })
    qs = {q["rule"]: q for q in questions(B, random.Random(0))}
    assert qs["ltv"]["answer"] == 60.0
    assert qs["age"]["answer"] == 39          # 생일 하루 전
    assert qs["tenure"]["answer"] == 9        # 입사 10년 되기 하루 전
    assert qs["sales_rest"]["answer"] == 450000000
    assert _age(_birth_from_rrn("000229-3000000"), _birth_from_rrn("250228-3000000")) == 24
    json.dumps(qs, ensure_ascii=False)


def test_missing_or_unparseable_prediction_scores_zero():
    kie = _item("kie", {"a": None, "b": None, "c": "x"},
                eval={"fields": {k: {"type": "text", "norm": None} for k in "abc"}})
    marks = _item("marks", {"seal.a": False}, eval={"types": {"seal.a": "seal"}})
    dc = _item("doc_check", {"missing": []}, eval={"required": ["주민등록증"]})
    for it in (kie, marks, dc):
        for preds in ({}, {it["id"]: "모르겠습니다"}):
            r = E.score_task(it["task"], [it], preds)
            assert r["metrics"][r["main"]] == 0, (it["task"], preds)
    r = E.score_task("ocr_field", [_item("ocr_field", "가나")], {})
    assert r["metrics"]["cer"] == 1


def test_case_helpers():
    from docgen.bench.cases import amount_like, equivalent, shift_first_date

    assert amount_like("금 오억이천만원정 (₩520,000,000)", 600000000) == "금 육억원정 (₩600,000,000)"
    assert amount_like("327,000,000원", 300000000) == "300,000,000원"
    assert amount_like("일금 사억원정", 450000000) == "일금 사억오천만원정"
    assert shift_first_date("2020.08.19 ~ 현재", -366) == "2019.08.19 ~ 현재"
    rng = random.Random(0)
    assert equivalent({"value": "830424-1621292", "type": "rrn", "label": "주민등록번호"}, rng) == "830424-1******"
    assert equivalent({"value": "010-1234-5678", "type": "phone", "label": "연락처"}, rng) == "01012345678"
    d = equivalent({"value": "2025.09.20", "type": "date", "norm": "2025-09-20", "label": "생년월일"}, rng)
    assert d and d != "2025.09.20" and value_match(d, "2025.09.20", "date", "2025-09-20")
