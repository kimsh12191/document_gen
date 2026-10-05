"""법인 관련 서류 (등기사항증명서, 정관, 주주명부, 재무제표, 법인인감증명서, 의사록, 위임장).

같은 프로필의 법인 서류끼리는 등기번호·목적·임원 취임일·발행예정주식수 등이 서로 맞아야 하므로,
그런 '법인 고정 사실'은 `_facts(p)`에서 프로필 seed 기반의 별도 Random 으로 한 번 만든다.
서류마다 달라지는 값(발급번호, 일시, 문구 변형 등)은 서류 rng 로 만든다.
"""
from __future__ import annotations

from ..entities import COMPANY_CORE, COMPANY_PREFIX, World
from ..registry import doc
from ._common import *  # noqa: F401,F403

PAR_VALUE = 5000

# 업종(종목)별 정관/등기부 목적 후보 (앞쪽일수록 주된 사업)
_PURPOSES = {
    "전자부품": ["전자부품 제조업", "전자부품 도소매업", "반도체 관련 부품 제조 및 판매업", "인쇄회로기판(PCB) 조립업",
             "전기·전자 기기 제조 및 판매업", "전자부품 수출입업", "전자제품 연구개발업", "부동산 임대업"],
    "자동차부품": ["자동차 부품 제조업", "자동차 부품 도소매업", "금형 설계 및 제작업", "금속 가공 및 열처리업",
              "자동차 부품 수출입업", "산업용 기계 제조업", "부동산 임대업"],
    "화학제품": ["기초 화학물질 제조업", "합성수지 및 플라스틱 제품 제조업", "화학제품 도소매업", "도료 및 접착제 제조업",
             "화학제품 수출입업", "환경 관련 약품 제조 및 판매업", "부동산 임대업"],
    "식료품": ["식료품 제조 및 가공업", "식품 도소매업", "건강기능식품 제조 및 판매업", "농수산물 가공 및 유통업",
            "식품 수출입업", "통신판매업", "부동산 임대업"],
    "응용소프트웨어 개발": ["응용 소프트웨어 개발 및 공급업", "정보통신 서비스업", "컴퓨터 프로그래밍 서비스업",
                    "시스템 통합 자문 및 구축 서비스업", "데이터베이스 및 온라인 정보 제공업", "전자상거래업",
                    "소프트웨어 유지보수업", "교육 서비스업"],
    "시스템 통합": ["시스템 통합 자문 및 구축 서비스업", "컴퓨터 및 주변기기 도소매업", "정보통신 공사업",
               "소프트웨어 개발 및 공급업", "네트워크 장비 판매 및 설치업", "전산장비 유지보수업", "정보보호 컨설팅업"],
    "무역": ["무역업", "수출입 대행업", "각종 상품 도소매업", "물품 중개업", "전자상거래업", "국제 물류 주선업", "부동산 임대업"],
    "의류 도매": ["의류 도소매업", "섬유 및 원단 도소매업", "의류 제조업", "패션 잡화 도소매업", "전자상거래업",
              "의류 수출입업", "디자인 서비스업"],
    "실내건축": ["실내건축 공사업", "건축공사업", "인테리어 디자인업", "건축자재 도소매업", "가구 제조 및 판매업",
             "부동산 개발 및 공급업", "전문 건설업"],
    "광고대행": ["광고 대행업", "광고물 제작업", "옥외 광고업", "출판 및 인쇄업", "영상 제작 및 배급업", "행사 기획 및 대행업",
             "온라인 마케팅 대행업"],
    "화물운송": ["일반화물 자동차 운송업", "화물 운송 주선업", "창고업", "국제 물류 주선업", "택배업", "자동차 정비업",
             "부동산 임대업"],
    "의료기기": ["의료기기 제조업", "의료기기 도소매업", "의료기기 수출입업", "의료용품 제조 및 판매업", "의료기기 수리업",
             "의료기기 연구개발업", "부동산 임대업"],
    "경영컨설팅": ["경영 컨설팅업", "기업 인수합병 자문업", "교육 및 연수 서비스업", "인력 공급 및 알선업", "시장조사 및 여론조사업",
              "투자 자문업(금융투자업 제외)", "부동산 컨설팅업"],
    "한식 음식점": ["일반 음식점업", "프랜차이즈 가맹사업", "식품 제조 및 가공업", "식자재 도소매업", "단체 급식업",
               "통신판매업", "부동산 임대업"],
}
_TAIL_PURPOSE = ["위 각 호에 관련된 부대사업 일체", "위 각호에 부대되는 사업 일체", "위 각 호와 관련된 부대사업 일체"]
_NEWSPAPERS = ["매일경제신문", "한국경제신문", "서울경제신문", "머니투데이", "조선일보", "중앙일보", "동아일보", "한국일보"]


def _kd(d: date) -> str:
    """등기부식 날짜: '2023 년 03 월 15 일'"""
    return f"{d.year} 년 {d.month:02d} 월 {d.day:02d} 일"


def _name_core(name: str) -> str:
    return name.replace("주식회사", "").replace("(주)", "").strip()


def _formal(name: str) -> str:
    """등기부·인감증명서·정관에 적히는 정식 상호: '(주)한빛전자' → '주식회사 한빛전자'."""
    return f"주식회사 {name[3:].strip()}" if name.startswith("(주)") else name


def _side_person(seed: str):
    """프로필에 없는 인물(감사·직원·대리인)을 seed 문자열로 결정론적으로 만든다."""
    w = World(0)
    w.rng = random.Random(seed)
    return w.person(birth_range=(1962, 1995))


def _add_years(d: date, n: int) -> date:
    try:
        return d.replace(year=d.year + n)
    except ValueError:  # 2월 29일
        return date(d.year + n, 3, 1)


class _Row(dict):
    """등기부 한 줄. 말소 표시(빨간 줄)는 값이 아니라 속성으로 둔다 (정답에 들어가지 않음)."""
    struck = False


class _Doc(dict):
    """서류 데이터. 화면 구성 선택(전문 수록 여부 등)은 값이 아니라 속성으로 둔다 (정답에 들어가지 않음)."""
    full = False


