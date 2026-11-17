"""employment_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/income.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.income import _DUTIES, _leave_period  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("employment_certificate", "재직증명서", "income")
def employment_certificate(p: Profile, rng: random.Random) -> dict:
    """회사가 발급하는 재직증명서 (근로기준법 제39조 사용증명서, 법정서식 없음 — 통용 양식).

    통용 양식: 문서번호 / 인적사항(성명·주민등록번호(또는 생년월일)·주소) / 재직사항(회사명·사업자등록번호·
    소재지·소속·직위·재직기간·담당업무) / 용도·제출처 / 증명 문구 / 발급일 / 회사명·대표이사 (직인).
    """
    e = p.employment
    c = e.company
    df = rng.choice(["kor", "dot", "dot"])
    idv = rng.random()
    employee = {"name": p.person.name, "address": p.person.address.road_full}
    if idv < 0.55:
        employee["rrn"] = K.mask_rrn(p.person.rrn)
    elif idv < 0.75:
        employee["rrn"] = p.person.rrn
    else:
        employee["birth"] = D(p.person.birth, rng.choice(["kor", "dot"]))
    employment = {
        "department": e.department,
        "position": e.position,
        "period": f"{D(e.hire_date, df)} ~ 현재",
        "duty": _DUTIES.get(e.department, "일반 사무"),
    }
    # 특수 상황: 기간제(계약직) 근로자 — 고용형태와 현재 계약기간을 함께 적는다
    if special(rng, "contract_worker", 0.08):
        employment["employment_type"] = rng.choice(["계약직", "계약직(기간제)", "촉탁직"])
        cs = e.hire_date
        while date(cs.year + 1, cs.month, min(cs.day, 28)) <= p.issue_date:
            cs = date(cs.year + 1, cs.month, min(cs.day, 28))
        ce = date(cs.year + 1, cs.month, min(cs.day, 28)) - timedelta(days=1)
        employment["contract_period"] = f"{D(cs, df)} ~ {D(ce, df)}"
    # 특수 상황: 육아휴직 (현재 휴직 중이거나 지난 휴직 이력)
    if special(rng, "parental_leave", 0.1):
        lv = _leave_period(p)
        if lv:
            employment["leave"] = f"{D(lv[0], df)} ~ {D(lv[1], df)} ({rng.choice(['육아휴직', '육아휴직', '출산전후휴가 및 육아휴직'])})"
    # 특수 상황: 급여(연봉)를 함께 적어 달라고 한 경우 (재직 및 급여 증명)
    if special(rng, "salary_shown", 0.12):
        employment["annual_salary"] = f"연 {won(e.annual_salary)}" if rng.random() < 0.5 else won(e.annual_salary)
    return {
        "doc_no": rng.choice([f"제 {p.issue_date.year}-{rng.randint(1, 999):03d} 호",
                              f"제{p.issue_date:%y}{rng.randint(1, 999):04d}호"]),
        "employee": employee,
        "company": {
            "name": c.name,
            "biz_no": c.biz_no,
            "address": c.address.road_short,
            "phone": c.phone,
            "ceo": c.ceo.name,
        },
        "employment": employment,
        "purpose": rng.choice(["금융기관 제출용", "대출 신청용", "은행 제출용"]),
        "submit_to": p.bank,
        "issue_date": D(p.issue_date, rng.choice(["kor", "kor_short"])),
    }
