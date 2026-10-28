"""debt_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/finance.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.finance import _acct_no, _korean_amount  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


def _remaining(principal: int, annual_rate: float, n: int, k: int) -> int:
    """원리금균등분할상환 k회 납입 후 잔액."""
    r = annual_rate / 12
    if k >= n:
        return 0
    return int(principal * ((1 + r) ** n - (1 + r) ** k) / ((1 + r) ** n - 1))


@doc("debt_certificate", "부채증명서", "finance")
def debt_certificate(p: Profile, rng: random.Random) -> dict:
    """은행 발급 부채증명서 (대출 잔액)."""
    base = p.issue_date - timedelta(days=rng.choice([0, 0, 1]))
    if heavy(rng, 0.2):  # 대출이 여러 건인 차주 (같은 과목 추가 대출·사업자대출 포함)
        kinds = rng.sample(["주택담보대출", "신용대출", "마이너스통장대출", "가계일반자금대출"], rng.randint(2, 4))
        kinds += rng.choices(["신용대출", "가계일반자금대출", "중도금대출", "예적금담보대출", "개인사업자대출"],
                             weights=[3, 3, 1, 2, 2], k=rng.randint(3, 8))
    else:
        kinds = rng.sample(["주택담보대출", "신용대출", "마이너스통장대출", "전세자금대출", "가계일반자금대출"], rng.choice([1, 2, 2, 3]))
    if "주택담보대출" in kinds and "전세자금대출" in kinds:
        kinds.remove("전세자금대출")
    once = {"주택담보대출", "중도금대출", "마이너스통장대출", "전세자금대출"}  # 한 사람이 보통 한 건만 갖는 과목
    kinds = [k for i, k in enumerate(kinds) if k not in once or k not in kinds[:i]]
    show_type = special(rng, "rate_type", 0.3)  # 금리 옆에 (고정)/(변동) 표기
    loans, tot_amt, tot_bal = [], 0, 0
    for kind in kinds:
        if kind == "주택담보대출":
            amt = K.round_to(p.property.price * rng.uniform(0.35, 0.65), 1_000_000)
            years, rate = rng.choice([20, 30, 30, 35]), rng.uniform(3.3, 4.9)
            start = rand_date(rng, base - timedelta(days=365 * 8), base - timedelta(days=200))
            k = (base.year - start.year) * 12 + base.month - start.month
            bal = _remaining(amt, rate / 100, years * 12, k)
            mat = date(start.year + years, start.month, min(start.day, 28))
        elif kind == "전세자금대출":
            amt = K.round_to(p.property.lease_deposit * rng.uniform(0.5, 0.8), 1_000_000)
            rate, years = rng.uniform(3.0, 4.6), 2
            start = rand_date(rng, base - timedelta(days=700), base - timedelta(days=60))
            bal, mat = amt, date(start.year + 2, start.month, min(start.day, 28))
        elif kind == "마이너스통장대출":
            amt = rng.choice([10, 20, 30, 50, 70, 100]) * 1_000_000
            rate = rng.uniform(4.8, 7.9)
            start = rand_date(rng, base - timedelta(days=330), base - timedelta(days=10))
            bal, mat = K.round_to(amt * rng.uniform(0, 0.9), 1), date(start.year + 1, start.month, min(start.day, 28))
        elif kind == "신용대출":
            amt = K.round_to(p.employment.annual_salary * rng.uniform(0.3, 1.2), 1_000_000)
            rate = rng.uniform(4.3, 7.5)
            start = rand_date(rng, base - timedelta(days=330), base - timedelta(days=10))
            bal, mat = amt, date(start.year + 1, start.month, min(start.day, 28))
        elif kind == "중도금대출":
            amt = K.round_to(p.property.price * rng.uniform(0.2, 0.4), 1_000_000)
            rate = rng.uniform(3.8, 5.2)
            start = rand_date(rng, base - timedelta(days=700), base - timedelta(days=30))
            bal, mat = amt, date(start.year + 3, start.month, min(start.day, 28))
        elif kind == "예적금담보대출":
            amt = rng.choice([5, 10, 20, 30]) * 1_000_000
            rate = rng.uniform(3.5, 5.0)
            start = rand_date(rng, base - timedelta(days=330), base - timedelta(days=10))
            bal, mat = amt, date(start.year + 1, start.month, min(start.day, 28))
        else:
            amt = rng.choice([10, 20, 30, 50]) * 1_000_000 * (3 if kind == "개인사업자대출" else 1)
            rate, n = rng.uniform(4.5, 7.0), rng.choice([36, 60])
            start = rand_date(rng, base - timedelta(days=900), base - timedelta(days=60))
            k = (base.year - start.year) * 12 + base.month - start.month
            bal, mat = _remaining(amt, rate / 100, n, k), start + timedelta(days=round(n * 30.44))
        tot_amt += amt
        tot_bal += bal
        loans.append({"subject": kind, "account_no": _acct_no(rng, p.bank), "loan_date": D(start, "dot"),
                      "maturity": D(mat, "dot"), "amount": won(amt, ""), "balance": won(bal, ""),
                      "rate": f"{rate:.2f}%" + (f" ({'변동' if kind in ('신용대출', '마이너스통장대출') or rng.random() < 0.5 else '고정'})" if show_type else "")})
    guarantee = special(rng, "guarantee", 0.2)  # 다른 사람 대출의 연대보증
    d = {
        "cert_no": f"제 {base.year}-{rng.randint(10000, 99999)} 호",
        "borrower": {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn), "address": p.person.address.road_short},
        "base_date": D(base, "kor") + " 현재",
        "loans": loans,
        "total_amount": won(tot_amt, ""),
        "total_balance": won(tot_bal, ""),
        "total_korean": _korean_amount(tot_bal),
        "guarantee": "있음" if guarantee else "없음",
        "overdue": "없음",
        "purpose": rng.choice(["금융기관 제출용", "대출 신청용", "회사 제출용", "법원 제출용"]),
        "issue_date": D(p.issue_date, "kor_short"),
        "issuer": f"{p.bank} {p.bank_branch}장",
    }
    if guarantee:
        g_amt = rng.choice([10, 20, 30, 50]) * 1_000_000
        d["guarantee_detail"] = f"{K.make_name(rng, rng.choice('MF'))[0]} 차주 {rng.choice(['신용대출', '사업자대출', '전세자금대출'])} 연대보증 {won(g_amt)}"
    # 특수 상황: 연체 중인 대출 — 연체여부 '있음'과 연체 내역
    if special(rng, "overdue", 0.08):
        i = rng.randrange(len(loans))
        days = rng.choice([12, 35, 47, 62, 95, 128])
        bal_i = int(loans[i]["balance"].replace(",", "")) or int(loans[i]["amount"].replace(",", ""))
        amt_due = K.round_to(bal_i * rng.uniform(0.005, 0.03), 10) * (1 + days // 30)
        d["overdue"] = "있음"
        d["overdue_detail"] = (f"{loans[i]['subject']}({loans[i]['account_no']}) 연체 {days}일, 연체원리금 {won(amt_due)}"
                               + (" (기한이익상실)" if days >= 90 else ""))
    return d
