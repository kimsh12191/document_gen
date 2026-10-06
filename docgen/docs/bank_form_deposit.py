"""은행 자체 서식 — 수신 제신고·증명·위임 (상속예금, 잔액증명, 통합제신고, 정보제공, 대여금고, 위임장).

서식 구성은 하나은행 공개 서식에서 뽑은 기재란 명세를 따랐다
(add_template/field_specs/예금/{001,011,015,024,025,028}.json).
"""
from ..registry import doc
from ._common import *  # noqa: F401,F403
from .bank_form_loan import _relative

# ---------------------------------------------------------------------------
# 공용 헬퍼
# ---------------------------------------------------------------------------

ACCOUNT_KINDS = ["저축예금", "자유입출금예금", "정기예금", "정기적금", "주택청약종합저축", "외화정기예금",
                 "특정금전신탁", "수시입출금식예금(MMDA)"]


def _staff(rng: random.Random) -> dict:
    return {"clerk": K.make_name(rng, rng.choice("MF"))[0],
            "manager": K.make_name(rng, rng.choice("MF"))[0]}


def _date(p: Profile, rng: random.Random) -> str:
    return D(p.issue_date, rng.choice(["kor", "kor", "kor_short", "dot"]))


def _birth(per: Person, rng: random.Random) -> str:
    """생년월일 칸 — 서식에 따라 주민번호를 쓰기도 한다."""
    return K.mask_rrn(per.rrn) if rng.random() < 0.25 else D(per.birth, "dot")


def _acct_no(p: Profile, rng: random.Random) -> str:
    from ..entities import BANK_ACCT_FMT
    fmt = BANK_ACCT_FMT.get(p.bank, "###-##-######")
    return "".join(str(rng.randint(0, 9)) if c == "#" else c for c in fmt)


def _accounts(p: Profile, rng: random.Random, n: int) -> list[dict]:
    return [{"number": _acct_no(p, rng), "kind": rng.choice(ACCOUNT_KINDS),
             "balance": K.won(K.round_to(rng.uniform(3e5, 2.4e8), 1000))} for _ in range(n)]


def _branch(p: Profile) -> str:
    return p.bank_branch


# ---------------------------------------------------------------------------
# 상속예금 명의변경(지급) 의뢰서 — 5-08-0084
# ---------------------------------------------------------------------------

RELATIONS = ["배우자", "자녀", "자녀", "자녀", "부", "모", "형제자매"]


@doc("inheritance_deposit_claim", "상속예금 지급·명의변경 의뢰서", "bank_form", category="internal")
def inheritance_deposit_claim(p: Profile, rng: random.Random) -> dict:
    """사망한 예금주의 예금을 상속인에게 지급·명의변경하는 의뢰서 (손해담보 확약·위임장 겸용)."""
    per = p.person
    # 피상속인은 고객의 부 또는 모 — 프로필의 가족을 그대로 쓴다
    dead = p.father if rng.random() < 0.6 else p.mother
    death = recent(rng, p, 240)
    n = rng.choices([1, 2, 3, 4], weights=[40, 32, 18, 10])[0]
    accounts = _accounts(p, rng, n + (rng.randint(2, 4) if heavy(rng, 0.3) else 0))
    total = sum(int(a["balance"].replace(",", "").rstrip("원")) for a in accounts)
    kind = rng.choices(["지급", "분할지급", "소액지급"], weights=[55, 25, 20])[0]

    heirs = [{"name": per.name, "birth": _birth(per, rng), "relation": "자녀",
              "share": "1/2" if p.spouse else "1/1", "delegate": "본인"}]
    for other in ([p.mother] if dead is p.father else [p.father]) + p.children[:1]:
        if other is None or rng.random() < 0.25:
            continue
        heirs.append({"name": other.name, "birth": _birth(other, rng),
                      "relation": rng.choice(RELATIONS), "share": "1/2",
                      "delegate": rng.choices(["위임(주된 상속인 앞)", "본인"], weights=[70, 30])[0]})

    data = {
        "bank": p.bank,
        "branch": _branch(p),
        "deceased": {
            "name": dead.name,
            "birth": D(dead.birth, "dot"),
            "rrn": K.mask_rrn(dead.rrn),
            "death_date": D(death, "dot"),
            "address": dead.address.road_short,
        },
        "payout": {
            "kind": kind,
            "amount": K.won(total) if kind != "분할지급" else K.won(K.round_to(total * 0.5, 1000)),
            "date": D(p.issue_date, "dot"),
        },
        "accounts": accounts,
        "total": K.won(total),
        "main_heir": {"name": per.name, "birth": _birth(per, rng), "relation": "자녀",
                      "address": per.address.road_short, "phone": per.mobile,
                      "delegate": "본인", "account": p.accounts[0].number},
        "heirs": heirs,
        "documents": rng.sample(["가족관계증명서", "기본증명서", "제적등본", "상속인 인감증명서",
                                 "사망진단서", "주민등록말소자 초본"], k=rng.randint(3, 5)),
        "unpaid_confirm": rng.choice(["없음", "없음", "있음"]),
        "date": _date(p, rng),
        "signature": per.name,
        "staff": _staff(rng),
    }
    return data


