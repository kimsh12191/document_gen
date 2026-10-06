"""선언형 폼 스펙 — 서식 하나를 '수정 영역(기재란) 목록'으로만 등록한다.

수제 템플릿(templates/<그룹>/<id>.html.j2)을 깎는 대신, 서식을 이렇게 적는다.

    FORM("fx_capital_report", "자본거래 사후보고 확인서", "fx", code="외환-1234",
         sections=[("신고인", [("customer.name", "성명", "text"),
                             ("customer.rrn", "주민등록번호", "text")]),
                   ("거래내역", [("amount", "신고금액", "amount")])])

렌더링은 templates/_generic_form.html.j2 하나가 맡고, 값은 아래 VALUE 표가 만든다.
VALUE 에 있는 키는 Profile 에서 끌어오므로 (성명 → p.person.name) 같은 프로필로 만든
다른 서류와 사람·회사·계좌가 일치한다. 표에 없는 키는 kind 로 그럴듯한 값을 만든다.

스펙 파일 docgen/docs/forms_*.py 는 scripts/build_form_specs.py 가
add_template/field_specs/ (PDF 에서 뽑은 기재란) 로부터 생성한다.
"""
from __future__ import annotations

import random
from datetime import timedelta
from typing import Callable

from . import korean as K
from .entities import BANK_ACCT_FMT, Profile
from .registry import GROUPS, REGISTRY, DocSpec

D = K.fmt_date

# ---------------------------------------------------------------------------
# 1) 프로필에서 끌어오는 값 — 키 → (Profile, Random) -> 표시 문자열
# ---------------------------------------------------------------------------


def _acct(p: Profile, r: random.Random) -> str:
    fmt = BANK_ACCT_FMT.get(p.bank, "###-##-######")
    return "".join(str(r.randint(0, 9)) if c == "#" else c for c in fmt)


VALUE: dict[str, Callable[[Profile, random.Random], str]] = {
    # 개인
    "customer.name": lambda p, r: p.person.name,
    "customer.name_en": lambda p, r: p.person.name_en,
    "customer.rrn": lambda p, r: K.mask_rrn(p.person.rrn) if r.random() < 0.35 else p.person.rrn,
    "customer.birth": lambda p, r: D(p.person.birth, "dot"),
    "customer.address": lambda p, r: p.person.address.road_short,
    "customer.address_full": lambda p, r: p.person.address.road_full,
    "customer.phone": lambda p, r: p.person.mobile,
    "customer.email": lambda p, r: p.person.email,
    "customer.nationality": lambda p, r: p.person.nationality,
    "customer.gender": lambda p, r: p.person.gender_ko,
    "customer.job": lambda p, r: p.employment.job,
    "customer.zipcode": lambda p, r: p.person.address.zipcode,
    # 법인·사업자
    "company.name": lambda p, r: p.corporation.name,
    "company.name_en": lambda p, r: p.corporation.name_en,
    "company.biz_no": lambda p, r: p.corporation.biz_no,
    "company.corp_no": lambda p, r: p.corporation.corp_no or K.corp_reg_no(r),
    "company.ceo": lambda p, r: p.corporation.ceo.name,
    "company.address": lambda p, r: p.corporation.address.road_short,
    "company.phone": lambda p, r: p.corporation.phone,
    "company.fax": lambda p, r: p.corporation.fax,
    "company.email": lambda p, r: p.corporation.email,
    "company.biz_type": lambda p, r: p.corporation.biz_type,
    "company.biz_item": lambda p, r: p.corporation.biz_item,
    "company.established": lambda p, r: D(p.corporation.established, "dot"),
    "company.employees": lambda p, r: f"{p.corporation.employees}명",
    "company.capital": lambda p, r: K.won(p.corporation.capital),
    "company.revenue": lambda p, r: K.won(p.corporation.revenue),
    "company.department": lambda p, r: p.employment.department,
    # 직장
    "employer.name": lambda p, r: p.employment.company.name,
    "employer.biz_no": lambda p, r: p.employment.company.biz_no,
    "employer.phone": lambda p, r: p.employment.company.phone,
    "employer.hire_date": lambda p, r: D(p.employment.hire_date, "dot"),
    "employer.position": lambda p, r: p.employment.position,
    "employer.salary": lambda p, r: K.won(p.employment.annual_salary),
    # 은행·계좌
    "bank": lambda p, r: p.bank,
    "branch": lambda p, r: p.bank_branch,
    "account": _acct,
    "account.holder": lambda p, r: p.person.name,
    "account.balance": lambda p, r: K.won(K.round_to(r.uniform(1e5, 9e7), 1000)),
    # 상대방·대리인
    "agent.name": lambda p, r: (p.spouse or p.father).name,
    "agent.birth": lambda p, r: D((p.spouse or p.father).birth, "dot"),
    "agent.phone": lambda p, r: (p.spouse or p.father).mobile,
    "agent.relation": lambda p, r: "배우자" if p.spouse else "부",
    # 외환
    "foreign.name": lambda p, r: p.foreign.name,
    "foreign.address": lambda p, r: p.foreign.address,
    "foreign.country": lambda p, r: p.foreign.country,
    "foreign.bank": lambda p, r: p.foreign.bank,
    "foreign.swift": lambda p, r: p.foreign.swift,
    "foreign.account": lambda p, r: p.foreign.account,
    "foreign.contact": lambda p, r: p.foreign.contact,
    # 부동산
    "property.address": lambda p, r: p.property.address.road_short,
    "property.kind": lambda p, r: p.property.kind,
    "property.area": lambda p, r: f"{p.property.exclusive_area}㎡",
    "property.price": lambda p, r: K.won(p.property.price),
    # 일자
    "date": lambda p, r: D(p.issue_date, r.choice(["kor", "kor", "dot"])),
    "signature": lambda p, r: p.person.name,
    "signature.corp": lambda p, r: p.corporation.name,
}

