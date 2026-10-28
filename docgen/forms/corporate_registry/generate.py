"""corporate_registry: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/corporate.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from __future__ import annotations

from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.corporate import PAR_VALUE, _Row, _addr, _facts  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


def _kd(d: date) -> str:
    """등기부식 날짜: '2023 년 03 월 15 일'"""
    return f"{d.year} 년 {d.month:02d} 월 {d.day:02d} 일"


@doc("corporate_registry", "법인 등기사항전부증명서(현재 유효사항)", "corporate")
def corporate_registry(p: Profile, rng: random.Random) -> dict:
    """인터넷등기소 발급 법인 등기사항전부증명서.

    기본은 '현재 유효사항'. heavy/special(full_history) 이면 '말소사항 포함'으로 상호·본점·자본금·목적·임원·지점의
    지난 기록을 모두 싣고 말소된 기록은 빨간 줄로 긋는다 (실제 등기부 방식). 임원 변경이 많으면 여러 쪽."""
    c, fx = p.corporation, _facts(p)
    issued_at = p.issue_date - timedelta(days=rng.randint(0, 10))
    hh, mm, ss = rng.randint(9, 18), rng.randint(0, 59), rng.randint(0, 59)
    full = heavy(rng, 0.3) or special(rng, "full_history", 0.2)
    pref = sum(h["shares"] for h in fx["holders"] if h["type"] != "보통주")

    def chg(dt: date | None, word: str) -> dict | None:
        if dt is None:
            return None
        return {"changed": f"{D(dt, 'dot')} {word}", "registered": f"{D(dt + timedelta(days=(dt.toordinal() % 9) + 2), 'dot')} 등기"}

    def cap_state(shares: int, dt: date | None) -> dict:
        p_ = pref if shares == fx["issued"] else 0
        st = {"issued_shares": f"{shares:,} 주", "common_shares": f"{shares - p_:,} 주",
              "capital": f"금 {shares * PAR_VALUE:,} 원"}
        if p_:
            st["preferred_shares"] = f"{p_:,} 주"
        if dt:
            st.update(chg(dt, "변경"))
        return st

    def officer(e: dict, history: bool) -> dict:
        it = {"position": e["role"], "name": e["person"].name, "rrn": K.mask_rrn(e["person"].rrn, 0),
              "appointed": _kd(e["start"]), "appointment_type": e["kind"], "registered": _kd(e["reg"])}
        if e["role"] == "대표이사":
            it["address"] = _addr(e["person"].address)
        if history and e["end"]:
            it.update(ended=_kd(e["end"]["date"]), end_type=e["end"]["kind"], end_registered=_kd(e["end"]["reg"]))
        it = _Row(it)
        it.struck = history and e["struck"]
        return it

    ents = sorted(fx["entries"], key=lambda e: (e["reg"], e["order"])) if full else fx["officers"]
    names, offices, caps, pvs = fx["names"], fx["offices"], fx["capital_hist"], fx["purpose_versions"]
    d = {
        "issue_scope": "말소사항 포함" if full else "현재 유효사항",
        "reg_no": fx["reg_no"],
        "corp_reg_no": c.corp_no,
        "company_name": names[-1][0],
        "company_name_change": chg(names[-1][1], "변경"),
        "head_office": _addr(c.address),
        "head_office_change": chg(offices[-1][1], "이전"),
        "notice_method": fx["notice"],
        "par_value": f"금 {PAR_VALUE:,} 원",
        "authorized_shares": f"{fx['authorized']:,} 주",
        **cap_state(fx["issued"], None),
        "capital_change": chg(caps[-1][1], "변경"),
        "purposes": [f"{i}. {x}" for i, x in enumerate(fx["purposes"], 1)],
        "purpose_change": chg(pvs[-1][1], "변경"),
        "officers": [officer(e, full) for e in ents],
        "established": _kd(c.established),
        "opening_reason": "설립",
        "opening_date": _kd(c.established),
        "jurisdiction": courthouse(c.address),
        "issue_no": "".join(str(rng.randint(0, 9)) for _ in range(rng.choice([16, 20]))),
    }
    if full:
        d["name_history"] = [{"name": nm, **(chg(dt, "변경") or {})} for nm, dt in names[:-1]]
        d["office_history"] = [{"address": _addr(a), **(chg(dt, "이전") or {})} for a, dt in offices[:-1]]
        d["capital_history"] = [cap_state(n, dt) for n, dt in caps[:-1]]
        d["purpose_history"] = [{"purposes": [f"{i}. {x}" for i, x in enumerate(items, 1)], **(chg(dt, "변경") or {})}
                                for items, dt in pvs[:-1]]
    brs = [b for b in fx["branches"] if full or not b["closed"]]
    if brs:
        d["branches"] = []
        for i, b in enumerate(brs, 1):
            it = {"no": str(i), "address": _addr(b["address"]), "opened": _kd(b["opened"]),
                  "opened_registered": _kd(b["opened"] + timedelta(days=b["opened"].toordinal() % 7 + 3))}
            it = _Row(it)
            if b["closed"]:
                it.struck = True
                it.update(closed=_kd(b["closed"]),
                          closed_registered=_kd(b["closed"] + timedelta(days=b["closed"].toordinal() % 7 + 2)))
            d["branches"].append(it)
    co = fx["co_ceo"]
    if co and co["joint"]:
        d["joint_representation"] = f"대표이사 {p.person.name}, 대표이사 {co['person'].name}는 공동으로 회사를 대표"
        d["joint_registered"] = _kd(co["start"] + timedelta(days=co["start"].toordinal() % 9 + 2))
    d = {k: v for k, v in d.items() if v is not None}
    if rng.random() < 0.4:
        d["issue_type"] = "열람용"
        d["viewed_at"] = f"{issued_at.year}년{issued_at.month:02d}월{issued_at.day:02d}일 {hh:02d}시{mm:02d}분{ss:02d}초"
    else:
        d["issue_type"] = rng.choice(["제출용", "발급용"])
        d["issue_date"] = f"서기 {issued_at.year}년 {issued_at.month:02d}월 {issued_at.day:02d}일"
        d["issue_date_short"] = D(issued_at, "slash")
        d["confirm_no"] = "-".join("".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789") for _ in range(4))
                                   for _ in range(3))
        d["fee"] = "1,000원"
    return d
