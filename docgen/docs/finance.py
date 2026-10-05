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
        closed = special(rng, "closed", 0.06)  # 해지된 계좌의 통장 (해지 거래 후 잔액 0, '해지' 도장)
        zero = not closed and special(rng, "zero_balance", 0.05)  # 전액 출금해 잔액 0
        # 첫 장에 거래가 몇 줄 더 찍힌 통장
        n_more = rng.randint(2, 5) if (special(rng, "more_tx", 0.3) or closed or zero) else 0
        bal, day, txs = first, a.opened, []
        for k in range(n_more):
            day = min(p.issue_date, day + timedelta(days=rng.randint(1, 40)))
            last = k == n_more - 1
            if last and (closed or zero):
                memo = "해지" if closed else rng.choice(["타행이체", "모바일출금", "CD출금"])
                out, inn = bal, 0
            elif rng.random() < 0.12:
                memo, out, inn = "이자", 0, rng.randint(1, 3_000)
            elif rng.random() < 0.55 or bal < 20_000:
                memo, out, inn = rng.choice(["급여", "타행입금", "모바일입금"]), 0, K.round_to(rng.uniform(10_000, 3_500_000), 10)
            else:  # 마지막 줄(해지·전액출금) 전에는 잔액을 남긴다
                memo, inn = rng.choice(["체크카드", "CD출금", "자동이체", "모바일출금"]), 0
                out = min(bal - 10_000, K.round_to(rng.uniform(5_000, 800_000), 10))
            bal = bal - out + inn
            txs.append({"date": D(day, "dot"), "memo": memo, **({"out": won(out, "")} if out else {}),
                        **({"in": won(inn, "")} if inn else {}), "balance": won(bal, "")})
        if txs:
            d["txs"] = txs
        if closed:
            d["status"] = "해지"
            d["closed_date"] = D(day, "dot")
    else:
        d["issue_date"] = D(p.issue_date, "dot")
        # 금융거래한도계좌 (대포통장 방지용 이체·출금 한도 제한) — 개설한 지 얼마 안 된 계좌
        if special(rng, "limit_account", 0.3) and (p.issue_date - a.opened).days < 1100:
            d["limit_note"] = rng.choice(["금융거래한도계좌", "금융거래한도계좌 (1일 이체·출금 한도 100만원)",
                                          "한도제한계좌 (1일 한도 30만원)"])
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


