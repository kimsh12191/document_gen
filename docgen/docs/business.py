"""개인사업자·법인사업자 등록 및 재무 관련 서류 (국세청 발급).

이 파일에는 그룹 서식들이 같이 쓰는 도우미만 있다. 서식마다 값 만드는 함수(@doc)는 서식 폴더
docgen/forms/<ID>/generate.py 에 있고, 끝의 FORMS 차례로 등록한다.

개인사업체(p.business)의 연도별 매출·손익·재무상태는 _pl()/_bs() 로 계산한다.
이 값은 p.seed 에서 파생한 난수로 만들기 때문에 서류(표준재무제표증명, 부가가치세 과세표준증명,
종합소득세 신고서 등)가 달라도 같은 고객이면 같은 숫자가 나온다.
"""
import os

from ..entities import COMPANY_PREFIX, World
from ._common import *  # noqa: F401,F403
from ..registry import register_folder_forms

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


def _signed(n: int) -> str:
    return won(n, "") if n >= 0 else "-" + won(-n, "")


# 이 그룹의 코드 서식. 값 만드는 함수는 서식 폴더 docgen/forms/<ID>/generate.py 에 있다 (여기는 같이 쓰는 도우미).
FORMS = ('business_registration_certificate', 'business_registration_certificate_corp', 'business_registration_proof', 'standard_financial_statement_proof',)
register_folder_forms(__name__, FORMS)   # 예전 @doc 차례 그대로 등록 (서식 목록·데이터셋 순서)
