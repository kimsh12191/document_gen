"""은행 자체 서식 — 수신·고객확인·외환 (계좌개설, 고객확인, 동의서, 해외송금, FATCA/CRS)."""
from ..banks import since
from ..entities import BANK_ACCT_FMT
from ..registry import doc
from ._common import *  # noqa: F401,F403
from .bank_form_loan import _age, _foreigner, _minor, _new_person, _relative, _solo  # 변형용 공용 헬퍼


# ---------------------------------------------------------------------------
# 이 모듈 전용 헬퍼
# ---------------------------------------------------------------------------

def _bank(p: Profile) -> dict:
    return {"name": p.bank}


def _staff_name(rng: random.Random) -> str:
    return K.make_name(rng, rng.choice("MF"))[0]


def _staff(rng: random.Random) -> dict:
    return {"clerk": _staff_name(rng), "manager": _staff_name(rng)}


def _rrn(p: Profile, rng: random.Random, masked_ratio: float = 0.4) -> str:
    return K.mask_rrn(p.person.rrn) if rng.random() < masked_ratio else p.person.rrn


def _new_account_no(bank: str, rng: random.Random) -> str:
    fmt = BANK_ACCT_FMT.get(bank, "###-##-######")
    return "".join(str(rng.randint(0, 9)) if c == "#" else c for c in fmt)


def _occupation(p: Profile, rng: random.Random) -> dict:
    """직업 구분 + (해당 시) 직장명/직위."""
    kind = rng.choices(["급여소득자", "개인사업자", "전문직", "주부", "학생", "무직", "기타"],
                       weights=[70, 14, 5, 5, 1, 2, 3])[0]
    if kind == "학생" and p.person.age > 35:
        kind = "급여소득자"
    if kind in ("급여소득자", "전문직"):
        return {"type": kind, "company": p.employment.company.name, "position": p.employment.position}
    if kind == "개인사업자":
        return {"type": kind, "company": p.business.name, "position": "대표"}
    return {"type": kind}


def _id_type(p: Profile, rng: random.Random) -> str:
    ids = ["주민등록증", "운전면허증", "여권"] + (["모바일신분증"] if since(p.issue_date, "mobile_id") else [])
    return rng.choices(ids, weights=[60, 28, 6, 6][:len(ids)])[0]


def _date(p: Profile, rng: random.Random) -> str:
    return D(p.issue_date, rng.choice(["kor", "kor", "kor_short", "dot"]))


# ---------------------------------------------------------------------------
# 고객확인서 (개인) — 은행 서식명: 고객거래확인서(개인·개인사업자용)
# ---------------------------------------------------------------------------

CDD_JOBS = ["급여소득자", "개인사업자", "전문직", "공무원", "연금소득자", "주부", "학생", "무직", "기타"]
CDD_PURPOSES = ["급여 및 생활비", "저축 및 투자", "보험료 납부결제", "공과금 납부결제", "카드대금 결제",
                "대출원리금 상환결제", "사업상 거래", "기타"]
CDD_FUNDS = ["근로 및 연금소득", "퇴직소득", "사업소득", "부동산임대소득", "부동산양도소득",
             "금융소득(이자 및 배당)", "상속·증여", "일시 재산양도로 인한 소득", "기타"]


@doc("customer_due_diligence", "고객확인서(개인)", "bank_form", category="internal")
def customer_due_diligence(p: Profile, rng: random.Random) -> dict:
    """특정금융정보법 제5조의2에 따른 개인 고객확인(CDD) — 은행 '고객거래확인서(개인·개인사업자용)'."""
    per = p.person
    job = _occupation(p, rng)
    if job["type"] == "주부" and per.gender == "M":
        job = {"type": "무직"}
    if per.age >= 62 and job["type"] in ("무직", "기타") and rng.random() < 0.6:
        job = {"type": "연금소득자"}
    work = {"type": job["type"]}
    if job["type"] in ("급여소득자", "전문직"):
        emp = p.employment
        work.update({"company": emp.company.name, "department": f"{emp.department} / {emp.position}",
                     "industry": emp.company.biz_type, "work_phone": emp.company.phone})
    elif job["type"] == "개인사업자":
        b = p.business
        work.update({"company": b.name, "biz_no": b.biz_no, "opened": D(b.established, "dot"),
                     "industry": f"{b.biz_type} / {b.biz_item}", "work_phone": b.phone})
    fund = {"급여소득자": "근로 및 연금소득", "전문직": "근로 및 연금소득", "연금소득자": "근로 및 연금소득",
            "개인사업자": "사업소득"}.get(job["type"]) or rng.choice(
        ["부동산임대소득", "금융소득(이자 및 배당)", "상속·증여", "기타"])
    if job["type"] == "개인사업자":
        purpose = rng.choice(["사업상 거래", "사업상 거래", "급여 및 생활비", "대출원리금 상환결제"])
    else:
        purpose = rng.choices(CDD_PURPOSES[:6], weights=[50, 20, 5, 8, 9, 8])[0]
    data = {
        "bank": _bank(p),
        "customer": {
            "name": per.name,
            "name_en": per.name_en,
            "rrn": _rrn(p, rng),
            "resident_type": "내국인",
            "gender": "남" if per.gender == "M" else "여",
            "nationality": per.nationality,
            "address": per.address.road_full,
            "mobile": per.mobile,
            "email": per.email,
        },
        "job": work,
        "transaction": {
            "purpose": purpose,
            "fund_source": fund,
            "expected_amount": rng.choices(["1천만원 미만", "1천만원~5천만원", "5천만원~1억원", "1억원 이상"],
                                           weights=[50, 32, 12, 6])[0],
            "frequency": rng.choices(["월 5회 미만", "월 5~10회", "월 10~20회", "월 20회 이상"],
                                     weights=[35, 35, 20, 10])[0],
        },
        "beneficial_owner": "예",
        "pep": "아니오",
        "date": _date(p, rng),
        "signature": per.name,
        "bank_use": {
            "risk_grade": rng.choices(["저위험", "중위험", "고위험"], weights=[70, 26, 4])[0],
            "id_type": _id_type(p, rng),
            "branch": p.bank_branch,
            **_staff(rng),
        },
    }
    _cdd_variants(p, rng, data)
    return data


