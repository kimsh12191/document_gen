"""pension_enrollment_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/income.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.income import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _MEAL,
    _ensure_gap,
    _months_between,
    _pension_base,
    _t10,
    _work_history,
)
from docgen.registry import doc


@doc("pension_enrollment_certificate", "국민연금 가입자 가입증명", "income")
def pension_enrollment_certificate(p: Profile, rng: random.Random) -> dict:
    """국민연금공단 발급 가입자 가입증명 — 국민연금법 시행규칙 [별지 제11호서식] 국민연금가입자증명서.

    □ 가입자의 인적사항(발급번호·발급일자·성명·주민등록번호) / □ 가입자의 종류 및 자격 취득일
    (최초 자격취득일, 가입자 종류·사업장명칭·자격취득일·자격상실일) / 증명 문구 / 국민연금공단 이사장.
    """
    hist = _work_history(p, many=heavy(rng, 0.3))  # 이직이 잦은 사람: 사업장 이동 다수
    exempt = special(rng, "pension_exemption", 0.15)  # 실직 기간 납부예외
    if exempt:
        hist = _ensure_gap(hist, "local", rng)
    voluntary = special(rng, "voluntary_member", 0.08)  # 소득 없는 기간 임의가입
    if voluntary:
        hist = _ensure_gap(hist, "dep", rng)
    df = rng.choice(["dot", "dash"])
    cur_wage = _pension_base(_t10(p.employment.annual_salary / 12) - _MEAL, p.issue_date)
    rows, months = [], 0
    for h in hist:
        end = h["end"] or p.issue_date
        if h["kind"] == "dep" and not voluntary:
            continue  # 소득 없는 배우자: 적용제외 (가입 이력 없음)
        kind = {"work": "사업장가입자", "local": "지역가입자", "dep": "임의가입자"}[h["kind"]]
        row = {"kind": kind, "start": D(h["start"], df)}
        if h["kind"] == "work":
            row["workplace"] = h["name"]
            row["wage"] = won(h["wage"] if h["wage"] else cur_wage, "")
        elif h["kind"] == "dep":
            row["wage"] = won(rng.choice([1_000_000, 1_000_000, 1_500_000, 2_000_000]) if h["start"].year >= 2015
                              else rng.choice([700_000, 900_000, 1_000_000]), "")
        else:
            row["wage"] = won(K.round_to(rng.uniform(900_000, 1_500_000), 1000), "")
            if exempt and (rng.random() < 0.7 or not any(r_.get("note", "").startswith("납부예외") for r_ in rows)):
                row["note"] = rng.choice(["납부예외(실직)", "납부예외(실직)", "납부예외(휴·폐업)"])
        if not row.get("note", "").startswith("납부예외"):
            months += _months_between(h["start"], end)
        if h["end"]:
            row["end"] = D(h["end"], df)
        rows.append(row)
    return {
        "issue_no": f"{p.issue_date:%Y%m%d}-{rng.randint(10000000, 99999999)}",
        "person": {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.5 else p.person.rrn},
        "first_acquired": D(next(h["start"] for h in hist if h["kind"] != "dep" or voluntary), df),
        "total_months": f"{months}개월",
        "rows": rows,
        "purpose": rng.choice(["금융기관 제출용", "은행 제출용", "기타"]),
        "issue_date": D(p.issue_date, "kor_short"),
        "issue_date_head": D(p.issue_date, df),
    }
