"""local_tax_payment_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/tax.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.tax import _cert_purpose  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


# ---------------------------------------------------------------------------
# 지방세 납세증명서
# ---------------------------------------------------------------------------
@doc("local_tax_payment_certificate", "지방세 납세증명서", "tax")
def local_tax_payment_certificate(p: Profile, rng: random.Random) -> dict:
    """정부24·위택스 발급 지방세 납세증명서 (체납 없음). 개인사업자면 상호·사업자등록번호도 적는다.

    special local_deferral: 징수유예등 내역 1~2건 (재산세·자동차세·지방소득세), local_short_validity: 유효기간이
    30일 안에 오는 정기분 납기까지.
    """
    issue = p.issue_date
    taxpayer = {
        "name": p.person.name,
        "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.7 else p.person.rrn,
        "address": p.person.address.road_full,
    }
    if rng.random() < 0.4:
        taxpayer.update(trade_name=p.business.name, biz_no=p.business.biz_no)
    end = issue + timedelta(days=29)
    if special(rng, "local_short_validity", 0.08):
        cands = sorted(date(y, m, d) for y in (issue.year, issue.year + 1)
                       for m, d in ((6, 30), (7, 31), (8, 31), (9, 30), (12, 31)))
        end = next((d for d in cands if issue < d <= end), end)
    out = {
        "issue_no": issue_no(rng),
        "taxpayer": taxpayer,
        "valid_period": f"{D(issue, 'kor')} ~ {D(end, 'kor')}",
        "purpose": _cert_purpose(rng, p),
        "arrears": "없음",
        "issue_date": D(issue, "kor"),
        "issuer": district_office(p.person.address),
    }
    if special(rng, "local_deferral", 0.08):
        rows = []
        opts = [("재산세", 7, 31), ("재산세", 9, 30), ("자동차세", 6, 30), ("자동차세", 12, 31), ("지방소득세", 5, 31)]
        for item, m, d in rng.sample(opts, rng.choice([1, 1, 2])):
            due = date(issue.year, m, d)
            if due >= issue - timedelta(days=10):
                due = date(issue.year - 1, m, d)
            start = due + timedelta(days=rng.randint(-15, 5))
            if start + timedelta(days=180) <= issue:
                start = issue - timedelta(days=rng.randint(20, 150))
            amt = K.round_to(rng.uniform(1.2e5, 2.4e6), 10)
            rows.append({"tax_year": f"{due.year}", "tax_item": item, "due": D(due, "dot"), "amount": won(amt, ""),
                         "period": f"{D(start, 'dot')} ~ {D(start + timedelta(days=rng.choice([181, 273, 364])), 'dot')}"})
        out["deferrals"] = rows
    else:
        out["deferral"] = "해당없음"
    return out
