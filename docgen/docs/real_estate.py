"""부동산 관련 서류: 등기사항전부증명서, 건축물대장, 토지대장, 매매계약서, 임대차계약서, 전입세대확인서.

같은 프로필이면 서류 사이의 사실관계(매매일, 근저당, 소유권 이전 여부, 공유자 등)가 맞도록
`_facts(p)`가 프로필 seed 로부터 결정론적으로 공통 사실을 만든다.
매도인 = p.property.seller (기존 소유자), 매수인/임차인 = p.person.

등기 이력(`_history`)도 `_facts` 안에서 만든다. 소유자가 여러 번 바뀌거나 근저당 설정·말소가 반복되는
'이력이 많은 물건'(heavy)과 공유·신탁·가압류·전세권 같은 특수 상황은 프로필 단위로 정해지므로
등기부·토지대장·건축물대장·계약서가 서로 어긋나지 않는다.
"""
import re

from ..entities import World
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
# 합병·분할로 근저당권이 넘어간 은행: 옛 명의, 주소, 기준일, 등기원인
_MERGERS = {
    "하나은행": ("주식회사한국외환은행", "서울특별시 중구 을지로 35", date(2015, 9, 1), "회사합병"),
    "농협은행": ("농업협동조합중앙회", "서울특별시 중구 새문안로 16", date(2012, 3, 2), "회사분할"),
}
_BRANCHES = ["역삼", "서초", "잠실", "목동", "분당", "일산", "해운대", "수성", "둔산", "광교", "여의도", "종로",
             "상계", "평촌", "동탄", "송도", "센텀", "범어", "상무", "청주"]
_TRUSTEES = ["한국토지신탁주식회사", "코람코자산신탁주식회사", "주식회사케이비부동산신탁", "하나자산신탁주식회사",
             "대한토지신탁주식회사", "주식회사아시아신탁", "교보자산신탁주식회사", "주식회사무궁화신탁"]
_CREDITORS = ["주식회사신한카드", "주식회사케이비국민카드", "서울보증보험주식회사", "현대캐피탈주식회사",
              "롯데캐피탈주식회사", "주식회사우리카드", "신용보증기금", "기술보증기금", "주식회사삼성카드"]
_DEVELOPERS = ["대림", "삼호", "한양", "동아", "금호", "우방", "태영", "신동아", "동부", "한라", "벽산", "쌍용", "경남", "코오롱"]
_SIDO_CODE = {"서울특별시": "11", "부산광역시": "26", "대구광역시": "27", "인천광역시": "28", "광주광역시": "29",
              "대전광역시": "30", "울산광역시": "31", "세종특별자치시": "36", "경기도": "41", "강원특별자치도": "51",
              "충청북도": "43", "충청남도": "44", "전북특별자치도": "52", "전라남도": "46", "경상북도": "47",
              "경상남도": "48", "제주특별자치도": "50"}


class _Row(dict):
    """등기부 한 줄. 말소 표시 같은 화면 상태는 값이 아니라 속성으로 둔다 (정답에 들어가지 않음)."""
    struck = False       # 말소된 사항: 줄 전체에 빨간 실선
    addr_struck = False  # 등기명의인표시변경으로 바뀐 옛 주소


class _Hand(str):
    """손으로 덧붙여 쓴 특약 (템플릿에서 손글씨 모양으로 그린다)."""
    hand = True


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


def _court(a: Address) -> str:
    """관할 법원 (등기소명에서 '등기국/등기과/…등기소'를 뗀다). 예) '수원지방법원 성남지원'"""
    out = []
    for w in courthouse(a).split():
        if w.endswith(("법원", "지원")):
            out.append(w)
    return " ".join(out)


def _days(a: date, b: date) -> int:
    return (b - a).days


def _iga(name: str) -> str:
    """이름 뒤 주격 조사: 받침이 있으면 '이', 없으면 '가'."""
    c = name[-1]
    return name + ("이" if "가" <= c <= "힣" and (ord(c) - 0xAC00) % 28 else "가")


def _eun(name: str) -> str:
    c = name[-1]
    return name + ("은" if "가" <= c <= "힣" and (ord(c) - 0xAC00) % 28 else "는")


def _between(r: random.Random, lo: date, hi: date) -> date | None:
    return rand_date(r, lo, hi) if hi > lo else None


# ---------------------------------------------------------------------------
# 공통 사실관계
# ---------------------------------------------------------------------------

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
    units_per_floor = r.choice([2, 2, 4, 4, 6]) if is_apt else r.choice([2, 3, 4])
    floor_area = round(pr.exclusive_area * r.uniform(1.25, 1.4) * units_per_floor, 2)
    if is_apt:
        land_total = round(r.uniform(9000, 60000), 1)
        dev = f"주식회사{r.choice(_DEVELOPERS)}{r.choice(['건설', '산업개발', '종합건설'])}"
        dev_rrn = K.corp_reg_no(r)
        dev_corp = True
    else:
        land_total = round(max(pr.land_area * units_per_floor * total_floors * r.uniform(1.0, 1.3), 180), 1)
        dev = _rand_person(r)
        dev_rrn = K.rrn(r, rand_date(r, date(1950, 1, 1), date(1975, 12, 31)), "M")
        dev_corp = False
    seller_resident = r.random() < 0.6
    seller_addr = a.road_full if seller_resident else pr.seller.address.road_full
    jibun = a.jibun.split("-")
    f = {
        "a": a, "pr": pr, "dong_no": dong_no, "ho": ho, "floor": floor, "total_floors": total_floors,
        "bname": bname, "is_apt": is_apt, "usage": usage, "usage_full": usage_full,
        "preserve": preserve, "seller_acq": seller_acq, "transferred": transferred, "contract": contract,
        "middle": middle, "balance": balance, "price": price, "down": down, "middle_amt": middle_amt,
        "balance_amt": price - down - middle_amt, "seller_price": seller_price,
        "floor_area": floor_area, "land_total": land_total,
        "dev": dev, "dev_rrn": dev_rrn, "dev_corp": dev_corp,
        "dev_no": dev_rrn if dev_corp else K.mask_rrn(dev_rrn, keep=0),
        "dev_addr": f"{a.region} {r.choice(['중앙로', '대학로', '시청로'])} {r.randint(1, 200)}",
        "seller_resident": seller_resident, "seller_addr": seller_addr,
        "units": r.randint(280, 2400) if is_apt else units_per_floor * total_floors,
        "units_per_floor": units_per_floor,
        "bonbun": int(jibun[0]), "bubun": int(jibun[1]) if len(jibun) > 1 else 0,
        "dong_code": f"{_SIDO_CODE[a.sido]}{r.randint(110, 890)}{r.randint(101, 140)}00",
        "drawing_no": f"도면편철장 제{r.randint(1, 9)}책 제{r.randint(1, 900)}장",
        "land_right_date": preserve - timedelta(days=r.randint(3, 20)),
        "road_reg": date(2012, r.randint(1, 12), r.randint(1, 28)) if completed.year < 2011 else None,
        "land_grade": r.randint(120, 260),
        "zoning": r.choice(["제2종일반주거지역", "제3종일반주거지역", "제3종일반주거지역", "준주거지역", "제2종일반주거지역(7층이하)"]),
    }
    f["hist"] = _history(p, f, r)
    return f


# ---------------------------------------------------------------------------
# 등기 이력 (갑구·을구)
# ---------------------------------------------------------------------------

def _pi(name: str, rrn: str, addr: str, corp: bool = False, person: Person | None = None) -> dict:
    """등기명의인 정보. rrn 은 주민등록번호(전체) 또는 법인등록번호."""
    return {"name": name, "rrn": rrn, "addr": addr, "corp": corp, "person": person, "addr0": None, "addr_chg": None}


def _addr_at(pi: dict, d: date) -> str:
    return pi["addr0"] if pi["addr_chg"] and d < pi["addr_chg"] else pi["addr"]


