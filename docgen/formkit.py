"""서식 생성 스크립트(서식 폴더의 generate.py)가 쓰는 도우미. 칸 목록(fields.json)이 만든 값은 글자라서
날짜·금액을 숫자로 바꿔 계산하고, 같은 표기로 되돌린다.

    from docgen.formkit import to_date, date_like, to_amount, amount_like, won_korean, rows

    def adjust(d, p, rng):
        s, e = to_date(d["period"]["start"]), to_date(d["period"]["end"])
        if s and e and s > e:
            d["period"]["start"], d["period"]["end"] = date_like(e, d["period"]["start"]), date_like(s, d["period"]["end"])
        d["total"]["out"] = amount_like(sum(to_amount(r["out"]) or 0 for r in rows(d, "rows")), d["total"]["out"])
        return d

연결점·약속은 docgen/htmlform.py (run_script), 설명은 docgen/manual/NEW_FORM_SPEC.md 8절.
"""
from __future__ import annotations

import re
from datetime import date, timedelta

from .korean import won_korean   # noqa: F401  (스크립트가 여기서 가져다 쓴다: 120000000 → '일억이천만')

__all__ = ["to_date", "date_like", "date_style", "to_amount", "amount_like", "won_korean", "rows", "add_days", "get", "put",
           "FORMATS", "fmt"]

_DATE = re.compile(r"(\d{4})\s*[.\-/년]\s*(\d{1,2})\s*[.\-/월]\s*(\d{1,2})")


def to_date(s) -> date | None:
    """'2025.01.03' · '2025-01-03' · '2025/1/3' · '2025년 1월 3일' → date. 읽지 못하면 None."""
    if isinstance(s, date):
        return s
    m = _DATE.search(str(s or ""))
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def date_style(like) -> str:
    """보기 글자의 날짜 표기: dot · dash · slash · kor(0 채움) · kor_short."""
    s = str(like or "")
    if "년" in s:
        return "kor" if re.search(r"월\s*0\d|년\s*0\d", s) else "kor_short"
    for sep, style in (("-", "dash"), ("/", "slash")):
        if re.search(rf"\d{sep}\d", s):
            return style
    return "dot"


def date_like(d: date, like=None) -> str:
    """date → like 와 같은 표기의 글자 (like 가 없으면 2025.01.03)."""
    from .korean import fmt_date

    return fmt_date(d, date_style(like))


def add_days(s, days: int):
    """날짜 글자에 days 일을 더해 같은 표기로. 읽지 못하면 그대로."""
    d = to_date(s)
    return date_like(d + timedelta(days=days), s) if d else s


def to_amount(s) -> int | None:
    """'1,234,000원' · '₩1,234,000' · '-12,000' → 정수. 숫자가 없으면 None."""
    if isinstance(s, (int, float)):
        return int(s)
    t = str(s or "")
    digits = re.sub(r"[^0-9]", "", t.split(".")[0])
    if not digits:
        return None
    return -int(digits) if re.match(r"^\s*[-−△▲]", t) else int(digits)


def amount_like(n: int, like=None) -> str:
    """정수 → like 와 같은 꼴 (쉼표, 앞뒤 글자 '원'·'₩'·'USD ' 등 유지). like 가 없으면 '1,234,000'."""
    s = str(like or "")
    m = re.match(r"^(\D*?)[-−]?[\d,]+(\.\d+)?(\D*)$", s.strip())
    head, tail = (m.group(1), m.group(3)) if m else ("", "")
    comma = "," in s or not s
    body = f"{abs(n):,}" if comma else str(abs(n))
    return f"{head}{'-' if n < 0 else ''}{body}{tail}"


def rows(d: dict, name: str) -> list[dict]:
    """반복 표의 행 목록 (없으면 빈 목록)."""
    v = get(d, name)
    return [r for r in v if isinstance(r, dict)] if isinstance(v, list) else []


