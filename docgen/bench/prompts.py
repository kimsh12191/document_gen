"""평가 문항의 질문 문장 (build 가 쓰고, studio·학습 실행도 같은 문장으로 묻는다).

문장 원본은 docgen/forms/_common/questions.json (모든 서식의 기본값 — 서식 폴더의 questions.json 에 없으면 이것).
여기서는 그 글을 읽어 format 용 틀(P_KIE 등, JSON 중괄호는 {{ }})로 바꿔 둔다. 문장은 그 JSON 에서 고친다.
표준 라이브러리만 쓰므로 렌더링 환경(jinja2·Playwright)이 없어도 import 된다.
문장을 바꾸면 guide/reference/questions.md 도 같이 고친다 (docgen/tests/test_bench.py 가 둘이 같은지 본다).
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
# freetext: 기타·비고·사유 칸의 자유 기재를 DB 칸으로. 보기 목록은 docgen/freetext.py (freetext_prompt 가 채운다)
P_FREETEXT = _fmt(DEFAULTS["freetext"]["prompt"], ("label", "basis", "purposes", "reasons", "requests"))
LINE = DEFAULTS["kie"]["item"]   # 질문의 항목 한 줄 틀 (서식의 questions.json 의 item 으로 바꿀 수 있다)
# 표(목록) 과제 (docgen/bench/tasks/table*.py). {target} 표를 가리키는 말, {scope} 범위 (없으면 빈칸), {columns} 열 줄들
P_TABLE = _fmt(DEFAULTS["table"]["prompt"], ("target", "scope", "columns"))
P_TABLE_READ = _fmt(DEFAULTS["table_read"]["prompt"], ("target", "scope"))
P_TABLE_FIND = _fmt(DEFAULTS["table_find"]["prompt"])
P_TABLE_QA = _fmt(DEFAULTS["table_qa"]["prompt"], ("target", "question"))
COLUMN = DEFAULTS["table"]["column"]   # 열 한 줄 틀


def table_target(how: str, title: str | None = None, labels: list[str] | None = None, box: list[int] | None = None,
                 page: int | None = None) -> str:
    """표를 가리키는 말. how: title (제목) / header (머리글 두어 개) / box (위치) / only (표가 하나뿐인 서류)."""
    if how == "title":
        return f"'{title}' 표"
    if how == "header":
        return "·".join(f"'{x}'" for x in labels) + " 열이 있는 표"
    if how == "box":
        return f"{page}쪽 bbox_2d={json.dumps(box)} 위치의 표"
    return "표"


def table_scope(page: int | None = None, first: int | None = None) -> str:
    """범위: 그 쪽의 행만 / 앞에서부터 몇 행까지. 없으면 빈칸 (모든 행)."""
    if page:
        return f" (단, {page}쪽에 있는 행만)"
    if first:
        return f" (단, 앞에서부터 {first}행까지만)"
    return ""


def column_line(key: str, label: str | None, note: str | None = None) -> str:
    """표 열 한 줄 '- 키: 항목명 (설명)'. 설명은 칸 목록 fields.json 의 그 열 칸 "q": {"note"} (없으면 뺌)."""
    return COLUMN.replace("{key}", key).replace("{label}", label or "-").replace("{note}", f" ({note})" if note else "")


def freetext_prompt(label: str, basis: str) -> str:
    from ..freetext import PURPOSES, REASONS, REQUESTS

    return P_FREETEXT.format(label=label, basis=basis, purposes=", ".join(PURPOSES), reasons=", ".join(REASONS),
                             requests=", ".join(REQUESTS))


def _norm(s: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]", "", (s or "").lower())


def row_of(key: str) -> str:
    """표 칸이면 몇 번째 행인지: "debts.1.balance" → "2행", "기업부담금_목록.0.상품명" → "기업부담금 목록 1행" (행은 0부터 센다)."""
    segs = key.split(".")
    nums = [i for i, s in enumerate(segs) if s.isdigit()]
    if not nums:
        return ""
    i = nums[0]
    table = ".".join(segs[:i]).replace("_", " ")   # 한글 키면 표 이름으로 쓴다
    table = table + " " if re.search(r"[가-힣]", table) else ""
    return f"{table}{int(segs[i]) + 1}{'번째' if i == len(segs) - 1 else '행'}"


def kie_line(key: str, label: str | None, extra: str = "", siblings: list[dict] | None = None,
             note: str | None = None, line: str | None = None) -> str:
    """kie·marks 항목 한 줄: '- 키: 키 설명 (덧붙임)'. 키·키 설명은 서식의 칸 그대로(fields.json·템플릿).
    덧붙임은 표의 몇 번째 행, extra(marks 의 종류·보기), 키 설명이 같은 칸이 또 있으면 몇 번째 칸인지
    (작성일·작성일2 처럼 행 번호가 없는 반복 칸). 칸에 질문 설명 q.note 를 적었으면 그것만 쓴다."""
    if note is not None:   # 칸 목록 fields.json 의 그 칸 "q": {"note"} 그대로 (docgen/formquestions.pick)
        return item_line(key, label, ", ".join(x for x in [note, extra] if x), line)
    desc = row_of(key)
    desc = "" if _norm(desc) == _norm(label or "") else desc
    same = [s["key"] for s in siblings or [] if _norm(s.get("label") or "") == _norm(label or "")]
    if label and len(same) > 1 and key in same and not any(p.isdigit() for p in key.split(".")):
        desc = ", ".join(x for x in [desc, f"같은 설명 중 {same.index(key) + 1}번째 칸"] if x)
    return item_line(key, label, ", ".join(x for x in [desc, extra] if x), line)


def item_line(key: str, label: str | None, note: str, line: str | None = None) -> str:
    """{key}·{label}(없으면 -)·{note}(괄호 설명, 없으면 빈칸)를 채운다. 글자 그대로 바꿔 넣는다 (항목명에 중괄호가 있어도 됨)."""
    return ((line or LINE).replace("{key}", key).replace("{label}", label or "-")
            .replace("{note}", f" ({note})" if note else ""))


def text_of(template: str) -> str:
    """format 용 틀(P_KIE 의 {{ }})을 사람이 읽고 고치는 글로: {{ → {, }} → }. {items} 같은 자리는 그대로."""
    return template.replace("{{", "{").replace("}}", "}")

