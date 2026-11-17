"""land_register: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/real_estate.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.real_estate import _addr_at, _area, _facts  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("land_register", "토지대장", "real_estate")
def land_register(p: Profile, rng: random.Random) -> dict:
    """토지대장 등본 (집합건물 대지). 소유자 변동 이력이 길면 여러 쪽."""
    f = _facts(p)
    a, pr, hist = f["a"], f["pr"], f["hist"]
    land_rows = []
    d0 = f["preserve"] - timedelta(days=rng.randint(200, 900))
    if heavy(rng, 0.2):  # 분할·합병·지목변경이 거듭된 토지
        dd = d0 - timedelta(days=rng.randint(4000, 9000))
        area = f["land_total"] * rng.uniform(1.6, 2.4)
        for _ in range(rng.randint(3, 6)):
            dd += timedelta(days=rng.randint(200, 1500))
            if dd >= d0:
                break
            area = area * rng.uniform(0.8, 1.05)
            land_rows.append({"category": rng.choice(["(08)대", "(08)대", "(02)답", "(01)전", "(05)임야"]) if not land_rows else rng.choice(["(08)대", "(08)대", "(02)답"]),
                              "area": _area(round(area, 1)),
                              "reason": f"({rng.choice(['20', '30', '40', '42', '50'])}){D(dd, 'kor')}\n"
                                        + rng.choice(["분할되어 본번에 -%d을 부함" % rng.randint(1, 60), "지목변경", "등록전환",
                                                      "구획정리 완료", "합병", "면적정정", "행정구역명칭변경"])})
    elif rng.random() < 0.5:
        land_rows.append({"category": "(08)대", "area": _area(round(f["land_total"] * rng.uniform(1.05, 1.4), 1)),
                          "reason": f"({rng.choice(['20', '40'])}){D(d0 - timedelta(days=rng.randint(300, 3000)), 'kor')}\n"
                                    + rng.choice(["구획정리 완료", "지목변경", "등록전환"])})
    land_rows.append({"category": "(08)대", "area": _area(f["land_total"]),
                      "reason": f"(30){D(d0, 'kor')}\n분할되어 본번에 -{f['bubun'] or rng.randint(1, 30)}을 부함"
                      if land_rows or rng.random() < 0.5 else f"(40){D(d0, 'kor')}\n구획정리 완료"})
    code = {"소유권보존": "(01)소유권보존", "소유권이전": "(03)소유권이전", "소유권일부이전": "(04)소유권일부이전", "주소변경": "(11)주소변경"}
    owners = []
    for c in hist["chain"]:
        for pi, _ in c["owners"]:
            owners.append({"change_date": D(c["date"], "kor"), "change_cause": code[c["cause"]],
                           "address": _addr_at(pi, c["date"] + timedelta(days=1 if c["cause"] == "주소변경" else 0)),
                           "name": pi["name"], "reg_no": pi["rrn"] if pi["corp"] else K.mask_rrn(pi["rrn"])})
    if f["is_apt"] or pr.kind == "오피스텔":
        n = f["units"] - 1
        for o in owners[1:]:
            o["co_owners"] = f"외 {n:,}인"
    # 개별공시지가 (원/㎡): 대지권 면적당 가치로 역산
    base = pr.official_price * rng.uniform(0.45, 0.65) / max(pr.land_area, 1)
    y = p.issue_date.year if p.issue_date >= date(p.issue_date.year, 5, 31) else p.issue_date.year - 1
    prices = []
    for yy in range(y, y - rng.choice([5, 6, 7, 7]), -1):  # 정부24 발급본은 최근 7년 기본 표시
        prices.append({"base_date": f"{yy}/01/01", "price": won(K.round_to(base, 1000), "")})
        base /= rng.uniform(1.0, 1.1)
    prices.reverse()
    grades = [{"date": f"{yy}.{mm:02d}.01. 수정", "grade": str(g)} for yy, mm, g in
              [(1984, 7, f["land_grade"] - rng.randint(20, 40)), (1987, 7, f["land_grade"] - rng.randint(5, 18)),
               (1990, 1, f["land_grade"])]]
    t = p.issue_date
    return {
        "unique_no": f"{f['dong_code']}-1{f['bonbun']:04d}-{f['bubun']:04d}",
        "drawing_no": str(rng.randint(1, 60)),
        "issue_no": f"{t.year}{rng.randint(10000000, 99999999)}",
        "location": f"{a.region} {a.dong}",
        "sheet_no": f"{rng.randint(1, 3)}-{rng.randint(1, 2)}",
        "processed_time": f"{rng.randint(9, 17):02d}시 {rng.randint(0, 59):02d}분 {rng.randint(0, 59):02d}초",
        "jibun": a.jibun,
        "scale": rng.choice(["수치", "1:1200", "1:600", "1:1000"]),
        "issuer_name": rng.choice(["인터넷민원", "인터넷민원", "무인민원발급기"]),
        "land": land_rows,
        "owners": owners,
        "grades": grades,
        "zoning": f["zoning"],
        "land_prices": prices,
        "issue_date": D(t, rng.choice(["kor", "kor_short"])),
        "issuer": district_office(a),
    }
