"""서식의 질문·답 questions.json (docgen/formquestions.py): 지금 규칙으로 만든 파일은 문항을 바꾸지 않고,
고친 줄(묻지 않기·항목명·설명·목록 밖 칸·뺄 칸·분류 정답)과 서식 전용 질문(extra → form_qa)이 그대로 반영된다."""
import json

import pytest

from docgen import formquestions as FQ
from docgen.bench import tasks as T
from docgen.bench.evaluate import SCORERS, main_metric
from docgen.bench.runner import oracle_output
from docgen.entities import make_profile
from docgen.registry import load_all, refresh
from docgen.render import render
from docgen.schema import build_fields

TEMPLATE = """{% extends "_base.html.j2" %}
{% import "_macros.html.j2" as m with context %}
{% block content %}
<p>{{ f("bank", label="은행명") }} {{ f("branch", label="취급점") }}</p>
<p>{{ f("loan.amount", label="신청금액") }} {{ f("memo", label="비고") }}</p>
<table>{% for r in d.rows %}<tr><td>{{ f("rows." ~ loop.index0 ~ ".out", label="출금") }}</td></tr>{% endfor %}</table>
{% endblock %}
"""
FORM = {"name": "질문 시험", "group": "finance", "category": "external", "page": "a4", "origin": "analyzer", "parent": None}
FIELDS = {"engine": "html", "unit": "px",
          "fields": {"bank": {"label": "은행명", "type": "text", "source": "rule:fixed", "text": "국민은행"},
                     "branch": {"label": "취급점", "type": "text", "source": "rule:fixed", "text": "센텀지점"},
                     "loan.amount": {"label": "신청금액", "type": "amount", "source": "rule:fixed", "text": "35,000,000원"},
                     "memo": {"label": "비고", "type": "text", "source": "rule:empty"}},
          "lists": {"rows": {"min": 2, "max": 2, "fields": {"out": {"label": "출금", "type": "amount", "source": "rule:amount"}}}}}
ID = "t_question_form"