_EDD_ASSETS = ["5억원 미만", "5억원~10억원", "10억원~30억원", "30억원 이상"]


def _cdd_variants(p: Profile, rng: random.Random, data: dict) -> None:
    """고객확인서(개인) 변형: 강화된 고객확인(EDD) 추가정보(여러 쪽), 외국인, 대리인, 실제소유자 별도, 공란, 체크 누락."""
    per = p.person
    cu = data["customer"]
    if _solo(p) and special(rng, "foreigner", 0.1):  # 외국인 고객 (외국인등록증으로 실명확인)
        fo = _foreigner(p, rng)
        cu.update({"name": fo["name"], "name_en": fo["name_en"], "rrn": fo["arc_no"], "resident_type": "외국인",
                   "gender": "남" if fo["gender"] == "M" else "여", "nationality": fo["nationality"],
                   "mobile": fo["mobile"], "email": fo["email"]})
        data["signature"] = fo["name_en"] if rng.random() < 0.6 else fo["name"]
        data["bank_use"]["id_type"] = rng.choice(["외국인등록증", "여권"])
    if special(rng, "agent", 0.1):  # 대리인 거래
        ag, rel = _relative(p, rng)
        data["agent"] = {"name": ag.name, "rrn": K.mask_rrn(ag.rrn), "relation": rel}
    if special(rng, "not_owner", 0.06):  # 실제소유자가 따로 있는 경우 (예: 부모 자금 관리)
        ow, _ = _relative(p, rng, ("부", "모", "배우자"))
        data["beneficial_owner"] = "아니오"
        data["owner"] = {"name": ow.name, "birth": D(ow.birth, "dot"), "nationality": ow.nationality}
    if heavy(rng, 0.15):  # 고위험 고객: 강화된 고객확인(EDD) 추가정보 → 2쪽
        data["bank_use"]["risk_grade"] = "고위험"
        sal = p.employment.annual_salary
        accts = []
        for _ in range(rng.randint(3, 7)):
            b = rng.choice(["국민은행", "신한은행", "우리은행", "농협은행", "기업은행", "카카오뱅크", "미래에셋증권", "삼성증권"])
            accts.append({"bank": b, "kind": rng.choice(["보통예금", "정기예금", "증권위탁", "외화예금", "적금"]),
                          "purpose": rng.choice(["급여 수령", "생활비", "투자", "사업 결제", "저축", "임대료 수령"])})
        data["edd"] = {
            "annual_income": f"{sal // 10000:,}만원",
            "assets": rng.choices(_EDD_ASSETS, weights=[40, 30, 20, 10])[0],
            "fund_detail": rng.choice([f"{p.employment.company.name} 근로소득 및 상여금", "부동산 매각대금 (매매계약서 제출)",
                                       "부모로부터 증여받은 자금 (증여세 신고서 제출)", "보유 주식 매도대금",
                                       "임대소득 (임대차계약서 제출)"]),
            "purpose_detail": rng.choice(["해외 부동산 취득 자금 송금", "사업자금 결제 및 거래처 대금 지급",
                                          "자녀 해외 유학자금 관리", "고액 현금 입출금 (매장 매출금)", "주식·가상자산 투자자금 이체"]),
            "cash_tx": rng.choice(["해당 없음", "월 1~2회 (1천만원 이상)", "월 3회 이상 (1천만원 이상)"]),
            "overseas_tx": rng.choice(["해당 없음", "있음 (미국)", "있음 (중국)", "있음 (베트남)", "있음 (싱가포르)"]),
            "accounts": accts,
        }
    if special(rng, "sparse", 0.12):  # 선택 항목 미기재
        for k in rng.sample(["email", "name_en"], rng.randint(1, 2)):
            cu[k] = None
    if special(rng, "no_check", 0.08):  # 체크 누락
        data["transaction"][rng.choice(["frequency", "expected_amount", "fund_source"])] = None


# ---------------------------------------------------------------------------
# 고객확인서 (법인·단체)
# ---------------------------------------------------------------------------

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


_INVESTORS = ["한국투자파트너스", "에이티넘인베스트먼트", "KB인베스트먼트", "스틱벤처스", "IBK기업은행", "산업은행",
              "미래에셋벤처투자", "카카오벤처스", "우리사주조합", "신한벤처투자", "LB인베스트먼트", "중소기업진흥공단"]


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


# ---------------------------------------------------------------------------
# 개인(신용)정보 수집·이용·제공·조회 동의서
# ---------------------------------------------------------------------------

_GUARANTORS = ["신용보증기금", "기술보증기금", "한국주택금융공사", "서울보증보험", "지역신용보증재단"]
_MARKETING_CHANNELS = ["전화", "문자메시지", "이메일", "우편", "앱 푸시"]


