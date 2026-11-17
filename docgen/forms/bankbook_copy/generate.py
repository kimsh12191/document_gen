"""bankbook_copy: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/finance.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.registry import doc


def _bank_phone(rng: random.Random, p: Profile) -> str:
    return K.landline(rng, p.person.address.sido)


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
