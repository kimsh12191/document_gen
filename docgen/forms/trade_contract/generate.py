"""trade_contract: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/fx.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
import re
from docgen.docs.fx import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _Out,
    _dec,
    _en,
    _goods_rows,
    _money,
    _party,
    _shipment,
    _words,
)
from decimal import Decimal
from docgen.registry import doc


_PKG_WORD = {"CTNS": "CARTONS", "CASES": "WOODEN CASES", "ROLLS": "ROLLS", "BAGS": "BAGS", "DRUMS": "DRUMS"}


def _amount_words(x: Decimal, cur: str) -> str:
    names = {"USD": ("US DOLLARS", "CENTS"), "EUR": ("EURO", "CENTS"), "JPY": ("JAPANESE YEN", ""),
             "GBP": ("POUNDS STERLING", "PENCE"), "CAD": ("CANADIAN DOLLARS", "CENTS"), "AUD": ("AUSTRALIAN DOLLARS", "CENTS")}
    major, minor = names[cur]
    whole = int(x)
    cents = int((x - whole) * 100)
    s = f"SAY {names[cur][0]} {_words(whole)}"
    if cents and minor:
        s += f" AND {minor} {_words(cents)}"
    return s + " ONLY"


_GTC = [  # (제목, 본문) — 계약서 뒷면/별첨 일반거래조건. {..} 는 정답 값으로 채운다
    ("Quality", "The Seller shall guarantee that the quality of the goods is in accordance with the specifications and samples approved by the Buyer. Any deviation shall be notified to the Buyer in writing before shipment."),
    ("Quantity", "Quantity shown herein is subject to a variation of {qty_tolerance} more or less at the Seller's option, and the difference shall be settled at the contract price."),
    ("Shipment", "The date of the Bill of Lading shall be accepted as conclusive evidence of the date of shipment. The Seller shall advise the Buyer by fax or e-mail of the vessel name, B/L number, quantity and invoice value within 3 days after shipment."),
    ("Delay in Shipment", "In case of delay in shipment caused by the Seller, the Seller shall pay a penalty of {late_penalty} of the value of the delayed goods per week, not exceeding 5% of the total contract value."),
    ("Payment", "Payment shall be made as specified on the face hereof. All banking charges outside the Buyer's country shall be for the account of the Seller."),
    ("Packing", "Goods shall be packed in strong export packing, with due care for protection against moisture, rough handling and pilferage. Each package shall bear the shipping mark and package number."),
    ("Insurance", "Where insurance is to be effected by the Seller, it shall be covered with an insurance company of good standing for 110% of the invoice value."),
    ("Inspection", "The Buyer shall have the right to inspect the goods within {inspection_days} days after arrival at the port of destination. Inspection at the port of loading shall not prejudice the Buyer's rights of claim."),
    ("Claims", "Any claim by the Buyer regarding quality or quantity shall be made in writing within {claim_days} days after arrival of the goods at destination, accompanied by a survey report of a recognized surveyor."),
    ("Warranty", "The Seller warrants the goods against defects in material and workmanship for a period of {warranty} from the date of delivery."),
    ("Force Majeure", "Neither party shall be liable for failure or delay in performance due to causes beyond its reasonable control, including acts of God, war, epidemics, strikes, government orders or port congestion."),
    ("Intellectual Property", "The Seller shall hold the Buyer harmless from any claim of infringement of patents, trademarks, designs or copyrights arising from the goods supplied hereunder."),
    ("Taxes and Duties", "All taxes and duties levied in the country of origin shall be borne by the Seller, and those in the country of destination by the Buyer."),
    ("Late Payment", "Overdue payments shall bear interest at the rate of {late_interest} per annum from the due date until the date of actual payment."),
    ("Termination", "Either party may terminate this contract by written notice if the other party commits a material breach and fails to remedy it within 30 days after receipt of such notice."),
    ("Confidentiality", "Each party shall keep confidential all technical and commercial information received from the other party in connection with this contract."),
    ("Assignment", "Neither party shall assign or transfer this contract or any rights hereunder without the prior written consent of the other party."),
    ("Governing Law", "This contract shall be governed by and construed in accordance with the laws of {governing_law}."),
    ("Notices", "All notices under this contract shall be in writing and sent by registered mail, courier or e-mail to the addresses stated herein."),
    ("Entire Agreement", "This contract constitutes the entire agreement between the parties and supersedes all prior negotiations. Any amendment shall be valid only if made in writing and signed by both parties."),
]


@doc("trade_contract", "무역 매매계약서(Sales Contract)", "fx")
def trade_contract(p: Profile, rng: random.Random) -> dict:
    """SALES CONTRACT (수출입 매매계약서)."""
    s = _shipment(p)
    cur = s["cur"]
    seller, buyer = "seller", "consignee"
    corp_signer = (p.person.name_en.title(), rng.choice(["President & CEO", "CEO", "Representative Director"]))
    cp_signer = (s["signer"] if s["intermediary"] else s["cp"]["contact"],
                 rng.choice(["Sales Director", "General Manager", "Export Manager", "Managing Director"]))
    s_sign, b_sign = (cp_signer, corp_signer) if s["direction"] == "import" else (corp_signer, cp_signer)
    latest = s["on_board"] + timedelta(days=rng.randint(3, 20))
    lots = s["lots"] or 1
    if s["lots"]:  # 분할선적: 계약 물량 전체, 회차별 선적 기한
        first = s["on_board"] - timedelta(days=30 * (s["lot"] - 1) + rng.randint(0, 5))
        sched = "; ".join(f"{['1st', '2nd', '3rd'][i]} lot not later than {D(first + timedelta(days=30 * i + 10), 'en_long')}"
                          for i in range(s["lots"]))
        shipment = (f"In {_words(s['lots']).lower()} ({s['lots']}) lots of equal quantity: {sched}. "
                    f"Partial shipments allowed, transshipment {rng.choice(['allowed', 'not allowed'])}.")
    else:
        shipment = (f"Not later than {D(latest, 'en_long')}. "
                    f"Partial shipments {rng.choice(['allowed', 'not allowed'])}, transshipment {rng.choice(['allowed', 'not allowed'])}.")
    pay = {
        "T/T IN ADVANCE": "100% by telegraphic transfer in advance, within 7 days after the date of this contract.",
        "T/T 30 DAYS AFTER B/L DATE": "By telegraphic transfer within 30 days after B/L date.",
        "T/T 60 DAYS AFTER B/L DATE": "By telegraphic transfer within 60 days after B/L date.",
        "L/C AT SIGHT": "By an irrevocable documentary credit at sight, to be opened within 15 days after contract date.",
        "L/C 90 DAYS AFTER B/L DATE": "By an irrevocable usance L/C 90 days after B/L date, to be opened within 15 days after contract date.",
        "D/P AT SIGHT": "Documents against payment at sight through the Buyer's bank.",
        "D/A 60 DAYS AFTER B/L DATE": "Documents against acceptance, 60 days after B/L date.",
    }[s["payment"]]
    mid = s["intermediary"]
    if mid:
        pay += f" Payment to be remitted to the Seller's account with {mid['bank'].title()} (SWIFT: {mid['swift']})."
    clauses = {
        "price_terms": f"{s['incoterm']} {s['incoterm_place']} (INCOTERMS 2020), prices in {cur}.",
        "shipment": shipment,
        "payment": pay,
        "packing": f"Export standard packing in {_PKG_WORD.get(s['pkg_unit'], 'packages').lower()}, suitable for ocean transportation.",
        "inspection": ("Inspection performed under the export regulation of Korea is final in respect of quality and/or conditions of the contracted goods."
                       if s["direction"] == "export" else
                       rng.choice(["Seller's inspection at factory shall be final as to quality and quantity.",
                                   "Inspection by an independent surveyor (SGS or equivalent) at the port of loading; cost borne by the Seller."])),
        "origin": s["origin"].title() if s["origin"] != "KOREA" else "Republic of Korea",
        "shipping_mark": s["marks"].replace(f"C/NO. 1-{s['total_pkgs']}", "C/NO. 1-UP"),
        "port_of_shipment": s["pol"],
        "destination": s["pod"],
        "arbitration": rng.choice([
            "Any dispute shall be finally settled by arbitration in Seoul under the Arbitration Rules of the Korean Commercial Arbitration Board.",
            "Any dispute shall be settled by arbitration in Singapore under the SIAC Rules.",
        ]),
    }
    if s["incoterm"] == "CIF":
        clauses["insurance"] = "To be covered by the Seller for 110% of invoice value against Institute Cargo Clauses (A)."
    if mid:
        clauses["manufacturer"] = f"{s['shipper']['name']}, {s['shipper']['address']} (goods to be shipped directly from the manufacturer)"
    total = (s["total"] * lots).quantize(_dec(cur))
    sign_date = s["contract_date"] + timedelta(days=rng.randint(0, 4))
    out = _Out({
        "contract_no": s["contract_no"],
        "contract_date": _en(s["contract_date"], rng),
        "seller": {**_party(s, seller), "signer": s_sign[0], "title": s_sign[1]},
        "buyer": {**_party(s, buyer), "signer": b_sign[0], "title": b_sign[1], "sign_date": D(sign_date, "en")},
        "items": _goods_rows(s, lots),
        "total_amount": f"{cur} {_money(total, cur)}",
        "total_words": _amount_words(total, cur),
        "clauses": clauses,
    })
    out["seller"]["sign_date"] = D(s["contract_date"], "en")
    if heavy(rng, 0.3):  # 일반거래조건(General Terms and Conditions) 12~20개 조항이 별첨으로 붙는 계약서
        k = rng.randint(12, len(_GTC))
        picks = sorted(rng.sample(range(len(_GTC)), k))
        out["gtc_terms"] = {
            "qty_tolerance": rng.choice(["3%", "5%", "10%"]), "late_penalty": rng.choice(["0.5%", "1%"]),
            "inspection_days": str(rng.choice([14, 21, 30])), "claim_days": str(rng.choice([14, 30, 60, 90])),
            "warranty": rng.choice(["twelve (12) months", "eighteen (18) months", "twenty-four (24) months"]),
            "late_interest": rng.choice(["6%", "8%", "10%", "12%"]),
            "governing_law": rng.choice(["the Republic of Korea", "England and Wales", "Singapore", "the State of New York, U.S.A."]),
        }
        out.opt["gtc"] = [_GTC[i] for i in picks]
        used = set(re.findall(r"\{(\w+)\}", " ".join(_GTC[i][1] for i in picks)))
        out["gtc_terms"] = {k: v for k, v in out["gtc_terms"].items() if k in used}
    if special(rng, "price_amend", 0.12):  # 인쇄된 단가 하나를 손으로 고치고 이니셜 (정답은 고친 값)
        out.opt["amend_item"] = rng.randrange(len(out["items"]))
    if special(rng, "hand_filled", 0.3):  # 서명 아래 이름·직위·일자를 손으로 기재
        out.opt["hand"] = True
    return out
