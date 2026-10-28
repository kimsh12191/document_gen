"""vat_tax_base_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/tax.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.business import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _biz_facts,
    _half_base,
    _hometax_no,
    _industry,
    _pl,
    _prng,
    _tax_office,
    _vat_simple,
)
from docgen.docs.tax import _cert_purpose, _floor10, _signed  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


# ---------------------------------------------------------------------------
# 부가가치세 과세표준증명
# ---------------------------------------------------------------------------
_EXEMPT_ITEMS = ("학원", "농산물")


def _vat_periods(p: Profile) -> list[dict]:
    """과세기간 목록 (오래된 것부터). 간이과세자는 1년, 일반과세자는 반기. 간이→일반 전환(_biz_facts switch)이면
    전환 전은 간이(전환 연도는 1.1~6.30), 이후 일반."""
    b, issue = p.business, p.issue_date
    sw = _biz_facts(p)["switch"]
    simple_now = _vat_simple(p)
    out = []
    for y in range(b.established.year, issue.year + 1):
        simple_y = simple_now or (sw is not None and y < sw.year)
        if simple_y:
            start = max(date(y, 1, 1), b.established)
            out.append({"start": start, "end": date(y, 12, 31), "due": date(y + 1, 1, 25), "simple": True,
                        "base": _half_base(p, y, 1) + _half_base(p, y, 2), "y": y, "h": 0})
            continue
        for h in (1, 2):
            start = max(date(y, 1, 1) if h == 1 else date(y, 7, 1), b.established)
            end = date(y, 6, 30) if h == 1 else date(y, 12, 31)
            if start > end:
                continue
            simple_h = sw is not None and y == sw.year and h == 1
            out.append({"start": start, "end": end, "due": date(y, 7, 25) if h == 1 else date(y + 1, 1, 25),
                        "simple": simple_h, "base": _half_base(p, y, h), "y": y, "h": h})
    return [r for r in out if r["due"] < issue]


@doc("vat_tax_base_certificate", "부가가치세 과세표준증명", "tax")
def vat_tax_base_certificate(p: Profile, rng: random.Random) -> dict:
    """홈택스 발급 부가가치세 과세표준증명 (개인사업자).

    heavy: 3~5년치(일반 6~10기간). special: vat_prelim(예정신고 분리), vat_amended(수정신고 줄 추가),
    vat_late(기한후신고), vat_refund(시설투자 환급). 휴업(_biz_facts suspended) 기간은 매출 0 또는 감소,
    간이→일반 전환(simple_to_general)이면 앞쪽 기간이 1년 단위 간이과세 기간.
    """
    b = p.business
    issue = p.issue_date
    va_rate = _industry(b)[1]
    many = heavy(rng, 0.25)
    periods = _vat_periods(p)
    n_simple = rng.randint(4, 6) if many else 3
    n_general = rng.randint(6, 10) if many else 4
    keep = []
    for r in reversed(periods):
        if len(keep) >= (n_simple if r["simple"] and all(k["simple"] for k in keep) else n_general):
            break
        keep.append(r)
    keep.reverse()
    rows = []
    for r in keep:
        base = r["base"]
        if r["simple"]:
            full = (r["end"] - r["start"]).days > 200
            tax = 0 if base < (48_000_000 if full else 24_000_000) else \
                max(0, _floor10(int(base * va_rate * 0.1) - int(base * 0.7 * 0.013)))
        else:
            pl = _pl(p, r["y"])
            buy_ratio = (pl["cogs"] + pl["rent"] + pl["other_sga"] // 2) / max(pl["revenue"], 1)
            buy_ratio *= _prng(p, "vatbuy", r["y"], r["h"]).uniform(0.9, 1.1)
            card = int(base * 0.6 * 0.013) if b.biz_type in ("음식점업", "소매업") else 0
            tax = _floor10(int(base * 0.1 * (1 - buy_ratio)) - min(card, 5_000_000))
        filed = rand_date(rng, r["end"] + timedelta(days=5), min(r["due"], issue - timedelta(days=1)))
        rows.append({"start": r["start"], "end": r["end"], "kind": "정기확정", "filed": filed, "base": base, "tax": tax,
                     "due": r["due"], "simple": r["simple"]})
    general = [i for i, r in enumerate(rows) if not r["simple"] and r["base"] > 0]
    if general and special(rng, "vat_prelim", 0.1):  # 예정신고를 한 기간: 예정(1~3월) + 확정(4~6월)
        for i in sorted(rng.sample(general[-2:], min(2, len(general[-2:]))), reverse=True):
            r = rows[i]
            mid = date(r["start"].year, 3, 31) if r["end"].month == 6 else date(r["start"].year, 9, 30)
            if r["start"] > mid:
                continue
            share = rng.uniform(0.42, 0.55)
            pb = _floor10(int(r["base"] * share))
            pt = _floor10(int(r["tax"] * share))
            pre = {"start": r["start"], "end": mid, "kind": "예정신고", "base": pb, "tax": pt, "simple": False,
                   "filed": rand_date(rng, mid + timedelta(days=5), mid + timedelta(days=25)), "due": mid + timedelta(days=25)}
            rows[i] = dict(r, start=mid + timedelta(days=1), base=r["base"] - pb, tax=r["tax"] - pt)
            rows.insert(i, pre)
    if rows and special(rng, "vat_late", 0.06):
        i = rng.randrange(len(rows))
        r = rows[i]
        late = r["due"] + timedelta(days=rng.randint(5, 60))
        if late < issue:
            r.update(kind="기한후신고", filed=late)
    general = [i for i, r in enumerate(rows) if not r["simple"] and r["kind"] == "정기확정"]
    if general and special(rng, "vat_refund", 0.08):
        r = rows[rng.choice(general)]
        r["tax"] = -K.round_to(rng.uniform(2e6, 1.5e7), 10)
    if rows and special(rng, "vat_amended", 0.1):
        i = rng.randrange(len(rows))
        r = rows[i]
        filed = r["filed"] + timedelta(days=rng.randint(30, 200))
        if filed < issue:
            k = rng.uniform(1.02, 1.12)
            nb = _floor10(int(r["base"] * k))
            nt = r["tax"] + _floor10(int((nb - r["base"]) * 0.1))
            rows.insert(i + 1, dict(r, kind="수정신고", filed=filed, base=nb, tax=nt))
    fmt = rng.choice(["dash", "dot"])
    # 학원(교육용역)·농산물은 면세 매출이 대부분인 과·면세 겸영사업자로 본다.
    exempt_share = _prng(p, "vatexempt").uniform(0.85, 0.97) if b.biz_item in _EXEMPT_ITEMS else 0.0
    items = []
    for r in rows:
        exempt = _floor10(int(r["base"] * exempt_share))
        taxable = r["base"] - exempt
        tax = _floor10(int(r["tax"] * (1 - exempt_share))) if r["tax"] > 0 else r["tax"]
        items.append({"period": f"{D(r['start'], fmt)} ~ {D(r['end'], fmt)}", "kind": r["kind"],
                      "filed": D(r["filed"], fmt), "base_total": won(r["base"], ""), "base_taxable": won(taxable, ""),
                      "base_exempt": won(exempt, ""), "tax": _signed(tax)})
    return {
        "issue_no": _hometax_no(rng),
        "taxpayer": {
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn),
            "trade_name": b.name,
            "biz_no": b.biz_no,
            "address": b.address.road_full,
            "biz_type": b.biz_type,
            "biz_item": b.biz_item,
        },
        "items": items,
        "purpose": _cert_purpose(rng, p),
        "issue_date": D(issue, "kor"),
        "issuer": _tax_office(b.address),
    }
