"""부동산 관련 서류: 등기사항전부증명서, 건축물대장, 토지대장, 매매계약서, 임대차계약서, 전입세대확인서.

같은 프로필이면 서류 사이의 사실관계(매매일, 근저당, 소유권 이전 여부 등)가 맞도록
`_facts(p)`가 프로필 seed 로부터 결정론적으로 공통 사실을 만든다.
매도인 = p.property.seller (기존 소유자), 매수인/임차인 = p.person.
"""
import re

from ..registry import doc
from ._common import *  # noqa: F401,F403

# 은행 등기명의 (근저당권자 표시용)
_BANK_LEGAL = {
    "국민은행": ("주식회사국민은행", "서울특별시 영등포구 국제금융로8길 26"),
    "신한은행": ("주식회사신한은행", "서울특별시 중구 세종대로9길 20"),
    "우리은행": ("주식회사우리은행", "서울특별시 중구 소공로 51"),
    "하나은행": ("주식회사하나은행", "서울특별시 중구 을지로 35"),
    "농협은행": ("농협은행주식회사", "서울특별시 중구 통일로 120"),
    "기업은행": ("중소기업은행", "서울특별시 중구 을지로 79"),
    "SC제일은행": ("주식회사한국스탠다드차타드은행", "서울특별시 종로구 종로 47"),
    "부산은행": ("주식회사부산은행", "부산광역시 남구 문현금융로 30"),
    "iM뱅크": ("주식회사 아이엠뱅크", "대구광역시 수성구 달구벌대로 2310"),
}
_DEVELOPERS = ["대림", "삼호", "한양", "동아", "금호", "우방", "태영", "신동아", "동부", "한라", "벽산", "쌍용", "경남", "코오롱"]
_SIDO_CODE = {"서울특별시": "11", "부산광역시": "26", "대구광역시": "27", "인천광역시": "28", "광주광역시": "29",
              "대전광역시": "30", "울산광역시": "31", "세종특별자치시": "36", "경기도": "41", "강원특별자치도": "51",
              "충청북도": "43", "충청남도": "44", "전북특별자치도": "52", "전라남도": "46", "경상북도": "47",
              "경상남도": "48", "제주특별자치도": "50"}


def _rd(d: date) -> str:
    """등기부식 날짜: 2015년3월2일"""
    return f"{d.year}년{d.month}월{d.day}일"


def _mask_name(name: str) -> str:
    """홍길동 -> 홍*동, 김민 -> 김*, 남궁민수 -> 남**수"""
    if len(name) <= 2:
        return name[0] + "*"
    return name[0] + "*" * (len(name) - 2) + name[-1]


def _bank_legal(bank: str) -> tuple[str, str, str]:
    name, addr = _BANK_LEGAL.get(bank, (f"주식회사{bank}", "서울특별시 중구 세종대로 39"))
    return name, K.corp_reg_no(random.Random(f"bank:{bank}")), addr


def _area(x: float) -> str:
    return f"{x:,.2f}".rstrip("0").rstrip(".") if x != int(x) else f"{int(x):,}"


def _rand_person(rng: random.Random, gender=None) -> str:
    return K.make_name(rng, gender or rng.choice("MF"))[0]


