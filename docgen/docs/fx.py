"""외환·무역 서류 (대부분 영문): 상업송장, 매매계약서, 선하증권, 포장명세서, 수입신고필증, 입학허가서, 학비 청구서.

이 파일에는 그룹 서식들이 같이 쓰는 도우미만 있다. 서식마다 값 만드는 함수(@doc)는 서식 폴더
docgen/forms/<ID>/generate.py 에 있고, 끝의 FORMS 차례로 등록한다.

같은 프로필이면 무역 서류들의 선적 정보(품목, 수량, 금액, B/L 번호, 선박, 일자)가 일치하도록
`_shipment(p)`가 프로필 seed 로부터 결정론적으로 공통 사실을 만든다.
유학 서류(입학허가서·학비청구서)는 `_study(p)`로 학교·학생·학기 정보를 공유한다.
"""
import math
import re
from decimal import ROUND_HALF_UP, Decimal

from ..entities import _ROMAN_PREFIX
from ._common import *  # noqa: F401,F403
from ..registry import register_folder_forms

# ---------------------------------------------------------------------------
# 로마자 표기 (국어의 로마자 표기법 단순화 버전)
# ---------------------------------------------------------------------------
_CHO = ["g", "kk", "n", "d", "tt", "r", "m", "b", "pp", "s", "ss", "", "j", "jj", "ch", "k", "t", "p", "h"]
_JUNG = ["a", "ae", "ya", "yae", "eo", "e", "yeo", "ye", "o", "wa", "wae", "oe", "yo", "u", "wo", "we", "wi", "yu", "eu", "ui", "i"]
_JONG = ["", "k", "k", "k", "n", "n", "n", "t", "l", "k", "m", "l", "l", "l", "p", "l", "m", "p", "p", "t", "t", "ng", "t", "t", "k", "t", "p", "t"]
_SIDO_EN = {"서울특별시": "Seoul", "부산광역시": "Busan", "대구광역시": "Daegu", "인천광역시": "Incheon",
            "광주광역시": "Gwangju", "대전광역시": "Daejeon", "울산광역시": "Ulsan", "세종특별자치시": "Sejong-si",
            "경기도": "Gyeonggi-do", "강원특별자치도": "Gangwon-do", "충청북도": "Chungcheongbuk-do",
            "충청남도": "Chungcheongnam-do", "전북특별자치도": "Jeonbuk-do", "전라남도": "Jeollanam-do",
            "경상북도": "Gyeongsangbuk-do", "경상남도": "Gyeongsangnam-do", "제주특별자치도": "Jeju-do"}
_BLDG_EN = {"지식산업센터": "Knowledge Industry Center", "오피스텔": "Officetel", "타워": "Tower", "빌딩": "Building",
            "센터": "Center", "프라자": "Plaza", "스퀘어": "Square"}
_BANK_EN = {"국민은행": ("KOOKMIN BANK", "CZNBKRSE"), "신한은행": ("SHINHAN BANK", "SHBKKRSE"),
            "우리은행": ("WOORI BANK", "HVBKKRSE"), "하나은행": ("HANA BANK", "KOEXKRSE"),
            "KEB하나은행": ("KEB HANA BANK", "KOEXKRSE"), "외환은행": ("KOREA EXCHANGE BANK", "KOEXKRSE"),
            "농협은행": ("NONGHYUP BANK", "NACFKRSE"), "기업은행": ("INDUSTRIAL BANK OF KOREA", "IBKOKRSE"),
            "SC제일은행": ("STANDARD CHARTERED BANK KOREA", "SCBLKRSE"), "부산은행": ("BUSAN BANK", "PUSBKR2P"),
            "iM뱅크": ("iM BANK", "DAEBKR22")}


def _rom_syl(text: str) -> str:
    out, prev_final = [], ""
    for ch in text:
        c = ord(ch) - 0xAC00
        if not 0 <= c < 11172:
            out.append(ch)
            prev_final = ""
            continue
        cho, jung, jong = c // 588, (c % 588) // 28, c % 28
        ini = _CHO[cho]
        if cho == 5:  # ㄹ
            ini = "l" if prev_final == "l" else "r"
        if cho == 11 and prev_final in ("k", "t", "p") and out:  # 연음 단순 처리
            out[-1] = out[-1][:-1] + {"k": "g", "t": "d", "p": "b"}[prev_final]
        fin = _JONG[jong]
        out.append(ini + _JUNG[jung] + fin)
        prev_final = fin
    return "".join(out)


_ROM_FIXED = {"월드컵로": "World Cup-ro", "달맞이길": "Dalmaji-gil", "컨벤시아대로": "Convensia-daero",
              "센텀중앙로": "Centum jungang-ro", "인천타워대로": "Incheon tower-daero", "포스코대로": "POSCO-daero"}


def _rom(text: str) -> str:
    """'테헤란로' -> 'Teheran-ro', '강남구' -> 'Gangnam-gu', '성남시 분당구' -> 'Bundang-gu, Seongnam-si'"""
    parts = []
    for w in text.split():
        if w in _ROM_FIXED:
            parts.append(_ROM_FIXED[w])
            continue
        for suf, en in (("대로", "daero"), ("로", "ro"), ("길", "gil"), ("구", "gu"), ("시", "si"), ("군", "gun"),
                        ("동", "dong"), ("읍", "eup"), ("면", "myeon")):
            if w.endswith(suf) and len(w) > len(suf):
                stem = w[:-len(suf)]
                parts.append(f"{_rom_syl(stem).capitalize()}-{en}")
                break
        else:
            parts.append(_rom_syl(w).capitalize())
    return ", ".join(reversed(parts))


def _bldg_en(name: str) -> str:
    for k, v in _ROMAN_PREFIX.items():
        if name.startswith(k):
            rest = name[len(k):]
            return f"{v} {_BLDG_EN.get(rest, _rom_syl(rest).capitalize())}".strip()
    return _rom_syl(name).capitalize()


