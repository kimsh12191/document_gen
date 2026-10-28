"""alien_registration_card: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/identity.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.registry import doc


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
    if special(rng, "long_name", 0.1):  # 이름이 길어 두 줄로 넘어가는 경우
        extra = {"PHILIPPINES": ["DELA CRUZ", "DE LOS SANTOS"], "INDIA": ["KUMAR", "RAJ"], "VIETNAM": ["THANH", "NGOC"]}
        given = f"{given} {rng.choice(extra.get(country, ['ALEXANDER', 'ELIZABETH', 'MARIE']))} {rng.choice(males + females)}"
    visa, visa_name, _w = rng.choices(_VISAS, [v[2] for v in _VISAS])[0]
    if special(rng, "permanent_resident", 0.06):  # 영주(F-5) 자격자: 영주증
        visa, visa_name = "F-5", "영주"
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