def _rd(r: random.Random, lo: date, hi: date) -> date:
    """lo~hi 사이 날짜 (구간이 비면 lo)."""
    return rand_date(r, lo, hi) if lo < hi else lo


def _region_of(a: Address):
    return next((x for x in K.REGIONS if x[0] == a.sido and x[1] == a.sigungu), None)


def _former_name(r: random.Random, name: str, used: set[str]) -> str:
    """상호 변경 전 이름: 앞말(한빛·대성…)이나 뒷말(전자→산업…)을 바꾼다."""
    core = _name_core(name)
    pre, suf = core, ""
    for _, _, _, s in COMPANY_CORE:
        if core.endswith(s) and len(core) > len(s):
            pre, suf = core[:-len(s)], s
            break
    for _ in range(20):
        if suf and r.random() < 0.5:
            cand = f"주식회사 {r.choice(COMPANY_PREFIX)}{suf}"
        else:
            cand = f"주식회사 {pre}{r.choice(['산업', '테크', '코리아', '상사', '엔지니어링', '인터내셔널', '산업개발', '앤컴퍼니'])}"
        if cand not in used:
            return cand
    return f"주식회사 {pre}{len(used)}"


_INVESTORS = ["{p}벤처투자 주식회사", "{p}인베스트먼트 주식회사", "{p}기술투자 주식회사", "{p} 개인투자조합 제{n}호",
              "{p}창업투자 신기술사업투자조합 제{n}호", "{p}파트너스 벤처투자조합 {n}호"]


