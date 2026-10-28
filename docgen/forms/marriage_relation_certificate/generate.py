"""marriage_relation_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/family.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.family import _detail, _fam_common, _life, _member, _rrn, _ymd  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


def _spouse_name(per) -> str:
    orig = getattr(per, "original", None)
    return f"{per.name}({orig})" if orig else per.name


@doc("marriage_relation_certificate", "혼인관계증명서", "family")
def marriage_relation_certificate(p: Profile, rng: random.Random) -> dict:
    """혼인관계증명서 (일반/상세). 일반은 현재 혼인만, 상세는 이혼한 혼인(외국인 배우자 포함)까지 표시."""
    L = _life(p)
    detail = _detail(rng)
    full = rng.random() < 0.3
    out = {"cert_type": "상세" if detail else "일반",
           "self": _member(p, p.person, "person", "본인", masked=not full and rng.random() < 0.5)}
    ex = L["ex"]
    if detail and ex:
        e = ex["person"]
        wed = {"kind": "혼인", "reported": _ymd(ex["married"]), "spouse_name": _spouse_name(e)}
        if e.nationality != "대한민국":
            wed.update(spouse_birth=_ymd(e.birth), spouse_nationality=e.nationality)
        else:
            wed["spouse_rrn"] = _rrn(e, not full)
        wed["office"] = ex["office"]
        div = {"kind": "이혼"}
        if ex["kind"] == "재판":
            jd = ex["divorced"] - timedelta(days=rng.randint(10, 40))
            div.update(judgment_date=_ymd(jd), court=ex["court"])
        div.update(reported=_ymd(ex["divorced"]), spouse_name=_spouse_name(e))
        if e.nationality != "대한민국":
            div["spouse_nationality"] = e.nationality
        else:
            div["spouse_rrn"] = _rrn(e, not full)
        div["office"] = ex["div_office"]
        out["past_events"] = [wed, div]
    if p.spouse is not None:
        out["spouse"] = _member(p, p.spouse, "spouse", "배우자", not full)
        md = L["married"]
        office_addr = p.address_history[-1][1] if rng.random() < 0.5 else p.person.address
        out["marriage"] = {
            "reported": _ymd(md),
            "spouse_name": p.spouse.name,
            "spouse_rrn": _rrn(p.spouse, not full),
            "office": office_addr.region,
        }
    out.update(_fam_common(rng, p))
    return out