@doc("balance_certificate", "잔액증명서", "finance")
def balance_certificate(p: Profile, rng: random.Random) -> dict:
    """은행 예금잔액증명서 (예금주·고객번호 / 과목·계좌번호·예금잔액·미결제타점권·질권·지급정지·압류 여부 / 합계)."""
    a = p.accounts[0]
    base = p.issue_date - timedelta(days=rng.choice([0, 0, 1]))
    accts = [(x.number, rng.choice(["보통예금", "저축예금"]), x.balance, x.opened, None) for x in p.accounts if x.bank == a.bank]
    many = heavy(rng, 0.2)  # 적금·예금 계좌가 많은 고객 (표가 길어진다)
    for _ in range(rng.randint(6, 14) if many else rng.choice([0, 1, 1, 2, 3])):
        kind = rng.choice(["정기예금", "정기적금", "주택청약종합저축", "자유적립식예금"] + (["MMDA", "기업자유예금", "청년도약계좌", "보통예금"] if many else []))
        opened = rand_date(rng, date(2018, 1, 1), base - timedelta(days=60))
        if kind == "주택청약종합저축":
            bal, mat = rng.randint(24, 150) * 100_000, None
        elif kind in ("MMDA", "보통예금", "기업자유예금"):
            bal, mat = K.round_to(rng.uniform(1e4, 3e7), 1), None
        elif kind == "정기예금":
            bal = K.round_to(rng.uniform(5e6, 1e8), 1_000_000)
            mat = opened + timedelta(days=365 * rng.choice([1, 2, 3]))
        else:
            bal = rng.randint(6, 36) * rng.choice([100_000, 300_000, 500_000])
            mat = opened + timedelta(days=365 * rng.choice([1, 2, 3]))
        while mat and mat <= base:
            mat += timedelta(days=365)
        accts.append((_acct_no(rng, a.bank), kind, bal, opened, mat))
    if not many:
        accts = accts[:5]  # 한 장에 5계좌까지
    rows, remarks = [], []
    for no, kind, bal, opened, mat in accts:
        pledged = mat is not None and rng.random() < 0.1
        rows.append({"kind": kind, "account_no": no, "balance": won(bal, ""), "uncleared": "0",
                     "pledge": "유" if pledged else "무", "restriction": "무"})
    # 특수 상황: 질권 설정 (예금담보대출 등) — 해당 계좌 질권 '유' + 비고에 질권자 기재
    if special(rng, "pledge", 0.1):
        cand = [i for i, x in enumerate(accts) if x[4] is not None] or list(range(len(rows)))
        i = rng.choice(cand)
        rows[i]["pledge"] = "유"
        who = rng.choice([f"{a.bank} (예금담보대출)", f"{a.bank} (예금담보대출)", "서울보증보험(주)", f"{K.make_name(rng, rng.choice('MF'))[0]} (임대차보증금 담보)"])
        remarks.append(f"계좌번호 {rows[i]['account_no']} : 질권설정 (질권자 : {who}, 설정금액 {won(K.round_to(accts[i][2] * rng.uniform(0.5, 1.0), 10_000))})")
    # 특수 상황: 압류·가압류 — 지급정지 사유 표기
    if special(rng, "seizure", 0.06):
        i = 0
        kind = rng.choice(["압류", "가압류", "지급정지"])
        rows[i]["restriction"] = kind
        court = rng.choice(["서울중앙지방법원", "서울남부지방법원", "수원지방법원", "부산지방법원", "인천지방법원", "대전지방법원"])
        case = f"{base.year - rng.choice([0, 1])}{rng.choice(['타채', '카단', '카합'])}{rng.randint(1000, 99999)}"
        if kind == "지급정지":
            remarks.append(f"계좌번호 {rows[i]['account_no']} : 지급정지 (사고신고 접수)")
        else:
            remarks.append(f"계좌번호 {rows[i]['account_no']} : {kind} ({court} {case}, 청구금액 {won(K.round_to(rng.uniform(1e6, 3e7), 10_000))})")
    # 특수 상황: 외화예금 — 외화 잔액과 기준일 매매기준율 환산액
    fx = None
    if special(rng, "foreign_currency", 0.12):
        cur, rate = rng.choice([("USD", rng.uniform(1300, 1450)), ("EUR", rng.uniform(1420, 1600)), ("JPY", rng.uniform(880, 980) / 100)])
        amt = round(rng.uniform(800, 60_000) * (100 if cur == "JPY" else 1), 2 if cur != "JPY" else 0)
        krw = int(amt * rate)
        fx = f"{cur} {rate * (100 if cur == 'JPY' else 1):,.2f}{' (100엔당)' if cur == 'JPY' else ''}"
        rows.append({"kind": f"외화보통예금({cur})", "account_no": _acct_no(rng, a.bank), "balance": won(krw, ""),
                     "fx_amount": f"{cur} {amt:,.2f}" if cur != "JPY" else f"{cur} {amt:,.0f}",
                     "uncleared": "0", "pledge": "무", "restriction": "무"})
        accts.append((rows[-1]["account_no"], "외화", krw, None, None))
    total = sum(x[2] for x in accts)
    d = {
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
    if remarks:
        d["remarks"] = remarks
    if fx:
        d["fx_rate"] = fx
    return d


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
    rows, lump, inst, fees, next_month, cash = [], 0, 0, 0, 0, 0
    n = rng.randint(40, 110) if heavy(rng, 0.25) else rng.randint(10, 16)  # 이용내역이 많은 회원은 여러 쪽
    items = []  # (이용일, 가맹점, 금액, 할부개월, 회차, 무이자, 종류)
    for _ in range(n):
        if rng.random() < 0.18:
            months = rng.choice([2, 3, 3, 5, 6, 10, 12])
            seq = rng.randint(1, months)
            amt = K.round_to(rng.uniform(200_000, 2_500_000), 100)
            used = months_back(us_start, seq - 1) + timedelta(days=rng.randint(0, 27))
            items.append((used, rng.choice(_BIG_SHOPS), amt, months, seq, rng.random() < 0.5, "buy"))
        else:
            used = us_start + timedelta(days=rng.randint(0, (us_end - us_start).days))
            hi = rng.choice([25_000, 60_000, 60_000, 150_000])
            items.append((used, rng.choice(_SHOPS), K.round_to(rng.uniform(2_500, hi), 10), 1, 1, True, "buy"))
    rand_day = lambda: us_start + timedelta(days=rng.randint(0, (us_end - us_start).days))  # noqa: E731
    # 특수 상황: 해외 이용 (외화 금액을 원화로 환산, 해외이용수수료 포함)
    if special(rng, "overseas", 0.12):
        for _ in range(rng.randint(1, 4)):
            m_, cur, rt = rng.choice([("AMAZON.COM", "USD", 1380), ("APPLE.COM/BILL", "USD", 1380), ("AGODA.COM", "USD", 1380),
                                      ("UNIQLO TOKYO", "JPY", 9.2), ("DON QUIJOTE OSAKA", "JPY", 9.2), ("NETFLIX.COM", "USD", 1380),
                                      ("STARBUCKS SINGAPORE", "SGD", 1030), ("BOOKING.COM", "EUR", 1500)])
            fa = round(rng.uniform(5, 400) * (100 if cur == "JPY" else 1), 2 if cur != "JPY" else 0)
            krw = _t10_c(fa * rt * 1.0125)  # 국제브랜드·해외서비스 수수료 포함
            fa_s = f"{fa:,.2f}" if cur != "JPY" else f"{fa:,.0f}"
            items.append((rand_day(), f"{m_} ({cur} {fa_s})", krw, 1, 1, True, "buy"))
    # 특수 상황: 현금서비스(단기카드대출) 이용
    if special(rng, "cash_advance", 0.12):
        for _ in range(rng.randint(1, 2)):
            items.append((rand_day(), rng.choice(["현금서비스", "단기카드대출(현금서비스)"]),
                          rng.choice([300_000, 500_000, 1_000_000, 1_500_000, 2_000_000]), 0, 0, False, "cash"))
    # 특수 상황: 승인취소 (반품·결제취소) — 음수 금액
    if special(rng, "cancelled", 0.1):
        buys = [x for x in items if x[6] == "buy" and x[3] == 1]
        for x in rng.sample(buys, min(len(buys), rng.randint(1, 2))):
            cd = min(us_end, x[0] + timedelta(days=rng.randint(0, 6)))
            items.append((cd, f"{x[1]} 승인취소" if rng.random() < 0.5 else f"{x[1]}(취소)", -x[2], 1, 1, True, "cancel"))
    items.sort(key=lambda x: x[0])
    for used, shop, amt, months, seq, free, kind in items:
        if kind == "cash":
            fee = _t10_c(amt * rng.uniform(0.165, 0.199) * rng.randint(10, 35) / 365)
            prin, after = amt, 0
            cash += prin
            months_s, seq_s = "현금서비스", "-"
        elif months == 1:
            prin, fee, after = amt, 0, 0
            lump += prin
            months_s, seq_s = "일시불", "-"
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
            months_s, seq_s = f"{months}개월", f"{seq}/{months}"
        fees += fee
        rows.append({"date": D(used, "dot"), "merchant": shop, "amount": won(amt, ""),
                     "months": months_s, "seq": seq_s,
                     "principal": won(prin, ""), "fee": won(fee, ""), "after": won(after, "")})
    total = lump + inst + cash + fees
    summary_extra = {}
    # 특수 상황: 전월 결제대금 연체 — 연체원금·연체이자가 이번 달 청구에 더해진다
    if special(rng, "overdue", 0.06):
        od = K.round_to(rng.uniform(150_000, 1_800_000), 10)
        od_fee = _t10_c(od * rng.uniform(0.17, 0.199) * rng.randint(15, 45) / 365)
        summary_extra = {"overdue": won(od, ""), "overdue_fee": won(od_fee, "")}
        total += od + od_fee
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
        "summary": {"lump": won(lump, ""), "installment": won(inst, ""), "cash": won(cash, ""), "fee": won(fees, ""),
                    "total": won(total, ""), "next_month": won(next_month, ""), "limit": won(limit, ""), **summary_extra},
        "fee_rate": f"연 {fee_rate * 100:.1f}%",
        # 100원당 할부개월별 수수료 (원금균등 상환 가정: 100 × 연율/12 × (n+1)/2)
        "fee_per_100": [{"months": f"{n}개월", "fee": f"{100 * fee_rate / 12 * (n + 1) / 2:.2f}원"} for n in (2, 3, 6, 10, 12)],
        "rows": rows,
        "sum": {"amount": won(sum(x[2] for x in items), ""), "principal": won(lump + inst + cash, ""), "fee": won(fees, "")},
    }


def _t10_c(x: float) -> int:
    return int(x) // 10 * 10