def _addr_en(a: Address) -> str:
    """영문 주소: '12F, Hanbit Tower, 123 Teheran-ro, Gangnam-gu, Seoul 06123, Korea'"""
    bits = []
    m = re.match(r"(\d+)층(?:\s*(\d+)호)?", a.detail or "")
    apt = re.match(r"(?:(\d+)동\s*)?(\d+)호", a.detail or "")
    if m:
        bits.append(f"Rm. {m.group(1)}{m.group(2)}" if m.group(2) else f"{m.group(1)}F")
        if m.group(2):
            bits.append(f"{m.group(1)}F")
        if a.building_name:
            bits.append(_bldg_en(a.building_name))
    elif apt:  # 주거용: 아파트 이름은 생략하고 동-호만 표기
        bits.append(f"Apt. {apt.group(1)}-{apt.group(2)}" if apt.group(1) else f"Unit {apt.group(2)}")
    bits.append(f"{a.building_no} {_rom(a.road)}")
    if a.sigungu:
        bits.append(_rom(a.sigungu))
    bits.append(f"{_SIDO_EN[a.sido]} {a.zipcode}, Korea")
    return ", ".join(bits)


# ---------------------------------------------------------------------------
# 무역 상대방 / 상품 / 운송
# ---------------------------------------------------------------------------
# 상대방이 대학인 프로필용 대체 거래처 (이름, 주소, 국가, 담당자)
_TRADE_PARTIES = [
    ("Golden Bridge Industrial Co., Ltd.", "No. 168 Huangpu Rd, Huangpu District, Guangzhou 510700", "CHINA", "Chen Jie"),
    ("Osaka Fine Parts Co., Ltd.", "4-5-10 Minamisemba, Chuo-ku, Osaka 542-0081", "JAPAN", "Kenji Sato"),
    ("Saigon Textile Export JSC", "112 Nguyen Hue Blvd, District 1, Ho Chi Minh City", "VIETNAM", "Tran Thi Mai"),
    ("Westfield Supply Inc.", "2500 Commerce Pkwy, Dallas, TX 75201", "UNITED STATES", "Michael Brown"),
]
_COUNTRY = {  # 국가: (ISO, 항구 목록, 운송일수, 통화, 상품군)
    "UNITED STATES": ("US", ["LONG BEACH, CA, USA", "LOS ANGELES, CA, USA", "OAKLAND, CA, USA", "SEATTLE, WA, USA"], (13, 20), "USD", ["chemical", "food", "medical", "machinery"]),
    "JAPAN": ("JP", ["TOKYO, JAPAN", "YOKOHAMA, JAPAN", "OSAKA, JAPAN", "NAGOYA, JAPAN"], (2, 4), "JPY", ["machinery", "electronics", "auto"]),
    "CHINA": ("CN", ["SHANGHAI, CHINA", "SHEKOU, CHINA", "QINGDAO, CHINA", "NINGBO, CHINA"], (2, 5), "USD", ["electronics", "auto", "textiles", "medical"]),
    "VIETNAM": ("VN", ["HO CHI MINH CITY (CAT LAI), VIETNAM", "HAIPHONG, VIETNAM"], (5, 8), "USD", ["textiles", "food"]),
    "GERMANY": ("DE", ["HAMBURG, GERMANY", "BREMERHAVEN, GERMANY"], (32, 40), "EUR", ["machinery", "auto", "medical"]),
    "SINGAPORE": ("SG", ["SINGAPORE"], (6, 9), "USD", ["chemical", "electronics"]),
}
_CONTACTS = {"UNITED STATES": ["John Miller", "Sarah Johnson", "Michael Brown"], "JAPAN": ["Akira Tanaka", "Kenji Sato", "Yuko Nakamura"],
             "CHINA": ["Li Wei", "Chen Jie", "Wang Fang"], "VIETNAM": ["Nguyen Van An", "Tran Thi Mai"],
             "GERMANY": ["Klaus Weber", "Anna Schmidt"], "SINGAPORE": ["Tan Wei Ming", "Lim Mei Ling"]}
_CP_CAT = {"Tokyo Seimitsu Kogyo K.K.": ["machinery", "electronics"], "Shenzhen Huaxin Electronics Ltd.": ["electronics"],
           "Mekong Garment JSC": ["textiles"], "Rheinland Maschinenbau GmbH": ["machinery"],
           "Osaka Fine Parts Co., Ltd.": ["machinery", "auto"], "Saigon Textile Export JSC": ["textiles"]}
_BIZ_CAT = {"전자부품": "electronics", "자동차부품": "auto", "화학제품": "chemical", "식료품": "food",
            "의류 도매": "textiles", "의료기기": "medical"}
