"""합성 고객 프로필.

하나의 Profile 안의 사람/회사/부동산/계좌 정보는 서로 일관되게 생성되므로,
같은 프로필로 여러 서류를 만들면 '한 고객이 제출한 서류 묶음'이 된다.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import date, timedelta

from . import korean as K


def rand_date(rng: random.Random, start: date, end: date) -> date:
    return start + timedelta(days=rng.randint(0, max(0, (end - start).days)))


@dataclass
class Address:
    sido: str
    sigungu: str
    dong: str
    road: str
    building_no: str
    jibun: str
    detail: str
    building_name: str
    zipcode: str

    @property
    def region(self) -> str:
        return " ".join(x for x in (self.sido, self.sigungu) if x)

    @property
    def road_full(self) -> str:
        """도로명주소: 서울특별시 강남구 테헤란로 123, 101동 1203호 (역삼동, 래미안아파트)"""
        s = f"{self.region} {self.road} {self.building_no}"
        if self.detail:
            s += f", {self.detail}"
        extra = ", ".join(x for x in (self.dong, self.building_name) if x)
        return f"{s} ({extra})"

    @property
    def road_short(self) -> str:
        s = f"{self.region} {self.road} {self.building_no}"
        return f"{s}, {self.detail}" if self.detail else s

    @property
    def jibun_full(self) -> str:
        """지번주소: 서울특별시 강남구 역삼동 123-45"""
        return f"{self.region} {self.dong} {self.jibun}"


@dataclass
class Person:
    name: str
    hanja: str
    surname_en: str
    given_en: str
    gender: str  # "M" / "F"
    birth: date
    rrn: str
    address: Address
    mobile: str
    email: str
    nationality: str = "대한민국"

    @property
    def name_en(self) -> str:
        return f"{self.surname_en} {self.given_en}"

    @property
    def age(self) -> int:
        return 2026 - self.birth.year

    @property
    def gender_ko(self) -> str:
        return "남" if self.gender == "M" else "여"


@dataclass
class Company:
    name: str
    name_en: str
    biz_no: str
    corp_no: str | None
    ceo: Person
    address: Address
    phone: str
    fax: str
    biz_type: str  # 업태
    biz_item: str  # 종목
    established: date
    capital: int
    employees: int
    revenue: int  # 연매출(원)
    kind: str  # "법인" / "개인"
    email: str = ""


@dataclass
class Employment:
    company: Company
    department: str
    position: str
    job: str
    hire_date: date
    annual_salary: int
    employee_no: str


@dataclass
class Property:
    address: Address
    kind: str  # 아파트 / 오피스텔 / 단독주택 / 다세대
    land_area: float  # 대지권 면적 ㎡
    exclusive_area: float  # 전용면적 ㎡
    floor: int
    total_floors: int
    structure: str
    completed: date
    price: int
    official_price: int
    unique_no: str
    seller: Person
    lease_deposit: int


@dataclass
class BankAccount:
    bank: str
    branch: str
    number: str
    holder: str
    opened: date
    balance: int


@dataclass
class ForeignParty:
    name: str
    address: str
    country: str
    contact: str
    email: str
    bank: str
    swift: str
    account: str


@dataclass
class Profile:
    seed: int
    issue_date: date
    person: Person
    spouse: Person | None
    children: list[Person]
    father: Person
    mother: Person
    address_history: list[tuple[date, Address]]
    employment: Employment
    business: Company  # 본인이 대표인 개인사업자
    corporation: Company  # 본인이 대표이사인 법인
    directors: list[Person]
    shareholders: list[tuple[Person | str, int]]  # (주주, 주식수)
    property: Property
    accounts: list[BankAccount]
    bank: str
    bank_branch: str
    foreign: ForeignParty
    extra: dict = field(default_factory=dict)


BANKS = ["국민은행", "신한은행", "우리은행", "하나은행", "농협은행", "기업은행", "SC제일은행",
         "부산은행", "iM뱅크", "카카오뱅크", "토스뱅크", "케이뱅크", "수협은행", "경남은행"]
BANK_ACCT_FMT = {"국민은행": "######-##-######", "신한은행": "###-###-######", "우리은행": "####-###-######",
                 "하나은행": "###-######-#####", "농협은행": "###-####-####-##", "기업은행": "###-######-##-###",
                 "카카오뱅크": "3333-##-#######", "토스뱅크": "1000-####-####", "케이뱅크": "100-###-######"}
BRANCH_SUFFIX = ["역삼", "삼성역", "여의도", "광화문", "명동", "판교", "서초", "잠실", "해운대", "센텀",
                 "수원", "분당", "일산", "송도", "둔산", "상무", "청주", "창원", "범어", "을지로"]

COMPANY_PREFIX = ["한빛", "대성", "미래", "세진", "동방", "태평양", "새한", "청솔", "우진", "다온", "누리",
                  "한결", "가온", "에이스", "제일", "삼정", "대한", "현대", "하나로", "신영", "그린",
                  "블루", "스마트", "넥스트", "코리아", "글로벌", "유니온", "아이엠", "케이", "디엔"]
COMPANY_CORE = [
    # (업태, 종목, 영문 suffix, 회사명 suffix)
    ("제조업", "전자부품", "Electronics", "전자"), ("제조업", "자동차부품", "Auto Parts", "오토텍"),
    ("제조업", "화학제품", "Chemical", "케미칼"), ("제조업", "식료품", "Foods", "식품"),
    ("정보통신업", "응용소프트웨어 개발", "Soft", "소프트"), ("정보통신업", "시스템 통합", "Systems", "시스템즈"),
    ("도매 및 소매업", "무역", "Trading", "무역"), ("도매 및 소매업", "의류 도매", "Fashion", "패션"),
    ("건설업", "실내건축", "Construction", "건설"), ("서비스업", "광고대행", "Communications", "커뮤니케이션"),
    ("운수업", "화물운송", "Logistics", "로지스"), ("제조업", "의료기기", "Medical", "메디칼"),
    ("서비스업", "경영컨설팅", "Partners", "파트너스"), ("숙박 및 음식점업", "한식 음식점", "F&B", "에프앤비"),
]
SOLE_BIZ = [("음식점업", "한식", "식당"), ("소매업", "전자상거래", "몰"), ("서비스업", "미용", "헤어"),
            ("소매업", "편의점", "마트"), ("서비스업", "학원", "학원"), ("음식점업", "커피전문점", "커피"),
            ("서비스업", "인테리어", "디자인"), ("제조업", "제과", "베이커리"), ("서비스업", "세무대리", "세무회계"),
            ("도매업", "농산물", "상회")]
DEPARTMENTS = ["경영지원팀", "재무팀", "인사팀", "영업1팀", "영업2팀", "마케팅팀", "개발팀", "연구소", "품질관리팀",
               "생산관리팀", "구매팀", "해외영업팀", "IT운영팀", "기획팀", "법무팀", "고객지원팀"]
POSITIONS = [("사원", 0), ("주임", 2), ("대리", 4), ("과장", 7), ("차장", 11), ("부장", 15), ("이사", 20)]
JOBS = ["사무직", "영업직", "연구개발", "생산직", "관리직", "전문직", "기술직"]

FOREIGN = [
    ("Pacific Rim Trading Co., Ltd.", "1200 Harbor Blvd, Long Beach, CA 90802", "UNITED STATES", "BOFAUS3N", "Bank of America"),
    ("Tokyo Seimitsu Kogyo K.K.", "2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 163-0001", "JAPAN", "MHCBJPJT", "Mizuho Bank"),
    ("Shenzhen Huaxin Electronics Ltd.", "88 Keji Rd, Nanshan District, Shenzhen 518057", "CHINA", "BKCHCNBJ", "Bank of China"),
    ("Mekong Garment JSC", "45 Le Loi St, District 1, Ho Chi Minh City", "VIETNAM", "BFTVVNVX", "Vietcombank"),
    ("Rheinland Maschinenbau GmbH", "Königsallee 60, 40212 Düsseldorf", "GERMANY", "DEUTDEDD", "Deutsche Bank"),
    ("Lion City Supplies Pte. Ltd.", "1 Raffles Place, #20-01, Singapore 048616", "SINGAPORE", "DBSSSGSG", "DBS Bank"),
    ("Northbridge University", "300 College Ave, Boston, MA 02115", "UNITED STATES", "CHASUS33", "JPMorgan Chase"),
]


class World:
    """seed 하나로 결정론적으로 엔티티를 만들어내는 팩토리."""

    def __init__(self, seed: int):
        self.seed = seed
        self.rng = random.Random(seed)

    # -- 기본 엔티티 -------------------------------------------------------
    def address(self, kind: str = "apt", region=None) -> Address:
        r = self.rng
        sido, sigungu, zip2, dongs, roads = region or r.choice(K.REGIONS)
        dong = r.choice(dongs)
        bno = str(r.randint(1, 650)) + (f"-{r.randint(1, 40)}" if r.random() < 0.3 else "")
        jibun = f"{r.randint(1, 1500)}" + (f"-{r.randint(1, 60)}" if r.random() < 0.6 else "")
        if kind == "apt":
            bname = r.choice(K.APT_NAMES) + r.choice(K.APT_SUFFIX) + ("아파트" if r.random() < 0.5 else "")
            detail = f"{r.randint(101, 125)}동 {r.randint(1, 25)}{r.randint(1, 4):02d}호"
        elif kind == "villa":
            bname = r.choice(["", "", "그린빌", "하이츠", "빌라", "맨션"])
            detail = f"{r.randint(1, 5)}0{r.randint(1, 4)}호"
        else:  # office
            bname = r.choice(COMPANY_PREFIX) + r.choice(K.BUILDING_NAMES)
            detail = f"{r.randint(2, 20)}층" + (f" {r.randint(1, 20):02d}호" if r.random() < 0.5 else "")
        return Address(sido, sigungu, dong, r.choice(roads), bno, jibun, detail, bname,
                       f"{zip2}{r.randint(0, 999):03d}")

    def person(self, gender=None, birth_range=(1960, 2000), address=None, surname=None) -> Person:
        r = self.rng
        gender = gender or r.choice("MF")
        name, hanja, sur_en, given_en = K.make_name(r, gender)
        if surname:  # 자녀는 부의 성을 따른다
            k, h, e = surname
            old_k = name[:len(name) - 2]
            name, hanja, sur_en = k + name[len(old_k):], h + hanja[len(old_k):], e
        birth = rand_date(r, date(birth_range[0], 1, 1), date(birth_range[1], 12, 31))
        domain = r.choice(["naver.com", "gmail.com", "daum.net", "kakao.com", "hanmail.net", "nate.com"])
        email = f"{given_en.lower()}{r.randint(1, 999)}@{domain}"
        return Person(name, hanja, sur_en, given_en, gender, birth, K.rrn(r, birth, gender),
                      address or self.address(), K.mobile(r), email)

    def company(self, ceo: Person, corporate: bool = True) -> Company:
        r = self.rng
        addr = self.address("office")
        if corporate:
            biz_type, item, en_suffix, ko_suffix = r.choice(COMPANY_CORE)
            prefix = r.choice(COMPANY_PREFIX)
            name = f"주식회사 {prefix}{ko_suffix}" if r.random() < 0.5 else f"(주){prefix}{ko_suffix}"
            name_en = f"{prefix.upper() if prefix.isascii() else _roman_prefix(prefix)} {en_suffix} Co., Ltd."
            capital = r.choice([50, 100, 300, 500, 1000, 2000, 5000]) * 1_000_000
            employees = r.randint(8, 350)
            revenue = K.round_to(employees * r.uniform(1.5e8, 4e8), 1_000_000)
        else:
            biz_type, item, ko_suffix = r.choice(SOLE_BIZ)
            name = f"{r.choice(COMPANY_PREFIX)}{ko_suffix}"
            name_en = name
            capital = 0
            employees = r.randint(0, 8)
            revenue = K.round_to(r.uniform(4e7, 9e8), 100_000)
        # 설립일은 대표자가 만 25세가 된 이후로 한다
        earliest = max(date(2005, 1, 1), date(ceo.birth.year + 25, ceo.birth.month, 1))
        est = rand_date(r, earliest, max(earliest + timedelta(days=200), date(2023, 12, 31)))
        return Company(
            name=name, name_en=name_en, biz_no=K.biz_no(r, corporate),
            corp_no=K.corp_reg_no(r) if corporate else None, ceo=ceo, address=addr,
            phone=K.landline(r, addr.sido), fax=K.landline(r, addr.sido), biz_type=biz_type,
            biz_item=item, established=est, capital=capital, employees=employees, revenue=revenue,
            kind="법인" if corporate else "개인",
            email=f"{r.choice(['info', 'contact', 'admin', 'biz'])}@{_roman_prefix(name)[:8].lower()}.co.kr",
        )

    def account(self, holder: str, bank: str | None = None) -> BankAccount:
        r = self.rng
        bank = bank or r.choice(BANKS)
        fmt = BANK_ACCT_FMT.get(bank, "###-##-######")
        number = "".join(str(r.randint(0, 9)) if c == "#" else c for c in fmt)
        return BankAccount(bank, f"{r.choice(BRANCH_SUFFIX)}지점", number, holder,
                           rand_date(r, date(2010, 1, 1), date(2025, 6, 30)),
                           K.round_to(r.uniform(1e5, 8e7), 1))

    # -- 프로필 -------------------------------------------------------------
    def profile(self) -> Profile:
        r = self.rng
        issue = rand_date(r, date(2025, 1, 2), date(2026, 9, 30))
        home = self.address(r.choice(["apt", "apt", "villa"]))
        p = self.person(birth_range=(1965, 1998), address=home)
        married = p.age >= 30 and r.random() < 0.7
        spouse = self.person("F" if p.gender == "M" else "M",
                             (p.birth.year - 4, min(p.birth.year + 4, 2000)), home) if married else None
        father_sur = (p.name[:len(p.name) - 2], p.hanja[:len(p.name) - 2], p.surname_en)
        children = []
        if spouse:
            husband = p if p.gender == "M" else spouse
            sur = (husband.name[:len(husband.name) - 2], husband.hanja[:len(husband.name) - 2], husband.surname_en)
            for _ in range(r.choice([0, 1, 1, 2, 2, 3])):
                y0 = max(p.birth.year, spouse.birth.year) + 27
                if y0 <= 2024:
                    children.append(self.person(None, (y0, 2024), home, surname=sur))
        father = self.person("M", (p.birth.year - 35, p.birth.year - 25), surname=father_sur)
        mother = self.person("F", (p.birth.year - 33, p.birth.year - 23))

        # 주소 이력 (초본용) - 마지막이 현재 주소
        hist = []
        d = date(p.birth.year + 19, 3, 1)
        for _ in range(r.randint(1, 4)):
            hist.append((d, self.address(r.choice(["apt", "villa"]))))
            d = rand_date(r, d + timedelta(days=300), d + timedelta(days=2500))
        hist.append((min(d, issue - timedelta(days=60)), home))

        employer = self.company(self.person(birth_range=(1955, 1975)), corporate=True)
        years = max(1, min(p.age - 25, r.randint(1, 20)))
        pos = [x for x in POSITIONS if x[1] <= years][-1][0]
        salary = K.round_to(r.uniform(3200, 4500) * 1e4 * (1 + 0.045 * years), 100_000)
        emp = Employment(employer, r.choice(DEPARTMENTS), pos, r.choice(JOBS),
                         rand_date(r, date(issue.year - years, 1, 1), date(issue.year - years, 12, 31)),
                         salary, f"{r.choice('ABCDEHKS')}{r.randint(10000, 99999)}")

        business = self.company(p, corporate=False)
        corp = self.company(p, corporate=True)
        directors = [self.person(birth_range=(1960, 1990)) for _ in range(r.randint(2, 3))]
        total_shares = corp.capital // 5000
        ceo_share = int(total_shares * r.uniform(0.4, 0.8))
        rest = total_shares - ceo_share
        d1 = int(rest * r.uniform(0.3, 0.7))
        shareholders = [(p, ceo_share), (directors[0], d1), (directors[1], rest - d1)]

        prop_kind = r.choice(["아파트", "아파트", "아파트", "오피스텔", "다세대주택"])
        prop_addr = home if r.random() < 0.4 else self.address("apt" if prop_kind == "아파트" else "villa")
        excl = round(r.choice([59.98, 74.95, 84.97, 84.99, 101.84, 114.7, 134.6]) * (1 if prop_kind == "아파트" else r.uniform(0.4, 0.9)), 2)
        unit_price = r.uniform(0.5e7, 3.2e7) if prop_addr.sido == "서울특별시" else r.uniform(0.25e7, 1.2e7)
        price = K.round_to(excl * 1.3 * unit_price, 10_000_000)
        floors = r.randint(5, 35) if prop_kind != "다세대주택" else r.randint(3, 5)
        prop = Property(
            address=prop_addr, kind=prop_kind, land_area=round(excl * r.uniform(0.3, 0.7), 2),
            exclusive_area=excl, floor=r.randint(1, floors), total_floors=floors,
            structure=r.choice(["철근콘크리트구조", "철근콘크리트벽식구조", "철골철근콘크리트구조"]),
            completed=rand_date(r, date(1988, 1, 1), date(2022, 12, 31)), price=price,
            official_price=K.round_to(price * r.uniform(0.6, 0.75), 1_000_000),
            unique_no=f"{r.randint(1101, 2843)}-{r.randint(1990, 2023)}-{r.randint(1, 99999):06d}",
            seller=self.person(birth_range=(1950, 1985)),
            lease_deposit=K.round_to(price * r.uniform(0.5, 0.8), 5_000_000),
        )
        bank = r.choice(BANKS[:9])
        accounts = [self.account(p.name, bank)] + [self.account(p.name) for _ in range(r.randint(0, 2))]
        fname, faddr, fcountry, fswift, fbank = r.choice(FOREIGN)
        foreign = ForeignParty(
            fname, faddr, fcountry,
            r.choice(["John Miller", "Akira Tanaka", "Li Wei", "Nguyen Van An", "Klaus Weber", "Tan Wei Ming", "Sarah Johnson"]),
            f"{r.choice(['sales', 'accounts', 'admissions', 'export'])}@{fname.split()[0].lower()}.com",
            fbank, fswift, "".join(str(r.randint(0, 9)) for _ in range(r.choice([10, 12, 14]))),
        )
        return Profile(
            seed=self.seed, issue_date=issue, person=p, spouse=spouse, children=children, father=father,
            mother=mother, address_history=hist, employment=emp, business=business, corporation=corp,
            directors=directors, shareholders=shareholders, property=prop, accounts=accounts, bank=bank,
            bank_branch=f"{r.choice(BRANCH_SUFFIX)}지점", foreign=foreign,
        )


_ROMAN_PREFIX = {"한빛": "Hanbit", "대성": "Daesung", "미래": "Mirae", "세진": "Sejin", "동방": "Dongbang",
                 "태평양": "Pacific", "새한": "Saehan", "청솔": "Chungsol", "우진": "Woojin", "다온": "Daon",
                 "누리": "Nuri", "한결": "Hangyeol", "가온": "Gaon", "에이스": "Ace", "제일": "Jeil",
                 "삼정": "Samjung", "대한": "Daehan", "현대": "Hyundai", "하나로": "Hanaro", "신영": "Shinyoung",
                 "그린": "Green", "블루": "Blue", "스마트": "Smart", "넥스트": "Next", "코리아": "Korea",
                 "글로벌": "Global", "유니온": "Union", "아이엠": "IM", "케이": "K", "디엔": "DN"}


def _roman_prefix(name: str) -> str:
    for k, v in _ROMAN_PREFIX.items():
        if k in name:
            return v
    return "company"


def make_profile(seed: int) -> Profile:
    return World(seed).profile()