def get(d: dict, key: str, default=None):
    """점 경로로 값 읽기: get(d, "period.start")."""
    cur = d
    for k in key.split("."):
        if isinstance(cur, list) and k.isdigit() and int(k) < len(cur):
            cur = cur[int(k)]
        elif isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return default
    return cur


def put(d: dict, key: str, value) -> None:
    """점 경로로 값 쓰기: put(d, "total.out", "1,000"). 중간 칸이 없으면 만든다."""
    parts = key.split(".")
    cur = d
    for k in parts[:-1]:
        nxt = cur.get(k)
        if not isinstance(nxt, dict):
            nxt = cur[k] = {}
        cur = nxt
    cur[parts[-1]] = value


# 칸의 표기 형식 (영역 편집기의 '표기', fields.json 칸의 "fmt"). 값이 그 꼴로 읽히지 않으면 그대로 둔다.
FORMATS = {
    "date.dot": ("날짜 2025.01.31", "2025.01.31"), "date.dash": ("날짜 2025-01-31", "2025-01-31"),
    "date.slash": ("날짜 2025/01/31", "2025/01/31"), "date.kor": ("날짜 2025년 01월 31일", "2025년 01월 31일"),
    "date.kor_short": ("날짜 2025년 1월 31일", "2025년 1월 31일"), "date.yymmdd": ("날짜 250131 (6자리)", "250131"),
    "date.yyyymmdd": ("날짜 20250131 (8자리)", "20250131"), "date.yy_dot": ("날짜 25.01.31", "25.01.31"),
    "amount.comma": ("금액 1,234,000", "1,234,000"), "amount.won": ("금액 1,234,000원", "1,234,000원"),
    "amount.plain": ("금액 1234000 (쉼표 없음)", "1234000"), "amount.korean": ("금액 일백이십삼만사천원", "일백이십삼만사천원"),
    "amount.korean_full": ("금액 일금 일백이십삼만사천원정", "일금 일백이십삼만사천원정"),
    "digits.plain": ("숫자만 (- 빼기: 01012345678)", "01012345678"),
    "text.upper": ("영문 대문자", "HONG GILDONG"),
}


def fmt(value, style: str | None):
    """값을 표기 형식으로 (FORMATS). 빈 값·모르는 형식·읽지 못하는 값은 그대로."""
    if value in (None, "") or not style or style not in FORMATS:
        return value
    s = str(value)
    if style.startswith("date."):
        d = to_date(s) or _compact_date(s)
        if not d:
            return value
        return {"date.dot": f"{d:%Y.%m.%d}", "date.dash": f"{d:%Y-%m-%d}", "date.slash": f"{d:%Y/%m/%d}",
                "date.kor": f"{d.year}년 {d.month:02d}월 {d.day:02d}일", "date.kor_short": f"{d.year}년 {d.month}월 {d.day}일",
                "date.yymmdd": f"{d:%y%m%d}", "date.yyyymmdd": f"{d:%Y%m%d}", "date.yy_dot": f"{d:%y.%m.%d}"}[style]
    if style.startswith("amount."):
        n = to_amount(s)
        if n is None:
            return value
        return {"amount.comma": f"{n:,}", "amount.won": f"{n:,}원", "amount.plain": str(n),
                "amount.korean": f"{won_korean(abs(n))}원", "amount.korean_full": f"일금 {won_korean(abs(n))}원정"}[style]
    if style == "digits.plain":
        return re.sub(r"[^0-9]", "", s) or value
    if style == "text.upper":
        return s.upper()
    return value


def _compact_date(s: str) -> date | None:
    """'20250131' · '250131' → date (생년월일 6자리는 앞 두 자리로 세기를 고른다)."""
    m = re.fullmatch(r"\s*(\d{8}|\d{6})\s*", s)
    if not m:
        return None
    t = m.group(1)
    y, rest = (int(t[:4]), t[4:]) if len(t) == 8 else ((1900 if int(t[:2]) > 30 else 2000) + int(t[:2]), t[2:])
    try:
        return date(y, int(rest[:2]), int(rest[2:]))
    except ValueError:
        return None