# (HS 품명, 거래품명, HS코드, 단위, 단가범위 USD, 포장당 수량, 포장당 순중량 kg, 포장당 CBM, 포장단위, 모델 접두, 기본세율 %)
_GOODS = {
    "electronics": [
        ("CERAMIC DIELECTRIC, MULTILAYER", "Multilayer Ceramic Capacitor 0402 100nF 16V", "8532.24-0000", "PCS", (0.004, 0.015), 100000, 8.5, 0.035, "CTNS", "CL05", 0),
        ("PRINTED CIRCUITS", "Printed Circuit Board, 6-Layer FR-4", "8534.00-1000", "PCS", (1.8, 6.5), 500, 14.0, 0.06, "CTNS", "PCB", 0),
        ("LITHIUM-ION ACCUMULATORS", "Li-ion Battery Cell 18650 3.6V 3000mAh", "8507.60-0000", "PCS", (1.6, 3.2), 400, 19.0, 0.035, "CTNS", "INR18650", 8),
        ("ELECTRONIC INTEGRATED CIRCUITS", "LED Driver IC, SOP-8", "8542.39-1000", "PCS", (0.12, 0.6), 20000, 6.0, 0.03, "CTNS", "LD", 0),
        ("FLAT PANEL DISPLAY MODULES", "TFT-LCD Module 10.1 inch", "8524.11-0000", "PCS", (28.0, 65.0), 20, 12.0, 0.08, "CTNS", "TM101", 0),
        ("ELECTRICAL CONNECTORS, FOR A VOLTAGE NOT EXCEEDING 1,000V", "Board-to-Board Connector 0.5mm Pitch 40P", "8536.69-9000", "PCS", (0.08, 0.45), 2000, 9.0, 0.03, "CTNS", "BB", 8),
        ("FIXED CARBON RESISTORS, CHIP TYPE", "Thick Film Chip Resistor 0603 10K OHM 1%", "8533.21-0000", "PCS", (0.001, 0.004), 100000, 7.0, 0.03, "CTNS", "RC", 0),
    ],
    "machinery": [
        ("BALL BEARINGS", "Deep Groove Ball Bearing 6205-2RS", "8482.10-0000", "PCS", (0.9, 3.5), 200, 22.0, 0.025, "CTNS", "6205", 8),
        ("CENTRIFUGAL PUMPS", "Centrifugal Pump 5.5kW", "8413.70-0000", "SETS", (420.0, 1600.0), 1, 85.0, 0.35, "CASES", "CP", 8),
        ("PARTS OF MACHINE TOOLS", "Spindle Unit for CNC Lathe", "8466.93-0000", "SETS", (850.0, 3800.0), 1, 120.0, 0.4, "CASES", "SP", 8),
        ("HYDRAULIC CYLINDERS", "Hydraulic Cylinder, Bore 80mm", "8412.21-0000", "PCS", (180.0, 650.0), 4, 96.0, 0.25, "CASES", "HC", 8),
        ("SOLENOID VALVES", "Solenoid Valve 1/2\" 24VDC", "8481.80-2000", "PCS", (12.0, 45.0), 20, 14.0, 0.04, "CTNS", "SV", 8),
        ("GEAR BOXES AND OTHER SPEED CHANGERS", "Planetary Gear Reducer Ratio 1:10", "8483.40-1000", "SETS", (150.0, 600.0), 2, 40.0, 0.06, "CASES", "PGR", 8),
    ],
    "textiles": [
        ("T-SHIRTS, KNITTED, OF COTTON", "Men's Cotton Crew Neck T-Shirt", "6109.10-0000", "PCS", (2.1, 5.5), 100, 18.0, 0.09, "CTNS", "MT", 13),
        ("ANORAKS, WIND-JACKETS, OF SYNTHETIC FIBRES", "Women's Padded Jacket (Polyester)", "6202.40-0000", "PCS", (11.0, 28.0), 20, 16.0, 0.14, "CTNS", "WJ", 13),
        ("DENIM FABRICS OF COTTON", "Denim Fabric 12oz, 58\" Width", "5209.42-0000", "YDS", (2.4, 4.8), 100, 45.0, 0.12, "ROLLS", "DN", 8),
        ("TROUSERS, OF COTTON", "Men's Chino Pants", "6203.42-0000", "PCS", (5.5, 12.0), 40, 19.0, 0.11, "CTNS", "CP", 13),
        ("CARDIGANS, KNITTED, OF COTTON", "Women's Cotton Knit Cardigan", "6110.20-0000", "PCS", (6.0, 14.0), 30, 15.0, 0.1, "CTNS", "KC", 13),
        ("DRESSES OF SYNTHETIC FIBRES", "Women's Polyester Midi Dress", "6204.43-0000", "PCS", (7.0, 18.0), 40, 14.0, 0.1, "CTNS", "WD", 13),
    ],
    "chemical": [
        ("POLYPROPYLENE, IN PRIMARY FORMS", "Polypropylene Resin (Homopolymer) H5300", "3902.10-0000", "KG", (1.05, 1.6), 25, 25.0, 0.04, "BAGS", "PP", 6.5),
        ("EPOXIDE RESINS", "Liquid Epoxy Resin EEW 185", "3907.30-0000", "KG", (2.8, 4.5), 220, 220.0, 0.28, "DRUMS", "EP", 6.5),
        ("PIGMENTS BASED ON TITANIUM DIOXIDE", "Titanium Dioxide Rutile R-902", "3206.11-0000", "KG", (2.6, 3.8), 25, 25.0, 0.035, "BAGS", "TR", 6.5),
        ("LINEAR LOW DENSITY POLYETHYLENE", "LLDPE Resin, Film Grade", "3901.10-9000", "KG", (1.0, 1.5), 25, 25.0, 0.04, "BAGS", "LL", 6.5),
        ("NON-IONIC ORGANIC SURFACE-ACTIVE AGENTS", "Nonionic Surfactant (Fatty Alcohol Ethoxylate)", "3402.42-0000", "KG", (1.8, 3.2), 200, 200.0, 0.28, "DRUMS", "NS", 6.5),
    ],
    "food": [
        ("SHRIMPS AND PRAWNS, FROZEN", "Frozen Vannamei Shrimp HLSO 21/25", "0306.17-1000", "KG", (7.5, 11.0), 10, 10.0, 0.03, "CTNS", "VS", 20),
        ("COFFEE, ROASTED, NOT DECAFFEINATED", "Roasted Coffee Beans, Arabica", "0901.21-0000", "KG", (9.0, 16.0), 12, 12.0, 0.05, "CTNS", "CB", 8),
        ("ALMONDS, SHELLED", "Shelled Almonds 23/25 Supreme", "0802.12-0000", "KG", (5.5, 8.5), 25, 25.0, 0.045, "CTNS", "AL", 8),
        ("SQUID, FROZEN", "Frozen Squid Whole Round", "0307.43-1000", "KG", (2.5, 4.5), 10, 10.0, 0.03, "CTNS", "SQ", 10),
        ("COCOA POWDER, NOT CONTAINING ADDED SUGAR", "Alkalized Cocoa Powder 10-12%", "1805.00-0000", "KG", (3.5, 7.0), 25, 25.0, 0.04, "BAGS", "CC", 8),
    ],
    "auto": [
        ("BRAKE PADS FOR MOTOR VEHICLES", "Disc Brake Pad Set, Front", "8708.30-1000", "SETS", (4.5, 14.0), 20, 24.0, 0.04, "CTNS", "BP", 8),
        ("OIL FILTERS FOR INTERNAL COMBUSTION ENGINES", "Engine Oil Filter", "8421.23-1000", "PCS", (0.9, 2.8), 50, 15.0, 0.06, "CTNS", "OF", 8),
        ("PARTS FOR SPARK-IGNITION ENGINES", "Piston Ring Set", "8409.91-0000", "SETS", (3.0, 9.0), 50, 12.0, 0.03, "CTNS", "PR", 8),
        ("SHOCK ABSORBERS FOR MOTOR VEHICLES", "Shock Absorber, Rear", "8708.80-1000", "PCS", (9.0, 28.0), 4, 10.0, 0.03, "CTNS", "SA", 8),
        ("SPARKING PLUGS", "Iridium Spark Plug", "8511.10-0000", "PCS", (1.8, 5.5), 100, 6.0, 0.02, "CTNS", "SPK", 8),
    ],
    "medical": [
        ("SYRINGES, WITH OR WITHOUT NEEDLES", "Disposable Syringe 5ml with Needle 23G", "9018.31-0000", "PCS", (0.03, 0.08), 1600, 11.0, 0.08, "CTNS", "DS", 8),
        ("GLOVES OF VULCANISED RUBBER", "Nitrile Examination Gloves, Powder Free (100pcs/box)", "4015.19-0000", "BOXES", (2.0, 4.5), 10, 6.5, 0.04, "CTNS", "NG", 8),
        ("ULTRASONIC SCANNING APPARATUS", "Portable Ultrasound Scanner", "9018.12-0000", "SETS", (2500.0, 9000.0), 1, 9.0, 0.08, "CTNS", "US", 8),
        ("CATHETERS, CANNULAE AND THE LIKE", "IV Cannula with Injection Port 22G", "9018.39-0000", "PCS", (0.08, 0.25), 1000, 9.0, 0.06, "CTNS", "IV", 8),
        ("SURGICAL FACE MASKS", "Surgical Face Mask 3-Ply (50pcs/box)", "6307.90-9000", "BOXES", (0.8, 2.0), 40, 8.0, 0.08, "CTNS", "SM", 10),
    ],
}
_VESSELS = ["STAR PIONEER", "OCEAN HARMONY", "BLUE HORIZON", "PACIFIC BRIDGE", "GOLDEN GATEWAY", "SEA FORTUNE",
            "MORNING CALM", "NORTHERN LIGHT", "SILVER WAVE", "EASTERN PROMISE", "CORAL VOYAGER", "HAN RIVER"]
