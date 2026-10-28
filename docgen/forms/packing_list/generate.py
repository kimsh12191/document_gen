"""packing_list: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/fx.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.fx import _Out, _en, _party, _remarks, _shipment  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("packing_list", "포장명세서(Packing List)", "fx")
def packing_list(p: Profile, rng: random.Random) -> dict:
    """PACKING LIST (포장명세서). 상업송장과 같은 선적 정보. 품목이 많으면 여러 쪽, 컨테이너별로 나눠 적기도 한다."""
    s = _shipment(p)
    rows, start = [], 1
    for it in s["items"]:
        end = start + it["pkgs"] - 1
        rows.append({"ctn_no": f"{start}-{end}" if end > start else str(start), "description": it["trade"],
                     "packages": f"{it['pkgs']:,} {it['pkg']}", "quantity": f"{it['qty']:,} {it['unit']}",
                     "net_weight": f"{it['net']:,.2f}", "gross_weight": f"{it['gross']:,.2f}", "measurement": f"{it['cbm']:,.3f}"})
        start = end + 1
    out = _Out({
        "shipper": _party(s, "seller"),
        "consignee": _party(s, "consignee"),
        "notify": "SAME AS CONSIGNEE",
        "port_of_loading": s["pol"],
        "final_destination": s["pod"],
        "carrier": f"{s['vessel']} V.{s['voyage']}",
        "sailing_date": _en(s["on_board"], rng),
        "invoice_no": s["inv_no"],
        "invoice_date": _en(s["inv_date"], rng),
        "marks": s["marks"],
        "items": rows,
        "total": {"packages": f"{s['total_pkgs']:,} {s['pkg_unit']}", "net_weight": f"{s['net']:,.2f} KGS",
                  "gross_weight": f"{s['gross']:,.2f} KGS", "measurement": f"{s['cbm']:,.3f} CBM"},
        "signed_by": s["seller"]["name"],
        "signer": s["signer"],
    })
    if s["lc_no"]:
        out["lc_no"] = s["lc_no"]
    _remarks(s, rng, out)
    conts = s["containers"]
    if len(conts) > 1 and all(it["cont"] is not None for it in s["items"]) and special(rng, "by_container", 0.6):
        # 컨테이너별 구분: 줄마다 실린 컨테이너, 컨테이너 소계
        out["containers"] = [{"no": c["no"], "seal": c["seal"], "packages": f"{c['pkgs']:,} {s['pkg_unit']}",
                              "net_weight": f"{c['net']:,.2f}", "gross_weight": f"{c['gross']:,.2f}",
                              "measurement": f"{c['cbm']:,.3f}"} for c in conts]
        out.opt["cont_of"] = [it["cont"] for it in s["items"]]
    return out
