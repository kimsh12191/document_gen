"""한국 서류에 쓰이는 값들의 포맷/생성 헬퍼.

모든 값은 학습용 합성 데이터이며 실존 인물·사업자와 무관하다.
"""
from __future__ import annotations

import random
from datetime import date

# ---------------------------------------------------------------------------
# 이름 (한글/한자/로마자)
# ---------------------------------------------------------------------------

# (한글, 한자, 여권 로마자, 가중치 = 인구 비율 %, 통계청 인구주택총조사 2015 에 가깝게)
SURNAMES = [
    ("김", "金", "KIM", 21.5), ("이", "李", "LEE", 14.7), ("박", "朴", "PARK", 8.4),
    ("최", "崔", "CHOI", 4.7), ("정", "鄭", "JUNG", 4.3), ("강", "姜", "KANG", 2.4),
    ("조", "趙", "CHO", 2.1), ("윤", "尹", "YOON", 2.1), ("장", "張", "JANG", 2.0),
    ("임", "林", "LIM", 1.7), ("한", "韓", "HAN", 1.5), ("오", "吳", "OH", 1.5),
    ("서", "徐", "SEO", 1.4), ("신", "申", "SHIN", 1.4), ("권", "權", "KWON", 1.4),
    ("황", "黃", "HWANG", 1.4), ("안", "安", "AHN", 1.3), ("송", "宋", "SONG", 1.3),
    ("류", "柳", "RYU", 1.2), ("전", "全", "JEON", 1.1), ("홍", "洪", "HONG", 1.1),
    ("고", "高", "KO", 0.9), ("문", "文", "MOON", 0.9), ("양", "梁", "YANG", 0.9),
    ("손", "孫", "SON", 0.9), ("배", "裵", "BAE", 0.8), ("백", "白", "BAEK", 0.8),
    ("허", "許", "HEO", 0.7), ("남", "南", "NAM", 0.6), ("심", "沈", "SIM", 0.5),
    ("노", "盧", "NOH", 0.6), ("하", "河", "HA", 0.5), ("곽", "郭", "KWAK", 0.4),
    ("성", "成", "SUNG", 0.4), ("차", "車", "CHA", 0.4), ("주", "朱", "JOO", 0.4),
    ("우", "禹", "WOO", 0.4), ("구", "具", "KOO", 0.4), ("민", "閔", "MIN", 0.3),
    ("진", "陳", "JIN", 0.3), ("나", "羅", "NA", 0.3), ("지", "池", "JI", 0.3),
    ("엄", "嚴", "EOM", 0.3), ("채", "蔡", "CHAE", 0.3), ("원", "元", "WON", 0.3),
    ("천", "千", "CHUN", 0.2), ("방", "方", "BANG", 0.2), ("공", "孔", "KONG", 0.2),
    ("현", "玄", "HYUN", 0.2), ("함", "咸", "HAM", 0.2), ("변", "卞", "BYUN", 0.3),
    ("염", "廉", "YEOM", 0.1), ("여", "呂", "YEO", 0.1), ("추", "秋", "CHU", 0.1),
    ("도", "都", "DO", 0.1), ("석", "石", "SEOK", 0.1), ("선", "宣", "SUN", 0.1),
    ("설", "薛", "SEOL", 0.1), ("마", "馬", "MA", 0.1), ("길", "吉", "KIL", 0.1),
    ("연", "延", "YEON", 0.1), ("위", "魏", "WI", 0.06), ("표", "表", "PYO", 0.05),
    ("명", "明", "MYUNG", 0.05), ("기", "奇", "KI", 0.05), ("반", "潘", "BAN", 0.05),
    ("왕", "王", "WANG", 0.05), ("금", "琴", "KEUM", 0.05), ("옥", "玉", "OK", 0.05),
    ("남궁", "南宮", "NAMGOONG", 0.04), ("황보", "皇甫", "HWANGBO", 0.03),
    ("제갈", "諸葛", "JEGAL", 0.02), ("선우", "鮮于", "SUNWOO", 0.01),
]

