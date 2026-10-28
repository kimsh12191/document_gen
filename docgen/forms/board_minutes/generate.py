"""board_minutes: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/corporate.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from __future__ import annotations

from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.corporate import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _Doc,
    _facts,
    _hm,
    _meeting_time,
    _notary,
    _venue,
    _weekday,
)
from docgen.entities import World
from docgen.registry import doc


def _board_agenda(kind: str, p: Profile, fx: dict, rng: random.Random, mdate: date) -> dict:
    c = p.corporation
    bank = f"{p.bank} {p.bank_branch}"
    if kind == "auth":
        return {"title": "차입 관련 제반 권한 위임의 건",
                "body": "의장은 제1호 의안의 차입과 관련하여 여신거래약정서 등 제반 서류의 작성, 날인 및 제출 등 일체의 권한을 "
                        "대표이사에게 위임할 것을 제안하고 그 가부를 물은바, {votes}원안대로 승인 가결하다."}
    if kind == "branch":
        w = World(0)
        w.rng = random.Random(f"newbranch:{p.seed}:{mdate}")
        a = w.address("office", rng.choice([x for x in K.REGIONS if x[0] != c.address.sido] or K.REGIONS))
        nm = f"{(a.sigungu.split()[0] if a.sigungu else a.sido)[:-1] or a.sido[:2]}지점"
        return {"title": "지점 설치의 건",
                "body": "의장은 영업망 확대를 위하여 아래와 같이 지점을 설치할 필요가 있음을 설명하고 그 가부를 물은바, {votes}원안대로 승인 가결하다.",
                "detail": f"지점명 : {nm} / 소재지 : {a.road_short} / 설치일 : {D(mdate + timedelta(days=rng.randint(10, 40)), 'dot')}"}
    if kind == "agm":
        gd = _weekday(mdate + timedelta(days=rng.randint(14, 25)))
        return {"title": "임시주주총회 소집의 건",
                "body": "의장은 아래와 같이 임시주주총회를 소집할 것을 제안하고 그 가부를 물은바, {votes}원안대로 승인 가결하다.",
                "detail": f"일시 : {D(gd, 'kor_short')} 오전 10시 / 장소 : 본점 회의실 / 회의목적사항 : "
                          + rng.choice(["이사 선임의 건, 정관 일부 변경의 건", "감사 선임의 건", "이사 보수한도 승인의 건"])}
    if kind == "fs":
        return {"title": f"제{max(1, mdate.year - c.established.year)}기 재무제표 및 영업보고서 승인의 건",
                "body": "의장은 제출된 재무제표(재무상태표, 손익계산서, 이익잉여금처분계산서) 및 영업보고서의 내용을 설명하고 "
                        "그 승인을 물은바, {votes}원안대로 승인하고 정기주주총회에 제출하기로 가결하다."}
    if kind == "collateral":
        amt = K.round_to(c.revenue * rng.uniform(0.03, 0.12), 10_000_000)
        return {"title": "담보 제공의 건",
                "body": "의장은 제1호 의안의 차입과 관련하여 회사 소유 부동산을 아래와 같이 담보로 제공할 것을 제안하고 그 가부를 물은바, "
                        "{votes}원안대로 승인 가결하다.",
                "detail": f"담보권자 : {p.bank} / 담보물 : 본사 사옥 토지 및 건물 / 채권최고액 : 금 {K.won_korean(amt)}원정 (₩{amt:,})"}
    if kind == "invest":
        amt = K.round_to(c.revenue * rng.uniform(0.01, 0.06), 1_000_000)
        item = rng.choice(["생산설비(자동화 라인) 도입", "본사 전산 시스템 고도화", "물류창고 증축", "연구개발용 장비 구입", "공장 설비 교체"])
        return {"title": "시설 투자 승인의 건",
                "body": "의장은 생산성 향상을 위하여 아래와 같이 시설에 투자하고자 함을 설명하고 그 가부를 물은바, {votes}원안대로 승인 가결하다.",
                "detail": f"투자내용 : {item} / 투자금액 : 금 {K.won_korean(amt)}원정 (₩{amt:,})"}
    if kind == "fx":
        lim = rng.choice([100_000, 300_000, 500_000, 1_000_000, 2_000_000])
        return {"title": "외국환거래약정 체결의 건",
                "body": "의장은 수출입 거래에 따른 외화 결제를 위하여 아래와 같이 외국환거래약정을 체결할 것을 제안하고 그 가부를 물은바, "
                        "{votes}원안대로 승인 가결하다.",
                "detail": f"거래은행 : {bank} / 약정한도 : USD {lim:,} / 약정기간 : 1년"}
    if kind == "ebank":
        return {"title": "기업 인터넷뱅킹 이용 및 법인카드 발급 신청의 건",
                "body": f"의장은 업무 효율화를 위하여 {bank}에 기업 인터넷뱅킹 이용 및 법인카드 발급을 신청하고 그 관리 책임자를 "
                        "재무팀장으로 지정할 것을 제안하고 그 가부를 물은바, {votes}원안대로 승인 가결하다."}
    if kind == "rule":
        return {"title": "임원 퇴직금 지급규정 개정안 상정의 건",
                "body": "의장은 임원 퇴직금 지급규정의 개정이 필요함을 설명하고 개정안을 주주총회에 상정할 것을 물은바, {votes}원안대로 승인 가결하다."}
    # lease
    dep = K.round_to(c.revenue * rng.uniform(0.002, 0.01), 1_000_000)
    return {"title": "본점 사무실 임대차계약 갱신의 건",
            "body": "의장은 본점 사무실의 임대차기간 만료에 따라 아래 조건으로 임대차계약을 갱신할 것을 제안하고 그 가부를 물은바, "
                    "{votes}원안대로 승인 가결하다.",
            "detail": f"임차목적물 : {c.address.road_short} / 보증금 : 금 {dep:,}원 / 월 차임 : 금 {K.round_to(dep * rng.uniform(0.05, 0.1), 100_000):,}원 / 기간 : 2년"}


@doc("board_minutes", "이사회의사록", "corporate")
def board_minutes(p: Profile, rng: random.Random) -> dict:
    """은행 차입 승인 이사회의사록 (출석 이사 기명날인).

    heavy: 안건 5~8개(지점 설치·주총 소집·담보 제공 등) → 2쪽. special: dissent 반대·기권 이사,
    remote 원격(화상) 참석, notarized 공증인 인증, seal_missing 일부 이사 날인 누락."""
    c, fx = p.corporation, _facts(p)
    mdate = _weekday(p.issue_date - timedelta(days=rng.randint(1, 20)))
    h, m, dur = _meeting_time(rng)
    directors = [o for o in fx["officers"] if o["role"] == "사내이사"]
    auditor_present = rng.random() < 0.7
    absent = 1 if (len(directors) >= 4 and rng.random() < 0.4) else 0
    attending = directors[:len(directors) - absent]
    amount = max(50_000_000, K.round_to(c.revenue * rng.uniform(0.04, 0.2), 10_000_000))
    months = rng.choice([12, 12, 24, 36, 60])
    start = mdate + timedelta(days=rng.randint(3, 15))
    end = date(start.year + months // 12, start.month, min(start.day, 28)) - timedelta(days=1)
    kind = rng.choice(["일반자금대출", "운전자금대출", "시설자금대출", "한도대출(마이너스)"])
    collateral = rng.choice(["신용", "신용보증기금 보증서", "기술보증기금 보증서", "본사 사옥 근저당권 설정", "신용 (연대보증 없음)"])
    many = heavy(rng, 0.25)
    pool = ["branch", "agm", "collateral", "invest", "fx", "ebank", "rule", "lease"] + (["fs"] if mdate.month <= 3 else [])
    extra = rng.sample(pool, rng.randint(3, 6)) if many else (rng.sample(pool, 1) if rng.random() < 0.3 else [])
    kinds = ["auth"] + extra
    agendas = [_board_agenda(k, p, fx, rng, mdate) for k in kinds]
    n_att = len(attending)
    dissent = special(rng, "dissent", 0.15) and n_att >= 3
    remote = special(rng, "remote", 0.15) and n_att >= 2
    others = [o["person"].name for o in attending[1:]]
    who = rng.choice(others) if others else None
    vote_idx = rng.randrange(len(agendas)) if dissent else -1
    for i, a in enumerate(agendas):
        if i == vote_idx:
            how = rng.choice(["반대", "반대", "기권"])
            a["votes"] = f"찬성 {n_att - 1}명, {how} 1명 (사내이사 {who})"
            reason = rng.choice(["추가 검토가 필요하다는", "시기상조라는", "비용 부담이 크다는", "사전 자료가 충분하지 않다는"])
            a["body"] = a["body"].replace("{votes}", "출석이사 과반수의 찬성으로 ") + \
                f" 사내이사 {who}는 {reason} 이유로 {how}하다."
        else:
            a["body"] = a["body"].replace("{votes}", rng.choice(["출석이사 전원이 이의 없이 찬성하여 ", "출석이사 전원의 찬성으로 "]))
        a["no"] = f"제{i + 2}호 의안"
    # 회의 시간은 안건 수에 따라
    end_m = h * 60 + m + dur + 8 * len(extra)
    signers = [{"title": "의장 대표이사", "name": p.person.name}] + \
        [{"title": "사내이사", "name": o["person"].name} for o in attending[1:]]
    if auditor_present:
        signers.append({"title": "감사", "name": fx["auditor"].name})
    d = {
        "company_name": c.name,
        "datetime": f"{D(mdate, 'kor_short')} {_hm(h, m)}",
        "venue": _venue(p, rng),
        "directors_total": f"{len(directors)}명",
        "directors_present": f"{len(attending)}명",
        "auditor_total": "1명",
        "auditor_present": "1명" if auditor_present else "0명",
        "chair": p.person.name,
        "loan": {
            "lender": p.bank,
            "bank": f"{p.bank} {p.bank_branch}",
            "kind": kind,
            "amount": f"금 {K.won_korean(amount)}원정 (₩{amount:,})",
            "period": f"{months // 12}년 ({D(start, 'dot')} ~ {D(end, 'dot')})",
            "purpose": "시설자금 (설비 취득)" if kind.startswith("시설") else rng.choice(["운전자금", "원자재 구입자금", "운영자금"]),
            "rate": rng.choice(["변동금리 (CD 91일물 + 가산금리)", "고정금리", "변동금리 (금융채 6개월 + 가산금리)", "은행 소정 금리"]),
            "collateral": collateral,
        },
        "agendas": agendas,
        "end_time": _hm(end_m // 60 % 24, end_m % 60),
        "minutes_date": D(mdate, "kor_short"),
        "head_office": c.address.road_short,
        "signers": signers,
    }
    if remote:
        rem = rng.sample(range(1, n_att), rng.randint(1, min(2, n_att - 1)))
        names = [attending[i]["person"].name for i in sorted(rem)]
        d["remote_attendees"] = ", ".join(f"사내이사 {x}" for x in names)
        d["remote_count"] = f"원격 참석 {len(names)}명 포함"
        d["remote_method"] = rng.choice(["화상회의", "화상회의, Zoom", "전화회의", "화상회의, Microsoft Teams"])
        for s in signers:
            if s["name"] in names:
                s["remote"] = "(원격 참석)"
    if special(rng, "notarized", 0.12):
        d["notary"] = _notary(p, rng, mdate)
    d = _Doc(d)
    d.seal_p = 0.5 if special(rng, "seal_missing", 0.12) else 0.95
    return d