# ---------------------------------------------------------------------------
# 예금(신탁)잔액증명 의뢰서 — 5-08-0094
# ---------------------------------------------------------------------------

CERT_PURPOSES = ["법원 제출용", "관공서 제출용", "세무서 제출용", "회계감사용", "비자 신청용",
                 "거래처 제출용", "본인 확인용", "입찰 참가용"]


@doc("balance_certificate_request", "예금(신탁)잔액증명 의뢰서", "bank_form", category="internal")
def balance_certificate_request(p: Profile, rng: random.Random) -> dict:
    """특정 기준일의 예금·신탁 잔액증명서 발급을 의뢰하는 서식."""
    per = p.person
    corporate = rng.random() < 0.25
    target = rng.choices(["지정계좌", "전체계좌"], weights=[62, 38])[0]
    accounts = _accounts(p, rng, rng.randint(1, 3)) if target == "지정계좌" else []
    receive = rng.choices(["창구수령", "E-mail", "카카오톡(문자)"], weights=[55, 30, 15])[0]
    agent = None
    if receive == "창구수령" and rng.random() < 0.3:
        who, relation = _relative(p, rng)
        agent = {"name": who.name, "birth": D(who.birth, "dot"), "relation": relation}

    data = {
        "bank": p.bank,
        "branch": _branch(p),
        "kind": rng.choices(["등록", "변경", "해제"], weights=[80, 12, 8])[0],
        "customer": {
            "name": p.corporation.name if corporate else per.name,
            "birth": p.corporation.biz_no if corporate else _birth(per, rng),
            "address": (p.corporation.address if corporate else per.address).road_short,
            "phone": per.mobile,
        },
        "base_date": D(recent(rng, p, 10), "kor"),
        "target": target,
        "accounts": accounts,
        "copies": f"{rng.choices([1, 2, 3, 5], weights=[55, 25, 12, 8])[0]}",
        "currency": rng.choices(["KRW", "USD"], weights=[88, 12])[0],
        "masking": rng.choices(["계좌마스킹(계좌번호 일부숨김)", "마스킹 않음"], weights=[45, 55])[0],
        "purpose": rng.choice(CERT_PURPOSES),
        "fee_account": p.accounts[0].number,
        "receive": receive,
        "email": per.email,
        "date": _date(p, rng),
        "signature": p.corporation.name if corporate else per.name,
        "staff": _staff(rng),
    }
    if agent:
        data["agent"] = agent
    return data


# ---------------------------------------------------------------------------
# 통합제신고서 — 주소·연락처·인감·비밀번호 등 변경 신고
# ---------------------------------------------------------------------------

CHANGE_ITEMS = ["주소 변경", "연락처 변경", "인감(서명) 변경", "비밀번호 변경",
                "통장 재발급", "성명(상호) 변경", "통장 분실신고", "E-mail 변경"]
