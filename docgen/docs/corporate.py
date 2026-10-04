"""법인 관련 서류 (등기사항증명서, 정관, 주주명부, 재무제표, 법인인감증명서, 의사록, 위임장).

같은 프로필의 법인 서류끼리는 등기번호·목적·임원 취임일·발행예정주식수 등이 서로 맞아야 하므로,
그런 '법인 고정 사실'은 `_facts(p)`에서 프로필 seed 기반의 별도 Random 으로 한 번 만든다.
서류마다 달라지는 값(발급번호, 일시, 문구 변형 등)은 서류 rng 로 만든다.
"""
from __future__ import annotations

from ..entities import World
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


def _facts(p: Profile) -> dict:
    """프로필 하나에 대해 항상 같은 법인 고정 사실."""
    c = p.corporation
    r = random.Random(f"corp-facts:{p.seed}:{c.corp_no}")
    issued = c.capital // PAR_VALUE
    authorized = max(issued * r.choice([4, 4, 10, 20]), r.choice([100_000, 200_000, 400_000, 1_000_000]))
    initial_shares = issued if r.random() < 0.6 else max(2000, issued // r.choice([2, 5, 10]))
    pool = _PURPOSES.get(c.biz_item, ["도소매업", "서비스업", "전자상거래업", "부동산 임대업"])
    n = min(len(pool), r.randint(4, 7))
    purposes = pool[:2] + sorted(r.sample(pool[2:], n - 2), key=pool.index)
    purposes.append(r.choice(_TAIL_PURPOSE))
    city = c.address.sido if c.address.sido.endswith("특별시") or c.address.sido.endswith("광역시") or \
        c.address.sido.endswith("자치시") else f"{c.address.sido} {c.address.sigungu.split()[0]}"
    domain = c.email.split("@")[-1]
    paper = r.choice(_NEWSPAPERS)
    if r.random() < 0.5:
        notice = f"{c.address.sido} 내에서 발행되는 일간 {paper}에 게재한다."
    else:
        notice = (f"회사의 인터넷 홈페이지(http://www.{domain})에 게재한다. 다만, 전산장애 또는 그 밖의 부득이한 사유로 "
                  f"인터넷 홈페이지에 공고를 할 수 없을 때에는 {c.address.sido}에서 발행되는 일간 {paper}에 게재한다.")

    # 임원: 대표이사(사내이사) = 본인, 사내이사 = directors, 감사 = 별도 인물
    def term(first: date) -> tuple[date, str]:
        start, kind = first, "취임"
        while _add_years(start, 3) < p.issue_date - timedelta(days=40):
            start, kind = _add_years(start, 3), "중임"
        return start, kind

    est = c.established
    officers = []
    people = [("사내이사", p.person, est)] + [
        ("사내이사", d, est if r.random() < 0.5 else rand_date(r, est, p.issue_date - timedelta(days=200)))
        for d in p.directors]
    auditor = _side_person(f"auditor:{p.seed}")
    people.append(("감사", auditor, est if r.random() < 0.6 else rand_date(r, est, p.issue_date - timedelta(days=200))))
    for role, person, first in people:
        start, kind = term(first)
        officers.append({"role": role, "person": person, "start": start, "kind": kind,
                         "reg": start + timedelta(days=r.randint(2, 13))})
    ceo_off = dict(officers[0], role="대표이사")
    officers.insert(1, ceo_off)
    articles_dates = [est] + sorted({rand_date(r, est + timedelta(days=200), p.issue_date - timedelta(days=60))
                                     for _ in range(r.randint(0, 3))
                                     if est + timedelta(days=200) < p.issue_date - timedelta(days=60)})
    return {
        "reg_no": f"{r.randint(1, 299999):06d}", "issued": issued, "authorized": authorized,
        "initial_shares": initial_shares, "purposes": purposes, "notice": notice, "city": city,
        "officers": officers, "auditor": auditor, "articles_dates": articles_dates,
        "seal_no": f"{r.randint(1, 9999):04d}",
        # 증자(설립 시 주식수 < 현재 발행주식수)·본점이전 이력: 등기부 우측 '변경/등기 연월일' 칸에 쓰인다
        "capital_increase": _later(r, est, p.issue_date) if initial_shares < issued else None,
        "office_move": _later(r, est, p.issue_date) if r.random() < 0.3 else None,
    }


def _later(r: random.Random, est: date, until: date) -> date | None:
    lo, hi = est + timedelta(days=180), until - timedelta(days=60)
    return rand_date(r, lo, hi) if lo < hi else None


def _addr(a: Address) -> str:
    return a.road_full


def _mask_any(rrn: str, rng: random.Random) -> str:
    return K.mask_rrn(rrn, rng.choice([0, 1, 1]))


# ---------------------------------------------------------------------------
# 1. 등기사항전부증명서 (현재 유효사항)
# ---------------------------------------------------------------------------

@doc("corporate_registry", "법인 등기사항전부증명서(현재 유효사항)", "corporate")
def corporate_registry(p: Profile, rng: random.Random) -> dict:
    """인터넷등기소 발급 법인 등기사항전부증명서(현재 유효사항)."""
    c, fx = p.corporation, _facts(p)
    issued_at = p.issue_date - timedelta(days=rng.randint(0, 10))
    hh, mm, ss = rng.randint(9, 18), rng.randint(0, 59), rng.randint(0, 59)
    officers = []
    for o in fx["officers"]:
        it = {"position": o["role"], "name": o["person"].name, "rrn": K.mask_rrn(o["person"].rrn, 0),
              "appointed": _kd(o["start"]), "appointment_type": o["kind"], "registered": _kd(o["reg"])}
        if o["role"] == "대표이사":
            it["address"] = _addr(o["person"].address)
        officers.append(it)
    viewing = rng.random() < 0.4

    def chg(dt: date | None, word: str) -> dict | None:
        if dt is None:
            return None
        reg = dt + timedelta(days=rng.randint(2, 10))
        return {"changed": f"{D(dt, 'dot')} {word}", "registered": f"{D(reg, 'dot')} 등기"}
    d = {
        "reg_no": fx["reg_no"],
        "corp_reg_no": c.corp_no,
        "company_name": _formal(c.name),
        "head_office": _addr(c.address),
        "notice_method": fx["notice"],
        "par_value": f"금 {PAR_VALUE:,} 원",
        "authorized_shares": f"{fx['authorized']:,} 주",
        "issued_shares": f"{fx['issued']:,} 주",
        "common_shares": f"{fx['issued']:,} 주",
        "capital": f"금 {c.capital:,} 원",
        "purposes": [f"{i}. {x}" for i, x in enumerate(fx["purposes"], 1)],
        "officers": officers,
        "established": _kd(c.established),
        "opening_reason": "설립",
        "opening_date": _kd(c.established),
        "jurisdiction": courthouse(c.address),
        "capital_change": chg(fx["capital_increase"], "변경"),
        "head_office_change": chg(fx["office_move"], "이전"),
        "issue_no": "".join(str(rng.randint(0, 9)) for _ in range(rng.choice([16, 20]))),
    }
    d = {k: v for k, v in d.items() if v is not None}
    if viewing:
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
    """주식회사 정관 첫 페이지(총칙·주식) + 부칙, 원본대조필."""
    c, fx = p.corporation, _facts(p)
    est = c.established
    dates = fx["articles_dates"]
    hist = [f"제정 {D(dates[0], 'dot')}"] + [f"개정 {D(x, 'dot')}" for x in dates[1:]]
    return {
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
        "certify_date": D(p.issue_date - timedelta(days=rng.randint(0, 7)), rng.choice(["kor", "kor_short", "dot"])),
        "ceo_name": p.person.name,
    }


# ---------------------------------------------------------------------------
# 3. 주주명부
# ---------------------------------------------------------------------------

@doc("shareholder_registry", "주주명부", "corporate")
def shareholder_registry(p: Profile, rng: random.Random) -> dict:
    """법인 주주명부 (대표이사 확인 날인)."""
    c, fx = p.corporation, _facts(p)
    total = sum(n for _, n in p.shareholders)
    # 지분율: 최대잔여법으로 합계 100 유지 (소수점 1자리 또는 2자리)
    dec = rng.choice([1, 2, 2])
    unit = 100 * 10 ** dec
    raw = [n * unit / total for _, n in p.shareholders]
    bp = [int(x) for x in raw]
    for i in sorted(range(len(raw)), key=lambda i: raw[i] - bp[i], reverse=True)[:unit - sum(bp)]:
        bp[i] += 1
    pct = (lambda b: f"{b / 10 ** dec:.{dec}f}%")
    directors = {d.name for d in p.directors}
    rows = []
    for i, ((sh, n), b) in enumerate(zip(p.shareholders, bp), 1):
        acq = c.established if (i == 1 or rng.random() < 0.5) else rand_date(rng, c.established, p.issue_date - timedelta(days=90))
        if isinstance(sh, str):  # 법인주주: 사업자등록번호
            name, idno, addr, note = sh, K.biz_no(random.Random(sh), corporate=True), "-", "법인주주"
        else:
            name, idno, addr = sh.name, _mask_any(sh.rrn, rng), sh.address.road_short
            note = "대표이사" if sh is p.person else ("사내이사" if sh.name in directors else "")
        rows.append({"no": str(i), "name": name, "id_no": idno, "address": addr, "share_type": "보통주",
                     "shares": f"{n:,}", "amount": f"{n * PAR_VALUE:,}", "ratio": pct(b), "acquired": D(acq, "dot"),
                     "note": note})
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


def _income(rev: int, rng: random.Random) -> dict:
    cogs = int(rev * rng.uniform(0.6, 0.85))
    gross = rev - cogs
    op_margin = rng.uniform(-0.03, 0.0) if rng.random() < 0.1 else rng.uniform(0.01, 0.12)
    sga = max(int(rev * 0.03), gross - int(rev * op_margin))
    op = gross - sga
    noi = int(rev * rng.uniform(0.002, 0.015))
    noe = int(rev * rng.uniform(0.003, 0.02))
    pre = op + noi - noe
    tax = int(pre * rng.uniform(0.08, 0.19)) if pre > 0 else 0
    return {"rev": rev, "cogs": cogs, "gross": gross, "sga": sga, "op": op, "noi": noi, "noe": noe,
            "pre": pre, "tax": tax, "net": pre - tax}


def _balance(rev: int, capital: int, re: int, rng: random.Random) -> dict:
    equity = capital + re
    liab = max(int(equity * rng.uniform(0.4, 2.2)), int(rev * rng.uniform(0.12, 0.3)))
    assets = equity + liab
    ca, nca = _split(assets, [rng.uniform(0.4, 0.75), 1])
    cash, ar, inv, oca = _split(ca, [rng.uniform(0.15, 0.35), rng.uniform(0.25, 0.45), rng.uniform(0.05, 0.3),
                                     rng.uniform(0.03, 0.1)])
    tang, intang, onca = _split(nca, [rng.uniform(0.6, 0.85), rng.uniform(0.01, 0.08), rng.uniform(0.07, 0.25)])
    cl, ncl = _split(liab, [rng.uniform(0.5, 0.8), 1])
    ap, stb, oap, ocl = _split(cl, [rng.uniform(0.25, 0.45), rng.uniform(0.2, 0.45), rng.uniform(0.05, 0.15),
                                    rng.uniform(0.05, 0.15)])
    ltb, sev = _split(ncl, [rng.uniform(0.6, 0.9), rng.uniform(0.1, 0.3)])
    return {"ca": ca, "cash": cash, "ar": ar, "inv": inv, "oca": oca, "nca": nca, "tang": tang, "intang": intang,
            "onca": onca, "assets": assets, "cl": cl, "ap": ap, "stb": stb, "oap": oap, "ocl": ocl, "ncl": ncl,
            "ltb": ltb, "sev": sev, "liab": liab, "capital": capital, "re": re, "equity": equity}


_BS_ASSETS = [("Ⅰ. 유동자산", "ca"), ("1. 현금및현금성자산", "cash"), ("2. 매출채권", "ar"), ("3. 재고자산", "inv"),
              ("4. 기타유동자산", "oca"), ("Ⅱ. 비유동자산", "nca"), ("1. 유형자산", "tang"), ("2. 무형자산", "intang"),
              ("3. 기타비유동자산", "onca"), ("자산총계", "assets")]
_BS_LIAB = [("Ⅰ. 유동부채", "cl"), ("1. 매입채무", "ap"), ("2. 단기차입금", "stb"), ("3. 미지급금", "oap"),
            ("4. 기타유동부채", "ocl"), ("Ⅱ. 비유동부채", "ncl"), ("1. 장기차입금", "ltb"), ("2. 퇴직급여충당부채", "sev"),
            ("부채총계", "liab")]
_BS_EQ = [("Ⅰ. 자본금", "capital"), ("Ⅱ. 이익잉여금", "re"), ("자본총계", "equity")]
_IS = [("Ⅰ. 매출액", "rev"), ("Ⅱ. 매출원가", "cogs"), ("Ⅲ. 매출총이익", "gross"), ("Ⅳ. 판매비와관리비", "sga"),
       ("Ⅴ. 영업이익(손실)", "op"), ("Ⅵ. 영업외수익", "noi"), ("Ⅶ. 영업외비용", "noe"),
       ("Ⅷ. 법인세비용차감전순이익(손실)", "pre"), ("Ⅸ. 법인세비용", "tax"), ("Ⅹ. 당기순이익(손실)", "net")]


@doc("financial_statements", "재무제표(재무상태표·손익계산서)", "corporate")
def financial_statements(p: Profile, rng: random.Random) -> dict:
    """최근 결산 2개년 비교 재무상태표 + 손익계산서 (자산 = 부채 + 자본)."""
    c = p.corporation
    unit_label, unit = rng.choice([("원", 1), ("원", 1), ("천원", 1000)])
    fy = p.issue_date.year - 1 if p.issue_date.month >= 4 else p.issue_date.year - 2
    fy = max(fy, c.established.year + 1)
    term = fy - c.established.year + 1
    rev_cur = round(c.revenue / unit)
    rev_prev = round(rev_cur / rng.uniform(0.88, 1.3))
    cap = c.capital // unit
    inc_prev, inc_cur = _income(rev_prev, rng), _income(rev_cur, rng)
    re0 = int(cap * rng.uniform(0.1, 1.5)) + int(rev_cur * rng.uniform(0.01, 0.2))
    if re0 + inc_prev["net"] <= 0 or re0 + inc_prev["net"] + inc_cur["net"] <= 0:
        re0 += abs(min(inc_prev["net"], inc_prev["net"] + inc_cur["net"])) + cap // 2
    re_prev = re0 + inc_prev["net"]
    re_cur = re_prev + inc_cur["net"]
    bs_prev, bs_cur = _balance(rev_prev, cap, re_prev, rng), _balance(rev_cur, cap, re_cur, rng)

    neg = rng.choice(["paren", "tri", "minus"])

    def fmt(n: int) -> str:
        if n >= 0:
            return f"{n:,}"
        return {"paren": f"({-n:,})", "tri": f"△{-n:,}", "minus": f"-{-n:,}"}[neg]

    def rows(spec, cur, prev):
        return [{"account": a, "current": fmt(cur[k]), "prior": fmt(prev[k])} for a, k in spec]

    prev_start = max(date(fy - 1, 1, 1), c.established)
    return {
        "company_name": c.name,
        "unit": f"(단위 : {unit_label})",
        "current_term": f"제 {term} 기",
        "prior_term": f"제 {term - 1} 기",
        "bs_current_date": f"{fy}년 12월 31일 현재",
        "bs_prior_date": f"{fy - 1}년 12월 31일 현재",
        "is_current_period": f"{fy}년 01월 01일부터 {fy}년 12월 31일까지",
        "is_prior_period": f"{prev_start.year}년 {prev_start.month:02d}월 {prev_start.day:02d}일부터 {fy - 1}년 12월 31일까지",
        "assets": rows(_BS_ASSETS, bs_cur, bs_prev),
        "liabilities": rows(_BS_LIAB, bs_cur, bs_prev),
        "equity": rows(_BS_EQ, bs_cur, bs_prev),
        "total_liabilities_equity": {"current": fmt(bs_cur["liab"] + bs_cur["equity"]),
                                     "prior": fmt(bs_prev["liab"] + bs_prev["equity"])},
        "income_statement": rows(_IS, inc_cur, inc_prev),
    }


# ---------------------------------------------------------------------------
# 5. 법인인감증명서
# ---------------------------------------------------------------------------

@doc("corporate_seal_certificate", "법인인감증명서", "corporate", sample_mark=True)
def corporate_seal_certificate(p: Profile, rng: random.Random) -> dict:
    """등기소 발급 법인 인감증명서."""
    c, fx = p.corporation, _facts(p)
    issued = p.issue_date - timedelta(days=rng.randint(0, 10))
    office = courthouse(c.address)
    return {
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


@doc("board_minutes", "이사회의사록", "corporate")
def board_minutes(p: Profile, rng: random.Random) -> dict:
    """은행 차입 승인 이사회의사록 (출석 이사 기명날인)."""
    c, fx = p.corporation, _facts(p)
    mdate = _weekday(p.issue_date - timedelta(days=rng.randint(1, 20)))
    h, m, dur = _meeting_time(rng)
    end_m = h * 60 + m + dur
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
    signers = [{"title": "의장 대표이사", "name": p.person.name}] + \
        [{"title": "사내이사", "name": o["person"].name} for o in attending[1:]]
    if auditor_present:
        signers.append({"title": "감사", "name": fx["auditor"].name})
    return {
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
        "end_time": _hm(end_m // 60, end_m % 60),
        "minutes_date": D(mdate, "kor_short"),
        "head_office": c.address.road_short,
        "signers": signers,
    }


@doc("shareholders_meeting_minutes", "임시주주총회의사록", "corporate")
def shareholders_meeting_minutes(p: Profile, rng: random.Random) -> dict:
    """임시주주총회의사록 (이사 선임 / 정관 변경 등)."""
    c, fx = p.corporation, _facts(p)
    mdate = _weekday(p.issue_date - timedelta(days=rng.randint(3, 40)))
    h, m, dur = _meeting_time(rng)
    end_m = h * 60 + m + dur
    holders = [(sh, n) for sh, n in p.shareholders]
    total = sum(n for _, n in holders)
    absent = 1 if rng.random() < 0.3 else 0
    present = holders[:len(holders) - absent]
    pshares = sum(n for _, n in present)
    agendas = []
    kinds = rng.sample(["director", "articles", "auditor", "pay"], rng.choice([1, 2, 2]))
    for k in kinds:
        if k == "director":
            d = p.directors[0]
            agendas.append({"title": "이사 선임의 건",
                            "body": f"의장은 사내이사 {d.name}의 임기가 만료됨에 따라 이사를 선임할 필요가 있음을 설명하고 "
                                    f"동인을 사내이사로 중임할 것을 물은 바, 출석주주 전원의 찬성으로 이를 승인 가결하다. "
                                    f"피선임자는 즉석에서 그 취임을 승낙하다.",
                            "detail": f"사내이사  {d.name} ({D(d.birth, 'kor_short')}생)  중임"})
        elif k == "auditor":
            a = fx["auditor"]
            agendas.append({"title": "감사 선임의 건",
                            "body": f"의장은 감사 {a.name}의 임기 만료로 감사를 선임하여야 함을 설명하고 그 선임을 물은 바, "
                                    f"출석주주 전원의 찬성으로 아래 사람을 감사로 선임하다. 피선임자는 즉석에서 취임을 승낙하다.",
                            "detail": f"감사  {a.name} ({D(a.birth, 'kor_short')}생)  중임"})
        elif k == "articles":
            pool = _PURPOSES.get(c.biz_item, [])
            new = rng.choice([x for x in ["전자상거래업", "부동산 임대업", "소프트웨어 개발 및 공급업", "수출입업", "교육 서비스업",
                                          "신재생에너지 발전업"] if x not in fx["purposes"] and x not in pool] or ["신규사업"])
            n = len(fx["purposes"])
            agendas.append({"title": "정관 일부 변경의 건",
                            "body": "의장은 사업 다각화를 위하여 정관 제2조(목적)에 사업목적을 추가할 필요가 있음을 설명하고 "
                                    "아래와 같이 정관을 변경할 것을 물은 바, 출석주주 전원의 찬성으로 원안대로 승인 가결하다.",
                            "detail": f"제2조(목적) 제{n}호 신설: \"{n}. {new}\" (종전 제{n}호는 제{n + 1}호로 이동)"})
        else:
            limit = K.round_to(min(2e9, max(1e8, c.revenue * rng.uniform(0.005, 0.02))), 50_000_000)
            agendas.append({"title": "이사 보수한도 승인의 건",
                            "body": "의장은 당해 사업연도 이사 보수한도액을 아래와 같이 정하고자 함을 설명하고 그 승인을 물은 바, "
                                    "출석주주 전원의 찬성으로 원안대로 승인 가결하다.",
                            "detail": f"이사 보수한도액: 금 {K.won_korean(limit)}원 (₩{limit:,})"})
    for i, a in enumerate(agendas, 1):
        a["no"] = f"제{i}호 의안"
    signers = [{"title": "의장 대표이사", "name": p.person.name}] + \
        [{"title": "사내이사", "name": d.name} for d in p.directors[:rng.randint(1, len(p.directors))]]
    return {
        "company_name": c.name,
        "datetime": f"{D(mdate, 'kor_short')} {_hm(h, m)}",
        "venue": _venue(p, rng),
        "shareholders_total": f"{len(holders)}명",
        "issued_shares": f"{total:,}주",
        "shareholders_present": f"{len(present)}명",
        "shares_present": f"{pshares:,}주",
        "present_ratio": f"{pshares * 100 / total:.2f}%",
        "chair": p.person.name,
        "agendas": agendas,
        "end_time": _hm(end_m // 60, end_m % 60),
        "minutes_date": D(mdate, "kor_short"),
        "head_office": c.address.road_short,
        "signers": signers,
    }


# ---------------------------------------------------------------------------
# 8. 위임장
# ---------------------------------------------------------------------------

_STAFF_POS = ["재무팀 과장", "경영지원팀 대리", "재무팀 차장", "총무팀 부장", "회계팀 과장", "경영지원실 실장", "관리팀 대리"]


@doc("power_of_attorney", "위임장", "corporate")
def power_of_attorney(p: Profile, rng: random.Random) -> dict:
    """은행 여신거래 관련 위임장 (법인 또는 개인 위임인)."""
    c = p.corporation
    corporate = rng.random() < 0.65
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
        grantor = {"type": "개인", "name": p.person.name, "rrn": _mask_any(p.person.rrn, rng),
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
    return {
        "grantor": grantor,
        "agent": {"name": agent.name, "rrn": _mask_any(agent.rrn, rng), "address": agent.address.road_full,
                  "phone": agent.mobile, "relation": relation},
        "tasks": [f"{i}. {t}" for i, t in enumerate(tasks, 1)],
        "period": f"{D(granted, 'dot')} ~ {D(granted + timedelta(days=rng.choice([30, 60, 90])), 'dot')}",
        "grant_date": D(granted, rng.choice(["kor", "kor_short"])),
        "recipient": f"{p.bank} 귀중",
        "attachment": "법인인감증명서 1부" if corporate else "인감증명서 1부",
    }
