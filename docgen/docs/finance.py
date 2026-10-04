"""금융거래 관련 서류 (은행·카드사 발급)."""
from ..entities import BANK_ACCT_FMT
from ..registry import doc
from ._common import *  # noqa: F401,F403
from .income import _pay_cfg, _payroll

_CARD_COS = ["신한카드", "삼성카드", "KB국민카드", "현대카드", "롯데카드", "우리카드", "하나카드", "BC카드", "NH농협카드"]
_INSURERS = ["삼성생명", "한화생명", "교보생명", "현대해상", "DB손해보험", "KB손해보험", "메리츠화재"]
_TELCO = ["SKT통신요금", "KT통신요금", "LGU+통신요금"]
_SHOPS = ["GS25", "CU", "세븐일레븐", "스타벅스", "이마트", "홈플러스", "올리브영", "다이소", "쿠팡", "배달의민족",
          "카카오T", "CGV", "교보문고", "파리바게뜨", "롯데마트", "네이버페이", "11번가", "무신사", "SK에너지", "GS칼텍스"]
_BIG_SHOPS = ["삼성디지털프라자", "롯데하이마트", "LG전자베스트샵", "한샘", "이케아코리아", "대한항공", "아시아나항공",
              "서울밝은치과의원", "현대백화점", "신세계백화점", "애플코리아"]


def _acct_no(rng: random.Random, bank: str) -> str:
    fmt = BANK_ACCT_FMT.get(bank, "###-##-######")
    return "".join(str(rng.randint(0, 9)) if c == "#" else c for c in fmt)


def _mask_acct(no: str) -> str:
    """계좌번호 가운데 일부를 * 처리. 예) 123-456-789012 -> 123-456-**9012"""
    digits = [i for i, c in enumerate(no) if c.isdigit()]
    hide = set(digits[-6:-4] + digits[-8:-6]) if len(digits) > 8 else set(digits[-6:-4])
    return "".join("*" if i in hide else c for i, c in enumerate(no))


def _short_company(name: str) -> str:
    return name.replace("주식회사 ", "").replace("(주)", "").strip()


def _bank_phone(rng: random.Random, p: Profile) -> str:
    return K.landline(rng, p.person.address.sido)


def _korean_amount(n: int) -> str:
    return f"금 {K.won_korean(n)}원정"


@doc("bankbook_copy", "통장사본", "finance")
def bankbook_copy(p: Profile, rng: random.Random) -> dict:
    """예금통장 첫 면 사본 (스캔본 또는 인터넷 출력본)."""
    a = p.accounts[0]
    style = rng.choice(["passbook", "passbook", "print"])
    product = rng.choice(["보통예금", "저축예금", "입출금이자유로운예금", "직장인우대통장", "급여통장", "자유입출금통장"])
    d = {
        "bank": a.bank,
        "product": product,
        "account_no": a.number,
        "holder": a.holder,
        "opened": D(a.opened, rng.choice(["dot", "dash"])),
        "branch": a.branch,
        "branch_phone": _bank_phone(rng, p),
    }
    if style == "passbook":
        first = rng.choice([1_000, 10_000, 50_000, 100_000, 300_000])
        d["first_tx"] = {"date": D(a.opened, "dot"), "memo": "신규", "amount": won(first, ""), "balance": won(first, "")}
        d["passbook_no"] = f"{rng.randint(1, 4):02d}"
    else:
        d["issue_date"] = D(p.issue_date, "dot")
    return d


