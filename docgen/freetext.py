"""기타 칸 정리(freetext) 과제: 비고·기타·사유·용도 칸에 사람이 대충 쓴 듯한 글과, 그 글을 DB 칸으로 정리한 정답.

정답(레코드)을 먼저 뽑고 글로 바꾼다 → 글과 정답이 늘 맞는다.
  레코드 키: purpose(용도 보기), reason(사유 보기), amount(원 정수), date(YYYY-MM-DD), period_months(개월),
            request(요청 보기), memo(다른 키에 맞지 않는 말, 글에 적힌 그대로), approx(대략적인 값의 키 목록)
  적히지 않은 키는 레코드에 없다 (null 을 쓰지 않는다).

생성기(realform.build_form)가 make() 로 글을 만들면, render() 가 열어 둔 collect() 에 {글: 정답} 이 쌓이고
data["_freetext"] 로 bench build 까지 간다 (docgen/bench/build.py 가 freetext 문항을 낸다).
"""
from __future__ import annotations

import calendar
import random
import re
import threading
from contextlib import contextmanager
from datetime import date, timedelta

KEYS = ("purpose", "reason", "amount", "date", "period_months", "request", "memo")

# 보기(DB 값) → 글에 쓰는 표현
PURPOSES = {
    "생활자금": ["생활비", "생활자금", "생활 안정자금", "생활비 용도"],
    "주택구입": ["집 사는데", "주택 구입", "아파트 매수", "주택매입"],
    "전세자금": ["전세 보증금", "전세금", "전세자금"],
    "사업자금": ["가게 운영비", "사업 운영자금", "사업자금", "매장 인테리어"],
    "학자금": ["대학 등록금", "학비", "학자금"],
    "자녀 교육비": ["애 학원비", "자녀 교육비", "아이 유학비"],
    "의료비": ["병원비", "수술비", "치료비"],
    "결혼자금": ["결혼 준비", "혼수", "결혼자금"],
    "차량구입": ["차 구입", "자동차 구입", "차량 구입"],
}
REASONS = {
    "만기 해지": ["만기돼서 해지", "만기 해지", "만기로 해지"],
    "해외 이주": ["이민 감", "해외 이주", "외국으로 이사"],
    "타행 이체": ["다른 은행으로 옮김", "타행으로 이전", "타행 이체"],
    "급여 수령": ["월급 통장 변경", "급여 받으려고", "급여 수령"],
    "본인 요청": ["본인 요청", "고객 요청", "본인이 원함"],
    "계좌 정리": ["안 쓰는 계좌 정리", "계좌 정리", "통장 정리"],
    "주소 변경": ["이사함", "주소 이전", "주소 변경"],
    "분실": ["통장 잃어버림", "카드 분실", "분실"],
}
REQUESTS = {
    "서류 추가 제출": ["서류 추가 제출 예정", "추가서류 낼게요", "서류 보완 예정", "소득서류 추가 제출"],
    "전화 연락": ["전화 주세요", "연락 바람", "전화 요망"],
    "우편 발송": ["우편으로 보내주세요", "우편 발송 요청"],
    "문자 안내": ["문자로 안내", "문자 주세요"],
    "방문 예정": ["다시 방문 예정", "지점 방문 예정", "재방문"],
}
MEMOS = ["배우자 동의함", "보증인 없음", "급여이체 예정", "기존 대출 상환 후 신청", "상담 후 결정",
         "신분증 사본 첨부", "자동이체 같이 신청", "가족 명의 계좌 있음"]
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


def _amount(r: random.Random) -> tuple[int, str, list[str]]:
    man = r.choice([300, 500, 800, 1000, 1500, 2000, 3000, 5000, 7000, 10000, 15000, 20000, 30000])
    won = man * 10000
    eok, rest = divmod(man, 10000)
    if eok:
        num = f"{eok}억" + (f" {rest}만" if rest else "")
        kor = f"{korean_number(eok) if eok > 1 else '일'}억" + (f"{korean_number(rest)}만" if rest else "")
    else:
        num, kor = f"{man:,}만", f"{korean_number(man)}만"
    forms = [(num + "원", False), (num, True), (kor + "원", False), (f"{won:,}원", False)]
    if man % 1000 == 0 and not eok:   # '3천' 처럼 만을 빼고 쓰는 표현 (대출 맥락에서 3천만원)
        forms.append((f"{man // 1000}천", True))
    text, short = r.choice(forms)
    return won, text, ["abbrev"] if short else []


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


def make(r: random.Random, today: date, slot: str, n_facts: int) -> tuple[str, dict, str]:
    """(글, 정답 레코드, 난이도). 난이도: simple · abbrev(줄임·구어) · relative(상대 날짜) · approx(대략)."""
    rec: dict = {}
    approx: list[str] = []
    tags: set[str] = set()
    parts: list[str] = []

    head = slot if slot != "note" else r.choice(["purpose", "reason", None])
    pool = {"purpose": ["amount", "period_months", "date_request", "memo"],
            "reason": ["date_request", "memo", "request"],
            None: ["amount", "date_request", "request", "memo", "period_months"]}[head]
    picks = r.sample(pool, min(len(pool), max(1, n_facts - (head is not None))))
    if head:
        canon = r.choice(list(VOCAB[head]))
        word = r.choice(VOCAB[head][canon])
        rec[head] = canon
        if word != canon:
            tags.add("abbrev")
        parts.append(word + (_ro(word) if head == "purpose" and r.random() < 0.3 else ""))
    if "amount" in picks:
        won, text, t = _amount(r)
        tags.update(t)
        if r.random() < 0.3:
            text = r.choice([f"{text} 정도", f"{text}쯤", f"약 {text}", f"{text} 내외"])
            approx.append("amount")
        rec["amount"] = won
        parts.append(text)
    if "period_months" in picks:
        months, text = _period(r)
        if r.random() < 0.2:
            text += r.choice([" 정도", "쯤"])
            approx.append("period_months")
        rec["period_months"] = months
        parts.append(text + r.choice(["", " 쓰고", " 사용", " 상환"]))
    if "date_request" in picks or "request" in picks:
        canon = r.choice(list(REQUESTS))
        word = r.choice(REQUESTS[canon])
        rec["request"] = canon
        if "date_request" in picks:
            d, dtext, rough, rel = _date(r, today)
            rec["date"] = d.isoformat()
            if rough:
                approx.append("date")
            if rel:
                tags.add("relative")
            parts.append(f"{dtext}까지 {word}")
        else:
            parts.append(word)
    if "memo" in picks:
        memo = r.choice(MEMOS)
        rec["memo"] = memo
        parts.append(memo)

    first = parts[:1] if head else []
    rest = parts[len(first):]
    r.shuffle(rest)
    sep = r.choice([", ", " ", " / ", ". ", ","])
    text = sep.join(first + rest)
    if r.random() < 0.15:
        text = "※ " + text
    if approx:
        rec["approx"] = sorted(approx)
    level = "approx" if approx else "relative" if "relative" in tags else "abbrev" if tags else "simple"
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
    for n in (r.choice([2, 3, 3, 4]), 2):
        text, rec, level = make(r, today, slot, n)
        if fits(text):
            record(text, rec, level, today)
            return text
    return None
