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
        # 카드 인쇄 발행일은 '2015. 3. 20.' (0 채움 없음) 표기가 일반적
        "issue_date": f"{issued.year}. {issued.month}. {issued.day}." if rng.random() < 0.75 else D(issued, "dot"),
        "issuer": district_office(a),
    }


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
    code = _POLICE[a.sido][0] if rng.random() < 0.75 else rng.choice([v[0] for v in _POLICE.values()] + ["28"])
    if a.sido == "경기도" and a.sigungu.startswith(_GG_NORTH) and code == "13":
        code = "28"  # 경기북부
    # AA-BB-CCCCCC-DE: 최초 발급지역·연도·일련번호·체크숫자(D)·발급회차(E)
    lic_no = f"{code}-{acquired.year % 100:02d}-{rng.randint(0, 999999):06d}-{rng.randint(0, 9)}{rng.choice('1111223')}"
    kind = rng.choices(["1종보통", "2종보통", "1종대형", "2종소형"], [55, 38, 5, 2])[0]
    renew = _add_years(issued, 10)
    if issued >= date(2026, 1, 1):  # 2026년 이후 발급분: 생일 전후 6개월
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
    if rng.random() < 0.25:
        out["condition"] = rng.choice(["A", "A", "B", "E"])
    out.update({
        "issue_date": D(issued, "dot"),
        "issuer": _police_name(a.sido, a.sigungu, issued),
        "serial": "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789") for _ in range(6)),
    })
    return out


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


