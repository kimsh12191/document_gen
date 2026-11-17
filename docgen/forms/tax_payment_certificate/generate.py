"""tax_payment_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/tax.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.business import _tax_office  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.docs.tax import _national_cert  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


# ---------------------------------------------------------------------------
# 국세 납세증명서 (개인 / 법인)
# ---------------------------------------------------------------------------
@doc("tax_payment_certificate", "납세증명서(국세완납증명)", "tax")
def tax_payment_certificate(p: Profile, rng: random.Random) -> dict:
    """홈택스 발급 국세 납세증명서 (개인사업자).

    special short_validity: 유효기간 단축 + 사유, tax_deferral: 연장ㆍ유예 명세, emigration: 해외이주용.
    """
    b = p.business
    out = {
        "taxpayer": {
            "trade_name": b.name,
            "biz_no": b.biz_no,
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.85 else p.person.rrn,
            "address": p.person.address.road_full,
        },
        **_national_cert(p, rng, False),
        "issuer": _tax_office(p.person.address),
    }
    return out
