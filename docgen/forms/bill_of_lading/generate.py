"""bill_of_lading: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/fx.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.fx import _Out, _party, _shipment, _words  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from decimal import Decimal
from docgen.registry import doc


@doc("bill_of_lading", "선하증권(B/L)", "fx")
def bill_of_lading(p: Profile, rng: random.Random) -> dict:
    """BILL OF LADING (해상 선하증권). 컨테이너가 많으면 부속 목록(ATTACHED SHEET)이 다음 쪽에 붙는다."""
    s = _shipment(p)
    if s["lc_no"]:
        cons_name, cons_addr = f"TO ORDER OF {s['lc_bank']}", None
    elif s["payment"].startswith("D/"):
        cons_name, cons_addr = "TO ORDER", None
    else:
        cons_name, cons_addr = s["consignee"]["name"], s["consignee"]["address"]
    consignee = {"name": cons_name}
    if cons_addr:
        consignee["address"] = cons_addr
    notify = _party(s, "consignee") if cons_addr is None else {"name": "SAME AS CONSIGNEE"}
    pod_place = s["pod"].split(",")[0]
    pol_place = s["pol"].split(",")[0]
    groups: dict[int, list] = {}
    for it in s["items"]:
        groups.setdefault(it["base"], []).append(it)
    descr = "\n".join(f"{g[0]['base_trade'] if len(g) > 1 else g[0]['trade']}  {sum(x['qty'] for x in g):,} {g[0]['unit']}"
                      for g in groups.values())
    conts = s["containers"]
    rider = len(conts) >= 4 or (s["heavy"] and len(conts) >= 2)
    out = _Out({
        "bl_no": s["bl_no"],
        "booking_no": s["booking_no"],
        "shipper": _party(s, "shipper"),
        "consignee": consignee,
        "notify": notify,
        "pre_carriage": rng.choice(["TRUCK", "BY TRUCK"]),
        "place_of_receipt": f"{pol_place} CY",
        "vessel_voyage": f"{s['vessel']} {s['voyage']}",
        "port_of_loading": s["pol"],
        "port_of_discharge": s["pod"],
        "place_of_delivery": f"{pod_place} CY",
        "forwarder": s["forwarder"],
        "containers": [{"no": c["no"], "seal": c["seal"], "type": c["type"]} for c in conts],
        "marks": s["marks"],
        "container_count": f"{len(conts)} X {conts[0]['type']}",
        "packages": f"{s['total_pkgs']:,} {s['pkg_unit']}",
        "origin": s["origin"],
        "description": descr,
        "gross_weight": f"{s['gross']:,.2f} KGS",
        "measurement": f"{s['cbm']:,.3f} CBM",
        "total_words": f"SAY: {_words(len(conts))} ({len(conts)}) CONTAINER{'S' if len(conts) > 1 else ''} ONLY",
        "freight": "FREIGHT PREPAID" if s["freight_prepaid"] else "FREIGHT COLLECT",
        "freight_payable_at": pol_place if s["freight_prepaid"] else pod_place,
        "originals": "THREE (3)",
        "issue_place": pol_place,
        "issue_date": D(s["on_board"], "en"),
        "on_board_date": D(s["on_board"], "en"),
        "carrier": s["carrier"].upper(),
    })
    if s["lc_no"]:
        out["lc_no"] = s["lc_no"]
    if rider:  # 부속 목록: 컨테이너별 포장수·중량·용적
        for c, src in zip(out["containers"], conts):
            c.update({"packages": f"{src['pkgs']:,} {s['pkg_unit']}", "gross_weight": f"{src['gross']:,.2f}",
                      "measurement": f"{src['cbm']:,.3f}"})
        out.opt["rider"] = True
    if special(rng, "freight_charges", 0.25):  # 운임 명세(요율·금액) 기재
        n = len(conts)
        big = conts[0]["type"].startswith("40")
        rate = Decimal(rng.randint(9, 38) * 50 * (2 if big else 1))
        pc = "prepaid" if s["freight_prepaid"] else "collect"
        rows = [("OCEAN FREIGHT", rate, pc), ("BUNKER ADJUSTMENT FACTOR (BAF)", Decimal(rng.randint(4, 12) * 25 * (2 if big else 1)), pc)]
        if rng.random() < 0.5:
            rows.append(("LOW SULPHUR SURCHARGE (LSS)", Decimal(rng.randint(2, 6) * 10 * (2 if big else 1)), pc))
        rows.append(("TERMINAL HANDLING CHARGE (ORIGIN)", Decimal(rng.randint(10, 26) * 10), "prepaid"))
        out["charges"] = [{"name": nm, "quantity": f"{n:.2f}", "rate": f"{rt:,.2f}", "per": "CNTR",
                           side: f"USD {rt * n:,.2f}"} for nm, rt, side in rows]
    if cons_addr and not s["lc_no"]:
        if special(rng, "surrender", 0.2):  # 서렌더 B/L: 선적지에서 원본 회수, 사본에 SURRENDERED 스탬프
            out["surrender"] = "SURRENDERED"
            out["surrender_date"] = D(s["on_board"] + timedelta(days=rng.randint(0, 3)), "en")
        elif special(rng, "sea_waybill", 0.06):  # 해상화물운송장 (원본 없음)
            out["document_type"] = "SEA WAYBILL"
            out["originals"] = "ZERO (0)"
    return out
