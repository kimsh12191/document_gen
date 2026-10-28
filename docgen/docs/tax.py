"""세금 관련 증명서 (국세청·지방자치단체 발급) 및 종합소득세 신고서.

이 파일에는 그룹 서식들이 같이 쓰는 도우미만 있다. 서식마다 값 만드는 함수(@doc)는 서식 폴더
docgen/forms/<ID>/generate.py 에 있고, 끝의 FORMS 차례로 등록한다.

개인사업체 매출·손익은 business.py 의 프로필 고정 모델(_revenue, _pl)을 공유하므로
부가가치세 과세표준증명·종합소득세 신고서·표준재무제표증명의 숫자가 서로 맞는다.
사업장 이전·간이→일반 전환·휴업·공동사업자 같은 사실은 business._biz_facts(), 종합소득세 신고 구분은
business._itr_filing() 이 프로필 단위로 정한다.
"""
import os

from ._common import *  # noqa: F401,F403
from . import business  # noqa: F401  (이 그룹 서식들이 쓰는 business 를 먼저 읽는다 — 서식 등록 차례가 예전과 같게)
from ..registry import register_folder_forms
from .business import (_biz_facts, _bookkeeping_double, _hometax_no, _industry, _itr_filing,
                       _pl, _prng, _sincere_filer)

# 종합소득세 기본세율 (2023년 귀속 이후): (과세표준 상한, 세율 %, 누진공제)
_BRACKETS = [
    (14_000_000, 6, 0), (50_000_000, 15, 1_260_000), (88_000_000, 24, 5_760_000),
    (150_000_000, 35, 15_440_000), (300_000_000, 38, 19_940_000), (500_000_000, 40, 25_940_000),
    (1_000_000_000, 42, 35_940_000), (float("inf"), 45, 65_940_000),
]


