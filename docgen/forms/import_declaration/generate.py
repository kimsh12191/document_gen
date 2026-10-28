"""import_declaration: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/fx.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
import re
from docgen.docs.fx import _dec, _money, _price_str, _shipment  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from decimal import Decimal, ROUND_DOWN
from docgen.registry import doc


_FTA = {"US": ("FUS1", "한미FTA"), "DE": ("FEU1", "한EU FTA"), "VN": ("FVN1", "한베트남FTA"),
        "SG": ("FSG1", "한싱가포르FTA"), "CN": ("FCN1", "한중FTA")}


_CUR_RATE = {"USD": (1280, 1480), "EUR": (1400, 1620), "JPY": (8.6, 9.8)}


# ---------------------------------------------------------------------------
# 수입신고필증
# ---------------------------------------------------------------------------
_AMEND_REASONS = ["(33)단가 정정 - 송품장 단가 오기", "(32)수량 정정 - 실물 검량 결과", "(18)총중량 정정 - B/L 중량 정정",
                  "(30)모델·규격 정정 - 송품장 기재 착오", "(42)원산지표시 정정", "(51)환율 적용 착오 정정"]


# (감면부호, 감면 근거) — 관세 감면이 있는 란 (부호 체계는 단순화)
_REDUCTIONS = [("Y4570", "관세법 제95조 공장자동화물품", 30.0), ("Y5020", "관세법 제90조 학술연구용품", 80.0),
               ("Y4510", "관세법 제95조 환경오염방지물품", 30.0), ("Y8010", "조세특례제한법 제118조 감면", 50.0)]


@doc("import_declaration", "수입신고필증", "fx")
def import_declaration(p: Profile, rng: random.Random) -> dict:
    """수입신고필증 (UNI-PASS 발행 양식). 과세가격·관세·부가세가 계산상 일치한다.
    란은 세번부호(상품)별로 묶고, 같은 상품의 모델·규격 줄은 란 안의 규격 줄(01, 02 ...)로 적는다."""
    s = _shipment(p, force_import=True)
    corp, cp, cur = s["corp"], s["cp"], s["cur"]
    lo, hi = _CUR_RATE[cur]
    rate = Decimal(str(round(rng.uniform(lo, hi), 4 if cur == "JPY" else 2)))
    total = s["total"]
    # 운임·보험료 가산 (FOB/FCA: 운임+보험, CFR: 보험)
    freight = Decimal(0)
    if s["incoterm"] in ("FOB", "FCA"):
        freight = (Decimal(str(rng.uniform(600, 3800))) * len(s["containers"]) * {"USD": 1, "EUR": Decimal("0.92"), "JPY": 150}[cur]).quantize(_dec(cur))
    insurance = (total * Decimal("0.0007")).quantize(_dec(cur)) if s["incoterm"] != "CIF" else Decimal(0)
    cif = total + freight + insurance
    fta = _FTA.get(s["iso"]) if rng.random() < 0.7 else None
    usd_rate = Decimal(str(round(rng.uniform(*_CUR_RATE["USD"]), 2))) if cur != "USD" else rate
    groups: dict[int, list] = {}
    for it in s["items"]:
        groups.setdefault(it["base"], []).append(it)
    reduce_at = None
    if special(rng, "duty_reduction", 0.12):
        cands = [i for i, g in enumerate(groups.values()) if g[0]["duty"] and not fta]
        reduce_at = rng.choice(cands) if cands else None
    red = rng.choice(_REDUCTIONS)
    items, sum_tax_base, sum_duty, sum_vat = [], 0, 0, 0
    for i, g in enumerate(groups.values()):
        it0 = g[0]
        g_amount = sum((x["amount"] for x in g), Decimal(0))
        cif_i = (cif * g_amount / total).quantize(_dec(cur))
        krw = int((cif_i * rate).to_integral_value(ROUND_DOWN))
        if fta and it0["duty"]:
            code, d_rate = fta[0], 0.0
        elif it0["duty"] == 0:
            code, d_rate = "C", 0.0
        else:
            code, d_rate = "A", float(it0["duty"])
        duty = int(krw * d_rate / 100) // 10 * 10
        line = {
            "line_no": f"{i + 1:03d}",
            "std_name": it0["std"],
            "trade_name": it0["base_trade"].upper(),
            "specs": [{"no": f"{j + 1:02d}", "model": it["model"] + (f", {it['var']}" if it["var"] else ""),
                       "quantity": f"{it['qty']:,} {it['unit']}", "unit_price": _price_str(it["price"], cur),
                       "amount": _money(it["amount"], cur)} for j, it in enumerate(g)],
            "hs_code": it0["hs"],
            "net_weight": f"{sum((x['net'] for x in g), Decimal(0)):,.1f} KG",
            "taxable_usd": f"${(Decimal(krw) / usd_rate).quantize(Decimal('1'), ROUND_DOWN):,}",
            "taxable_krw": f"₩{krw:,}",
            "origin": f"{s['iso']}-{'B' if fta else 'G'}-{'Y' if fta else 'N'}",
            "duty_type": "관",
            "duty_rate": f"{d_rate:.2f}({code})",
        }
        if i == reduce_at:  # 관세 감면: 감면율·감면부호·감면액, 세액은 감면 후
            cut = int(duty * red[2] / 100) // 10 * 10
            line["reduction"] = {"rate": f"{red[2]:.2f}", "code": red[0], "amount": f"{cut:,}"}
            duty -= cut
        vat = (krw + duty) // 10 // 10 * 10
        line["duty_amount"] = f"{duty:,}"
        line["vat_rate"] = "10.00(A)"
        line["vat_amount"] = f"{vat:,}"
        items.append(line)
        sum_tax_base += krw
        sum_duty += duty
        sum_vat += vat
    total_krw = sum_tax_base
    vat_base = total_krw + sum_duty
    decl_date = s["arrival"] + timedelta(days=rng.randint(0, 3))
    accept = decl_date + timedelta(days=rng.randint(0, 1))
    customs = {"BUSAN, KOREA": ("030", "부산세관", "KRPUS 부산항", ["부산신항만(주)", "부산신항국제터미널", "한진부산컨테이너터미널", "동부부산컨테이너터미널"]),
               "INCHEON, KOREA": ("020", "인천세관", "KRINC 인천항", ["인천컨테이너터미널", "선광신컨테이너터미널", "한진인천컨테이너터미널"])}[s["pod"]]
    broker_name = f"{rng.choice(['한길', '세원', '대한', '국제', '미래', '정원'])}관세법인"
    cn = re.sub(r"주식회사|\(주\)|\s", "", corp.name)
    ccode = (cn + "가나다라")[:4] + f"{rng.randint(1, 9)}{rng.randint(100000, 999999)}"
    pay_code = {"T/T": "TT", "L/C": "LS" if "SIGHT" in s["payment"] else "LU", "D/P": "DP", "D/A": "DA"}[s["payment"][:3]]
    mid = s["intermediary"]
    out = {
        "decl_no": f"{rng.randint(10000, 99999)}-{decl_date.year % 100:02d}-{rng.randint(1000000, 9999999)}{rng.choice('MUX')}",
        "decl_date": D(decl_date, "slash"),
        "customs": f"{customs[0]}-{rng.randint(10, 19)}",
        "arrival_date": D(s["arrival"], "slash"),
        "bl_no": s["bl_no"],
        "cargo_no": f"{s['arrival'].year % 100:02d}{s['scac']}{rng.randint(100000, 999999)}I-{rng.randint(1, 9999):04d}-{rng.randint(1, 30):03d}",
        "warehouse_date": D(s["arrival"] + timedelta(days=rng.randint(0, 2)), "slash"),
        "collection_type": rng.choice(["11", "11", "43"]),
        "declarant": f"{broker_name} {_kname(rng)}",
        "importer": {"name": corp.name, "code": ccode},
        "taxpayer": {"code": ccode, "address": corp.address.road_short, "name": corp.name, "ceo": corp.ceo.name, "biz_no": corp.biz_no},
        "forwarder": s["forwarder"].upper(),
        # 중계무역이면 거래처(판매자)는 제3국 무역회사
        "supplier": f"{mid['name'].upper()} ({mid['iso']})" if mid else f"{cp['name'].upper()} ({s['iso']})",
        "clearance_plan": rng.choice(["D 보세구역장치후", "C 보세구역도착전", "B 입항전신고"]),
        "origin_cert": "Y" if fta else "N",
        "total_weight": f"{s['gross']:,.0f} KG",
        "total_packages": f"{s['total_pkgs']:,} {'GT' if s['pkg_unit'] == 'PKGS' else s['pkg_unit'][:2]}",
        "arrival_port": customs[2],
        "transport": "10 FCL",
        "export_country": f"{s['iso']} {cp['country']}",
        "vessel": s["vessel"],
        "master_bl": s["bl_no"],
        "carrier_code": s["scac"],
        "inspection_place": f"{customs[0]}{rng.randint(10000, 99999)}-{rng.randint(10, 99)}{rng.randint(100000, 999999)} "
                            + rng.choice(customs[3]),
        "items": items,
        "line_total": f"{len(items):03d}",
        "payment": f"{s['incoterm']}-{cur}-{_money(total, cur)}-{pay_code}",
        "exchange_rate": f"{rate:,.4f}" if cur == "JPY" else f"{rate:,.2f}",
        "freight": f"₩{int(freight * rate):,}",
        "insurance": f"₩{int(insurance * rate):,}",
        "total_taxable": f"₩{total_krw:,}",
        "vat_base": f"₩{vat_base:,}",
        "tax": {"duty": f"{sum_duty:,}", "vat": f"{sum_vat:,}", "total": f"{sum_duty + sum_vat:,}"},
        "customs_office": customs[1],
        "receipt_datetime": f"{D(decl_date, 'slash')} {rng.randint(9, 17):02d}:{rng.randint(0, 59):02d}",
        "accept_date": D(accept, "slash"),
        "officer": _kname(rng),
    }
    if special(rng, "amended", 0.1):  # 수리 후 정정: 세관기재란에 정정승인 일자·사유
        out["amendment"] = {"date": D(min(p.issue_date, accept + timedelta(days=rng.randint(2, 15))), "slash"),
                            "reason": rng.choice(_AMEND_REASONS)}
    return out


def _kname(rng: random.Random) -> str:
    return K.make_name(rng, rng.choice("MF"))[0]
