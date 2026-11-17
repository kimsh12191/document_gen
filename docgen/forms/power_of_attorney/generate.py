"""power_of_attorney: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/corporate.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from __future__ import annotations

from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.corporate import _Doc, _side_person  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


_STAFF_POS = ["재무팀 과장", "경영지원팀 대리", "재무팀 차장", "총무팀 부장", "회계팀 과장", "경영지원실 실장", "관리팀 대리"]


@doc("power_of_attorney", "위임장", "corporate")
def power_of_attorney(p: Profile, rng: random.Random) -> dict:
    """은행 여신거래 관련 위임장 (법인 또는 개인 위임인)."""
    c = p.corporation
    corporate = rng.random() < 0.65
    bfmt = rng.choice(["dot", "kor"])
    if corporate:
        agent = _side_person(f"agent:{p.seed}:{rng.random()}")
        relation = f"직원 ({rng.choice(_STAFF_POS)})"
        grantor = {"type": "법인", "name": c.name, "ceo": p.person.name, "biz_no": c.biz_no,
                   "corp_reg_no": c.corp_no, "address": c.address.road_short, "phone": c.phone}
    else:
        fam = [(p.spouse, "배우자")] if p.spouse else []
        fam += [(ch, "자녀") for ch in p.children if ch.age >= 20]
        if fam and rng.random() < 0.7:
            agent, relation = rng.choice(fam)
        else:
            agent, relation = _side_person(f"agent:{p.seed}:{rng.random()}"), rng.choice(["지인", "친척", "법무사 사무원"])
        grantor = {"type": "개인", "name": p.person.name, "birth": D(p.person.birth, bfmt),
                   "address": p.person.address.road_full, "phone": p.person.mobile}
    bank = f"{p.bank} {p.bank_branch}"
    tasks = rng.choice([
        [f"{bank} 여신거래 관련 서류 제출 및 수령 일체", "대출 신청서 및 약정서 등 제반 서류의 작성·제출",
         "위 업무 처리에 필요한 증명서류의 발급 및 제출"],
        [f"{bank} 여신(대출) 기한연장 신청 및 관련 서류 제출 일체", "기한연장 약정서 수령 및 전달"],
        [f"{bank} 대출금 실행 관련 서류 제출 및 수령 일체", "담보 관련 서류(근저당권설정계약서 등) 제출",
         "인감증명서 등 구비서류 제출"],
        [f"{bank} 기업 인터넷뱅킹 및 여신거래 관련 서류 제출·수령 일체"],
    ])
    granted = p.issue_date - timedelta(days=rng.randint(0, 7))
    tasks = [f"{i}. {t}" for i, t in enumerate(tasks, 1)]
    d = {
        "grantor": grantor,
        "agent": {"name": agent.name, "birth": D(agent.birth, bfmt), "address": agent.address.road_full,
                  "phone": agent.mobile, "relation": relation},
        "tasks": tasks,
        "period": f"{D(granted, 'dot')} ~ {D(granted + timedelta(days=rng.choice([30, 60, 90])), 'dot')}",
        "grant_date": D(granted, rng.choice(["kor", "kor_short"])),
        "recipient": rng.choice([f"{p.bank} 귀중", f"{p.bank} {p.bank_branch} 귀중", f"{p.bank} {p.bank_branch}장 앞"]),
        "attachment": "법인인감증명서 1부" if corporate else "인감증명서 1부",
    }
    if special(rng, "single_use", 0.15):  # 기간 대신 1회 한정 / 짧은 기간
        if rng.random() < 0.5:
            d.pop("period")
            d["use_limit"] = rng.choice(["본 위임장은 위 업무 1회에 한하여 유효함", "위 건에 한하여 1회 사용"])
        else:
            d["period"] = f"{D(granted, 'dot')} ~ {D(granted + timedelta(days=rng.choice([3, 7, 14])), 'dot')} (기간 내 1회 한정)"
    if special(rng, "sub_delegation", 0.15):
        d["sub_delegation"] = "허용"
    elif rng.random() < 0.25:
        d["sub_delegation"] = "불허"
    if special(rng, "handwritten_extra", 0.15):  # 인쇄된 위임사항 아래 손으로 덧붙여 쓴 항목
        d["tasks_extra"] = f"{len(tasks) + 1}. " + rng.choice(["통장 및 OTP 재발급 신청·수령", "잔액증명서 발급 신청·수령",
                                                               "거래내역서 발급 신청", "인감 변경 신고", "대출 이자 납입일 변경 신청"])
    d = _Doc(d)
    d.seal_p = 0.85 if special(rng, "seal_missing", 0.08) else 1.0
    return d
