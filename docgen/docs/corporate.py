"""법인 관련 서류 (등기사항증명서, 정관, 주주명부, 재무제표, 법인인감증명서, 의사록, 위임장).

이 파일에는 그룹 서식들이 같이 쓰는 도우미만 있다. 서식마다 값 만드는 함수(@doc)는 서식 폴더
docgen/forms/<ID>/generate.py 에 있고, 끝의 FORMS 차례로 등록한다.

같은 프로필의 법인 서류끼리는 등기번호·목적·임원 취임일·발행예정주식수 등이 서로 맞아야 하므로,
그런 '법인 고정 사실'은 `_facts(p)`에서 프로필 seed 기반의 별도 Random 으로 한 번 만든다.
서류마다 달라지는 값(발급번호, 일시, 문구 변형 등)은 서류 rng 로 만든다.
"""
from __future__ import annotations

from ..entities import COMPANY_CORE, COMPANY_PREFIX, World
from ._common import *  # noqa: F401,F403
from ..registry import register_folder_forms

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


# ---------------------------------------------------------------------------
# 1. 등기사항전부증명서 (현재 유효사항)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 2. 정관
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 3. 주주명부
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 4. 재무제표 (재무상태표 + 손익계산서)
# ---------------------------------------------------------------------------

def _split(total: int, weights: list[float]) -> list[int]:
    s = sum(weights)
    out = [int(total * w / s) for w in weights[:-1]]
    return out + [total - sum(out)]


# ---------------------------------------------------------------------------
# 5. 법인인감증명서
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# 8. 위임장
# ---------------------------------------------------------------------------


# 이 그룹의 코드 서식. 값 만드는 함수는 서식 폴더 docgen/forms/<ID>/generate.py 에 있다 (여기는 같이 쓰는 도우미).
FORMS = ('corporate_registry', 'articles_of_incorporation', 'shareholder_registry', 'financial_statements', 'corporate_seal_certificate', 'board_minutes', 'shareholders_meeting_minutes', 'power_of_attorney',)
register_folder_forms(__name__, FORMS)   # 예전 @doc 차례 그대로 등록 (서식 목록·데이터셋 순서)