@doc("privacy_consent", "개인(신용)정보 수집·이용·제공·조회 동의서", "bank_form", category="internal")
def privacy_consent(p: Profile, rng: random.Random) -> dict:
    """여신 금융거래용 개인(신용)정보 동의서 (필수/선택 동의)."""
    guar = rng.sample(_GUARANTORS, rng.randint(2, 4))
    providers = [
        {"name": "신용정보집중기관(한국신용정보원)",
         "purpose": "본인의 신용을 판단하기 위한 자료로 활용하거나 공공기관에서 정책자료로 활용",
         "items": "개인식별정보, 신용거래정보, 신용도판단정보, 신용능력정보, 공공정보",
         "period": "관련 법령 및 규약에서 정한 기간"},
        {"name": rng.choice(["개인신용평가회사(NICE평가정보, 코리아크레딧뷰로)",
                             "NICE평가정보㈜, 코리아크레딧뷰로㈜"]),
         "purpose": "개인신용평가, 본인 실명 및 신용도 확인", "items": "개인식별정보, 신용거래정보, 신용도판단정보",
         "period": "제공 목적 달성 시까지"},
        {"name": ", ".join(guar), "purpose": "보증심사 및 보증서 발급·관리",
         "items": "개인식별정보, 신용거래정보, 신용능력정보", "period": "보증거래 종료일로부터 5년"},
    ]
    m_collect = rng.choice(["동의함", "동의하지 않음"])
    m_provide = rng.choice(["동의함", "동의하지 않음"]) if m_collect == "동의함" else "동의하지 않음"
    channels = sorted(rng.sample(_MARKETING_CHANNELS, rng.randint(1, 4)), key=_MARKETING_CHANNELS.index) \
        if m_collect == "동의함" else []
    if heavy(rng, 0.25):  # 제공받는 자가 많은 동의서 (보증기관·보험사·공공기관 등) → 여러 쪽
        providers += rng.sample(_EXTRA_PROVIDERS, rng.randint(6, len(_EXTRA_PROVIDERS)))
    data = {
        "bank": _bank(p),
        "consent": {
            "collect": "동의함",
            "unique_id": "동의함",
            "provide": "동의함",
            "provide_unique_id": "동의함",
            "inquiry": "동의함",
        },
        "providers": providers,
        "marketing": {"collect": m_collect, "provide": m_provide, "channels": channels},
        "applicant": {"name": p.person.name, "birth": D(p.person.birth, rng.choice(["dot", "kor"]))},
        "date": _date(p, rng),
        "bank_use": {"clerk": _staff_name(rng)},
    }
    if special(rng, "minor", 0.08):  # 미성년자 본인 + 법정대리인(부모) 동의
        kid = _minor(p, rng)
        data["applicant"] = {"name": kid.name, "birth": D(kid.birth, rng.choice(["dot", "kor"]))}
        data["legal_rep"] = {"name": p.person.name, "relation": "부" if p.person.gender == "M" else "모"}
    if special(rng, "marketing_unchecked", 0.12):  # 선택 동의란을 비워 둠 (체크 누락)
        data["marketing"] = {"collect": None, "provide": None, "channels": []}
    return data


_EXTRA_PROVIDERS = [
    {"name": "서울보증보험㈜", "purpose": "보증보험 가입 심사 및 보험금 지급", "items": "개인식별정보, 신용거래정보, 신용능력정보",
     "period": "보험계약 종료일로부터 5년"},
    {"name": "한국주택금융공사", "purpose": "주택금융 보증 심사 및 사후관리", "items": "개인식별정보, 신용거래정보, 주택 보유 정보",
     "period": "보증 종료일로부터 5년"},
    {"name": "주택도시보증공사", "purpose": "전세보증금반환보증 심사 및 관리", "items": "개인식별정보, 임대차 계약 정보",
     "period": "보증 종료일로부터 5년"},
    {"name": "국세청", "purpose": "소득금액증명 등 소득 확인", "items": "성명, 주민등록번호, 소득 자료", "period": "조회 목적 달성 시까지"},
    {"name": "국민건강보험공단", "purpose": "건강보험 자격 및 보험료 납부내역 확인", "items": "성명, 주민등록번호, 직장 및 보험료 정보",
     "period": "조회 목적 달성 시까지"},
    {"name": "국민연금공단", "purpose": "연금보험료 납부내역 확인", "items": "성명, 주민등록번호, 가입 이력", "period": "조회 목적 달성 시까지"},
    {"name": "행정안전부", "purpose": "주민등록 진위 및 전입세대 확인", "items": "성명, 주민등록번호, 주소", "period": "조회 목적 달성 시까지"},
    {"name": "금융결제원", "purpose": "자동이체·CMS 등록 및 어음정보 확인", "items": "성명, 계좌번호, 거래정보", "period": "거래 종료일로부터 5년"},
    {"name": "한국신용정보원 (채무재조정 정보)", "purpose": "신용회복 지원 및 채무조정 여부 확인", "items": "신용도판단정보",
     "period": "관련 법령에서 정한 기간"},
    {"name": "법무법인·법무사 (등기 위임)", "purpose": "근저당권 설정·말소 등기 업무", "items": "성명, 주민등록번호, 주소, 담보물 정보",
     "period": "등기 완료 시까지"},
    {"name": "감정평가법인", "purpose": "담보물 감정평가", "items": "성명, 연락처, 담보물 정보", "period": "평가 완료 후 1년"},
    {"name": "채권추심회사 (위탁 시)", "purpose": "연체채권 회수 업무 위탁", "items": "개인식별정보, 연락처, 신용거래정보",
     "period": "위탁계약 종료 시까지"},
]


# ---------------------------------------------------------------------------
# 예금거래신청서
# ---------------------------------------------------------------------------

_PRODUCTS = {
    "보통예금": ["주거래 우대통장", "급여 우대통장", "생활비 통장", "스마트 입출금통장"],
    "저축예금": ["저축예금", "자유저축예금"],
    "정기예금": ["정기예금(일반)", "e-정기예금", "실속 정기예금"],
    "정기적금": ["자유적립식 적금", "정액적립식 적금", "목돈마련 적금"],
    "주택청약종합저축": ["주택청약종합저축"],
}


