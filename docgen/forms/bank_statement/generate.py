"""bank_statement: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/finance.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.finance import _CARD_COS, _SHOPS  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.docs.income import _pay_cfg, _payroll  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


_INSURERS = ["삼성생명", "한화생명", "교보생명", "현대해상", "DB손해보험", "KB손해보험", "메리츠화재"]


_TELCO = ["SKT통신요금", "KT통신요금", "LGU+통신요금"]


def _short_company(name: str) -> str:
    return name.replace("주식회사 ", "").replace("(주)", "").strip()


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
    overdraft = special(rng, "overdraft", 0.08)  # 마이너스통장(한도대출 약정 입출금계좌): 잔액이 음수로 표시된다
    loan_int = special(rng, "loan_interest", 0.15)  # 대출이자 자동이체
    cancel = special(rng, "cancelled_tx", 0.1)  # 정정·취소 거래
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
            if overdraft:
                add(date(m.year, m.month, 21), "대출이자", out=rng.randint(30_000, 250_000), br="결산")
            else:
                add(date(m.year, m.month, 21), "예금결산이자", inn=rng.randint(30, 4000), br="결산")
        if loan_int:
            add(date(m.year, m.month, rng.choice([5, 10, 17, 27])), rng.choice(["대출이자", "주택담보대출이자", "신용대출이자"]),
                out=K.round_to(rng.uniform(150_000, 1_200_000), 10), br="자동이체")
        m = months_back(m, -1)
    fixed = len(ev)
    cap = rng.randint(30, 90) if heavy(rng) else 20  # 거래가 많은 통장은 여러 쪽
    target = rng.randint(max(12, fixed + 2), cap)
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
    ev = ev[:cap]
    if cancel:  # 잘못 보낸 이체를 취소(정정)한 거래: 같은 금액이 '취소'로 다시 들어온다
        outs = [e_ for e_ in ev if e_[2] and e_[4] in ("체크카드", "모바일", "인터넷")]
        if outs:
            o = rng.choice(outs)
            cd = min(end, o[0] + timedelta(days=rng.choice([1, 1, 2])))
            ev.append([cd, f"{o[1]} 취소" if o[4] == "체크카드" else "이체취소", 0, o[2], o[4]])
    for e_ in ev:
        if len(e_) == 5:
            e_.append(rng.randint(6 * 3600, 23 * 3600))
    ev.sort(key=lambda x: (x[0], x[5]))
    # 마지막 잔액 = 프로필 계좌 잔액. 역산하여 음수가 되면 마지막에 저축성 이체를 넣어 보정한다.
    final = a.balance
    limit = 0
    if overdraft:
        limit = rng.choice([10, 20, 30, 50, 70, 100]) * 1_000_000
        final = -K.round_to(limit * rng.uniform(0.1, 0.7), 1)

    def balances():
        bal, out = final, []
        for e_ in reversed(ev):
            out.append(bal)
            bal = bal - e_[3] + e_[2]
        return list(reversed(out)), bal

    bals, opening = balances()
    low = min([opening] + bals)
    floor = -limit + 10_000 if overdraft else 10_000  # 마이너스통장은 한도까지 음수 잔액 허용
    if low < floor:
        fix = K.round_to(floor - low + rng.uniform(50_000, 1_500_000), 10_000)
        ev.append([end, rng.choice(["정기예금", "적금이체", "증권이체"]), fix, 0, "모바일", 23 * 3600 + rng.randint(0, 3000)])
        ev.sort(key=lambda x: (x[0], x[5]))
        if len(ev) > cap:  # 가장 이른 거래 하나를 버리고 잔액을 다시 계산
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
    d = {
        "issue_no": f"{p.issue_date:%Y%m%d}-{rng.randint(100000, 999999)}",
        "holder": a.holder,
        "birth": D(p.person.birth, "dot"),
        "account_no": a.number,
        "product": rng.choice(["마이너스통장", "종합통장(한도대출)", "직장인 마이너스통장"]) if overdraft
        else rng.choice(["보통예금", "저축예금", "입출금이자유로운예금", "급여통장"]),
        "period": f"{D(start, 'dot')} ~ {D(end, 'dot')}",
        "opening_balance": won(opening, ""),
        "rows": rows,
        "summary": {"count": f"{len(rows)}건", "out": won(tot_out, ""), "in": won(tot_in, ""), "balance": won(final, "")},
        "issue_date": D(p.issue_date, rng.choice(["kor_short", "dot"])),
        "issuer": f"{p.bank} {p.bank_branch}",
    }
    if overdraft:
        d["overdraft_limit"] = won(limit, "")
    return d