@doc("passport", "여권", "identity", page="passport", sample_mark=True)
def passport(p: Profile, rng: random.Random) -> dict:
    """대한민국 여권 사진정보면 (MRZ 포함)."""
    per = p.person
    issued = rand_date(rng, max(date(per.birth.year + 18, 1, 1), p.issue_date - timedelta(days=9 * 365)),
                       p.issue_date - timedelta(days=20))
    expiry = _add_years(issued, 10) - timedelta(days=rng.choice([0, 0, 1]))
    if issued >= date(2021, 12, 21):  # 차세대 전자여권: M123A4567
        number = f"M{rng.randint(0, 999):03d}{rng.choice('ABCDEFGHJKLMNPRSTUVWXYZ')}{rng.randint(0, 9999):04d}"
    else:
        number = f"{rng.choice('MMMS')}{rng.randint(0, 99999999):08d}"
    given = per.given_en
    if rng.random() < 0.3 and len(given) > 3:  # 'GILDONG' / 'GIL DONG' 표기 혼재
        sylls = [K.GIVEN_ROMAN[c] for c in per.name[-2:]]
        if "".join(sylls) == given:
            given = " ".join(sylls)
    l1, l2 = passport_mrz("PM", per.surname_en, given, number, per.birth, per.gender, expiry)
    nextgen = issued >= date(2021, 12, 21)

    def pd(d: date) -> str:
        # 차세대 전자여권: 월 한글/영문 병기 ('05 3월/MAR 2021'), 구형: '05 MAR 2021'
        return f"{d.day:02d} {d.month}월/{D(d, 'en').split()[1]} {d.year}" if nextgen else D(d, "en")

    out = {
        "type": "PM",
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


# ---------------------------------------------------------------------------
# 외국인등록증
# ---------------------------------------------------------------------------

_FOREIGNERS = {
    # 국가: (남성 이름들, 여성 이름들, 성들)
    "VIETNAM": (["VAN AN", "VAN HUNG", "MINH TUAN", "DUC THANH", "QUANG HUY"],
                ["THI HOA", "THI LAN", "THU TRANG", "NGOC ANH", "THI MAI"],
                ["NGUYEN", "TRAN", "LE", "PHAM", "HOANG", "VU"]),
    "CHINA": (["WEI", "JIANGUO", "HAOYU", "ZHIQIANG", "XIAOMING"],
              ["LI NA", "XIAOYAN", "MEILING", "JING", "YUQI"],
              ["WANG", "LI", "ZHANG", "LIU", "CHEN", "ZHAO"]),
    "UNITED STATES OF AMERICA": (["JOHN MICHAEL", "DAVID JAMES", "ROBERT", "DANIEL", "CHRISTOPHER"],
                                 ["EMILY ROSE", "SARAH", "JESSICA ANN", "MEGAN", "ASHLEY"],
                                 ["SMITH", "JOHNSON", "WILLIAMS", "BROWN", "MILLER", "DAVIS"]),
    "PHILIPPINES": (["JOSE", "MARK ANTHONY", "JOHN PAUL", "RAMON"], ["MARIA CRISTINA", "ANGELICA", "JOY", "ROSALIE"],
                    ["SANTOS", "REYES", "CRUZ", "BAUTISTA", "GARCIA"]),
    "UZBEKISTAN": (["DILSHOD", "BEKZOD", "SARDOR", "RUSTAM"], ["NILUFAR", "DILNOZA", "MADINA", "ZARINA"],
                   ["KARIMOV", "RAKHIMOV", "YUSUPOV", "TOSHMATOV"]),
    "INDONESIA": (["BUDI", "AGUS", "RIZKY"], ["SITI", "DEWI", "PUTRI"], ["SANTOSO", "WIJAYA", "PRATAMA", "HIDAYAT"]),
    "NEPAL": (["RAM BAHADUR", "BIKASH", "SURESH"], ["SITA", "ANITA", "SUNITA"], ["SHRESTHA", "GURUNG", "TAMANG", "RAI"]),
    "THAILAND": (["SOMCHAI", "ANAN", "KITTI"], ["SUDA", "MALEE", "NARUMOL"], ["SRISUK", "WONGSA", "CHAIYAPORN"]),
    "MONGOLIA": (["BATBAYAR", "GANBOLD", "TEMUULEN"], ["OYUNCHIMEG", "NARANTUYA", "ANUJIN"], ["BATAA", "DORJ", "ENKHBAYAR"]),
    "JAPAN": (["HIROSHI", "TAKUYA", "KENJI"], ["YUKI", "AYAKA", "MISAKI"], ["TANAKA", "SATO", "SUZUKI", "WATANABE"]),
    "INDIA": (["RAHUL", "AMIT KUMAR", "VIKRAM"], ["PRIYA", "ANANYA", "DEEPIKA"], ["SHARMA", "PATEL", "SINGH", "GUPTA"]),
    "CANADA": (["RYAN", "MATTHEW"], ["OLIVIA", "HANNAH"], ["TREMBLAY", "WILSON", "MARTIN"]),
}

_VISAS = [("E-7", "특정활동", 20), ("E-9", "비전문취업", 18), ("D-2", "유학", 12), ("F-6", "결혼이민", 10),
          ("F-5", "영주", 8), ("F-2", "거주", 6), ("H-2", "방문취업", 6), ("E-2", "회화지도", 6),
          ("D-8", "기업투자", 4), ("F-4", "재외동포", 6), ("D-10", "구직", 4)]

_IMMIGRATION = {
    "서울특별시": ["서울출입국·외국인청장", "서울남부출입국·외국인사무소장"],
    "부산광역시": ["부산출입국·외국인청장"], "대구광역시": ["대구출입국·외국인사무소장"],
    "인천광역시": ["인천출입국·외국인청장"], "광주광역시": ["광주출입국·외국인사무소장"],
    "대전광역시": ["대전출입국·외국인사무소장"], "울산광역시": ["울산출입국·외국인사무소장"],
    "세종특별자치시": ["대전출입국·외국인사무소장"], "경기도": ["수원출입국·외국인청장", "양주출입국·외국인사무소장"],
    "강원특별자치도": ["춘천출입국·외국인사무소장"], "충청북도": ["청주출입국·외국인사무소장"],
    "충청남도": ["대전출입국·외국인사무소장"], "전북특별자치도": ["전주출입국·외국인사무소장"],
    "전라남도": ["광주출입국·외국인사무소장"], "경상북도": ["대구출입국·외국인사무소장"],
    "경상남도": ["창원출입국·외국인사무소장"], "제주특별자치도": ["제주출입국·외국인청장"],
}


@doc("alien_registration_card", "외국인등록증", "identity", page="card", sample_mark=True)
def alien_registration_card(p: Profile, rng: random.Random) -> dict:
    """외국인등록증(RESIDENCE CARD) 앞면. 프로필에 외국인이 없으므로 이 서류 안에서 외국인을 만든다."""
    country = rng.choice(list(_FOREIGNERS))
    males, females, surnames = _FOREIGNERS[country]
    gender = rng.choice("MF")
    surname = rng.choice(surnames)
    given = rng.choice(males if gender == "M" else females)
    if country == "VIETNAM" and gender == "M" and given.startswith("THI"):
        given = "VAN AN"
    birth = rand_date(rng, date(1968, 1, 1), date(2003, 12, 31))
    visa, visa_name, _w = rng.choices(_VISAS, [v[2] for v in _VISAS])[0]
    issued = rand_date(rng, p.issue_date - timedelta(days=4 * 365), p.issue_date - timedelta(days=15))
    a = p.person.address
    return {
        "registration_no": K.rrn(rng, birth, gender, foreigner=True),
        "name": f"{surname} {given}",
        "country": country,
        "sex": gender,
        "visa_status": f"{visa_name}({visa})" if rng.random() < 0.75 else f"{visa} ({visa_name})",
        "issue_date": D(issued, "dot"),
        "issuer": rng.choice(_IMMIGRATION[a.sido]),
    }


# ---------------------------------------------------------------------------
# 인감증명서 / 본인서명사실확인서
# ---------------------------------------------------------------------------

@doc("seal_certificate", "인감증명서", "identity", sample_mark=True)
def seal_certificate(p: Profile, rng: random.Random) -> dict:
    """인감증명서 (인감증명법 시행령 별지 제14호서식 / 전자발급 제14호의2서식). 일반용 / 부동산 매도용."""
    per = p.person
    a = per.address
    online = rng.random() < 0.25  # 2024.9.30.~ 정부24 전자발급(일반용만)
    kind = "일반용" if online else rng.choice(["일반용", "일반용", "부동산 매도용"])
    out = {
        "doc_no": issue_no(rng, 16) if online else issue_no(rng, 12),
        "applicant_type": "본인" if online or rng.random() < 0.85 else "대리인",
        "person": {
            "name": per.name,
            "name_hanja": per.hanja,
            "rrn": per.rrn,
            "nationality": per.nationality,
            "address": a.road_full,
        },
        "seal_name": per.name + "인",
        "usage_type": kind,
    }
    if out["applicant_type"] == "대리인":
        name, rrn, _ = _rand_person_text(rng)
        out["agent"] = {"name": name, "rrn": K.mask_rrn(rrn)}
    if kind == "부동산 매도용":
        name, rrn, addr = _rand_person_text(rng)
        out["buyer"] = {"name": name, "rrn": rrn, "address": addr}
        out["applicant_signature"] = per.name if out["applicant_type"] == "본인" else out["agent"]["name"]
    out["issue_date"] = D(p.issue_date, rng.choice(["kor", "kor_short"]))
    out["issuer"] = _local_issuer(rng, a)
    return out


_SIG_RE_USAGES = ["소유권 이전(매매, 증여 등)", "제한물권 설정(근저당권 설정, 전세권 설정 등)", "그 밖의 용도(가등기 설정, 가등기 말소 등)"]


@doc("signature_confirmation", "본인서명사실확인서", "identity", sample_mark=True)
def signature_confirmation(p: Profile, rng: random.Random) -> dict:
    """본인서명사실확인서 (본인서명사실 확인 등에 관한 법률 시행령 별지 제2호서식)."""
    per = p.person
    a = per.address
    out = {
        "doc_no": issue_no(rng, 16),
        "signer": {"name": per.name, "rrn": per.rrn, "address": a.road_full},
    }
    r = rng.random()
    if r < 0.5:  # 부동산 관련 용도
        usage = rng.choices(_SIG_RE_USAGES, [35, 55, 10])[0]
        out["real_estate_usage"] = usage
        if usage.startswith("소유권"):
            name, rrn, addr = _rand_person_text(rng)
            out["counterparty"] = {"name": name, "rrn": rrn, "address": addr}
        elif usage.startswith("제한물권"):  # 근저당권자 = 대출 은행(법인)
            out["counterparty"] = {
                "name": f"주식회사 {p.bank}",
                "rrn": K.corp_reg_no(rng),
                "address": f"서울특별시 중구 {rng.choice(['을지로', '세종대로', '남대문로', '소공로'])} {rng.randint(10, 120)}",
            }
    else:  # 그 외의 용도 (제출기관이 요청하는 내용)
        out["other_usage"] = rng.choice([
            f"대출보증용({p.bank} {p.bank_branch} 제출)", f"금융기관 대출 약정용({p.bank} 제출)",
            "대출보증용", "법인등기용", "보증 계약용", f"여신거래 약정용({p.bank} {p.bank_branch})",
        ])
    if rng.random() < 0.12:
        name, _rrn, addr = _rand_person_text(rng)
        out["delegate"] = {"name": name, "address": addr}
    out["signature"] = per.name
    out["issue_date"] = D(p.issue_date, rng.choice(["kor", "kor_short"]))
    out["issuer"] = _local_issuer(rng, a)
    return out
