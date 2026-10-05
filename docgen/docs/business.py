"""개인사업자·법인사업자 등록 및 재무 관련 서류 (국세청 발급).

개인사업체(p.business)의 연도별 매출·손익·재무상태는 _pl()/_bs() 로 계산한다.
이 값은 p.seed 에서 파생한 난수로 만들기 때문에 서류(표준재무제표증명, 부가가치세 과세표준증명,
종합소득세 신고서 등)가 달라도 같은 고객이면 같은 숫자가 나온다.
"""
import os

from ..entities import COMPANY_PREFIX, World
from ..registry import doc
from ._common import *  # noqa: F401,F403

# ---------------------------------------------------------------------------
# 업종 정보: 종목 → (매출원가율 범위, 간이과세 업종별 부가가치율, 업종코드, 복식부기의무 기준 매출액)
# ---------------------------------------------------------------------------
_INDUSTRY = {
    "한식": ((0.34, 0.44), 0.15, "552101", 150_000_000),
    "전자상거래": ((0.58, 0.74), 0.15, "525101", 300_000_000),
    "미용": ((0.08, 0.18), 0.30, "930201", 75_000_000),
    "편의점": ((0.72, 0.80), 0.15, "521300", 300_000_000),
    "학원": ((0.04, 0.12), 0.30, "809009", 75_000_000),
    "커피전문점": ((0.30, 0.40), 0.15, "552303", 150_000_000),
    "인테리어": ((0.55, 0.70), 0.30, "452106", 150_000_000),
    "제과": ((0.40, 0.50), 0.20, "158100", 150_000_000),
    "세무대리": ((0.00, 0.05), 0.40, "741201", 75_000_000),
    "농산물": ((0.80, 0.88), 0.15, "512101", 300_000_000),
}
_DEFAULT_INDUSTRY = ((0.40, 0.60), 0.20, "749909", 150_000_000)
_SECONDARY = [("소매업", "전자상거래", "525101"), ("도매업", "기타 도매", "513999"), ("서비스업", "기타 서비스", "749909")]

SIMPLE_TAX_LIMIT = 104_000_000  # 간이과세 기준 공급대가 (2024.7.1 이후)


def _industry(b) -> tuple:
    return _INDUSTRY.get(b.biz_item, _DEFAULT_INDUSTRY)


def _prng(p: Profile, *keys) -> random.Random:
    """프로필 고정 난수. 같은 고객의 여러 서류에서 같은 값이 나와야 하는 수치에 쓴다."""
    return random.Random(":".join(["biz", str(p.seed), *map(str, keys)]))


def _vat_simple(p: Profile) -> bool:
    """간이과세자 여부."""
    return p.business.revenue < SIMPLE_TAX_LIMIT


def _bookkeeping_double(p: Profile) -> bool:
    """복식부기의무자 여부."""
    return p.business.revenue >= _industry(p.business)[3]


def _hometax_no(rng: random.Random) -> str:
    """홈택스 민원증명 발급번호 '1234-567-8901-234'."""
    return f"{rng.randint(1000, 9999)}-{rng.randint(100, 999)}-{rng.randint(1000, 9999)}-{rng.randint(100, 999)}"


def _filed_year(p: Profile) -> int:
    """발급일 기준 종합소득세 신고(5월)가 끝난 가장 최근 귀속연도."""
    return p.issue_date.year - 1 if p.issue_date >= date(p.issue_date.year, 6, 1) else p.issue_date.year - 2


def _sincere_filer(p: Profile) -> bool:
    """성실신고확인대상 여부 (복식부기 기준 수입금액의 5배 이상으로 근사)."""
    return p.business.revenue >= _industry(p.business)[3] * 5


def _itr_filed_date(p: Profile, y: int) -> date:
    """y년 귀속 종합소득세 신고일. 신고서·표준재무제표증명이 같은 날짜를 쓰도록 프로필 고정 난수로 만든다."""
    deadline = date(y + 1, 6, 30) if _bookkeeping_double(p) and _sincere_filer(p) else date(y + 1, 5, 31)
    filed = rand_date(_prng(p, "itr_filed", y), date(y + 1, 5, 2), deadline)
    return max(date(y + 1, 5, 2), min(filed, p.issue_date - timedelta(days=1)))  # 발급일 이후 신고는 불가


