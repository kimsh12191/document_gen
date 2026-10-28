"""basic_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/family.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.family import _detail, _fam_common, _life, _member, _ymd  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("basic_certificate", "기본증명서", "family")
def basic_certificate(p: Profile, rng: random.Random) -> dict:
    """기본증명서 (일반/상세). 상세에는 개명·국적취득·성별정정 기록이 나온다."""
    L = _life(p)
    per = p.person
    detail = _detail(rng)
    me = _member(p, per, "person", "본인", masked=rng.random() < 0.5)
    nat = L["natur"]
    if nat:
        birth = {"place": nat["birthplace"]}
    else:
        sido, sigungu, _z, dongs, _r = rng.choice(K.REGIONS) if rng.random() < 0.5 else \
            next(x for x in K.REGIONS if x[0] == p.address_history[0][1].sido)
        place = " ".join(x for x in (sido, sigungu) if x)
        if rng.random() < 0.4:
            place += f" {rng.choice(dongs)}"
        late = special(rng, "late_birth_report", 0.05)  # 출생신고가 늦은 경우 (과태료 대상)
        reported = per.birth + timedelta(days=rng.randint(40, 700) if late else rng.randint(3, 30))
        birth = {"place": place, "reported": _ymd(reported), "reporter": rng.choice(["부", "부", "모"])}
    out = {"cert_type": "상세" if detail else "일반", "self": me, "birth": birth}
    if detail and nat:
        out["naturalization"] = {"acquired": _ymd(nat["date"]), "reason": "귀화허가", "prev_nationality": nat["prev"],
                                 "notified": _ymd(nat["notified"]), "notifier": "법무부장관"}
    if detail and L["rename"]:
        ren = L["rename"]
        out["name_change"] = {"permitted": _ymd(ren["permitted"]), "court": ren["court"], "old_name": ren["old"],
                              "reported": _ymd(ren["reported"])}
    if detail and L["gender_fix"]:
        gf = L["gender_fix"]
        new, old = per.gender_ko, "여" if per.gender == "M" else "남"
        out["correction"] = {"permitted": _ymd(gf["permitted"]), "court": gf["court"],
                             "content": f"성별 {old} → {new}", "reported": _ymd(gf["reported"])}
    out.update(_fam_common(rng, p))
    return out