@doc("account_opening_application", "예금거래신청서", "bank_form", category="internal")
def account_opening_application(p: Profile, rng: random.Random) -> dict:
    """계좌개설(신규) 신청서 — 상품, 통장, 전자금융, 알림 서비스."""
    per = p.person
    job = _occupation(p, rng)
    ptype = rng.choices(list(_PRODUCTS), weights=[50, 8, 17, 18, 7])[0]
    product = {"type": ptype, "name": rng.choice(_PRODUCTS[ptype])}
    if ptype in ("보통예금", "저축예금"):
        product["amount"] = won(rng.choice([0, 10_000, 10_000, 50_000, 100_000, rng.randint(1, 300) * 10_000]))
    elif ptype == "정기예금":
        product["amount"] = won(rng.randint(5, 200) * 1_000_000)
        product["term"] = rng.choice(["6개월", "12개월", "12개월", "24개월", "36개월"])
        product["interest_payment"] = rng.choices(["만기일시지급", "월이자지급"], weights=[75, 25])[0]
        product["linked_account"] = p.accounts[0].number
    else:
        product["amount"] = won(rng.choice([2, 3, 5, 10, 20, 30, 50, 100]) * 10_000 if ptype == "주택청약종합저축"
                                else rng.randint(1, 30) * 50_000)
        product["term"] = "자유" if ptype == "주택청약종합저축" else rng.choice(["12개월", "24개월", "36개월"])
        product["linked_account"] = p.accounts[0].number
    demand = ptype in ("보통예금", "저축예금")
    internet = rng.choice(["신청", "신청", "미신청"])
    mobile = rng.choice(["신청", "신청", "신청", "미신청"])
    ebank = {"internet": internet, "mobile": mobile}
    if "신청" in (internet, mobile):
        ebank["otp"] = rng.choice(["OTP 발급", "기존 OTP 사용", "보안카드"]
                                  + (["모바일OTP"] if since(p.issue_date, "mobile_otp") else []))
        once = rng.choice([100, 500, 1000, 1000, 5000])
        ebank["limit_once"] = won(once * 10_000)
        ebank["limit_day"] = won(min(once * rng.choice([1, 2, 5]), 5000) * 10_000)
    else:
        ebank["otp"] = "미신청"
    customer = {
        "name": per.name, "name_en": per.name_en, "rrn": _rrn(p, rng, 0.3),
        "address": per.address.road_full, "zipcode": per.address.zipcode,
        "mobile": per.mobile, "email": per.email, "job": job["type"],
    }
    if "company" in job:
        customer["company"] = job["company"]
    data = {
        "bank": _bank(p),
        "customer": customer,
        "product": product,
        "passbook": rng.choice(["발행", "발행", "미발행"]),
        "seal_type": rng.choice(["서명", "서명", "인감", "인감+서명"]),
        "check_card": rng.choice(["신청", "미신청"]) if demand else "미신청",
        "ebank": ebank,
        "alert": rng.choice(["SMS", "앱 푸시", "앱 푸시", "미신청"]),
        "mail_to": rng.choice(["자택", "이메일", "이메일", "수령 안함"] + (["직장"] if "company" in job else [])),
        "salary_transfer": rng.choice(["지정", "미지정"]) if demand and job["type"] in ("급여소득자", "전문직") else "미지정",
        # 예금자보호한도: 2025.9.1.부터 1억원 (이전 5천만원). 주택청약종합저축은 비보호(주택도시기금).
        **({} if ptype == "주택청약종합저축" else
           {"protection_limit": "1억원" if p.issue_date >= date(2025, 9, 1) else "5천만원"}),
        "date": _date(p, rng),
        "signature": per.name,
        "bank_use": {
            "account_no": _new_account_no(p.bank, rng),
            "branch": p.bank_branch,
            "id_type": _id_type(p, rng),
            **_staff(rng),
        },
    }
    _aoa_variants(p, rng, data)
    return data


def _aoa_variants(p: Profile, rng: random.Random, data: dict) -> None:
    """예금거래신청서 변형: 여러 상품 동시 신규(여러 쪽), 미성년자(법정대리인), 대리인, 외국인, 공란."""
    cu = data["customer"]
    if heavy(rng, 0.15):  # 한 번에 여러 계좌 신규 (적금·청약·외화예금 등)
        extra = []
        for _ in range(rng.randint(4, 8)):
            t = rng.choice(["정기적금", "정기예금", "주택청약종합저축", "외화보통예금", "저축예금", "자유적립식 적금"])
            amt = (f"USD {rng.choice([100, 300, 500, 1000]):,}" if t.startswith("외화")
                   else won(rng.choice([10, 20, 30, 50, 100, 300, 500, 1000]) * 10_000))
            extra.append({"type": t, "name": rng.choice(_PRODUCTS.get(t, [t])), "amount": amt,
                          "term": "자유" if t in ("주택청약종합저축", "외화보통예금", "저축예금") else rng.choice(["6개월", "12개월", "24개월", "36개월"]),
                          "account_no": _new_account_no(p.bank, rng)})
        data["extra_products"] = extra
    if special(rng, "minor", 0.1):  # 미성년 자녀 명의 계좌를 부모가 법정대리인으로 개설
        kid = _minor(p, rng)
        cu.update({"name": kid.name, "name_en": kid.name_en, "rrn": K.mask_rrn(kid.rrn) if rng.random() < 0.7 else kid.rrn,
                   "mobile": kid.mobile if _age(p, kid) >= 12 else None, "email": None, "job": "학생" if _age(p, kid) >= 7 else "기타"})
        cu.pop("company", None)
        data["signature"] = kid.name
        data["salary_transfer"] = "미지정"
        if data["mail_to"] in ("이메일", "직장"):
            data["mail_to"] = "자택"
        data["legal_rep"] = {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn),
                             "relation": "부" if p.person.gender == "M" else "모", "phone": p.person.mobile,
                             "documents": rng.choice(["가족관계증명서(상세), 법정대리인 신분증", "기본증명서(상세), 가족관계증명서, 법정대리인 신분증"])}
    elif special(rng, "agent", 0.1):  # 대리인 신규 (위임장·본인 인감증명서 제출)
        ag, rel = _relative(p, rng)
        data["agent"] = {"name": ag.name, "rrn": K.mask_rrn(ag.rrn), "relation": rel, "phone": ag.mobile}
    elif _solo(p) and special(rng, "foreigner", 0.08):  # 외국인 고객
        fo = _foreigner(p, rng)
        cu.update({"name": fo["name"], "name_en": fo["name_en"], "rrn": fo["arc_no"], "mobile": fo["mobile"],
                   "email": fo["email"], "nationality": fo["nationality"]})
        data["signature"] = fo["name"]
        data["bank_use"]["id_type"] = "외국인등록증"
    if special(rng, "sparse", 0.12):  # 선택 항목 미기재
        for k in rng.sample(["email", "name_en", "zipcode"], rng.randint(1, 3)):
            cu[k] = None


