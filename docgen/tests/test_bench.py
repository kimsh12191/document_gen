"""벤치마크 채점기·변조 함수 검사 (렌더링 없이)."""
import json
import random

from docgen.bench import evaluate as E
from docgen.bench import perturb
from docgen.bench.metrics import cer, parse_json, substring_distance, to_number, value_match


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


def test_kie_line_explains_key():
    """질문의 항목 줄은 서식의 키·키 설명 그대로, 덧붙임은 표의 행과 같은 설명 칸의 순번뿐 (키 사전 없음)."""
    from docgen.bench.prompts import kie_line

    assert kie_line("customer.name", "성명") == "- customer.name: 성명"
    assert kie_line("debts.1.balance", "잔액") == "- debts.1.balance: 잔액 (2행)"
    assert kie_line("special_terms.2", "특약사항") == "- special_terms.2: 특약사항 (3번째)"
    assert kie_line("기업부담금_목록.0.상품명", "상품명") == "- 기업부담금_목록.0.상품명: 상품명 (기업부담금 목록 1행)"
    assert kie_line("memo", None) == "- memo: -"
    sib = [{"key": "date", "label": "작성일"}, {"key": "memo", "label": "비고"}, {"key": "date2", "label": "작성일"}]
    assert kie_line("date2", "작성일", siblings=sib) == "- date2: 작성일 (같은 설명 중 2번째 칸)"
    assert kie_line("memo", "비고", siblings=sib) == "- memo: 비고"
    assert kie_line("housing", "주택", extra="체크박스, 보기: 자가 / 전세") == "- housing: 주택 (체크박스, 보기: 자가 / 전세)"


def test_guide_quotes_every_benchmark_prompt():
    """guide/questions.md 는 사용자가 베껴 쓰는 문서라 학습·평가 질문과 같아야 한다 (옛 bank/tests 에서 옮김)."""
    from pathlib import Path

    from docgen.bench import prompts

    guide = (Path(__file__).resolve().parents[2] / "guide" / "questions.md").read_text(encoding="utf-8")
    for name in [n for n in dir(prompts) if n.startswith("P_")]:
        assert getattr(prompts, name).replace("{{", "{").replace("}}", "}") in guide, name


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

    assert E.s_ocr_page(_item("ocr_page", ["김나우", "010-1234-5678"]), "성명 김나우\n전화 010-1234-5678")["metrics"]["recall"] == 1
    assert E.s_ocr_field(_item("ocr_field", "김나우"), "김 나 우")["metrics"]["exact"] == 1


def test_missing_or_unparseable_prediction_scores_zero():
    kie = _item("kie", {"a": None, "b": None, "c": "x"},
                eval={"fields": {k: {"type": "text", "norm": None} for k in "abc"}})
    marks = _item("marks", {"seal.a": False}, eval={"types": {"seal.a": "seal"}})
    for it in (kie, marks):
        for preds in ({}, {it["id"]: "모르겠습니다"}):
            r = E.score_task(it["task"], [it], preds)
            assert r["metrics"][r["main"]] == 0, (it["task"], preds)
    r = E.score_task("ocr_field", [_item("ocr_field", "가나")], {})
    assert r["metrics"]["cer"] == 1


def test_swift_record_matches_model_output_format():
    from docgen.bench.build import swift_record

    page = swift_record({"id": "ocr_page/x", "task": "ocr_page", "images": ["a.png", "b.jpg"], "prompt": "읽으세요",
                         "answer": ["가나", "다라"]})
    assert page["images"] == ["a.png", "b.jpg"] and page["messages"][0]["content"] == "<image><image>읽으세요"
    assert page["messages"][1]["content"] == "가나\n다라"


def test_train_and_test_seeds_do_not_overlap():
    from docgen.bench.build import SPLITS

    test = set(range(SPLITS["test"][0], SPLITS["test"][0] + 10_000))
    train = set(range(SPLITS["train"][0], SPLITS["train"][0] + 100_000))
    assert not test & train
    assert min(test | train) > 100_000  # docgen generate 의 seed(0부터)와도 떨어져 있음