# 이름 음절 → 한자 후보
GIVEN_SYLLABLES = {
    "민": "敏民旻珉", "서": "瑞書序舒", "지": "智志知芝", "현": "賢炫玄鉉",
    "준": "俊峻埈準", "영": "英榮映泳", "수": "秀洙守壽", "호": "浩昊鎬虎",
    "우": "宇佑祐雨", "진": "眞珍鎭振", "연": "延娟妍姸", "은": "恩銀垠殷",
    "아": "雅娥兒亞", "윤": "允潤胤玧", "하": "夏河賀昰", "도": "道度到桃",
    "재": "在載宰材", "성": "成誠星聖", "혜": "惠慧蕙譓", "정": "正貞廷晶",
    "경": "京慶景敬", "원": "元媛源圓", "태": "泰太兌台", "희": "熙喜姬希",
    "주": "周柱珠宙", "유": "有裕侑柔", "승": "承昇勝丞", "예": "藝睿禮叡",
    "동": "東棟童", "상": "相尙祥", "석": "錫碩石", "용": "龍容勇",
    "철": "哲喆鐵", "훈": "勳薰訓", "혁": "赫爀", "나": "娜那奈",
    "소": "素昭韶", "채": "彩采埰", "다": "多茶", "건": "建健乾",
    "규": "圭奎揆", "기": "基起琪", "미": "美媄", "선": "善宣璇",
    "숙": "淑", "순": "順淳", "옥": "玉", "자": "子慈", "환": "煥桓",
    "형": "炯亨衡", "욱": "旭昱郁", "빈": "彬斌", "린": "麟璘",
    "율": "律栗", "시": "時是", "인": "仁寅", "찬": "燦讚",
}

GIVEN_ROMAN = {
    "민": "MIN", "서": "SEO", "지": "JI", "현": "HYUN", "준": "JUN", "영": "YOUNG",
    "수": "SU", "호": "HO", "우": "WOO", "진": "JIN", "연": "YEON", "은": "EUN",
    "아": "A", "윤": "YUN", "하": "HA", "도": "DO", "재": "JAE", "성": "SEONG",
    "혜": "HYE", "정": "JEONG", "경": "KYUNG", "원": "WON", "태": "TAE", "희": "HEE",
    "주": "JU", "유": "YU", "승": "SEUNG", "예": "YE", "동": "DONG", "상": "SANG",
    "석": "SEOK", "용": "YONG", "철": "CHUL", "훈": "HOON", "혁": "HYUK", "나": "NA",
    "소": "SO", "채": "CHAE", "다": "DA", "건": "GEON", "규": "GYU", "기": "GI",
    "미": "MI", "선": "SUN", "숙": "SOOK", "순": "SOON", "옥": "OK", "자": "JA",
    "환": "HWAN", "형": "HYUNG", "욱": "WOOK", "빈": "BIN", "린": "RIN",
    "율": "YUL", "시": "SI", "인": "IN", "찬": "CHAN",
}

GIVEN_SYLLABLES.update({"식": "植湜", "병": "炳秉", "종": "鍾宗", "광": "光廣", "명": "明命", "란": "蘭", "안": "安晏",
                        "이": "利伊", "섭": "燮", "봉": "鳳", "범": "範", "람": "嵐", "솔": "率", "온": "溫", "결": "潔", "가": "佳嘉", "보": "寶甫", "춘": "春"})
GIVEN_ROMAN.update({"식": "SIK", "병": "BYUNG", "종": "JONG", "광": "KWANG", "명": "MYUNG", "란": "RAN", "안": "AN",
                    "이": "I", "섭": "SEOP", "봉": "BONG", "범": "BEOM", "람": "RAM", "솔": "SOL", "온": "ON", "결": "GYEOL", "가": "GA", "보": "BO", "춘": "CHUN"})

MALE_FIRST = list("민준현우진도재성태승동상석용철훈혁건규기환형욱찬호영수종병광정시지서예주유선연")
FEMALE_FIRST = list("서지민수연은아윤하혜정경원희주유예나소채다미선숙순옥영명현가")
MALE_SECOND = list("준현우진호영수민석훈혁환성재도원철규기찬율승태빈섭범종식")
FEMALE_SECOND = list("은아윤하희연지서혜정경원주유예린미영수빈진나선숙인란솔온")
# 출생 연대별 흔한 이름 (반은 여기서, 반은 음절 조합으로): 1960년대 영숙·영수 … 2010년대 서아·하준
POPULAR = {
    1960: ("영수 영호 영식 정수 성수 영철 경수 상철 성호 종수 병철 재호 동수 진호 광수 용수 정호 명수",
           "영숙 정숙 순자 영희 명숙 경숙 미숙 영자 정희 순옥 현숙 혜숙 은숙 경희 미경 옥순 춘자 정자"),
    1970: ("성호 영수 성훈 상훈 정훈 성민 동훈 준호 재훈 성진 지훈 상현 정호 민수 현석 영진 종훈 진우",
           "미영 은영 미경 은정 현정 미정 정미 수진 지영 혜영 선영 은주 미란 경미 현주 미숙 은희 수정"),
    1980: ("지훈 성민 현우 준호 민수 동현 성현 정훈 상우 재현 진우 민석 현준 승현 준영 영민 태현 지원",
           "지영 수진 지은 혜진 은지 미진 수연 지현 정은 유진 민정 은정 현정 소영 지혜 선영 보미 다영"),
    1990: ("민준 지훈 현우 준호 동현 성민 승현 민재 도현 준혁 승민 지환 상민 우진 태현 건우 민호 재원",
           "지은 수빈 유진 지현 민지 수진 예진 은지 혜원 다은 서연 지원 하은 지수 예린 소연 가영 다혜"),
    2000: ("민준 서준 현우 지훈 도윤 준서 건우 우진 지호 예준 승우 민성 시우 주원 유준 동건 지환 준혁",
           "서연 민서 지민 서현 수빈 지원 예은 하은 윤서 채원 지유 다인 예린 수아 지아 가은 서영 유나"),
    2010: ("서준 도윤 하준 시우 은우 이준 지호 예준 주원 유준 도현 건우 선우 우진 연우 이안 준우 시윤",
           "서아 하윤 지안 서윤 하은 아윤 지우 수아 이서 윤서 지유 채원 서연 하린 시아 아린 이나 소율"),
}


