"""career_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/income.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.income import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _DUTIES,
    _company_name,
    _leave_period,
    _months_between,
)
from docgen.entities import DEPARTMENTS, POSITIONS
from docgen.registry import doc


@doc("career_certificate", "경력증명서", "income")
def career_certificate(p: Profile, rng: random.Random) -> dict:
    """현 직장이 발급하는 경력증명서 (근로기준법 제39조 사용증명서, 통용 양식: 인적사항 / 경력사항
    (근무기간·근무부서·직위·담당업무) / 총 근무기간 / 용도·제출처 / 증명 문구 / 회사 정보·대표이사 직인)."""
    e = p.employment
    c = e.company
    names = [x[0] for x in POSITIONS]
    idx = names.index(e.position)
    promos = [(e.hire_date if i == 0 else date(e.hire_date.year + th, 1, 1), nm)
              for i, (nm, th) in enumerate(POSITIONS[:idx + 1])]
    promos = [s for s in promos if s[0] < p.issue_date]
    df = rng.choice(["dot", "dot", "dash", "kor"])
    # 구간: (시작일, 부서, 직위, 담당업무)
    if heavy(rng, 0.25):
        # 인사발령(부서 이동·승진·겸무)이 많은 장기 근속자: 발령마다 한 줄
        segs, cur, dept = [], e.hire_date, rng.choice(DEPARTMENTS)
        pi = 0
        while cur < p.issue_date:
            while pi + 1 < len(promos) and promos[pi + 1][0] <= cur:
                pi += 1
            segs.append([cur, dept, promos[pi][1], _DUTIES.get(dept, "일반 사무")])
            nxt = months_back(cur, -rng.choice([3, 6, 6, 8, 12, 12, 18]))
            nxt = date(nxt.year, nxt.month, 1)
            if pi + 1 < len(promos) and promos[pi + 1][0] < nxt:
                nxt = promos[pi + 1][0]  # 승진 발령
            elif rng.random() < 0.65:
                dept = rng.choice([x for x in DEPARTMENTS if x != dept])  # 전보 발령
            cur = nxt
        # 마지막 구간은 현재 부서·직위
        segs[-1][1], segs[-1][2], segs[-1][3] = e.department, e.position, _DUTIES.get(e.department, "일반 사무")
        for s in segs:
            if rng.random() < 0.12 and s[2] in ("과장", "차장", "부장"):
                s[3] = f"{s[3]} (팀장 직무대행)" if rng.random() < 0.5 else f"{s[3]} / {rng.choice(DEPARTMENTS)} 겸무"
    else:
        stints = promos
        if len(stints) > 6:
            stints = [(e.hire_date, stints[-6][1])] + stints[-5:]
        segs = []
        for i, (start, pos) in enumerate(stints):
            last = i == len(stints) - 1
            dept = e.department if last or rng.random() < 0.6 else rng.choice(DEPARTMENTS)
            segs.append([start, dept, pos, _DUTIES.get(dept, "일반 사무")])
    ends = [segs[i + 1][0] - timedelta(days=1) for i in range(len(segs) - 1)] + [None]
    segs = [s + [en] for s, en in zip(segs, ends)]  # [시작, 부서, 직위, 업무, 끝(None=현재)]
    # 특수 상황: 계열사 파견 근무 구간
    if special(rng, "dispatch", 0.08):
        cand = [i for i, s in enumerate(segs) if s[4] and (s[4] - s[0]).days > 200]
        if cand:
            i = rng.choice(cand)
            s = segs[i]
            ds = date(s[0].year, s[0].month, 1) if s[0].day == 1 else s[0]
            de = months_back(ds, -rng.choice([3, 6, 6, 12]))
            if de < s[4]:
                aff = _company_name(random.Random(f"aff:{p.seed}"))
                segs[i:i + 1] = [[ds, f"{aff} 파견", s[2], "계열사 파견 근무", de - timedelta(days=1)],
                                 [de, s[1], s[2], s[3], s[4]]]
    # 특수 상황: 육아휴직 기간 (해당 구간을 휴직 전/휴직/복직으로 나눈다)
    leave_m = 0
    if special(rng, "parental_leave", 0.12):
        lv = _leave_period(p)
        if lv:
            for i, s in enumerate(segs):
                end = s[4] or p.issue_date
                if s[0] < lv[0] <= end:
                    ongoing = lv[1] >= p.issue_date
                    new = [[s[0], s[1], s[2], s[3], lv[0] - timedelta(days=1)]]
                    if ongoing:  # 현재 휴직 중: 이후 발령 없음
                        new.append([lv[0], e.department, e.position, "육아휴직", None])
                    else:
                        new.append([lv[0], s[1], s[2], "육아휴직", lv[1]])
                        for sg in [[lv[1] + timedelta(days=1), s[1], s[2], s[3], s[4]]] + segs[i + 1:]:
                            if sg[4] is not None and sg[4] <= lv[1]:
                                continue  # 휴직 중에 끝난 구간은 없앤다
                            sg[0] = max(sg[0], lv[1] + timedelta(days=1))
                            new.append(sg)
                    segs = segs[:i] + new
                    leave_m = _months_between(lv[0], min(lv[1], p.issue_date))
                    break
    rows = []
    for s in segs:
        rows.append({"period": f"{D(s[0], df)} ~ {D(s[4], df) if s[4] else '현재'}", "department": s[1],
                     "position": s[2], "duty": s[3]})
    m = (p.issue_date.year - e.hire_date.year) * 12 + p.issue_date.month - e.hire_date.month
    if p.issue_date.day < e.hire_date.day:
        m -= 1
    total = f"{m // 12}년 {m % 12}개월"
    if leave_m:
        total += f" (휴직기간 {leave_m}개월 포함)"
    return {
        "doc_no": rng.choice([f"제 {p.issue_date.year}-{rng.randint(1, 999):03d} 호",
                              f"{c.name.replace('(주)', '').replace('주식회사 ', '')[:2]}인사-{p.issue_date.year}-{rng.randint(10, 999)}"]),
        "person": {
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.6 else p.person.rrn,
            "address": p.person.address.road_full,
            "phone": p.person.mobile,
        },
        "hire_date": D(e.hire_date, df),
        "total_period": total,
        "careers": rows,
        "purpose": rng.choice(["금융기관 제출용", "은행 제출용", "대출 신청용", "경력 확인용"]),
        "submit_to": p.bank,
        "company": {
            "name": c.name,
            "biz_no": c.biz_no,
            "address": c.address.road_short,
            "phone": c.phone,
            "ceo": c.ceo.name,
        },
        "issue_date": D(p.issue_date, rng.choice(["kor", "kor_short"])),
    }
