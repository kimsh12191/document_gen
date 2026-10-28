"""resident_registration_copy: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/family.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.family import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _addr_text,
    _life,
    _new_addr,
    _new_person,
    _resident_issuer,
    _rrn,
    _yrs,
)
from docgen.registry import doc


def _sib_rel(head, sib) -> str:
    """세대주와 형제자매의 관계 표기."""
    if sib.birth < head.birth:
        if sib.gender == "M":
            return "형" if head.gender == "M" else "오빠"
        return "누나" if head.gender == "M" else "언니"
    return "동생"


@doc("resident_registration_copy", "주민등록표 등본", "family")
def resident_registration_copy(p: Profile, rng: random.Random) -> dict:
    """주민등록표 등본 (세대 전체). 부모·형제 동거, 세대주 변경, 동거인, 과거 주소 변동 포함 발급 등."""
    L = _life(p)
    hh = L["household"]
    moved_in, home = p.address_history[-1]
    masked = rng.random() < 0.5
    dfmt = "dash" if rng.random() < 0.85 else "dot"  # 정부24·주민센터 발급본은 2015-03-02 표기
    child_style = rng.random() < 0.8
    members = []
    cut = p.issue_date - timedelta(days=3)

    def add(per, rel: str, d: date, reason: str):
        members.append({
            "no": str(len(members) + 1), "relation": rel, "name": per.name, "name_hanja": per.hanja,
            "rrn": _rrn(per, masked), "moved_in": D(min(d, cut), dfmt), "reason": reason,
        })
        if per.hanja is None:
            del members[-1]["name_hanja"]

    def kid_rel(c) -> str:
        return "자" if child_style else ("아들" if c.gender == "M" else "딸")

    formed_reason = rng.choice(["전입세대구성", "전입세대구성", "세대분리"])
    if hh["mode"] == "parents":
        F = hh["formed"]
        head = p.father if hh["head"] == "father" else p.mother
        add(head, "본인", F, "전입")
        if hh["head"] == "father" and "mother" not in L["dead"]:
            add(p.mother, "배우자", F, "전입")
        for s in [x for x in L["siblings"] if x.birth < F]:
            add(s, kid_rel(s), F, "전입")
        add(p.person, kid_rel(p.person), moved_in, L["current_reason"])
        for s in [x for x in L["siblings"] if x.birth >= F]:
            add(s, kid_rel(s), s.birth + timedelta(days=rng.randint(3, 25)), "출생등록")
        if hh.get("head_change"):
            formed = ("세대주변경", hh["head_change"])
        else:
            formed = (formed_reason, F)
        head_since = F
    else:
        head = p.spouse if hh["head"] == "spouse" else p.person
        if hh["head"] == "spouse" and hh.get("head_change"):
            add(p.spouse, "본인", hh["spouse_joined"], rng.choice(["전입", "세대합가"]))
            add(p.person, "배우자", moved_in, L["current_reason"])
            formed = ("세대주변경", hh["head_change"])
            head_since = hh["spouse_joined"]
        else:
            head_since = moved_in
            add(head, "본인", moved_in, L["current_reason"] if head is p.person else "전입")
            if p.spouse is not None:
                other = p.spouse if head is p.person else p.person
                md = L["married"]
                if md > moved_in:  # 혼인 후 세대주 주소로 전입
                    joined = min(md + timedelta(days=rng.randint(0, 40)), p.issue_date - timedelta(days=10))
                    add(other, "배우자", joined, rng.choice(["전입", "전입", "세대합가"]))
                else:
                    add(other, "배우자", moved_in, "전입")
            formed = (rng.choice(["전입세대구성", "전입세대구성", "세대분리"] + (["세대합가"] if p.spouse else [])), moved_in)
        for c in sorted(p.children, key=lambda x: x.birth):
            if c.birth > moved_in:
                add(c, kid_rel(c), c.birth + timedelta(days=rng.randint(3, 25)), "출생등록")
            else:
                add(c, kid_rel(c), moved_in, "전입")
        # 부모 동거 (세대원이 많은 세대)
        late = [moved_in + timedelta(days=30), p.issue_date - timedelta(days=40)]
        for w in hh["co_parents"]:
            d = rand_date(rng, *late) if late[1] > late[0] else moved_in
            if w == "spouse_mother":
                sm = _new_person(rng, "F", rand_date(rng, _yrs(p.spouse.birth, -34), _yrs(p.spouse.birth, -22)))
                add(sm, "모", d, rng.choice(["전입", "세대합가"]))
            else:
                add(getattr(p, w), "부" if w == "father" else "모", d, rng.choice(["전입", "세대합가"]))
        if hh["mode"] == "siblings":
            for s in L["siblings"][:2]:
                add(s, _sib_rel(p.person, s), rand_date(rng, moved_in, max(moved_in, p.issue_date - timedelta(days=40))),
                    "전입")
    # 동거인 (친족이 아닌 세대원)
    if special(rng, "cohabitant", 0.06):
        lo = max(head_since, moved_in) + timedelta(days=10)
        hi = p.issue_date - timedelta(days=15)
        g = rng.choice("MF")
        b = rand_date(rng, date(1960, 1, 1), date(2003, 12, 31))
        add(_new_person(rng, g, b), "동거인", rand_date(rng, lo, hi) if hi > lo else hi, "전입")

    # 과거의 주소 변동 사항 포함 발급(선택)
    past = []
    many = heavy(rng, 0.3)
    if many or rng.random() < 0.35:
        if head is p.person:
            src = [x for x in L["rows"] if x["kind"] in ("profile", "extra") and x["date"] < moved_in]
            src = [(x["date"], x, x["reason"]) for x in src]
        else:  # 세대주(배우자·부모)의 이전 주소
            n = rng.randint(6, 18) if many else rng.randint(1, 3)
            d = head_since - timedelta(days=rng.randint(200, 900))
            src = []
            for _ in range(n):
                if d < _yrs(head.birth, 18):
                    break
                src.append((d, {"addr": _new_addr(rng), "date": d}, "전입"))
                d -= timedelta(days=rng.randint(180, 1400))
            src.reverse()
        if not many:
            src = src[-rng.randint(1, 3):]
        for i, (d, row, reason) in enumerate(src):
            past.append({"no": str(i + 1), "address": _addr_text(row, rng), "moved_in": D(d, dfmt), "reason": reason})
    out = {
        "household_head": {"name": head.name, "name_hanja": head.hanja},
        "household_formed": {"reason": formed[0], "date": D(formed[1], dfmt)},
        "past_addresses": past,
        "current_address": {"address": home.road_full, "moved_in": D(moved_in if head is p.person else head_since, dfmt),
                            "reason": L["current_reason"] if head is p.person else "전입"},
        "members": members,
    }
    out.update(_resident_issuer(rng, p))
    return out
