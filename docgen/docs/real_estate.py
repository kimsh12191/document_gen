"""부동산 관련 서류: 등기사항전부증명서, 건축물대장, 토지대장, 매매계약서, 임대차계약서, 전입세대확인서.

이 파일에는 그룹 서식들이 같이 쓰는 도우미만 있다. 서식마다 값 만드는 함수(@doc)는 서식 폴더
docgen/forms/<ID>/generate.py 에 있고, 끝의 FORMS 차례로 등록한다.

같은 프로필이면 서류 사이의 사실관계(매매일, 근저당, 소유권 이전 여부, 공유자 등)가 맞도록
`_facts(p)`가 프로필 seed 로부터 결정론적으로 공통 사실을 만든다.
매도인 = p.property.seller (기존 소유자), 매수인/임차인 = p.person.

등기 이력(`_history`)도 `_facts` 안에서 만든다. 소유자가 여러 번 바뀌거나 근저당 설정·말소가 반복되는
'이력이 많은 물건'(heavy)과 공유·신탁·가압류·전세권 같은 특수 상황은 프로필 단위로 정해지므로
등기부·토지대장·건축물대장·계약서가 서로 어긋나지 않는다.
"""
import re

from ..entities import World
from ._common import *  # noqa: F401,F403
from ..registry import register_folder_forms

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
    a, seller = f["a"], f["pr"].seller
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


# ---------------------------------------------------------------------------
# 집합건축물대장(전유부, 갑)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 토지대장
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# 부동산(아파트) 매매계약서
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 주택임대차표준계약서 (전세)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 전입세대확인서
# ---------------------------------------------------------------------------


# 이 그룹의 코드 서식. 값 만드는 함수는 서식 폴더 docgen/forms/<ID>/generate.py 에 있다 (여기는 같이 쓰는 도우미).
FORMS = ('real_estate_registry', 'building_register', 'land_register', 'sales_contract', 'lease_contract', 'move_in_household_list',)
register_folder_forms(__name__, FORMS)   # 예전 @doc 차례 그대로 등록 (서식 목록·데이터셋 순서)