def _reg_no(pi: dict) -> str:
    """등기부식 등록번호 (개인은 뒷자리 전부 가림)"""
    return pi["rrn"] if pi["corp"] else K.mask_rrn(pi["rrn"], keep=0)


def _mortgagee(r: random.Random, a: Address, d: date, bank: str | None = None) -> dict:
    """근저당권자 표시. 옛 명의(합병 전 외환은행 등)면 old 에 지금 은행 키를 남긴다."""
    if bank is None and r.random() < 0.18:  # 제2금융권
        stem = a.dong[:-1] if a.dong.endswith("동") else a.dong
        name = r.choice([f"{stem}새마을금고", f"{stem}신용협동조합", "주식회사오케이저축은행", "삼성생명보험주식회사"])
        return {"mortgagee": f"{name} {K.corp_reg_no(random.Random('mg:' + name))}",
                "mortgagee_address": f"{a.region} {a.road} {r.randint(1, 300)}", "bank": name, "old": None}
    bank = bank or r.choice(list(_BANK_LEGAL))
    name, no, addr = _bank_legal(bank)
    old = None
    if bank in _MERGERS and d < _MERGERS[bank][2] and r.random() < 0.7:
        name, addr = _MERGERS[bank][0], _MERGERS[bank][1]
        no = K.corp_reg_no(random.Random(f"bank:{name}"))
        old = bank
    elif bank == "iM뱅크" and d < date(2024, 6, 5):
        name = "주식회사대구은행"
    return {"mortgagee": f"{name} {no}", "mortgagee_address": f"{addr}\n({r.choice(_BRANCHES)}지점)", "bank": bank, "old": old}


