"""family_relation_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/family.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.family import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _P,
    _bon,
    _bon_of,
    _detail,
    _fam_common,
    _life,
    _member,
)
from docgen.registry import doc


def _foreign_parents(p: Profile, L: dict):
    """귀화자(중국 동포)의 부모는 중국 국적 외국인으로 기록된다."""
    if not L["natur"]:
        return p.father, p.mother
    f = _P(p.father.name, p.father.hanja, p.father.birth, None, "M", "중국")
    m = _P(p.mother.name, p.mother.hanja, p.mother.birth, None, "F", "중국")
    return f, m


@doc("family_relation_certificate", "가족관계증명서", "family")
def family_relation_certificate(p: Profile, rng: random.Random) -> dict:
    """가족관계증명서 (일반/상세). 사망한 부모, 전혼 자녀, 입양(친생부모) 등."""
    L = _life(p)
    detail = _detail(rng)
    full = rng.random() < 0.3  # 주민등록번호 뒷자리 모두 표시 신청
    me = _member(p, p.person, "person", "본인", masked=not full and rng.random() < 0.5)
    dead = L["dead"]
    fa, mo = _foreign_parents(p, L)
    adopted = L["adopted"] if detail else None
    fam = [_member(p, fa, "father", "양부" if adopted else "부", not full, status="사망" if "father" in dead else None),
           _member(p, mo, "mother", "양모" if adopted else "모", not full, status="사망" if "mother" in dead else None)]
    if adopted:
        bon = _bon_of(p, "person")
        fam.append(_member(p, adopted["father"], "bio", "친생부", not full, bon=bon))
        fam.append(_member(p, adopted["mother"], "bio", "친생모", not full,
                           bon=_bon(p, adopted["mother"], "biomother")))
    if p.spouse is not None:
        fam.append(_member(p, p.spouse, "spouse", "배우자", not full))
    kids = [(c, _bon_of(p, "child"), None) for c in p.children]
    if detail:
        ex = L["ex"]
        for c in L["ex_children"]:
            father_is_me = p.person.gender == "M"
            kb = _bon_of(p, "person") if father_is_me or (ex and ex["person"].nationality != "대한민국") \
                else _bon(p, ex["person"], "exhusband")
            kids.append((c, kb, None))
        if L["dead_child"]:
            kids.append((L["dead_child"][0], _bon_of(p, "child"), "사망"))
    for c, kb, st in sorted(kids, key=lambda x: x[0].birth):
        fam.append(_member(p, c, "child", "자녀", not full, bon=kb, status=st))
    out = {"cert_type": "상세" if detail else "일반", "self": me, "family": fam}
    out.update(_fam_common(rng, p))
    return out
