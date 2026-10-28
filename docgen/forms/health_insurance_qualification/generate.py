"""health_insurance_qualification: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/income.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.income import _company_name, _ensure_gap, _work_history  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("health_insurance_qualification", "건강보험 자격득실확인서", "income")
def health_insurance_qualification(p: Profile, rng: random.Random) -> dict:
    """국민건강보험공단 발급 건강보험 자격득실 확인서 (국민건강보험법 제11조 자격취득 등의 확인).

    가입자구분(직장가입자·지역세대주·지역세대원·직장피부양자) / 사업장 명칭 / 자격취득일 / 자격상실일.
    """
    hist = _work_history(p, many=heavy(rng, 0.3))  # 이직이 잦은 사람: 자격 취득·상실 반복
    if special(rng, "regional_switch", 0.15):  # 퇴직 후 지역가입자로 전환된 기간
        hist = _ensure_gap(hist, "local", rng)
    if special(rng, "spouse_dependent", 0.1):  # 퇴직 후 배우자(가족)의 피부양자로 등재된 기간
        hist = _ensure_gap(hist, "dep", rng)
    fam_co = _company_name(random.Random(f"famco:{p.seed}"))
    df = rng.choice(["dot", "dash"])
    rows = [{"kind": "직장피부양자", "start": D(p.person.birth, df), "end": D(hist[0]["start"], df)}]
    items = []
    for h in hist:
        if h["kind"] == "work":
            row = {"kind": "직장가입자", "workplace": h["name"]}
        elif h["kind"] == "dep":
            row = {"kind": "직장피부양자", "workplace": fam_co}
        else:
            row = {"kind": rng.choice(["지역세대주", "지역세대원"])}
        items.append((h["start"], row, h["end"]))
    # 특수 상황: 두 사업장에 동시에 다닌 기간 (이중 직장가입)
    if special(rng, "dual_job", 0.05):
        lo, hi = p.employment.hire_date + timedelta(days=60), p.issue_date - timedelta(days=60)
        if hi > lo:
            ds = rand_date(rng, lo, hi)
            de = ds + timedelta(days=rng.randint(60, 400))
            items.append((ds, {"kind": "직장가입자", "workplace": _company_name(rng)}, de if de < p.issue_date else None))
            items.sort(key=lambda x: x[0])
    for start, row, end in items:
        row["start"] = D(start, df)
        if end:
            row["end"] = D(end, df)
        rows.append(row)
    if p.person.birth.year < 1977:  # 전산 기록 이전 이력은 생략
        rows = rows[1:]
    return {
        "issue_no": f"{rng.randint(1000, 9999)}-{rng.randint(1000, 9999)}-{rng.randint(1000, 9999)}-{rng.randint(1000, 9999)}",
        "person": {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.6 else p.person.rrn},
        "rows": rows,
        "purpose": rng.choice(["금융기관 제출용", "은행 제출용", "기타 제출용"]),
        "issue_date": D(p.issue_date, "kor_short"),
    }
