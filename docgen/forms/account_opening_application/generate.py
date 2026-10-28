"""account_opening_application: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/bank_form_account.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.bank_form_account import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _bank,
    _date,
    _id_type,
    _occupation,
    _rrn,
    _staff,
)
from docgen.docs.bank_form_loan import _age, _foreigner, _minor, _relative, _solo  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.banks import since
from docgen.entities import BANK_ACCT_FMT
from docgen.registry import doc


def _new_account_no(bank: str, rng: random.Random) -> str:
    fmt = BANK_ACCT_FMT.get(bank, "###-##-######")
    return "".join(str(rng.randint(0, 9)) if c == "#" else c for c in fmt)


_PRODUCTS = {
    "보통예금": ["주거래 우대통장", "급여 우대통장", "생활비 통장", "스마트 입출금통장"],
    "저축예금": ["저축예금", "자유저축예금"],
    "정기예금": ["정기예금(일반)", "e-정기예금", "실속 정기예금"],
    "정기적금": ["자유적립식 적금", "정액적립식 적금", "목돈마련 적금"],
    "주택청약종합저축": ["주택청약종합저축"],
}


@doc("account_opening_application", "예금거래신청서", "bank_form", category="internal")
def account_opening_application(p: Profile, rng: random.Random) -> dict:
    """계좌개설(신규) 신청서 — 상품, 통장, 전자금융, 알림 서비스."""
    per = p.person
    job = _occupation(p, rng)
    ptype = rng.choices(list(_PRODUCTS), weights=[50, 8, 17, 18, 7])[0]
    product = {"type": ptype, "name": rng.choice(_PRODUCTS[ptype])}
    if ptype in ("보통예금", "저축예금"):
        product["amount"] = won(rng.choice([0, 10_000, 10_000, 50_000, 100_000, rng.randint(1, 300) * 10_000]))
    elif ptype == "정기예금":
        product["amount"] = won(rng.randint(5, 200) * 1_000_000)
        product["term"] = rng.choice(["6개월", "12개월", "12개월", "24개월", "36개월"])
        product["interest_payment"] = rng.choices(["만기일시지급", "월이자지급"], weights=[75, 25])[0]
        product["linked_account"] = p.accounts[0].number
    else:
        product["amount"] = won(rng.choice([2, 3, 5, 10, 20, 30, 50, 100]) * 10_000 if ptype == "주택청약종합저축"
                                else rng.randint(1, 30) * 50_000)
        product["term"] = "자유" if ptype == "주택청약종합저축" else rng.choice(["12개월", "24개월", "36개월"])
        product["linked_account"] = p.accounts[0].number
    demand = ptype in ("보통예금", "저축예금")
    internet = rng.choice(["신청", "신청", "미신청"])
    mobile = rng.choice(["신청", "신청", "신청", "미신청"])
    ebank = {"internet": internet, "mobile": mobile}
    if "신청" in (internet, mobile):
        ebank["otp"] = rng.choice(["OTP 발급", "기존 OTP 사용", "보안카드"]
                                  + (["모바일OTP"] if since(p.issue_date, "mobile_otp") else []))
        once = rng.choice([100, 500, 1000, 1000, 5000])
        ebank["limit_once"] = won(once * 10_000)
        ebank["limit_day"] = won(min(once * rng.choice([1, 2, 5]), 5000) * 10_000)
    else:
        ebank["otp"] = "미신청"
    customer = {
        "name": per.name, "name_en": per.name_en, "rrn": _rrn(p, rng, 0.3),
        "address": per.address.road_full, "zipcode": per.address.zipcode,
        "mobile": per.mobile, "email": per.email, "job": job["type"],
    }
    if "company" in job:
        customer["company"] = job["company"]
    data = {
        "bank": _bank(p),
        "customer": customer,
        "product": product,
        "passbook": rng.choice(["발행", "발행", "미발행"]),
        "seal_type": rng.choice(["서명", "서명", "인감", "인감+서명"]),
        "check_card": rng.choice(["신청", "미신청"]) if demand else "미신청",
        "ebank": ebank,
        "alert": rng.choice(["SMS", "앱 푸시", "앱 푸시", "미신청"]),
        "mail_to": rng.choice(["자택", "이메일", "이메일", "수령 안함"] + (["직장"] if "company" in job else [])),
        "salary_transfer": rng.choice(["지정", "미지정"]) if demand and job["type"] in ("급여소득자", "전문직") else "미지정",
        # 예금자보호한도: 2025.9.1.부터 1억원 (이전 5천만원). 주택청약종합저축은 비보호(주택도시기금).
        **({} if ptype == "주택청약종합저축" else
           {"protection_limit": "1억원" if p.issue_date >= date(2025, 9, 1) else "5천만원"}),
        "date": _date(p, rng),
        "signature": per.name,
        "bank_use": {
            "account_no": _new_account_no(p.bank, rng),
            "branch": p.bank_branch,
            "id_type": _id_type(p, rng),
            **_staff(rng),
        },
    }
    _aoa_variants(p, rng, data)
    return data


def _aoa_variants(p: Profile, rng: random.Random, data: dict) -> None:
    """예금거래신청서 변형: 여러 상품 동시 신규(여러 쪽), 미성년자(법정대리인), 대리인, 외국인, 공란."""
    cu = data["customer"]
    if heavy(rng, 0.15):  # 한 번에 여러 계좌 신규 (적금·청약·외화예금 등)
        extra = []
        for _ in range(rng.randint(4, 8)):
            t = rng.choice(["정기적금", "정기예금", "주택청약종합저축", "외화보통예금", "저축예금", "자유적립식 적금"])
            amt = (f"USD {rng.choice([100, 300, 500, 1000]):,}" if t.startswith("외화")
                   else won(rng.choice([10, 20, 30, 50, 100, 300, 500, 1000]) * 10_000))
            extra.append({"type": t, "name": rng.choice(_PRODUCTS.get(t, [t])), "amount": amt,
                          "term": "자유" if t in ("주택청약종합저축", "외화보통예금", "저축예금") else rng.choice(["6개월", "12개월", "24개월", "36개월"]),
                          "account_no": _new_account_no(p.bank, rng)})
        data["extra_products"] = extra
    if special(rng, "minor", 0.1):  # 미성년 자녀 명의 계좌를 부모가 법정대리인으로 개설
        kid = _minor(p, rng)
        cu.update({"name": kid.name, "name_en": kid.name_en, "rrn": K.mask_rrn(kid.rrn) if rng.random() < 0.7 else kid.rrn,
                   "mobile": kid.mobile if _age(p, kid) >= 12 else None, "email": None, "job": "학생" if _age(p, kid) >= 7 else "기타"})
        cu.pop("company", None)
        data["signature"] = kid.name
        data["salary_transfer"] = "미지정"
        if data["mail_to"] in ("이메일", "직장"):
            data["mail_to"] = "자택"
        data["legal_rep"] = {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn),
                             "relation": "부" if p.person.gender == "M" else "모", "phone": p.person.mobile,
                             "documents": rng.choice(["가족관계증명서(상세), 법정대리인 신분증", "기본증명서(상세), 가족관계증명서, 법정대리인 신분증"])}
    elif special(rng, "agent", 0.1):  # 대리인 신규 (위임장·본인 인감증명서 제출)
        ag, rel = _relative(p, rng)
        data["agent"] = {"name": ag.name, "rrn": K.mask_rrn(ag.rrn), "relation": rel, "phone": ag.mobile}
    elif _solo(p) and special(rng, "foreigner", 0.08):  # 외국인 고객
        fo = _foreigner(p, rng)
        cu.update({"name": fo["name"], "name_en": fo["name_en"], "rrn": fo["arc_no"], "mobile": fo["mobile"],
                   "email": fo["email"], "nationality": fo["nationality"]})
        data["signature"] = fo["name"]
        data["bank_use"]["id_type"] = "외국인등록증"
    if special(rng, "sparse", 0.12):  # 선택 항목 미기재
        for k in rng.sample(["email", "name_en", "zipcode"], rng.randint(1, 3)):
            cu[k] = None