CARRIERS = ["SKT", "KT", "LGU+", "기타"]


@doc("integrated_change_report", "통합제신고서", "bank_form", category="internal")
def integrated_change_report(p: Profile, rng: random.Random) -> dict:
    """예금 거래 신고사항(주소·연락처·인감·비밀번호 등)을 한 장으로 바꾸는 제신고 서식."""
    per = p.person
    items = rng.sample(CHANGE_ITEMS, k=rng.choices([1, 2, 3], weights=[55, 32, 13])[0])
    old_addr = p.address_history[-2][1] if len(p.address_history) > 1 else per.address
    before, after = {}, {}
    if "주소 변경" in items:
        before["address"] = old_addr.road_short
        after["address"] = per.address.road_short
    if "연락처 변경" in items or "E-mail 변경" in items:
        before["phone"] = K.mobile(random.Random(f"old:{p.seed}"))
        after["phone"] = per.mobile
    if "인감(서명) 변경" in items:
        before["seal"] = "구 인감"
        after["seal"] = "신 인감"

    agent = None
    if rng.random() < 0.22:
        who, relation = _relative(p, rng)
        agent = {"name": who.name, "birth": D(who.birth, "dot"), "relation": relation}

    return {
        "bank": p.bank,
        "branch": _branch(p),
        "customer": {"name": per.name, "birth": _birth(per, rng),
                     "address": per.address.road_short, "phone": per.mobile},
        "account": _acct_no(p, rng),
        "items": items,
        "before": before or {"note": "해당 없음"},
        "after": after or {"note": "해당 없음"},
        "phone_kind": rng.choices(["스마트폰", "일반폰", "알뜰폰"], weights=[84, 6, 10])[0],
        "carrier": rng.choices(CARRIERS, weights=[38, 30, 26, 6])[0],
        "receive": rng.choice(["창구수령", "등기우편", "수령 생략"]),
        **({"agent": agent} if agent else {}),
        "date": _date(p, rng),
        "signature": per.name,
        "staff": _staff(rng),
    }


# ---------------------------------------------------------------------------
# 금융거래정보제공(요구·동의)서 — 5-08-0016
# ---------------------------------------------------------------------------

INFO_ITEMS = ["거래내역 조회", "잔액 조회", "계좌 개설 현황", "대출 거래내역", "외화 거래내역"]
INFO_RECEIVERS = ["법원", "세무서", "수사기관", "보험회사", "회계법인", "본인", "변호사"]


@doc("financial_info_disclosure", "금융거래정보제공(요구·동의)서", "bank_form", category="internal")
def financial_info_disclosure(p: Profile, rng: random.Random) -> dict:
    """금융실명법 제4조에 따라 본인의 금융거래정보 제공을 요구하거나 제3자 제공에 동의하는 서식."""
    per = p.person
    kind = rng.choices(["요구", "동의"], weights=[60, 40])[0]
    period = rng.choices(["최근 3개월", "최근 6개월", "최근 1년", "기간 지정"], weights=[30, 25, 25, 20])[0]
    start = months_back(p.issue_date, rng.choice([3, 6, 12, 24]))
    return {
        "bank": p.bank,
        "branch": _branch(p),
        "kind": kind,
        "customer": {"name": per.name, "birth": _birth(per, rng),
                     "address": per.address.road_short, "phone": per.mobile},
        "receiver": "본인" if kind == "요구" else rng.choice(INFO_RECEIVERS),
        "purpose": rng.choice(["소송 자료 제출", "세무 신고 자료", "보험금 청구", "본인 거래 확인",
                               "상속 재산 확인", "대출 심사 자료"]),
        "items": rng.sample(INFO_ITEMS, k=rng.randint(1, 3)),
        "account_scope": rng.choices(["전체", "지정"], weights=[45, 55])[0],
        "accounts": _accounts(p, rng, rng.randint(1, 2)),
        "period": period,
        "period_range": f"{D(start, 'dot')} ~ {D(p.issue_date, 'dot')}",
        "valid_until": D(p.issue_date + timedelta(days=rng.choice([30, 60, 90])), "kor"),
        "notify": rng.choices(["통보 요청", "통보 생략"], weights=[35, 65])[0],
        "fee": K.won(rng.choice([0, 1000, 2000, 3000])),
        "date": _date(p, rng),
        "signature": per.name,
        "staff": _staff(rng),
    }