def _facts(p: Profile) -> dict:
    """프로필 하나에 대해 항상 같은 법인 고정 사실 (등기 이력·주주 구성 포함).

    여기서 정하는 변형(heavy/special)은 프로필 단위라 같은 고객의 등기부·정관·주주명부·의사록이 같은 이야기를 한다.
      heavy 'hist'     임원 변경이 잦은 법인 (취임·중임·사임·퇴임 기록 다수, 증자 여러 번, 본점 이전 여러 번)
      heavy 'holders'  주주가 많은 법인 (20~40명)
      special name_change / office_move / purpose_added / branch / officer_turnover / co_ceo / treasury_stock / investor
    """
    c = p.corporation
    r = random.Random(f"corp-facts:{p.seed}:{c.corp_no}")
    est = c.established
    lim = p.issue_date - timedelta(days=40)  # 등기 이력은 발급일 40일 전까지
    issued = c.capital // PAR_VALUE
    authorized = max(issued * r.choice([4, 4, 10, 20]), r.choice([100_000, 200_000, 400_000, 1_000_000]))
    hist_heavy = heavy(r, 0.3)
    initial_shares = issued if r.random() < 0.6 else max(2000, issued // r.choice([2, 5, 10]))
    if hist_heavy and initial_shares == issued and issued >= 4000:
        initial_shares = issued // r.choice([2, 4, 5])
    pool = _PURPOSES.get(c.biz_item, ["도소매업", "서비스업", "전자상거래업", "부동산 임대업"])
    n = min(len(pool), r.randint(4, 7))
    purposes = pool[:2] + sorted(r.sample(pool[2:], n - 2), key=pool.index)
    tail = r.choice(_TAIL_PURPOSE)
    city = c.address.sido if c.address.sido.endswith("특별시") or c.address.sido.endswith("광역시") or \
        c.address.sido.endswith("자치시") else f"{c.address.sido} {c.address.sigungu.split()[0]}"
    domain = c.email.split("@")[-1]
    paper = r.choice(_NEWSPAPERS)
    if r.random() < 0.5:
        notice = f"{c.address.sido} 내에서 발행되는 일간 {paper}에 게재한다."
    else:
        notice = (f"회사의 인터넷 홈페이지(http://www.{domain})에 게재한다. 다만, 전산장애 또는 그 밖의 부득이한 사유로 "
                  f"인터넷 홈페이지에 공고를 할 수 없을 때에는 {c.address.sido}에서 발행되는 일간 {paper}에 게재한다.")

    def reg(d: date) -> date:
        return d + timedelta(days=r.randint(2, 13))

    def dates(k: int) -> list[date]:
        """설립 반년 뒤 ~ lim 사이 서로 다른 날짜 k개 (오름차순)."""
        lo = est + timedelta(days=180)
        return sorted({_rd(r, lo, lim - timedelta(days=20)) for _ in range(k)}) if lo < lim - timedelta(days=20) else []

    # --- 상호 변경 ---------------------------------------------------------
    names = [(_formal(c.name), None)]
    if special(r, "name_change", 0.12):
        ds = dates(2 if hist_heavy and r.random() < 0.3 else 1)
        if ds:
            back = [_formal(c.name)]
            for _ in ds:
                back.append(_former_name(r, c.name, set(back)))
            olds = back[1:][::-1]  # 오래된 것부터
            names = [(olds[0], None)] + list(zip(olds[1:] + [_formal(c.name)], ds))
    # --- 본점 이전 ---------------------------------------------------------
    offices = [(c.address, None)]
    if special(r, "office_move", 0.3):
        ds = dates(1 + (r.randint(0, 2) if hist_heavy else 0))
        w = World(0)
        w.rng = random.Random(f"office:{p.seed}")
        olds = [w.address("office", _region_of(c.address) if r.random() < 0.7 else None) for _ in ds]
        offices = [(olds[0], None)] + [(a, d) for a, d in zip(olds[1:], ds)] + [(c.address, ds[-1])] if ds else offices
    # --- 자본금 증자 -------------------------------------------------------
    capital_hist = [(initial_shares, None)]
    if initial_shares < issued:
        k = r.randint(2, 4) if hist_heavy else 1
        ds = dates(k)
        mids = sorted({K.round_to(r.uniform(initial_shares, issued), 100) for _ in range(len(ds) - 1)} - {initial_shares, issued})
        steps = mids + [issued]
        capital_hist += list(zip(steps, ds[-len(steps):])) if ds else []
        if len(capital_hist) == 1:  # 날짜를 못 정한 경우: 설립 때부터 현재 주식수
            initial_shares, capital_hist = issued, [(issued, None)]
    # --- 목적 추가 ---------------------------------------------------------
    purpose_versions = [(purposes + [tail], None)]
    if special(r, "purpose_added", 0.25) and len(purposes) > 3:
        cand = list(range(2, len(purposes)))
        added = sorted(r.sample(cand, min(len(cand), r.randint(1, 3 if hist_heavy else 2))))
        ds = dates(2 if hist_heavy and len(added) >= 2 and r.random() < 0.5 else 1)
        if ds:
            groups = [added[:1], added[1:]] if len(ds) == 2 else [added]
            vers, have = [], [i for i in range(len(purposes)) if i not in added]
            vers.append(([purposes[i] for i in have] + [tail], None))
            for g, d in zip(groups, ds):
                have = sorted(have + g)
                vers.append(([purposes[i] for i in have] + [tail], d))
            purpose_versions = vers
    # --- 지점 --------------------------------------------------------------
    branches = []
    if special(r, "branch", 0.15) or (hist_heavy and r.random() < 0.4):
        w = World(0)
        w.rng = random.Random(f"branch:{p.seed}")
        for d in dates(r.randint(2, 4) if hist_heavy else r.randint(1, 2)):
            a = w.address("office", r.choice([x for x in K.REGIONS if x[0] != c.address.sido] or K.REGIONS))
            closed = _rd(r, d + timedelta(days=300), lim) if hist_heavy and r.random() < 0.35 and d + timedelta(days=300) < lim else None
            branches.append({"address": a, "opened": d, "closed": closed,
                             "name": f"{(a.sigungu.split()[0] if a.sigungu else a.sido)[:-1] or a.sido[:2]}지점"})

    # --- 임원 --------------------------------------------------------------
    def chain(first: date, until: date) -> list[date]:
        out = [first]
        while _add_years(out[-1], 3) < until:
            out.append(_add_years(out[-1], 3))
        return out

    entries = []  # 등기부 임원란 기록 하나 = 임기 하나

    def add(role, person, starts, order, first_kind="취임", end=None):
        for i, s in enumerate(starts):
            last = i == len(starts) - 1
            entries.append({"role": role, "person": person, "start": s, "kind": first_kind if i == 0 else "중임",
                            "reg": reg(s), "end": end if last else None, "struck": not last or end is not None,
                            "order": order})

    ceo_starts = chain(est, lim)
    add("사내이사", p.person, ceo_starts, 0)
    add("대표이사", p.person, ceo_starts, 1)
    co_ceo = None
    dir_firsts = [est if r.random() < 0.5 else _rd(r, est, p.issue_date - timedelta(days=200)) for _ in p.directors]
    for i, (d, first) in enumerate(zip(p.directors, dir_firsts)):
        starts = chain(first, lim)
        add("사내이사", d, starts, 2 + 2 * i)
        if i == 0 and special(r, "co_ceo", 0.06):
            k = r.randrange(len(starts))
            add("대표이사", d, starts[k:], 3)
            co_ceo = {"person": d, "joint": r.random() < 0.5, "start": starts[k]}
    auditor = _side_person(f"auditor:{p.seed}")
    aud_first = est if r.random() < 0.6 else _rd(r, est, p.issue_date - timedelta(days=200))
    add("감사", auditor, chain(aud_first, lim), 20)
    if aud_first > est + timedelta(days=60):  # 전임 감사
        prev = _side_person(f"auditor0:{p.seed}")
        st = chain(est, aud_first)
        expired = _add_years(st[-1], 3) <= aud_first + timedelta(days=5)
        add("감사", prev, st, 20, end=(aud_first, "퇴임" if expired else "사임"))
    n_past = r.randint(3, 7) if hist_heavy else (r.randint(1, 2) if special(r, "officer_turnover", 0.3) else 0)
    for i in range(n_past):
        if est + timedelta(days=200) >= lim - timedelta(days=400):
            break
        person = _side_person(f"past-officer:{p.seed}:{i}")
        st = [_rd(r, est, lim - timedelta(days=400))]
        while r.random() < 0.45 and _add_years(st[-1], 3) < lim - timedelta(days=200):
            st.append(_add_years(st[-1], 3))
        expiry = _add_years(st[-1], 3)
        if expiry < lim and r.random() < 0.45:
            end = (expiry, "퇴임")
        else:
            end = (_rd(r, st[-1] + timedelta(days=60), min(expiry, lim) - timedelta(days=1)), "사임")
        add(r.choice(["사내이사"] * 6 + ["기타비상무이사", "사외이사"]), person, st, 10 + i, end=end)
    for e in entries:
        if e["end"]:
            e["end"] = {"date": e["end"][0], "kind": e["end"][1], "reg": reg(e["end"][0])}

    # --- 정관 개정일: 상호·본점(시 단위)·목적·발행예정주식 변경 + 그 밖의 개정 -------------
    rev = {d for _, d in names[1:]} | {d for _, d in purpose_versions[1:]}
    rev |= {d - timedelta(days=r.randint(0, 10)) for (a, d) in offices[1:] if d and r.random() < 0.5}
    extra = r.randint(3, 8) if hist_heavy else r.randint(0, 3)
    rev |= set(dates(extra))
    articles_dates = [est] + sorted(x for x in rev if x and x > est + timedelta(days=30))

    fx = {
        "reg_no": f"{r.randint(1, 299999):06d}", "issued": issued, "authorized": authorized,
        "initial_shares": initial_shares, "purposes": purposes + [tail], "notice": notice, "city": city,
        "auditor": auditor, "articles_dates": articles_dates, "seal_no": f"{r.randint(1, 9999):04d}",
        "names": names, "offices": offices, "capital_hist": capital_hist, "purpose_versions": purpose_versions,
        "branches": branches, "entries": entries, "co_ceo": co_ceo, "hist_heavy": hist_heavy,
    }
    # 현재 임원 (현재 유효사항 순서: 대표 사내이사, 대표이사, 사내이사들, 감사)
    cur = sorted([e for e in entries if not e["struck"]], key=lambda e: e["order"])
    fx["officers"] = cur
    fx["holders"] = _cap_table(p, r, fx)
    return fx


def _cap_table(p: Profile, r: random.Random, fx: dict) -> list[dict]:
    """주주 구성. 기본은 프로필의 3명. heavy 면 주주 20~40명, 자기주식·투자사(우선주) 특수 상황.
    대표이사 주식수와 지분 25% 이상 주주는 프로필 그대로 둔다 (실제소유자 확인서와 맞춤)."""
    c = p.corporation
    est = c.established
    issued = fx["issued"]
    base = list(p.shareholders)
    many = heavy(r, 0.25)
    treasury = special(r, "treasury_stock", 0.1)
    investor = special(r, "investor", 0.12)
    late = p.issue_date - timedelta(days=90)
    rows = []
    for i, (sh, n) in enumerate(base):
        acq = est if (i == 0 or r.random() < 0.5) else _rd(r, est, late)
        rows.append({"holder": sh, "shares": n, "type": "보통주", "acquired": acq, "kind": "base"})
    if not (many or treasury or investor):
        return rows
    # 지분 25% 미만인 이사 주식 일부를 떼어 다른 주주에게 나눈다
    pool = 0
    lo, hi = (0.35, 0.7) if (many or investor) else (0.1, 0.3)
    for row in rows[1:]:
        if row["shares"] * 4 < issued:
            take = int(row["shares"] * r.uniform(lo, hi))
            row["shares"] -= take
            pool += take
    extras, alloc = [], []  # (holder, type, kind), 주식수
    left = pool
    if treasury and left >= 10:
        n = max(1, int(pool * (r.uniform(0.15, 0.3) if (many or investor) else 1.0)))
        extras.append((c.name, "보통주", "treasury"))
        alloc.append(n)
        left -= n
    if investor and left >= 10:
        inv = int(left * (r.uniform(0.35, 0.6) if many else 1.0))
        k = r.randint(1, 2) if inv >= 20 else 1
        pref = r.random() < 0.5 and len(fx["capital_hist"]) > 1
        cut = _split(inv, [r.uniform(0.5, 1.0) for _ in range(k)])
        for n in cut:
            nm = r.choice(_INVESTORS).format(p=r.choice(COMPANY_PREFIX), n=r.randint(1, 12))
            extras.append((nm, "상환전환우선주" if pref else "보통주", "investor"))
            alloc.append(n)
        left -= inv
    if many and left >= 17:
        k = min(r.randint(17, 37), left // 3)
        ws = [r.uniform(0.3, 1.6) for _ in range(k)]
        cut = _split(left - k, ws)
        for j, n in enumerate(cut):
            extras.append((_side_person(f"holder:{p.seed}:{j}"), "보통주", "minor"))
            alloc.append(n + 1)
        left = 0
    if left and alloc:  # 남은 주식은 마지막 주주에게
        alloc[-1] += left
    elif left:
        rows[1]["shares"] += left
    if not extras:
        return rows
    incs = [d for _, d in fx["capital_hist"][1:]]
    for (h, typ, kind), n in zip(extras, alloc):
        if kind == "investor" and incs:
            acq = incs[-1]
        else:
            acq = _rd(r, est + timedelta(days=200), late)
        rows.append({"holder": h, "shares": n, "type": typ, "acquired": acq, "kind": kind})
    # 우선주는 정렬상 뒤로, 자기주식은 맨 끝
    rows = rows[:len(base)] + sorted(rows[len(base):], key=lambda x: (x["kind"] == "treasury", x["kind"] != "investor", -x["shares"]))
    return rows


def _addr(a: Address) -> str:
    return a.road_full


def _mask_any(rrn: str, rng: random.Random) -> str:
    return K.mask_rrn(rrn, rng.choice([0, 1, 1]))


# ---------------------------------------------------------------------------
# 1. 등기사항전부증명서 (현재 유효사항)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# 2. 정관
# ---------------------------------------------------------------------------

@doc("articles_of_incorporation", "정관", "corporate")
def articles_of_incorporation(p: Profile, rng: random.Random) -> dict:
    """주식회사 정관 사본 (원본대조필).

    기본은 첫 쪽(총칙·주식)만 싣고 '중략' 후 부칙. heavy 면 전문(주주총회·이사·감사·계산 장까지, 3~4쪽).
    개정 이력은 프로필 단위(_facts): 상호 변경·목적 추가 등 등기부 변경과 같은 날 개정, 해당 조문 끝에 <개정 …>."""
    c, fx = p.corporation, _facts(p)
    est = c.established
    dates = fx["articles_dates"]
    hist = [f"제정 {D(dates[0], 'dot')}"] + [f"개정 {D(x, 'dot')}" for x in dates[1:]]
    full = heavy(rng, 0.3)
    preferred = any(h["type"] != "보통주" for h in fx["holders"])
    d = {
        "company_name": _formal(c.name),
        "company_name_en": c.name_en,
        "purposes": [f"{i}. {x}" for i, x in enumerate(fx["purposes"], 1)],
        "head_office_city": fx["city"],
        "notice_method": fx["notice"],
        "authorized_shares": f"{fx['authorized']:,}주",
        "par_value": f"금 {PAR_VALUE:,}원",
        "initial_shares": f"{fx['initial_shares']:,}주",
        "effective_date": D(est, "kor_short"),
        "revision_history": hist,
        "revision_effective": [D(x, "kor_short") for x in dates[1:]],
        "ceo_name": p.person.name,
    }
    amended = {}
    if len(fx["names"]) > 1:
        amended["company_name"] = ", ".join(D(dt, "dot") for _, dt in fx["names"][1:])
    if len(fx["purpose_versions"]) > 1:
        amended["purposes"] = ", ".join(D(dt, "dot") for _, dt in fx["purpose_versions"][1:])
    if preferred:
        amended["share_types"] = D(fx["capital_hist"][-1][1] or dates[-1], "dot")
    if amended:
        d["amended"] = amended
    if special(rng, "cert_missing", 0.1):  # 원본대조필 없이 사본만 낸 경우
        d.pop("ceo_name")
    else:
        d["certify_date"] = D(p.issue_date - timedelta(days=rng.randint(0, 7)), rng.choice(["kor", "kor_short", "dot"]))
    if preferred:
        d["preferred"] = "상환전환우선주식"
    d = _Doc(d)
    d.full = full
    return d


# ---------------------------------------------------------------------------
# 3. 주주명부
# ---------------------------------------------------------------------------

@doc("shareholder_registry", "주주명부", "corporate")
def shareholder_registry(p: Profile, rng: random.Random) -> dict:
    """법인 주주명부 (대표이사 확인 날인).

    주주 구성은 프로필 단위(_cap_table): heavy 면 주주 20~40명(여러 쪽), 자기주식(회사 명의, 비고 '자기주식'),
    투자사 법인주주(상환전환우선주) 특수 상황."""
    c, fx = p.corporation, _facts(p)
    holders = fx["holders"]
    total = sum(h["shares"] for h in holders)
    # 지분율: 최대잔여법으로 합계 100 유지 (소수점 1자리 또는 2자리)
    dec = rng.choice([1, 2, 2])
    unit = 100 * 10 ** dec
    raw = [h["shares"] * unit / total for h in holders]
    bp = [int(x) for x in raw]
    for i in sorted(range(len(raw)), key=lambda i: raw[i] - bp[i], reverse=True)[:unit - sum(bp)]:
        bp[i] += 1
    pct = (lambda b: f"{b / 10 ** dec:.{dec}f}%")
    directors = {d.name for d in p.directors}
    rows = []
    for i, (h, b) in enumerate(zip(holders, bp), 1):
        sh, n = h["holder"], h["shares"]
        if h["kind"] == "treasury":
            name, idno, addr, note = c.name, c.biz_no, c.address.road_short, "자기주식"
        elif isinstance(sh, str):  # 법인주주: 사업자등록번호
            w = World(0)
            w.rng = random.Random(f"investor:{sh}")
            name, idno, addr, note = sh, K.biz_no(random.Random(sh), corporate=True), w.address("office").road_short, "법인주주"
        else:
            name, idno, addr = sh.name, _mask_any(sh.rrn, rng), sh.address.road_short
            note = "대표이사" if sh is p.person else ("사내이사" if sh.name in directors else "")
        rows.append({"no": str(i), "name": name, "id_no": idno, "address": addr, "share_type": h["type"],
                     "shares": f"{n:,}", "amount": f"{n * PAR_VALUE:,}", "ratio": pct(b), "acquired": D(h["acquired"], "dot"),
                     "note": note or None})
    base = p.issue_date - timedelta(days=rng.randint(0, 20))
    return {
        "base_date": D(base, rng.choice(["kor", "dot"])),
        "company_name": c.name,
        "corp_reg_no": c.corp_no,
        "biz_no": c.biz_no,
        "head_office": c.address.road_short,
        "total_shares": f"{total:,}주",
        "par_value": won(PAR_VALUE),
        "capital": won(c.capital),
        "shareholders": rows,
        "sum_shares": f"{total:,}",
        "sum_amount": f"{total * PAR_VALUE:,}",
        "sum_ratio": pct(unit),
        "certify_date": D(p.issue_date, rng.choice(["kor", "kor_short"])),
        "ceo_name": p.person.name,
    }


# ---------------------------------------------------------------------------
# 4. 재무제표 (재무상태표 + 손익계산서)
# ---------------------------------------------------------------------------

def _split(total: int, weights: list[float]) -> list[int]:
    s = sum(weights)
    out = [int(total * w / s) for w in weights[:-1]]
    return out + [total - sum(out)]


def _income(rev: int, rng: random.Random, loss: bool = False) -> dict:
    cogs = int(rev * rng.uniform(0.6, 0.85))
    gross = rev - cogs
    op_margin = rng.uniform(-0.03, 0.0) if rng.random() < 0.1 else rng.uniform(0.01, 0.12)
    if loss:  # 당기순손실: 영업손실이 영업외손익으로 메워지지 않을 만큼
        op_margin = rng.uniform(-0.08, -0.025)
    sga = max(int(rev * 0.03), gross - int(rev * op_margin))
    op = gross - sga
    noi = int(rev * rng.uniform(0.002, 0.015))
    noe = int(rev * rng.uniform(0.003, 0.02))
    pre = op + noi - noe
    tax = int(pre * rng.uniform(0.08, 0.19)) if pre > 0 else 0
    int_inc = int(noi * rng.uniform(0.3, 0.9))
    int_exp = int(noe * rng.uniform(0.5, 0.95))
    return {"rev": rev, "cogs": cogs, "gross": gross, "sga": sga, "op": op, "noi": noi, "noe": noe,
            "pre": pre, "tax": tax, "net": pre - tax, "int_inc": int_inc, "int_exp": int_exp}


_MFG = {"전자부품", "자동차부품", "화학제품", "식료품", "의료기기"}


def _bs_layout(c, rng: random.Random) -> dict:
    """재무상태표에 나올 세부 계정 구성(두 기 공통). 일반기업회계기준 과목 배열 순서."""
    mfg = c.biz_item in _MFG
    tang = ["기계장치", rng.choice(["차량운반구", "비품"])] if mfg else ["차량운반구", "비품"]
    if rng.random() < 0.25:
        tang = ["토지"] + tang
    return {
        "quick": ["현금및현금성자산"] + (["단기금융상품"] if rng.random() < 0.3 else []) + ["매출채권", "대손충당금"]
                 + [x for x in ["미수금", "선급금"] if rng.random() < 0.4],
        "inv": ["제품", "원재료"] if mfg else ["상품"],
        "invest": ["장기금융상품"] if rng.random() < 0.5 else [],
        "tang": tang,
        "intang": [rng.choice(["소프트웨어", "개발비", "특허권"])] if rng.random() < 0.7 else [],
        "onca": ["임차보증금"],
        "cl": ["매입채무", "미지급금"] + (["예수금"] if rng.random() < 0.5 else []) + ["단기차입금"]
              + (["미지급세금"] if rng.random() < 0.4 else []),
        "ncl": ["장기차입금", "퇴직급여충당부채"],
    }


def _balance(rev: int, capital: int, re: int, lay: dict, rng: random.Random, pref: int = 0) -> list[tuple[str, int, int]]:
    """(과목, 금액, 단계) 목록. 단계 0=Ⅰ·Ⅱ, 1=(1)(2), 2=세부계정, 9=총계. 자산총계 = 부채총계 + 자본총계."""
    equity = capital + re
    liab = max(int(equity * rng.uniform(0.4, 2.2)), int(rev * rng.uniform(0.12, 0.3)))
    assets = equity + liab
    ca, nca = _split(assets, [rng.uniform(0.4, 0.75), 1])
    quick, inv = _split(ca, [rng.uniform(0.6, 0.9), rng.uniform(0.1, 0.4) if "제품" in lay["inv"] else rng.uniform(0.03, 0.15)])
    groups = [g for g in ("invest", "tang", "intang", "onca") if lay[g]]
    wts = {"invest": rng.uniform(0.05, 0.2), "tang": rng.uniform(0.5, 0.8), "intang": rng.uniform(0.01, 0.06),
           "onca": rng.uniform(0.05, 0.2)}
    nca_parts = dict(zip(groups, _split(nca, [wts[g] for g in groups])))

    def detail(total: int, names: list[str]) -> list[tuple[str, int, int]]:
        """세부 계정 배분. 대손충당금·감가상각누계액은 바로 위 계정의 차감 항목으로 넣는다."""
        if not names:
            return []
        plus = [n for n in names if n != "대손충당금"]
        vals = dict(zip(plus, _split(total, [rng.uniform(0.3, 1.0) * (2.5 if i == 0 else 1) for i, _ in enumerate(plus)])))
        out = []
        for n in names:
            if n == "대손충당금":
                ar = vals["매출채권"]
                allow = int(ar * rng.uniform(0.005, 0.02))
                out[-1] = ("매출채권", ar + allow, 2)
                out.append(("대손충당금", -allow, 2))
            elif n in ("기계장치", "차량운반구", "비품", "건물"):
                net = vals[n]
                dep = int(net * rng.uniform(0.2, 1.2))
                out += [(n, net + dep, 2), ("감가상각누계액", -dep, 2)]
            else:
                out.append((n, vals[n], 2))
        return out

    rows = [("자　　산", None, -1), ("Ⅰ. 유동자산", ca, 0), ("(1) 당좌자산", quick, 1)] + detail(quick, lay["quick"])
    rows += [("(2) 재고자산", inv, 1)] + detail(inv, lay["inv"]) + [("Ⅱ. 비유동자산", nca, 0)]
    labels = {"invest": "투자자산", "tang": "유형자산", "intang": "무형자산", "onca": "기타비유동자산"}
    for i, g in enumerate(groups, 1):
        rows += [(f"({i}) {labels[g]}", nca_parts[g], 1)] + detail(nca_parts[g], lay[g])
    rows.append(("자산총계", assets, 9))
    cl, ncl = _split(liab, [rng.uniform(0.5, 0.8), 1])
    rows += [("부　　채", None, -1), ("Ⅰ. 유동부채", cl, 0)] + detail(cl, lay["cl"])
    rows += [("Ⅱ. 비유동부채", ncl, 0)] + detail(ncl, lay["ncl"]) + [("부채총계", liab, 9)]
    rows += [("자　　본", None, -1), ("Ⅰ. 자본금", capital, 0), ("보통주자본금", capital - pref, 2)]
    rows += [("우선주자본금", pref, 2)] if pref else []
    rows += [
             ("Ⅱ. 이익잉여금" if re >= 0 else "Ⅱ. 결손금", re, 0),
             ("미처분이익잉여금" if re >= 0 else "미처리결손금", re, 2),
             ("자본총계", equity, 9), ("부채와자본총계", liab + equity, 9)]
    return rows


_SGA = ["급여", "퇴직급여", "복리후생비", "여비교통비", "접대비", "통신비", "수도광열비", "세금과공과", "감가상각비",
        "지급임차료", "수선비", "보험료", "차량유지비", "운반비", "교육훈련비", "도서인쇄비", "소모품비", "지급수수료",
        "광고선전비", "대손상각비", "무형자산상각비", "잡비"]
_MFG_EXP = ["복리후생비", "전력비", "가스수도료", "감가상각비", "수선비", "보험료", "소모품비", "외주가공비", "운반비",
            "지급수수료", "세금과공과", "차량유지비"]


@doc("financial_statements", "재무제표(재무상태표·손익계산서)", "corporate")
def financial_statements(p: Profile, rng: random.Random) -> dict:
    """최근 결산 2개년 비교 재무상태표 + 손익계산서 (일반기업회계기준 과목 배열, 자산 = 부채 + 자본).

    heavy: 판매비와관리비·매출원가 세부 계정 + 이익잉여금처분계산서 (+ 제조업은 제조원가명세서) → 2~3쪽.
    special: net_loss 당기순손실, certified 원본대조(대표이사 확인·법인인감)."""
    c, fx = p.corporation, _facts(p)
    unit_label, unit = rng.choice([("원", 1), ("원", 1), ("천원", 1000)])
    fy = p.issue_date.year - 1 if p.issue_date.month >= 4 else p.issue_date.year - 2
    fy = max(fy, c.established.year + 1)
    term = fy - c.established.year + 1
    rev_cur = round(c.revenue / unit)
    rev_prev = round(rev_cur / rng.uniform(0.88, 1.3))
    cap = c.capital // unit
    pref = sum(h["shares"] for h in fx["holders"] if h["type"] != "보통주") * PAR_VALUE // unit
    loss = special(rng, "net_loss", 0.1)
    inc_prev, inc_cur = _income(rev_prev, rng), _income(rev_cur, rng, loss)
    re0 = int(cap * rng.uniform(0.1, 1.5)) + int(rev_cur * rng.uniform(0.01, 0.2))
    if re0 + inc_prev["net"] <= 0 or re0 + inc_prev["net"] + inc_cur["net"] <= 0:
        re0 += abs(min(inc_prev["net"], inc_prev["net"] + inc_cur["net"])) + cap // 2
    re_prev = re0 + inc_prev["net"]
    re_cur = re_prev + inc_cur["net"]
    lay = _bs_layout(c, rng)
    bs_prev, bs_cur = _balance(rev_prev, cap, re_prev, lay, rng, pref), _balance(rev_cur, cap, re_cur, lay, rng, pref)
    big = heavy(rng, 0.25)

    neg = rng.choice(["paren", "paren", "tri", "minus"])

    def fmt(n: int | None) -> str:
        if n is None:
            return ""
        if n >= 0:
            return f"{n:,}"
        return {"paren": f"({-n:,})", "tri": f"△{-n:,}", "minus": f"-{-n:,}"}[neg]

    def bs_rows(lo: int, hi: int):
        return [{"account": a, "current": fmt(v), "prior": fmt(pv)}
                for (a, v, lv), (_, pv, _) in zip(bs_cur[lo:hi], bs_prev[lo:hi]) if lv >= 0]

    def bs_val(rows, name):
        return next((v for a, v, lv in rows if a == name and lv == 2), 0)

    def rows3(spec):
        return [{"account": a, "current": fmt(x), "prior": fmt(y)} for a, x, y in spec]

    idx = [i for i, (_, _, lv) in enumerate(bs_cur) if lv == -1] + [len(bs_cur) - 1]
    service = c.biz_item in ("응용소프트웨어 개발", "시스템 통합", "광고대행", "화물운송", "경영컨설팅")
    mfg = c.biz_item in _MFG
    sales = "용역매출" if service else ("제품매출" if mfg else "상품매출")
    spec = [("Ⅰ. 매출액", inc_cur["rev"], inc_prev["rev"]), (sales, inc_cur["rev"], inc_prev["rev"]),
            ("Ⅱ. 매출원가", inc_cur["cogs"], inc_prev["cogs"])]
    made = None
    if big and not service:  # 매출원가 = 기초재고 + 당기제조(매입) - 기말재고
        inv = "제품" if mfg else "상품"
        end_c, end_p = bs_val(bs_cur, inv), bs_val(bs_prev, inv)
        beg_p = int(end_p * rng.uniform(0.8, 1.2))
        made = (inc_cur["cogs"] - end_p + end_c, inc_prev["cogs"] - beg_p + end_p)
        spec += [(f"기초{inv}재고액", end_p, beg_p),
                 ("당기제품제조원가" if mfg else "당기상품매입액", made[0], made[1]),
                 (f"기말{inv}재고액", end_c, end_p)]
    spec += [("Ⅲ. 매출총이익", inc_cur["gross"], inc_prev["gross"]),
             ("Ⅳ. 판매비와관리비", inc_cur["sga"], inc_prev["sga"])]
    if big:
        accs = _SGA[:3] + sorted(rng.sample(_SGA[3:], rng.randint(9, 15)), key=_SGA.index)
        w = [rng.uniform(4, 7) if a == "급여" else rng.uniform(0.3, 1.5) for a in accs]
        cur = _split(inc_cur["sga"], [x * rng.uniform(0.85, 1.15) for x in w])
        prv = _split(inc_prev["sga"], w)
        spec += list(zip(accs, cur, prv))
    spec += [("Ⅴ. 영업이익(손실)", inc_cur["op"], inc_prev["op"]), ("Ⅵ. 영업외수익", inc_cur["noi"], inc_prev["noi"]),
             ("이자수익", inc_cur["int_inc"], inc_prev["int_inc"])]
    if big:
        spec += [("잡이익", inc_cur["noi"] - inc_cur["int_inc"], inc_prev["noi"] - inc_prev["int_inc"])]
    spec += [("Ⅶ. 영업외비용", inc_cur["noe"], inc_prev["noe"]), ("이자비용", inc_cur["int_exp"], inc_prev["int_exp"])]
    if big:
        spec += [("잡손실", inc_cur["noe"] - inc_cur["int_exp"], inc_prev["noe"] - inc_prev["int_exp"])]
    spec += [("Ⅷ. 법인세비용차감전순이익(손실)", inc_cur["pre"], inc_prev["pre"]),
             ("Ⅸ. 법인세비용", inc_cur["tax"], inc_prev["tax"]), ("Ⅹ. 당기순이익(손실)", inc_cur["net"], inc_prev["net"])]
    prev_start = max(date(fy - 1, 1, 1), c.established)
    d = {
        "company_name": c.name,
        "unit": f"(단위 : {unit_label})",
        "current_term": f"제 {term}(당)기",
        "prior_term": f"제 {term - 1}(전)기",
        "bs_current_date": f"{fy}년 12월 31일 현재",
        "bs_prior_date": f"{fy - 1}년 12월 31일 현재",
        "is_current_period": f"{fy}년 01월 01일부터 {fy}년 12월 31일까지",
        "is_prior_period": f"{prev_start.year}년 {prev_start.month:02d}월 {prev_start.day:02d}일부터 {fy - 1}년 12월 31일까지",
        "assets": bs_rows(idx[0] + 1, idx[1]),
        "liabilities": bs_rows(idx[1] + 1, idx[2]),
        "equity": bs_rows(idx[2] + 1, idx[3]),
        "total_liabilities_equity": {"current": fmt(bs_cur[-1][1]), "prior": fmt(bs_prev[-1][1])},
        "income_statement": rows3(spec),
    }
    if big:
        # 이익잉여금처분계산서: 전기 처분액은 0 (재무상태표 이익잉여금 = 전기말 + 당기순이익과 맞춤)
        div = K.round_to(cap * rng.uniform(0.02, 0.1), 1000 // unit or 1) if rng.random() < 0.35 and re_cur > cap and not loss else 0
        legal = div // 10
        ap = [("Ⅰ. 미처분이익잉여금", re_cur, re_prev), ("전기이월미처분이익잉여금", re_prev, re0),
              ("당기순이익(손실)", inc_cur["net"], inc_prev["net"]), ("Ⅱ. 이익잉여금처분액", legal + div, 0)]
        if div:
            ap += [("이익준비금", legal, 0), ("현금배당", div, 0)]
        ap += [("Ⅲ. 차기이월미처분이익잉여금", re_cur - legal - div, re_prev)]
        d["appropriation"] = rows3(ap)
        agm = _weekday(date(fy + 1, 3, rng.randint(20, 31)))
        agm0 = _weekday(date(fy, 3, rng.randint(20, 31)))
        d["appropriation_date_current"] = f"처분예정일 {agm.year}년 {agm.month:02d}월 {agm.day:02d}일"
        d["appropriation_date_prior"] = f"처분확정일 {agm0.year}년 {agm0.month:02d}월 {agm0.day:02d}일"
        if mfg and made:
            rows = []
            for m_tot, raw_end, raw_beg in ((made[0], bs_val(bs_cur, "원재료"), bs_val(bs_prev, "원재료")),
                                            (made[1], bs_val(bs_prev, "원재료"), None)):
                beg = raw_beg if raw_beg is not None else int(raw_end * rng.uniform(0.8, 1.2))
                mat, labor, exp = _split(m_tot, [rng.uniform(0.5, 0.7), rng.uniform(0.15, 0.25), rng.uniform(0.12, 0.25)])
                sal, ret = _split(labor, [0.9, 0.1])
                rows.append({"mat": mat, "beg": beg, "buy": mat - beg + raw_end, "end": raw_end, "labor": labor,
                             "sal": sal, "ret": ret, "exp": exp, "tot": m_tot})
            exps = sorted(rng.sample(_MFG_EXP, rng.randint(7, 11)), key=_MFG_EXP.index)
            ew = [rng.uniform(0.3, 1.5) for _ in exps]
            e_cur, e_prv = _split(rows[0]["exp"], ew), _split(rows[1]["exp"], [x * rng.uniform(0.85, 1.15) for x in ew])
            cc, pp = rows
            mc = [("Ⅰ. 재료비", cc["mat"], pp["mat"]), ("기초원재료재고액", cc["beg"], pp["beg"]),
                  ("당기원재료매입액", cc["buy"], pp["buy"]), ("기말원재료재고액", cc["end"], pp["end"]),
                  ("Ⅱ. 노무비", cc["labor"], pp["labor"]), ("급여", cc["sal"], pp["sal"]), ("퇴직급여", cc["ret"], pp["ret"]),
                  ("Ⅲ. 경비", cc["exp"], pp["exp"])] + list(zip(exps, e_cur, e_prv)) + \
                 [("Ⅳ. 당기총제조비용", cc["tot"], pp["tot"]), ("Ⅴ. 당기제품제조원가", cc["tot"], pp["tot"])]
            d["manufacturing_cost"] = rows3(mc)
    if special(rng, "certified", 0.25):
        d["certify_date"] = D(p.issue_date - timedelta(days=rng.randint(0, 10)), rng.choice(["kor", "kor_short"]))
        d["ceo_name"] = p.person.name
    return d


# ---------------------------------------------------------------------------
# 5. 법인인감증명서
# ---------------------------------------------------------------------------

@doc("corporate_seal_certificate", "법인인감증명서", "corporate", sample_mark=True)
def corporate_seal_certificate(p: Profile, rng: random.Random) -> dict:
    """등기소 발급 법인 인감증명서."""
    c, fx = p.corporation, _facts(p)
    issued = p.issue_date - timedelta(days=rng.randint(0, 10))
    office = courthouse(c.address)
    d = {
        "issue_no": f"{rng.randint(1000, 9999)}-{rng.randint(1000, 9999)}-{rng.randint(1000, 9999)}-{rng.randint(1000, 9999)}",
        "reg_no": fx["reg_no"],
        "corp_reg_no": c.corp_no,
        "company_name": _formal(c.name),
        "head_office": _addr(c.address),
        "rep_title": "대표이사",
        "rep_name": p.person.name,
        "rep_rrn": K.mask_rrn(p.person.rrn, rng.choice([0, 1])),
        "issue_date": f"{issued.year}년 {issued.month:02d}월 {issued.day:02d}일",
        "issue_office": office,
        "registrar": _side_person(f"registrar:{office}:{issued.year}").name,
        "fee": rng.choice(["1,000원", "1,000원", "700원"]),
        "purpose": rng.choice(["금융기관 제출용", "은행 제출용", "여신거래용", "일반용"]),
    }
    if special(rng, "purpose_blank", 0.1):  # 용도란을 비워 둔 채 발급
        d["purpose"] = None
    if special(rng, "internet_issue", 0.2):  # 전자증명서로 인터넷 발급: 발급확인번호, 전산운영책임관
        d["issue_office"] = "법원행정처 등기정보중앙관리소"
        d.pop("registrar")
        d["fee"] = "500원"
        d["confirm_no"] = "-".join("".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789") for _ in range(4))
                                   for _ in range(3))
    return d


# ---------------------------------------------------------------------------
# 6. 이사회의사록 / 7. 임시주주총회의사록
# ---------------------------------------------------------------------------

def _weekday(d: date) -> date:
    """주말·1월 1일을 피해 직전 평일로 옮긴다."""
    while d.weekday() >= 5 or (d.month, d.day) == (1, 1):
        d -= timedelta(days=1)
    return d


def _meeting_time(rng: random.Random) -> tuple[int, int, int]:
    h = rng.choice([9, 10, 10, 11, 14, 15, 16])
    m = rng.choice([0, 0, 0, 30])
    return h, m, rng.randint(20, 55)


def _hm(h: int, m: int) -> str:
    ampm = "오전" if h < 12 else "오후"
    return f"{ampm} {h if h <= 12 else h - 12}시 {m:02d}분"


def _venue(p: Profile, rng: random.Random) -> str:
    return rng.choice(["본점 회의실", "본점 소회의실", "본점 대회의실", "회사 본점 회의실"]) + f" ({p.corporation.address.road_short})"


_NOTARY_FIRMS = ["법무법인 한결", "법무법인 율촌", "법무법인 세움", "법무법인 동인", "법무법인 바른길", "법무법인 정명",
                 "법무법인 대륙", "법무법인 해송", "공증인가 법무법인 신원", "공증인가 법무법인 다올"]


def _notary(p: Profile, rng: random.Random, mdate: date) -> dict:
    """의사록 인증(공증) 기재: 등부 번호, 인증일, 공증인(법무법인), 담당 변호사."""
    nd = mdate + timedelta(days=rng.randint(0, 6))
    while nd.weekday() >= 5:
        nd += timedelta(days=1)
    return {"reg_no": f"{nd.year}년 제{rng.randint(1, 4999)}호", "date": D(nd, "kor_short"),
            "office": rng.choice(_NOTARY_FIRMS), "lawyer": _side_person(f"notary:{p.seed}:{nd}").name}


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


# ---------------------------------------------------------------------------
# 8. 위임장
# ---------------------------------------------------------------------------

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
