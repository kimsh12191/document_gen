"""shareholders_meeting_minutes: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/corporate.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from __future__ import annotations

from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.corporate import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _Doc,
    _PURPOSES,
    _facts,
    _hm,
    _meeting_time,
    _notary,
    _side_person,
    _venue,
    _weekday,
)
from docgen.registry import doc


_HOLDER_PROXY = ["배우자", "직원", "가족", "법무사 사무원", "대리인"]


def _gm_agenda(kind: str, p: Profile, fx: dict, rng: random.Random, mdate: date, fy: int) -> dict:
    c = p.corporation
    if kind == "director":
        d = p.directors[0]
        return {"title": "이사 선임의 건", "special": False,
                "body": f"의장은 사내이사 {d.name}의 임기가 만료됨에 따라 이사를 선임할 필요가 있음을 설명하고 "
                        f"동인을 사내이사로 중임할 것을 물은바, {{votes}}이를 승인 가결하다. 피선임자는 즉석에서 그 취임을 승낙하다.",
                "detail": f"사내이사  {d.name} ({D(d.birth, 'kor_short')}생)  중임"}
    if kind == "new_director":
        nd = _side_person(f"newdir:{p.seed}:{mdate}")
        return {"title": "신규 이사 선임의 건", "special": False,
                "body": "의장은 경영체제 강화를 위하여 이사 1명을 추가로 선임할 필요가 있음을 설명하고 아래 사람을 사내이사로 선임할 것을 "
                        "물은바, {votes}이를 승인 가결하다. 피선임자는 즉석에서 그 취임을 승낙하다.",
                "detail": f"사내이사  {nd.name} ({D(nd.birth, 'kor_short')}생)  신규 선임"}
    if kind == "auditor":
        a = fx["auditor"]
        return {"title": "감사 선임의 건", "special": False,
                "body": f"의장은 감사 {a.name}의 임기 만료로 감사를 선임하여야 함을 설명하고 그 선임을 물은바, "
                        f"{{votes}}아래 사람을 감사로 선임하다. 피선임자는 즉석에서 취임을 승낙하다.",
                "detail": f"감사  {a.name} ({D(a.birth, 'kor_short')}생)  중임"}
    if kind == "articles":
        pool = _PURPOSES.get(c.biz_item, [])
        new = rng.choice([x for x in ["전자상거래업", "부동산 임대업", "소프트웨어 개발 및 공급업", "수출입업", "교육 서비스업",
                                      "신재생에너지 발전업"] if x not in fx["purposes"] and x not in pool] or ["신규사업"])
        n = len(fx["purposes"])
        return {"title": "정관 일부 변경의 건", "special": True,
                "body": "의장은 사업 다각화를 위하여 정관 제2조(목적)에 사업목적을 추가할 필요가 있음을 설명하고 "
                        "아래와 같이 정관을 변경할 것을 물은바, {votes}원안대로 승인 가결하다.",
                "detail": f"제2조(목적) 제{n}호 신설: \"{n}. {new}\" (종전 제{n}호는 제{n + 1}호로 이동)"}
    if kind == "authorized":
        new = fx["authorized"] * rng.choice([2, 4, 5])
        return {"title": "정관 일부 변경의 건 (발행예정주식총수)", "special": True,
                "body": "의장은 향후 자금 조달에 대비하여 정관 제5조의 발행예정주식총수를 늘릴 필요가 있음을 설명하고 그 가부를 물은바, "
                        "{votes}원안대로 승인 가결하다.",
                "detail": f"제5조 발행예정주식의 총수 : {fx['authorized']:,}주 → {new:,}주"}
    if kind == "pay":
        limit = K.round_to(min(2e9, max(1e8, c.revenue * rng.uniform(0.005, 0.02))), 50_000_000)
        return {"title": "이사 보수한도 승인의 건", "special": False,
                "body": "의장은 당해 사업연도 이사 보수한도액을 아래와 같이 정하고자 함을 설명하고 그 승인을 물은바, "
                        "{votes}원안대로 승인 가결하다.",
                "detail": f"이사 보수한도액: 금 {K.won_korean(limit)}원 (₩{limit:,})"}
    if kind == "auditor_pay":
        limit = K.round_to(min(3e8, max(2e7, c.revenue * rng.uniform(0.0005, 0.002))), 10_000_000)
        return {"title": "감사 보수한도 승인의 건", "special": False,
                "body": "의장은 당해 사업연도 감사 보수한도액을 아래와 같이 정하고자 함을 설명하고 그 승인을 물은바, {votes}원안대로 승인 가결하다.",
                "detail": f"감사 보수한도액: 금 {K.won_korean(limit)}원 (₩{limit:,})"}
    if kind == "fs":
        return {"title": f"제{max(1, fy - c.established.year + 1)}기({fy}년도) 재무제표 승인의 건", "special": False,
                "body": "의장은 제출된 재무상태표, 손익계산서 및 이익잉여금처분계산서(안)의 내용을 설명하고 그 승인을 물은바, "
                        "{votes}원안대로 승인 가결하다.", "detail": None}
    if kind == "dividend":
        per = rng.choice([50, 100, 150, 200, 250, 300, 500])
        return {"title": "이익배당의 건", "special": False,
                "body": "의장은 아래와 같이 현금배당을 실시할 것을 제안하고 그 가부를 물은바, {votes}원안대로 승인 가결하다.",
                "detail": f"배당의 종류 : 현금배당 / 1주당 배당금 : 보통주 {per:,}원 / 배당기준일 : {fy}.12.31"}
    return {"title": "임원 퇴직금 지급규정 개정의 건", "special": False,
            "body": "의장은 임원 퇴직금 지급규정의 개정 필요성과 개정안의 주요 내용을 설명하고 그 승인을 물은바, {votes}원안대로 승인 가결하다.",
            "detail": "대표이사 지급률 : 퇴직 전 3년 평균 연봉의 1/10 × 근속연수 × 3배수 → 2배수"}


@doc("shareholders_meeting_minutes", "임시주주총회의사록", "corporate")
def shareholders_meeting_minutes(p: Profile, rng: random.Random) -> dict:
    """임시(또는 정기)주주총회의사록 (이사 선임 / 정관 변경 등).

    주주 구성은 _facts 와 같다(자기주식은 의결권 없음). heavy: 안건 4~7개 + 출석주주 명단(주주가 많으면 여러 쪽).
    special: annual 정기주주총회(재무제표 승인·배당), dissent 반대 주식수 기재, proxy 위임장에 의한 대리출석,
    notarized 공증인 인증, seal_missing 일부 이사 날인 누락."""
    c, fx = p.corporation, _facts(p)
    annual = special(rng, "annual", 0.3)
    fy = p.issue_date.year - 1 if p.issue_date.month >= 4 else p.issue_date.year - 2
    if annual:
        mdate = _weekday(date(fy + 1, 3, rng.randint(15, 31)))
    else:
        mdate = _weekday(p.issue_date - timedelta(days=rng.randint(3, 40)))
    h, m, dur = _meeting_time(rng)
    voters = [hd for hd in fx["holders"] if hd["kind"] != "treasury"]
    treasury = sum(hd["shares"] for hd in fx["holders"] if hd["kind"] == "treasury")
    total = sum(hd["shares"] for hd in voters)
    many = heavy(rng, 0.25)
    if len(voters) > 6:  # 주주가 많으면 소액주주 일부 불참
        present = [hd for i, hd in enumerate(voters) if i < 3 or hd["kind"] == "investor" or rng.random() < 0.7]
    else:
        absent = 1 if rng.random() < 0.3 else 0
        present = voters[:len(voters) - absent]
    pshares = sum(hd["shares"] for hd in present)
    if annual:
        kinds = ["fs"] + rng.sample(["director", "auditor", "pay", "auditor_pay", "dividend"], rng.randint(3, 4) if many else rng.randint(1, 2))
    else:
        pool = ["director", "articles", "auditor", "pay", "new_director", "authorized", "rule", "auditor_pay"]
        kinds = rng.sample(pool, rng.randint(4, 7)) if many else rng.sample(pool[:4], rng.choice([1, 2, 2]))
    agendas = [_gm_agenda(k, p, fx, rng, mdate, fy) for k in kinds]
    dissent = special(rng, "dissent", 0.12) and len(present) >= 3
    vi = next((i for i, a in enumerate(agendas) if a["special"]), rng.randrange(len(agendas))) if dissent else -1
    opp = None
    if dissent:
        cands = [hd for hd in present[1:] if hd["shares"] * 3 < pshares]
        opp = rng.choice(cands) if cands else None
    for i, a in enumerate(agendas):
        if i == vi and opp:
            against = opp["shares"]
            name = opp["holder"] if isinstance(opp["holder"], str) else opp["holder"].name
            rule = "출석주주 의결권의 3분의 2 이상" if a["special"] else "출석주주 의결권의 과반수"
            a["votes"] = f"찬성 {pshares - against:,}주, 반대 {against:,}주"
            a["body"] = a["body"].replace("{votes}", f"{rule}인 {pshares - against:,}주의 찬성으로 ") + \
                f" (주주 {name} 반대)"
        else:
            a["body"] = a["body"].replace("{votes}", rng.choice(["출석주주 전원의 찬성으로 ", "출석주주 전원의 찬성으로 ", "출석주주 전원이 이의 없이 찬성하여 "]))
        a.pop("special")
        if a.get("detail") is None:
            a.pop("detail", None)
        a["no"] = f"제{i + 1}호 의안"
    end_m = h * 60 + m + dur + 6 * len(kinds)
    signers = [{"title": "의장 대표이사", "name": p.person.name}] + \
        [{"title": "사내이사", "name": d.name} for d in p.directors[:rng.randint(1, len(p.directors))]]
    d = {
        "meeting_title": "정기주주총회의사록" if annual else "임시주주총회의사록",
        "company_name": c.name,
        "datetime": f"{D(mdate, 'kor_short')} {_hm(h, m)}",
        "venue": _venue(p, rng),
        "shareholders_total": f"{len(voters)}명",
        "issued_shares": f"{total:,}주",
        "shareholders_present": f"{len(present)}명",
        "shares_present": f"{pshares:,}주",
        "present_ratio": f"{pshares * 100 / total:.2f}%",
        "chair": p.person.name,
        "agendas": agendas,
        "end_time": _hm(end_m // 60 % 24, end_m % 60),
        "minutes_date": D(mdate, "kor_short"),
        "head_office": c.address.road_short,
        "signers": signers,
    }
    if treasury:
        d["treasury_shares"] = f"{treasury:,}주"
    proxy = special(rng, "proxy", 0.2) and len(present) >= 2
    proxies = {}
    if proxy:
        cand = [i for i, hd in enumerate(present) if i > 0]
        for i in rng.sample(cand, min(len(cand), rng.randint(1, max(1, len(cand) // 4)))):
            hd = present[i]
            if isinstance(hd["holder"], str):
                proxies[i] = _side_person(f"proxy:{p.seed}:{i}").name + " (직원)"
            else:
                proxies[i] = _side_person(f"proxy:{p.seed}:{i}").name + f" ({rng.choice(_HOLDER_PROXY)})"
        d["proxy_count"] = f"위임장에 의한 대리출석 {len(proxies)}명 포함"
    if many or proxy:
        rows = []
        for i, hd in enumerate(present):
            sh = hd["holder"]
            rows.append({"name": sh if isinstance(sh, str) else sh.name, "shares": f"{hd['shares']:,}",
                         "method": "대리출석" if i in proxies else "본인출석", "proxy": proxies.get(i)})
        d["attendees"] = rows
    if special(rng, "notarized", 0.15):
        d["notary"] = _notary(p, rng, mdate)
    d = _Doc(d)
    d.seal_p = 0.5 if special(rng, "seal_missing", 0.12) else 0.95
    return d