# ---------------------------------------------------------------------------
# 금융거래목적확인서
# ---------------------------------------------------------------------------

@doc("financial_transaction_purpose", "금융거래목적확인서", "bank_form", category="internal")
def financial_transaction_purpose(p: Profile, rng: random.Random) -> dict:
    """입출금계좌 신규 시 금융거래 목적과 증빙서류를 확인하는 서식 (대포통장 예방)."""
    per = p.person
    job = _occupation(p, rng)
    if job["type"] in ("급여소득자", "전문직"):
        purpose = rng.choice(["급여계좌"] * 5 + ["공과금 이체", "모임 회비"])
    elif job["type"] == "개인사업자":
        purpose = rng.choice(["사업자 거래"] * 3 + ["공과금 이체"])
    elif job["type"] == "학생":
        purpose = "아르바이트"
    else:
        purpose = rng.choice(["공과금 이체", "모임 회비", "기타"])
    data = {
        "bank": _bank(p),
        "customer": {
            "name": per.name, "rrn": _rrn(p, rng), "address": per.address.road_full,
            "mobile": per.mobile, "job": job["type"],
        },
        "account_type": rng.choice(["보통예금", "보통예금", "저축예금"]),
        "purpose": purpose,
    }
    if "company" in job:
        data["customer"]["company"] = job["company"]
    if purpose == "기타":
        data["purpose_detail"] = rng.choice(["생활비 관리", "연금 수령", "자녀 용돈 관리"])
    data["evidence"] = {
        "급여계좌": lambda: rng.choice(["재직증명서", "근로소득원천징수영수증", "급여명세서", "건강보험 자격득실확인서"]),
        "사업자 거래": lambda: rng.choice(["사업자등록증명", "부가가치세 과세표준증명", "전자세금계산서(공급자용)"]),
        "공과금 이체": lambda: rng.choice(["공과금 납입영수증", "아파트 관리비 고지서"]),
        "모임 회비": lambda: "모임 회칙 및 구성원 명부",
        "아르바이트": lambda: "근로계약서, 고용주 사업자등록증 사본",
    }.get(purpose, lambda: "연금 수급증명서" if data.get("purpose_detail") == "연금 수령" else "가족관계증명서")()
    data["questions"] = {
        "q1": "아니오",
        "q2": "아니오",
        "q3": rng.choices(["아니오", "예"], weights=[80, 20])[0],
    }
    data["date"] = _date(p, rng)
    data["signature"] = per.name
    data["bank_use"] = {
        "result": rng.choices(["일반계좌 개설", "금융거래한도계좌 개설"], weights=[88, 12])[0],
        **_staff(rng),
    }
    if _solo(p) and special(rng, "foreigner", 0.08):  # 외국인 근로자 급여계좌
        fo = _foreigner(p, rng, (22, 45))
        data["customer"].update({"name": fo["name"], "rrn": fo["arc_no"], "mobile": fo["mobile"],
                                 "nationality": fo["nationality"]})
        data["signature"] = fo["name"]
    if special(rng, "no_evidence", 0.1):  # 증빙서류 미제출 → 금융거래한도계좌
        data["evidence"] = None
        data["bank_use"]["result"] = "금융거래한도계좌 개설"
    if special(rng, "no_check", 0.1):  # 확인사항 체크 누락
        data["questions"][rng.choice(["q1", "q2", "q3"])] = None
    return data


# ---------------------------------------------------------------------------
# 해외송금신청서 (당발송금)
# ---------------------------------------------------------------------------

_BANK_ADDR = {
    "BOFAUS3N": "222 Broadway, New York, NY 10038, U.S.A.",
    "CHASUS33": "383 Madison Avenue, New York, NY 10179, U.S.A.",
    "MHCBJPJT": "1-5-5 Otemachi, Chiyoda-ku, Tokyo 100-8176, Japan",
    "BKCHCNBJ": "1 Fuxingmen Nei Dajie, Xicheng District, Beijing, China",
    "BFTVVNVX": "198 Tran Quang Khai St, Hoan Kiem, Hanoi, Vietnam",
    "DEUTDEDD": "Königsallee 45-47, 40212 Düsseldorf, Germany",
    "DBSSSGSG": "12 Marina Boulevard, Marina Bay Financial Centre, Singapore 018982",
}
# 통화별 (가능 통화, 원화 환율 범위, 환율 단위)
_CCY = {"USD": (1340, 1480, 1), "JPY": (880, 990, 100), "EUR": (1450, 1620, 1), "CNY": (185, 205, 1),
        "SGD": (1000, 1100, 1)}
# 옛 은행 서식(2011~2020)용 연평균 매매기준율 근사값 (원, JPY 는 100엔당)
_CCY_YEAR = {
    "USD": {2011: 1108, 2012: 1127, 2013: 1095, 2014: 1053, 2015: 1132, 2016: 1160, 2017: 1131, 2018: 1100, 2019: 1166, 2020: 1180},
    "JPY": {2011: 1391, 2012: 1413, 2013: 1123, 2014: 996, 2015: 935, 2016: 1068, 2017: 1009, 2018: 997, 2019: 1070, 2020: 1106},
    "EUR": {2011: 1541, 2012: 1448, 2013: 1454, 2014: 1398, 2015: 1256, 2016: 1284, 2017: 1276, 2018: 1299, 2019: 1305, 2020: 1345},
    "CNY": {2011: 171, 2012: 179, 2013: 178, 2014: 171, 2015: 180, 2016: 175, 2017: 167, 2018: 166, 2019: 169, 2020: 171},
    "SGD": {2011: 881, 2012: 902, 2013: 875, 2014: 831, 2015: 823, 2016: 840, 2017: 819, 2018: 816, 2019: 855, 2020: 855},
}
_COUNTRY_CCY = {"UNITED STATES": ["USD"], "JAPAN": ["JPY", "JPY", "USD"], "CHINA": ["USD", "USD", "CNY"],
                "VIETNAM": ["USD"], "GERMANY": ["EUR", "EUR", "USD"], "SINGAPORE": ["USD", "SGD"]}