@pytest.fixture()
def form(tmp_path, monkeypatch):
    reg = load_all()
    d = tmp_path / "private" / ID
    (d / "look").mkdir(parents=True)
    (d / "look" / "template.html.j2").write_text(TEMPLATE, encoding="utf-8")
    (d / "form.json").write_text(json.dumps(FORM, ensure_ascii=False), encoding="utf-8")
    (d / "fields.json").write_text(json.dumps(FIELDS, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setenv("DOCGEN_PRIVATE_FORMS", str(tmp_path / "private"))
    assert refresh()["added"] == [ID]
    yield d
    reg.pop(ID, None)


def _args(tmp_path, seed=7):
    """그림 없이 그린 문서 한 건 → T.make_single 인자 (위치 없는 칸)."""
    spec = load_all()[ID]
    _, raw, data = render(spec, make_profile(seed), seed)
    (tmp_path / "crops").mkdir(exist_ok=True)
    r = {"doc_id": ID, "name": spec.name, "group": spec.group, "condition": "clean", "writing": "print", "seed": seed,
         "images": ["doc.png"], "sizes": [(800, 1000)], "fields": build_fields(raw), "raw_keys": [f["key"] for f in raw],
         "visible": {f["key"] for f in raw}, "data": data}
    return r, f"images/{ID}_{seed}", tmp_path, 0, 40


def _items(tmp_path):
    return {x["task"]: x for x in T.make_single(*_args(tmp_path))}


def _write(d, body):
    (d / "questions.json").write_text(FQ.dump(body), encoding="utf-8")


def test_default_file_changes_nothing_and_edits_change_the_questions(form, tmp_path):
    before = _items(tmp_path)
    body = FQ.default(ID, seeds=2)
    assert [it["key"] for it in body["kie"]["items"]] == ["bank", "branch", "loan.amount", "memo", "rows.*.out"]
    _write(form, body)
    assert json.loads((form / "questions.json").read_text(encoding="utf-8")) == body   # 한 줄에 항목 하나로 써도 같은 JSON
    assert _items(tmp_path) == before

    items = {it["key"]: it for it in body["kie"]["items"]}
    items["memo"]["ask"] = False
    items["loan.amount"]["label"] = "대출 신청금액"
    items["rows.*.out"]["note"] = "거래 내역 출금액"
    body["classify"] = {"answer": "질문 시험서", "aliases": ["시험 서식"]}
    body["ocr_page"] = {"exclude": ["branch"]}
    _write(form, body)
    after = _items(tmp_path)
    kie = after["kie"]
    assert "- memo:" not in kie["prompt"] and "memo" not in {a["key"] for a in kie["answer"]}
    assert "- loan.amount: 대출 신청금액" in kie["prompt"]
    assert "- rows.0.out: 출금 (거래 내역 출금액)" in kie["prompt"]
    assert after["classify"]["answer"] == "질문 시험서" and after["classify"]["eval"]["aliases"] == ["시험 서식"]
    assert "센텀지점" not in after["ocr_page"]["answer"] and "국민은행" in after["ocr_page"]["answer"]

    body["kie"] = {"others": "skip", "items": [{"key": "bank", "label": "은행명"}]}   # 목록에 없는 칸은 묻지 않는다
    _write(form, body)
    assert [a["key"] for a in _items(tmp_path)["kie"]["answer"]] == ["bank"]


def test_extra_questions_are_form_qa_items_answered_from_the_fields(form, tmp_path):
    body = FQ.default(ID, seeds=2)
    body["extra"] = [
        {"id": "amount", "prompt": "대출 신청금액은 얼마입니까? 숫자로만.", "type": "number", "answer": "{loan.amount}"},
        {"id": "where", "prompt": "어느 은행 어느 지점입니까?", "type": "text", "answer": "{bank} {branch}"},
        {"id": "has_memo", "prompt": "비고가 적혀 있습니까?", "type": "yesno", "when": "memo"},
        {"id": "has_bank", "prompt": "은행명이 적혀 있습니까?", "type": "yesno", "when": "bank"},
        {"id": "memo_text", "prompt": "비고 내용은?", "type": "text", "answer": "{memo}"},   # 빈 칸 → 이 문서에서는 묻지 않음
    ]
    _write(form, body)
    qa = [x for x in T.make_single(*_args(tmp_path)) if x["task"] == "form_qa"]
    assert {x["meta"]["question"]: x["answer"] for x in qa} == {
        "amount": 35000000, "where": "국민은행 센텀지점", "has_memo": "아니오", "has_bank": "예"}
    for x in qa:
        s = SCORERS["form_qa"](x, oracle_output(x))["metrics"]
        assert s[main_metric("form_qa", s)] == 1
    wrong = next(x for x in qa if x["meta"]["question"] == "where")
    assert SCORERS["form_qa"](wrong, "국민은행 해운대지점")["metrics"]["acc"] == 0
    assert SCORERS["form_qa"](wrong, "국민은행  센텀지점.")["metrics"]["acc"] == 1



def test_checks_catch_bad_files_missing_keys_and_new_fields(form):
    (form / "questions.json").write_text('{"kie": {"items": [{"label": "x"}]}, "extra": [{"id": "a b", "type": "date"}], "oops": 1}',
                                         encoding="utf-8")
    why = FQ.check_dir(form)
    assert any("모르는 항목" in w for w in why) and any('"key"' in w for w in why)
    assert any("id 가 없거나" in w for w in why) and any("type 은" in w for w in why)
    assert any(p["id"] == ID and "questions.json" in p["reason"] for p in refresh()["problems"])

    body = FQ.default(ID, seeds=2)
    body["kie"]["items"] = [it for it in body["kie"]["items"] if it["key"] != "memo"] + [{"key": "gone.key", "label": "없음"}]
    body["kie"]["items"][0]["label"] = "거래은행"
    body["extra"] = [{"id": "x", "prompt": "?", "type": "text", "answer": "{nope}"}]
    _write(form, body)
    r = FQ.check(ID, seeds=2)
    assert any("지금 칸에 없는 키" in p and "gone.key" in p for p in r["problems"])
    assert any("extra x" in p and "nope" in p for p in r["problems"])
    assert any("질문 목록에 없는 칸" in n and "memo" in n for n in r["notes"])
    assert any("항목명과 다르게" in n and "거래은행" in n for n in r["notes"])

    merged, added = FQ.add_new(body, FQ.default(ID, seeds=2))
    assert added == ["kie:memo"] and merged["kie"]["items"][0]["label"] == "거래은행"   # 사람이 고친 줄은 그대로