@doc("bank_statement", "거래내역확인서", "finance")
def bank_statement(p: Profile, rng: random.Random) -> dict:
    """은행 발급 예금 거래내역확인서 (조회기간 거래 목록, 잔액 일관).

    열 구성은 국내 은행 거래내역 통용 형식: 거래일시 / 적요(거래구분) / 기재내용(보낸분·받는분) /
    찾으신금액 / 맡기신금액 / 거래후잔액.
    """
    a = p.accounts[0]
    end = p.issue_date - timedelta(days=1)
    n_m = rng.choice([1, 2, 2, 3])
    sm = months_back(end, n_m)
    start = date(sm.year, sm.month, min(end.day, 28)) + timedelta(days=1)
    span = (end - start).days
    cfg = _pay_cfg(p)
    employer = _short_company(p.employment.company.name)
    card = rng.choice(_CARD_COS)
    card_day = rng.choice([12, 14, 15, 25])
    mgmt = rng.random() < 0.8
    ev = []  # (date, memo, out, in, branch)

    def add(d, memo, out=0, inn=0, br=None):
        if start <= d <= end:
            ev.append([d, memo, out, inn, br or rng.choice(["인터넷", "모바일", "모바일"])])

    m = date(start.year, start.month, 1)
    while m <= end:
        pr = _payroll(p, m.year, m.month)
        pd = date(m.year, m.month, min(cfg["pay_day"], 28))
        add(pd, rng.choice([employer, f"{employer[:6]}급여", "급여"]), inn=pr["net"], br=rng.choice(["펌뱅킹", "타행입금"]))
        add(date(m.year, m.month, card_day), card, out=K.round_to(rng.uniform(250_000, 2_200_000), 10), br="자동이체")
        if mgmt:
            add(date(m.year, m.month, rng.choice([25, 26, 27])), "아파트관리비", out=K.round_to(rng.uniform(150_000, 420_000), 10), br="자동이체")
        add(date(m.year, m.month, rng.choice([18, 20, 21])), rng.choice(_TELCO), out=K.round_to(rng.uniform(45_000, 130_000), 10), br="자동이체")
        if m.month in (3, 6, 9, 12):
            add(date(m.year, m.month, 21), "예금결산이자", inn=rng.randint(30, 4000), br="결산")
        m = months_back(m, -1)
    fixed = len(ev)
    target = rng.randint(max(12, fixed + 2), 20)
    while len(ev) < target:
        d = start + timedelta(days=rng.randint(0, span))
        k = rng.random()
        if k < 0.25:
            add(d, rng.choice(_SHOPS), out=K.round_to(rng.uniform(3_000, 120_000), 10), br="체크카드")
        elif k < 0.45:
            add(d, K.make_name(rng, rng.choice("MF"))[0], out=K.round_to(rng.uniform(20_000, 800_000), 1000))
        elif k < 0.55:
            add(d, rng.choice(["CD출금", "ATM출금"]), out=rng.choice([50_000, 100_000, 200_000, 300_000]), br="CD출금")
        elif k < 0.7:
            add(d, K.make_name(rng, rng.choice("MF"))[0], inn=K.round_to(rng.uniform(10_000, 600_000), 1000), br=rng.choice(["타행입금", "모바일"]))
        elif k < 0.82:
            add(d, rng.choice(_INSURERS), out=K.round_to(rng.uniform(40_000, 250_000), 10), br="자동이체")
        elif k < 0.9:
            add(d, rng.choice(["적금이체", "청약저축", "주택청약"]), out=rng.choice([100_000, 200_000, 300_000, 500_000]), br="자동이체")
        else:
            add(d, rng.choice(["네이버페이", "카카오페이", "토스"]), out=K.round_to(rng.uniform(5_000, 200_000), 10))
    ev = ev[:20]
    for e_ in ev:
        e_.append(rng.randint(6 * 3600, 23 * 3600))
    ev.sort(key=lambda x: (x[0], x[5]))
    # 마지막 잔액 = 프로필 계좌 잔액. 역산하여 음수가 되면 마지막에 저축성 이체를 넣어 보정한다.
    final = a.balance

    def balances():
        bal, out = final, []
        for e_ in reversed(ev):
            out.append(bal)
            bal = bal - e_[3] + e_[2]
        return list(reversed(out)), bal

    bals, opening = balances()
    low = min([opening] + bals)
    if low < 10_000:
        fix = K.round_to(10_000 - low + rng.uniform(50_000, 1_500_000), 10_000)
        ev.append([end, rng.choice(["정기예금", "적금이체", "증권이체"]), fix, 0, "모바일", 23 * 3600 + rng.randint(0, 3000)])
        ev.sort(key=lambda x: (x[0], x[5]))
        if len(ev) > 20:  # 가장 이른 거래 하나를 버리고 잔액을 다시 계산
            ev = ev[1:]
        bals, opening = balances()
    zero = rng.choice(["0", ""])
    rows = []
    for e_, b in zip(ev, bals):
        t = e_[5]
        r = {"datetime": f"{D(e_[0], 'dot')} {t // 3600:02d}:{t % 3600 // 60:02d}:{rng.randint(0, 59):02d}",
             "type": e_[4], "memo": e_[1], "balance": won(b, "")}
        if e_[2] or zero:
            r["out"] = won(e_[2], "")
        if e_[3] or zero:
            r["in"] = won(e_[3], "")
        rows.append(r)
    tot_out = sum(e_[2] for e_ in ev)
    tot_in = sum(e_[3] for e_ in ev)
    return {
        "issue_no": f"{p.issue_date:%Y%m%d}-{rng.randint(100000, 999999)}",
        "holder": a.holder,
        "birth": D(p.person.birth, "dot"),
        "account_no": a.number,
        "product": rng.choice(["보통예금", "저축예금", "입출금이자유로운예금", "급여통장"]),
        "period": f"{D(start, 'dot')} ~ {D(end, 'dot')}",
        "opening_balance": won(opening, ""),
        "rows": rows,
        "summary": {"count": f"{len(rows)}건", "out": won(tot_out, ""), "in": won(tot_in, ""), "balance": won(final, "")},
        "issue_date": D(p.issue_date, rng.choice(["kor_short", "dot"])),
        "issuer": f"{p.bank} {p.bank_branch}",
    }