def _history(p: Profile, f: dict, r: random.Random) -> dict:
    """소유권 변동과 갑구·을구 등기 사항을 시간 순으로 만든다.

    사건(ev)을 먼저 모은 뒤 날짜 순으로 정렬해 순위번호·접수번호를 매기고, 말소 사건이 가리키는 줄에 말소 표시를 한다."""
    a, pr, seller = f["a"], f["pr"], f["pr"].seller
    issue = p.issue_date
    H = heavy(r, 0.3)
    sp = {k: special(r, k, q) for k, q in (
        ("joint_owner", 0.15), ("joint_buyer", 0.2), ("reg_seizure", 0.15), ("reg_active_seizure", 0.05),
        ("reg_trust", 0.07), ("reg_jeonse", 0.1), ("reg_lease_order", 0.06), ("reg_mort_change", 0.15),
        ("reg_addr_change", 0.12))}
    evs: list[dict] = []

    def ev(sec: str, d: date, prio: int = 1, **kw) -> dict:
        e = {"sec": sec, "date": d, "prio": prio, "seq": len(evs), "subs": [], "end": None, **kw}
        evs.append(e)
        return e

    def cancel(tgt: dict, d: date, tail: str, cause: str, prio: int = 1) -> None:
        tgt["end"] = d
        ev(tgt["sec"], d, prio, kind="cancel", target=tgt, tail=tail, cause=f"{_rd(d)}\n{cause}")

    def value_at(d: date) -> int:
        span = max(1, _days(f["preserve"], issue))
        return K.round_to(f["price"] * (0.4 + 0.6 * _days(f["preserve"], d) / span), 10_000_000)

    # --- 소유자 (시대별) -----------------------------------------------------
    dev = _pi(f["dev"], f["dev_rrn"], f["dev_addr"], corp=f["dev_corp"])
    eras = [{"owners": [(dev, None)], "start": f["preserve"], "dev": True, "cause": None}]
    gap = _days(f["preserve"], f["seller_acq"])
    want = r.randint(2, 5) if H else r.choices([0, 1, 2], [60, 28, 12])[0]
    n_mid = max(0, min(want, gap // 500 - 1))
    for i in range(n_mid):
        seg = gap / (n_mid + 1)
        d = f["preserve"] + timedelta(days=int(seg * (i + 1) + r.uniform(-seg / 4, seg / 4)))
        w = World(f"re-owner:{p.seed}:{i}")
        per = w.person(birth_range=(1940, 1985))
        pi = _pi(per.name, per.rrn, a.road_full if r.random() < 0.5 else per.address.road_full, person=per)
        cause = r.choices(["매매", "증여", "상속", "협의분할에 의한 상속"], [80, 8, 7, 5])[0]
        eras.append({"owners": [(pi, None)], "start": d, "cause": cause})
    seller_pi = _pi(seller.name, seller.rrn, f["seller_addr"], person=seller)
    co_seller = None
    if sp["joint_owner"]:
        w = World(f"re-co:{p.seed}")
        y = seller.birth.year
        co_seller = w.person(gender="F" if seller.gender == "M" else "M", birth_range=(y - 5, y + 4))
    co_pi = _pi(co_seller.name, co_seller.rrn, f["seller_addr"], person=co_seller) if co_seller else None
    joint_at_acq = bool(co_seller) and r.random() < 0.5
    eras.append({"owners": [(seller_pi, "2분의 1"), (co_pi, "2분의 1")] if joint_at_acq else [(seller_pi, None)],
                 "start": f["seller_acq"], "cause": "매매", "price": f["seller_price"], "seller": True})
    co_buyer = p.spouse if (f["transferred"] and sp["joint_buyer"] and p.spouse) else None
    if f["transferred"]:
        me = _pi(p.person.name, p.person.rrn, p.person.address.road_full, person=p.person)
        owners = [(me, None)]
        if co_buyer:
            owners = [(me, "2분의 1"), (_pi(co_buyer.name, co_buyer.rrn, p.person.address.road_full, person=co_buyer), "2분의 1")]
        eras.append({"owners": owners, "start": f["balance"], "cause": "매매", "price": f["price"], "buyer": True,
                     "cause_date": f["contract"]})
    for i, e in enumerate(eras):
        e["end"] = eras[i + 1]["start"] if i + 1 < len(eras) else None

    # 소유권 이전 사건
    for e in eras:
        d = e["start"]
        if e.get("dev"):
            e["ev"] = ev("gap", d, kind="own", purpose="소유권보존", cause=None, owners=e["owners"])
            continue
        cd = e.get("cause_date") or d - timedelta(days=r.randint(30, 70) if e["cause"] == "매매" else r.randint(5, 120))
        price = e.get("price") or (value_at(cd) if e["cause"] == "매매" else None)
        e["ev"] = ev("gap", d, kind="own", purpose="소유권이전", cause=f"{_rd(cd)}\n{e['cause']}", owners=e["owners"],
                     price=price if (e["cause"] == "매매" and d >= date(2006, 6, 1)) else None)

    # --- 시대별 사건 ----------------------------------------------------------
    plan_mg = None
    try:  # 은행 대출 서식(근저당권설정계약서)과 같은 대출 조건
        from .bank_form_loan import _plan_personal
        plan_mg = _plan_personal(p)["mortgage"]
    except Exception:  # noqa: BLE001
        plan_mg = None

    def mortgage(era: dict, d: date, prio: int = 1, bank: str | None = None, max_amt: int | None = None,
                 branch: str | None = None) -> dict:
        owner = era["owners"][0][0]
        mg = _mortgagee(r, a, d, bank)
        if branch and bank:
            mg["mortgagee_address"] = mg["mortgagee_address"].split("\n")[0] + f"\n({branch})"
        if max_amt is None:
            loan = K.round_to(value_at(d) * r.uniform(0.3, 0.6), 1_000_000)
            max_amt = int(loan * (1.3 if d < date(2012, 1, 1) else r.choice([1.2, 1.2, 1.1, 1.3])))
        row = {"purpose": "근저당권설정", "cause": f"{_rd(d)}\n설정계약", "max_amount": f"금{won(max_amt)}",
               "debtor": owner["name"], "debtor_address": _addr_at(owner, d),
               "mortgagee": mg["mortgagee"], "mortgagee_address": mg["mortgagee_address"]}
        return ev("eul", d, prio, kind="main", type="mortgage", row=row, max=max_amt, mg=mg, era=era)

    def free(era: dict, d: date) -> bool:
        b = era.get("block")
        return not b or not (b[0] - timedelta(days=20) <= d <= b[1] + timedelta(days=20))

    target_era = next((e for e in eras if e.get("seller")), eras[-1])
    rent_eras = [e for e in eras[1:] if not e.get("buyer") and (not e.get("seller") or not f["seller_resident"])]
    for era in eras[1:]:
        S = era["start"]
        E = era["end"] or issue
        cur = era["end"] is None
        owner = era["owners"][0][0]
        active: list[dict] = []
        # 신탁 (담보신탁 후 신탁재산 귀속)
        if (sp["reg_trust"] and era is target_era) or (H and not cur and r.random() < 0.15):
            t1 = _between(r, S + timedelta(days=90), E - timedelta(days=560))
            if t1 and not era.get("buyer"):
                t2 = t1 + timedelta(days=r.randint(365, max(366, min(1400, _days(t1, E) - 90))))
                if t2 < E - timedelta(days=30):
                    era["block"] = (t1, t2)
                    tr = r.choice(_TRUSTEES)
                    tpi = _pi(tr, K.corp_reg_no(random.Random("trust:" + tr)),
                              f"서울특별시 강남구 테헤란로 {random.Random('trust-a:' + tr).randint(100, 520)}", corp=True)
                    t_ev = ev("gap", t1, kind="own", purpose="소유권이전", cause=f"{_rd(t1)}\n신탁",
                              owners=[(tpi, None)], role="수탁자", trust_no=f"신탁원부 제{t1.year}-{r.randint(100, 9999)}호")
                    ev("gap", t2, kind="own", purpose="소유권이전", cause=f"{_rd(t2)}\n신탁재산의귀속",
                       owners=era["owners"], trust_cancel=t_ev)
        # 등기명의인표시변경 (주소 이전)
        if len(era["owners"]) == 1 and not owner["corp"] and not era.get("block") and (
                (sp["reg_addr_change"] and era is target_era) or (H and r.random() < 0.3)):
            tc = _between(r, S + timedelta(days=120), E - timedelta(days=30))
            if tc:
                old = World(f"re-addr:{p.seed}:{owner['name']}").address("apt" if r.random() < 0.6 else "villa").road_full
                if old != owner["addr"]:
                    owner["addr0"], owner["addr_chg"] = old, tc
                    ev("gap", tc, kind="sub", target=era["ev"], tail="번등기명의인표시변경", cause=f"{_rd(tc - timedelta(days=r.randint(3, 40)))}\n전거",
                       content={"change": f"{owner['name']}의 주소 {owner['addr']}"}, addr=True)
        # 공유자 지분 증여 (부부 공동명의 전환)
        if era.get("seller") and co_pi and not joint_at_acq:
            tg = _between(r, (era["block"][1] if era.get("block") else S) + timedelta(days=200), E - timedelta(days=60))
            if tg and free(era, tg):
                ev("gap", tg, kind="own", purpose="소유권일부이전", cause=f"{_rd(tg - timedelta(days=r.randint(3, 30)))}\n증여",
                   owners=[(co_pi, "2분의 1")], partial=True)
            else:
                ev("gap", S + timedelta(days=1), kind="own", purpose="소유권일부이전",
                   cause=f"{_rd(S)}\n증여", owners=[(co_pi, "2분의 1")], partial=True)
        # 근저당: 취득할 때, 그 뒤 대환·추가 대출
        if era.get("buyer"):
            if plan_mg and plan_mg["purpose"] == "주택구입자금":
                mx = K.round_to(plan_mg["amount"] * plan_mg["max_ratio"] / 100, 1_000_000)
                active.append(mortgage(era, S, 2, bank=p.bank if p.bank in _BANK_LEGAL else None, max_amt=mx,
                                       branch=p.bank_branch))
            elif plan_mg and plan_mg["purpose"].startswith("타행"):  # 지금 은행으로 옮겨 올 타행 대출
                others = [b for b in _BANK_LEGAL if b != p.bank]
                active.append(mortgage(era, S, 2, bank=r.choice(others)))
            else:
                active.append(mortgage(era, S, 2, bank=p.bank if p.bank in _BANK_LEGAL else None, branch=p.bank_branch))
        elif r.random() < (0.8 if H else 0.6):
            active.append(mortgage(era, S, 2))
        if not era.get("buyer"):
            t = S
            for _ in range(r.randint(1, 3) if H else int(r.random() < 0.15)):
                t = t + timedelta(days=r.randint(300, 1100))
                if t >= E - timedelta(days=20):
                    break
                if not free(era, t):
                    continue
                new = mortgage(era, t)
                if active and r.random() < 0.8:  # 대환: 새 근저당 설정 후 옛 근저당 말소
                    old = active.pop(0)
                    c = min(t + timedelta(days=r.randint(0, 10)), E - timedelta(days=1), issue - timedelta(days=1))
                    cancel(old, max(c, t), "번근저당권설정등기말소", "해지")
                active.append(new)
        # 전세권 / 임차권등기명령 (소유자가 살지 않던 시기)
        if era in rent_eras:
            if (sp["reg_jeonse"] and era is (rent_eras[-1])) or (H and r.random() < 0.35):
                t = _between(r, S + timedelta(days=30), E - timedelta(days=780))
                if t and free(era, t):
                    w = World(f"re-jeonse:{p.seed}:{t}")
                    ten = w.person(birth_range=(1960, 1995))
                    end = date(t.year + 2, t.month, min(t.day, 28)) - timedelta(days=1)
                    dep = K.round_to(value_at(t) * r.uniform(0.5, 0.7), 5_000_000)
                    je = ev("eul", t, kind="main", type="jeonse", row={
                        "purpose": "전세권설정", "cause": f"{_rd(t)}\n설정계약", "deposit": f"금{won(dep)}",
                        "scope": "주거용 건물의 전부", "period": f"{_rd(t)}부터\n{_rd(end)}까지",
                        "jeonse_holder": f"{ten.name} {K.mask_rrn(ten.rrn, keep=0)}", "jeonse_holder_address": ten.address.road_full},
                        dep=dep, who=ten.name)
                    cancel(je, min(end + timedelta(days=r.randint(0, 40)), E - timedelta(days=2)), "번전세권설정등기말소", "해지")
            if (sp["reg_lease_order"] and era is rent_eras[0]) or (H and r.random() < 0.15):
                t0 = _between(r, S + timedelta(days=30), E - timedelta(days=900))
                if t0:
                    lend = t0 + timedelta(days=730)
                    t = lend + timedelta(days=r.randint(15, 80))
                    c = t + timedelta(days=r.randint(40, 300))
                    if c < E - timedelta(days=2) and free(era, t):
                        w = World(f"re-lease:{p.seed}:{t0}")
                        ten = w.person(birth_range=(1960, 1995))
                        dep = K.round_to(value_at(t0) * r.uniform(0.45, 0.65), 5_000_000)
                        mv = t0 + timedelta(days=r.randint(0, 5))
                        le = ev("eul", t, kind="main", type="lease", row={
                            "purpose": "주택임차권",
                            "cause": f"{_rd(t - timedelta(days=r.randint(5, 20)))}\n{_court(a)}의\n임차권등기명령\n({t.year}카임{r.randint(100, 9999)})",
                            "deposit": f"금{won(dep)}", "rent": "없음", "scope": "주거용 건물의 전부",
                            "contract_date": _rd(t0 - timedelta(days=r.randint(10, 60))), "resident_date": _rd(mv),
                            "possession_date": _rd(mv), "fixed_date": _rd(mv + timedelta(days=r.randint(0, 3))),
                            "lessee": f"{ten.name} {K.mask_rrn(ten.rrn, keep=0)}", "lessee_address": ten.address.road_full},
                            dep=dep, who=ten.name)
                        cancel(le, c, "번주택임차권등기말소", "해제")
        # 가압류·압류 (그리고 말소)
        if not era.get("buyer") and not owner["corp"]:
            n = (r.choices([0, 1, 2], [55, 35, 10])[0] if H else 0) + (1 if sp["reg_seizure"] and era is target_era else 0)
            for _ in range(n):
                t = _between(r, S + timedelta(days=60), E - timedelta(days=90))
                if not t or not free(era, t):
                    continue
                c = min(t + timedelta(days=r.randint(30, 600)), E - timedelta(days=2))
                if c <= t:
                    continue
                sz = ev("gap", t, kind="main", type="seizure", row=_seizure_row(r, a, t, p))
                cancel(sz, c, f"번{sz['row']['purpose']}등기말소", r.choice(["해제", "해제", "취하"]) if sz["row"]["purpose"] == "가압류" else "해제")
            if cur and era.get("seller") and sp["reg_active_seizure"]:
                t = _between(r, max(S + timedelta(days=30), issue - timedelta(days=300)), issue - timedelta(days=15))
                if t and free(era, t):
                    era["open_seizure"] = ev("gap", t, kind="main", type="seizure", row=_seizure_row(r, a, t, p, "가압류"))
        if H and not cur and not era.get("buyer") and active and r.random() < 0.25:  # 임의경매 신청 후 취하
            m0 = active[0]
            t = _between(r, max(S, m0["date"]) + timedelta(days=200), E - timedelta(days=120))
            if t and free(era, t):
                bank_name = m0["row"]["mortgagee"]
                ae = ev("gap", t, kind="main", type="auction", row={
                    "purpose": "임의경매개시결정",
                    "cause": f"{_rd(t - timedelta(days=r.randint(2, 10)))}\n{_court(a)}의\n임의경매개시결정\n({t.year}타경{r.randint(1000, 99999)})",
                    "creditor": bank_name, "creditor_address": m0["row"]["mortgagee_address"].split("\n")[0]})
                cancel(ae, min(t + timedelta(days=r.randint(40, 300)), E - timedelta(days=3)), "번임의경매개시결정등기말소", "취하")
        # 다음 소유자에게 넘어갈 때 남은 근저당 말소 (잔금일, 이전등기 앞 번호)
        if not cur:
            for m_ in active:
                cancel(m_, E, "번근저당권설정등기말소", "해지", prio=0)
            active = []
        era["active"] = active

    # 근저당권 변경(채권최고액 감액)·이전(은행 합병)
    morts = [e for e in evs if e.get("type") == "mortgage"]
    did_change = False
    for m_ in morts:
        end = m_["end"] or issue
        want = (H and r.random() < 0.35) or (sp["reg_mort_change"] and not did_change and m_["era"] is target_era)
        if want:
            t = _between(r, m_["date"] + timedelta(days=120), end - timedelta(days=15))
            if t and free(m_["era"], t):
                new_max = K.round_to(m_["max"] * r.uniform(0.5, 0.85), 1_000_000)
                ev("eul", t, kind="sub", target=m_, tail="번근저당권변경", cause=f"{_rd(t)}\n변경계약",
                   content={"change": f"채권최고액 금{won(new_max)}"}, new_max=new_max)
                did_change = True
        old = m_["mg"]["old"]
        if old:
            cut = _MERGERS[old][2]
            t = _between(r, cut + timedelta(days=10), min(end - timedelta(days=5), cut + timedelta(days=500), issue))
            if t:
                name, no, addr = _bank_legal(old)
                ev("eul", t, kind="sub", target=m_, tail="번근저당권이전", cause=f"{_rd(cut)}\n{_MERGERS[old][3]}",
                   content={"mortgagee": f"{name} {no}", "mortgagee_address": f"{addr}\n({r.choice(_BRANCHES)}지점)"},
                   new_mortgagee=f"{name} {no}")

    return _compile(evs, eras, r, f, p, co_seller, co_buyer, H, sp)


def _seizure_row(r: random.Random, a: Address, t: date, p: Profile, kind: str | None = None) -> dict:
    """가압류 또는 압류 등기의 내용."""
    kind = kind or r.choice(["가압류", "가압류", "압류"])
    if kind == "가압류":
        cr = r.choice(_CREDITORS + ["개인"])
        if cr == "개인":
            w = World(f"re-cred:{p.seed}:{t}")
            per = w.person(birth_range=(1950, 1990))
            cred, caddr = f"{per.name} {K.mask_rrn(per.rrn, keep=0)}", per.address.road_full
        else:
            cred, caddr = f"{cr} {K.corp_reg_no(random.Random('cr:' + cr))}", f"서울특별시 {r.choice(['중구', '종로구', '영등포구', '강남구'])} {r.choice(['세종대로', '을지로', '국제금융로', '테헤란로'])} {r.randint(10, 400)}"
        row = {"purpose": "가압류", "cause": f"{_rd(t - timedelta(days=r.randint(1, 6)))}\n{_court(a)}의\n가압류 결정({t.year}카단{r.randint(1000, 99999)})",
               "claim_amount": f"금{won(K.round_to(r.uniform(3e6, 9e7), 1000) + r.randint(0, 999))}",
               "creditor": cred, "creditor_address": caddr}
    else:
        which = r.random()
        if which < 0.5:
            row = {"purpose": "압류", "cause": f"{_rd(t - timedelta(days=r.randint(1, 6)))}\n압류({r.choice(['징수과', '체납징세과', '징세과'])}-{r.randint(1000, 99999)})",
                   "right_holder": "국", "agency": tax_office(a).removesuffix("장")}
        elif which < 0.8:
            gu = (a.sigungu.split()[-1] if a.sigungu else "")
            row = {"purpose": "압류", "cause": f"{_rd(t - timedelta(days=r.randint(1, 6)))}\n압류({r.choice(['세무과', '징수과', '세외수입과'])}-{r.randint(1000, 99999)})",
                   "right_holder": f"{a.sido}{gu}".replace(" ", "")}
        else:
            row = {"purpose": "압류", "cause": f"{_rd(t - timedelta(days=r.randint(1, 6)))}\n압류({a.sigungu.split()[-1] if a.sigungu else a.sido}지사-{r.randint(1000, 99999)})",
                   "right_holder": "국민건강보험공단"}
    return row


def _compile(evs, eras, r, f, p, co_seller, co_buyer, H, sp) -> dict:
    """사건을 정렬해 갑구·을구 줄을 만든다."""
    gapgu: list[_Row] = []
    eulgu: list[_Row] = []
    rank = {"gap": 0, "eul": 0}
    nos: dict[date, int] = {}
    state: list[dict] = []  # 현재 소유자 [{pi, share, rank}]
    chain: list[dict] = []  # 소유자 변동 (대장용)
    for e in sorted(evs, key=lambda e: (e["date"], e["prio"], e["seq"])):
        d = e["date"]
        nos[d] = nos[d] + 1 if d in nos else r.randint(1500, 98000)
        receipt = f"{_rd(d)}\n제{nos[d]}호"
        out = gapgu if e["sec"] == "gap" else eulgu
        if e["kind"] == "own":
            rank["gap"] += 1
            rk = str(rank["gap"])
            row = _Row(rank=rk, purpose=e["purpose"], receipt=receipt)
            if e["cause"]:
                row["cause"] = e["cause"]
            owners = e["owners"]
            if e.get("trust_cancel"):  # 신탁재산 귀속: 신탁 전 소유자(지분 그대로)에게 돌아온다
                owners = e["trust_cancel"]["prev_state"]
            if e.get("trust_no"):
                e["prev_state"] = [(s["pi"], None if s["share"] == "단독소유" else s["share"]) for s in state]
            if len(owners) == 1 and owners[0][1] is None:
                pi = owners[0][0]
                row["holder"] = {"role": e.get("role", "소유자"), "name": pi["name"], "reg_no": _reg_no(pi), "address": _addr_at(pi, d)}
                if e.get("price"):
                    row["holder"]["note"] = f"거래가액 금{won(e['price'])}"
            else:
                row["holders"] = []
                for i, (pi, share) in enumerate(owners):
                    h = {"share": f"지분 {share}", "name": pi["name"], "reg_no": _reg_no(pi), "address": _addr_at(pi, d)}
                    if i == 0:
                        h = {"role": "공유자", **h}
                    row["holders"].append(h)
                if e.get("price"):
                    row["note"] = f"거래가액 금{won(e['price'])}"
            e["row"], e["rank"] = row, rk
            gapgu.append(row)
            if e.get("trust_no"):
                tr = _Row(purpose="신탁", trust_no=e["trust_no"])
                e["trust_row"] = tr
                gapgu.append(tr)
            if e.get("trust_cancel"):
                tgt = e["trust_cancel"]
                gapgu.append(_Row(purpose=f"{tgt['rank']}번신탁등기말소", cause="신탁재산의귀속"))
                tgt["trust_row"].struck = True
            # 소유 상태
            if e.get("partial"):
                for s in state:
                    s["share"] = "2분의 1"
                state += [{"pi": pi, "share": share, "rank": rk} for pi, share in owners]
                cause = "소유권일부이전"
            else:
                state = [{"pi": pi, "share": share or "단독소유", "rank": rk} for pi, share in owners]
                cause = "소유권보존" if e["purpose"] == "소유권보존" else "소유권이전"
            chain.append({"date": d, "cause": cause, "owners": [(pi, share) for pi, share in owners]})
        elif e["kind"] == "main":
            rank[e["sec"]] += 1
            rk = str(rank[e["sec"]])
            row = _Row(rank=rk, purpose=e["row"]["purpose"], receipt=receipt, **{k: v for k, v in e["row"].items() if k != "purpose"})
            e["row"], e["rank"] = row, rk
            e["owners_then"] = [s["pi"]["name"] for s in state]
            out.append(row)
        elif e["kind"] == "sub":
            tgt = e["target"]
            rk = f"{tgt['rank']}-{len(tgt['subs']) + 1}"
            row = _Row(rank=rk, purpose=f"{tgt['rank']}{e['tail']}", receipt=receipt, cause=e["cause"], **e["content"])
            tgt["subs"].append(row)
            out.append(row)
            if e.get("addr"):
                tgt["row"].addr_struck = True
                pi = next(s for s in tgt["owners"])[0]
                chain.append({"date": d, "cause": "주소변경", "owners": [(pi, None)]})
            if e.get("new_max"):
                tgt["cur_max"] = e["new_max"]
            if e.get("new_mortgagee"):
                tgt["cur_mortgagee"] = e["new_mortgagee"]
        else:  # cancel
            tgt = e["target"]
            rank[e["sec"]] += 1
            out.append(_Row(rank=str(rank[e["sec"]]), purpose=f"{tgt['rank']}{e['tail']}", receipt=receipt, cause=e["cause"]))
            tgt["row"].struck = True
            for s in tgt["subs"]:
                s.struck = True
            tgt["cancelled"] = True
    cur_names = [s["pi"]["name"] for s in state]
    open_gap = [e for e in evs if e["kind"] == "main" and e["sec"] == "gap" and not e.get("cancelled")]
    open_eul = [e for e in evs if e["kind"] == "main" and e["sec"] == "eul" and not e.get("cancelled")]
    seller_era = next(e for e in eras if e.get("seller"))
    # 계약 당시 매도인(임대인) 명의로 남아 있던 근저당·가압류 (계약서 특약용)
    def open_at(d: date) -> list[dict]:
        out = []
        for e in evs:
            if e["kind"] != "main" or e.get("type") not in ("mortgage", "seizure", "jeonse", "lease"):
                continue
            if e["date"] <= d and (e["end"] is None or e["end"] > d) and seller_era["start"] <= e["date"] < (seller_era["end"] or date.max):
                out.append(e)
        return out
    return {"gapgu": gapgu, "eulgu": eulgu, "state": state, "chain": chain, "cur_names": cur_names,
            "open_gap": open_gap, "open_eul": open_eul, "open_at": open_at, "heavy": H, "sp": sp,
            "co_seller": co_seller, "co_buyer": co_buyer}


def _unit_label(f: dict) -> str:
    """'래미안아파트 제101동 제12층 제1203호'"""
    s = f["bname"]
    if f["dong_no"]:
        s += f" 제{f['dong_no']}동"
    return f"{s} 제{f['floor']}층 제{f['ho']}호"


def _brokers(rng: random.Random, f: dict) -> list[dict]:
    """개업공인중개사 (공동중개면 매도인측·매수인측 2곳)."""
    out = [_broker(rng, f)]
    if special(rng, "co_broker", 0.35):
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
    """등기사항전부증명서(말소사항 포함) - 집합건물. 표제부·갑구·을구.

    이력이 많은 물건(소유권 이전·근저당 설정/말소 반복)은 갑구·을구가 길어져 여러 쪽이 된다.
    말소된 사항은 빨간 실선으로 지우고, 말소 등기('3번근저당권설정등기말소')는 별도 순위번호로 적는다."""
    f = _facts(p)
    a, pr, hist = f["a"], f["pr"], f["hist"]
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
    buildings = [_Row(display_no="1", receipt=_rd(f["preserve"]), location=loc_old if f["road_reg"] else loc,
                      detail=detail, cause=f["drawing_no"])]
    if f["road_reg"]:  # 도로명주소 직권 등기: 1번은 말소(실선), 2번에 도로명주소 추가
        buildings[0].struck = True
        buildings.append(_Row(display_no="2", location=loc, cause=f"도로명주소\n{_rd(f['road_reg'])} 등기"))
    land = {"display_no": "1", "location": f"1. {a.jibun_full}", "category": "대",
            "area": f"{_area(f['land_total'])}㎡", "cause": f"{_rd(f['preserve'])} 등기"}
    unit = {"display_no": "1", "receipt": _rd(f["preserve"]), "unit_no": f"제{f['floor']}층 제{f['ho']}호",
            "detail": f"{pr.structure}\n{_area(pr.exclusive_area)}㎡", "cause": f["drawing_no"]}
    land_right = {"display_no": "1", "kind": "1 소유권대지권", "ratio": f"{_area(f['land_total'])}분의 {_area(pr.land_area)}",
                  "cause": f"{_rd(f['land_right_date'])} 대지권\n{_rd(f['preserve'])} 등기"}
    t = view_dt
    hh, mm, ss = rng.randint(8, 18), rng.randint(0, 59), rng.randint(0, 59)
    out = {
        "unique_no": pr.unique_no,
        "property": f"{a.jibun_full} {_unit_label(f)}",
    }
    rows = len(hist["gapgu"]) * 3 + len(hist["eulgu"]) * 5
    pages = 1 + max(0, (rows - 30) // 70)  # 증명서 본문 쪽수 (요약 쪽 번호 표시용 어림)
    summary = rng.random() < 0.18  # 마지막 장: 주요 등기사항 요약 (참고용)
    if summary:
        out["summary"] = _registry_summary(hist)
        out["page_label"] = f"{pages + 1}/{pages + 1}"
    else:
        out.update({"registry_office": courthouse(a), "buildings": buildings, "land": land, "unit": unit, "land_right": land_right,
                    "gapgu": hist["gapgu"], "eulgu": hist["eulgu"]})
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


def _registry_summary(hist: dict) -> dict:
    """주요 등기사항 요약(참고용): 말소되지 않은 사항만."""
    owners = []
    for s in sorted(hist["state"], key=lambda s: s["pi"]["name"]):
        pi = s["pi"]
        owners.append({"name": f"{pi['name']} ({'소유자' if s['share'] == '단독소유' else '공유자'})", "reg_no": _reg_no(pi),
                       "share": s["share"], "address": pi["addr"], "rank": s["rank"]})
    target = ", ".join(hist["cur_names"]) if len(hist["cur_names"]) < 3 else f"{hist['cur_names'][0]} 등"

    def main_text(e: dict) -> str:
        row = e["row"]
        if e["type"] == "mortgage":
            mx = f"금{won(e['cur_max'])}" if e.get("cur_max") else row["max_amount"]
            who = (e.get("cur_mortgagee") or row["mortgagee"]).split()[0]
            return f"채권최고액 {mx}  근저당권자 {who}"
        if e["type"] == "jeonse":
            return f"전세금 {row['deposit']}  전세권자 {e['who']}"
        if e["type"] == "lease":
            return f"임차보증금 {row['deposit']}  임차권자 {e['who']}"
        if "claim_amount" in row:
            return f"청구금액 {row['claim_amount']}  채권자 {row['creditor'].split()[0]}"
        if "right_holder" in row:
            return f"권리자 {row['right_holder']}"
        return f"채권자 {row.get('creditor', '').split()[0]}"

    def items(evs: list) -> list:
        return [{"rank": e["rank"], "purpose": e["row"]["purpose"], "receipt": e["row"]["receipt"].replace("\n", " "),
                 "main": main_text(e), "target_owner": target} for e in sorted(evs, key=lambda e: int(e["rank"]))]
    return {"owners": owners, "gapgu_rights": items(hist["open_gap"]), "rights": items(hist["open_eul"])}


# ---------------------------------------------------------------------------
# 집합건축물대장(전유부, 갑)
# ---------------------------------------------------------------------------

def _share_frac(share: str | None) -> str:
    return {"2분의 1": "1/2", None: "1/1", "단독소유": "1/1"}.get(share, share)


@doc("building_register", "집합건축물대장(전유부)", "real_estate", page="a4_landscape")
def building_register(p: Profile, rng: random.Random) -> dict:
    """집합건축물대장(전유부, 갑) 등본.

    소유자 변동 이력이 많거나 공용부분이 많은 경우(heavy)는 표를 세로로 쌓아 여러 쪽이 된다."""
    f = _facts(p)
    a, pr, hist = f["a"], f["pr"], f["hist"]
    long_doc = heavy(rng, 0.25)
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
    if long_doc:  # 공용부분을 층·용도별로 잘게 나눠 적은 대장
        extra = ["경비실", "주민운동시설", "작은도서관", "어린이집", "경로당", "펌프실", "발전기실", "전기실", "쓰레기보관소",
                 "자전거보관소", "옥탑", "물탱크실", "피트층", "방재실", "커뮤니티시설", "옥상"]
        for u in rng.sample(extra, rng.randint(6, 12)):
            fl = "옥탑1층" if u in ("옥탑", "옥상", "물탱크실") else rng.choice(["지1층", "지2층", "1층", "1층"])
            common.append({"kind": rng.choice(["주", "부"]), "floor": fl, "structure": pr.structure, "usage": u,
                           "area": f"{pr.exclusive_area * rng.uniform(0.005, 0.06):.2f}"})
    # 공동주택가격: 매년 1월 1일 기준, 4월 말 공시
    y = p.issue_date.year if p.issue_date >= date(p.issue_date.year, 4, 30) else p.issue_date.year - 1
    prices, v = [], pr.official_price
    for yy in range(y, y - (rng.randint(6, 9) if long_doc else rng.randint(3, 4)), -1):
        prices.append({"base_date": f"{yy}.01.01", "price": won(v, "")})
        v = K.round_to(v / rng.uniform(1.0, 1.12), 1_000_000)
    ho_name = (f"{f['dong_no']}동 " if f["dong_no"] else "") + f"{f['ho']}호"

    def row(pi: dict, share, d: date, cause: str, addr_d: date | None = None) -> dict:
        return {"name": pi["name"], "rrn": pi["rrn"] if pi["corp"] else K.mask_rrn(pi["rrn"]),
                "address": _addr_at(pi, addr_d or d), "share": _share_frac(share), "change_date": D(d, "dot"),
                "change_cause": cause}
    full = long_doc or special(rng, "owner_history", 0.3) or len(hist["state"]) > 1
    owners = []
    if full:  # 소유자 변동 이력 전체
        cmap = {"소유권보존": "소유권보존", "소유권이전": "소유권이전", "소유권일부이전": "소유권일부이전", "주소변경": "등기명의인표시변경"}
        for c in hist["chain"]:
            for pi, share in c["owners"]:
                owners.append(row(pi, share, c["date"], cmap[c["cause"]], c["date"] + timedelta(days=1) if c["cause"] == "주소변경" else None))
        # 공유자 지분: 일부이전 뒤에는 기존 소유자 지분도 1/2 로 적힌다
        for s in hist["state"]:
            for o in owners:
                if o["name"] == s["pi"]["name"]:
                    o["share"] = _share_frac(s["share"])
    else:
        last = hist["chain"][-1]
        for s in hist["state"]:
            pi = s["pi"]
            d = max(c["date"] for c in hist["chain"] if any(x[0]["name"] == pi["name"] for x in c["owners"]))
            owners.append(row(pi, s["share"], d, "소유권이전" if last["cause"] != "소유권보존" else "소유권보존"))
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
        "owners": owners,
        "issue_date": D(p.issue_date, rng.choice(["kor", "kor_short"])),
        "officer": f"{rng.choice(['건축과', '건축행정과', '민원여권과', '종합민원과'])}",
        "officer_phone": K.landline(rng, a.sido),
        "issuer": district_office(a),
    }
    if not full:
        out["owners_note"] = "※ 이 건축물대장은 현소유자만 표시한 것입니다."
    if special(rng, "violation", 0.08):  # 위반건축물 표시 (발코니 불법확장·무단증축 등)
        out["violation"] = "위반건축물"
    if pr.kind != "오피스텔":  # 오피스텔은 공동주택가격 공시 대상이 아님
        out["house_prices"] = prices
    return out


# ---------------------------------------------------------------------------
# 토지대장
# ---------------------------------------------------------------------------

@doc("land_register", "토지대장", "real_estate")
def land_register(p: Profile, rng: random.Random) -> dict:
    """토지대장 등본 (집합건물 대지). 소유자 변동 이력이 길면 여러 쪽."""
    f = _facts(p)
    a, pr, hist = f["a"], f["pr"], f["hist"]
    land_rows = []
    d0 = f["preserve"] - timedelta(days=rng.randint(200, 900))
    if heavy(rng, 0.2):  # 분할·합병·지목변경이 거듭된 토지
        dd = d0 - timedelta(days=rng.randint(4000, 9000))
        area = f["land_total"] * rng.uniform(1.6, 2.4)
        for _ in range(rng.randint(3, 6)):
            dd += timedelta(days=rng.randint(200, 1500))
            if dd >= d0:
                break
            area = area * rng.uniform(0.8, 1.05)
            land_rows.append({"category": rng.choice(["(08)대", "(08)대", "(02)답", "(01)전", "(05)임야"]) if not land_rows else rng.choice(["(08)대", "(08)대", "(02)답"]),
                              "area": _area(round(area, 1)),
                              "reason": f"({rng.choice(['20', '30', '40', '42', '50'])}){D(dd, 'kor')}\n"
                                        + rng.choice(["분할되어 본번에 -%d을 부함" % rng.randint(1, 60), "지목변경", "등록전환",
                                                      "구획정리 완료", "합병", "면적정정", "행정구역명칭변경"])})
    elif rng.random() < 0.5:
        land_rows.append({"category": "(08)대", "area": _area(round(f["land_total"] * rng.uniform(1.05, 1.4), 1)),
                          "reason": f"({rng.choice(['20', '40'])}){D(d0 - timedelta(days=rng.randint(300, 3000)), 'kor')}\n"
                                    + rng.choice(["구획정리 완료", "지목변경", "등록전환"])})
    land_rows.append({"category": "(08)대", "area": _area(f["land_total"]),
                      "reason": f"(30){D(d0, 'kor')}\n분할되어 본번에 -{f['bubun'] or rng.randint(1, 30)}을 부함"
                      if land_rows or rng.random() < 0.5 else f"(40){D(d0, 'kor')}\n구획정리 완료"})
    code = {"소유권보존": "(01)소유권보존", "소유권이전": "(03)소유권이전", "소유권일부이전": "(04)소유권일부이전", "주소변경": "(11)주소변경"}
    owners = []
    for c in hist["chain"]:
        for pi, _ in c["owners"]:
            owners.append({"change_date": D(c["date"], "kor"), "change_cause": code[c["cause"]],
                           "address": _addr_at(pi, c["date"] + timedelta(days=1 if c["cause"] == "주소변경" else 0)),
                           "name": pi["name"], "reg_no": pi["rrn"] if pi["corp"] else K.mask_rrn(pi["rrn"])})
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
# 계약서 공통
# ---------------------------------------------------------------------------

def _amount(n: int) -> str:
    return f"금 {K.won_korean(n)}원정 (₩{n:,})"


def _party(per: Person, addr: str) -> dict:
    return {"address": addr, "rrn": per.rrn, "phone": per.mobile, "name": per.name}


def _agent(p: Profile, rng: random.Random, principal: Person) -> dict:
    """대리인 (위임장·인감증명서 지참). 보통 가족."""
    w = World(f"re-agent:{p.seed}:{principal.name}")
    ag = w.person(birth_range=(principal.birth.year - 8, min(principal.birth.year + 30, 2004)))
    rel = rng.choice(["배우자", "자녀", "형제", "부모"] if principal.birth.year < 1975 else ["배우자", "형제", "부모"])
    return {"address": ag.address.road_full, "rrn": ag.rrn, "name": ag.name, "relation": rel}


def _open_specials(f: dict, d: date, who: str) -> list[str]:
    """계약일 현재 매도인(임대인) 명의로 남아 있는 근저당·가압류 처리 특약."""
    out = []
    for e in f["hist"]["open_at"](d):
        row = e["row"]
        if e["type"] == "mortgage":
            out.append(f"{who}은 잔금 지급일까지 을구 {e['rank']}번 근저당권(채권최고액 {row['max_amount']}, "
                       f"{row['mortgagee'].split()[0]})을 말소하기로 하며, 잔금으로 상환할 수 있다.")
        elif e["type"] == "seizure" and row["purpose"] == "가압류":
            out.append(f"{who}은 잔금 지급일 전까지 갑구 {e['rank']}번 가압류({row['claim_amount']})를 해제하여 "
                       "말소하기로 하며, 이를 이행하지 않을 경우 매수인은 계약을 해제하고 계약금의 배액을 청구할 수 있다.")
    return out


_EXTRA_SPECIALS = [
    "잔금일 기준으로 관리비 및 제세공과금은 매도인이 정산한다.",
    "매도인은 잔금일까지 임차인 없이 명도하기로 한다.",
    "본 계약 이후 매도인은 추가 담보 설정이나 임대를 하지 않는다.",
    "옵션(빌트인 가전 등)은 현 상태로 포함하여 매도한다.",
    "누수 등 중대한 하자는 잔금일 이후 6개월 이내 매도인이 책임진다.",
    "장기수선충당금은 매수인이 매도인에게 잔금일에 별도로 지급한다.",
    "매수인의 대출이 금융기관 사정으로 부결될 경우 계약금은 반환하고 계약은 해제한다.",
    "확장공사 부분 및 붙박이장, 시스템에어컨(거실·안방) 등은 매매대금에 포함한다.",
    "매도인은 잔금일 전 매수인의 인테리어 공사를 위한 출입에 협조한다.",
    "현관 도어락 비밀번호 및 공동현관 카드키 2개는 잔금일에 인계한다.",
    "전입세대 열람 결과 매도인 세대 외 전입자가 있을 경우 매도인이 잔금일까지 전출시킨다.",
    "주차장 지정 1대는 현 상태대로 승계한다.",
    "매도인은 국세·지방세 완납증명서를 잔금일에 제시한다.",
    "본 계약서에 명시되지 않은 사항은 민법 및 부동산 거래 관례에 따른다.",
    "계약금 중 일부(금 일천만원정)는 가계약금으로 이미 수령하였음을 확인한다.",
    "매수인은 잔금일 전 현장을 다시 확인할 수 있으며, 이때 발견된 하자는 쌍방 협의하여 처리한다.",
    "베란다 결로·곰팡이 부분은 현 상태로 인정하고 매수한다.",
    "매도인의 이사 일정상 잔금일은 쌍방 합의로 1주일 범위에서 조정할 수 있다.",
]
_HAND_SPECIALS = ["잔금일에 관리비 선수관리비 정산함.", "거실 에어컨 1대 두고 감.", "잔금일 오전 중 이사 완료 조건.",
                  "중도금 없이 잔금 일시 지급.", "도배는 매수인이 진행함.", "보일러 점검 후 이상 시 매도인 수리."]


# ---------------------------------------------------------------------------
# 부동산(아파트) 매매계약서
# ---------------------------------------------------------------------------

@doc("sales_contract", "부동산 매매계약서", "real_estate")
def sales_contract(p: Profile, rng: random.Random) -> dict:
    """부동산(아파트) 매매계약서 (공인중개사 중개)."""
    f = _facts(p)
    a, pr, seller, hist = f["a"], f["pr"], f["pr"].seller, f["hist"]
    dfmt = rng.choice(["kor", "kor_short"])
    pay = {"price": _amount(f["price"]), "down": _amount(f["down"])}
    if f["middle"]:
        pay["middle"] = _amount(f["middle_amt"])
        pay["middle_date"] = D(f["middle"], dfmt)
    pay["balance"] = _amount(f["balance_amt"])
    pay["balance_date"] = D(f["balance"], dfmt)
    specials = ["현 시설물 상태의 계약이며, 매수인은 등기사항증명서 및 현장을 확인하고 계약함."]
    specials += _open_specials(f, f["contract"], "매도인")
    specials.append(f"매수인은 {p.bank} 주택담보대출로 잔금 일부를 지급할 예정이며, 매도인은 이에 협조한다.")
    long_doc = heavy(rng, 0.25)  # 특약이 많아 여러 쪽이 되는 계약서
    specials += rng.sample(_EXTRA_SPECIALS, rng.randint(9, 16) if long_doc else rng.randint(1, 2))
    co_s, co_b = hist["co_seller"], hist["co_buyer"]
    if co_s:
        specials.append(f"본 부동산은 매도인 {seller.name}, {co_s.name}의 공유(각 2분의 1)이며, 공유자 전원이 계약한다.")
    if co_b:
        specials.append(f"매수인 {p.person.name}, {_eun(co_b.name)} 각 2분의 1 지분으로 공동 매수한다.")
    out = {
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
        "contract_date": D(f["contract"], dfmt),
        "seller": _party(seller, f["seller_addr"]),
        "buyer": _party(p.person, p.person.address.road_full),
        "brokers": _brokers(rng, f),
    }
    if co_s:
        out["co_seller"] = _party(co_s, f["seller_addr"])
    if co_b:
        out["co_buyer"] = _party(co_b, p.person.address.road_full)
    if special(rng, "agent", 0.1):  # 매도인 대리 계약
        ag = _agent(p, rng, seller)
        out["seller_agent"] = {k: ag[k] for k in ("address", "rrn", "name")}
        specials.append(f"매도인의 {ag['relation']} {_iga(ag['name'])} 매도인의 위임장 및 인감증명서를 지참하여 대리 계약하며, "
                        "잔금일에 매도인 본인이 참석하여 확인한다.")
    specials = [f"{i + 1}. {s}" for i, s in enumerate(specials)]
    if special(rng, "hand_special", 0.12):  # 계약 현장에서 손으로 덧붙인 특약
        specials.append(_Hand(f"{len(specials) + 1}. {rng.choice(_HAND_SPECIALS)}"))
    out["specials"] = specials
    return out


# ---------------------------------------------------------------------------
# 주택임대차표준계약서 (전세)
# ---------------------------------------------------------------------------

_LEASE_EXTRA = ["반려동물 사육은 임대인의 동의를 받아야 한다.", "벽걸이TV, 못 자국 등 경미한 훼손은 원상복구 대상에서 제외한다.",
                "관리비는 실사용 기준으로 임차인이 부담한다.", "도배·장판은 잔금일 전까지 임대인이 교체하여 준다.",
                "임대인은 임차인의 전세보증금반환보증 가입에 협조한다.", "임대인은 잔금일까지 국세·지방세 완납증명서를 임차인에게 제시한다.",
                "계약기간 중 임대인이 주택을 매도하는 경우 임대인은 매수인에게 본 계약의 승계를 고지한다.",
                "보일러·수전 등 노후로 인한 고장은 임대인이 수리하고, 임차인 과실로 인한 고장은 임차인이 부담한다.",
                "임차인은 입주 전 시설 상태를 사진으로 촬영하여 임대인과 공유한다.",
                "계약 만료 2개월 전까지 쌍방 의사표시가 없으면 동일 조건으로 갱신된 것으로 본다.",
                "흡연은 세대 내 및 베란다에서 금지한다.", "현관 도어락 비밀번호는 입주일에 변경한다.",
                "임대인은 보증금 반환 시 관리비 정산금을 공제할 수 있다.", "에어컨 실외기 설치 위치는 관리사무소 규정을 따른다.",
                "임차인은 전입신고 및 확정일자를 잔금일 당일에 받기로 한다."]


@doc("lease_contract", "주택임대차표준계약서", "real_estate")
def lease_contract(p: Profile, rng: random.Random) -> dict:
    """주택임대차표준계약서 (전세). 임대인 = 기존 소유자(seller), 임차인 = 본인."""
    f = _facts(p)
    a, pr, lord, hist = f["a"], f["pr"], f["pr"].seller, f["hist"]
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
    if not f["transferred"]:
        specials += [s.replace("잔금 지급일까지", "잔금일까지").replace(", 잔금으로 상환할 수 있다", "")
                     .replace("매수인은 계약을 해제하고", "임차인은 계약을 해제하고") for s in _open_specials(f, cdate, "임대인")]
    long_doc = heavy(rng, 0.2)
    specials += rng.sample(_LEASE_EXTRA, rng.randint(8, 13) if long_doc else int(rng.random() < 0.3))
    co_l = hist["co_seller"] if not f["transferred"] else None
    out = {
        "landlord_name": lord.name + (f", {co_l.name}" if co_l else ""), "tenant_name": p.person.name,
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
        "contract_date": D(cdate, dfmt),
        "landlord": _party(lord, f["seller_addr"]),
        "tenant": _party(p.person, p.person.address.road_full),
        "brokers": _brokers(rng, f),
    }
    if co_l:
        out["co_landlord"] = _party(co_l, f["seller_addr"])
        specials.append(f"본 주택은 임대인 {lord.name}, {co_l.name}의 공유이며, 보증금 반환 의무는 공유자 전원이 연대하여 부담한다.")
    if special(rng, "agent", 0.12):  # 임대인 대리 계약 (해외 거주·고령 등)
        ag = _agent(p, rng, lord)
        out["landlord_agent"] = {k: ag[k] for k in ("address", "rrn", "name")}
        specials.append(f"임대인의 {ag['relation']} {_iga(ag['name'])} 임대인의 위임장 및 인감증명서를 지참하여 대리 계약하며, "
                        "보증금은 임대인 명의 계좌로만 입금한다.")
    specials = [f"{i + 1}. {s}" for i, s in enumerate(specials)]
    if special(rng, "hand_special", 0.12):
        specials.append(_Hand(f"{len(specials) + 1}. " + rng.choice(["입주청소 후 입주.", "잔금일 오전 중 열쇠 인계.",
                                                                  "현관 센서등 교체해 줌.", "주차 1대 등록 가능."])))
    out["specials"] = specials
    return out


# ---------------------------------------------------------------------------
# 전입세대확인서
# ---------------------------------------------------------------------------

@doc("move_in_household_list", "전입세대확인서", "real_estate")
def move_in_household_list(p: Profile, rng: random.Random) -> dict:
    """전입세대확인서(열람). 해당 주소에 전입신고된 세대주 목록.

    다세대·오피스텔을 건물 전체(동·호 없이)로 열람하면 여러 세대가 나오고, 많으면 여러 쪽이 된다."""
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
    long_doc = heavy(rng, 0.2)
    multi = pr.kind != "아파트" and (long_doc or special(rng, "multi_household", 0.15))
    cohab_case = special(rng, "cohabitant", 0.12)
    unknown = special(rng, "unknown_resident", 0.05)  # 거주불명자 등록 세대
    units = [(f["ho"], nm, d) for nm, d in heads]
    if multi:  # 같은 건물 다른 호실 세대
        n = rng.randint(14, 28) if long_doc else rng.randint(4, 9)
        per_floor = max(2, f["units_per_floor"])
        floors = max(2, f["total_floors"])
        cand = [f"{fl}{i:02d}" for fl in range(1, floors + 1) for i in range(1, per_floor + 1)]
        if pr.kind == "다세대주택" and rng.random() < 0.5:
            cand += [f"B{i:02d}" for i in range(1, per_floor + 1)]
        cand = [c for c in cand if c != f["ho"]]
        for ho in rng.sample(cand, min(n, len(cand))):
            units.append((ho, _rand_person(rng), p.issue_date - timedelta(days=rng.randint(10, 3600))))
            if rng.random() < 0.1:  # 한 호실에 세대가 둘
                units.append((ho, _rand_person(rng), p.issue_date - timedelta(days=rng.randint(10, 2000))))
        units.sort(key=lambda u: (not u[0].startswith("B"), int(u[0].lstrip("B")), u[2]))
    cohab = []
    for i, (ho, nm, d) in enumerate(units):
        first_same = rng.random() < 0.75
        first_nm, first_d = (nm, d) if first_same else (_rand_person(rng), d - timedelta(days=rng.randint(0, 3)))
        n_co = 1 if rng.random() < 0.15 else 0  # 주민등록표상 동거인(세대원 아님)은 드묾
        if cohab_case and ho == f["ho"] and i == next(j for j, u in enumerate(units) if u[0] == f["ho"]):
            n_co = rng.randint(1, 2)
        reg = "거주불명자" if unknown and i == len(units) - 1 and len(units) > 1 else "거주자"
        row = {"no": str(i + 1), "head_name": _mask_name(nm), "move_in_date": D(min(d, p.issue_date), "dash"),
               "reg_type": reg, "first_name": _mask_name(first_nm), "first_date": D(min(first_d, p.issue_date), "dash"),
               "first_reg_type": reg, "cohabitants": str(n_co)}
        if multi:
            row = {"no": row["no"], "unit": f"{ho}호", **{k: v for k, v in row.items() if k != "no"}}
        rows.append(row)
        for _ in range(n_co):
            cd = min(d + timedelta(days=rng.randint(30, 900)), p.issue_date)
            cohab.append({"no": str(len(cohab) + 1), "name": _mask_name(_rand_person(rng)), "move_in_date": D(cd, "dash"),
                          "reg_type": "거주자"})
    purpose = rng.choice(["금융기관 대출(주택담보대출)", "금융기관 제출", "전세자금대출 신청", "임대차계약 체결"])
    jibun = f"{a.jibun_full} " + (f"{f['dong_no']}동 " if f["dong_no"] else "") + f"{f['ho']}호"
    road = a.road_full
    if multi:  # 건물 전체 열람: 동·호 없이
        jibun = a.jibun_full
        road = f"{a.region} {a.road} {a.building_no} ({a.dong}" + (f", {a.building_name})" if a.building_name else ")")
    return {
        "issue_no": issue_no(rng, 16),
        "issue_date": D(p.issue_date, "dot"),
        "address": road,
        "jibun_address": jibun,
        "households": rows,
        **({"cohabitants": cohab} if cohab else {}),
        "kind": rng.choice(["열람", "교부", "교부"]),
        "applicant": {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn), "address": p.person.address.road_full,
                      "purpose": purpose},
        "view_date": D(p.issue_date, "kor"),
        "issuer": community_center(a),
    }
