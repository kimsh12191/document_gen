"""move_in_household_list: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/real_estate.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.real_estate import _facts, _rand_person  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


def _mask_name(name: str) -> str:
    """홍길동 -> 홍*동, 김민 -> 김*, 남궁민수 -> 남**수"""
    if len(name) <= 2:
        return name[0] + "*"
    return name[0] + "*" * (len(name) - 2) + name[-1]


@doc("move_in_household_list", "전입세대확인서", "real_estate")
def move_in_household_list(p: Profile, rng: random.Random) -> dict:
    """전입세대확인서(열람). 해당 주소에 전입신고된 세대주 목록.

    다세대·오피스텔을 건물 전체(동·호 없이)로 열람하면 여러 세대가 나오고, 많으면 여러 쪽이 된다."""
    f = _facts(p)
    a, pr, seller = f["a"], f["pr"], f["pr"].seller
    rows = []
    if f["transferred"]:
        heads = [(p.person.name, f["balance"] + timedelta(days=rng.randint(0, 14)))]
    elif f["seller_resident"]:
        heads = [(seller.name, f["seller_acq"] + timedelta(days=rng.randint(0, 30)))]
        if rng.random() < 0.15:
            heads.append((_rand_person(rng), heads[0][1] + timedelta(days=rng.randint(200, 2000))))
    else:
        heads = [(_rand_person(rng), p.issue_date - timedelta(days=rng.randint(200, 1400)))]
    long_doc = heavy(rng, 0.2)
    multi = pr.kind != "아파트" and (long_doc or special(rng, "multi_household", 0.15))
    cohab_case = special(rng, "cohabitant", 0.12)
    unknown = special(rng, "unknown_resident", 0.05)  # 거주불명자 등록 세대
    units = [(f["ho"], nm, d) for nm, d in heads]
    if multi:  # 같은 건물 다른 호실 세대
        n = rng.randint(14, 28) if long_doc else rng.randint(4, 9)
        per_floor = max(2, f["units_per_floor"])
        floors = max(2, f["total_floors"])
        cand = [f"{fl}{i:02d}" for fl in range(1, floors + 1) for i in range(1, per_floor + 1)]
        if pr.kind == "다세대주택" and rng.random() < 0.5:
            cand += [f"B{i:02d}" for i in range(1, per_floor + 1)]
        cand = [c for c in cand if c != f["ho"]]
        for ho in rng.sample(cand, min(n, len(cand))):
            units.append((ho, _rand_person(rng), p.issue_date - timedelta(days=rng.randint(10, 3600))))
            if rng.random() < 0.1:  # 한 호실에 세대가 둘
                units.append((ho, _rand_person(rng), p.issue_date - timedelta(days=rng.randint(10, 2000))))
        units.sort(key=lambda u: (not u[0].startswith("B"), int(u[0].lstrip("B")), u[2]))
    cohab = []
    for i, (ho, nm, d) in enumerate(units):
        first_same = rng.random() < 0.75
        first_nm, first_d = (nm, d) if first_same else (_rand_person(rng), d - timedelta(days=rng.randint(0, 3)))
        n_co = 1 if rng.random() < 0.15 else 0  # 주민등록표상 동거인(세대원 아님)은 드묾
        if cohab_case and ho == f["ho"] and i == next(j for j, u in enumerate(units) if u[0] == f["ho"]):
            n_co = rng.randint(1, 2)
        reg = "거주불명자" if unknown and i == len(units) - 1 and len(units) > 1 else "거주자"
        row = {"no": str(i + 1), "head_name": _mask_name(nm), "move_in_date": D(min(d, p.issue_date), "dash"),
               "reg_type": reg, "first_name": _mask_name(first_nm), "first_date": D(min(first_d, p.issue_date), "dash"),
               "first_reg_type": reg, "cohabitants": str(n_co)}
        if multi:
            row = {"no": row["no"], "unit": f"{ho}호", **{k: v for k, v in row.items() if k != "no"}}
        rows.append(row)
        for _ in range(n_co):
            cd = min(d + timedelta(days=rng.randint(30, 900)), p.issue_date)
            cohab.append({"no": str(len(cohab) + 1), "name": _mask_name(_rand_person(rng)), "move_in_date": D(cd, "dash"),
                          "reg_type": "거주자"})
    purpose = rng.choice(["금융기관 대출(주택담보대출)", "금융기관 제출", "전세자금대출 신청", "임대차계약 체결"])
    jibun = f"{a.jibun_full} " + (f"{f['dong_no']}동 " if f["dong_no"] else "") + f"{f['ho']}호"
    road = a.road_full
    if multi:  # 건물 전체 열람: 동·호 없이
        jibun = a.jibun_full
        road = f"{a.region} {a.road} {a.building_no} ({a.dong}" + (f", {a.building_name})" if a.building_name else ")")
    return {
        "issue_no": issue_no(rng, 16),
        "issue_date": D(p.issue_date, "dot"),
        "address": road,
        "jibun_address": jibun,
        "households": rows,
        **({"cohabitants": cohab} if cohab else {}),
        "kind": rng.choice(["열람", "교부", "교부"]),
        "applicant": {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn), "address": p.person.address.road_full,
                      "purpose": purpose},
        "view_date": D(p.issue_date, "kor"),
        "issuer": community_center(a),
    }