def _facts(p: Profile) -> dict:
    """부동산 서류들이 공유하는 사실관계 (프로필 seed 기준 결정론적)."""
    r = random.Random(f"real_estate:{p.seed}")
    pr = p.property
    a = pr.address
    m = re.match(r"(?:(\d+)동\s*)?(\d+)호", a.detail or "")
    dong_no, ho = (m.group(1), m.group(2)) if m else (None, f"{pr.floor}0{r.randint(1, 4)}")
    floor = max(1, int(ho) // 100)
    total_floors = max(pr.total_floors, floor + r.randint(0, 3))
    stem = a.dong[:-1] if a.dong.endswith("동") else a.dong
    fallback = ["오피스텔", "타워", "시티", "스테이"] if pr.kind == "오피스텔" else ["빌라", "하이츠", "맨션", "그린빌"]
    bname = a.building_name or stem + r.choice(fallback)
    is_apt = pr.kind == "아파트"
    usage = {"아파트": "아파트", "오피스텔": "오피스텔", "다세대주택": "다세대주택"}[pr.kind]
    usage_full = {"아파트": "공동주택(아파트)", "오피스텔": "업무시설(오피스텔)", "다세대주택": "공동주택(다세대주택)"}[pr.kind]
    completed = pr.completed
    preserve = completed + timedelta(days=r.randint(15, 70))
    lo = max(preserve + timedelta(days=60), date(pr.seller.birth.year + 26, 1, 1))
    hi = max(lo + timedelta(days=30), p.issue_date - timedelta(days=900))
    seller_acq = rand_date(r, lo, hi)
    transferred = r.random() < 0.35
    if p.extra.get("loan_kind") == "jeonse":  # 전세 시나리오: 고객은 세입자이므로 소유권이 넘어오지 않는다
        transferred = False
    if transferred:
        contract = p.issue_date - timedelta(days=r.randint(95, 150))
        balance = contract + timedelta(days=r.randint(40, 75))
    else:
        contract = p.issue_date - timedelta(days=r.randint(3, 30))
        balance = contract + timedelta(days=r.randint(45, 90))
    middle = contract + timedelta(days=r.randint(20, 35)) if r.random() < 0.5 else None
    price = pr.price
    down = K.round_to(price * 0.1, 1_000_000)
    middle_amt = K.round_to(price * r.uniform(0.2, 0.4), 10_000_000) if middle else 0
    seller_price = K.round_to(price * r.uniform(0.55, 0.9), 10_000_000)
    seller_mort = None
    if r.random() < 0.7:
        bank = r.choice(list(_BANK_LEGAL))
        loan = K.round_to(seller_price * r.uniform(0.3, 0.6), 1_000_000)
        seller_mort = {"bank": bank, "branch": f"{r.choice(['역삼', '서초', '잠실', '목동', '분당', '일산', '해운대', '수성', '둔산', '광교'])}지점",
                       "max": int(loan * r.choice([1.2, 1.2, 1.3])), "date": seller_acq, "no": r.randint(10000, 99999)}
    buyer_loan = K.round_to(price * r.uniform(0.4, 0.7), 1_000_000)
    units_per_floor = r.choice([2, 2, 4, 4, 6]) if is_apt else r.choice([2, 3, 4])
    floor_area = round(pr.exclusive_area * r.uniform(1.25, 1.4) * units_per_floor, 2)
    if is_apt:
        land_total = round(r.uniform(9000, 60000), 1)
        dev = f"주식회사{r.choice(_DEVELOPERS)}{r.choice(['건설', '산업개발', '종합건설'])}"
        dev_no = K.corp_reg_no(r)
    else:
        land_total = round(max(pr.land_area * units_per_floor * total_floors * r.uniform(1.0, 1.3), 180), 1)
        dev = _rand_person(r)
        dev_no = K.mask_rrn(K.rrn(r, rand_date(r, date(1950, 1, 1), date(1975, 12, 31)), "M"), keep=0)
    seller_resident = r.random() < 0.6
    seller_addr = a.road_full if seller_resident else pr.seller.address.road_full
    jibun = a.jibun.split("-")
    return {
        "a": a, "pr": pr, "dong_no": dong_no, "ho": ho, "floor": floor, "total_floors": total_floors,
        "bname": bname, "is_apt": is_apt, "usage": usage, "usage_full": usage_full,
        "preserve": preserve, "preserve_no": r.randint(10000, 99999), "seller_acq": seller_acq,
        "seller_acq_no": r.randint(10000, 99999), "transferred": transferred, "contract": contract,
        "middle": middle, "balance": balance, "price": price, "down": down, "middle_amt": middle_amt,
        "balance_amt": price - down - middle_amt, "seller_price": seller_price, "seller_mort": seller_mort,
        "buyer_loan": buyer_loan, "buyer_max": int(buyer_loan * r.choice([1.2, 1.2, 1.1])),
        "buyer_no": r.randint(10000, 99999), "floor_area": floor_area, "land_total": land_total,
        "dev": dev, "dev_no": dev_no, "dev_addr": f"{a.region} {r.choice(['중앙로', '대학로', '시청로'])} {r.randint(1, 200)}",
        "seller_resident": seller_resident, "seller_addr": seller_addr,
        "units": r.randint(280, 2400) if is_apt else units_per_floor * total_floors,
        "bonbun": int(jibun[0]), "bubun": int(jibun[1]) if len(jibun) > 1 else 0,
        "dong_code": f"{_SIDO_CODE[a.sido]}{r.randint(110, 890)}{r.randint(101, 140)}00",
        "drawing_no": f"도면편철장 제{r.randint(1, 9)}책 제{r.randint(1, 900)}장",
        "land_right_date": preserve - timedelta(days=r.randint(3, 20)),
        "road_reg": date(2012, r.randint(1, 12), r.randint(1, 28)) if completed.year < 2011 else None,
        "land_grade": r.randint(120, 260),
        "zoning": r.choice(["제2종일반주거지역", "제3종일반주거지역", "제3종일반주거지역", "준주거지역", "제2종일반주거지역(7층이하)"]),
    }


def _unit_label(f: dict) -> str:
    """'래미안아파트 제101동 제12층 제1203호'"""
    s = f["bname"]
    if f["dong_no"]:
        s += f" 제{f['dong_no']}동"
    return f"{s} 제{f['floor']}층 제{f['ho']}호"


def _brokers(rng: random.Random, f: dict) -> list[dict]:
    """개업공인중개사 (공동중개면 매도인측·매수인측 2곳)."""
    out = [_broker(rng, f)]
    if rng.random() < 0.35:
        out.append(_broker(rng, f, other=True))
    for b in out:
        if rng.random() < 0.3:
            b["assistant"] = _rand_person(rng)
    return out


def _broker(rng: random.Random, f: dict, other: bool = False) -> dict:
    a = f["a"]
    stem = (a.dong[:-1] if a.dong.endswith("동") else a.dong) + rng.choice(["", "역", "중앙", "제일", "행복", "명문"]) if other else f["bname"][:rng.choice([2, 3])]
    office_name = f"{stem}{rng.choice(['공인중개사사무소', '부동산중개', '공인중개사', '부동산공인중개사사무소'])}"
    return {
        "office_address": f"{a.region} {a.road} {rng.randint(1, 400)}, 1층 {rng.randint(101, 112)}호 ({a.dong})",
        "office_name": office_name,
        "representative": _rand_person(rng),
        "reg_no": f"{rng.randint(11110, 48890)}-{rng.randint(2008, 2023)}-{rng.randint(1, 3000):05d}",
        "phone": K.landline(rng, a.sido),
    }


# ---------------------------------------------------------------------------
# 등기사항전부증명서 (집합건물)
# ---------------------------------------------------------------------------

@doc("real_estate_registry", "등기사항전부증명서(집합건물)", "real_estate")
def real_estate_registry(p: Profile, rng: random.Random) -> dict:
    """등기사항전부증명서(말소사항 포함) - 집합건물. 표제부·갑구·을구."""
    f = _facts(p)
    a, pr, seller = f["a"], f["pr"], f["pr"].seller
    view_dt = p.issue_date
    loc = f"{a.jibun_full} {f['bname']}" + (f" 제{f['dong_no']}동" if f["dong_no"] else "")
    loc += f"\n[도로명주소]\n{a.region} {a.road} {a.building_no}"
    nf = f["total_floors"]
    under = rng.random() < 0.7
    area1 = round(f["floor_area"] * rng.uniform(0.75, 0.95), 2)
    detail = (f"{pr.structure}\n(철근)콘크리트지붕 {nf}층 {f['usage_full']}\n"
              + (f"지하1층 {_area(round(f['floor_area'] * rng.uniform(0.6, 1.1), 2))}㎡\n" if under else "")
              + f"1층 {_area(area1)}㎡\n"
              + (f"2층 {_area(f['floor_area'])}㎡" if nf <= 2 else f"2층~{nf}층 각 {_area(f['floor_area'])}㎡"))
    loc_old = f"{a.jibun_full} {f['bname']}" + (f" 제{f['dong_no']}동" if f["dong_no"] else "")
    buildings = [{"display_no": "1", "receipt": _rd(f["preserve"]),
                  "location": loc_old if f["road_reg"] else loc, "detail": detail, "cause": f["drawing_no"]}]
    if f["road_reg"]:  # 도로명주소 직권 등기: 1번은 말소(실선), 2번에 도로명주소 추가
        buildings.append({"display_no": "2", "location": loc,
                          "cause": f"도로명주소\n{_rd(f['road_reg'])} 등기"})
    land = {"display_no": "1", "location": f"1. {a.jibun_full}", "category": "대",
            "area": f"{_area(f['land_total'])}㎡", "cause": f"{_rd(f['preserve'])} 등기"}
    unit = {"display_no": "1", "receipt": _rd(f["preserve"]), "unit_no": f"제{f['floor']}층 제{f['ho']}호",
            "detail": f"{pr.structure}\n{_area(pr.exclusive_area)}㎡", "cause": f["drawing_no"]}
    land_right = {"display_no": "1", "kind": "1 소유권대지권", "ratio": f"{_area(f['land_total'])}분의 {_area(pr.land_area)}",
                  "cause": f"{_rd(f['land_right_date'])} 대지권\n{_rd(f['preserve'])} 등기"}

    gapgu = [{
        "rank": "1", "purpose": "소유권보존", "receipt": f"{_rd(f['preserve'])}\n제{f['preserve_no']}호", "cause": "",
        "holder": {"role": "소유자", "name": f["dev"], "reg_no": f["dev_no"], "address": f["dev_addr"]},
    }, {
        "rank": "2", "purpose": "소유권이전", "receipt": f"{_rd(f['seller_acq'])}\n제{f['seller_acq_no']}호",
        "cause": f"{_rd(f['seller_acq'] - timedelta(days=rng.randint(30, 70)))}\n매매",
        "holder": {"role": "소유자", "name": seller.name, "reg_no": K.mask_rrn(seller.rrn, keep=0), "address": f["seller_addr"]},
    }]
    del gapgu[0]["cause"]
    if f["seller_acq"] >= date(2006, 6, 1):  # 거래가액 등기는 2006.6.1 이후
        gapgu[1]["holder"]["note"] = f"거래가액 금{won(f['seller_price'])}"
    eulgu = []
    sm = f["seller_mort"]
    if sm:
        bn, bno, baddr = _bank_legal(sm["bank"])
        eulgu.append({
            "rank": "1", "purpose": "근저당권설정", "receipt": f"{_rd(sm['date'])}\n제{sm['no']}호",
            "cause": f"{_rd(sm['date'])}\n설정계약",
            "max_amount": f"금{won(sm['max'])}", "debtor": seller.name, "debtor_address": f["seller_addr"],
            "mortgagee": f"{bn} {bno}", "mortgagee_address": f"{baddr}\n({sm['branch']})",
        })
    if f["transferred"]:
        bal = f["balance"]
        gapgu.append({
            "rank": "3", "purpose": "소유권이전", "receipt": f"{_rd(bal)}\n제{f['buyer_no']}호",
            "cause": f"{_rd(f['contract'])}\n매매",
            "holder": {"role": "소유자", "name": p.person.name, "reg_no": K.mask_rrn(p.person.rrn, keep=0),
                       "address": p.person.address.road_full, "note": f"거래가액 금{won(f['price'])}"},
        })
        if sm:
            eulgu.append({"rank": "2", "purpose": "1번근저당권설정등기말소", "receipt": f"{_rd(bal)}\n제{f['buyer_no'] + 1}호",
                          "cause": f"{_rd(bal)}\n해지"})
        bn, bno, baddr = _bank_legal(p.bank)
        eulgu.append({
            "rank": str(len(eulgu) + 1), "purpose": "근저당권설정", "receipt": f"{_rd(bal)}\n제{f['buyer_no'] + (2 if sm else 1)}호",
            "cause": f"{_rd(bal)}\n설정계약",
            "max_amount": f"금{won(f['buyer_max'])}", "debtor": p.person.name, "debtor_address": p.person.address.road_full,
            "mortgagee": f"{bn} {bno}", "mortgagee_address": f"{baddr}\n({p.bank_branch})",
        })
    t = view_dt
    hh, mm, ss = rng.randint(8, 18), rng.randint(0, 59), rng.randint(0, 59)
    out = {
        "unique_no": pr.unique_no,
        "property": f"{a.jibun_full} {_unit_label(f)}",
    }
    summary = rng.random() < 0.18  # 마지막 장: 주요 등기사항 요약 (참고용)
    if summary:
        out["summary"] = _registry_summary(gapgu, eulgu)
    else:
        out.update({"registry_office": courthouse(a), "buildings": buildings, "land": land, "unit": unit, "land_right": land_right,
                    "gapgu": gapgu, "eulgu": eulgu})
    if rng.random() < 0.5:
        out["view_datetime"] = f"{t.year}년{t.month:02d}월{t.day:02d}일 {hh:02d}시{mm:02d}분{ss:02d}초"
    else:
        out["issue_no"] = "".join(str(rng.randint(0, 9)) for _ in range(20))
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        out["confirm_no"] = "-".join("".join(rng.choice(letters) for _ in range(4)) for _ in range(2)) + f"-{rng.randint(0, 9999):04d}"
        out["issue_date_short"] = f"{t.year}/{t.month:02d}/{t.day:02d}"
        if not summary:
            out["issue_date"] = f"{t.year}년 {t.month}월 {t.day}일"
            out["fee"] = "1,000원"
    return out


def _registry_summary(gapgu: list, eulgu: list) -> dict:
    """주요 등기사항 요약(참고용): 말소되지 않은 사항만."""
    cur = gapgu[-1]
    h = cur["holder"]
    owners = [{"name": f"{h['name']} (소유자)", "reg_no": h["reg_no"], "share": "단독소유", "address": h["address"],
               "rank": cur["rank"]}]
    gone = {r["purpose"].split("번")[0] for r in eulgu if "번근저당권설정등기말소" in r["purpose"]}
    rights = []
    for r in eulgu:
        if "max_amount" not in r or r["rank"] in gone:
            continue
        rights.append({"rank": r["rank"], "purpose": r["purpose"], "receipt": r["receipt"].replace("\n", " "),
                       "main": f"채권최고액 {r['max_amount']}  근저당권자 {r['mortgagee'].split()[0]}",
                       "target_owner": h["name"]})
    return {"owners": owners, "rights": rights}


# ---------------------------------------------------------------------------
# 집합건축물대장(전유부, 갑)
# ---------------------------------------------------------------------------

@doc("building_register", "집합건축물대장(전유부)", "real_estate", page="a4_landscape")
def building_register(p: Profile, rng: random.Random) -> dict:
    """집합건축물대장(전유부, 갑) 등본."""
    f = _facts(p)
    a, pr = f["a"], f["pr"]
    owner_p, owner_date = (p.person, f["balance"]) if f["transferred"] else (pr.seller, f["seller_acq"])
    owner_addr = p.person.address.road_full if f["transferred"] else f["seller_addr"]
    common = [
        {"kind": "주", "floor": "각층", "structure": pr.structure, "usage": "계단실,복도,승강기",
         "area": f"{pr.exclusive_area * rng.uniform(0.18, 0.28):.2f}"},
    ]
    if f["is_apt"] or rng.random() < 0.5:
        common.append({"kind": "주", "floor": "지1층", "structure": pr.structure, "usage": "주차장",
                       "area": f"{pr.exclusive_area * rng.uniform(0.25, 0.45):.2f}"})
    if f["is_apt"]:
        common.append({"kind": "주", "floor": "지1층", "structure": pr.structure, "usage": "기계실,전기실",
                       "area": f"{pr.exclusive_area * rng.uniform(0.02, 0.06):.2f}"})
        if rng.random() < 0.5:
            common.append({"kind": "부", "floor": "1층", "structure": pr.structure, "usage": "관리사무소,주민공동시설",
                           "area": f"{pr.exclusive_area * rng.uniform(0.03, 0.08):.2f}"})
    # 공동주택가격: 매년 1월 1일 기준, 4월 말 공시
    y = p.issue_date.year if p.issue_date >= date(p.issue_date.year, 4, 30) else p.issue_date.year - 1
    prices, v = [], pr.official_price
    for yy in range(y, y - rng.randint(3, 4), -1):
        prices.append({"base_date": f"{yy}.01.01", "price": won(v, "")})
        v = K.round_to(v / rng.uniform(1.0, 1.12), 1_000_000)
    ho_name = (f"{f['dong_no']}동 " if f["dong_no"] else "") + f"{f['ho']}호"
    out = {
        "confirm_no": issue_no(rng, 16),
        "unique_no": f"{f['dong_code']}-3-{f['bonbun']:04d}{f['bubun']:04d}",
        "building_name": f["bname"] + (f" 제{f['dong_no']}동" if f["dong_no"] else ""),
        "unit_name": ho_name,
        "site_location": f"{a.region} {a.dong}",
        "jibun": a.jibun,
        "road_address": f"{a.region} {a.road} {a.building_no}",
        "exclusive": [{"kind": "주", "floor": f"{f['floor']}층", "structure": pr.structure, "usage": f["usage"],
                       "area": f"{pr.exclusive_area:.2f}"}],
        "common": common,
        "owner": {
            "name": owner_p.name,
            "rrn": K.mask_rrn(owner_p.rrn),
            "address": owner_addr,
            "share": "1/1",
            "change_date": D(owner_date, "dot"),
            "change_cause": "소유권이전",
        },
        "issue_date": D(p.issue_date, rng.choice(["kor", "kor_short"])),
        "officer": f"{rng.choice(['건축과', '건축행정과', '민원여권과', '종합민원과'])}",
        "officer_phone": K.landline(rng, a.sido),
        "issuer": district_office(a),
    }
    if pr.kind != "오피스텔":  # 오피스텔은 공동주택가격 공시 대상이 아님
        out["house_prices"] = prices
    return out


# ---------------------------------------------------------------------------
# 토지대장
# ---------------------------------------------------------------------------

@doc("land_register", "토지대장", "real_estate")
def land_register(p: Profile, rng: random.Random) -> dict:
    """토지대장 등본 (집합건물 대지)."""
    f = _facts(p)
    a, pr = f["a"], f["pr"]
    land_rows = []
    d0 = f["preserve"] - timedelta(days=rng.randint(200, 900))
    if rng.random() < 0.5:
        land_rows.append({"category": "(08)대", "area": _area(round(f["land_total"] * rng.uniform(1.05, 1.4), 1)),
                          "reason": f"({rng.choice(['20', '40'])}){D(d0 - timedelta(days=rng.randint(300, 3000)), 'kor')}\n"
                                    + rng.choice(["구획정리 완료", "지목변경", "등록전환"])})
    land_rows.append({"category": "(08)대", "area": _area(f["land_total"]),
                      "reason": f"(30){D(d0, 'kor')}\n분할되어 본번에 -{f['bubun'] or rng.randint(1, 30)}을 부함"
                      if land_rows or rng.random() < 0.5 else f"(40){D(d0, 'kor')}\n구획정리 완료"})
    owners = [{"change_date": D(f["preserve"], "kor"), "change_cause": "(01)소유권보존",
               "address": f["dev_addr"], "name": f["dev"], "reg_no": f["dev_no"]}]
    cur = (p.person, f["balance"], p.person.address.road_full) if f["transferred"] else (pr.seller, f["seller_acq"], f["seller_addr"])
    if f["transferred"]:
        owners.append({"change_date": D(f["seller_acq"], "kor"), "change_cause": "(03)소유권이전",
                       "address": f["seller_addr"], "name": pr.seller.name, "reg_no": K.mask_rrn(pr.seller.rrn)})
    owners.append({"change_date": D(cur[1], "kor"), "change_cause": "(03)소유권이전",
                   "address": cur[2], "name": cur[0].name, "reg_no": K.mask_rrn(cur[0].rrn)})
    if f["is_apt"] or pr.kind == "오피스텔":
        n = f["units"] - 1
        for o in owners[1:]:
            o["co_owners"] = f"외 {n:,}인"
    # 개별공시지가 (원/㎡): 대지권 면적당 가치로 역산
    base = pr.official_price * rng.uniform(0.45, 0.65) / max(pr.land_area, 1)
    y = p.issue_date.year if p.issue_date >= date(p.issue_date.year, 5, 31) else p.issue_date.year - 1
    prices = []
    for yy in range(y, y - rng.choice([5, 6, 7, 7]), -1):  # 정부24 발급본은 최근 7년 기본 표시
        prices.append({"base_date": f"{yy}/01/01", "price": won(K.round_to(base, 1000), "")})
        base /= rng.uniform(1.0, 1.1)
    prices.reverse()
    grades = [{"date": f"{yy}.{mm:02d}.01. 수정", "grade": str(g)} for yy, mm, g in
              [(1984, 7, f["land_grade"] - rng.randint(20, 40)), (1987, 7, f["land_grade"] - rng.randint(5, 18)),
               (1990, 1, f["land_grade"])]]
    t = p.issue_date
    return {
        "unique_no": f"{f['dong_code']}-1{f['bonbun']:04d}-{f['bubun']:04d}",
        "drawing_no": str(rng.randint(1, 60)),
        "issue_no": f"{t.year}{rng.randint(10000000, 99999999)}",
        "location": f"{a.region} {a.dong}",
        "sheet_no": f"{rng.randint(1, 3)}-{rng.randint(1, 2)}",
        "processed_time": f"{rng.randint(9, 17):02d}시 {rng.randint(0, 59):02d}분 {rng.randint(0, 59):02d}초",
        "jibun": a.jibun,
        "scale": rng.choice(["수치", "1:1200", "1:600", "1:1000"]),
        "issuer_name": rng.choice(["인터넷민원", "인터넷민원", "무인민원발급기"]),
        "land": land_rows,
        "owners": owners,
        "grades": grades,
        "zoning": f["zoning"],
        "land_prices": prices,
        "issue_date": D(t, rng.choice(["kor", "kor_short"])),
        "issuer": district_office(a),
    }


# ---------------------------------------------------------------------------
# 부동산(아파트) 매매계약서
# ---------------------------------------------------------------------------

def _amount(n: int) -> str:
    return f"금 {K.won_korean(n)}원정 (₩{n:,})"


@doc("sales_contract", "부동산 매매계약서", "real_estate")
def sales_contract(p: Profile, rng: random.Random) -> dict:
    """부동산(아파트) 매매계약서 (공인중개사 중개)."""
    f = _facts(p)
    a, pr, seller = f["a"], f["pr"], f["pr"].seller
    dfmt = rng.choice(["kor", "kor_short"])
    pay = {"price": _amount(f["price"]), "down": _amount(f["down"])}
    if f["middle"]:
        pay["middle"] = _amount(f["middle_amt"])
        pay["middle_date"] = D(f["middle"], dfmt)
    pay["balance"] = _amount(f["balance_amt"])
    pay["balance_date"] = D(f["balance"], dfmt)
    specials = ["현 시설물 상태의 계약이며, 매수인은 등기사항증명서 및 현장을 확인하고 계약함."]
    if f["seller_mort"]:
        specials.append(f"매도인은 잔금 지급일까지 을구 1번 근저당권(채권최고액 금{won(f['seller_mort']['max'])})을 "
                        "말소하기로 하며, 잔금으로 상환할 수 있다.")
    specials.append(f"매수인은 {p.bank} 주택담보대출로 잔금 일부를 지급할 예정이며, 매도인은 이에 협조한다.")
    specials += rng.sample([
        "잔금일 기준으로 관리비 및 제세공과금은 매도인이 정산한다.",
        "매도인은 잔금일까지 임차인 없이 명도하기로 한다.",
        "본 계약 이후 매도인은 추가 담보 설정이나 임대를 하지 않는다.",
        "옵션(빌트인 가전 등)은 현 상태로 포함하여 매도한다.",
        "누수 등 중대한 하자는 잔금일 이후 6개월 이내 매도인이 책임진다.",
    ], rng.randint(1, 2))
    return {
        "property": {
            "location": a.road_full,
            "land_category": "대",
            "land_right": f"소유권대지권 {_area(f['land_total'])}분의 {_area(pr.land_area)}",
            "land_area": f"{_area(pr.land_area)}㎡",
            "structure": pr.structure,
            "usage": f["usage_full"],
            "building_area": f"{_area(pr.exclusive_area)}㎡",
        },
        "payment": pay,
        "specials": [f"{i + 1}. {s}" for i, s in enumerate(specials)],
        "contract_date": D(f["contract"], dfmt),
        "seller": {"address": f["seller_addr"], "rrn": seller.rrn, "phone": seller.mobile, "name": seller.name},
        "buyer": {"address": p.person.address.road_full, "rrn": p.person.rrn, "phone": p.person.mobile, "name": p.person.name},
        "brokers": _brokers(rng, f),
    }


# ---------------------------------------------------------------------------
# 주택임대차표준계약서 (전세)
# ---------------------------------------------------------------------------

@doc("lease_contract", "주택임대차표준계약서", "real_estate")
def lease_contract(p: Profile, rng: random.Random) -> dict:
    """주택임대차표준계약서 (전세). 임대인 = 기존 소유자(seller), 임차인 = 본인."""
    f = _facts(p)
    a, pr, lord = f["a"], f["pr"], f["pr"].seller
    r = random.Random(f"lease:{p.seed}")
    cdate = p.issue_date - timedelta(days=r.randint(3, 25))
    start = cdate + timedelta(days=r.randint(20, 60))
    end = date(start.year + 2, start.month, start.day if not (start.month == 2 and start.day == 29) else 28) - timedelta(days=1)
    dep = pr.lease_deposit
    down = K.round_to(dep * rng.choice([0.05, 0.1, 0.1]), 1_000_000)
    dfmt = rng.choice(["kor", "kor_short"])
    stamp_d = cdate + timedelta(days=rng.randint(0, 5))
    mort_d = start + timedelta(days=2)
    specials = [
        f"주택을 인도받은 임차인은 {D(start, 'kor_short')}까지 주민등록(전입신고)과 주택임대차계약서상 확정일자를 받기로 하고, "
        f"임대인은 {D(mort_d, 'kor_short')}(최소한 임차인의 위 약정일자 이틀 후부터 가능)에 저당권 등 담보권을 설정할 수 있다.",
        "임대인이 위 특약에 위반하여 임차주택에 저당권 등 담보권을 설정한 경우에는 임차인은 임대차계약을 해제 또는 해지할 수 있다.",
        f"임차인은 {p.bank} 전세자금대출을 신청할 예정이며, 임대인은 이에 협조한다. "
        "임차인의 귀책사유 없이 대출이 불가한 경우 본 계약은 무효로 하고 임대인은 계약금을 즉시 반환한다.",
    ]
    if rng.random() < 0.6:  # 2023 개정 표준계약서 권고 특약
        specials.insert(2, "임대차계약 체결 이후 임대인이 사전에 고지하지 않은 선순위 임대차 정보나 미납·체납한 국세·지방세가 "
                           "확인되는 경우, 임차인은 위약금 없이 임대차계약을 해제할 수 있다.")
    if f["seller_mort"] and not f["transferred"]:
        specials.append(f"임대인은 잔금일까지 을구 1번 근저당권(채권최고액 금{won(f['seller_mort']['max'])})을 말소하기로 한다.")
    specials += rng.sample(["반려동물 사육은 임대인의 동의를 받아야 한다.", "벽걸이TV, 못 자국 등 경미한 훼손은 원상복구 대상에서 제외한다.",
                            "관리비는 실사용 기준으로 임차인이 부담한다.", "도배·장판은 잔금일 전까지 임대인이 교체하여 준다."], int(rng.random() < 0.3))
    return {
        "landlord_name": lord.name, "tenant_name": p.person.name,
        "house": {
            "location": a.road_full,
            "land_category": "대",
            "land_area": f"{_area(f['land_total'])}㎡",
            "structure_usage": f"{pr.structure} / {f['usage_full']}",
            "building_area": f"{_area(pr.exclusive_area)}㎡",
            "lease_part": f"전부 ({_area(pr.exclusive_area)}㎡)",
        },
        "contract_type": rng.choice(["신규 계약", "신규 계약", "신규 계약", "합의에 의한 재계약"]),
        "management_fee": rng.choice(["세대별 사용량 및 관리규약에 따른 부과액(공용관리비 면적 비례)", "관리사무소 부과 고지서 기준 실비",
                                      "관리규약에 따라 관리주체가 부과하는 금액"]),
        "tax_arrears": "없음",
        "prior_fixed_date": "해당 없음",
        "deposit": _amount(dep),
        "down_payment": _amount(down),
        "balance": _amount(dep - down),
        "balance_date": D(start, dfmt),
        "handover_date": D(start, dfmt),
        "end_date": D(end, dfmt),
        "fixed_date": {"date": D(stamp_d, "dot"), "no": f"{stamp_d.year}-{rng.randint(100, 9999)}",
                       "office": community_center(a).removesuffix("장") + "행정복지센터"},
        "specials": [f"{i + 1}. {s}" for i, s in enumerate(specials)],
        "contract_date": D(cdate, dfmt),
        "landlord": {"address": f["seller_addr"], "rrn": lord.rrn, "phone": lord.mobile, "name": lord.name},
        "tenant": {"address": p.person.address.road_full, "rrn": p.person.rrn, "phone": p.person.mobile, "name": p.person.name},
        "brokers": _brokers(rng, f),
    }


# ---------------------------------------------------------------------------
# 전입세대확인서
# ---------------------------------------------------------------------------

@doc("move_in_household_list", "전입세대확인서", "real_estate")
def move_in_household_list(p: Profile, rng: random.Random) -> dict:
    """전입세대확인서(열람). 해당 주소에 전입신고된 세대주 목록."""
    f = _facts(p)
    a, pr, seller = f["a"], f["pr"], f["pr"].seller
    rows = []
    if f["transferred"]:
        heads = [(p.person.name, f["balance"] + timedelta(days=rng.randint(0, 14)))]
    elif f["seller_resident"]:
        heads = [(seller.name, f["seller_acq"] + timedelta(days=rng.randint(0, 30)))]
        if rng.random() < 0.15:
            heads.append((_rand_person(rng), heads[0][1] + timedelta(days=rng.randint(200, 2000))))
    else:
        heads = [(_rand_person(rng), p.issue_date - timedelta(days=rng.randint(200, 1400)))]
    cohab = []
    for i, (nm, d) in enumerate(heads):
        first_same = rng.random() < 0.75
        first_nm, first_d = (nm, d) if first_same else (_rand_person(rng), d - timedelta(days=rng.randint(0, 3)))
        n_co = 1 if rng.random() < 0.15 else 0  # 주민등록표상 동거인(세대원 아님)은 드묾
        rows.append({"no": str(i + 1), "head_name": _mask_name(nm), "move_in_date": D(min(d, p.issue_date), "dash"),
                     "reg_type": "거주자", "first_name": _mask_name(first_nm), "first_date": D(min(first_d, p.issue_date), "dash"),
                     "first_reg_type": "거주자", "cohabitants": str(n_co)})
        for _ in range(n_co):
            cd = min(d + timedelta(days=rng.randint(30, 900)), p.issue_date)
            cohab.append({"no": str(len(cohab) + 1), "name": _mask_name(_rand_person(rng)), "move_in_date": D(cd, "dash"),
                          "reg_type": "거주자"})
    purpose = rng.choice(["금융기관 대출(주택담보대출)", "금융기관 제출", "전세자금대출 신청", "임대차계약 체결"])
    return {
        "issue_no": issue_no(rng, 16),
        "issue_date": D(p.issue_date, "dot"),
        "address": a.road_full,
        "jibun_address": f"{a.jibun_full} " + (f"{f['dong_no']}동 " if f["dong_no"] else "") + f"{f['ho']}호",
        "households": rows,
        **({"cohabitants": cohab} if cohab else {}),
        "kind": rng.choice(["열람", "교부", "교부"]),
        "applicant": {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn), "address": p.person.address.road_full,
                      "purpose": purpose},
        "view_date": D(p.issue_date, "kor"),
        "issuer": community_center(a),
    }