# 한국은행 지급사유코드(5자리) — 검색으로 확인된 코드만 사용 (JPMorgan Korea payment purpose code list)
#   10101 사전송금방식 통관수입대금, 10103 사후송금방식 통관수입대금, 30101 유학 및 연수
_PURPOSE_CODE = {"유학생경비": "30101"}


def _fx_fee(usd_equiv: float) -> int:
    if usd_equiv <= 500:
        return 5_000
    if usd_equiv <= 2_000:
        return 10_000
    if usd_equiv <= 5_000:
        return 15_000
    return 20_000


@doc("overseas_remittance_application", "해외송금신청서", "bank_form", category="internal")
def overseas_remittance_application(p: Profile, rng: random.Random) -> dict:
    """당발송금(전신송금 T/T) 신청서 + 은행 사용란(환율/원화환산액)."""
    per, fo = p.person, p.foreign
    school = "University" in fo.name
    ccy = "USD" if school else rng.choice(_COUNTRY_CCY.get(fo.country, ["USD"]))
    lo, hi, unit = _CCY[ccy]
    if p.issue_date.year in _CCY_YEAR[ccy]:
        avg = _CCY_YEAR[ccy][p.issue_date.year]
        lo, hi = avg * 0.97, avg * 1.03
    rate = round(rng.uniform(lo, hi), 2)
    if school:
        purpose = "유학생경비"
        amount = rng.randint(180, 480) * 100.0
    else:
        purpose = rng.choices(["수입대금", "기타"], weights=[85, 15])[0]
        usd = rng.uniform(3_000, 150_000)
        amount = usd * 1350 / (rate / unit)
    if ccy == "JPY":
        amount = float(K.round_to(amount, 1000))
        amt_str = f"{int(amount):,}"
    else:
        amount = round(amount, 2) if not school else amount
        amt_str = f"{amount:,.2f}"
    krw = int(round(amount * rate / unit))
    fee = _fx_fee(krw / 1350)
    cable = 8_000
    yy = p.issue_date
    if school:
        message = f"TUITION FEE {yy.year} {rng.choice(['FALL', 'SPRING'])} / ID {rng.randint(10_000_000, 99_999_999)}"
        documents = "입학허가서(I-20), 등록금 납부고지서"
    elif purpose == "수입대금":
        message = f"INVOICE NO. {fo.name.split()[0][:3].upper()}-{yy.year}-{rng.randint(1, 999):04d}"
        documents = rng.choice(["Commercial Invoice, 수입계약서", "Commercial Invoice, B/L 사본", "Proforma Invoice"])
        code = "10101" if documents.startswith("Proforma") else "10103"
    else:
        message = f"SERVICE FEE CONTRACT {rng.randint(100, 999)}"
        documents = "용역계약서, Invoice"
    remittance = {
        "currency": ccy,
        "amount": amt_str,
        "purpose": purpose,
        "charge": rng.choices(["SHA", "OUR", "BEN"], weights=[60, 30, 10])[0],
        "method": "전신송금(T/T)",
        "message": message,
        "documents": documents,
    }
    if purpose == "수입대금":
        remittance["purpose_code"] = code
    elif purpose in _PURPOSE_CODE:
        remittance["purpose_code"] = _PURPOSE_CODE[purpose]
    remitter = {"name": per.name, "name_en": per.name_en, "rrn": _rrn(p, rng),
                "address": per.address.road_full, "phone": per.mobile}
    if purpose == "수입대금":
        remitter["company"] = f"{p.business.name} ({p.business.biz_no})"
    data = {
        "bank": _bank(p),
        "remitter": remitter,
        "beneficiary": {
            "name": fo.name, "address": fo.address, "country": fo.country, "account_no": fo.account,
            "relationship": "교육기관(학비 납부)" if school else "거래처",
            "bank_name": fo.bank, "swift": fo.swift, "bank_address": _BANK_ADDR.get(fo.swift, fo.country),
        },
        "remittance": remittance,
        "date": _date(p, rng),
        "signature": per.name,
        "bank_use": {
            "ref_no": f"OR{yy:%y%m%d}{rng.randint(0, 99999):05d}",
            "rate": f"{rate:,.2f}",
            "krw_amount": won(krw),
            "fee": won(fee),
            "cable_fee": won(cable),
            "total": won(krw + fee + cable),
            "branch": p.bank_branch,
            **_staff(rng),
        },
    }
    _remit_variants(p, rng, data, school)
    return data


# 외국인 근로자 본국 송금용 수취은행 (국가: 은행명, SWIFT, 통화)
_HOME_BANKS = {
    "VIETNAM": ("JOINT STOCK COMMERCIAL BANK FOR FOREIGN TRADE OF VIETNAM", "BFTVVNVX", "USD"),
    "CHINA": ("BANK OF CHINA", "BKCHCNBJ", "CNY"),
    "PHILIPPINES": ("BDO UNIBANK, INC.", "BNORPHMM", "USD"),
    "INDONESIA": ("PT BANK NEGARA INDONESIA (PERSERO) TBK", "BNINIDJA", "USD"),
    "THAILAND": ("KASIKORNBANK PUBLIC COMPANY LIMITED", "KASITHBK", "USD"),
    "UZBEKISTAN": ("NATIONAL BANK OF UZBEKISTAN", "NBFAUZ2X", "USD"),
    "MONGOLIA": ("KHAN BANK", "AGMOMNUB", "USD"),
}
_HOME_CITY = {"VIETNAM": "HANOI", "CHINA": "QINGDAO", "PHILIPPINES": "MANILA", "INDONESIA": "JAKARTA",
              "THAILAND": "BANGKOK", "UZBEKISTAN": "TASHKENT", "MONGOLIA": "ULAANBAATAR"}
