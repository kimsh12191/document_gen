"""corporate_customer_due_diligence: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/bank_form_account.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.bank_form_account import _INVESTORS, _bank, _date, _staff  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.docs.bank_form_loan import _new_person, _solo  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("corporate_customer_due_diligence", "고객확인서(법인·단체)", "bank_form", category="internal")
def corporate_customer_due_diligence(p: Profile, rng: random.Random) -> dict:
    """법인 고객확인 + 실제소유자 확인 서식."""
    c = p.corporation
    ceo = c.ceo
    total = sum(n for _, n in p.shareholders) or 1
    owners = []
    for i, (holder, shares) in enumerate(p.shareholders):
        ratio = shares / total * 100
        if ratio < 25:
            continue
        if isinstance(holder, Person):
            owners.append({"name": holder.name, "birth": D(holder.birth, "dot"), "nationality": holder.nationality,
                           "ratio": f"{ratio:.2f}%", "relation": "대표이사" if holder is ceo else "임원(이사)"})
        else:
            owners.append({"name": str(holder), "birth": "-", "nationality": "대한민국",
                           "ratio": f"{ratio:.2f}%", "relation": "주주"})
    owners.sort(key=lambda o: -float(o["ratio"].rstrip("%")))
    same = rng.random() < 0.6
    data = {
        "bank": _bank(p),
        "corp": {
            "name": c.name,
            "name_en": c.name_en,
            "biz_no": c.biz_no,
            "corp_no": c.corp_no or "-",
            "established": D(c.established, rng.choice(["dot", "kor"])),
            "industry": f"{c.biz_type} / {c.biz_item}",
            "hq_address": c.address.road_full,
            "biz_address": "본점과 동일" if same else c.address.road_short,
            "phone": c.phone,
            "email": c.email,
            "corp_type": rng.choices(["중소기업", "대기업"], weights=[95, 5])[0],
            "listed": rng.choices(["비상장", "코넥스", "코스닥"], weights=[92, 4, 4])[0],
        },
        "rep": {
            "name": ceo.name,
            "name_en": ceo.name_en,
            "birth": D(ceo.birth, "dot"),
            "nationality": ceo.nationality,
        },
        "transaction": {
            "purpose": rng.choice(["사업상 거래(결제)", "운영자금 관리", "급여 지급", "대출"]),
            "fund_source": rng.choices(["영업수익", "자본금", "차입금", "투자수익"], weights=[70, 12, 13, 5])[0],
        },
        "owner_step": "1단계",
        "owners": owners,
        "pep": "아니오",
        "date": _date(p, rng),
        "bank_use": {
            "risk_grade": rng.choices(["저위험", "중위험", "고위험"], weights=[60, 34, 6])[0],
            "documents": ["사업자등록증", "법인등기사항전부증명서", "주주명부"]
            + [x for x in ("정관", "법인인감증명서") if rng.random() < 0.5],
            "branch": p.bank_branch,
            **_staff(rng),
        },
    }
    _corp_cdd_variants(p, rng, data)
    return data


def _corp_cdd_variants(p: Profile, rng: random.Random, data: dict) -> None:
    """법인 고객확인서 변형: 주주 다수(여러 쪽), 3단계(대표자) 확인, 거래담당자(대리인), 공란, 체크 누락."""
    c = p.corporation
    if _solo(p) and heavy(rng, 0.25):
        # 투자 유치로 주주가 많은 법인: 별지 주주현황 + 25% 기준 재판정
        holders = [(c.ceo.name, D(c.ceo.birth, "dot"), "대표이사")]
        holders += [(d.name, D(d.birth, "dot"), "이사") for d in p.directors]
        for inv in rng.sample(_INVESTORS, rng.randint(2, 5)):
            holders.append((inv, "-", "주주(법인)"))
        for _ in range(rng.randint(6, 16)):
            x = _new_person(p, rng, None, (28, 65))
            holders.append((x.name, D(x.birth, "dot"), rng.choice(["주주", "주주", "주주(임직원)"])))
        weights = ([rng.uniform(25, 110)] + [rng.uniform(3, 15) for _ in p.directors]
                   + [rng.uniform(4, 15) for _ in range(len(holders) - 1 - len(p.directors))])
        tot_shares = c.capital // 5000
        shares = [max(100, int(tot_shares * w / sum(weights))) for w in weights]
        tot = sum(shares)
        sh = []
        for (name, birth, rel), n in zip(holders, shares):
            sh.append({"name": name, "birth": birth, "shares": f"{n:,}", "ratio": f"{n / tot * 100:.2f}%", "relation": rel})
        sh.sort(key=lambda r: -float(r["ratio"][:-1]))
        data["shareholders"] = sh
        top = [r for r in sh if float(r["ratio"][:-1]) >= 25]
        if top:
            data["owner_step"] = "1단계"
            data["owners"] = [{"name": r["name"], "birth": r["birth"], "nationality": "대한민국", "ratio": r["ratio"],
                               "relation": r["relation"]} for r in top]
        else:  # 25% 이상 주주가 없으면 2단계(최대 지분 소유자)
            r = sh[0]
            data["owner_step"] = "2단계"
            data["owners"] = [{"name": r["name"], "birth": r["birth"], "nationality": "대한민국", "ratio": r["ratio"],
                               "relation": f"최대주주({r['relation']})"}]
    elif special(rng, "step3", 0.1):  # 지분 확인 불가 → 3단계(대표자)
        data["owner_step"] = "3단계"
        data["owners"] = [{"name": c.ceo.name, "birth": D(c.ceo.birth, "dot"), "nationality": c.ceo.nationality,
                           "ratio": "-", "relation": "대표자"}]
    if special(rng, "agent", 0.15):  # 거래담당자(대리인)
        x = _new_person(p, rng, None, (26, 50))
        data["agent"] = {"name": x.name, "rrn": K.mask_rrn(x.rrn),
                         "position": rng.choice(["재무팀 과장", "경리 대리", "경영지원팀 차장", "회계팀 주임"])}
    if special(rng, "sparse", 0.1):
        for k in rng.sample(["name_en", "email"], rng.randint(1, 2)):
            data["corp"][k] = None
        data["rep"]["name_en"] = None
    if special(rng, "no_check", 0.08):
        k = rng.choice(["corp.listed", "transaction.fund_source", "pep"])
        if "." in k:
            data[k.split(".")[0]][k.split(".")[1]] = None
        else:
            data[k] = None
