"""standard_financial_statement_proof: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/business.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.business import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _filed_year,
    _hometax_no,
    _itr_filing,
    _pl,
    _prng,
    _revenue,
    _signed,
    _split,
    _tax_office,
)
from docgen.registry import doc


def _bs(p: Profile, y: int) -> dict:
    """y년말 표준재무상태표 (정수 금액)."""
    r = _prng(p, "bs", y)
    rev = max(_revenue(p, y), 10_000_000)
    assets = int(rev * r.uniform(0.35, 1.1)) // 1000 * 1000 + r.randint(0, 999)
    cur = int(assets * r.uniform(0.35, 0.65))
    cogs_ratio = _pl(p, y)["cogs"] / rev
    inventory = int(cur * r.uniform(0.1, 0.45) * min(1.0, cogs_ratio * 1.4))
    quick = cur - inventory
    noncur = assets - cur
    invest = int(noncur * r.uniform(0.0, 0.12))
    intangible = int(noncur * r.uniform(0.0, 0.05))
    other_nc = int(noncur * r.uniform(0.15, 0.4))  # 임차보증금 등
    tangible = noncur - invest - intangible - other_nc
    liab = int(assets * r.uniform(0.3, 0.8))
    cur_liab = int(liab * r.uniform(0.3, 0.7))
    return {"current": cur, "quick": quick, "inventory": inventory, "noncurrent": noncur,
            "investment": invest, "tangible": tangible, "intangible": intangible, "other_noncurrent": other_nc,
            "assets": assets, "current_liab": cur_liab, "noncurrent_liab": liab - cur_liab, "liabilities": liab,
            "capital": assets - liab, "equity": assets - liab, "liab_equity": assets}


def _fs_detail(p: Profile, y: int, pl: dict, bs: dict) -> tuple[dict, dict]:
    """표준재무상태표·표준손익계산서 세부 계정 (heavy). 합계는 요약 계정과 같다.
    감가상각누계액은 자산 바로 아래에 음수로 둔다."""
    r = _prng(p, "fsdetail", y)
    sec = {}
    sec["quick"] = _split(r, bs["quick"], ["현금및현금성자산", "단기금융상품", "매출채권", "미수금", "선급금", "선급비용", "부가세대급금"],
                          must=("현금및현금성자산", "매출채권"))
    # 매출채권 아래 대손충당금
    for i, a in enumerate(sec["quick"]):
        if a["account"] == "매출채권" and a["amount"] > 1_000_000 and r.random() < 0.6:
            allow = int(a["amount"] * r.uniform(0.01, 0.03)) // 10 * 10
            a["amount"] += allow
            sec["quick"].insert(i + 1, {"account": "대손충당금", "amount": -allow})
            break
    item = p.business.biz_item
    inv_names = ["제품", "원재료", "재공품"] if item in ("제과",) else ["상품", "저장품"]
    sec["inventory"] = _split(r, bs["inventory"], inv_names, must=(inv_names[0],))
    sec["investment"] = _split(r, bs["investment"], ["장기금융상품", "장기대여금", "보험예치금"], must=("장기금융상품",))
    tang = []
    for a in _split(r, bs["tangible"], ["차량운반구", "비품", "시설장치", "기계장치", "건물"], keep=0.6, must=("비품", "시설장치")):
        acc = int(a["amount"] * r.uniform(0.25, 1.2)) // 10 * 10
        tang += [{"account": a["account"], "amount": a["amount"] + acc}, {"account": "감가상각누계액", "amount": -acc}]
    sec["tangible"] = tang
    sec["intangible"] = _split(r, bs["intangible"], ["영업권", "소프트웨어", "상표권"], keep=0.5)
    sec["other_noncurrent"] = _split(r, bs["other_noncurrent"], ["임차보증금", "기타보증금"], must=("임차보증금",))
    sec["current_liab"] = _split(r, bs["current_liab"], ["매입채무", "미지급금", "예수금", "부가세예수금", "미지급비용", "선수금", "단기차입금"],
                                 must=("매입채무", "미지급금", "예수금"))
    sec["noncurrent_liab"] = _split(r, bs["noncurrent_liab"], ["장기차입금", "퇴직급여충당부채", "장기미지급금"], keep=0.5, must=("장기차입금",))
    bs_acc = {k: v for k, v in sec.items() if v}

    pls = {}
    rev_names = {"한식": ["음식매출", "배달매출"], "커피전문점": ["음료매출", "상품매출"], "제과": ["제품매출", "상품매출"],
                 "미용": ["용역매출", "상품매출"], "학원": ["수강료수입", "교재매출"], "세무대리": ["용역매출", "기장수수료수입"],
                 "인테리어": ["공사수입", "상품매출"]}.get(item, ["상품매출", "기타매출"])
    pls["revenue"] = _split(r, pl["revenue"], rev_names, keep=0.6, must=(rev_names[0],))
    begin = _bs(p, y - 1)["inventory"] if y - 1 >= p.business.established.year else 0
    end = bs["inventory"]
    begin = min(begin, pl["cogs"] + end)
    pls["cogs"] = [{"account": "기초재고액", "amount": begin},
                   {"account": "당기매입액", "amount": pl["cogs"] - begin + end},
                   {"account": "기말재고액", "amount": end}]
    pls["sga"] = _split(r, pl["other_sga"], ["퇴직급여", "여비교통비", "기업업무추진비" if y >= 2024 else "접대비", "통신비", "수도광열비",
                                             "세금과공과", "수선비", "보험료", "차량유지비", "운반비", "교육훈련비", "도서인쇄비",
                                             "소모품비", "지급수수료", "광고선전비", "대손상각비", "잡비"],
                        keep=0.65, must=("통신비", "세금과공과", "지급수수료", "소모품비"))
    pls["non_op_income"] = _split(r, pl["non_op_income"], ["이자수익", "잡이익"], must=("이자수익",))
    pls["non_op_expense"] = _split(r, pl["non_op_expense"], ["이자비용", "잡손실"], must=("이자비용",))
    w = lambda n: _signed(n)  # noqa: E731
    fmt = lambda d: {k: [{"account": a["account"], "amount": w(a["amount"])} for a in v] for k, v in d.items() if v}  # noqa: E731
    return fmt(bs_acc), fmt(pls)


@doc("standard_financial_statement_proof", "표준재무제표증명", "business")
def standard_financial_statement_proof(p: Profile, rng: random.Random) -> dict:
    """홈택스 발급 표준재무제표증명(개인): 표준재무상태표 + 표준손익계산서.

    heavy: 세부 계정과목까지 표시 (재무상태표 30~40줄, 손익계산서 25~35줄, 2~3쪽).
    신고구분·신고일은 종합소득세 신고(_itr_filing)와 같다 (기한후신고·수정신고면 그 날짜).
    """
    b = p.business
    y = _filed_year(p)
    if y < b.established.year:
        y = b.established.year
    pl, bs = _pl(p, y), _bs(p, y)
    start = max(date(y, 1, 1), b.established)
    w = lambda n: won(n, "")  # noqa: E731
    fmt = rng.choice(["dash", "dot"])
    filing = _itr_filing(p, y)
    kind, filed = filing["kind"], filing["filed"]
    if kind == "경정청구":  # 경정청구는 재무제표를 다시 내지 않는다
        kind, filed = "정기신고", filing["original"]
    out = {
        "issue_no": _hometax_no(rng),
        "taxpayer_type": "개인",
        "taxpayer": {
            "trade_name": b.name,
            "biz_no": b.biz_no,
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn),
            "biz_type": b.biz_type,
            "biz_item": b.biz_item,
            "address": b.address.road_full,
        },
        "period": f"{D(start, fmt)} ~ {D(date(y, 12, 31), fmt)}",
        "attachments": "표준재무상태표, 표준손익계산서",
        "filing_kind": kind,
        "filed_date": D(filed, fmt),
        "balance_sheet": {k: w(v) for k, v in bs.items()},
        "income_statement": {k: w(v) for k, v in pl.items()},
        "issue_date": D(p.issue_date, "kor"),
        "issuer": _tax_office(b.address),
    }
    if heavy(rng, 0.3):
        out["bs_accounts"], out["pl_accounts"] = _fs_detail(p, y, pl, bs)
        del out["income_statement"]["other_sga"]  # 세부 계정으로 나눠 표시
    return out
