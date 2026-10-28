"""signature_confirmation: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/identity.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.identity import _corp_party, _local_issuer, _rand_person_text  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


_SIG_RE_USAGES = ["소유권 이전(매매, 증여 등)", "제한물권 설정(근저당권 설정, 전세권 설정 등)", "그 밖의 용도(가등기 설정, 가등기 말소 등)"]


@doc("signature_confirmation", "본인서명사실확인서", "identity", sample_mark=True)
def signature_confirmation(p: Profile, rng: random.Random) -> dict:
    """본인서명사실확인서 (본인서명사실 확인 등에 관한 법률 시행령 별지 제2호서식)."""
    per = p.person
    a = per.address
    out = {
        "doc_no": issue_no(rng, 16),
        "signer": {"name": per.name, "rrn": per.rrn, "address": a.road_full},
    }
    r = rng.random()
    if r < 0.5:  # 부동산 관련 용도
        usage = rng.choices(_SIG_RE_USAGES, [35, 55, 10])[0]
        out["real_estate_usage"] = usage
        if usage.startswith("소유권"):
            if special(rng, "corp_counterparty", 0.15):  # 법인에 매도
                name, rrn, addr = _corp_party(rng)
            else:
                name, rrn, addr = _rand_person_text(rng)
            out["counterparty"] = {"name": name, "rrn": rrn, "address": addr}
        elif usage.startswith("제한물권"):  # 근저당권자 = 대출 은행(법인)
            out["counterparty"] = {
                "name": f"주식회사 {p.bank}",
                "rrn": K.corp_reg_no(rng),
                "address": f"서울특별시 중구 {rng.choice(['을지로', '세종대로', '남대문로', '소공로'])} {rng.randint(10, 120)}",
            }
    else:  # 그 외의 용도 (제출기관이 요청하는 내용)
        out["other_usage"] = rng.choice([
            f"대출보증용({p.bank} {p.bank_branch} 제출)", f"금융기관 대출 약정용({p.bank} 제출)",
            "대출보증용", "법인등기용", "보증 계약용", f"여신거래 약정용({p.bank} {p.bank_branch})",
        ])
    if special(rng, "delegate", 0.12):  # 위임받은 사람(대리 제출)
        name, _rrn, addr = _rand_person_text(rng)
        out["delegate"] = {"name": name, "address": addr}
    out["signature"] = per.name
    out["issue_date"] = D(p.issue_date, rng.choice(["kor", "kor_short"]))
    out["issuer"] = _local_issuer(rng, a)
    return out
