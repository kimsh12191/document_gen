"""합성 고객 프로필.

하나의 Profile 안의 사람/회사/부동산/계좌 정보는 서로 일관되게 생성되므로,
같은 프로필로 여러 서류를 만들면 '한 고객이 제출한 서류 묶음'이 된다.
make_profile(seed) 가 seed 하나로 결정론적으로 만들고, 서류 생성 함수(docgen/docs/*.py)가 받아 쓴다.
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
                 "카카오뱅크": "3333-##-#######", "토스뱅크": "1000-####-####", "케이뱅크": "100-###-######",
                 "외환은행": "###-######-###", "KEB하나은행": "###-######-#####"}
BRANCH_SUFFIX = ["역삼", "삼성역", "여의도", "광화문", "명동", "판교", "서초", "잠실", "해운대", "센텀",
                 "수원", "분당", "일산", "송도", "둔산", "상무", "청주", "창원", "범어", "을지로"]

COMPANY_PREFIX = ["한빛", "대성", "미래", "세진", "동방", "태평양", "새한", "청솔", "우진", "다온", "누리",
                  "한결", "가온", "에이스", "제일", "삼정", "대한", "현대", "하나로", "신영", "그린",
                  "블루", "스마트", "넥스트", "코리아", "글로벌", "유니온", "아이엠", "케이", "디엔",
                  "동양", "삼보", "일신", "대원", "세원", "성광", "영진", "태양", "한성", "금강", "백두", "한라", "서해", "동해",
                  "남산", "한울", "솔빛", "나래", "보람", "아라", "하늘", "새벽", "참", "바른", "온누리", "이레", "예림",
                  "진성", "효성", "광명", "청우", "덕산", "삼원", "중앙", "동신", "대영", "선진", "우성", "신화", "명성",
                  "에코", "퓨처", "알파", "오메가", "노바", "비전", "엘림", "제이", "에스", "티엔", "지엠", "와이즈",
                  "인터", "메가", "프라임", "베스트", "골든", "실버", "웰", "탑", "하이", "뉴"]
COMPANY_CORE = [
    # (업태, 종목, 영문 suffix, 회사명 suffix)
    ("제조업", "전자부품", "Electronics", "전자"), ("제조업", "자동차부품", "Auto Parts", "오토텍"),
    ("제조업", "화학제품", "Chemical", "케미칼"), ("제조업", "식료품", "Foods", "식품"),
    ("정보통신업", "응용소프트웨어 개발", "Soft", "소프트"), ("정보통신업", "시스템 통합", "Systems", "시스템즈"),
    ("도매 및 소매업", "무역", "Trading", "무역"), ("도매 및 소매업", "의류 도매", "Fashion", "패션"),
    ("건설업", "실내건축", "Construction", "건설"), ("서비스업", "광고대행", "Communications", "커뮤니케이션"),
    ("운수업", "화물운송", "Logistics", "로지스"), ("제조업", "의료기기", "Medical", "메디칼"),
    ("서비스업", "경영컨설팅", "Partners", "파트너스"), ("숙박 및 음식점업", "한식 음식점", "F&B", "에프앤비"),
    ("제조업", "금속가공제품", "Metal", "금속"), ("제조업", "플라스틱제품", "Plastics", "플라텍"),
    ("제조업", "산업용 기계", "Machinery", "기계"), ("제조업", "반도체 장비", "Semitech", "세미텍"),
    ("제조업", "화장품", "Cosmetics", "코스메틱"), ("제조업", "의약품", "Pharm", "제약"),
    ("제조업", "가구", "Furniture", "가구"), ("제조업", "섬유제품", "Textile", "섬유"),
    ("정보통신업", "데이터베이스 및 온라인정보", "Data", "데이터"), ("정보통신업", "게임 소프트웨어", "Games", "게임즈"),
    ("도매 및 소매업", "식자재 유통", "Distribution", "유통"), ("도매 및 소매업", "전자상거래", "Commerce", "커머스"),
    ("건설업", "토목공사", "E&C", "이앤씨"), ("부동산업", "부동산 임대", "Development", "개발"),
    ("전문 과학 및 기술 서비스업", "엔지니어링", "Engineering", "엔지니어링"), ("교육 서비스업", "교육 컨텐츠", "Edu", "에듀"),
    ("운수 및 창고업", "물류창고", "Logis", "물류"), ("에너지업", "태양광 발전", "Energy", "에너지"),
]
SOLE_BIZ = [("음식점업", "한식", "식당"), ("소매업", "전자상거래", "몰"), ("서비스업", "미용", "헤어"),
            ("소매업", "편의점", "마트"), ("서비스업", "학원", "학원"), ("음식점업", "커피전문점", "커피"),
            ("서비스업", "인테리어", "디자인"), ("제조업", "제과", "베이커리"), ("서비스업", "세무대리", "세무회계"),
            ("도매업", "농산물", "상회")]
# 직업 → 그 직업이 일하는 부서 (직업·부서를 따로 뽑으면 '법무팀 생산직' 같은 조합이 나온다), 가중치
JOB_DEPTS = {
    "사무직": (["경영지원팀", "재무팀", "회계팀", "인사팀", "총무팀", "구매팀", "기획팀"], 22),
    "영업직": (["영업1팀", "영업2팀", "국내영업팀", "해외영업팀", "영업기획팀", "B2B영업팀"], 14),
    "연구개발": (["연구소", "개발팀", "선행개발팀", "제품개발팀", "소프트웨어개발팀"], 10),
    "생산직": (["생산1팀", "생산2팀", "생산관리팀", "제조팀", "설비보전팀"], 10),
    "기술직": (["기술지원팀", "설비팀", "시공팀", "엔지니어링팀"], 8),
    "관리직": (["경영기획팀", "전략기획팀", "관리부", "운영팀"], 7),
    "전문직": (["법무팀", "세무팀", "감사팀", "재무팀"], 5),
    "IT직": (["IT운영팀", "정보보안팀", "데이터팀", "플랫폼개발팀"], 8),
    "마케팅": (["마케팅팀", "브랜드팀", "홍보팀", "디지털마케팅팀"], 6),
    "서비스직": (["고객지원팀", "CS팀", "매장운영팀"], 6),
    "물류직": (["물류팀", "배송관리팀", "SCM팀"], 4),
    "품질관리": (["품질관리팀", "품질보증팀", "QA팀"], 4),
}
DEPARTMENTS = sorted({d for ds, _ in JOB_DEPTS.values() for d in ds} | {"고객지원팀", "법무팀"})
POSITIONS = [("사원", 0), ("주임", 2), ("대리", 4), ("과장", 7), ("차장", 11), ("부장", 15), ("이사", 20)]
JOBS = list(JOB_DEPTS)

FOREIGN = [   # 예전 고정 7곳 (유학 학교는 docgen/docs/fx.py 의 학교 목록과 이름이 같아야 한다)
    ("Northbridge University", "300 College Ave, Boston, MA 02115", "UNITED STATES", "CHASUS33", "JPMorgan Chase"),
]
# 해외 거래 상대: 나라별로 이름·주소·은행·담당자를 맞춰 조합한다 (예전: 7곳 고정, 담당자 나라 불일치)
# 나라: (가중치, 회사 앞말, 회사 업종말, 법인 꼴, 거리, 도시·우편, 은행 [(이름, SWIFT)], 담당자 이름, 성)
FOREIGN_COUNTRIES = {
    "UNITED STATES": (20, ["Pacific", "Summit", "Liberty", "Atlas", "Evergreen", "Northstar", "Bluewater", "Granite", "Pioneer", "Redwood"],
                      ["Trading", "Industries", "Supply", "Components", "Technologies", "Foods", "Medical", "Materials"],
                      ["{} Co., Ltd.", "{} Inc.", "{} LLC", "{} Corporation"],
                      ["Harbor Blvd", "Main St", "Market St", "Commerce Dr", "Industrial Pkwy", "Oak Ave", "Broadway"],
                      ["Long Beach, CA 90802", "Los Angeles, CA 90021", "Seattle, WA 98104", "Houston, TX 77002", "Chicago, IL 60607",
                       "Newark, NJ 07102", "San Jose, CA 95113", "Atlanta, GA 30303"],
                      [("Bank of America, N.A.", "BOFAUS3N"), ("JPMorgan Chase Bank, N.A.", "CHASUS33"), ("Wells Fargo Bank, N.A.", "WFBIUS6S"),
                       ("Citibank, N.A.", "CITIUS33")],
                      ["John", "Sarah", "Michael", "Emily", "David", "Jessica", "Robert", "Ashley"],
                      ["Miller", "Johnson", "Brown", "Davis", "Wilson", "Taylor", "Anderson", "Clark"]),
    "JAPAN": (18, ["Tokyo", "Osaka", "Nagoya", "Yamato", "Fuji", "Sakura", "Asahi", "Kansai", "Nippon", "Chubu"],
              ["Seimitsu", "Denki", "Shoji", "Kogyo", "Kasei", "Buhin", "Trading", "Fine Parts"],
              ["{} Co., Ltd.", "{} K.K.", "{} Corporation"],
              ["Nishi-Shinjuku", "Marunouchi", "Umeda", "Nihonbashi", "Sakae", "Shiba", "Kitahama"],
              ["Shinjuku-ku, Tokyo 163-0001", "Chiyoda-ku, Tokyo 100-0005", "Kita-ku, Osaka 530-0001", "Naka-ku, Nagoya 460-0008",
               "Minato-ku, Tokyo 105-0014", "Chuo-ku, Osaka 541-0041"],
              [("Mizuho Bank, Ltd.", "MHCBJPJT"), ("MUFG Bank, Ltd.", "BOTKJPJT"), ("Sumitomo Mitsui Banking Corporation", "SMBCJPJT")],
              ["Akira", "Kenji", "Yuko", "Hiroshi", "Naoko", "Takeshi", "Mai", "Daisuke"],
              ["Tanaka", "Sato", "Nakamura", "Suzuki", "Watanabe", "Ito", "Yamamoto", "Kobayashi"]),
    "CHINA": (22, ["Shenzhen", "Shanghai", "Ningbo", "Qingdao", "Guangzhou", "Suzhou", "Xiamen", "Tianjin", "Dongguan", "Hangzhou"],
              ["Huaxin Electronics", "Hengtai Trading", "Jinlong Chemical", "Tianli Machinery", "Xinhua Textile", "Dongfang Import & Export",
               "Hongda Auto Parts", "Ruifeng Medical"],
              ["{} Co., Ltd.", "{} Ltd."],
              ["Keji Rd", "Century Ave", "Zhongshan Rd", "Jiefang Rd", "Renmin Rd", "Binhai Ave"],
              ["Nanshan District, Shenzhen 518057", "Pudong New Area, Shanghai 200120", "Yinzhou District, Ningbo 315100",
               "Shinan District, Qingdao 266071", "Tianhe District, Guangzhou 510620", "Suzhou Industrial Park, Suzhou 215021"],
              [("Bank of China", "BKCHCNBJ"), ("Industrial and Commercial Bank of China", "ICBKCNBJ"),
               ("China Construction Bank", "PCBCCNBJ"), ("Agricultural Bank of China", "ABOCCNBJ")],
              ["Wei", "Jie", "Fang", "Lei", "Na", "Hao", "Min", "Yan"], ["Li", "Chen", "Wang", "Zhang", "Liu", "Yang", "Zhao", "Huang"]),
    "VIETNAM": (12, ["Mekong", "Saigon", "Hanoi", "Hai Phong", "Dong Nai", "Binh Duong", "Viet", "Sao Mai"],
                ["Garment", "Textile Export", "Seafood", "Furniture", "Electronics", "Food Processing", "Coffee", "Footwear"],
                ["{} JSC", "{} Co., Ltd.", "{} Joint Stock Company"],
                ["Le Loi St", "Nguyen Hue Blvd", "Tran Hung Dao St", "Hai Ba Trung St", "Vo Van Kiet St"],
                ["District 1, Ho Chi Minh City", "Thu Duc City, Ho Chi Minh City", "Hoan Kiem District, Hanoi",
                 "Ngo Quyen District, Hai Phong", "Bien Hoa City, Dong Nai"],
                [("Joint Stock Commercial Bank for Foreign Trade of Vietnam", "BFTVVNVX"), ("Vietinbank", "ICBVVNVX"),
                 ("BIDV", "BIDVVNVX")],
                ["Van An", "Thi Mai", "Minh Tuan", "Thu Ha", "Quoc Bao", "Thi Lan"], ["Nguyen", "Tran", "Le", "Pham", "Hoang", "Vo"]),
    "GERMANY": (8, ["Rheinland", "Bayern", "Nord", "Hansa", "Schwarzwald", "Elbe", "Main", "Alpen"],
                ["Maschinenbau", "Technik", "Chemie", "Medizintechnik", "Automotive", "Handels"],
                ["{} GmbH", "{} AG", "{} GmbH & Co. KG"],
                ["Königsallee", "Hauptstraße", "Industriestraße", "Bahnhofstraße", "Friedrichstraße"],
                ["40212 Düsseldorf", "80331 München", "20095 Hamburg", "70173 Stuttgart", "60311 Frankfurt am Main"],
                [("Deutsche Bank AG", "DEUTDEDD"), ("Commerzbank AG", "COBADEFF"), ("DZ Bank AG", "GENODEFF")],
                ["Klaus", "Anna", "Thomas", "Julia", "Stefan", "Laura"], ["Weber", "Schmidt", "Müller", "Fischer", "Wagner", "Becker"]),
    "SINGAPORE": (8, ["Lion City", "Marina", "Raffles", "Orchard", "Straits", "Temasek"],
                  ["Supplies", "Trading", "Logistics", "Resources", "Electronics", "Chemicals"],
                  ["{} Pte. Ltd."],
                  ["Raffles Place", "Robinson Road", "Cecil Street", "Shenton Way", "Anson Road"],
                  ["Singapore 048616", "Singapore 068898", "Singapore 049712", "Singapore 079903"],
                  [("DBS Bank Ltd.", "DBSSSGSG"), ("Oversea-Chinese Banking Corporation", "OCBCSGSG"), ("United Overseas Bank", "UOVBSGSG")],
                  ["Wei Ming", "Mei Ling", "Jun Jie", "Hui Min"], ["Tan", "Lim", "Lee", "Ng", "Ong"]),
    "HONG KONG": (4, ["Golden Crown", "Pacific Rim", "Harbour", "Kowloon", "Victoria"], ["International", "Trading", "Holdings", "Sourcing"],
                  ["{} Ltd.", "{} Limited"], ["Queensway", "Connaught Road Central", "Nathan Road", "Des Voeux Road"],
                  ["Admiralty, Hong Kong", "Central, Hong Kong", "Tsim Sha Tsui, Kowloon"],
                  [("The Hongkong and Shanghai Banking Corporation Ltd.", "HSBCHKHH"), ("Bank of China (Hong Kong) Limited", "BKCHHKHH")],
                  ["Ka Wai", "Siu Ming", "Wing Yan", "Chi Keung"], ["Chan", "Wong", "Leung", "Cheung", "Lau"]),
    "THAILAND": (3, ["Siam", "Bangkok", "Chao Phraya", "Krung", "Thai"], ["Rubber", "Food Industries", "Auto Parts", "Packaging"],
                 ["{} Co., Ltd.", "{} Public Company Limited"], ["Sukhumvit Rd", "Silom Rd", "Rama IV Rd"],
                 ["Khlong Toei, Bangkok 10110", "Bang Rak, Bangkok 10500", "Pathum Wan, Bangkok 10330"],
                 [("Bangkok Bank", "BKKBTHBK"), ("Kasikornbank", "KASITHBK"), ("Siam Commercial Bank", "SICOTHBK")],
                 ["Somchai", "Suda", "Anan", "Nok"], ["Srisuk", "Chaiyaporn", "Wongsakul", "Rattanakul"]),
    "INDIA": (3, ["Bharat", "Mumbai", "Deccan", "Ganga", "Lotus"], ["Pharma", "Textiles", "Steel", "Software", "Exports"],
              ["{} Pvt. Ltd.", "{} Limited"], ["MG Road", "Nariman Point", "Anna Salai"],
              ["Mumbai 400021", "Bengaluru 560001", "Chennai 600002"],
              [("State Bank of India", "SBININBB"), ("HDFC Bank", "HDFCINBB"), ("ICICI Bank", "ICICINBB")],
              ["Rahul", "Priya", "Amit", "Anjali"], ["Sharma", "Patel", "Gupta", "Iyer"]),
    "UNITED KINGDOM": (2, ["Thames", "Albion", "Crown", "Windsor"], ["Trading", "Engineering", "Imports"], ["{} Ltd.", "{} PLC"],
                       ["King Street", "High Street", "Victoria Road"], ["London EC2V 6DN", "Manchester M2 4WU", "Birmingham B3 2BJ"],
                       [("Barclays Bank PLC", "BARCGB22"), ("HSBC UK Bank plc", "HBUKGB4B"), ("Lloyds Bank plc", "LOYDGB2L")],
                       ["James", "Oliver", "Emma", "Charlotte"], ["Smith", "Jones", "Evans", "Thomas"]),
}


# 개인 이메일: 실제 점유율에 가깝게 (네이버가 절반 가까이), 아이디 꼴도 여러 가지
EMAIL_DOMAINS = {"naver.com": 45, "gmail.com": 25, "daum.net": 8, "hanmail.net": 8, "kakao.com": 6, "nate.com": 5,
                 "hotmail.com": 1, "icloud.com": 1, "outlook.com": 1}


def _email(r: random.Random, sur_en: str, given_en: str, birth: date) -> str:
    g, s = given_en.lower(), sur_en.lower()
    local = r.choice([f"{g}{r.randint(1, 999)}", f"{s}{g}", f"{s}.{g}", f"{g[0]}{s}{birth.strftime('%y')}",
                      f"{s}{g}{birth.strftime('%m%d')}", f"{g}_{s}", f"{s}{g[:1]}{r.randint(10, 99)}",
                      f"{g}{birth.year}", f"{r.choice(['happy', 'sky', 'blue', 'star', 'sun', 'moon', 'dream'])}{g}{r.randint(1, 99)}"])
    return f"{local}@{r.choices(list(EMAIL_DOMAINS), weights=list(EMAIL_DOMAINS.values()))[0]}"


class World:
    """seed 하나로 결정론적으로 엔티티를 만들어내는 팩토리."""

    def __init__(self, seed: int):
        self.seed = seed
        self.rng = random.Random(seed)

    # -- 기본 엔티티 -------------------------------------------------------
    def address(self, kind: str = "apt", region=None) -> Address:
        r = self.rng
        sido, sigungu, zip_head, dongs, roads = region or r.choices(K.REGIONS, weights=K.REGION_WEIGHTS)[0]   # 인구 비율
        road = r.choice(roads)
        dong = K.ROAD_DONG.get((sido, sigungu, road)) or r.choice(dongs)   # 그 길이 지나는 동
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
        tail = 5 - len(zip_head)
        return Address(sido, sigungu, dong, road, bno, jibun, detail, bname,
                       f"{zip_head}{r.randint(0, 10 ** tail - 1):0{tail}d}")

    def person(self, gender=None, birth_range=(1960, 2000), address=None, surname=None) -> Person:
        r = self.rng
        gender = gender or r.choice("MF")
        birth = rand_date(r, date(birth_range[0], 1, 1), date(birth_range[1], 12, 31))
        name, hanja, sur_en, given_en = K.make_name(r, gender, birth.year)   # 반은 그 연대에 흔한 이름
        if surname:  # 자녀는 부의 성을 따른다
            k, h, e = surname
            old_k = name[:len(name) - 2]
            name, hanja, sur_en = k + name[len(old_k):], h + hanja[len(old_k):], e
        email = _email(r, sur_en, given_en, birth)
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
    def profile(self, bank: str | None = None) -> Profile:
        r = self.rng
        _bank_override = bank
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
        job = r.choices(JOBS, weights=[w for _, w in JOB_DEPTS.values()])[0]
        emp = Employment(employer, r.choice(JOB_DEPTS[job][0]), pos, job,
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
        bank = _bank_override or bank
        accounts = [self.account(p.name, bank)] + [self.account(p.name) for _ in range(r.randint(0, 2))]
        foreign = _foreign_party(r)
        return Profile(
            seed=self.seed, issue_date=issue, person=p, spouse=spouse, children=children, father=father,
            mother=mother, address_history=hist, employment=emp, business=business, corporation=corp,
            directors=directors, shareholders=shareholders, property=prop, accounts=accounts, bank=bank,
            bank_branch=f"{r.choice(BRANCH_SUFFIX)}지점", foreign=foreign,
        )


def _foreign_party(r: random.Random) -> ForeignParty:
    acct = "".join(str(r.randint(0, 9)) for _ in range(r.choice([10, 12, 14])))
    if r.random() < 0.1:   # 유학 학교
        fname, faddr, fcountry, fswift, fbank = FOREIGN[0]
        return ForeignParty(fname, faddr, fcountry, r.choice(["Sarah Johnson", "Michael Brown"]), "admissions@northbridge.edu",
                            fbank, fswift, acct)
    names = list(FOREIGN_COUNTRIES)
    country = r.choices(names, weights=[FOREIGN_COUNTRIES[c][0] for c in names])[0]
    _, pre, core, legal, streets, cities, banks, firsts, lasts = FOREIGN_COUNTRIES[country]
    name = r.choice(legal).format(f"{r.choice(pre)} {r.choice(core)}")
    addr = f"{r.randint(1, 2400)} {r.choice(streets)}, {r.choice(cities)}"
    bank, swift = r.choice(banks)
    contact = f"{r.choice(lasts)} {r.choice(firsts)}" if country in ("CHINA", "VIETNAM", "HONG KONG") else f"{r.choice(firsts)} {r.choice(lasts)}"
    domain = "".join(c for c in name.split()[0].lower() if c.isascii() and c.isalpha()) or "trade"
    tld = {"JAPAN": "co.jp", "CHINA": "com.cn", "VIETNAM": "com.vn", "GERMANY": "de", "SINGAPORE": "com.sg", "HONG KONG": "com.hk",
           "THAILAND": "co.th", "INDIA": "co.in", "UNITED KINGDOM": "co.uk"}.get(country, "com")
    email = f"{r.choice(['sales', 'accounts', 'export', 'info', 'trade', contact.split()[0].lower()])}@{domain}.{tld}"
    return ForeignParty(name, addr, country, contact, email, bank, swift, acct)


_ROMAN_PREFIX = {"한빛": "Hanbit", "대성": "Daesung", "미래": "Mirae", "세진": "Sejin", "동방": "Dongbang",
                 "태평양": "Pacific", "새한": "Saehan", "청솔": "Chungsol", "우진": "Woojin", "다온": "Daon",
                 "누리": "Nuri", "한결": "Hangyeol", "가온": "Gaon", "에이스": "Ace", "제일": "Jeil",
                 "삼정": "Samjung", "대한": "Daehan", "현대": "Hyundai", "하나로": "Hanaro", "신영": "Shinyoung",
                 "그린": "Green", "블루": "Blue", "스마트": "Smart", "넥스트": "Next", "코리아": "Korea",
                 "글로벌": "Global", "유니온": "Union", "아이엠": "IM", "케이": "K", "디엔": "DN",
                 "동양": "Dongyang", "삼보": "Sambo", "일신": "Ilshin", "대원": "Daewon", "세원": "Sewon", "성광": "Sungkwang",
                 "영진": "Youngjin", "태양": "Taeyang", "한성": "Hansung", "금강": "Kumkang", "백두": "Baekdu", "한라": "Halla",
                 "서해": "Seohae", "동해": "Donghae", "남산": "Namsan", "한울": "Hanul", "솔빛": "Solbit", "나래": "Narae",
                 "보람": "Boram", "아라": "Ara", "하늘": "Haneul", "새벽": "Saebyeok", "참": "Cham", "바른": "Bareun",
                 "온누리": "Onnuri", "이레": "Ire", "예림": "Yerim", "진성": "Jinsung", "효성": "Hyosung", "광명": "Kwangmyung",
                 "청우": "Chungwoo", "덕산": "Deoksan", "삼원": "Samwon", "중앙": "Joongang", "동신": "Dongshin",
                 "대영": "Daeyoung", "선진": "Sunjin", "우성": "Woosung", "신화": "Shinhwa", "명성": "Myungsung",
                 "에코": "Eco", "퓨처": "Future", "알파": "Alpha", "오메가": "Omega", "노바": "Nova", "비전": "Vision",
                 "엘림": "Elim", "제이": "J", "에스": "S", "티엔": "TN", "지엠": "GM", "와이즈": "Wise", "인터": "Inter",
                 "메가": "Mega", "프라임": "Prime", "베스트": "Best", "골든": "Golden", "실버": "Silver", "웰": "Well",
                 "탑": "Top", "하이": "Hi", "뉴": "New"}


def _roman_prefix(name: str) -> str:
    for k, v in _ROMAN_PREFIX.items():
        if k in name:
            return v
    return "company"


def make_profile(seed: int, bank: str | None = None) -> Profile:
    """bank: 주거래은행 고정 (None 이면 랜덤)."""
    return World(seed).profile(bank)