def _income_tax(base: int) -> tuple[int, int, int]:
    """(산출세액, 세율%, 누진공제)."""
    for cap, rate, prog in _BRACKETS:
        if base <= cap:
            return max(0, base * rate // 100 - prog), rate, prog
    raise AssertionError


def _floor10(n: int) -> int:
    return n // 10 * 10


def _signed(n: int) -> str:
    return won(n, "") if n >= 0 else "-" + won(-n, "")


def _cert_purpose(rng: random.Random, p: Profile) -> str:
    return rng.choice(["금융기관 제출", "금융기관 제출용", "대출 신청", "은행 제출", f"{p.bank} 제출"])


_PAYERS = ["조달청", "한국토지주택공사", "서울특별시", "한국도로공사", "한국전력공사"]


def _purpose_pair(rng: random.Random, p: Profile, corp: bool) -> dict:
    """사용목적 체크항목(대금 수령 / 해외이주 / 기타) + 괄호 안 구체적 목적 + 대금 지급자.
    special emigration: 개인의 해외이주용 발급."""
    kind = rng.choices(["기타", "대금 수령"], [9, 1])[0]
    if not corp and special(rng, "emigration", 0.03):
        return {"purpose_type": "해외이주", "purpose": "해외이주 신고", "payer": None}
    if kind == "대금 수령":
        payer = rng.choice(_PAYERS + [district_office(p.person.address).replace("청장", "청").replace("장", "")])
        return {"purpose_type": kind, "purpose": rng.choice(["공사대금 수령", "용역대금 수령", "물품대금 수령"]), "payer": payer}
    return {"purpose_type": kind, "purpose": _cert_purpose(rng, p), "payer": None}


def _due_dates(issue: date, corp: bool) -> list[tuple[date, str]]:
    """발급일 전후의 지정납부기한 후보 (기한, 세목 설명)."""
    out = []
    for y in (issue.year - 1, issue.year, issue.year + 1):
        out += [(date(y, 1, 25), f"{y - 1}년 2기 부가가치세"), (date(y, 7, 25), f"{y}년 1기 부가가치세")]
        if corp:
            out += [(date(y, 3, 31), f"{y - 1}사업연도 법인세"), (date(y, 8, 31), f"{y}사업연도 법인세 중간예납"),
                    (date(y, 4, 25), f"{y}년 1기 부가가치세 예정"), (date(y, 10, 25), f"{y}년 2기 부가가치세 예정")]
        else:
            out += [(date(y, 5, 31), f"{y - 1}년 귀속 종합소득세"), (date(y, 11, 30), f"{y}년 귀속 종합소득세 중간예납")]
    return sorted(out)


def _validity(rng: random.Random, p: Profile, corp: bool, name: str) -> tuple[str, str | None]:
    """납세증명서 유효기간: 발급일부터 30일. special(name): 신고·고지 후 납부기한이 30일 안에 오는 국세가 있으면
    그 지정납부기한까지로 줄이고 사유를 적는다 (국세징수법 시행령 제98조)."""
    issue = p.issue_date
    end, reason = issue + timedelta(days=29), None
    if special(rng, name, 0.12):
        due = next(((d, t) for d, t in _due_dates(issue, corp) if issue < d <= issue + timedelta(days=29)), None)
        if due:
            end, reason = due[0], f"{due[1]} 납부기한({D(due[0], 'kor_short')}) 도래"
    return f"{D(issue, 'kor')} ~ {D(end, 'kor')}", reason


def _deferrals(rng: random.Random, p: Profile, corp: bool) -> list[dict]:
    """연장ㆍ유예 명세 1~2건 (납부기한 연장 / 납부고지 유예 / 압류ㆍ매각의 유예)."""
    issue = p.issue_date
    rows = []
    for _ in range(rng.choice([1, 1, 2])):
        kind = rng.choice(["납부기한등 연장", "납부고지의 유예", "압류ㆍ매각의 유예"])
        item = rng.choice(["법인세", "부가가치세", "원천세"] if corp else ["종합소득세", "부가가치세", "부가가치세"])
        md = {"법인세": [(3, 31)], "종합소득세": [(5, 31)], "부가가치세": [(1, 25), (7, 25)],
              "원천세": [(m, 10) for m in range(1, 13)]}[item]
        lo = issue - timedelta(days=150 if kind != "압류ㆍ매각의 유예" else 420)
        hi = issue - timedelta(days=20 if kind != "압류ㆍ매각의 유예" else 80)
        cands = [date(y, m, d) for y in (issue.year - 2, issue.year - 1, issue.year) for m, d in md if lo <= date(y, m, d) <= hi]
        if not cands:
            continue
        due = rng.choice(cands)
        start = due + timedelta(days=1) if kind != "압류ㆍ매각의 유예" else due + timedelta(days=rng.randint(40, 70))
        end = start + timedelta(days=rng.choice([182, 273, 364]))
        if end <= issue:
            end = issue + timedelta(days=rng.randint(60, 200))
        if item == "법인세":
            tp = f"{due.year - 1}.01.01 ~ {due.year - 1}.12.31"
        elif item == "종합소득세":
            tp = f"{due.year - 1}년 귀속"
        elif item == "원천세":
            pm = due.month - 1 or 12
            tp = f"{due.year if due.month > 1 else due.year - 1}년 {pm}월"
        else:
            tp = f"{due.year}년 1기" if due.month == 7 else f"{due.year - 1}년 2기"
        amt = K.round_to(rng.uniform(0.6e6, 9e6) * (3 if corp else 1), 10)
        rows.append({"kind": kind, "period": f"{D(start, 'dot')} ~ {D(end, 'dot')}", "tax_period": tp, "tax_item": item,
                     "due": D(due, "dot"), "amount": won(amt, "")})
    return rows


def _national_cert(p: Profile, rng: random.Random, corp: bool) -> dict:
    valid, reason = _validity(rng, p, corp, "short_validity")
    out = {
        "issue_no": _hometax_no(rng),
        "valid_period": valid,
        "valid_reason": reason,
        **_purpose_pair(rng, p, corp),
        "arrears": "없음",
        "issue_date": D(p.issue_date, "kor"),
    }
    rows = _deferrals(rng, p, corp) if special(rng, "tax_deferral", 0.08) else []
    if rows:
        out["deferrals"] = rows
    else:
        out["deferral"] = "해당없음"
    return out


# ---------------------------------------------------------------------------
# 종합소득세 과세표준확정신고 및 납부계산서
# ---------------------------------------------------------------------------
def _wage_deduction(g: int) -> int:
    """근로소득공제."""
    if g <= 5_000_000:
        return g * 70 // 100
    if g <= 15_000_000:
        return 3_500_000 + (g - 5_000_000) * 40 // 100
    if g <= 45_000_000:
        return 7_500_000 + (g - 15_000_000) * 15 // 100
    if g <= 100_000_000:
        return 12_000_000 + (g - 45_000_000) * 5 // 100
    return min(14_750_000 + (g - 100_000_000) * 2 // 100, 20_000_000)


def _reduce_rate(months: int) -> float:
    """수정신고 과소신고가산세 감면율 (법정신고기한 경과 개월 수)."""
    for m, r in ((1, 0.9), (3, 0.75), (6, 0.5), (12, 0.3), (18, 0.2), (24, 0.1)):
        if months <= m:
            return r
    return 0.0


_ITR_CACHE: dict = {}


def _itr_calc(p: Profile, y: int) -> dict:
    """y년 귀속 종합소득세 계산 (프로필 고정). 지방세 과세증명의 지방소득세(종합소득분)도 이 값을 쓴다.

    heavy itr_many: 소득 종류 다수(근로·부동산임대·이자배당·기타). special itr_wage / itr_rental / itr_other: 한 가지 추가.
    """
    key = (p.seed, y, p.issue_date, os.environ.get("DOCGEN_SPECIAL", ""), os.environ.get("DOCGEN_HEAVY", ""))
    if key in _ITR_CACHE:
        return _ITR_CACHE[key]
    r = _prng(p, "itr", y)
    b, fx = p.business, _biz_facts(p)
    filing = _itr_filing(p, y)
    many = heavy(r, 0.25)
    pl = _pl(p, y)
    share = fx["joint"]["own_share"] if fx["joint"] else 100
    rev = pl["revenue"] * share // 100
    biz_income = pl["net"] * share // 100
    code = _industry(b)[2]
    incomes = [{"type": "사업소득", "payer": b.name, "revenue": rev, "expense": rev - biz_income, "amount": biz_income,
                "withheld": 0}]
    wage = special(r, "itr_wage", 0.1) or (many and r.random() < 0.5)
    rental = special(r, "itr_rental", 0.08) or (many and r.random() < 0.5)
    fin = many and r.random() < 0.4
    other = special(r, "itr_other", 0.08) or (many and r.random() < 0.5)
    wage_gross = 0
    if wage:
        g = K.round_to(r.uniform(1.8e7, 4.8e7), 10_000)
        wage_gross = g
        ded = _wage_deduction(g)
        emp = f"(주){r.choice(['한빛', '대성', '미래', '세진', '우진', '다온'])}{r.choice(['산업', '테크', '물산', '푸드'])}"
        incomes.append({"type": "근로소득", "payer": emp, "revenue": g, "expense": ded, "amount": g - ded,
                        "withheld": _floor10(int(g * r.uniform(0.012, 0.04)))})
    if rental:
        rv = r.choice([60, 80, 100, 120, 150, 200, 250]) * 10_000 * 12
        ex = _floor10(int(rv * r.uniform(0.25, 0.45)))
        incomes.append({"type": "부동산임대업소득", "payer": f"{p.property.address.sigungu or p.property.address.sido} 주택임대",
                        "revenue": rv, "expense": ex, "amount": rv - ex, "withheld": 0})
    if fin:
        it = K.round_to(r.uniform(1.3e7, 2.4e7), 10)
        dv = K.round_to(r.uniform(5e6, 1.5e7), 10)
        incomes.append({"type": "이자소득", "payer": p.accounts[0].bank, "revenue": it, "expense": 0, "amount": it,
                        "withheld": _floor10(it * 14 // 100)})
        incomes.append({"type": "배당소득", "payer": r.choice(["삼성전자(주)", "(주)케이티앤지", "현대자동차(주)", "에스케이텔레콤(주)"]),
                        "revenue": dv, "expense": 0, "amount": dv, "withheld": _floor10(dv * 14 // 100)})
    if other:
        orv = K.round_to(r.uniform(3e6, 9e6), 1000)
        oex = orv * 60 // 100
        incomes.append({"type": "기타소득", "payer": r.choice(["한국생산성본부", "(사)한국외식업중앙회", "○○대학교 산학협력단", "한국방송공사"]),
                        "revenue": orv, "expense": oex, "amount": orv - oex, "withheld": _floor10((orv - oex) * 20 // 100)})
    total_income = sum(i["amount"] for i in incomes)

    # 인적공제 대상자
    deps = [{"relation": "본인", "person": p.person, "extra": None}]
    if p.spouse and r.random() < 0.5:
        deps.append({"relation": "배우자", "person": p.spouse, "extra": None})
    for c in p.children:
        if c.birth.year <= y and y - c.birth.year < 20:
            deps.append({"relation": "자녀", "person": c, "extra": None})
    for rel, par in (("부", p.father), ("모", p.mother)):
        if y - par.birth.year >= 60 and r.random() < (0.5 if many else 0.25):
            deps.append({"relation": rel, "person": par, "extra": "경로우대" if y - par.birth.year >= 70 else None})
    personal = 1_500_000 * len(deps)
    extra = 1_000_000 * sum(1 for d in deps if d["extra"])
    pension = _floor10(min(total_income // 12, 6_170_000) * 9 // 100 * 12)
    yellow = 0
    if r.random() < 0.55:
        limits = (6_000_000, 4_000_000) if y >= 2025 else (5_000_000, 3_000_000)
        lim = limits[0] if biz_income <= 40_000_000 else limits[1] if biz_income <= 100_000_000 else 2_000_000
        yellow = min(r.choice([1_200_000, 2_400_000, 3_000_000, 3_600_000, 6_000_000]), lim)
    ded_items = [("기본공제", personal)]
    if extra:
        ded_items.append(("추가공제", extra))
    ded_items.append(("연금보험료공제", pension))
    if wage_gross:
        ded_items.append(("특별소득공제(보험료)", _floor10(wage_gross * 45 // 1000)))
    if yellow:
        ded_items.append(("소기업ㆍ소상공인 공제부금 소득공제", yellow))
    claim = filing["kind"] == "경정청구"
    missed = None
    if claim:  # 경정청구: 당초 신고에서 빠뜨린 공제를 추가
        missed = ("소기업ㆍ소상공인 공제부금 소득공제", 3_000_000) if not yellow else ("추가공제", 1_000_000)
        ded_items.append(missed)
    deduction = sum(a for _, a in ded_items)
    base = max(0, total_income - deduction)
    computed, rate, _ = _income_tax(base)
    paper = filing["kind"] == "정기신고" and r.random() < 0.2
    kids = sum(1 for c in p.children if c.birth.year <= y and 8 <= y - c.birth.year < 20)
    credits = []
    if kids:
        one, two, more = (250_000, 550_000, 400_000) if y >= 2025 else (150_000, 350_000, 300_000)
        credits.append(("자녀세액공제", one if kids == 1 else two + more * (kids - 2)))
    if wage_gross:
        wt = computed * incomes[1]["amount"] // max(total_income, 1)
        credits.append(("근로소득세액공제", min(_floor10(wt * 55 // 100), 660_000)))
    credits.append(("표준세액공제", 70_000))
    if not paper:
        credits.append(("전자신고세액공제", 20_000))
    credit = min(computed, sum(a for _, a in credits))
    determined = computed - credit
    withheld = sum(i["withheld"] for i in incomes)
    mid = _floor10(int(determined * r.uniform(0.25, 0.45))) if y > b.established.year else 0
    prepaid_items = []
    if mid:
        prepaid_items.append(("중간예납세액", mid))
    if withheld:
        prepaid_items.append(("원천징수세액", withheld))
    penalties = []
    deadline = date(y + 1, 6, 30) if _bookkeeping_double(p) and _sincere_filer(p) else date(y + 1, 5, 31)
    if filing["kind"] == "기한후신고":
        days = filing["late_days"]
        unpaid = max(0, determined - mid - withheld)
        penalties.append(("무신고가산세", _floor10(int(unpaid * 0.2 * (0.5 if days <= 30 else 0.7 if days <= 90 else 0.8)))))
        penalties.append(("납부지연가산세", _floor10(unpaid * 22 * days // 100_000)))
    elif filing["kind"] == "수정신고":
        added = _floor10(int(determined * r.uniform(0.08, 0.25)))
        days = (filing["filed"] - deadline).days
        penalties.append(("과소신고가산세", _floor10(int(added * 0.1 * (1 - _reduce_rate(max(1, days // 30)))))))
        penalties.append(("납부지연가산세", _floor10(added * 22 * max(days, 0) // 100_000)))
        prepaid_items.append(("당초 신고 납부세액", max(0, determined - added - mid - withheld)))
    elif claim:
        old_det = computed - credit + _income_tax(base + missed[1])[0] - computed
        prepaid_items.append(("당초 신고 납부세액", max(0, old_det - mid - withheld)))
    penalty = sum(a for _, a in penalties)
    total = determined + penalty
    prepaid = sum(a for _, a in prepaid_items)
    payable = total - prepaid
    if payable > 0:
        payable = _floor10(payable)
    installment = 0
    if payable > 10_000_000 and filing["kind"] == "정기신고" and r.random() < 0.6:
        installment = payable - 10_000_000 if payable <= 20_000_000 else _floor10(payable // 2)
    double = _bookkeeping_double(p)
    if double:
        filing_type = "성실신고확인" if _sincere_filer(p) else r.choice(["자기조정", "외부조정"])
    else:
        filing_type = r.choices(["간편장부", "추계-기준율", "추계-단순율"], [8, 1, 1])[0]
    agent = filing_type in ("외부조정", "성실신고확인") or special(r, "itr_tax_agent", 0.3)
    paper = paper and not agent
    out = {
        "filing": filing, "many": many, "incomes": incomes, "deps": deps, "ded_items": ded_items, "credits": credits,
        "penalties": penalties, "prepaid_items": prepaid_items, "total_income": total_income, "deduction": deduction,
        "base": base, "rate": rate, "computed": computed, "credit": credit, "determined": determined, "penalty": penalty,
        "total": total, "prepaid": prepaid, "payable": payable, "installment": installment, "filing_type": filing_type,
        "bookkeeping": "복식부기의무자" if double else "간편장부대상자", "agent": agent, "paper": paper, "share": share,
        "code": code, "detail": many or len(incomes) > 1 or filing["kind"] != "정기신고" or bool(fx["joint"]) or r.random() < 0.3,
    }
    _ITR_CACHE[key] = out
    return out


class _Doc(dict):
    """서류 데이터. 화면 구성 선택(손글씨 서면 신고 등)은 값이 아니라 속성으로 둔다 (정답에 들어가지 않음)."""
    paper = False


# 이 그룹의 코드 서식. 값 만드는 함수는 서식 폴더 docgen/forms/<ID>/generate.py 에 있다 (여기는 같이 쓰는 도우미).
FORMS = ('tax_payment_certificate', 'tax_payment_certificate_corp', 'local_tax_payment_certificate', 'local_tax_assessment', 'vat_tax_base_certificate', 'income_tax_return',)
register_folder_forms(__name__, FORMS)   # 예전 @doc 차례 그대로 등록 (서식 목록·데이터셋 순서)
