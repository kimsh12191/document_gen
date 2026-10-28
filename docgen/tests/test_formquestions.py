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


def _set_q(d, q: dict):
    """칸 목록 fields.json 의 칸마다 질문 설정 q (키 → q, 반복 행은 rows.out)."""
    body = json.loads(json.dumps(FIELDS))
    for k, v in q.items():
        if k.startswith("rows."):
            body["lists"]["rows"]["fields"][k.split(".", 1)[1]]["q"] = v
        else:
            body["fields"][k]["q"] = v
    (d / "fields.json").write_text(json.dumps(body, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def _write(d, body):
    (d / "questions.json").write_text(FQ.dump(body), encoding="utf-8")


def test_only_changes_are_written_and_they_change_the_questions(form, tmp_path):
    before = _items(tmp_path)
    view = FQ.resolved(ID, seeds=2)
    assert [it["key"] for it in view["kie"]["items"]] == ["bank", "branch", "loan.amount", "memo", "rows.*.out"]
    assert view["kie"]["prompt"] == FQ.common_prompt("kie") and not view["kie"]["changed"]
    assert all(it["ask"] and not it["changed"] and it["q_label"] == it["label"] for it in view["kie"]["items"])

    from docgen.preview import source_hash

    h = source_hash(ID, common=False)
    _set_q(form, {"memo": {"ask": False}, "loan.amount": {"label": "대출 신청금액"}, "rows.out": {"note": "거래 내역 출금액"},
                  "branch": {"ocr": False}})
    assert source_hash(ID, common=False) == h   # 질문 설정 q 는 그림을 바꾸지 않아 서식 해시(재검수)에 안 들어간다
    _write(form, {"classify": {"answer": "질문 시험서", "aliases": ["시험 서식"]}})
    after = _items(tmp_path)
    kie = after["kie"]
    assert "- memo:" not in kie["prompt"] and "memo" not in {a["key"] for a in kie["answer"]}
    assert "- loan.amount: 대출 신청금액" in kie["prompt"] and "- bank: 은행명" in kie["prompt"]   # 안 적은 칸은 칸의 항목명
    assert "- rows.0.out: 출금 (거래 내역 출금액)" in kie["prompt"]
    assert after["classify"]["answer"] == "질문 시험서" and after["classify"]["eval"]["aliases"] == ["시험 서식"]
    assert "센텀지점" not in after["ocr_page"]["answer"] and "국민은행" in after["ocr_page"]["answer"]
    view = {it["key"]: it for it in FQ.resolved(ID, seeds=2)["kie"]["items"]}
    assert view["memo"]["ask"] is False and view["memo"]["changed"] == ["ask"]
    assert view["loan.amount"]["q_label"] == "대출 신청금액" and view["loan.amount"]["label"] == "신청금액"

    body = json.loads(json.dumps(FIELDS))
    body["q"] = {"bank": {"label": "은행명"}}   # 칸 줄이 없거나(부모 값·체크·도장) 줄 밖에 적고 싶을 때: 맨 위 q 묶음
    (form / "fields.json").write_text(json.dumps(body, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    assert source_hash(ID, common=False) == h
    _write(form, {"kie": {"others": "skip"}})   # 예전 꼴 "others" 는 읽지 않고 (check 가 알려 줌) 모든 칸을 묻는다
    assert "- bank: 은행명" in _items(tmp_path)["kie"]["prompt"]
    assert any("others" in w for w in FQ.check_dir(form))
    (form / "questions.json").unlink()
    _set_q(form, {})
    assert _items(tmp_path) == before


def test_slim_turns_an_old_full_copy_into_only_the_changes(form, tmp_path):
    before = _items(tmp_path)
    full = {task: {"prompt": FQ.common_prompt(task), "line": "- {key}: {label}{note}", "answer": "list_box", "others": "ask",
                   "items": [{"key": it["key"], "label": it["label"], "from": "x"} for it in FQ.resolved(ID, seeds=2)[task]["items"]]}
            for task in ("kie", "marks")}
    full |= {"ocr_field": {"prompt": FQ.common_prompt("ocr_field"), "exclude": []}, "ocr_page": {"prompt": FQ.common_prompt("ocr_page"), "exclude": []},
             "classify": {"prompt": FQ.common_prompt("classify"), "answer": "질문 시험", "aliases": []}, "extra": []}
    _write(form, full)
    assert _items(tmp_path) == before   # 예전 꼴(전체 사본)도 그대로 읽힌다
    assert FQ.slim(ID, full) == {}
    full["kie"]["items"][1]["label"] = "지점"
    assert FQ.slim(ID, full) == {"kie": {"items": [{"key": "branch", "label": "지점"}]}}
    assert FQ.write(ID, {}) is None and not (form / "questions.json").exists()


def test_extra_questions_are_form_qa_items_answered_from_the_fields(form, tmp_path):
    body = {}
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



def test_checks_catch_bad_files_missing_keys_and_mismatches(form):
    (form / "questions.json").write_text('{"kie": {"items": [{"label": "x"}]}, "extra": [{"id": "a b", "type": "date"}], "oops": 1}',
                                         encoding="utf-8")
    why = FQ.check_dir(form)
    assert any("모르는 항목" in w for w in why) and any("fields.json" in w and "q" in w for w in why)
    assert any("id 가 없거나" in w for w in why) and any("type 은" in w for w in why)
    assert any(p["id"] == ID and "questions.json" in p["reason"] for p in refresh()["problems"])

    _set_q(form, {"bank": {"asked": 1}})
    _write(form, {"extra": [{"id": "x", "prompt": "?", "type": "text", "answer": "{nope}"}]})
    assert any("모르는 칸 'asked'" in p and "fields.json:" in p for p in FQ.check(ID, seeds=2)["problems"])
    _set_q(form, {"bank": {"label": "거래은행"}, "memo": {"ask": False}})
    r = FQ.check(ID, seeds=2)
    assert any("extra x" in p and "nope" in p for p in r["problems"])
    assert any("항목명과 다르게" in n and "거래은행" in n for n in r["notes"])
    assert any("묻지 않는 칸" in n and "memo" in n for n in r["notes"])


def test_question_and_answer_templates_come_from_the_form_file(form, tmp_path):
    view = FQ.resolved(ID, seeds=2)["kie"]
    assert view["item"] == "- {key}: {label}{note}" and view["answer_empty"] == {"key": "{key}", "value": None}
    assert view["answer"] == {"key": "{key}", "value": "{value}", "bbox_2d": "{bbox_2d}", "page": "{page}"}

    body = {"kie": {"prompt": '이 증명서에서 아래 항목을 [{"항목": 키, "값": 적힌 값}] 목록으로 답하세요.\n{items}',
                    "item": "* {label} → {key}", "answer": {"항목": "{key}", "값": "{value}"}, "answer_empty": {"항목": "{key}", "값": "없음"}},
            "classify": {"prompt": "서류 이름만 답하세요."}}
    _write(form, body)
    got = _items(tmp_path)
    kie = got["kie"]
    assert kie["prompt"].startswith("이 증명서에서") and "* 은행명 → bank" in kie["prompt"]
    assert kie["answer"][0] == {"항목": "bank", "값": "국민은행"}   # 틀 그대로, 위치 자리가 없으니 위치 없음
    assert {"항목": "memo", "값": "없음"} in kie["answer"]          # 빈 칸 틀
    assert kie["eval"]["answer_fields"] == {"key": "항목", "value": "값"}
    assert got["classify"]["prompt"] == "서류 이름만 답하세요."
    s = SCORERS["kie"](kie, oracle_output(kie))["metrics"]
    assert "vl_f1" not in s and main_metric("kie", s) == "f1" and s["f1"] == 1   # 칸 이름을 거꾸로 읽고, 위치 점수는 뺌
    wrong = json.dumps([{"항목": "bank", "값": "신한은행"}], ensure_ascii=False)
    assert SCORERS["kie"](kie, wrong)["metrics"]["f1"] < 1

    r = FQ.check(ID, seeds=2)
    assert not r["problems"] and any("kie: 질문 문장이 공통 문장과 다릅니다" in n for n in r["notes"])
    body["kie"]["prompt"] = "아래 항목의 값을 목록으로 답하세요.\n{items}"   # 답 틀의 칸 이름을 질문에 안 적음
    _write(form, body)
    assert any("질문 문장에 없습니다" in p and "항목" in p for p in FQ.check(ID, seeds=2)["problems"])

    body["kie"] = {"prompt": "항목 자리 없음", "answer": {"value": "{value}"}, "line": "- {key}"}
    _write(form, body)
    why = FQ.check_dir(form)
    assert any("{items}" in w for w in why) and any('"{key}"' in w for w in why) and any("line → item" in w for w in why)


def test_editor_save_keeps_question_settings(form):
    """html 편집기 저장(칸 선언을 통째로 바꿈)도 칸의 q 를 지우지 않는다."""
    from docgen import formfields

    _set_q(form, {"memo": {"ask": False}, "rows.out": {"note": "출금액"}})
    plain = json.loads(json.dumps(FIELDS))
    plain["fields"]["memo"]["label"] = "비고란"   # 편집기가 보낸 새 선언 (q 없음)
    formfields.update(ID, {"fields": plain["fields"], "lists": plain["lists"]}, formfields.VALUE_KEYS)
    body = json.loads((form / "fields.json").read_text(encoding="utf-8"))
    assert body["fields"]["memo"] == {**plain["fields"]["memo"], "q": {"ask": False}}
    assert body["lists"]["rows"]["fields"]["out"]["q"] == {"note": "출금액"}


def test_marks_answer_with_renamed_fields_is_scored_like_the_default():
    tpl, empty = {"항목": "{key}", "선택": "{value}", "bbox_2d": "{bbox_2d}", "page": "{page}"}, {"항목": "{key}", "선택": None}
    ans = [FQ.fill_answer(tpl, empty, "consent", "동의", {"bbox_2d": [10, 10, 20, 20], "page": 1}),
           FQ.fill_answer(tpl, empty, "seal", False, {}), FQ.fill_answer(tpl, empty, "agree2", None, {})]
    assert ans == [{"항목": "consent", "선택": "동의", "bbox_2d": [10, 10, 20, 20], "page": 1}, {"항목": "seal", "선택": False},
                   {"항목": "agree2", "선택": None}]
    item = {"task": "marks", "answer": ans, "eval": {"types": {"consent": "checkbox", "seal": "seal", "agree2": "checkbox"},
                                                     "answer_fields": FQ.answer_fields(tpl)}}
    assert SCORERS["marks"](item, oracle_output(item))["metrics"]["acc"] == 1
    wrong = json.dumps([{"항목": "consent", "선택": "부동의"}, {"항목": "seal", "선택": True}], ensure_ascii=False)
    assert SCORERS["marks"](item, wrong)["metrics"]["acc"] < 1
