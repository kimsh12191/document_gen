"""cross_check 과제용: 서류 묶음에서 '여러 서류에 같이 나오는 값'을 찾아 한 서류에서만 바꾼다.

실제 심사에서 잡아야 하는 불일치(신청서 성명 오기, 주민번호 한 자리 틀림, 주소 번지 다름, 금액 다름,
계좌번호 한 자리 다름)를 흉내 낸다. 값은 HTML 의 <span data-field> 안 글자만 바꿔 다시 렌더링하므로
바뀐 서류의 나머지 모양은 원본과 같다.
"""
from __future__ import annotations

import random
import re
from datetime import date, timedelta

from markupsafe import Markup, escape

from .metrics import norm_text

# 서류끼리 맞춰 봐야 하는 항목 (항목명 기준)
SHARED_LABEL = re.compile(r"성명|이름|예금주|대표자|주민등록번호|생년월일|주소|소재지|연락처|전화|휴대|계좌|상호|법인명|회사명|"
                          r"사업자등록번호|법인등록번호|금액|대금|보증금|채권최고액|근무처|직장명")
# 같은 값이 여러 서류에 나와도 대조 대상이 아닌 것 (은행·지점, 발급·작성일 등)
SKIP_LABEL = re.compile(r"은행|지점|취급점|발급|작성일|신청일|수수료|담당|책임자")
NAME_LABEL = re.compile(r"성명|이름|예금주|대표자")
SYLLABLES = "김이박최정강조윤장임한오서신권황안송류홍민서준지우현수영진하은도연서윤재성혜경미선희정호석"


def _span(key: str, text: str) -> str:
    body = escape(text).replace("\n", Markup("<br>"))
    return f'<span class="fv" data-field="{escape(key)}">{body}</span>'


def visible_keys(html: str) -> set[str]:
    """화면에 글자로 보이는 값 칸의 키 (원본 서식의 투명 칸·체크 보기 칸 제외)."""
    hidden = set(re.findall(r'<div class="(?:ov hid|opt)"[^>]*>\s*<span class="fv" data-field="([^"]+)"', html))
    return set(re.findall(r'data-field="([^"]+)"', html)) - hidden


def candidates(docs: list[dict]) -> list[list[tuple[int, int]]]:
    """같은 값이 두 서류 이상에 나오는 묶음들. 원소는 (서류 번호, 필드 번호).

    docs[i] = {"fields": 라벨 필드, "raw_keys": 필드별 HTML 키, "visible": 보이는 키 집합}"""
    by_val: dict[str, list[tuple[int, int]]] = {}
    for di, d in enumerate(docs):
        for fi, f in enumerate(d["fields"]):
            v, lab = f.get("value"), f.get("label") or ""
            if (v is None or f["type"] in ("checkbox", "checkbox_multi", "seal", "signature") or f.get("bbox") is None
                    or fi >= len(d["raw_keys"]) or d["raw_keys"][fi] not in d["visible"]
                    or not SHARED_LABEL.search(lab) or SKIP_LABEL.search(lab)):
                continue
            nv = norm_text(v)
            if len(nv) < 2 or "*" * 3 in nv:  # 가린 값(******)은 대조할 수 없다
                continue
            if f["type"] in ("amount", "amount_korean", "number"):  # '327,000,000' 과 '327,000,000원' 은 같은 값
                if not isinstance(f.get("norm"), (int, float)) or abs(f["norm"]) < 10000:
                    continue
                nv = f"#{f['norm']:g}"
            elif f["type"] in ("date", "phone"):
                nv = f"{f['type']}:{f.get('norm')}"
            by_val.setdefault(nv, []).append((di, fi))
    groups = []
    for occ in by_val.values():
        if len({di for di, _ in occ}) >= 2:
            groups.append(occ)
    return groups


def _change_digit(s: str, rng: random.Random, positions: list[int]) -> str:
    i = rng.choice(positions)
    d = int(s[i])
    return s[:i] + str((d + rng.randint(1, 9)) % 10) + s[i + 1:]


