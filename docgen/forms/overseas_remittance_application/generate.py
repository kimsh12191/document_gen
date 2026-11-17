"""overseas_remittance_application: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/bank_form_account.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.bank_form_account import _bank, _date, _rrn, _staff  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.docs.bank_form_loan import _foreigner, _relative, _solo  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


_BANK_ADDR = {
    "BOFAUS3N": "222 Broadway, New York, NY 10038, U.S.A.",
    "CHASUS33": "383 Madison Avenue, New York, NY 10179, U.S.A.",
    "MHCBJPJT": "1-5-5 Otemachi, Chiyoda-ku, Tokyo 100-8176, Japan",
    "BKCHCNBJ": "1 Fuxingmen Nei Dajie, Xicheng District, Beijing, China",
    "BFTVVNVX": "198 Tran Quang Khai St, Hoan Kiem, Hanoi, Vietnam",
    "DEUTDEDD": "Königsallee 45-47, 40212 Düsseldorf, Germany",
    "DBSSSGSG": "12 Marina Boulevard, Marina Bay Financial Centre, Singapore 018982",
}


# 통화별 (가능 통화, 원화 환율 범위, 환율 단위)
_CCY = {"USD": (1340, 1480, 1), "JPY": (880, 990, 100), "EUR": (1450, 1620, 1), "CNY": (185, 205, 1),
        "SGD": (1000, 1100, 1)}


# 옛 은행 서식(2011~2020)용 연평균 매매기준율 근사값 (원, JPY 는 100엔당)
_CCY_YEAR = {
    "USD": {2011: 1108, 2012: 1127, 2013: 1095, 2014: 1053, 2015: 1132, 2016: 1160, 2017: 1131, 2018: 1100, 2019: 1166, 2020: 1180},
    "JPY": {2011: 1391, 2012: 1413, 2013: 1123, 2014: 996, 2015: 935, 2016: 1068, 2017: 1009, 2018: 997, 2019: 1070, 2020: 1106},
    "EUR": {2011: 1541, 2012: 1448, 2013: 1454, 2014: 1398, 2015: 1256, 2016: 1284, 2017: 1276, 2018: 1299, 2019: 1305, 2020: 1345},
    "CNY": {2011: 171, 2012: 179, 2013: 178, 2014: 171, 2015: 180, 2016: 175, 2017: 167, 2018: 166, 2019: 169, 2020: 171},
    "SGD": {2011: 881, 2012: 902, 2013: 875, 2014: 831, 2015: 823, 2016: 840, 2017: 819, 2018: 816, 2019: 855, 2020: 855},
}


_COUNTRY_CCY = {"UNITED STATES": ["USD"], "JAPAN": ["JPY", "JPY", "USD"], "CHINA": ["USD", "USD", "CNY"],
                "VIETNAM": ["USD"], "GERMANY": ["EUR", "EUR", "USD"], "SINGAPORE": ["USD", "SGD"]}


# 한국은행 지급사유코드(5자리) — 검색으로 확인된 코드만 사용 (JPMorgan Korea payment purpose code list)
#   10101 사전송금방식 통관수입대금, 10103 사후송금방식 통관수입대금, 30101 유학 및 연수
_PURPOSE_CODE = {"유학생경비": "30101"}


def _fx_fee(usd_equiv: float) -> int:
    if usd_equiv <= 500:
        return 5_000
    if usd_equiv <= 2_000:
        return 10_000
    if usd_equiv <= 5_000:
        return 15_000
    return 20_000


@doc("overseas_remittance_application", "해외송금신청서", "bank_form", category="internal")
def overseas_remittance_application(p: Profile, rng: random.Random) -> dict:
    """당발송금(전신송금 T/T) 신청서 + 은행 사용란(환율/원화환산액)."""
    per, fo = p.person, p.foreign
    school = "University" in fo.name
    ccy = "USD" if school else rng.choice(_COUNTRY_CCY.get(fo.country, ["USD"]))
    lo, hi, unit = _CCY[ccy]
    if p.issue_date.year in _CCY_YEAR[ccy]:
        avg = _CCY_YEAR[ccy][p.issue_date.year]
        lo, hi = avg * 0.97, avg * 1.03
    rate = round(rng.uniform(lo, hi), 2)
    if school:
        purpose = "유학생경비"
        amount = rng.randint(180, 480) * 100.0
    else:
        purpose = rng.choices(["수입대금", "기타"], weights=[85, 15])[0]
        usd = rng.uniform(3_000, 150_000)
        amount = usd * 1350 / (rate / unit)
    if ccy == "JPY":
        amount = float(K.round_to(amount, 1000))
        amt_str = f"{int(amount):,}"
    else:
        amount = round(amount, 2) if not school else amount
        amt_str = f"{amount:,.2f}"
    krw = int(round(amount * rate / unit))
    fee = _fx_fee(krw / 1350)
    cable = 8_000
    yy = p.issue_date
    if school:
        message = f"TUITION FEE {yy.year} {rng.choice(['FALL', 'SPRING'])} / ID {rng.randint(10_000_000, 99_999_999)}"
        documents = "입학허가서(I-20), 등록금 납부고지서"
    elif purpose == "수입대금":
        message = f"INVOICE NO. {fo.name.split()[0][:3].upper()}-{yy.year}-{rng.randint(1, 999):04d}"
        documents = rng.choice(["Commercial Invoice, 수입계약서", "Commercial Invoice, B/L 사본", "Proforma Invoice"])
        code = "10101" if documents.startswith("Proforma") else "10103"
    else:
        message = f"SERVICE FEE CONTRACT {rng.randint(100, 999)}"
        documents = "용역계약서, Invoice"
    remittance = {
        "currency": ccy,
        "amount": amt_str,
        "purpose": purpose,
        "charge": rng.choices(["SHA", "OUR", "BEN"], weights=[60, 30, 10])[0],
        "method": "전신송금(T/T)",
        "message": message,
        "documents": documents,
    }
    if purpose == "수입대금":
        remittance["purpose_code"] = code
    elif purpose in _PURPOSE_CODE:
        remittance["purpose_code"] = _PURPOSE_CODE[purpose]
    remitter = {"name": per.name, "name_en": per.name_en, "rrn": _rrn(p, rng),
                "address": per.address.road_full, "phone": per.mobile}
    if purpose == "수입대금":
        remitter["company"] = f"{p.business.name} ({p.business.biz_no})"
    data = {
        "bank": _bank(p),
        "remitter": remitter,
        "beneficiary": {
            "name": fo.name, "address": fo.address, "country": fo.country, "account_no": fo.account,
            "relationship": "교육기관(학비 납부)" if school else "거래처",
            "bank_name": fo.bank, "swift": fo.swift, "bank_address": _BANK_ADDR.get(fo.swift, fo.country),
        },
        "remittance": remittance,
        "date": _date(p, rng),
        "signature": per.name,
        "bank_use": {
            "ref_no": f"OR{yy:%y%m%d}{rng.randint(0, 99999):05d}",
            "rate": f"{rate:,.2f}",
            "krw_amount": won(krw),
            "fee": won(fee),
            "cable_fee": won(cable),
            "total": won(krw + fee + cable),
            "branch": p.bank_branch,
            **_staff(rng),
        },
    }
    _remit_variants(p, rng, data, school)
    return data


# 외국인 근로자 본국 송금용 수취은행 (국가: 은행명, SWIFT, 통화)
_HOME_BANKS = {
    "VIETNAM": ("JOINT STOCK COMMERCIAL BANK FOR FOREIGN TRADE OF VIETNAM", "BFTVVNVX", "USD"),
    "CHINA": ("BANK OF CHINA", "BKCHCNBJ", "CNY"),
    "PHILIPPINES": ("BDO UNIBANK, INC.", "BNORPHMM", "USD"),
    "INDONESIA": ("PT BANK NEGARA INDONESIA (PERSERO) TBK", "BNINIDJA", "USD"),
    "THAILAND": ("KASIKORNBANK PUBLIC COMPANY LIMITED", "KASITHBK", "USD"),
    "UZBEKISTAN": ("NATIONAL BANK OF UZBEKISTAN", "NBFAUZ2X", "USD"),
    "MONGOLIA": ("KHAN BANK", "AGMOMNUB", "USD"),
}


_HOME_CITY = {"VIETNAM": "HANOI", "CHINA": "QINGDAO", "PHILIPPINES": "MANILA", "INDONESIA": "JAKARTA",
              "THAILAND": "BANGKOK", "UZBEKISTAN": "TASHKENT", "MONGOLIA": "ULAANBAATAR"}


_HOME_GIVEN = {"VIETNAM": ["THI MAI", "VAN HUNG", "THI LAN", "VAN NAM"], "CHINA": ["MING", "XIU YING", "JUN", "FANG"],
               "PHILIPPINES": ["ROSA", "JOSE", "ANGELICA", "MARK"], "INDONESIA": ["DEWI", "BUDI", "AGUS", "SRI"],
               "THAILAND": ["ANAN", "MALEE", "SOMSAK", "NOK"], "UZBEKISTAN": ["DILNOZA", "BEKZOD", "SHAHNOZA", "RUSTAM"],
               "MONGOLIA": ["TUYA", "BOLD", "SARNAI", "GANZORIG"]}


_BATCH_PARTIES = [
    ("SHENZHEN HUAXIN ELECTRONICS CO., LTD.", "CHINA", "BANK OF CHINA SHENZHEN BRANCH", "BKCHCNBJ45A"),
    ("NINGBO OCEAN TRADING CO., LTD.", "CHINA", "INDUSTRIAL AND COMMERCIAL BANK OF CHINA", "ICBKCNBJNBO"),
    ("SAIGON TEXTILE JSC", "VIETNAM", "VIETCOMBANK HO CHI MINH", "BFTVVNVX007"),
    ("OSAKA PRECISION PARTS K.K.", "JAPAN", "MUFG BANK, LTD.", "BOTKJPJT"),
    ("TOKYO MATERIALS CO., LTD.", "JAPAN", "MIZUHO BANK, LTD.", "MHCBJPJT"),
    ("PACIFIC SUPPLY INC.", "UNITED STATES", "BANK OF AMERICA, N.A.", "BOFAUS3N"),
    ("WEST COAST LOGISTICS LLC", "UNITED STATES", "JPMORGAN CHASE BANK, N.A.", "CHASUS33"),
    ("RHEIN MASCHINENBAU GMBH", "GERMANY", "DEUTSCHE BANK AG", "DEUTDEDD"),
    ("LION CITY COMPONENTS PTE. LTD.", "SINGAPORE", "DBS BANK LTD.", "DBSSSGSG"),
    ("BANGKOK PACKAGING CO., LTD.", "THAILAND", "BANGKOK BANK PCL", "BKKBTHBK"),
    ("MANILA AGRI EXPORTS CORP.", "PHILIPPINES", "BDO UNIBANK, INC.", "BNORPHMM"),
]


def _remit_variants(p: Profile, rng: random.Random, data: dict, school: bool) -> None:
    """해외송금신청서 변형: 여러 건 일괄 송금(별지, 여러 쪽), 외국인 근로자 본국 송금, 대리인, 공란."""
    if not school and heavy(rng, 0.2):  # 거래처 여러 곳에 한 번에 송금 → 별지 송금명세
        rows = []
        for name, country, bank, swift in rng.sample(_BATCH_PARTIES, rng.randint(6, 11)):
            cur = {"JAPAN": "JPY", "GERMANY": "EUR"}.get(country, "USD")
            amt = rng.uniform(2_000, 60_000)
            rows.append({"beneficiary": name, "country": country, "bank": f"{bank} ({swift})",
                         "account_no": "".join(str(rng.randint(0, 9)) for _ in range(rng.choice([10, 12, 14]))),
                         "currency": cur,
                         "amount": f"{int(K.round_to(amt * 140, 1000)):,}" if cur == "JPY" else f"{amt:,.2f}",
                         "message": f"INV {rng.choice(['NO.', ''])}{rng.randint(1000, 9999)}"})
        data["batch"] = rows
        data["batch_count"] = f"{len(rows) + 1}건"
    if _solo(p) and special(rng, "foreign_worker", 0.12):  # 외국인 근로자의 국내 보수 본국 송금
        fo = _foreigner(p, rng, (23, 45), nations=_HOME_BANKS)
        country = fo["nationality_en"]
        bank, swift, cur = _HOME_BANKS[country]
        rel = rng.choice(["배우자", "부", "모", "본인"])
        if rel == "본인":
            bname = fo["name_en"]
        else:
            bname = f"{fo['surname_en']} {rng.choice(_HOME_GIVEN[country])}"
        data["remitter"] = {"name": fo["name"], "name_en": fo["name_en"], "rrn": fo["arc_no"],
                            "address": p.person.address.road_full, "phone": fo["mobile"]}
        data["signature"] = fo["name"]
        data["beneficiary"] = {"name": bname, "address": f"{_HOME_CITY[country]}, {country}", "country": country,
                               "account_no": "".join(str(rng.randint(0, 9)) for _ in range(rng.choice([10, 12, 13]))),
                               "relationship": "본인 명의 본국 계좌" if rel == "본인" else f"가족({rel})",
                               "bank_name": bank, "swift": swift, "bank_address": f"{_HOME_CITY[country]}, {country}"}
        amt = float(rng.randint(50, 250) * 100) if cur == "CNY" else rng.randint(8, 40) * 100.0
        lo, hi, _ = _CCY[cur]
        if p.issue_date.year in _CCY_YEAR[cur]:
            avg = _CCY_YEAR[cur][p.issue_date.year]
            lo, hi = avg * 0.97, avg * 1.03
        rate = round(rng.uniform(lo, hi), 2)
        krw = int(round(amt * rate))
        data["remittance"] = {"currency": cur, "amount": f"{amt:,.2f}", "purpose": "국내보수송금", "charge": "OUR",
                              "method": "전신송금(T/T)", "message": rng.choice(["FAMILY SUPPORT", "SALARY", "FOR FAMILY"]),
                              "documents": "근로계약서, 급여명세서(소득증빙)"}
        data["bank_use"].update({"rate": f"{rate:,.2f}", "krw_amount": won(krw), "fee": won(_fx_fee(krw / 1350)),
                                 "total": won(krw + _fx_fee(krw / 1350) + 8_000)})
        data.pop("batch", None)
        data.pop("batch_count", None)
    elif special(rng, "agent", 0.08):  # 가족이 대리 신청 (위임장 첨부)
        ag, rel = _relative(p, rng)
        data["agent"] = {"name": ag.name, "rrn": K.mask_rrn(ag.rrn), "relation": rel, "phone": ag.mobile}
    if special(rng, "sparse", 0.1):  # 선택 기재란 공란
        for k in rng.sample(["relationship", "address"], rng.randint(1, 2)):
            data["beneficiary"][k] = None
