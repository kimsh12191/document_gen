"""commercial_invoice: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/fx.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.fx import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _Out,
    _dec,
    _en,
    _goods_rows,
    _money,
    _party,
    _remarks,
    _shipment,
)
from decimal import Decimal, ROUND_HALF_UP
from docgen.registry import doc


@doc("commercial_invoice", "상업송장(Commercial Invoice)", "fx")
def commercial_invoice(p: Profile, rng: random.Random) -> dict:
    """COMMERCIAL INVOICE (수출입 상업송장). 품목이 많으면(heavy, 프로필 단위) 여러 쪽, 합계는 마지막 쪽."""
    s = _shipment(p)
    cur = s["cur"]
    out = _Out({
        "shipper": _party(s, "seller"),
        "consignee": _party(s, "consignee"),
        "notify": rng.choice(["SAME AS CONSIGNEE", "SAME AS ABOVE"]) if not s["lc_no"] else f"{s['consignee']['name']}",
        "port_of_loading": s["pol"],
        "final_destination": s["pod"],
        "carrier": f"{s['vessel']} V.{s['voyage']}",
        "sailing_date": _en(s["on_board"], rng),
        "invoice_no": s["inv_no"],
        "invoice_date": _en(s["inv_date"], rng),
        "terms": {"delivery": f"{s['incoterm']} {s['incoterm_place']} (INCOTERMS 2020)", "payment": s["payment"]},
        "origin": s["origin"],
        "marks": s["marks"],
        "items": _goods_rows(s),
        "total_quantity": f"{s['total_pkgs']:,} {s['pkg_unit']}",
        "total_amount": f"{cur} {_money(s['total'], cur)}",
        "signed_by": s["seller"]["name"],
        "signer": s["signer"],
    })
    if s["lc_no"]:
        out["lc"] = {"no": s["lc_no"], "date": _en(s["lc_date"], rng), "bank": s["lc_bank"]}
    _remarks(s, rng, out)
    mid = s["intermediary"]
    if mid:  # 제3국 결제: 대금은 송장 발행인(제3국 무역회사) 계좌로
        out["beneficiary_bank"] = {"name": mid["bank"], "swift": mid["swift"], "account": mid["account"]}
    if s["incoterm"] == "CIF" and special(rng, "price_breakdown", 0.3):
        # CIF 가격 구성: FOB 가격 + 해상운임 + 보험료
        q = _dec(cur)
        freight = (s["total"] * Decimal(str(round(rng.uniform(0.015, 0.05), 4)))).quantize(q)
        ins = (s["total"] * Decimal("1.1") * Decimal("0.0007")).quantize(q, ROUND_HALF_UP)
        out["price_breakdown"] = {"fob": f"{cur} {_money(s['total'] - freight - ins, cur)}",
                                  "freight": f"{cur} {_money(freight, cur)}", "insurance": f"{cur} {_money(ins, cur)}"}
    return out