def _shift_day(value: str, iso: str, rng: random.Random) -> str | None:
    """날짜 표시 형식은 그대로 두고 일(日)만 바꾼다."""
    try:
        d0 = date.fromisoformat(iso)
    except (TypeError, ValueError):
        return None
    runs = list(re.finditer(r"\d+", value))
    if len(runs) < 3:
        return None
    for _ in range(10):
        d1 = d0 + timedelta(days=rng.choice([-1, 1]) * rng.randint(1, 9))
        if d1.month == d0.month:
            break
    else:
        return None
    r = runs[2]
    day = f"{d1.day:0{len(r.group())}d}" if r.group().startswith("0") else str(d1.day)
    return value[:r.start()] + day + value[r.end():]


def shift_date(value: str, iso: str, days: int) -> str | None:
    """날짜 표시 형식(구분자·자릿수)은 그대로 두고 날짜를 days 만큼 옮긴다. '2025년 9월 20일' → '2025년 6월 12일'."""
    try:
        d1 = date.fromisoformat(iso) + timedelta(days=days)
    except (TypeError, ValueError):
        return None
    runs = list(re.finditer(r"\d+", value))
    if len(runs) != 3:
        return None
    padded = all(len(r.group()) == 2 for r in runs[1:])  # '2025.02.02' 처럼 월·일이 두 자리 형식
    out, last = [], 0
    for i, (r, n) in enumerate(zip(runs, (d1.year, d1.month, d1.day))):
        s = r.group()
        if i == 0:
            txt = f"{n % 100:02d}" if len(s) == 2 else str(n)
        else:
            txt = f"{n:02d}" if padded else str(n)
        out.append(value[last:r.start()] + txt)
        last = r.end()
    return "".join(out) + value[last:]


def mutate(f: dict, rng: random.Random) -> str | None:
    """필드 값을 '그럴듯하게 틀린' 값으로 바꾼다. 못 바꾸면 None."""
    v: str = f["value"]
    t, lab = f["type"], f.get("label") or ""
    if t == "date" and (out := _shift_day(v, f.get("norm"), rng)):
        return out
    if t in ("amount", "amount_korean", "number"):
        start = v.find("(") + 1  # '금 오억원정 (₩520,000,000)' 은 괄호 안 숫자를 바꾼다
        digits = [m.start() + start for m in re.finditer(r"\d", v[start:])]
        if len(digits) >= 3:
            # 앞쪽 두 자리 중 하나를 바꾼다 (금액이 눈에 띄게 다르게)
            return _change_digit(v, rng, digits[:2])
    if NAME_LABEL.search(lab) and re.fullmatch(r"[가-힣]{2,5}", v.strip()):
        s = v.strip()
        i = rng.randrange(1, len(s))  # 성은 그대로
        c = rng.choice([x for x in SYLLABLES if x != s[i]])
        return v.replace(s, s[:i] + c + s[i + 1:], 1)
    digits = [m.start() for m in re.finditer(r"\d", v)]
    if digits:
        if t == "rrn":  # 뒷자리 첫 숫자(성별)는 그대로 두고 나머지에서
            digits = [i for i in digits if i != v.find("-") + 1] or digits
        return _change_digit(v, rng, digits[-6:] if len(digits) > 6 else digits)
    syl = [i for i, c in enumerate(v) if "가" <= c <= "힣"]
    if len(syl) >= 2:
        i = rng.choice(syl[1:])
        return v[:i] + rng.choice([x for x in SYLLABLES if x != v[i]]) + v[i + 1:]
    return None


def apply(html: str, raw_key: str, old: str, new: str) -> str | None:
    """HTML 에서 그 칸의 글자만 바꾼다. 칸을 못 찾으면 None."""
    a = _span(raw_key, old)
    if html.count(a) != 1:
        return None
    return html.replace(a, _span(raw_key, new))
