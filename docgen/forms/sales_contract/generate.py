"""sales_contract: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

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


def _eun(name: str) -> str:
    c = name[-1]
    return name + ("은" if "가" <= c <= "힣" and (ord(c) - 0xAC00) % 28 else "는")


_EXTRA_SPECIALS = [
    "잔금일 기준으로 관리비 및 제세공과금은 매도인이 정산한다.",
    "매도인은 잔금일까지 임차인 없이 명도하기로 한다.",
    "본 계약 이후 매도인은 추가 담보 설정이나 임대를 하지 않는다.",
    "옵션(빌트인 가전 등)은 현 상태로 포함하여 매도한다.",
    "누수 등 중대한 하자는 잔금일 이후 6개월 이내 매도인이 책임진다.",
    "장기수선충당금은 매수인이 매도인에게 잔금일에 별도로 지급한다.",
    "매수인의 대출이 금융기관 사정으로 부결될 경우 계약금은 반환하고 계약은 해제한다.",
    "확장공사 부분 및 붙박이장, 시스템에어컨(거실·안방) 등은 매매대금에 포함한다.",
    "매도인은 잔금일 전 매수인의 인테리어 공사를 위한 출입에 협조한다.",
    "현관 도어락 비밀번호 및 공동현관 카드키 2개는 잔금일에 인계한다.",
    "전입세대 열람 결과 매도인 세대 외 전입자가 있을 경우 매도인이 잔금일까지 전출시킨다.",
    "주차장 지정 1대는 현 상태대로 승계한다.",
    "매도인은 국세·지방세 완납증명서를 잔금일에 제시한다.",
    "본 계약서에 명시되지 않은 사항은 민법 및 부동산 거래 관례에 따른다.",
    "계약금 중 일부(금 일천만원정)는 가계약금으로 이미 수령하였음을 확인한다.",
    "매수인은 잔금일 전 현장을 다시 확인할 수 있으며, 이때 발견된 하자는 쌍방 협의하여 처리한다.",
    "베란다 결로·곰팡이 부분은 현 상태로 인정하고 매수한다.",
    "매도인의 이사 일정상 잔금일은 쌍방 합의로 1주일 범위에서 조정할 수 있다.",
]


_HAND_SPECIALS = ["잔금일에 관리비 선수관리비 정산함.", "거실 에어컨 1대 두고 감.", "잔금일 오전 중 이사 완료 조건.",
                  "중도금 없이 잔금 일시 지급.", "도배는 매수인이 진행함.", "보일러 점검 후 이상 시 매도인 수리."]


@doc("sales_contract", "부동산 매매계약서", "real_estate")
def sales_contract(p: Profile, rng: random.Random) -> dict:
    """부동산(아파트) 매매계약서 (공인중개사 중개)."""
    f = _facts(p)
    a, pr, seller, hist = f["a"], f["pr"], f["pr"].seller, f["hist"]
    dfmt = rng.choice(["kor", "kor_short"])
    pay = {"price": _amount(f["price"]), "down": _amount(f["down"])}
    if f["middle"]:
        pay["middle"] = _amount(f["middle_amt"])
        pay["middle_date"] = D(f["middle"], dfmt)
    pay["balance"] = _amount(f["balance_amt"])
    pay["balance_date"] = D(f["balance"], dfmt)
    specials = ["현 시설물 상태의 계약이며, 매수인은 등기사항증명서 및 현장을 확인하고 계약함."]
    specials += _open_specials(f, f["contract"], "매도인")
    specials.append(f"매수인은 {p.bank} 주택담보대출로 잔금 일부를 지급할 예정이며, 매도인은 이에 협조한다.")
    long_doc = heavy(rng, 0.25)  # 특약이 많아 여러 쪽이 되는 계약서
    specials += rng.sample(_EXTRA_SPECIALS, rng.randint(9, 16) if long_doc else rng.randint(1, 2))
    co_s, co_b = hist["co_seller"], hist["co_buyer"]
    if co_s:
        specials.append(f"본 부동산은 매도인 {seller.name}, {co_s.name}의 공유(각 2분의 1)이며, 공유자 전원이 계약한다.")
    if co_b:
        specials.append(f"매수인 {p.person.name}, {_eun(co_b.name)} 각 2분의 1 지분으로 공동 매수한다.")
    out = {
        "property": {
            "location": a.road_full,
            "land_category": "대",
            "land_right": f"소유권대지권 {_area(f['land_total'])}분의 {_area(pr.land_area)}",
            "land_area": f"{_area(pr.land_area)}㎡",
            "structure": pr.structure,
            "usage": f["usage_full"],
            "building_area": f"{_area(pr.exclusive_area)}㎡",
        },
        "payment": pay,
        "contract_date": D(f["contract"], dfmt),
        "seller": _party(seller, f["seller_addr"]),
        "buyer": _party(p.person, p.person.address.road_full),
        "brokers": _brokers(rng, f),
    }
    if co_s:
        out["co_seller"] = _party(co_s, f["seller_addr"])
    if co_b:
        out["co_buyer"] = _party(co_b, p.person.address.road_full)
    if special(rng, "agent", 0.1):  # 매도인 대리 계약
        ag = _agent(p, rng, seller)
        out["seller_agent"] = {k: ag[k] for k in ("address", "rrn", "name")}
        specials.append(f"매도인의 {ag['relation']} {_iga(ag['name'])} 매도인의 위임장 및 인감증명서를 지참하여 대리 계약하며, "
                        "잔금일에 매도인 본인이 참석하여 확인한다.")
    specials = [f"{i + 1}. {s}" for i, s in enumerate(specials)]
    if special(rng, "hand_special", 0.12):  # 계약 현장에서 손으로 덧붙인 특약
        specials.append(_Hand(f"{len(specials) + 1}. {rng.choice(_HAND_SPECIALS)}"))
    out["specials"] = specials
    return out
