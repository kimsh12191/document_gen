"""서식 카드 FORM.md (docgen/formcard.py): 저장소의 카드는 지금 파일과 맞고, 칸·질문·답을 실제 생성 결과대로 적는다."""
import json

import pytest

from docgen import formcard as FC
from docgen import formquestions as FQ
from docgen.registry import load_all


def test_repository_cards_are_fresh():
    """서식 파일·questions.json·공통 질문·키 사전을 고쳤으면 카드를 다시 만든다: python -m docgen.formdir card --stale"""
    stale = [i for i in load_all() if FC.stale(i)]
    assert not stale, f"오래된 카드 {len(stale)}개 (python -m docgen.formdir card --all --stale --workers 4): {stale[:10]}"


def test_card_goes_stale_when_the_form_questions_change(tmp_path, monkeypatch):
    doc = "employment_certificate"
    assert not FC.stale(doc)
    p = tmp_path / "questions.json"
    real = FQ.path
    monkeypatch.setattr(FQ, "path", lambda doc_id: p if doc_id == doc else real(doc_id))
    p.write_text(json.dumps({"kie": {"items": [{"key": "purpose", "label": "발급 용도"}]}}, ensure_ascii=False), encoding="utf-8")
    assert FC.stale(doc)


def test_card_shows_fields_positions_and_the_real_questions(tmp_path):
    pytest.importorskip("playwright")
    from docgen.bench.build import Builder

    b = Builder(tmp_path, 1.0)
    try:
        text = FC.render_card("employment_certificate", b)
    finally:
        b.close()
    assert "card-hash: " + FC.card_hash("employment_certificate") in text
    assert "| `customer.name` ← `employee.name` | 성명 | text | 1쪽 [" in text   # 공통 키 ← 서식 키, 위치
    assert "look/template.html.j2:" in text and "generate.py" in text
    assert "- customer.name: 성명 (고객 성명)" in text   # 실제 질문 줄
    assert '{"key": "customer.name", "value": "' in text   # 실제 정답
    assert "## 고치려면" in text


def test_common_values_list_is_current():
    """값 출처 목록 docgen/forms/_common/values.md 는 코드에서 만든다: python -m docgen.formdir values"""
    assert (FC.SHARED / "values.md").read_text(encoding="utf-8") == FC.values_md()
