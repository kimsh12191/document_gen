"""financial_statements: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/corporate.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from __future__ import annotations

from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.corporate import PAR_VALUE, _facts, _split, _weekday  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


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
