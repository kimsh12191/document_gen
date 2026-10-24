"""기타 칸 정리(freetext) 과제: 비고·기타·사유·용도 칸에 사람이 대충 쓴 듯한 글과, 그 글을 DB 칸으로 정리한 정답.

칸 종류(용도·사유·비고)별 문장 틀(docgen/freetext_templates.json, 130여 개)을 골라 자리({amount}, {date} …)를
채운다. 정답 = 채운 값 + 틀에 정해 둔 값(set) → 글과 정답이 늘 맞는다.
  레코드 키: purpose(용도 보기), reason(사유 보기), amount(원 정수), date(YYYY-MM-DD), period_months(개월),
            request(요청 보기), memo(다른 키에 맞지 않는 말, 글에 적힌 그대로), approx(대략적인 값의 키 목록)
  적히지 않은 키는 레코드에 없다 (null 을 쓰지 않는다).

생성기(realform.build_form)가 make() 로 글을 만들면, render() 가 열어 둔 collect() 에 {글: 정답} 이 쌓이고
data["_freetext"] 로 bench build 까지 간다 (docgen/bench/build.py 가 freetext 문항을 낸다).
"""
from __future__ import annotations

import calendar
import json
import random
import re
import threading
from contextlib import contextmanager
from datetime import date, timedelta
from functools import lru_cache
from pathlib import Path

KEYS = ("purpose", "reason", "amount", "date", "period_months", "request", "memo")

# 보기(DB 값) → 글에 쓰는 표현. 틀(freetext_templates.json)의 {purpose}·{reason}·{request} 자리에 들어가므로
# 용도·사유는 명사꼴, 요청은 문장 끝에 오는 꼴로 쓴다.
PURPOSES = {
    "생활자금": ["생활비", "생활자금", "생활 안정자금"],
    "주택구입": ["주택 구입", "집 구입", "아파트 매수", "주택매입"],
    "전세자금": ["전세 보증금", "전세금", "전세자금"],
    "사업자금": ["가게 운영비", "사업 운영자금", "사업자금", "매장 인테리어"],
    "학자금": ["대학 등록금", "학비", "학자금"],
    "자녀 교육비": ["애 학원비", "자녀 교육비", "아이 유학비"],
    "의료비": ["병원비", "수술비", "치료비"],
    "결혼자금": ["결혼 준비", "혼수", "결혼자금"],
    "차량구입": ["차 구입", "자동차 구입", "차량 구입"],
}
REASONS = {
    "만기 해지": ["만기 해지", "만기", "적금 만기"],
    "해외 이주": ["해외 이주", "이민", "해외 이사"],
    "타행 이체": ["타행 이체", "타행 이전", "다른 은행 이전"],
    "급여 수령": ["급여 수령", "급여계좌 변경", "월급 통장 변경"],
    "본인 요청": ["본인 요청", "고객 요청", "본인 희망"],
    "계좌 정리": ["계좌 정리", "통장 정리", "안 쓰는 계좌 정리"],
    "주소 변경": ["주소 변경", "주소 이전", "이사"],
    "분실": ["분실", "통장 분실", "카드 분실"],
}
REQUESTS = {
    "서류 추가 제출": ["서류 추가 제출 예정", "추가서류 낼게요", "서류 보완 예정", "소득서류 추가 제출"],
    "전화 연락": ["전화 주세요", "연락 바람", "전화 요망"],
    "우편 발송": ["우편으로 보내주세요", "우편 발송 요청"],
    "문자 안내": ["문자로 안내", "문자 주세요"],
    "방문 예정": ["다시 방문 예정", "지점 방문 예정", "재방문"],
}
MEMOS = ["배우자 동의함", "보증인 없음", "급여이체 예정", "기존 대출 상환 후 신청", "상담 후 결정",
         "신분증 사본 첨부", "자동이체 같이 신청", "가족 명의 계좌 있음", "등본 첨부", "대리인 방문"]
# 용도별 금액 (만원): 학자금 3억 같은 어색한 조합을 막는다. 용도 없으면 GENERAL
AMOUNTS = {
    "생활자금": [300, 500, 800, 1000, 1500, 2000, 3000, 5000], "주택구입": [10000, 15000, 20000, 30000, 40000, 50000],
    "전세자금": [5000, 8000, 10000, 15000, 20000, 30000], "사업자금": [1000, 2000, 3000, 5000, 10000, 20000],
    "학자금": [300, 400, 500, 800, 1000, 1500], "자녀 교육비": [100, 200, 300, 500, 1000, 2000],
    "의료비": [100, 200, 300, 500, 1000, 3000], "결혼자금": [1000, 2000, 3000, 5000],
    "차량구입": [1000, 2000, 3000, 4000, 6000],
}
GENERAL = [100, 300, 500, 1000, 2000, 3000, 5000, 10000]
TEMPLATES_PATH = Path(__file__).resolve().parent / "freetext_templates.json"
VOCAB = {"purpose": PURPOSES, "reason": REASONS, "request": REQUESTS}