def _revenue_raw(p: Profile, y: int) -> int:
    """y년 매출액(공급가액, 휴업 반영 전). 기준연도(발급연도-1)는 p.business.revenue 에 맞춘다."""
    b = p.business
    if y < b.established.year:
        return 0
    ref = p.issue_date.year - 1
    g = _prng(p, "growth").uniform(-0.03, 0.10)
    r = _prng(p, "rev", y)
    noise = r.uniform(0.995, 1.005) if y == ref else r.uniform(0.95, 1.05)
    rev = b.revenue * (1 + g) ** (y - ref) * noise
    if y == b.established.year:
        rev *= (12 - b.established.month + 0.5) / 12
    return int(rev) // 10 * 10


def _half_share(p: Profile, y: int) -> float:
    """y년 매출 중 1기(1~6월) 비중."""
    b = p.business
    if y == b.established.year:
        if b.established.month > 6:
            return 0.0
        return (6.5 - b.established.month) / (12.5 - b.established.month)
    return _prng(p, "half", y).uniform(0.44, 0.55)


def _half_base(p: Profile, y: int, h: int) -> int:
    """y년 h기(1: 1~6월, 2: 7~12월) 매출. 휴업기간(_biz_facts suspended)만큼 줄어든다."""
    raw = _revenue_raw(p, y)
    h1 = int(raw * _half_share(p, y)) // 10 * 10
    base = h1 if h == 1 else raw - h1
    start, end = (date(y, 1, 1), date(y, 6, 30)) if h == 1 else (date(y, 7, 1), date(y, 12, 31))
    return int(base * _active_ratio(p, start, end)) // 10 * 10


def _revenue(p: Profile, y: int) -> int:
    """y년 매출액(공급가액) = 1기 + 2기."""
    return _half_base(p, y, 1) + _half_base(p, y, 2)