_HOME_GIVEN = {"VIETNAM": ["THI MAI", "VAN HUNG", "THI LAN", "VAN NAM"], "CHINA": ["MING", "XIU YING", "JUN", "FANG"],
               "PHILIPPINES": ["ROSA", "JOSE", "ANGELICA", "MARK"], "INDONESIA": ["DEWI", "BUDI", "AGUS", "SRI"],
               "THAILAND": ["ANAN", "MALEE", "SOMSAK", "NOK"], "UZBEKISTAN": ["DILNOZA", "BEKZOD", "SHAHNOZA", "RUSTAM"],
               "MONGOLIA": ["TUYA", "BOLD", "SARNAI", "GANZORIG"]}
_BATCH_PARTIES = [
    ("SHENZHEN HUAXIN ELECTRONICS CO., LTD.", "CHINA", "BANK OF CHINA SHENZHEN BRANCH", "BKCHCNBJ45A"),
    ("NINGBO OCEAN TRADING CO., LTD.", "CHINA", "INDUSTRIAL AND COMMERCIAL BANK OF CHINA", "ICBKCNBJNBO"),
    ("SAIGON TEXTILE JSC", "VIETNAM", "VIETCOMBANK HO CHI MINH", "BFTVVNVX007"),
    ("OSAKA PRECISION PARTS K.K.", "JAPAN", "MUFG BANK, LTD.", "BOTKJPJT"),
    ("TOKYO MATERIALS CO., LTD.", "JAPAN", "MIZUHO BANK, LTD.", "MHCBJPJT"),
    ("PACIFIC SUPPLY INC.", "UNITED STATES", "BANK OF AMERICA, N.A.", "BOFAUS3N"),
    ("WEST COAST LOGISTICS LLC", "UNITED STATES", "JPMORGAN CHASE BANK, N.A.", "CHASUS33"),
    ("RHEIN MASCHINENBAU GMBH", "GERMANY", "DEUTSCHE BANK AG", "DEUTDEDD"),
    ("LION CITY COMPONENTS PTE. LTD.", "SINGAPORE", "DBS BANK LTD.", "DBSSSGSG"),
    ("BANGKOK PACKAGING CO., LTD.", "THAILAND", "BANGKOK BANK PCL", "BKKBTHBK"),
    ("MANILA AGRI EXPORTS CORP.", "PHILIPPINES", "BDO UNIBANK, INC.", "BNORPHMM"),
]


def _remit_variants(p: Profile, rng: random.Random, data: dict, school: bool) -> None:
    """해외송금신청서 변형: 여러 건 일괄 송금(별지, 여러 쪽), 외국인 근로자 본국 송금, 대리인, 공란."""
    rem, ben = data["remittance"], data["beneficiary"]
    if not school and heavy(rng, 0.2):  # 거래처 여러 곳에 한 번에 송금 → 별지 송금명세
        rows = []
        for name, country, bank, swift in rng.sample(_BATCH_PARTIES, rng.randint(6, 11)):
            cur = {"JAPAN": "JPY", "GERMANY": "EUR"}.get(country, "USD")
            amt = rng.uniform(2_000, 60_000)
            rows.append({"beneficiary": name, "country": country, "bank": f"{bank} ({swift})",
                         "account_no": "".join(str(rng.randint(0, 9)) for _ in range(rng.choice([10, 12, 14]))),
                         "currency": cur,
                         "amount": f"{int(K.round_to(amt * 140, 1000)):,}" if cur == "JPY" else f"{amt:,.2f}",
                         "message": f"INV {rng.choice(['NO.', ''])}{rng.randint(1000, 9999)}"})
        data["batch"] = rows
        data["batch_count"] = f"{len(rows) + 1}건"
    if _solo(p) and special(rng, "foreign_worker", 0.12):  # 외국인 근로자의 국내 보수 본국 송금
        fo = _foreigner(p, rng, (23, 45), nations=_HOME_BANKS)
        country = fo["nationality_en"]
        bank, swift, cur = _HOME_BANKS[country]
        rel = rng.choice(["배우자", "부", "모", "본인"])
        if rel == "본인":
            bname = fo["name_en"]
        else:
            bname = f"{fo['surname_en']} {rng.choice(_HOME_GIVEN[country])}"
        data["remitter"] = {"name": fo["name"], "name_en": fo["name_en"], "rrn": fo["arc_no"],
                            "address": p.person.address.road_full, "phone": fo["mobile"]}
        data["signature"] = fo["name"]
        data["beneficiary"] = {"name": bname, "address": f"{_HOME_CITY[country]}, {country}", "country": country,
                               "account_no": "".join(str(rng.randint(0, 9)) for _ in range(rng.choice([10, 12, 13]))),
                               "relationship": "본인 명의 본국 계좌" if rel == "본인" else f"가족({rel})",
                               "bank_name": bank, "swift": swift, "bank_address": f"{_HOME_CITY[country]}, {country}"}
        amt = float(rng.randint(50, 250) * 100) if cur == "CNY" else rng.randint(8, 40) * 100.0
        lo, hi, _ = _CCY[cur]
        if p.issue_date.year in _CCY_YEAR[cur]:
            avg = _CCY_YEAR[cur][p.issue_date.year]
            lo, hi = avg * 0.97, avg * 1.03
        rate = round(rng.uniform(lo, hi), 2)
        krw = int(round(amt * rate))
        data["remittance"] = {"currency": cur, "amount": f"{amt:,.2f}", "purpose": "국내보수송금", "charge": "OUR",
                              "method": "전신송금(T/T)", "message": rng.choice(["FAMILY SUPPORT", "SALARY", "FOR FAMILY"]),
                              "documents": "근로계약서, 급여명세서(소득증빙)"}
        data["bank_use"].update({"rate": f"{rate:,.2f}", "krw_amount": won(krw), "fee": won(_fx_fee(krw / 1350)),
                                 "total": won(krw + _fx_fee(krw / 1350) + 8_000)})
        data.pop("batch", None)
        data.pop("batch_count", None)
    elif special(rng, "agent", 0.08):  # 가족이 대리 신청 (위임장 첨부)
        ag, rel = _relative(p, rng)
        data["agent"] = {"name": ag.name, "rrn": K.mask_rrn(ag.rrn), "relation": rel, "phone": ag.mobile}
    if special(rng, "sparse", 0.1):  # 선택 기재란 공란
        for k in rng.sample(["relationship", "address"], rng.randint(1, 2)):
            data["beneficiary"][k] = None