# 칸 고르기 (항목명, 공백 뺀 것). 용도 칸 → purpose, 사유 칸 → reason, 비고·기타 칸 → 둘 다 올 수 있음
SLOT_PURPOSE = re.compile(r"^(자금)?용도$|자금용도|용도및목적|^(대출|자금)?(사용)?목적$")
SLOT_REASON = re.compile(r"^(해지|변경|정정|거절|취소|해제|재발급|발급|해약|이전|신청)?사유$")
SLOT_NOTE = re.compile(r"^(비고|기타|특기사항|특이사항|참고사항|기타참고사항|기타사항|요청사항|기타요청사항|메모)$")

RATE = 0.4   # 고른 칸 중 자유 기재 글을 넣는 비율 (나머지는 지금처럼 '해당 없음'·단어 하나)

_DIGIT = "영일이삼사오육칠팔구"


def slot_of(label: str) -> str | None:
    s = re.sub(r"\s", "", label or "")
    if SLOT_PURPOSE.search(s):
        return "purpose"
    if SLOT_REASON.search(s):
        return "reason"
    if SLOT_NOTE.search(s):
        return "note"
    return None


def korean_number(n: int) -> str:
    """1~9999 를 한글 수사로 (3000 → 삼천, 1500 → 천오백)."""
    out = ""
    for unit, v in (("천", 1000), ("백", 100), ("십", 10)):
        d = n // v % 10
        if d:
            out += ("" if d == 1 else _DIGIT[d]) + unit
    return out + (_DIGIT[n % 10] if n % 10 else "")


def _amount(r: random.Random, purpose: str | None = None) -> tuple[int, str]:
    man = r.choice(AMOUNTS.get(purpose, GENERAL))
    won = man * 10000
    eok, rest = divmod(man, 10000)
    if eok:
        num = f"{eok}억" + (f" {rest}만" if rest else "")
        kor = f"{korean_number(eok) if eok > 1 else '일'}억" + (f"{korean_number(rest)}만" if rest else "")
    else:
        num, kor = f"{man:,}만", f"{korean_number(man)}만"
    forms = [num + "원", num, kor + "원", f"{won:,}원"]
    if man % 1000 == 0 and not eok:   # '3천' 처럼 만을 빼고 쓰는 표현 (대출 맥락에서 3천만원)
        forms.append(f"{man // 1000}천")
    return won, r.choice(forms)


def _period(r: random.Random) -> tuple[int, str]:
    months = r.choice([3, 6, 12, 12, 18, 24, 36, 60])
    forms = [f"{months}개월"]
    if months % 12 == 0:
        y = months // 12
        forms += [f"{y}년", f"{'일이삼사오'[y - 1]}년" if y <= 5 else f"{y}년"]
    if months == 6:
        forms.append("반년")
    if months == 18:
        forms.append("1년 반")
    return months, r.choice(forms)


def _last_day(y: int, m: int) -> date:
    return date(y, m, calendar.monthrange(y, m)[1])


def _next_month(d: date) -> tuple[int, int]:
    return (d.year + 1, 1) if d.month == 12 else (d.year, d.month + 1)


def _date(r: random.Random, today: date) -> tuple[date, str, bool, bool]:
    """(날짜, 표현, 대략인지, 상대 표현인지). 상대 날짜는 today(질문에 주는 기준일) 기준."""
    y, m = _next_month(today)
    kind = r.choice(["abs", "abs", "abs", "end", "mid", "early", "days", "week"])
    if kind == "end":
        return _last_day(y, m), r.choice(["다음달 말", "담달 말", "다음 달 말일"]), False, True
    if kind == "mid":
        return date(y, m, 15), r.choice(["다음달 중순", "담달 중순"]), True, True
    if kind == "early":
        return date(y, m, 1), r.choice(["다음달 초", "다음 달 초"]), True, True
    if kind == "days":
        n = r.choice([3, 5, 7, 10, 14, 30])
        return today + timedelta(days=n), "일주일 뒤" if n == 7 and r.random() < 0.5 else f"{n}일 뒤", False, True
    if kind == "week":
        return today + timedelta(days=7), r.choice(["다음주", "담주"]), True, True
    d = today + timedelta(days=r.randint(5, 120))
    text = r.choice([f"{d.month}월 {d.day}일", f"{d.month}/{d.day}", f"'{d.year % 100:02d}.{d.month}.{d.day}",
                     f"{d.year}.{d.month:02d}.{d.day:02d}", f"{d.month}.{d.day}"])
    return d, text, False, False