def _pl(p: Profile, y: int) -> dict:
    """y년 표준손익계산서 (정수 금액)."""
    r = _prng(p, "pl", y)
    rev = _revenue(p, y)
    lo, hi = _industry(p.business)[0]
    cogs = int(rev * r.uniform(lo, hi))
    gross = rev - cogs
    margin = min(r.uniform(0.07, 0.22), gross / max(rev, 1) - 0.05)
    op = int(rev * max(margin, 0.03))
    sga = gross - op
    emp = p.business.employees
    w = {
        "salary": r.uniform(3, 6) * min(emp, 4) / 2 if emp else 0.0,
        "rent": r.uniform(1.5, 3.0),
        "depreciation": r.uniform(0.4, 1.2),
        "other_sga": r.uniform(1.0, 2.5),
    }
    w["welfare"] = w["salary"] * 0.12
    tot = sum(w.values())
    parts = {k: int(sga * v / tot) // 10 * 10 for k, v in w.items() if k != "other_sga"}
    parts["other_sga"] = sga - sum(parts.values())
    noi = int(rev * r.uniform(0.0005, 0.006))
    noe = int(rev * r.uniform(0.002, 0.018))
    return {"revenue": rev, "cogs": cogs, "gross": gross, "sga": sga, **parts, "op": op,
            "non_op_income": noi, "non_op_expense": noe, "net": op + noi - noe}


def _bs(p: Profile, y: int) -> dict:
    """y년말 표준재무상태표 (정수 금액)."""
    r = _prng(p, "bs", y)
    rev = max(_revenue(p, y), 10_000_000)
    assets = int(rev * r.uniform(0.35, 1.1)) // 1000 * 1000 + r.randint(0, 999)
    cur = int(assets * r.uniform(0.35, 0.65))
    cogs_ratio = _pl(p, y)["cogs"] / rev
    inventory = int(cur * r.uniform(0.1, 0.45) * min(1.0, cogs_ratio * 1.4))
    quick = cur - inventory
    noncur = assets - cur
    invest = int(noncur * r.uniform(0.0, 0.12))
    intangible = int(noncur * r.uniform(0.0, 0.05))
    other_nc = int(noncur * r.uniform(0.15, 0.4))  # 임차보증금 등
    tangible = noncur - invest - intangible - other_nc
    liab = int(assets * r.uniform(0.3, 0.8))
    cur_liab = int(liab * r.uniform(0.3, 0.7))
    return {"current": cur, "quick": quick, "inventory": inventory, "noncurrent": noncur,
            "investment": invest, "tangible": tangible, "intangible": intangible, "other_noncurrent": other_nc,
            "assets": assets, "current_liab": cur_liab, "noncurrent_liab": liab - cur_liab, "liabilities": liab,
            "capital": assets - liab, "equity": assets - liab, "liab_equity": assets}


def _tax_office(addr: Address) -> str:
    """관할 세무서장. 공용 tax_office() 가 한 글자 이름(예: '달세무서장')을 만들면 '울산남부세무서장' 식으로 보정."""
    name = tax_office(addr)
    if len(name) >= 6:
        return name
    last = addr.sigungu.split()[-1] if addr.sigungu else addr.sido
    return f"{K.sido_short(addr.sido)}{last[:-1]}{'부' if len(last) == 2 else ''}세무서장"


def _side_person(seed: str, gender=None) -> Person:
    """프로필에 없는 인물(공동사업자·세무대리인 등)을 seed 문자열로 결정론적으로 만든다."""
    w = World(0)
    w.rng = random.Random(seed)
    return w.person(gender=gender, birth_range=(1960, 1996))


# ---------------------------------------------------------------------------
# 프로필 고정 변형 (사업자등록증·사업자등록증명·부가세 과세표준증명·종합소득세 신고서·표준재무제표증명 공통)
# ---------------------------------------------------------------------------
# 주업종별로 흔히 추가 등록하는 부업종 (업태, 종목, 업종코드)
_SECONDARY_BY = {
    "한식": [("소매업", "전자상거래", "525101"), ("음식점업", "기타 외국식", "552107")],
    "전자상거래": [("도매업", "기타 도매", "513999"), ("서비스업", "광고 대행", "743002")],
    "미용": [("소매업", "화장품", "523311"), ("서비스업", "피부미용", "930202")],
    "편의점": [("소매업", "담배", "522604"), ("서비스업", "택배 대리점", "630401")],
    "학원": [("출판업", "교재 출판", "221100"), ("서비스업", "온라인 교육", "809005")],
    "커피전문점": [("제조업", "제과", "158100"), ("소매업", "전자상거래", "525101")],
    "인테리어": [("건설업", "실내건축", "452106"), ("도매업", "건축자재", "513320")],
    "제과": [("음식점업", "커피전문점", "552303"), ("소매업", "전자상거래", "525101")],
    "세무대리": [("서비스업", "경영컨설팅", "741400")],
    "농산물": [("소매업", "전자상거래", "525101"), ("소매업", "과실 및 채소", "522102")],
}
_FACTS_CACHE: dict = {}


def _biz_facts(p: Profile) -> dict:
    """개인사업체 프로필 고정 변형. 같은 고객이면 사업자등록증·사업자등록증명·부가세 과세표준증명·
    종합소득세 신고서·표준재무제표증명이 같은 사실을 쓴다.

      special joint_business     공동사업자 (배우자 또는 지인, 손익분배비율)
      special biz_moved          사업장 이전 (사업자등록증 정정 교부)
      special biz_added          업종 추가 (부업종)
      special simple_to_general  간이과세자 → 일반과세자 전환 (현재 일반과세자만)
      special trade_renamed      상호 변경
      special biz_suspended      휴업 후 재개 (휴업기간 매출 없음 → 부가세 무실적·감소)
    """
    b = p.business
    ck = (p.seed, b.biz_no, p.issue_date, os.environ.get("DOCGEN_SPECIAL", ""), os.environ.get("DOCGEN_HEAVY", ""))
    if ck in _FACTS_CACHE:
        return _FACTS_CACHE[ck]
    r = _prng(p, "facts")
    est, lim = b.established, p.issue_date - timedelta(days=30)
    fx = {"joint": None, "moved": None, "added": None, "switch": None, "renamed": None, "suspended": None}

    def when(after: int):
        lo = est + timedelta(days=after)
        return rand_date(r, lo, lim) if lo < lim else None

    if special(r, "joint_business", 0.08):
        if p.spouse and r.random() < 0.6:
            mate, relation = p.spouse, "배우자"
        else:
            mate, relation = _side_person(f"biz-partner:{p.seed}"), "기타"
        own = r.choice([50, 50, 60, 70])
        fx["joint"] = {"name": mate.name, "rrn": mate.rrn, "share": 100 - own, "own_share": own, "relation": relation}
    if special(r, "biz_moved", 0.12) and (d := when(300)):
        w = World(0)
        w.rng = random.Random(f"biz-old-office:{p.seed}")
        region = next((x for x in K.REGIONS if x[0] == b.address.sido and x[1] == b.address.sigungu), None)
        fx["moved"] = {"date": d, "old_address": w.address("office", region if r.random() < 0.7 else None)}
    if special(r, "biz_added", 0.15) and (d := when(200)):
        cands = _SECONDARY_BY.get(b.biz_item) or [s for s in _SECONDARY if s[1] != b.biz_item]
        t, i, c = r.choice(cands)
        fx["added"] = {"date": d, "biz_type": t, "biz_item": i, "code": c}
    if not _vat_simple(p) and special(r, "simple_to_general", 0.12):
        ys = [y for y in range(est.year + 1, p.issue_date.year + 1) if date(y, 7, 1) < lim]
        if ys:
            fx["switch"] = date(r.choice(ys[-3:]), 7, 1)
    if special(r, "trade_renamed", 0.06) and (d := when(300)):
        pre = next((x for x in sorted(COMPANY_PREFIX, key=len, reverse=True) if b.name.startswith(x)), None)
        rest = b.name[len(pre):] if pre else b.name[-2:]
        old = r.choice([x for x in COMPANY_PREFIX if x != pre]) + rest
        fx["renamed"] = {"date": d, "old_name": old}
    if special(r, "biz_suspended", 0.05):
        lo = max(est + timedelta(days=300), p.issue_date - timedelta(days=3 * 365))
        hi = lim - timedelta(days=240)
        if lo < hi:
            s = rand_date(r, lo, hi)
            fx["suspended"] = {"start": s, "end": s + timedelta(days=r.randint(60, 200))}
    _FACTS_CACHE[ck] = fx
    return fx


def _active_ratio(p: Profile, start: date, end: date) -> float:
    """start~end 중 휴업하지 않은 날의 비율."""
    sus = _biz_facts(p)["suspended"]
    if not sus or end < start:
        return 1.0
    lo, hi = max(start, sus["start"]), min(end, sus["end"])
    off = max(0, (hi - lo).days + 1)
    ratio = 1 - off / ((end - start).days + 1)
    return 0.0 if ratio < 0.12 else ratio


def _itr_filing(p: Profile, y: int) -> dict:
    """y년 귀속 종합소득세 신고 구분과 신고일 (프로필 고정). 표준재무제표증명과 같은 값을 쓴다.

      special itr_late          기한후신고
      special itr_amended       수정신고 (정기신고 뒤 과소신고분 추가 납부)
      special itr_refund_claim  경정청구 (정기신고 뒤 공제 누락분 환급 청구)
    """
    r = _prng(p, "itr_kind", y)
    base = _itr_filed_date(p, y)
    deadline = date(y + 1, 6, 30) if _bookkeeping_double(p) and _sincere_filer(p) else date(y + 1, 5, 31)
    lim = p.issue_date - timedelta(days=1)
    late, amended, claim = special(r, "itr_late", 0.05), special(r, "itr_amended", 0.07), special(r, "itr_refund_claim", 0.05)
    gap = r.randint(5, 80), r.randint(60, 300), r.randint(60, 400)
    if late and deadline + timedelta(days=gap[0]) <= lim:
        return {"kind": "기한후신고", "filed": deadline + timedelta(days=gap[0]), "original": None, "late_days": gap[0]}
    if amended and base + timedelta(days=gap[1]) <= lim:
        return {"kind": "수정신고", "filed": base + timedelta(days=gap[1]), "original": base}
    if claim and base + timedelta(days=gap[2]) <= lim:
        return {"kind": "경정청구", "filed": base + timedelta(days=gap[2]), "original": base}
    return {"kind": "정기신고", "filed": base, "original": None}


def _cert_date(rng: random.Random):
    """사업자등록증 날짜 표기. 실물은 '2020 년 01 월 05 일'처럼 단위 앞뒤를 띄운다."""
    style = rng.choice(["spaced", "spaced", "kor"])
    if style == "spaced":
        return lambda d: f"{d.year} 년 {d.month:02d} 월 {d.day:02d} 일"
    return lambda d: D(d, "kor")


def _biz_kind_label(p: Profile) -> str:
    return "간이과세자" if _vat_simple(p) else "일반과세자"


def _purpose(rng: random.Random, p: Profile) -> tuple[str, str]:
    return (rng.choice(["금융기관 제출", "대출 신청", "금융기관 제출용", "은행 제출"]),
            rng.choice([p.bank, f"{p.bank} {p.bank_branch}", "금융기관"]))


def _reissue(rng: random.Random, events: list, est: date, issue: date) -> tuple[str, date, str]:
    """사업자등록증 발급사유·발급일. events: [(날짜, '정정(…)')]. 정정 사유가 있으면 대개 마지막 정정 때 받은 증,
    아니면 그 뒤 재발급. 정정이 없으면 신규/재발급. 반환: (발급사유, 발급일, 정정 사유 또는 '')."""
    events = sorted(e for e in events if e[0] and e[0] < issue - timedelta(days=2))
    if events:
        d, why = events[-1]
        issued = min(d + timedelta(days=rng.randint(0, 10)), issue - timedelta(days=1))
        later = d + timedelta(days=60)
        if rng.random() < 0.15 and later < issue - timedelta(days=3):
            return "재발급", rand_date(rng, later, issue - timedelta(days=3)), why
        return why, issued, why
    reason = rng.choices(["신규", "재발급"], [5, 3])[0]
    if reason == "신규":
        return reason, est + timedelta(days=rng.randint(0, 12)), ""
    return reason, rand_date(rng, est + timedelta(days=200), issue - timedelta(days=3)), ""


# ---------------------------------------------------------------------------
# 사업자등록증 (개인)
# ---------------------------------------------------------------------------
@doc("business_registration_certificate", "사업자등록증", "business")
def business_registration_certificate(p: Profile, rng: random.Random) -> dict:
    """세무서가 발급하는 개인사업자 사업자등록증.

    정정 교부(사업장 이전·업종 추가·과세유형 전환·상호 변경)와 공동사업자는 _biz_facts() 의 프로필 고정 사실을 따른다.
    """
    b, fx = p.business, _biz_facts(p)
    events = []
    if fx["moved"]:
        events.append((fx["moved"]["date"], "정정(사업장 소재지 변경)"))
    if fx["added"]:
        events.append((fx["added"]["date"], "정정(업종 추가)"))
    if fx["switch"]:
        events.append((fx["switch"], "정정(과세유형 전환)"))
    if fx["renamed"]:
        events.append((fx["renamed"]["date"], "정정(상호 변경)"))
    reason, issued, _ = _reissue(rng, events, b.established, p.issue_date)
    fd = _cert_date(rng)
    out = {
        "kind": _biz_kind_label(p),
        "biz_no": b.biz_no,
        "trade_name": b.name,
        "name": p.person.name,
        "birth": fd(p.person.birth),
        "opened": fd(b.established),
        "address": b.address.road_full,
        "biz_type": b.biz_type,
        "biz_item": b.biz_item,
        "issue_reason": reason,
        "co_owner": fx["joint"]["name"] if fx["joint"] else None,
        "unit_taxation": "부",
        "issue_date": fd(issued),
        "issuer": _tax_office(b.address),
    }
    if fx["added"] and fx["added"]["date"] <= issued:
        out["sub_kinds"] = [{"biz_type": fx["added"]["biz_type"], "biz_item": fx["added"]["biz_item"]}]
    if rng.random() < 0.4:
        out["einvoice_email"] = rng.choice([p.person.email, b.email])
    return out


# ---------------------------------------------------------------------------
# 사업자등록증 (법인)
# ---------------------------------------------------------------------------
def _corp_facts(p: Profile) -> dict | None:
    """법인 등기 이력(corporate.py _facts: 본점 이전·상호 변경·공동대표). 가져올 수 없으면 None."""
    try:
        from .corporate import _facts
        return _facts(p)
    except Exception:  # noqa: BLE001 - 다른 그룹 모듈 변경에 영향받지 않게
        return None


@doc("business_registration_certificate_corp", "사업자등록증(법인사업자)", "business")
def business_registration_certificate_corp(p: Profile, rng: random.Random) -> dict:
    """세무서가 발급하는 법인사업자 사업자등록증.

    본점 이전·상호 변경·공동대표 취임은 법인등기부(corporate._facts)와 같은 날짜를 쓰고, 등기 뒤 1~4주 안에 정정 교부.
    """
    c = p.corporation
    cf = _corp_facts(p) or {}
    pad = lambda d: d + timedelta(days=rng.randint(7, 25)) if d else None  # noqa: E731
    events = []
    offices = cf.get("offices") or []
    if len(offices) > 1 and offices[-1][1]:
        events.append((pad(offices[-1][1]), "정정(본점 이전)"))
    names = cf.get("names") or []
    if len(names) > 1 and names[-1][1]:
        events.append((pad(names[-1][1]), "정정(상호 변경)"))
    co = cf.get("co_ceo")
    if co and co.get("start") and co["start"] > c.established:
        events.append((pad(co["start"]), "정정(대표자 변경)"))
    added = None
    ra = _prng(p, "corp-added")
    if special(ra, "corp_biz_added", 0.12):
        lo = c.established + timedelta(days=300)
        if lo < p.issue_date - timedelta(days=30):
            t, i, code = ra.choice([s for s in _SECONDARY if s[1] != c.biz_item])
            added = {"date": rand_date(ra, lo, p.issue_date - timedelta(days=30)), "biz_type": t, "biz_item": i}
            events.append((added["date"], "정정(업종 추가)"))
    reason, issued, _ = _reissue(rng, events, c.established, p.issue_date)
    fd = _cert_date(rng)
    out = {
        "biz_no": c.biz_no,
        "corp_name": c.name,
        "ceo": p.person.name,
        "opened": fd(c.established),
        "corp_reg_no": c.corp_no,
        "address": c.address.road_full,
        "head_office": c.address.road_full,
        "biz_type": c.biz_type,
        "biz_item": c.biz_item,
        "issue_reason": reason,
        "unit_taxation": "부",
        "issue_date": fd(issued),
        "issuer": _tax_office(c.address),
    }
    if co and co.get("person") is not None and (not co.get("start") or co["start"] <= issued):
        out["co_ceo"] = co["person"].name
    if added and added["date"] <= issued:
        out["sub_kinds"] = [{"biz_type": added["biz_type"], "biz_item": added["biz_item"]}]
    if rng.random() < 0.5:
        out["einvoice_email"] = c.email
    return out


# ---------------------------------------------------------------------------
# 사업자등록증명 (홈택스)
# ---------------------------------------------------------------------------
@doc("business_registration_proof", "사업자등록증명", "business")
def business_registration_proof(p: Profile, rng: random.Random) -> dict:
    """홈택스에서 발급한 개인사업자 사업자등록증명. 부업종·공동사업자는 _biz_facts() 를 따른다."""
    b, fx = p.business, _biz_facts(p)
    _, _, code, _ = _industry(b)
    kinds = [{"biz_type": b.biz_type, "biz_item": b.biz_item, "code": code, "main": "주업종"}]
    if fx["added"]:
        a = fx["added"]
        kinds.append({"biz_type": a["biz_type"], "biz_item": a["biz_item"], "code": a["code"], "main": "부업종"})
    purpose, submit_to = _purpose(rng, p)
    fmt = rng.choice(["kor", "dash"])
    registered = b.established + timedelta(days=rng.randint(-10, 15))
    out = {
        "issue_no": _hometax_no(rng),
        "trade_name": b.name,
        "biz_no": b.biz_no,
        "name": p.person.name,
        "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.8 else p.person.rrn,
        "address": b.address.road_full,
        "opened": D(b.established, fmt),
        "registered": D(registered, fmt),
        "kind": _biz_kind_label(p),
        "kinds": kinds,
        "joint": "해당" if fx["joint"] else "해당없음",
        "purpose": purpose,
        "submit_to": submit_to,
        "issue_date": D(p.issue_date, "kor"),
        "issuer": _tax_office(b.address),
    }
    if fx["joint"]:
        j = fx["joint"]
        out["co_owners"] = [
            {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn), "share": f"{j['own_share']}%", "role": "대표공동사업자"},
            {"name": j["name"], "rrn": K.mask_rrn(j["rrn"]), "share": f"{j['share']}%", "role": "공동사업자"},
        ]
    return out