@doc("balance_certificate", "잔액증명서", "finance")
def balance_certificate(p: Profile, rng: random.Random) -> dict:
    """은행 예금잔액증명서 (예금주·고객번호 / 과목·계좌번호·예금잔액·미결제타점권·질권·지급정지·압류 여부 / 합계)."""
    a = p.accounts[0]
    base = p.issue_date - timedelta(days=rng.choice([0, 0, 1]))
    accts = [(x.number, rng.choice(["보통예금", "저축예금"]), x.balance, x.opened, None) for x in p.accounts if x.bank == a.bank]
    for _ in range(rng.choice([0, 1, 1, 2, 3])):
        kind = rng.choice(["정기예금", "정기적금", "주택청약종합저축", "자유적립식예금"])
        opened = rand_date(rng, date(2018, 1, 1), base - timedelta(days=60))
        if kind == "주택청약종합저축":
            bal, mat = rng.randint(24, 150) * 100_000, None
        elif kind == "정기예금":
            bal = K.round_to(rng.uniform(5e6, 1e8), 1_000_000)
            mat = opened + timedelta(days=365 * rng.choice([1, 2, 3]))
        else:
            bal = rng.randint(6, 36) * rng.choice([100_000, 300_000, 500_000])
            mat = opened + timedelta(days=365 * rng.choice([1, 2, 3]))
        while mat and mat <= base:
            mat += timedelta(days=365)
        accts.append((_acct_no(rng, a.bank), kind, bal, opened, mat))
    rows = []
    for no, kind, bal, opened, mat in accts[:5]:  # 한 번에 최대 5계좌 표시
        pledged = mat is not None and rng.random() < 0.1
        rows.append({"kind": kind, "account_no": no, "balance": won(bal, ""), "uncleared": "0",
                     "pledge": "유" if pledged else "무", "restriction": "무"})
    accts = accts[:5]
    total = sum(x[2] for x in accts)
    return {
        "cert_no": f"제 {base.year}-{rng.randint(10000, 99999)} 호",
        "holder": {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn)},
        "base_date": D(base, "kor") + " 현재",
        "rows": rows,
        "total": won(total, ""),
        "total_korean": _korean_amount(total),
        "currency": "KRW",
        "purpose": rng.choice(["금융기관 제출용", "비자 발급용", "입찰 참가용", "대출 신청용", "유학 신청용"]),
        "issue_date": D(p.issue_date, "kor_short"),
        "issuer": f"{p.bank} {p.bank_branch}장",
    }


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
    kinds = rng.sample(["주택담보대출", "신용대출", "마이너스통장대출", "전세자금대출", "가계일반자금대출"], rng.choice([1, 2, 2, 3]))
    if "주택담보대출" in kinds and "전세자금대출" in kinds:
        kinds.remove("전세자금대출")
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
        else:
            amt = rng.choice([10, 20, 30, 50]) * 1_000_000
            rate, n = rng.uniform(4.5, 7.0), rng.choice([36, 60])
            start = rand_date(rng, base - timedelta(days=900), base - timedelta(days=60))
            k = (base.year - start.year) * 12 + base.month - start.month
            bal, mat = _remaining(amt, rate / 100, n, k), start + timedelta(days=round(n * 30.44))
        tot_amt += amt
        tot_bal += bal
        loans.append({"subject": kind, "account_no": _acct_no(rng, p.bank), "loan_date": D(start, "dot"),
                      "maturity": D(mat, "dot"), "amount": won(amt, ""), "balance": won(bal, ""), "rate": f"{rate:.2f}%"})
    guarantee = rng.random() < 0.2
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
        d["guarantee_detail"] = f"{K.make_name(rng, rng.choice('MF'))[0]} 차주 신용대출 연대보증 {won(g_amt)}"
    return d