def _ro(word: str) -> str:
    """조사 '로/으로' (받침 없거나 ㄹ 받침이면 '로')."""
    c = ord(word[-1]) - 0xAC00
    return "으로" if 0 <= c < 11172 and c % 28 not in (0, 8) else "로"


@lru_cache(maxsize=1)
def templates() -> dict[str, list[dict]]:
    """칸 종류별 문장 틀 (docgen/freetext_templates.json)."""
    out: dict[str, list[dict]] = {}
    for t in json.loads(TEMPLATES_PATH.read_text(encoding="utf-8"))["templates"]:
        out.setdefault(t["slot"], []).append(t)
    return out


SLOTS_RE = re.compile(r"\{(purpose|reason|amount|period|date|request|memo)\}")


def make(r: random.Random, today: date, slot: str) -> tuple[str, dict, str]:
    """칸 종류에 맞는 틀 하나를 골라 채운다 → (글, 정답 레코드, 난이도)."""
    return make_from(r.choice(templates()[slot]), r, today)


def make_from(tpl: dict, r: random.Random, today: date) -> tuple[str, dict, str]:
    """틀 하나를 채운다. 난이도: short(값 나열) · sentence(문장) · relative(상대 날짜) · approx(대략적인 값)."""
    rec: dict = dict(tpl.get("set", {}))
    approx = set(tpl.get("approx", []))
    relative = False

    def fill(m: re.Match) -> str:
        nonlocal relative
        k = m.group(1)
        if k in VOCAB:
            canon = rec[k] if k == "purpose" and k in rec else r.choice(list(VOCAB[k]))
            rec[k] = canon
            return r.choice(VOCAB[k][canon])
        if k == "amount":
            won, text = _amount(r, rec.get("purpose"))
            rec["amount"] = won
            return text
        if k == "period":
            rec["period_months"], text = _period(r)
            return text
        if k == "date":
            d, text, rough, rel = _date(r, today)
            rec["date"] = d.isoformat()
            if rough:
                approx.add("date")
            relative |= rel
            return text
        rec["memo"] = r.choice(MEMOS)
        return rec["memo"]

    if "{purpose}" in tpl["t"]:   # 금액이 용도보다 앞에 와도 용도에 맞는 금액이 되게 용도를 먼저 정한다
        rec["purpose"] = r.choice(list(PURPOSES))
    text = SLOTS_RE.sub(fill, tpl["t"])
    text = re.sub(r"(.)\(으\)로", lambda m: m.group(1) + _ro(m.group(1)), text)
    if r.random() < 0.1:
        text = "※ " + text if not text.startswith("※") else text
    if approx:
        rec["approx"] = sorted(approx)
    bare = re.sub(r"[\s,./()\-:※]", "", SLOTS_RE.sub("", tpl["t"]))
    level = "approx" if approx else "relative" if relative else "short" if len(bare) <= 4 else "sentence"
    return text, rec, level


# ---------------------------------------------------------------------------
# 생성 중 모으기: render() 가 collect() 를 열고, 생성기가 make 한 글의 정답을 record() 로 넣는다
# ---------------------------------------------------------------------------
_local = threading.local()


@contextmanager
def collect():
    prev = getattr(_local, "sink", None)
    _local.sink = sink = {}
    try:
        yield sink
    finally:
        _local.sink = prev


def record(text: str, rec: dict, level: str, today: date) -> None:
    sink = getattr(_local, "sink", None)
    if sink is not None:
        sink[text] = {"answer": rec, "level": level, "basis": today.isoformat()}


def fill(label: str, seed_key: str, today: date, fits) -> str | None:
    """칸 하나에 자유 기재 글을 넣을지 정하고 넣으면 글을 돌려준다. fits(글) → 칸에 읽을 만한 크기로 들어가는지.

    seed_key 로 따로 뽑으므로 서류의 다른 칸 값은 바뀌지 않는다."""
    slot = slot_of(label)
    if slot is None:
        return None
    r = random.Random(f"freetext:{seed_key}")
    if r.random() >= RATE:
        return None
    for _ in range(6):   # 칸에 안 들어가면 다른 틀로 (짧은 틀이 많아 대개 몇 번 안에 들어감)
        text, rec, level = make(r, today, slot)
        if fits(text):
            record(text, rec, level, today)
            return text
    return None