# ---------------------------------------------------------------------------
# 2) 표에 없는 키 — kind 로 그럴듯한 값을 만든다
# ---------------------------------------------------------------------------

CURRENCIES = ["USD", "USD", "USD", "EUR", "JPY", "CNY", "GBP", "SGD"]
GENERIC_TEXT = ["해당 없음", "별첨과 같음", "기재 생략", "상기와 같음"]


def _fallback(kind: str, label: str, p: Profile, r: random.Random) -> str | None:
    if kind == "date":
        return D(p.issue_date - timedelta(days=r.randint(0, 60)), r.choice(["dot", "kor"]))
    if kind == "amount":
        # 서식마다 금액 규모가 달라 한쪽으로 치우치지 않게 자릿수부터 고른다
        hi = r.choice([1e6, 1e7, 1e7, 1e8, 5e8])
        return K.won(K.round_to(r.uniform(hi / 20, hi), 10_000))
    if kind == "fx_amount":
        return f"{r.choice(CURRENCIES)} {K.round_to(r.uniform(1e4, 2e6), 100):,}"
    if kind == "percent":
        return f"{r.uniform(0.1, 9.9):.2f}%"
    if kind == "number":
        return "-".join("".join(str(r.randint(0, 9)) for _ in range(n))
                        for n in r.choice([[4, 4, 4], [3, 6, 5], [6, 7]]))
    if kind == "count":
        return f"{r.randint(1, 50)}"
    if kind == "currency":
        return r.choice(CURRENCIES)
    if kind == "rate":
        return f"{r.uniform(1150, 1480):,.2f}"
    if kind == "blank":          # 서식에는 있으나 비워 두는 칸
        return None
    return r.choice(GENERIC_TEXT)


# ---------------------------------------------------------------------------
# 3) 등록
# ---------------------------------------------------------------------------

TEMPLATE = "_generic_form.html.j2"


def _put(data: dict, path: str, value) -> None:
    """'company.name' 같은 경로에 값을 넣는다 — 템플릿의 f('company.name') 이 찾는 자리."""
    cur = data
    parts = path.split(".")
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = cur[part] = {}
        cur = nxt
    cur[parts[-1]] = value


def _build(spec_fields: list[tuple], code: str, title_note: str):
    """FORM 이 등록할 생성 함수를 만든다."""

    def generate(p: Profile, rng: random.Random) -> dict:
        data: dict = {"bank": p.bank, "branch": p.bank_branch, "form_code": code,
                      "date": VALUE["date"](p, rng), "signature": p.person.name,
                      "sections": []}
        for title, fields in spec_fields:
            items = []
            for key, label, kind, options in fields:
                if options:
                    value = rng.choice(options)
                elif key in VALUE:
                    value = VALUE[key](p, rng)
                else:
                    value = _fallback(kind, label, p, rng)
                _put(data, key, value)
                items.append({"key": key, "label": label, "kind": kind,
                              "options": options, "value": value})
            data["sections"].append({"title": title, "items": items})
        data["title_note"] = title_note
        return data

    return generate


def FORM(id: str, name: str, group: str, sections: list, *, code: str = "",
         category: str = "internal", page: str = "a4", description: str = "",
         title_note: str = "") -> None:
    """서식 하나를 선언형으로 등록한다. sections: [(제목, [(키, 라벨, 종류, 보기|None), ...]), ...]"""
    assert group in GROUPS, group
    if id in REGISTRY:
        raise ValueError(f"duplicate doc id: {id}")
    # 같은 키가 여러 번 나오면 뒤에 번호를 붙여 GT 경로를 유일하게 만든다
    seen: dict[str, int] = {}
    fixed = []
    for title, fields in sections:
        out = []
        for item in fields:
            key, label, kind = item[0], item[1], item[2]
            options = item[3] if len(item) > 3 else None
            seen[key] = seen.get(key, 0) + 1
            if seen[key] > 1:
                key = f"{key}{seen[key]}"
            out.append((key, label, kind, options))
        fixed.append((title, out))
    REGISTRY[id] = DocSpec(id, name, group, category, TEMPLATE,
                           _build(fixed, code, title_note), page, False,
                           description or f"{name} — 하나은행 공개 서식 기준 선언형 스펙")
