"""신원·신분 확인 서류. 모두 '견본' 표시가 강제로 들어간다 (sample_mark=True).

이 파일에는 그룹 서식들이 같이 쓰는 도우미만 있다. 서식마다 값 만드는 함수(@doc)는 서식 폴더
docgen/forms/<ID>/generate.py 에 있고, 끝의 FORMS 차례로 등록한다.
"""
from ._common import *  # noqa: F401,F403
from ..registry import register_folder_forms


# ---------------------------------------------------------------------------
# 공통 헬퍼 (이 모듈 전용)
# ---------------------------------------------------------------------------

def _add_years(d: date, n: int) -> date:
    try:
        return d.replace(year=d.year + n)
    except ValueError:  # 2/29
        return d.replace(year=d.year + n, day=28)


def _center_head(addr: Address) -> str:
    """주민센터(읍·면·동)장 명칭. 예) '서울특별시 강남구 역삼동장'"""
    return " ".join(x for x in (addr.sido, addr.sigungu, addr.dong + "장") if x)


def _local_issuer(rng: random.Random, addr: Address) -> str:
    """읍·면·동장 또는 시장·구청장·군수 중 하나."""
    return _center_head(addr) if rng.random() < 0.7 else district_office(addr)


def _rand_person_text(rng: random.Random, birth_range=(1955, 1995)):
    """거래 상대방 등 문서에만 나오는 인물: (성명, 주민등록번호, 주소)."""
    gender = rng.choice("MF")
    name = K.make_name(rng, gender)[0]
    birth = rand_date(rng, date(birth_range[0], 1, 1), date(birth_range[1], 12, 31))
    sido, sigungu, _zip, _dongs, roads = rng.choice(K.REGIONS)
    region = " ".join(x for x in (sido, sigungu) if x)
    addr = f"{region} {rng.choice(roads)} {rng.randint(1, 650)}"
    if rng.random() < 0.6:
        addr += f", {rng.randint(101, 125)}동 {rng.randint(1, 25)}{rng.randint(1, 4):02d}호"
    return name, K.rrn(rng, birth, gender), addr


# ---------------------------------------------------------------------------
# 운전면허증
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 여권 (정보면)
# ---------------------------------------------------------------------------

def _mrz_val(c: str) -> int:
    if c.isdigit():
        return int(c)
    if c == "<":
        return 0
    return ord(c) - ord("A") + 10


def _mrz_check(s: str) -> str:
    w = (7, 3, 1)
    return str(sum(_mrz_val(c) * w[i % 3] for i, c in enumerate(s)) % 10)


def _mrz_name(s: str) -> str:
    return "".join(c if c.isalpha() else "<" for c in s.upper())


def passport_mrz(doc_type: str, surname: str, given: str, number: str, dob: date, sex: str,
                 expiry: date, optional: str = "") -> tuple[str, str]:
    """ICAO 9303 TD3 2줄 MRZ (체크 디지트 계산 포함)."""
    line1 = (doc_type.ljust(2, "<") + "KOR" + _mrz_name(surname) + "<<" + _mrz_name(given)).ljust(44, "<")[:44]
    num = number.ljust(9, "<")
    b = f"{dob:%y%m%d}"
    e = f"{expiry:%y%m%d}"
    opt = optional.ljust(14, "<")
    opt_chk = _mrz_check(opt) if optional else "<"
    composite = num + _mrz_check(num) + b + _mrz_check(b) + e + _mrz_check(e) + opt + opt_chk
    line2 = (num + _mrz_check(num) + "KOR" + b + _mrz_check(b) + sex + e + _mrz_check(e) + opt + opt_chk
             + _mrz_check(composite))
    assert len(line2) == 44, line2
    return line1, line2


# ---------------------------------------------------------------------------
# 외국인등록증
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 인감증명서 / 본인서명사실확인서
# ---------------------------------------------------------------------------

def _corp_party(rng: random.Random):
    """법인 거래상대방: (법인명, 법인등록번호, 본점 소재지)."""
    from ..entities import COMPANY_PREFIX
    name = rng.choice(["주식회사 ", ""]) + rng.choice(COMPANY_PREFIX) + rng.choice(["개발", "건설", "디앤씨", "부동산", "에셋", "홀딩스"])
    if not name.startswith("주식회사"):
        name += rng.choice([" 주식회사", "(주)"])
    sido, sigungu, _z, _d, roads = rng.choice(K.REGIONS)
    return name, K.corp_reg_no(rng), f"{' '.join(x for x in (sido, sigungu) if x)} {rng.choice(roads)} {rng.randint(1, 500)}"


# 이 그룹의 코드 서식. 값 만드는 함수는 서식 폴더 docgen/forms/<ID>/generate.py 에 있다 (여기는 같이 쓰는 도우미).
FORMS = ('resident_id_card', 'driver_license', 'passport', 'alien_registration_card', 'seal_certificate', 'signature_confirmation',)
register_folder_forms(__name__, FORMS)   # 예전 @doc 차례 그대로 등록 (서식 목록·데이터셋 순서)
