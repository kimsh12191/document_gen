"""driver_license: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/identity.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.identity import _add_years  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


# 시·도 → (면허번호 지역코드, 시도경찰청 명칭(2021~), 지방경찰청 명칭(~2020))
_POLICE = {
    "서울특별시": ("11", "서울특별시경찰청장", "서울지방경찰청장"),
    "부산광역시": ("12", "부산광역시경찰청장", "부산지방경찰청장"),
    "경기도": ("13", "경기도남부경찰청장", "경기남부지방경찰청장"),
    "강원특별자치도": ("14", "강원특별자치도경찰청장", "강원지방경찰청장"),
    "충청북도": ("15", "충청북도경찰청장", "충북지방경찰청장"),
    "충청남도": ("16", "충청남도경찰청장", "충남지방경찰청장"),
    "전북특별자치도": ("17", "전북특별자치도경찰청장", "전북지방경찰청장"),
    "전라남도": ("18", "전라남도경찰청장", "전남지방경찰청장"),
    "경상북도": ("19", "경상북도경찰청장", "경북지방경찰청장"),
    "경상남도": ("20", "경상남도경찰청장", "경남지방경찰청장"),
    "제주특별자치도": ("21", "제주특별자치도경찰청장", "제주지방경찰청장"),
    "대구광역시": ("22", "대구광역시경찰청장", "대구지방경찰청장"),
    "인천광역시": ("23", "인천광역시경찰청장", "인천지방경찰청장"),
    "광주광역시": ("24", "광주광역시경찰청장", "광주지방경찰청장"),
    "대전광역시": ("25", "대전광역시경찰청장", "대전지방경찰청장"),
    "울산광역시": ("26", "울산광역시경찰청장", "울산지방경찰청장"),
    "세종특별자치시": ("25", "세종특별자치시경찰청장", "세종지방경찰청장"),
}


_GG_NORTH = ("고양", "의정부", "남양주", "파주", "양주", "구리", "포천", "동두천", "가평", "연천")


def _police_name(sido: str, sigungu: str, issued: date) -> str:
    _code, new, old = _POLICE[sido]
    if sido == "경기도" and sigungu.startswith(_GG_NORTH):
        new, old = "경기도북부경찰청장", "경기북부지방경찰청장"
    if sido == "강원특별자치도" and issued < date(2023, 6, 11):
        new = "강원도경찰청장"
    if sido == "전북특별자치도" and issued < date(2024, 1, 18):
        new = "전라북도경찰청장"
    return new if issued >= date(2021, 1, 1) else old


@doc("driver_license", "운전면허증", "identity", page="card", sample_mark=True)
def driver_license(p: Profile, rng: random.Random) -> dict:
    """자동차운전면허증 앞면."""
    per = p.person
    a = per.address
    acquired = rand_date(rng, date(per.birth.year + 19, 1, 1), min(date(per.birth.year + 32, 12, 31), p.issue_date - timedelta(days=400)))
    # 최근 갱신(발급)일: 취득 후 10년 주기, 마지막 주기 안
    issued = acquired
    while _add_years(issued, 10) < p.issue_date - timedelta(days=30):
        issued = _add_years(issued, 10)
    issued = rand_date(rng, issued, min(_add_years(issued, 1), p.issue_date - timedelta(days=30)))
    renew_base = issued
    reissued = special(rng, "reissued", 0.12)  # 분실 재발급: 발급일은 최근, 면허번호 끝자리(발급회차) 증가
    if reissued:
        issued = rand_date(rng, max(issued, p.issue_date - timedelta(days=900)), p.issue_date - timedelta(days=20))
    code = _POLICE[a.sido][0] if rng.random() < 0.75 else rng.choice([v[0] for v in _POLICE.values()] + ["28"])
    if a.sido == "경기도" and a.sigungu.startswith(_GG_NORTH) and code == "13":
        code = "28"  # 경기북부
    # AA-BB-CCCCCC-DE: 최초 발급지역·연도·일련번호·체크숫자(D)·발급회차(E)
    lic_no = f"{code}-{acquired.year % 100:02d}-{rng.randint(0, 999999):06d}-{rng.randint(0, 9)}{rng.choice('1111223') if not reissued else rng.choice('234')}"
    kind = rng.choices(["1종보통", "2종보통", "1종대형", "2종소형"], [55, 38, 5, 2])[0]
    renew = _add_years(renew_base, 10)  # 재발급해도 적성검사(갱신)기간은 그대로
    if renew_base >= date(2026, 1, 1):  # 2026년 이후 발급분: 생일 전후 6개월
        bday = _add_years(per.birth, renew.year - per.birth.year)
        lo, hi = bday - timedelta(days=183), bday + timedelta(days=182)
        period = f"{lo:%Y.%m.%d}~{hi:%Y.%m.%d}"
    else:  # 종전: 10년이 되는 해 1.1.~12.31.
        period = f"{renew.year}.01.01~{renew.year}.12.31"
    out = {
        "license_type": kind,
        "license_no": lic_no,
        "name": per.name,
        "rrn": per.rrn if rng.random() < 0.8 else K.mask_rrn(per.rrn),
        "address": a.road_short if len(a.road_short) <= 34 or rng.random() < 0.5 else f"{a.region} {a.road} {a.building_no}\n{a.detail}",
    }
    if kind.startswith("1종"):
        out["aptitude_period"] = period
    else:
        out["renewal_period"] = period
    if special(rng, "condition", 0.2):  # 조건: A 자동변속기, B 의수, C 의족, D 보청기, E 청각장애인 표지·볼록거울
        out["condition"] = rng.choice(["A", "A", "A", "B", "C", "D", "E"])
    out.update({
        "issue_date": D(issued, "dot"),
        "issuer": _police_name(a.sido, a.sigungu, issued),
        "serial": "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789") for _ in range(6)),
    })
    return out