# ---------------------------------------------------------------------------
# 해외금융계좌 납세자 확인서 (FATCA/CRS)
# ---------------------------------------------------------------------------

_OTHER_RES = [("일본 (JAPAN)", "JAPAN"), ("중국 (CHINA)", "CHINA"), ("싱가포르 (SINGAPORE)", "SINGAPORE"),
              ("캐나다 (CANADA)", "CANADA"), ("호주 (AUSTRALIA)", "AUSTRALIA")]


@doc("fatca_crs", "해외금융계좌 납세자 확인서(개인)", "bank_form", category="internal")
def fatca_crs(p: Profile, rng: random.Random) -> dict:
    """FATCA/CRS 본인확인서(개인/개인사업자용) — 국제조세조정법·금융정보자동교환 이행규정에 따른 자기확인서."""
    per = p.person
    kind = rng.choices(["kr", "us", "other"], weights=[88, 6, 6])[0]
    res = []
    birth_place = "대한민국 (KOREA)"
    nationality = "대한민국 (KOREA)"
    if kind == "us":
        category = rng.choice(["미국 시민권자(이중국적자 포함)", "미국 영주권자", "미국 세법상 미국 거주자"])
        res.append({"country": "미국 (U.S.A.)",
                    "tin": f"{rng.randint(100, 665)}-{rng.randint(10, 99)}-{rng.randint(1000, 9999)}"})
        if category.startswith("미국 시민권자"):
            nationality = "대한민국, 미국"
            if rng.random() < 0.6:
                birth_place = "미국 (U.S.A.)"
    elif kind == "other":
        category = "미국 이외의 해외 거주자"
        country = rng.choice(_OTHER_RES)[0]
        reason = rng.choices(["A", "B", "C"], weights=[2, 6, 2])[0]
        r = {"country": country, "no_tin_reason": reason}
        if reason == "B":
            r["reason_detail"] = rng.choice(["단기 체류로 납세자번호 발급 대상 아님", "납세자번호 발급 신청 중"])
        res.append(r)
    else:
        category = "해당사항 없음"
    if kind != "kr" and special(rng, "multi_residence", 0.4):  # 거주관할권이 둘 이상
        for country, _ in rng.sample([x for x in _OTHER_RES if x[0] not in [r["country"] for r in res]], rng.randint(1, 2)):
            r = {"country": country}
            if rng.random() < 0.5:
                r["tin"] = "".join(str(rng.randint(0, 9)) for _ in range(rng.choice([9, 10, 12])))
            else:
                r["no_tin_reason"] = rng.choice(["A", "C"])
            res.append(r)
    data = {
        "bank": _bank(p),
        "holder": {
            "name": per.name,
            "surname_en": per.surname_en,
            "given_en": per.given_en,
            "birth": D(per.birth, rng.choice(["dot", "dash"])),
            "birth_place": birth_place,
            "nationality": nationality,
            "mobile": per.mobile,
            "address": per.address.road_full,
        },
        "residence_category": category,
        "residences": res,
        "date": _date(p, rng),
        "signature": per.name,
        "bank_use": {"branch": p.bank_branch, **_staff(rng)},
    }
    h = data["holder"]
    if _solo(p) and special(rng, "foreigner", 0.08):  # 국내 거주 외국인 (CRS: 본국 세법상 거주자)
        fo = _foreigner(p, rng)
        h.update({"name": fo["name"], "surname_en": fo["surname_en"], "given_en": fo["given_en"],
                  "birth": D(fo["birth"], rng.choice(["dot", "dash"])), "mobile": fo["mobile"],
                  "birth_place": f"{fo['nationality']} ({fo['nationality_en']})",
                  "nationality": f"{fo['nationality']} ({fo['nationality_en']})"})
        data["signature"] = fo["name"]
        if fo["nationality_en"] == "UNITED STATES":
            data["residence_category"] = "미국 시민권자(이중국적자 포함)"
            data["residences"] = [{"country": "미국 (U.S.A.)",
                                   "tin": f"{rng.randint(100, 665)}-{rng.randint(10, 99)}-{rng.randint(1000, 9999)}"}]
        else:
            data["residence_category"] = rng.choice(["미국 이외의 해외 거주자", "해당사항 없음"])
            data["residences"] = [{"country": f"{fo['nationality']} ({fo['nationality_en']})",
                                   "tin": "".join(str(rng.randint(0, 9)) for _ in range(rng.choice([9, 10, 12])))}] \
                if data["residence_category"] != "해당사항 없음" else []
    if special(rng, "no_check", 0.08):  # 해외 거주자 여부 체크 누락 (내국인)
        if data["residence_category"] == "해당사항 없음":
            data["residence_category"] = None
    if special(rng, "sparse", 0.1):  # 선택 기재란 공란
        h[rng.choice(["mobile", "birth_place"])] = None
    return data
