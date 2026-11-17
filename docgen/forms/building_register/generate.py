"""building_register: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/real_estate.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.real_estate import _addr_at, _facts  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


def _share_frac(share: str | None) -> str:
    return {"2분의 1": "1/2", None: "1/1", "단독소유": "1/1"}.get(share, share)


@doc("building_register", "집합건축물대장(전유부)", "real_estate", page="a4_landscape")
def building_register(p: Profile, rng: random.Random) -> dict:
    """집합건축물대장(전유부, 갑) 등본.

    소유자 변동 이력이 많거나 공용부분이 많은 경우(heavy)는 표를 세로로 쌓아 여러 쪽이 된다."""
    f = _facts(p)
    a, pr, hist = f["a"], f["pr"], f["hist"]
    long_doc = heavy(rng, 0.25)
    common = [
        {"kind": "주", "floor": "각층", "structure": pr.structure, "usage": "계단실,복도,승강기",
         "area": f"{pr.exclusive_area * rng.uniform(0.18, 0.28):.2f}"},
    ]
    if f["is_apt"] or rng.random() < 0.5:
        common.append({"kind": "주", "floor": "지1층", "structure": pr.structure, "usage": "주차장",
                       "area": f"{pr.exclusive_area * rng.uniform(0.25, 0.45):.2f}"})
    if f["is_apt"]:
        common.append({"kind": "주", "floor": "지1층", "structure": pr.structure, "usage": "기계실,전기실",
                       "area": f"{pr.exclusive_area * rng.uniform(0.02, 0.06):.2f}"})
        if rng.random() < 0.5:
            common.append({"kind": "부", "floor": "1층", "structure": pr.structure, "usage": "관리사무소,주민공동시설",
                           "area": f"{pr.exclusive_area * rng.uniform(0.03, 0.08):.2f}"})
    if long_doc:  # 공용부분을 층·용도별로 잘게 나눠 적은 대장
        extra = ["경비실", "주민운동시설", "작은도서관", "어린이집", "경로당", "펌프실", "발전기실", "전기실", "쓰레기보관소",
                 "자전거보관소", "옥탑", "물탱크실", "피트층", "방재실", "커뮤니티시설", "옥상"]
        for u in rng.sample(extra, rng.randint(6, 12)):
            fl = "옥탑1층" if u in ("옥탑", "옥상", "물탱크실") else rng.choice(["지1층", "지2층", "1층", "1층"])
            common.append({"kind": rng.choice(["주", "부"]), "floor": fl, "structure": pr.structure, "usage": u,
                           "area": f"{pr.exclusive_area * rng.uniform(0.005, 0.06):.2f}"})
    # 공동주택가격: 매년 1월 1일 기준, 4월 말 공시
    y = p.issue_date.year if p.issue_date >= date(p.issue_date.year, 4, 30) else p.issue_date.year - 1
    prices, v = [], pr.official_price
    for yy in range(y, y - (rng.randint(6, 9) if long_doc else rng.randint(3, 4)), -1):
        prices.append({"base_date": f"{yy}.01.01", "price": won(v, "")})
        v = K.round_to(v / rng.uniform(1.0, 1.12), 1_000_000)
    ho_name = (f"{f['dong_no']}동 " if f["dong_no"] else "") + f"{f['ho']}호"

    def row(pi: dict, share, d: date, cause: str, addr_d: date | None = None) -> dict:
        return {"name": pi["name"], "rrn": pi["rrn"] if pi["corp"] else K.mask_rrn(pi["rrn"]),
                "address": _addr_at(pi, addr_d or d), "share": _share_frac(share), "change_date": D(d, "dot"),
                "change_cause": cause}
    full = long_doc or special(rng, "owner_history", 0.3) or len(hist["state"]) > 1
    owners = []
    if full:  # 소유자 변동 이력 전체
        cmap = {"소유권보존": "소유권보존", "소유권이전": "소유권이전", "소유권일부이전": "소유권일부이전", "주소변경": "등기명의인표시변경"}
        for c in hist["chain"]:
            for pi, share in c["owners"]:
                owners.append(row(pi, share, c["date"], cmap[c["cause"]], c["date"] + timedelta(days=1) if c["cause"] == "주소변경" else None))
        # 공유자 지분: 일부이전 뒤에는 기존 소유자 지분도 1/2 로 적힌다
        for s in hist["state"]:
            for o in owners:
                if o["name"] == s["pi"]["name"]:
                    o["share"] = _share_frac(s["share"])
    else:
        last = hist["chain"][-1]
        for s in hist["state"]:
            pi = s["pi"]
            d = max(c["date"] for c in hist["chain"] if any(x[0]["name"] == pi["name"] for x in c["owners"]))
            owners.append(row(pi, s["share"], d, "소유권이전" if last["cause"] != "소유권보존" else "소유권보존"))
    out = {
        "confirm_no": issue_no(rng, 16),
        "unique_no": f"{f['dong_code']}-3-{f['bonbun']:04d}{f['bubun']:04d}",
        "building_name": f["bname"] + (f" 제{f['dong_no']}동" if f["dong_no"] else ""),
        "unit_name": ho_name,
        "site_location": f"{a.region} {a.dong}",
        "jibun": a.jibun,
        "road_address": f"{a.region} {a.road} {a.building_no}",
        "exclusive": [{"kind": "주", "floor": f"{f['floor']}층", "structure": pr.structure, "usage": f["usage"],
                       "area": f"{pr.exclusive_area:.2f}"}],
        "common": common,
        "owners": owners,
        "issue_date": D(p.issue_date, rng.choice(["kor", "kor_short"])),
        "officer": f"{rng.choice(['건축과', '건축행정과', '민원여권과', '종합민원과'])}",
        "officer_phone": K.landline(rng, a.sido),
        "issuer": district_office(a),
    }
    if not full:
        out["owners_note"] = "※ 이 건축물대장은 현소유자만 표시한 것입니다."
    if special(rng, "violation", 0.08):  # 위반건축물 표시 (발코니 불법확장·무단증축 등)
        out["violation"] = "위반건축물"
    if pr.kind != "오피스텔":  # 오피스텔은 공동주택가격 공시 대상이 아님
        out["house_prices"] = prices
    return out
