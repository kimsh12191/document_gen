"""평가 문항의 질문 문장 (build 가 쓰고, studio·학습 실행도 같은 문장으로 묻는다).

문장 원본은 docgen/forms/_common/questions.json (모든 서식의 기본값 — 서식 폴더의 questions.json 에 없으면 이것).
여기서는 그 글을 읽어 format 용 틀(P_KIE 등, JSON 중괄호는 {{ }})로 바꿔 둔다. 문장은 그 JSON 에서 고친다.
표준 라이브러리만 쓰므로 렌더링 환경(jinja2·Playwright)이 없어도 import 된다.
문장을 바꾸면 guide/questions.md 도 같이 고친다 (docgen/tests/test_bench.py 가 둘이 같은지 본다).
"""
import json
import re
from pathlib import Path

COMMON = Path(__file__).resolve().parents[1] / "forms" / "_common" / "questions.json"
DEFAULTS = json.loads(COMMON.read_text(encoding="utf-8"))   # {과제: {"prompt", "line"?, "answer"?}}


def _fmt(text: str, names: tuple = ()) -> str:
    """사람이 쓴 글 → format 틀: 중괄호를 모두 {{ }} 로 감추고 자리(names)만 되살린다."""
    out = text.replace("{", "{{").replace("}", "}}")
    return re.sub(r"\{\{(" + "|".join(names) + r")\}\}", r"{\1}", out) if names else out


P_CLASSIFY = _fmt(DEFAULTS["classify"]["prompt"])
P_OCR_PAGE = _fmt(DEFAULTS["ocr_page"]["prompt"])
P_OCR_FIELD = _fmt(DEFAULTS["ocr_field"]["prompt"])
# kie·marks 는 값과 함께 위치를 답한다 (평가 세트 2.0). 좌표는 OCR 과제와 같은 bbox_2d: 그 쪽 이미지 기준 0~1000 정수.
P_KIE = _fmt(DEFAULTS["kie"]["prompt"], ("items",))
P_MARKS = _fmt(DEFAULTS["marks"]["prompt"], ("items",))
P_DOC_CHECK = _fmt(DEFAULTS["doc_check"]["prompt"], ("customer", "task", "required"))
P_CROSS = _fmt(DEFAULTS["cross_check"]["prompt"], ("customer", "task", "n", "pages"))
# freetext: 기타·비고·사유 칸의 자유 기재를 DB 칸으로. 보기 목록은 docgen/freetext.py (freetext_prompt 가 채운다)
P_FREETEXT = _fmt(DEFAULTS["freetext"]["prompt"], ("label", "basis", "purposes", "reasons", "requests"))
P_REVIEW = _fmt(DEFAULTS["review"]["prompt"], ("task", "pages", "question"))
LINE = DEFAULTS["kie"]["item"]   # 질문의 항목 한 줄 틀 (서식의 questions.json 의 item 으로 바꿀 수 있다)


def freetext_prompt(label: str, basis: str) -> str:
    from ..freetext import PURPOSES, REASONS, REQUESTS

    return P_FREETEXT.format(label=label, basis=basis, purposes=", ".join(PURPOSES), reasons=", ".join(REASONS),
                             requests=", ".join(REQUESTS))


def kie_line(form_id: str | None, key: str, label: str | None, doc_key: str | None = None, extra: str = "",
             siblings: list[dict] | None = None, note: str | None = None, line: str | None = None) -> str:
    """kie·marks 항목 한 줄: '- 키: 항목명 (설명)'. 설명은 키 사전의 누구의 무엇과 표의 행 (docgen.dictionary.describe).
    extra 는 marks 의 종류·보기처럼 괄호에 같이 넣을 것. siblings(그 문서의 같은 과제 칸, 문서 순서)에 항목명이 같은 칸이
    또 있으면 몇 번째 칸인지 붙인다 (작성일·작성일2 처럼 행 번호가 없는 반복 칸)."""
    if note is not None:   # 칸 목록 fields.json 의 그 칸 "q": {"note"} 그대로 (docgen/formquestions.pick)
        return item_line(key, label, ", ".join(x for x in [note, extra] if x), line)
    from .. import dictionary as DIC

    desc = DIC.describe(form_id, key, label, doc_key)
    same = [s["key"] for s in siblings or [] if DIC._norm(s.get("label") or "") == DIC._norm(label or "")]
    me = key if key in same else doc_key   # 공통 키로 묻는 칸은 서식의 키로 찾는다
    if label and len(same) > 1 and me in same and not any(p.isdigit() for p in key.split(".")):
        desc = ", ".join(x for x in [desc, f"같은 항목명 중 {same.index(me) + 1}번째 칸"] if x)
    return item_line(key, label, ", ".join(x for x in [desc, extra] if x), line)


def item_line(key: str, label: str | None, note: str, line: str | None = None) -> str:
    """{key}·{label}(없으면 -)·{note}(괄호 설명, 없으면 빈칸)를 채운다. 글자 그대로 바꿔 넣는다 (항목명에 중괄호가 있어도 됨)."""
    return ((line or LINE).replace("{key}", key).replace("{label}", label or "-")
            .replace("{note}", f" ({note})" if note else ""))


def text_of(template: str) -> str:
    """format 용 틀(P_KIE 의 {{ }})을 사람이 읽고 고치는 글로: {{ → {, }} → }. {items} 같은 자리는 그대로."""
    return template.replace("{{", "{").replace("}}", "}")

