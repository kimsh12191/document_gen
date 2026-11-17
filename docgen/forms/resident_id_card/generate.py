"""resident_id_card: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/identity.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.registry import doc


@doc("resident_id_card", "주민등록증", "identity", page="card", sample_mark=True)
def resident_id_card(p: Profile, rng: random.Random) -> dict:
    """주민등록증 앞면."""
    a = p.person.address
    issued = rand_date(rng, date(max(p.person.birth.year + 17, 2005), 1, 1), p.issue_date - timedelta(days=30))
    if special(rng, "reissued", 0.15):  # 분실·훼손 재발급: 발행일이 최근 날짜로 바뀐다 (앞면에 '재발급' 글자는 없음)
        issued = rand_date(rng, p.issue_date - timedelta(days=700), p.issue_date - timedelta(days=20))
    out = {
        "name": p.person.name,
        "name_hanja": p.person.hanja,
        "rrn": p.person.rrn,
        "address": f"{a.road_short}\n({a.dong}{', ' + a.building_name if a.building_name else ''})",
        # 카드 인쇄 발행일은 '2015. 3. 20.' (0 채움 없음) 표기가 일반적
        "issue_date": f"{issued.year}. {issued.month}. {issued.day}." if rng.random() < 0.75 else D(issued, "dot"),
        "issuer": district_office(a),
    }
    if special(rng, "no_hanja", 0.08):  # 한자 성명이 없는 사람: 괄호 한자 없이 한글 성명만
        del out["name_hanja"]
    if special(rng, "overseas_national", 0.03):  # 재외국민 주민등록증: 앞면에 '재외국민' 표시
        out["resident_type"] = "재외국민"
    return out