_CARRIERS = [("Trans-Pacific Marine Lines", "TPML", "TPMU"), ("Hanbada Shipping Co., Ltd.", "HBSC", "HBDU"),
             ("Oceanlink Container Lines", "OCLN", "OCLU"), ("Blue Anchor Shipping Ltd.", "BASL", "BAQU"),
             ("East Sea Express Line", "ESXL", "ESXU")]
_FORWARDERS = ["Seoul Global Logistics Co., Ltd.", "Hanil Air & Sea Co., Ltd.", "K-Link Forwarding Inc.", "Daon Logistics Co., Ltd."]

_ONES = "ZERO ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN ELEVEN TWELVE THIRTEEN FOURTEEN FIFTEEN SIXTEEN SEVENTEEN EIGHTEEN NINETEEN".split()
_TENS = "_ _ TWENTY THIRTY FORTY FIFTY SIXTY SEVENTY EIGHTY NINETY".split()


def _words(n: int) -> str:
    """정수 영문 표기: 1234 -> 'ONE THOUSAND TWO HUNDRED THIRTY FOUR'"""
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else " " + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " HUNDRED" + ("" if n % 100 == 0 else " " + _words(n % 100))
    for div, name in ((10 ** 9, "BILLION"), (10 ** 6, "MILLION"), (1000, "THOUSAND")):
        if n >= div:
            return _words(n // div) + " " + name + ("" if n % div == 0 else " " + _words(n % div))
    return str(n)


def _dec(cur: str) -> Decimal:
    return Decimal("1") if cur == "JPY" else Decimal("0.01")


def _money(x: Decimal, cur: str) -> str:
    return f"{x:,.0f}" if cur == "JPY" else f"{x:,.2f}"


def _price_str(x: Decimal, cur: str) -> str:
    if cur == "JPY":
        return f"{x:,.2f}" if x < 100 else f"{x:,.0f}"
    return f"{x:,.4f}" if x < 1 else f"{x:,.2f}"


def _counterparty(p: Profile, r: random.Random) -> dict:
    fp = p.foreign
    if "University" in fp.name or fp.country not in _COUNTRY:
        name, addr, country, contact = r.choice(_TRADE_PARTIES)
    else:
        name, addr, country = fp.name, fp.address, fp.country
        contact = r.choice(_CONTACTS[country])
    return {"name": name, "address": addr, "country": country, "contact": contact,
            "bank": fp.bank, "swift": fp.swift}


# 중계무역(제3국 결제) 판매자: 제조사(선적인)와 다른 나라의 무역회사가 송장을 발행하고 대금을 받는다.
_INTERMEDIARIES = [
    ("Pacific Rim Trading Ltd.", "Unit 1205, 12/F, 89 Queensway, Admiralty, Hong Kong", "HONG KONG", "HK",
     "THE HONGKONG AND SHANGHAI BANKING CORPORATION LTD., HONG KONG", "HSBCHKHHHKH"),
    ("Golden Crown International Ltd.", "Room 1802, 18/F, 88 Connaught Road Central, Hong Kong", "HONG KONG", "HK",
     "BANK OF CHINA (HONG KONG) LIMITED", "BKCHHKHH"),
    ("Asia Link Resources Pte. Ltd.", "80 Robinson Road, #10-01, Singapore 068898", "SINGAPORE", "SG",
     "DBS BANK LTD., SINGAPORE", "DBSSSGSG"),
    ("Meridian Global Sourcing Pte. Ltd.", "30 Cecil Street, #19-08, Singapore 049712", "SINGAPORE", "SG",
     "OVERSEA-CHINESE BANKING CORPORATION LTD.", "OCBCSGSG"),
]
_COLORS = ["BLACK", "NAVY", "WHITE", "GREY", "BEIGE", "KHAKI", "OLIVE", "BURGUNDY", "SKY BLUE", "CHARCOAL", "IVORY"]
_SIZES = ["XS", "S", "M", "L", "XL", "XXL"]


def _variant(cat: str, g: tuple, r: random.Random) -> str:
    """품목이 많은 송장의 줄 구분(색상·사이즈·등급·로트 등)."""
    if cat == "textiles":
        return f"{r.choice(_COLORS)}/{r.choice(_SIZES)}" if g[3] == "PCS" else f"COLOR {r.choice(['INDIGO', 'BLACK', 'ECRU', 'LIGHT BLUE'])}"
    if cat == "food":
        return r.choice(["GRADE A", "GRADE AA", "PREMIUM", "STANDARD"]) + f", LOT {r.randint(1, 12):02d}{r.choice('ABC')}"
    if cat == "chemical":
        return f"LOT NO. {r.randint(24, 26)}{r.randint(1, 12):02d}-{r.randint(1, 40):02d}"
    if cat == "medical" and g[3] != "SETS":
        return f"SIZE {r.choice(['S', 'M', 'L', 'XL'])}" if "Glove" in g[1] else ""
    return ""


def _alloc_containers(items: list[dict], ncont: int, r: random.Random) -> list[dict]:
    """컨테이너별 포장수·중량·용적. 줄이 충분히 많으면 줄 단위로 차례로 싣는다 (포장명세서 컨테이너별 구분과 일치)."""
    tot = float(sum(it["cbm"] for it in items)) or 1.0
    if ncont > 1 and len(items) >= 2 * ncont:
        per, cum, idx = tot / ncont, 0.0, []
        for it in items:
            idx.append(min(ncont - 1, int((cum + float(it["cbm"]) / 2) / per)))
            cum += float(it["cbm"])
        if len(set(idx)) == ncont:
            for it, k in zip(items, idx):
                it["cont"] = k
            out = []
            for k in range(ncont):
                rows = [it for it in items if it["cont"] == k]
                out.append({"pkgs": sum(it["pkgs"] for it in rows), "gross": sum((it["gross"] for it in rows), Decimal(0)),
                            "net": sum((it["net"] for it in rows), Decimal(0)), "cbm": sum((it["cbm"] for it in rows), Decimal(0))})
            return out
    # 줄 수가 적으면 합계를 나눈다 (줄과 컨테이너 대응 없음)
    w = [r.uniform(0.8, 1.2) for _ in range(ncont)]
    tot_v = {"pkgs": sum(it["pkgs"] for it in items), "gross": sum((it["gross"] for it in items), Decimal(0)),
             "net": sum((it["net"] for it in items), Decimal(0)), "cbm": sum((it["cbm"] for it in items), Decimal(0))}
    out, acc, cum = [], {k: 0 for k in tot_v}, 0.0
    for k in range(ncont):
        if k == ncont - 1:
            out.append({key: tot_v[key] - acc[key] for key in tot_v})
            break
        cum += w[k] / sum(w)
        sh = Decimal(str(round(cum, 4)))
        c = {"pkgs": max(acc["pkgs"] + 1, int(tot_v["pkgs"] * cum)) - acc["pkgs"],
             "gross": (tot_v["gross"] * sh).quantize(Decimal("0.01")) - acc["gross"],
             "net": (tot_v["net"] * sh).quantize(Decimal("0.01")) - acc["net"],
             "cbm": (tot_v["cbm"] * sh).quantize(Decimal("0.001")) - acc["cbm"]}
        out.append(c)
        for key in acc:
            acc[key] += c[key]
    return out


def _shipment(p: Profile, force_import: bool = False) -> dict:
    """무역 서류 공통 사실 (프로필 seed 기준 결정론적).
    여러 쪽·특수 상황(품목 다수, 분할선적, 신용장, 중계무역)도 여기서 정해 송장·포장명세서·계약서·B/L·수입신고필증이 서로 맞는다."""
    r = random.Random(f"fx:{p.seed}")
    rv = random.Random(f"fxv:{p.seed}")  # 변형 결정용 (기존 값의 난수 흐름을 바꾸지 않게 따로 둔다)
    many = heavy(rv, 0.25)
    split = special(rv, "split_shipment", 0.12)
    force_lc = special(rv, "lc", 0.12)
    triangular = special(rv, "triangular", 0.1)
    cp = _counterparty(p, r)
    iso, ports, transit, cur, cats = _COUNTRY[cp["country"]]
    if cur == "JPY" and r.random() < 0.3:
        cur = "USD"
    if cur == "EUR" and r.random() < 0.2:
        cur = "USD"
    corp = p.corporation
    direction = "import" if r.random() < 0.7 else "export"
    if force_import:
        direction = "import"
    cp_cat = r.choice(_CP_CAT[cp["name"]]) if cp["name"] in _CP_CAT else None
    own_cat = _BIZ_CAT.get(corp.biz_item)
    if direction == "import":
        cat = cp_cat or own_cat or r.choice(cats)
    else:  # 수출: 우리 회사 업종의 상품
        cat = own_cat or cp_cat or r.choice(cats)
    kr_port = "INCHEON, KOREA" if iso == "CN" and r.random() < 0.5 else "BUSAN, KOREA"
    foreign_port = r.choice(ports)
    tr_days = r.randint(*transit)
    if direction == "import":
        arrival = p.issue_date - timedelta(days=r.randint(4, 25))
        on_board = arrival - timedelta(days=tr_days)
        pol, pod = foreign_port, kr_port
    else:
        on_board = p.issue_date - timedelta(days=r.randint(3, 15))
        arrival = on_board + timedelta(days=tr_days)
        pol, pod = kr_port, foreign_port
    inv_date = on_board - timedelta(days=r.randint(1, 5))
    contract_date = inv_date - timedelta(days=r.randint(20, 60))
    incoterm = r.choice(["FOB", "FOB", "CIF", "CIF", "CFR", "FCA"])
    payment = r.choice(["T/T IN ADVANCE", "T/T 30 DAYS AFTER B/L DATE", "T/T 60 DAYS AFTER B/L DATE",
                        "L/C AT SIGHT", "L/C 90 DAYS AFTER B/L DATE", "D/P AT SIGHT", "D/A 60 DAYS AFTER B/L DATE"])
    if force_lc and "L/C" not in payment:
        payment = rv.choice(["L/C AT SIGHT", "L/C AT SIGHT", "L/C 90 DAYS AFTER B/L DATE"])
    fx = {"USD": Decimal(1), "EUR": Decimal("0.92"), "JPY": Decimal(150)}[cur]
    q = _dec(cur)
    goods = r.sample(_GOODS[cat], min(len(_GOODS[cat]), r.randint(2, 4)))
    target = r.uniform(25_000, 320_000) / len(goods)
    # 줄 구성: (상품, 단가USD, 포장수, 줄 구분)
    lines = []
    if many:  # 품목(라인아이템) 20~60개: 같은 상품의 색상·사이즈·모델별 줄
        base = rv.sample(_GOODS[cat], min(len(_GOODS[cat]), rv.randint(2, 6)))
        n = rv.randint(20, 60)
        picks = sorted(list(range(len(base))) + [rv.randrange(len(base)) for _ in range(n - len(base))])
        per_line = rv.uniform(150_000, 1_200_000) / n
        for b in picks:
            g = base[b]
            price_usd = rv.uniform(*g[4])
            pkgs = max(1, round(per_line * rv.uniform(0.3, 1.7) / (price_usd * g[5])))
            if g[8] == "CASES":
                pkgs = min(pkgs, rv.randint(1, 8))
            lines.append((g, price_usd, pkgs, _variant(cat, g, rv), b))
        # 컨테이너 2~9개 물량에 맞추기 (용적·중량 기준, 총액 상한 USD 3백만)
        cbm0 = sum(g[7] * k for g, _, k, _, _ in lines)
        val0 = sum(pu * g[5] * k for g, pu, k, _, _ in lines)
        gw0 = sum(g[6] * k for g, _, k, _, _ in lines)
        nwant = rv.randint(2, 9)
        f = min(nwant * rv.uniform(48, 62) / max(cbm0, 0.01), nwant * 23_000 / max(gw0, 1), 3_000_000 / max(val0, 1))
        if abs(f - 1) > 0.05:  # 싼 상품(수지·식품)은 물량을 줄이고, 비싼 소형 부품은 늘린다
            lines = [(g, pu, max(1, round(k * f)) if g[8] != "CASES" else min(max(1, round(k * f)), 40), v, b)
                     for g, pu, k, v, b in lines]
    else:
        for b, g in enumerate(goods):
            price_usd = r.uniform(*g[4])
            pkgs = max(1, round(target * r.uniform(0.4, 1.6) / (price_usd * g[5])))
            if g[8] in ("CASES",):
                pkgs = min(pkgs, r.randint(4, 30))
            lines.append((g, price_usd, pkgs, "", b))
    items, used_models = [], set()
    for g, price_usd, pkgs, var, b in lines:
        std, trade, hs, unit, (lo, hi), upc, net_pkg, cbm_pkg, pkg, model, duty = g
        price = Decimal(str(price_usd)) * fx
        price = price.quantize(Decimal("0.0001") if (price < 1 and cur != "JPY") else Decimal("0.01"), ROUND_HALF_UP)
        qty = pkgs * upc
        amount = (price * qty).quantize(q, ROUND_HALF_UP)
        net = round(net_pkg * pkgs, 2)
        tare = {"CTNS": 0.08, "CASES": 0.25, "ROLLS": 0.02, "BAGS": 0.01, "DRUMS": 0.07}[pkg]
        gross = round(net * (1 + tare), 2)
        rr = rv if many else r
        while True:
            mdl = f"{model}-{rr.randint(100, 999)}{rr.choice(['', 'A', 'B', 'S'])}"
            if mdl not in used_models:
                break
        used_models.add(mdl)
        items.append({"std": std, "trade": trade + (f", {var}" if var else ""), "base_trade": trade, "base": b, "var": var,
                      "hs": hs, "unit": unit, "price": price, "qty": qty, "amount": amount,
                      "pkgs": pkgs, "pkg": pkg, "net": Decimal(str(net)), "gross": Decimal(str(gross)),
                      "cbm": Decimal(str(round(cbm_pkg * pkgs, 3))), "model": mdl, "duty": duty, "cont": None})
    total = sum((it["amount"] for it in items), Decimal(0))
    total_pkgs = sum(it["pkgs"] for it in items)
    pkg_types = {it["pkg"] for it in items}
    pkg_unit = pkg_types.pop() if len(pkg_types) == 1 else "PKGS"
    net = sum((it["net"] for it in items), Decimal(0))
    gross = sum((it["gross"] for it in items), Decimal(0))
    cbm = sum((it["cbm"] for it in items), Decimal(0))
    if cbm <= 28 and gross <= 21000:
        ctype, ncont = "20'GP", 1
    else:
        ctype, ncont = "40'HC", max(1, math.ceil(float(cbm) / 65), math.ceil(float(gross) / 26000))
    carrier, scac, prefix = r.choice(_CARRIERS)
    containers = [{"no": f"{prefix}{r.randint(1000000, 9999999)}", "seal": f"{r.choice(['KR', 'SL', 'H'])}{r.randint(100000, 999999)}",
                   "type": ctype} for _ in range(ncont)]
    for c, st in zip(containers, _alloc_containers(items, ncont, rv)):
        c.update(st)
    corp_short = _short_name(corp.name_en)
    mid = None
    if triangular and direction == "import":
        cands = [m for m in _INTERMEDIARIES if m[2] != cp["country"]]
        nm, ad, ctry, miso, mbank, mswift = rv.choice(cands)
        mid = {"name": nm, "address": f"{ad}", "country": ctry, "iso": miso, "bank": mbank, "swift": mswift,
               "account": f"{rv.randint(100, 999)}-{rv.randint(100000, 999999)}-{rv.randint(100, 999)}"}
    if direction == "import":
        shipper = {"name": cp["name"], "address": cp["address"] + ", " + cp["country"]}
        consignee = {"name": corp.name_en.upper(), "address": _addr_en(corp.address).upper()}
        mark_name, mark_dest = corp_short, pod
    else:
        shipper = {"name": corp.name_en.upper(), "address": _addr_en(corp.address).upper()}
        consignee = {"name": cp["name"], "address": cp["address"] + ", " + cp["country"]}
        mark_name, mark_dest = cp["name"].split()[0].upper(), pod
    # 송장 발행인(판매자): 중계무역이면 제3국 무역회사, 실제 선적인(B/L Shipper)은 제조사
    seller = {"name": mid["name"].upper(), "address": mid["address"].upper()} if mid else shipper
    origin = cp["country"] if direction == "import" else "KOREA"
    lc = "L/C" in payment
    yy, mm = inv_date.year % 100, inv_date.month
    kbank, kswift = _BANK_EN.get(p.bank, (p.bank, ""))
    if lc:
        if direction == "import":
            lc_no = f"M{r.randint(1000, 9999)}{yy:02d}{mm:02d}{'NS' if 'SIGHT' in payment else 'NU'}{r.randint(10000, 99999)}"
            lc_bank = kbank
        else:
            lc_no = f"{iso}LC{yy:02d}{r.randint(100000, 999999)}"
            lc_bank = cp["bank"].upper()
        lc_date = contract_date + timedelta(days=r.randint(5, 15))
    inv_src = mid["name"] if mid else cp["name"]
    inv_prefix = (corp_short[:3] if direction == "export" else "".join(w[0] for w in inv_src.split()[:3])).upper()
    lots = lot = None
    if split:  # 분할선적: 계약 물량을 2~3회로 나눠 싣고, 이번 서류는 그중 한 회차
        lots = rv.choice([2, 2, 3])
        lot = rv.randint(1, lots)
    return {
        "direction": direction, "cp": cp, "iso": iso, "cur": cur, "corp": corp,
        "shipper": shipper, "consignee": consignee, "seller": seller, "intermediary": mid,
        "pol": pol, "pod": pod, "arrival": arrival,
        "on_board": on_board, "inv_date": inv_date, "contract_date": contract_date, "incoterm": incoterm,
        "incoterm_place": pol if incoterm in ("FOB", "FCA") else pod, "payment": payment,
        "items": items, "total": total, "total_pkgs": total_pkgs, "pkg_unit": pkg_unit,
        "net": net, "gross": gross, "cbm": cbm, "containers": containers, "carrier": carrier, "scac": scac,
        "vessel": r.choice(_VESSELS), "voyage": f"{r.randint(1, 160):03d}{'E' if direction == 'export' and iso == 'US' else r.choice('NSEW')}",
        "bl_no": f"{scac}{r.choice(['', 'KR', iso])}{r.randint(10000000, 99999999)}",
        "booking_no": f"{r.choice(['BKG', scac])}{r.randint(1000000, 9999999)}",
        "inv_no": f"{inv_prefix}-{yy:02d}{mm:02d}-{r.randint(1, 250):03d}",
        "contract_no": f"{inv_prefix}-SC-{yy:02d}{r.randint(100, 999)}",
        "lc_no": lc_no if lc else None, "lc_date": lc_date if lc else None, "lc_bank": lc_bank if lc else None,
        "kbank": kbank, "kswift": kswift,
        "marks": f"{mark_name}\n{mark_dest}\nC/NO. 1-{total_pkgs}\nMADE IN {origin}",
        "origin": origin, "forwarder": r.choice(_FORWARDERS),
        "freight_prepaid": incoterm in ("CIF", "CFR"),
        "signer": (rv.choice(["David Wong", "Grace Lim", "Kelvin Tan", "Michelle Chan"]) if mid
                   else cp["contact"] if direction == "import" else p.person.name_en.title()),
        "category": cat, "heavy": many, "lots": lots, "lot": lot,
    }


def _short_name(name_en: str) -> str:
    return name_en.split()[0].upper()


def _party(s: dict, who: str) -> dict:
    return {"name": s[who]["name"], "address": s[who]["address"]}


def _goods_rows(s: dict, mult: int = 1) -> list[dict]:
    """품목 줄. mult: 분할선적 계약서처럼 계약 전체 물량(회차 수 배)을 보일 때."""
    cur = s["cur"]
    rows = []
    for it in s["items"]:
        qty, amount = it["qty"] * mult, (it["amount"] * mult).quantize(_dec(cur))
        rows.append({"description": it["trade"], "model": it["model"], "quantity": f"{qty:,} {it['unit']}",
                     "unit_price": f"{cur} {_price_str(it['price'], cur)}", "amount": f"{cur} {_money(amount, cur)}"})
    return rows


def _en(d: date, rng: random.Random) -> str:
    return D(d, rng.choice(["en", "en_long"]))


def _ordinal(n: int) -> str:
    return {1: "1ST", 2: "2ND", 3: "3RD"}.get(n, f"{n}TH")


def _remarks(s: dict, rng: random.Random, out: dict) -> None:
    """송장·포장명세서 비고란: 분할선적 회차, 계약번호, 중계무역(실제 선적인·대금 수취 은행)."""
    if s["lots"]:
        out["partial_shipment"] = f"{_ordinal(s['lot'])} LOT OF {s['lots']} LOTS"
    if s["lots"] or s["intermediary"] or rng.random() < 0.35:
        out["contract_no"] = s["contract_no"]
    mid = s["intermediary"]
    if mid:
        out["manufacturer"] = {"name": s["shipper"]["name"], "address": s["shipper"]["address"]}


class _Out(dict):
    """서류 데이터 + 템플릿 전용 표시 옵션 `.opt` (정답이 아님: 어느 줄을 손으로 고쳤는지, 부속 목록을 붙일지 등)."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.opt = {}


# ---------------------------------------------------------------------------
# COMMERCIAL INVOICE
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# SALES CONTRACT
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# BILL OF LADING
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# PACKING LIST
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 유학: 입학허가서 / 학비 청구서
# ---------------------------------------------------------------------------
# (대학명, 주소, 국가, 통화, 은행, SWIFT, 라우팅 라벨, 학기제)
_UNIVERSITIES = [
    ("Northbridge University", "300 College Ave, Boston, MA 02115, USA", "US", "USD", "JPMorgan Chase Bank, N.A.", "CHASUS33", "ABA Routing No."),
    ("Westlake State University", "1800 Lakeview Dr, Seattle, WA 98105, USA", "US", "USD", "Bank of America, N.A.", "BOFAUS3N", "ABA Routing No."),
    ("Pacific Coast University", "5500 Ocean View Blvd, San Diego, CA 92122, USA", "US", "USD", "Wells Fargo Bank, N.A.", "WFBIUS6S", "ABA Routing No."),
    ("Lakeshore College of Arts and Sciences", "900 N Lake Shore Dr, Chicago, IL 60611, USA", "US", "USD", "Citibank, N.A.", "CITIUS33", "ABA Routing No."),
    ("University of Eastwood", "12 Kingsway, London WC2B 6XF, United Kingdom", "UK", "GBP", "Barclays Bank PLC", "BARCGB22", "Sort Code"),
    ("Maple Ridge University", "250 University Ave, Toronto, ON M5H 3E5, Canada", "CA", "CAD", "Royal Bank of Canada", "ROYCCAT2", "Transit No."),
    ("Southern Cross Institute of Technology", "45 Broadway, Ultimo NSW 2007, Australia", "AU", "AUD", "Commonwealth Bank of Australia", "CTBAAU2S", "BSB"),
]
_PROGRAMS = {
    "bachelor": [("Business Administration", "Bachelor of Science (B.S.)"), ("Computer Science", "Bachelor of Science (B.S.)"),
                 ("Economics", "Bachelor of Arts (B.A.)"), ("Psychology", "Bachelor of Arts (B.A.)"),
                 ("Mechanical Engineering", "Bachelor of Engineering (B.Eng.)"), ("Communication Design", "Bachelor of Fine Arts (B.F.A.)")],
    "master": [("Business Administration", "Master of Business Administration (MBA)"), ("Data Science", "Master of Science (M.S.)"),
               ("Finance", "Master of Science in Finance (MSF)"), ("Public Policy", "Master of Public Policy (MPP)"),
               ("Electrical and Computer Engineering", "Master of Science (M.S.)"), ("Education", "Master of Education (M.Ed.)")],
    "phd": [("Chemistry", "Doctor of Philosophy (Ph.D.)"), ("Computer Science", "Doctor of Philosophy (Ph.D.)"),
            ("Economics", "Doctor of Philosophy (Ph.D.)")],
}


def _study(p: Profile) -> dict:
    r = random.Random(f"study:{p.seed}")
    student = p.person
    for c in p.children:
        if 17 <= c.age <= 30:
            student = c
            break
    if "University" in p.foreign.name:
        uni = next(u for u in _UNIVERSITIES if u[0] == p.foreign.name)
    else:
        uni = r.choice(_UNIVERSITIES)
    name, addr, cc, cur, bank, swift, routing_label = uni
    age = student.age
    level = "bachelor" if age <= 21 else r.choice(["master", "master", "phd"]) if age <= 32 else "master"
    program, degree = r.choice(_PROGRAMS[level])
    years = {"bachelor": 4, "master": r.choice([1, 2, 2]), "phd": 5}[level]
    # 다음 학기 시작일
    t = p.issue_date
    if cc == "AU":
        start = date(t.year, 7, 22) if t.month < 6 else date(t.year + 1, 2, 24)
        term = ("Semester 2" if start.month == 7 else "Semester 1") + f", {start.year}"
    elif t.month <= 6:
        start = date(t.year, 8 if cc == "US" else 9, r.randint(18, 28))
        term = f"{'Fall' if cc != 'UK' else 'Autumn'} {start.year}"
    else:
        start = date(t.year + 1, 1, r.randint(8, 20))
        term = f"{'Spring' if cc != 'UK' else 'Winter'} {start.year}"
    letter_date = t - timedelta(days=r.randint(20, 90))
    tuition_scale = {"USD": 1, "GBP": 0.62, "CAD": 1.1, "AUD": 1.25}[cur]
    tuition = K.round_to(r.uniform(14000, 32000) * tuition_scale, 10)
    routing = {"ABA Routing No.": f"0{r.randint(10000000, 99999999)}", "Sort Code": f"{r.randint(10, 99)}-{r.randint(10, 99)}-{r.randint(10, 99)}",
               "Transit No.": f"{r.randint(10000, 99999)}-003", "BSB": f"062-{r.randint(100, 999)}"}[routing_label]
    out = {
        "student": student, "uni": name, "uni_addr": addr, "cc": cc, "cur": cur, "bank": bank, "swift": swift,
        "routing_label": routing_label, "routing": routing, "account": "".join(str(r.randint(0, 9)) for _ in range(r.choice([9, 10, 12]))),
        "level": level, "program": program, "degree": degree, "years": years, "start": start, "term": term,
        "letter_date": letter_date, "student_id": f"{r.choice('NWPLUM')}{r.randint(10, 99)}{r.randint(100000, 999999)}",
        "tuition": tuition, "director": r.choice(["Jennifer A. Collins", "Robert M. Hayes", "Emily R. Watson", "David L. Morgan", "Susan K. Patel"]),
        # 실제 대학 도메인(머리글자)과 겹치지 않도록 이름 전체로 만든다: westlakestate.edu
        "domain": "".join(w for w in name.split() if w not in ("University", "of", "and", "College", "Institute")).lower()
                  + {"US": ".edu", "UK": ".ac.uk", "CA": ".ca", "AU": ".edu.au"}[cc],
        "housing": r.random() < 0.6,
        "scholarship": None, "conditions": None, "deferred_from": None,
    }
    # 프로필 단위 특수 상황 (입학허가서와 학비 청구서가 맞도록): 장학금, 조건부 입학, 입학 연기
    rv = random.Random(f"studyv:{p.seed}")
    if special(rv, "scholarship", 0.25):
        nm = rv.choice(["International Merit Scholarship", "Dean's Scholarship", "Global Excellence Scholarship",
                        "Presidential Scholarship", "International Student Award"])
        if level == "phd" and rv.random() < 0.6:
            nm = "Graduate Tuition Fellowship"
        out["scholarship"] = {"name": nm, "amount": K.round_to(tuition * rv.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.5]), 10)}
    if special(rv, "conditional", 0.15):
        conds = []
        if cc in ("UK", "AU") and rv.random() < 0.5:
            conds.append("Successful completion of the " + rv.choice(["10-week", "6-week", "12-week"])
                         + " Pre-sessional English Programme with an overall grade of 65% or above")
        else:
            conds.append(rv.choice(["Submission of an official IELTS Academic score of overall 6.5 with no band below 6.0, or TOEFL iBT 90 or above",
                                    "Submission of an official TOEFL iBT score of 80 or above (or IELTS Academic 6.5)",
                                    "Submission of an official Duolingo English Test score of 115 or above"]))
        conds.append("Receipt of your official final transcript showing conferral of your bachelor's degree"
                     if level != "bachelor" else "Receipt of your official final high school transcript and diploma")
        if level != "bachelor" and rv.random() < 0.4:
            conds.append("Completion of a prerequisite course in " + rv.choice(["Statistics", "Calculus", "Programming", "Microeconomics"])
                         + " with a grade of B or better before enrollment")
        out["conditions"] = {"items": conds, "deadline": start - timedelta(days=rv.randint(20, 45))}
    if special(rv, "deferred", 0.06):
        out["deferred_from"] = term.replace(str(start.year), str(start.year - 1))
    return out


def _student_name(st: Person) -> str:
    return f"{st.given_en.title()} {st.surname_en.title()}"


_SYM = {"USD": "$", "GBP": "£", "CAD": "CA$", "AUD": "A$"}


def _fm(a: float, cur: str) -> str:
    sym = _SYM[cur]
    return f"-{sym}{abs(a):,.2f}" if a < 0 else f"{sym}{a:,.2f}"


# 이 그룹의 코드 서식. 값 만드는 함수는 서식 폴더 docgen/forms/<ID>/generate.py 에 있다 (여기는 같이 쓰는 도우미).
FORMS = ('commercial_invoice', 'trade_contract', 'bill_of_lading', 'packing_list', 'import_declaration', 'admission_letter', 'tuition_invoice',)
register_folder_forms(__name__, FORMS)   # 예전 @doc 차례 그대로 등록 (서식 목록·데이터셋 순서)