def pick_surname(rng: random.Random):
    return rng.choices(SURNAMES, weights=[s[3] for s in SURNAMES])[0][:3]


def make_name(rng: random.Random, gender: str, birth_year: int | None = None):
    """(한글, 한자, 로마자 성, 로마자 이름) 반환. birth_year 를 주면 반은 그 연대의 흔한 이름."""
    sur, sur_h, sur_r = pick_surname(rng)
    if birth_year and rng.random() < 0.5:
        decade = min(2010, max(1960, birth_year // 10 * 10))
        given = rng.choice(POPULAR[decade][0 if gender == "M" else 1].split())
    else:
        first = rng.choice(MALE_FIRST if gender == "M" else FEMALE_FIRST)
        second = rng.choice([c for c in (MALE_SECOND if gender == "M" else FEMALE_SECOND) if c != first])
        given = first + second
    hanja = sur_h + "".join(rng.choice(GIVEN_SYLLABLES[c]) for c in given)
    return sur + given, hanja, sur_r, "".join(GIVEN_ROMAN[c] for c in given)


# ---------------------------------------------------------------------------
# 주소
# ---------------------------------------------------------------------------

# 시도, 시군구, 우편번호 앞 3자리, 법정동·읍면, 도로명 — docgen/assets/regions.json (시군구 143곳, 인구 가중치,
# 도로마다 실제로 지나는 동을 짝지어 둠: ROAD_DONG). 인천 중구·서구, 화성시는 2026년 개편 전 이름으로 적는다.
def _load_regions():
    import json
    from pathlib import Path

    rows = json.loads((Path(__file__).with_name("assets") / "regions.json").read_text(encoding="utf-8"))
    regions = [(e["sido"], e["sigungu"], e["zip3"], e["dongs"], [r for r, _ in e["roads"]]) for e in rows]
    road_dong = {(e["sido"], e["sigungu"], r): dong for e in rows for r, dong in e["roads"]}
    return regions, [e["weight"] for e in rows], road_dong


REGIONS, REGION_WEIGHTS, ROAD_DONG = _load_regions()

APT_NAMES = ["래미안", "자이", "힐스테이트", "푸르지오", "e편한세상", "롯데캐슬", "아이파크",
             "더샵", "SK뷰", "센트레빌", "호반베르디움", "한신휴플러스", "우성", "현대", "삼익"]
APT_SUFFIX = ["", "1차", "2차", "센트럴", "파크", "리버뷰", "퍼스트", "에듀포레"]
BUILDING_NAMES = ["타워", "빌딩", "센터", "프라자", "스퀘어", "오피스텔", "지식산업센터"]


def sido_short(sido: str) -> str:
    return {"서울특별시": "서울", "부산광역시": "부산", "대구광역시": "대구", "인천광역시": "인천",
            "광주광역시": "광주", "대전광역시": "대전", "울산광역시": "울산", "세종특별자치시": "세종",
            "경기도": "경기", "강원특별자치도": "강원", "충청북도": "충북", "충청남도": "충남",
            "전북특별자치도": "전북", "전라남도": "전남", "경상북도": "경북", "경상남도": "경남",
            "제주특별자치도": "제주"}[sido]


# ---------------------------------------------------------------------------
# 식별번호
# ---------------------------------------------------------------------------

def rrn(rng: random.Random, birth: date, gender: str, foreigner: bool = False) -> str:
    """주민등록번호/외국인등록번호 형식 (검증용 체크섬 포함, 합성값)."""
    century2000 = birth.year >= 2000
    if foreigner:
        g = (7 if century2000 else 5) + (0 if gender == "M" else 1)
    else:
        g = (3 if century2000 else 1) + (0 if gender == "M" else 1)
    body = f"{birth:%y%m%d}{g}" + "".join(str(rng.randint(0, 9)) for _ in range(5))
    weights = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]
    s = sum(int(c) * w for c, w in zip(body, weights))
    check = (11 - s % 11) % 10
    return f"{body[:6]}-{body[6:]}{check}"


def mask_rrn(v: str, keep: int = 1) -> str:
    front, back = v.split("-")
    return f"{front}-{back[:keep]}{'*' * (7 - keep)}"


def biz_no(rng: random.Random, corporate: bool = False) -> str:
    """사업자등록번호 (체크섬 포함). 가운데 2자리: 개인 01~79, 법인 81~88."""
    head = f"{rng.randint(101, 899)}"
    mid = f"{rng.choice([81, 82, 86, 87, 88]) if corporate else rng.randint(1, 79):02d}"
    tail4 = f"{rng.randint(0, 9999):04d}"
    digits = [int(c) for c in head + mid + tail4]
    w = [1, 3, 7, 1, 3, 7, 1, 3, 5]
    s = sum(d * x for d, x in zip(digits, w)) + (digits[8] * 5) // 10
    check = (10 - s % 10) % 10
    return f"{head}-{mid}-{tail4}{check}"


def corp_reg_no(rng: random.Random) -> str:
    """법인등록번호 13자리 (체크섬 포함)."""
    office = rng.choice(["1101", "1311", "1201", "1301", "1601", "1350", "1715", "2001"])
    kind = rng.choice(["11", "11", "11", "12"])
    body = office + kind + f"{rng.randint(0, 999999):06d}"
    w = [1, 2] * 6
    s = sum(int(c) * x for c, x in zip(body, w))
    check = (10 - s % 10) % 10
    return f"{body[:6]}-{body[6:]}{check}"


def mobile(rng: random.Random) -> str:
    return f"010-{rng.randint(2000, 9999)}-{rng.randint(0, 9999):04d}"


AREA_CODES = {"서울": "02", "부산": "051", "대구": "053", "인천": "032", "광주": "062", "대전": "042",
              "울산": "052", "세종": "044", "경기": "031", "강원": "033", "충북": "043", "충남": "041",
              "전북": "063", "전남": "061", "경북": "054", "경남": "055", "제주": "064"}


def landline(rng: random.Random, sido: str) -> str:
    code = AREA_CODES[sido_short(sido)]
    mid = rng.randint(200, 9999) if code == "02" else rng.randint(200, 999)
    return f"{code}-{mid}-{rng.randint(0, 9999):04d}"


# ---------------------------------------------------------------------------
# 금액/날짜 포맷
# ---------------------------------------------------------------------------

_DIGITS = "영일이삼사오육칠팔구"
_HANJA_DIGITS = "零壹貳參肆伍陸柒捌玖"


def _korean_under_10000(n: int, digits: str, units: list[str]) -> str:
    out = ""
    for i, u in zip(range(3, -1, -1), units):
        d = (n // 10 ** i) % 10
        if d:
            # 공식 금액 표기 관행: '일천', '일백'은 쓰고 '일십'은 '십'으로 쓴다.
            out += ("" if (d == 1 and u in ("십",)) else digits[d]) + u
    return out


def won_korean(n: int, hanja: bool = False) -> str:
    """금액 한글 표기: 120000000 -> '일억이천만'. hanja=True면 '壹億貳阡萬'."""
    if n == 0:
        return "영"
    digits = _HANJA_DIGITS if hanja else _DIGITS
    units = ["阡", "百", "拾", ""] if hanja else ["천", "백", "십", ""]
    big = ["", "萬", "億", "兆"] if hanja else ["", "만", "억", "조"]
    parts = []
    for i, b in enumerate(big):
        chunk = (n // 10000 ** i) % 10000
        if chunk:
            parts.append(_korean_under_10000(chunk, digits, units) + b)
    return "".join(reversed(parts))


def won(n: int, suffix: str = "원") -> str:
    return f"{n:,}{suffix}"


def fmt_date(d: date, style: str = "dot") -> str:
    if style == "dot":
        return f"{d:%Y.%m.%d}"
    if style == "dash":
        return f"{d:%Y-%m-%d}"
    if style == "kor":
        return f"{d.year}년 {d.month:02d}월 {d.day:02d}일"
    if style == "kor_short":
        return f"{d.year}년 {d.month}월 {d.day}일"
    if style == "slash":
        return f"{d:%Y/%m/%d}"
    if style == "en":
        return d.strftime("%d %b %Y").upper()
    if style == "en_long":
        return d.strftime("%B %d, %Y")
    raise ValueError(style)


def round_to(n: float, unit: int) -> int:
    return int(round(n / unit) * unit)
