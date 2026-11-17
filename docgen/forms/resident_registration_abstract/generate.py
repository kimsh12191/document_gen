"""resident_registration_abstract: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/family.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.family import _P, _addr_text, _life, _resident_issuer, _rrn, _yrs  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("resident_registration_abstract", "주민등록표 초본", "family")
def resident_registration_abstract(p: Profile, rng: random.Random) -> dict:
    """주민등록표 초본 (개인 인적사항 + 주소 변동 이력). 이사가 잦은 사람은 여러 쪽이 된다."""
    L = _life(p)
    per = p.person
    masked = rng.random() < 0.4
    dfmt = "dash" if rng.random() < 0.85 else "dot"
    src = L["rows"]
    scope = "전체 포함"
    if len(src) <= 6 and rng.random() < 0.3:
        scope = "최근 5년"
        cut = _yrs(p.issue_date, -5)
        keep = [x for x in src if x["date"] >= cut]
        src = keep or src[-1:]
    rows = []
    for i, x in enumerate(src):
        changed = x["date"] + timedelta(days=rng.choice([0, 0, rng.randint(1, 13)]))  # 변동일=신고일(14일 이내)
        rows.append({
            "no": str(i + 1),
            "address": _addr_text(x, rng),
            "moved_in": D(x["date"], dfmt),
            "changed": D(min(changed, p.issue_date - timedelta(days=1)), dfmt),
            "reason": x["reason"],
            "head_relation": x["rel"],
            "status": x["status"],
        })
    out = {
        "person": {"name": per.name, "name_hanja": per.hanja, "rrn": _rrn(per, masked)},
    }
    # 개인 인적사항 변경 내용 (개명, 성별정정에 따른 주민등록번호 정정)
    changes = []
    ren, gf = L["rename"], L["gender_fix"]
    if ren:
        old = f"{ren['old']}({ren['old_hanja']})" if ren["old_hanja"] else ren["old"]
        new = f"{per.name}({per.hanja})" if per.hanja else per.name
        changes.append((ren["reported"], f"성명 {old} → {new}", "개명"))
    if gf:
        changes.append((gf["reported"], f"주민등록번호 {_rrn(_P('', None, per.birth, gf['old_rrn'], 'M'), masked)} → "
                                         f"{_rrn(per, masked)}", "주민등록번호정정(성별정정)"))
    if changes:
        out["person_changes"] = [{"no": str(i + 1), "content": c, "changed": D(d, dfmt), "reason": rs}
                                 for i, (d, c, rs) in enumerate(sorted(changes))]
    out["history_scope"] = scope
    out["addresses"] = rows
    out.update(_resident_issuer(rng, p))
    return out
