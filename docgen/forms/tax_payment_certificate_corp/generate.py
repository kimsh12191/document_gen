"""tax_payment_certificate_corp: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/tax.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.business import _tax_office  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.docs.tax import _national_cert  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("tax_payment_certificate_corp", "납세증명서(법인)", "tax")
def tax_payment_certificate_corp(p: Profile, rng: random.Random) -> dict:
    """홈택스 발급 국세 납세증명서 (법인)."""
    c = p.corporation
    return {
        "taxpayer": {
            "corp_name": c.name,
            "biz_no": c.biz_no,
            "ceo": p.person.name,
            "corp_reg_no": c.corp_no,
            "address": c.address.road_full,
        },
        **_national_cert(p, rng, True),
        "issuer": _tax_office(c.address),
    }