@doc("card_statement", "신용카드 이용대금명세서", "finance")
def card_statement(p: Profile, rng: random.Random) -> dict:
    """카드사 신용카드 이용대금명세서 (일시불·할부·수수료 합계 일관).

    결제하실 금액·결제일·결제계좌·이용기간 요약 / 이용내역(이용일자·이용하신 가맹점·이용금액·할부·회차·
    원금·수수료(이자)·결제 후 잔액) / 연간 할부수수료율 및 100원당 할부개월별 수수료 안내(표준약관상 통지사항).
    """
    company = rng.choice(_CARD_COS)
    pay_day = rng.choice([12, 14, 15])
    pm = months_back(p.issue_date, 0 if p.issue_date.day >= 5 else 1)
    pay_date = date(pm.year, pm.month, pay_day)
    us_start = months_back(pm, 1)
    us_end = pm - timedelta(days=1)
    fee_rate = rng.choice([0.115, 0.135, 0.149, 0.165, 0.18])
    rows, lump, inst, fees, next_month = [], 0, 0, 0, 0
    n = rng.randint(10, 16)
    items = []
    for _ in range(n):
        if rng.random() < 0.18:
            months = rng.choice([2, 3, 3, 5, 6, 10, 12])
            seq = rng.randint(1, months)
            amt = K.round_to(rng.uniform(200_000, 2_500_000), 100)
            used = months_back(us_start, seq - 1) + timedelta(days=rng.randint(0, 27))
            items.append((used, rng.choice(_BIG_SHOPS), amt, months, seq, rng.random() < 0.5))
        else:
            used = us_start + timedelta(days=rng.randint(0, (us_end - us_start).days))
            hi = rng.choice([25_000, 60_000, 60_000, 150_000])
            items.append((used, rng.choice(_SHOPS), K.round_to(rng.uniform(2_500, hi), 10), 1, 1, True))
    items.sort(key=lambda x: x[0])
    for used, shop, amt, months, seq, free in items:
        if months == 1:
            prin, fee, after = amt, 0, 0
            lump += prin
        else:
            per = amt // months
            paid_before = per * (seq - 1)
            prin = amt - paid_before if seq == months else per
            remain = amt - paid_before
            fee = 0 if free else _t10_c(remain * fee_rate / 12)
            after = remain - prin
            inst += prin
            if after:
                next_month += per if seq + 1 < months else after
        fees += fee
        rows.append({"date": D(used, "dot"), "merchant": shop, "amount": won(amt, ""),
                     "months": "일시불" if months == 1 else f"{months}개월", "seq": "-" if months == 1 else f"{seq}/{months}",
                     "principal": won(prin, ""), "fee": won(fee, ""), "after": won(after, "")})
    total = lump + inst + fees
    a = p.accounts[0]
    limit = rng.choice([500, 800, 1000, 1500, 2000, 3000]) * 10_000
    return {
        "company": company,
        "statement_month": f"{pm.year}년 {pm.month}월",
        "member": p.person.name,
        "card_no": f"{rng.randint(4000, 5599)}-{rng.randint(10, 99)}**-****-{rng.randint(1000, 9999)}",
        "pay_date": D(pay_date, "dot"),
        "pay_account": f"{a.bank} {_mask_acct(a.number)}",
        "usage_period": f"{D(us_start, 'dot')} ~ {D(us_end, 'dot')}",
        "summary": {"lump": won(lump, ""), "installment": won(inst, ""), "cash": "0", "fee": won(fees, ""),
                    "total": won(total, ""), "next_month": won(next_month, ""), "limit": won(limit, "")},
        "fee_rate": f"연 {fee_rate * 100:.1f}%",
        # 100원당 할부개월별 수수료 (원금균등 상환 가정: 100 × 연율/12 × (n+1)/2)
        "fee_per_100": [{"months": f"{n}개월", "fee": f"{100 * fee_rate / 12 * (n + 1) / 2:.2f}원"} for n in (2, 3, 6, 10, 12)],
        "rows": rows,
        "sum": {"amount": won(sum(x[2] for x in items), ""), "principal": won(lump + inst, ""), "fee": won(fees, "")},
    }


def _t10_c(x: float) -> int:
    return int(x) // 10 * 10
