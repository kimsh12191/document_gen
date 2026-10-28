"""card_statement: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/finance.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.finance import _CARD_COS, _SHOPS  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


_BIG_SHOPS = ["삼성디지털프라자", "롯데하이마트", "LG전자베스트샵", "한샘", "이케아코리아", "대한항공", "아시아나항공",
              "서울밝은치과의원", "현대백화점", "신세계백화점", "애플코리아"]


def _mask_acct(no: str) -> str:
    """계좌번호 가운데 일부를 * 처리. 예) 123-456-789012 -> 123-456-**9012"""
    digits = [i for i, c in enumerate(no) if c.isdigit()]
    hide = set(digits[-6:-4] + digits[-8:-6]) if len(digits) > 8 else set(digits[-6:-4])
    return "".join("*" if i in hide else c for i, c in enumerate(no))


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
