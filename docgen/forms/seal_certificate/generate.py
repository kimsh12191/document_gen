"""seal_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/identity.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.identity import _corp_party, _local_issuer, _rand_person_text  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("seal_certificate", "인감증명서", "identity", sample_mark=True)
def seal_certificate(p: Profile, rng: random.Random) -> dict:
    """인감증명서 (인감증명법 시행령 별지 제14호서식 / 전자발급 제14호의2서식). 일반용 / 부동산 매도용.
    대리 발급, 법인·공동 매수자, 미성년 자녀(법정대리인 동의) 발급 등."""
    subj, legal = p.person, None
    teens = [c for c in p.children if 17 <= (p.issue_date - c.birth).days // 365 < 19]
    if teens and special(rng, "minor_consent", 0.3):  # 17~18세 자녀의 인감증명: 법정대리인(부모) 동의
        subj, legal = teens[0], p.person
    a = p.person.address
    online = legal is None and rng.random() < 0.25  # 2024.9.30.~ 정부24 전자발급(일반용만)
    sale = not online and legal is None and special(rng, "real_estate_sale", 0.3)
    kind = "부동산 매도용" if sale else "일반용"
    agent = not online and special(rng, "agent", 0.15)  # 위임장을 받은 대리인이 발급
    out = {
        "doc_no": issue_no(rng, 16) if online else issue_no(rng, 12),
        "applicant_type": "대리인" if agent else "본인",
        "person": {
            "name": subj.name,
            "name_hanja": subj.hanja,
            "rrn": subj.rrn,
            "nationality": subj.nationality,
            "address": a.road_full,
        },
        "seal_name": subj.name + "인",
        "usage_type": kind,
    }
    if agent:
        name, rrn, _ = _rand_person_text(rng)
        out["agent"] = {"name": name, "rrn": K.mask_rrn(rrn)}
    if sale:
        if special(rng, "corp_buyer", 0.2):  # 매수자가 법인
            name, rrn, addr = _corp_party(rng)
        else:
            name, rrn, addr = _rand_person_text(rng)
            if special(rng, "joint_buyers", 0.12):  # 공동 매수(부부 공동명의 등): 매수자 모두 기재
                n2, r2, _a2 = _rand_person_text(rng)
                name, rrn = f"{name}, {n2}", f"{rrn}, {r2}"
        out["buyer"] = {"name": name, "rrn": rrn, "address": addr}
        out["applicant_signature"] = subj.name if not agent else out["agent"]["name"]
    if legal is not None:
        rel = "부" if legal.gender == "M" else "모"
        out["remark"] = f"법정대리인({rel}) {legal.name} 동의"
    out["issue_date"] = D(p.issue_date, rng.choice(["kor", "kor_short"]))
    out["issuer"] = _local_issuer(rng, a)
    return out
