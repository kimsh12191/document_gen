"""신원·신분 확인 서류. 모두 '견본' 표시가 강제로 들어간다 (sample_mark=True)."""
from ..registry import doc
from ._common import *  # noqa: F401,F403


@doc("resident_id_card", "주민등록증", "identity", page="card", sample_mark=True)
def resident_id_card(p: Profile, rng: random.Random) -> dict:
    """주민등록증 앞면."""
    a = p.person.address
    issued = rand_date(rng, date(max(p.person.birth.year + 17, 2005), 1, 1), p.issue_date - timedelta(days=30))
    return {
        "name": p.person.name,
        "name_hanja": p.person.hanja,
        "rrn": p.person.rrn,
        "address": f"{a.road_short}\n({a.dong}{', ' + a.building_name if a.building_name else ''})",
        "issue_date": D(issued, "dot"),
        "issuer": district_office(a),
    }