# ---------------------------------------------------------------------------
# 대여금고(신규·변경·해지)신청서 — 3-08-1282
# ---------------------------------------------------------------------------

BOX_SIZES = [("소형", 36_000), ("중형", 60_000), ("대형", 120_000), ("특대형", 200_000)]


@doc("safe_deposit_box_application", "대여금고 신청서", "bank_form", category="internal")
def safe_deposit_box_application(p: Profile, rng: random.Random) -> dict:
    """영업점 대여금고의 신규 임차·변경·해지를 신청하는 서식."""
    per = p.person
    kind = rng.choices(["신규", "변경", "해지"], weights=[62, 18, 20])[0]
    size, fee = rng.choice(BOX_SIZES)
    term = rng.choices(["12개월", "만기일 지정"], weights=[72, 28])[0]
    joint = None
    if rng.random() < 0.3:
        who, relation = _relative(p, rng)
        joint = {"name": who.name, "birth": D(who.birth, "dot"), "relation": relation}
    return {
        "bank": p.bank,
        "branch": _branch(p),
        "kind": kind,
        "customer": {"name": per.name, "birth": _birth(per, rng),
                     "address": per.address.road_short, "phone": per.mobile},
        "box": {
            "no": f"{rng.randint(1, 9)}-{rng.randint(1, 240):03d}",
            "size": size,
            "fee": K.won(fee),
            "deposit": K.won(rng.choice([50_000, 100_000, 0])),
            "term": term,
            "expires": D(p.issue_date + timedelta(days=365), "dot"),
        },
        **({"joint_user": joint} if joint else {}),
        "fee_account": p.accounts[0].number,
        "key_count": str(rng.choice([1, 2, 2])),
        "date": _date(p, rng),
        "signature": per.name,
        "staff": _staff(rng),
    }


# ---------------------------------------------------------------------------
# 위임장 (은행 거래용) — 5-08-0041
# ---------------------------------------------------------------------------

POA_SCOPE = ["신규계좌 개설", "비밀번호 변경", "통장·인감 분실신고", "계좌해지", "제신고(주소·연락처)",
             "잔액증명서 발급", "통장 재발급"]
POA_PRODUCTS = ["입출금이 자유로운 예금", "정기예금", "적금", "기타"]


@doc("bank_power_of_attorney", "위임장(은행 거래용)", "bank_form", category="internal")
def bank_power_of_attorney(p: Profile, rng: random.Random) -> dict:
    """예금 거래를 대리인에게 위임하는 은행 서식 (자필기재·인감 날인 포함)."""
    per = p.person
    agent, relation = _relative(p, rng)
    scope = rng.sample(POA_SCOPE, k=rng.choices([1, 2], weights=[70, 30])[0])
    detail = rng.choice(["비밀번호 변경", "통장/인감 분실", "계좌해지", "기타"])
    return {
        "bank": p.bank,
        "branch": _branch(p),
        "grantor": {"name": per.name, "birth": _birth(per, rng),
                    "address": per.address.road_short, "phone": per.mobile},
        "agent": {"name": agent.name, "birth": D(agent.birth, "dot"), "relation": relation,
                  "address": agent.address.road_short, "phone": agent.mobile},
        "scope": scope,
        "product": rng.choice(POA_PRODUCTS),
        "detail": detail,
        "detail_etc": "해외 체류로 본인 방문 불가" if detail == "기타" else None,
        "account": _acct_no(p, rng),
        "handwritten": "위 내용을 위임합니다",
        "valid_until": D(p.issue_date + timedelta(days=rng.choice([30, 60, 90])), "kor"),
        "date": _date(p, rng),
        "signature": per.name,
        "agent_signature": agent.name,
        "staff": _staff(rng),
    }
