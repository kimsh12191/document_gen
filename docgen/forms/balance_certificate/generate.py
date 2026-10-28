"""balance_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/finance.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.finance import _acct_no, _korean_amount  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


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
