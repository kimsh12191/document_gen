"""passport: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/identity.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.identity import _add_years, passport_mrz  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("passport", "여권", "identity", page="passport", sample_mark=True)
def passport(p: Profile, rng: random.Random) -> dict:
    """대한민국 여권 사진정보면 (MRZ 포함)."""
    per = p.person
    lo = max(date(per.birth.year + 18, 1, 1), p.issue_date - timedelta(days=9 * 365))
    issued = rand_date(rng, lo, p.issue_date - timedelta(days=20))
    if special(rng, "old_passport", 0.15) and lo < date(2020, 12, 1):  # 구형 전자여권 (주민등록번호 뒷자리 첫 숫자 인쇄)
        issued = rand_date(rng, lo, date(2020, 12, 1))
    single = special(rng, "single_use", 0.04)  # 단수여권: 종류 PS, 유효기간 1년
    if single:
        issued = rand_date(rng, p.issue_date - timedelta(days=300), p.issue_date - timedelta(days=10))
    ptype = "PS" if single else "PM"
    expiry = (_add_years(issued, 1) if single else _add_years(issued, 10)) - timedelta(days=rng.choice([0, 0, 1]))
    letter = "S" if single else "M"
    if issued >= date(2021, 12, 21):  # 차세대 전자여권: M123A4567
        number = f"{letter}{rng.randint(0, 999):03d}{rng.choice('ABCDEFGHJKLMNPRSTUVWXYZ')}{rng.randint(0, 9999):04d}"
    else:
        number = f"{letter}{rng.randint(0, 99999999):08d}"
    given = per.given_en
    if rng.random() < 0.3 and len(given) > 3:  # 'GILDONG' / 'GIL DONG' 표기 혼재
        sylls = [K.GIVEN_ROMAN[c] for c in per.name[-2:]]
        if "".join(sylls) == given:
            given = " ".join(sylls)
    l1, l2 = passport_mrz(ptype, per.surname_en, given, number, per.birth, per.gender, expiry)
    nextgen = issued >= date(2021, 12, 21)

    def pd(d: date) -> str:
        # 차세대 전자여권: 월 한글/영문 병기 ('05 3월/MAR 2021'), 구형: '05 MAR 2021'
        return f"{d.day:02d} {d.month}월/{D(d, 'en').split()[1]} {d.year}" if nextgen else D(d, "en")

    out = {
        "type": ptype,
        "country_code": "KOR",
        "passport_no": number,
        "surname": per.surname_en,
        "given_names": given,
        "name_korean": per.name,
        "nationality": "REPUBLIC OF KOREA",
        "date_of_birth": pd(per.birth),
        "sex": per.gender,
        "date_of_issue": pd(issued),
        "date_of_expiry": pd(expiry),
        "authority": "외교부/MINISTRY OF FOREIGN AFFAIRS" if nextgen else "MINISTRY OF FOREIGN AFFAIRS",
    }
    if issued < date(2020, 12, 21):  # 구형 여권에는 주민등록번호 뒷자리가 인쇄됨
        out["personal_no"] = per.rrn.split("-")[1][0] + "******"
    out["mrz"] = {"line1": l1, "line2": l2}
    return out
