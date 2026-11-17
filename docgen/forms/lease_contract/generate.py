"""lease_contract: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/real_estate.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.real_estate import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _Hand,
    _agent,
    _amount,
    _area,
    _brokers,
    _facts,
    _iga,
    _open_specials,
    _party,
)
from docgen.registry import doc


_LEASE_EXTRA = ["반려동물 사육은 임대인의 동의를 받아야 한다.", "벽걸이TV, 못 자국 등 경미한 훼손은 원상복구 대상에서 제외한다.",
                "관리비는 실사용 기준으로 임차인이 부담한다.", "도배·장판은 잔금일 전까지 임대인이 교체하여 준다.",
                "임대인은 임차인의 전세보증금반환보증 가입에 협조한다.", "임대인은 잔금일까지 국세·지방세 완납증명서를 임차인에게 제시한다.",
                "계약기간 중 임대인이 주택을 매도하는 경우 임대인은 매수인에게 본 계약의 승계를 고지한다.",
                "보일러·수전 등 노후로 인한 고장은 임대인이 수리하고, 임차인 과실로 인한 고장은 임차인이 부담한다.",
                "임차인은 입주 전 시설 상태를 사진으로 촬영하여 임대인과 공유한다.",
                "계약 만료 2개월 전까지 쌍방 의사표시가 없으면 동일 조건으로 갱신된 것으로 본다.",
                "흡연은 세대 내 및 베란다에서 금지한다.", "현관 도어락 비밀번호는 입주일에 변경한다.",
                "임대인은 보증금 반환 시 관리비 정산금을 공제할 수 있다.", "에어컨 실외기 설치 위치는 관리사무소 규정을 따른다.",
                "임차인은 전입신고 및 확정일자를 잔금일 당일에 받기로 한다."]


@doc("lease_contract", "주택임대차표준계약서", "real_estate")
def lease_contract(p: Profile, rng: random.Random) -> dict:
    """주택임대차표준계약서 (전세). 임대인 = 기존 소유자(seller), 임차인 = 본인."""
    f = _facts(p)
    a, pr, lord, hist = f["a"], f["pr"], f["pr"].seller, f["hist"]
    r = random.Random(f"lease:{p.seed}")
    cdate = p.issue_date - timedelta(days=r.randint(3, 25))
    start = cdate + timedelta(days=r.randint(20, 60))
    end = date(start.year + 2, start.month, start.day if not (start.month == 2 and start.day == 29) else 28) - timedelta(days=1)
    dep = pr.lease_deposit
    down = K.round_to(dep * rng.choice([0.05, 0.1, 0.1]), 1_000_000)
    dfmt = rng.choice(["kor", "kor_short"])
    stamp_d = cdate + timedelta(days=rng.randint(0, 5))
    mort_d = start + timedelta(days=2)
    specials = [
        f"주택을 인도받은 임차인은 {D(start, 'kor_short')}까지 주민등록(전입신고)과 주택임대차계약서상 확정일자를 받기로 하고, "
        f"임대인은 {D(mort_d, 'kor_short')}(최소한 임차인의 위 약정일자 이틀 후부터 가능)에 저당권 등 담보권을 설정할 수 있다.",
        "임대인이 위 특약에 위반하여 임차주택에 저당권 등 담보권을 설정한 경우에는 임차인은 임대차계약을 해제 또는 해지할 수 있다.",
        f"임차인은 {p.bank} 전세자금대출을 신청할 예정이며, 임대인은 이에 협조한다. "
        "임차인의 귀책사유 없이 대출이 불가한 경우 본 계약은 무효로 하고 임대인은 계약금을 즉시 반환한다.",
    ]
    if rng.random() < 0.6:  # 2023 개정 표준계약서 권고 특약
        specials.insert(2, "임대차계약 체결 이후 임대인이 사전에 고지하지 않은 선순위 임대차 정보나 미납·체납한 국세·지방세가 "
                           "확인되는 경우, 임차인은 위약금 없이 임대차계약을 해제할 수 있다.")
    if not f["transferred"]:
        specials += [s.replace("잔금 지급일까지", "잔금일까지").replace(", 잔금으로 상환할 수 있다", "")
                     .replace("매수인은 계약을 해제하고", "임차인은 계약을 해제하고") for s in _open_specials(f, cdate, "임대인")]
    long_doc = heavy(rng, 0.2)
    specials += rng.sample(_LEASE_EXTRA, rng.randint(8, 13) if long_doc else int(rng.random() < 0.3))
    co_l = hist["co_seller"] if not f["transferred"] else None
    out = {
        "landlord_name": lord.name + (f", {co_l.name}" if co_l else ""), "tenant_name": p.person.name,
        "house": {
            "location": a.road_full,
            "land_category": "대",
            "land_area": f"{_area(f['land_total'])}㎡",
            "structure_usage": f"{pr.structure} / {f['usage_full']}",
            "building_area": f"{_area(pr.exclusive_area)}㎡",
            "lease_part": f"전부 ({_area(pr.exclusive_area)}㎡)",
        },
        "contract_type": rng.choice(["신규 계약", "신규 계약", "신규 계약", "합의에 의한 재계약"]),
        "management_fee": rng.choice(["세대별 사용량 및 관리규약에 따른 부과액(공용관리비 면적 비례)", "관리사무소 부과 고지서 기준 실비",
                                      "관리규약에 따라 관리주체가 부과하는 금액"]),
        "tax_arrears": "없음",
        "prior_fixed_date": "해당 없음",
        "deposit": _amount(dep),
        "down_payment": _amount(down),
        "balance": _amount(dep - down),
        "balance_date": D(start, dfmt),
        "handover_date": D(start, dfmt),
        "end_date": D(end, dfmt),
        "fixed_date": {"date": D(stamp_d, "dot"), "no": f"{stamp_d.year}-{rng.randint(100, 9999)}",
                       "office": community_center(a).removesuffix("장") + "행정복지센터"},
        "contract_date": D(cdate, dfmt),
        "landlord": _party(lord, f["seller_addr"]),
        "tenant": _party(p.person, p.person.address.road_full),
        "brokers": _brokers(rng, f),
    }
    if co_l:
        out["co_landlord"] = _party(co_l, f["seller_addr"])
        specials.append(f"본 주택은 임대인 {lord.name}, {co_l.name}의 공유이며, 보증금 반환 의무는 공유자 전원이 연대하여 부담한다.")
    if special(rng, "agent", 0.12):  # 임대인 대리 계약 (해외 거주·고령 등)
        ag = _agent(p, rng, lord)
        out["landlord_agent"] = {k: ag[k] for k in ("address", "rrn", "name")}
        specials.append(f"임대인의 {ag['relation']} {_iga(ag['name'])} 임대인의 위임장 및 인감증명서를 지참하여 대리 계약하며, "
                        "보증금은 임대인 명의 계좌로만 입금한다.")
    specials = [f"{i + 1}. {s}" for i, s in enumerate(specials)]
    if special(rng, "hand_special", 0.12):
        specials.append(_Hand(f"{len(specials) + 1}. " + rng.choice(["입주청소 후 입주.", "잔금일 오전 중 열쇠 인계.",
                                                                  "현관 센서등 교체해 줌.", "주차 1대 등록 가능."])))
    out["specials"] = specials
    return out