# ---------------------------------------------------------------------------
# 표준재무제표증명 (개인)
# ---------------------------------------------------------------------------
def _split(r: random.Random, total: int, names: list[str], keep: float = 0.7, must: tuple = ()) -> list[dict]:
    """total 을 계정 여러 개로 나눈다 (일부 계정은 금액이 없어 빠진다). 나머지는 맨 앞 계정에."""
    chosen = [n for n in names if n in must or r.random() < keep] or names[:1]
    ws = [r.uniform(0.3, 3.0) for _ in chosen]
    s = sum(ws)
    amts = [int(total * w / s) // 10 * 10 for w in ws]
    amts[0] += total - sum(amts)
    return [{"account": n, "amount": a} for n, a in zip(chosen, amts) if a]


def _fs_detail(p: Profile, y: int, pl: dict, bs: dict) -> tuple[dict, dict]:
    """표준재무상태표·표준손익계산서 세부 계정 (heavy). 합계는 요약 계정과 같다.
    감가상각누계액은 자산 바로 아래에 음수로 둔다."""
    r = _prng(p, "fsdetail", y)
    sec = {}
    sec["quick"] = _split(r, bs["quick"], ["현금및현금성자산", "단기금융상품", "매출채권", "미수금", "선급금", "선급비용", "부가세대급금"],
                          must=("현금및현금성자산", "매출채권"))
    # 매출채권 아래 대손충당금
    for i, a in enumerate(sec["quick"]):
        if a["account"] == "매출채권" and a["amount"] > 1_000_000 and r.random() < 0.6:
            allow = int(a["amount"] * r.uniform(0.01, 0.03)) // 10 * 10
            a["amount"] += allow
            sec["quick"].insert(i + 1, {"account": "대손충당금", "amount": -allow})
            break
    item = p.business.biz_item
    inv_names = ["제품", "원재료", "재공품"] if item in ("제과",) else ["상품", "저장품"]
    sec["inventory"] = _split(r, bs["inventory"], inv_names, must=(inv_names[0],))
    sec["investment"] = _split(r, bs["investment"], ["장기금융상품", "장기대여금", "보험예치금"], must=("장기금융상품",))
    tang = []
    for a in _split(r, bs["tangible"], ["차량운반구", "비품", "시설장치", "기계장치", "건물"], keep=0.6, must=("비품", "시설장치")):
        acc = int(a["amount"] * r.uniform(0.25, 1.2)) // 10 * 10
        tang += [{"account": a["account"], "amount": a["amount"] + acc}, {"account": "감가상각누계액", "amount": -acc}]
    sec["tangible"] = tang
    sec["intangible"] = _split(r, bs["intangible"], ["영업권", "소프트웨어", "상표권"], keep=0.5)
    sec["other_noncurrent"] = _split(r, bs["other_noncurrent"], ["임차보증금", "기타보증금"], must=("임차보증금",))
    sec["current_liab"] = _split(r, bs["current_liab"], ["매입채무", "미지급금", "예수금", "부가세예수금", "미지급비용", "선수금", "단기차입금"],
                                 must=("매입채무", "미지급금", "예수금"))
    sec["noncurrent_liab"] = _split(r, bs["noncurrent_liab"], ["장기차입금", "퇴직급여충당부채", "장기미지급금"], keep=0.5, must=("장기차입금",))
    bs_acc = {k: v for k, v in sec.items() if v}

    pls = {}
    rev_names = {"한식": ["음식매출", "배달매출"], "커피전문점": ["음료매출", "상품매출"], "제과": ["제품매출", "상품매출"],
                 "미용": ["용역매출", "상품매출"], "학원": ["수강료수입", "교재매출"], "세무대리": ["용역매출", "기장수수료수입"],
                 "인테리어": ["공사수입", "상품매출"]}.get(item, ["상품매출", "기타매출"])
    pls["revenue"] = _split(r, pl["revenue"], rev_names, keep=0.6, must=(rev_names[0],))
    begin = _bs(p, y - 1)["inventory"] if y - 1 >= p.business.established.year else 0
    end = bs["inventory"]
    begin = min(begin, pl["cogs"] + end)
    pls["cogs"] = [{"account": "기초재고액", "amount": begin},
                   {"account": "당기매입액", "amount": pl["cogs"] - begin + end},
                   {"account": "기말재고액", "amount": end}]
    pls["sga"] = _split(r, pl["other_sga"], ["퇴직급여", "여비교통비", "기업업무추진비" if y >= 2024 else "접대비", "통신비", "수도광열비",
                                             "세금과공과", "수선비", "보험료", "차량유지비", "운반비", "교육훈련비", "도서인쇄비",
                                             "소모품비", "지급수수료", "광고선전비", "대손상각비", "잡비"],
                        keep=0.65, must=("통신비", "세금과공과", "지급수수료", "소모품비"))
    pls["non_op_income"] = _split(r, pl["non_op_income"], ["이자수익", "잡이익"], must=("이자수익",))
    pls["non_op_expense"] = _split(r, pl["non_op_expense"], ["이자비용", "잡손실"], must=("이자비용",))
    w = lambda n: _signed(n)  # noqa: E731
    fmt = lambda d: {k: [{"account": a["account"], "amount": w(a["amount"])} for a in v] for k, v in d.items() if v}  # noqa: E731
    return fmt(bs_acc), fmt(pls)


def _signed(n: int) -> str:
    return won(n, "") if n >= 0 else "-" + won(-n, "")


@doc("standard_financial_statement_proof", "표준재무제표증명", "business")
def standard_financial_statement_proof(p: Profile, rng: random.Random) -> dict:
    """홈택스 발급 표준재무제표증명(개인): 표준재무상태표 + 표준손익계산서.

    heavy: 세부 계정과목까지 표시 (재무상태표 30~40줄, 손익계산서 25~35줄, 2~3쪽).
    신고구분·신고일은 종합소득세 신고(_itr_filing)와 같다 (기한후신고·수정신고면 그 날짜).
    """
    b = p.business
    y = _filed_year(p)
    if y < b.established.year:
        y = b.established.year
    pl, bs = _pl(p, y), _bs(p, y)
    start = max(date(y, 1, 1), b.established)
    w = lambda n: won(n, "")  # noqa: E731
    fmt = rng.choice(["dash", "dot"])
    filing = _itr_filing(p, y)
    kind, filed = filing["kind"], filing["filed"]
    if kind == "경정청구":  # 경정청구는 재무제표를 다시 내지 않는다
        kind, filed = "정기신고", filing["original"]
    out = {
        "issue_no": _hometax_no(rng),
        "taxpayer_type": "개인",
        "taxpayer": {
            "trade_name": b.name,
            "biz_no": b.biz_no,
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn),
            "biz_type": b.biz_type,
            "biz_item": b.biz_item,
            "address": b.address.road_full,
        },
        "period": f"{D(start, fmt)} ~ {D(date(y, 12, 31), fmt)}",
        "attachments": "표준재무상태표, 표준손익계산서",
        "filing_kind": kind,
        "filed_date": D(filed, fmt),
        "balance_sheet": {k: w(v) for k, v in bs.items()},
        "income_statement": {k: w(v) for k, v in pl.items()},
        "issue_date": D(p.issue_date, "kor"),
        "issuer": _tax_office(b.address),
    }
    if heavy(rng, 0.3):
        out["bs_accounts"], out["pl_accounts"] = _fs_detail(p, y, pl, bs)
        del out["income_statement"]["other_sga"]  # 세부 계정으로 나눠 표시
    return out
