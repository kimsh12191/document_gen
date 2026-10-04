"""개인사업자·법인사업자 등록 및 재무 관련 서류 (국세청 발급).

개인사업체(p.business)의 연도별 매출·손익·재무상태는 _pl()/_bs() 로 계산한다.
이 값은 p.seed 에서 파생한 난수로 만들기 때문에 서류(표준재무제표증명, 부가가치세 과세표준증명,
종합소득세 신고서 등)가 달라도 같은 고객이면 같은 숫자가 나온다.
"""
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
    return rand_date(_prng(p, "itr_filed", y), date(y + 1, 5, 2), deadline)


def _revenue(p: Profile, y: int) -> int:
    """y년 매출액(공급가액). 기준연도(발급연도-1)는 p.business.revenue 에 맞춘다."""
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


# ---------------------------------------------------------------------------
# 사업자등록증 (개인)
# ---------------------------------------------------------------------------
@doc("business_registration_certificate", "사업자등록증", "business")
def business_registration_certificate(p: Profile, rng: random.Random) -> dict:
    """세무서가 발급하는 개인사업자 사업자등록증."""
    b = p.business
    reason = rng.choices(["신규", "재발급", "정정(사업장 소재지 변경)", "정정(상호 변경)"], [5, 3, 1, 1])[0]
    if reason == "신규":
        issued = b.established + timedelta(days=rng.randint(0, 12))
    else:
        issued = rand_date(rng, b.established + timedelta(days=200), p.issue_date - timedelta(days=3))
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
        "unit_taxation": "부",
        "issue_date": fd(issued),
        "issuer": _tax_office(b.address),
    }
    if rng.random() < 0.4:
        out["einvoice_email"] = rng.choice([p.person.email, b.email])
    return out


# ---------------------------------------------------------------------------
# 사업자등록증 (법인)
# ---------------------------------------------------------------------------
@doc("business_registration_certificate_corp", "사업자등록증(법인사업자)", "business")
def business_registration_certificate_corp(p: Profile, rng: random.Random) -> dict:
    """세무서가 발급하는 법인사업자 사업자등록증."""
    c = p.corporation
    reason = rng.choices(["신규", "재발급", "정정(대표자 변경)", "정정(본점 이전)"], [5, 3, 1, 1])[0]
    if reason == "신규":
        issued = c.established + timedelta(days=rng.randint(0, 12))
    else:
        issued = rand_date(rng, c.established + timedelta(days=200), p.issue_date - timedelta(days=3))
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
    if rng.random() < 0.5:
        out["einvoice_email"] = c.email
    return out


# ---------------------------------------------------------------------------
# 사업자등록증명 (홈택스)
# ---------------------------------------------------------------------------
@doc("business_registration_proof", "사업자등록증명", "business")
def business_registration_proof(p: Profile, rng: random.Random) -> dict:
    """홈택스에서 발급한 개인사업자 사업자등록증명."""
    b = p.business
    _, _, code, _ = _industry(b)
    kinds = [{"biz_type": b.biz_type, "biz_item": b.biz_item, "code": code, "main": "주업종"}]
    if rng.random() < 0.3:
        sec = rng.choice([s for s in _SECONDARY if s[1] != b.biz_item])
        kinds.append({"biz_type": sec[0], "biz_item": sec[1], "code": sec[2], "main": "부업종"})
    purpose, submit_to = _purpose(rng, p)
    fmt = rng.choice(["kor", "dash"])
    registered = b.established + timedelta(days=rng.randint(-10, 15))
    return {
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
        "joint": "해당없음",
        "purpose": purpose,
        "submit_to": submit_to,
        "issue_date": D(p.issue_date, "kor"),
        "issuer": _tax_office(b.address),
    }


# ---------------------------------------------------------------------------
# 표준재무제표증명 (개인)
# ---------------------------------------------------------------------------
@doc("standard_financial_statement_proof", "표준재무제표증명", "business")
def standard_financial_statement_proof(p: Profile, rng: random.Random) -> dict:
    """홈택스 발급 표준재무제표증명(개인): 표준재무상태표 + 표준손익계산서 요약."""
    b = p.business
    y = _filed_year(p)
    if y < b.established.year:
        y = b.established.year
    pl, bs = _pl(p, y), _bs(p, y)
    start = max(date(y, 1, 1), b.established)
    w = lambda n: won(n, "")  # noqa: E731
    fmt = rng.choice(["dash", "dot"])
    return {
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
        "filing_kind": "정기신고",
        "filed_date": D(_itr_filed_date(p, y), fmt),
        "balance_sheet": {k: w(v) for k, v in bs.items()},
        "income_statement": {k: w(v) for k, v in pl.items()},
        "issue_date": D(p.issue_date, "kor"),
        "issuer": _tax_office(b.address),
    }
