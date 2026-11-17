"""corporate_seal_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/corporate.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from __future__ import annotations

from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.corporate import _addr, _facts, _formal, _side_person  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("corporate_seal_certificate", "법인인감증명서", "corporate", sample_mark=True)
def corporate_seal_certificate(p: Profile, rng: random.Random) -> dict:
    """등기소 발급 법인 인감증명서."""
    c, fx = p.corporation, _facts(p)
    issued = p.issue_date - timedelta(days=rng.randint(0, 10))
    office = courthouse(c.address)
    d = {
        "issue_no": f"{rng.randint(1000, 9999)}-{rng.randint(1000, 9999)}-{rng.randint(1000, 9999)}-{rng.randint(1000, 9999)}",
        "reg_no": fx["reg_no"],
        "corp_reg_no": c.corp_no,
        "company_name": _formal(c.name),
        "head_office": _addr(c.address),
        "rep_title": "대표이사",
        "rep_name": p.person.name,
        "rep_rrn": K.mask_rrn(p.person.rrn, rng.choice([0, 1])),
        "issue_date": f"{issued.year}년 {issued.month:02d}월 {issued.day:02d}일",
        "issue_office": office,
        "registrar": _side_person(f"registrar:{office}:{issued.year}").name,
        "fee": rng.choice(["1,000원", "1,000원", "700원"]),
        "purpose": rng.choice(["금융기관 제출용", "은행 제출용", "여신거래용", "일반용"]),
    }
    if special(rng, "purpose_blank", 0.1):  # 용도란을 비워 둔 채 발급
        d["purpose"] = None
    if special(rng, "internet_issue", 0.2):  # 전자증명서로 인터넷 발급: 발급확인번호, 전산운영책임관
        d["issue_office"] = "법원행정처 등기정보중앙관리소"
        d.pop("registrar")
        d["fee"] = "500원"
        d["confirm_no"] = "-".join("".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789") for _ in range(4))
                                   for _ in range(3))
    return d
