"""소득·재직 관련 서류."""
from ..registry import doc
from ._common import *  # noqa: F401,F403


@doc("employment_certificate", "재직증명서", "income")
def employment_certificate(p: Profile, rng: random.Random) -> dict:
    """회사가 발급하는 재직증명서."""
    e = p.employment
    c = e.company
    purpose = rng.choice(["금융기관 제출용", "은행 제출용", "대출 신청용", "제출처: " + p.bank])
    return {
        "doc_no": f"제 {p.issue_date.year}-{rng.randint(1, 999):03d} 호",
        "employee": {
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.6 else p.person.rrn,
            "address": p.person.address.road_full,
        },
        "employment": {
            "department": e.department,
            "position": e.position,
            "job": e.job,
            "period": f"{D(e.hire_date, 'kor')} ~ 현재",
        },
        "company": {
            "name": c.name,
            "biz_no": c.biz_no,
            "address": c.address.road_short,
            "phone": c.phone,
            "ceo": c.ceo.name,
        },
        "purpose": purpose,
        "issue_date": D(p.issue_date, rng.choice(["kor", "kor_short"])),
    }
