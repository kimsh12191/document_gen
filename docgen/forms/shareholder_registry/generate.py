"""shareholder_registry: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/corporate.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from __future__ import annotations

from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.corporate import PAR_VALUE, _facts  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.entities import World
from docgen.registry import doc


def _mask_any(rrn: str, rng: random.Random) -> str:
    return K.mask_rrn(rrn, rng.choice([0, 1, 1]))


@doc("shareholder_registry", "주주명부", "corporate")
def shareholder_registry(p: Profile, rng: random.Random) -> dict:
    """법인 주주명부 (대표이사 확인 날인).

    주주 구성은 프로필 단위(_cap_table): heavy 면 주주 20~40명(여러 쪽), 자기주식(회사 명의, 비고 '자기주식'),
    투자사 법인주주(상환전환우선주) 특수 상황."""
    c, fx = p.corporation, _facts(p)
    holders = fx["holders"]
    total = sum(h["shares"] for h in holders)
    # 지분율: 최대잔여법으로 합계 100 유지 (소수점 1자리 또는 2자리)
    dec = rng.choice([1, 2, 2])
    unit = 100 * 10 ** dec
    raw = [h["shares"] * unit / total for h in holders]
    bp = [int(x) for x in raw]
    for i in sorted(range(len(raw)), key=lambda i: raw[i] - bp[i], reverse=True)[:unit - sum(bp)]:
        bp[i] += 1
    pct = (lambda b: f"{b / 10 ** dec:.{dec}f}%")
    directors = {d.name for d in p.directors}
    rows = []
    for i, (h, b) in enumerate(zip(holders, bp), 1):
        sh, n = h["holder"], h["shares"]
        if h["kind"] == "treasury":
            name, idno, addr, note = c.name, c.biz_no, c.address.road_short, "자기주식"
        elif isinstance(sh, str):  # 법인주주: 사업자등록번호
            w = World(0)
            w.rng = random.Random(f"investor:{sh}")
            name, idno, addr, note = sh, K.biz_no(random.Random(sh), corporate=True), w.address("office").road_short, "법인주주"
        else:
            name, idno, addr = sh.name, _mask_any(sh.rrn, rng), sh.address.road_short
            note = "대표이사" if sh is p.person else ("사내이사" if sh.name in directors else "")
        rows.append({"no": str(i), "name": name, "id_no": idno, "address": addr, "share_type": h["type"],
                     "shares": f"{n:,}", "amount": f"{n * PAR_VALUE:,}", "ratio": pct(b), "acquired": D(h["acquired"], "dot"),
                     "note": note or None})
    base = p.issue_date - timedelta(days=rng.randint(0, 20))
    return {
        "base_date": D(base, rng.choice(["kor", "dot"])),
        "company_name": c.name,
        "corp_reg_no": c.corp_no,
        "biz_no": c.biz_no,
        "head_office": c.address.road_short,
        "total_shares": f"{total:,}주",
        "par_value": won(PAR_VALUE),
        "capital": won(c.capital),
        "shareholders": rows,
        "sum_shares": f"{total:,}",
        "sum_amount": f"{total * PAR_VALUE:,}",
        "sum_ratio": pct(unit),
        "certify_date": D(p.issue_date, rng.choice(["kor", "kor_short"])),
        "ceo_name": p.person.name,
    }
