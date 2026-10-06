"""은행별 서식 표기(브랜드)와 옛 은행 서식(외환은행, KEB하나은행) 지원.

- Brand: 은행별 법인 명칭, 영문명, 서식 대표색, 계좌번호 형식, 서식이 쓰이던 기간(era).
- 옛 은행(era 가 있는 은행)은 지금은 없는 은행이므로 그 은행 서식은 그 시기 날짜로만 만든다.
  bank_view() 가 프로필의 모든 날짜를 그 시기로 옮기고(생년월일·주민번호 포함) 은행을 바꾼다.
- 은행 서식(bank_form 그룹)만 이 은행으로 바뀐다. 외부 발급 서류는 프로필 원래 은행을 쓴다.

근거:
  하나은행 서식 상단 줄  "3-06-1104(14-1) (2025.04 개정) (보존년한 : 완제일로부터 10년)",
                       "3-06-1040(6-1) (210×297) NCR74g/㎡ (2017.02 개정) (보존년한 : 완제일로부터 5년)"
                       결재란 "담당 책임자 관리자 부점장", 약정 상대방 "주식회사 하나은행 앞"
  KEB하나은행(2015.9~2020.1) 서식도 같은 번호 체계 (예: 5-16-0178(2-1) (2016.03 개정))
  구 외환은행 계좌번호 12자리, 하나은행 14자리. 외환은행 SWIFT KOEXKRSE (현 하나은행이 승계)
  외환은행 자체 서식번호 체계는 확인하지 못해 형식만 흉내 낸다 (docs/realism/bank_brands.md).
"""
from __future__ import annotations

import dataclasses
import random
from dataclasses import dataclass
from datetime import date

from . import korean as K
from .entities import BankAccount, Person, Profile, rand_date


@dataclass(frozen=True)
class Brand:
    name: str                  # 서식·GT 에 찍히는 은행명
    legal: str                 # 약정서 "○○ 앞" 법인 명칭
    en: str = ""               # 은행명 옆 작은 영문 (표시 전용)
    swift: str = ""
    accent: str | None = None  # 서식 인쇄색
    acct_fmt: str | None = None
    era: tuple[date, date] | None = None  # 이 은행 이름으로 서식이 쓰인 기간 (옛 은행만)
    family: str = ""           # 서식번호 줄 표기 계열 (hana / keb / 그 외)


BRANDS: dict[str, Brand] = {b.name: b for b in [
    Brand("하나은행", "주식회사 하나은행", "Hana Bank", "KOEXKRSE", "#008485", "###-######-#####", family="hana"),
    # 2015.9.1 하나·외환 통합 → 존속법인 상호 '주식회사 하나은행', 브랜드 'KEB하나은행' (2020.2 '하나은행'으로 변경)
    Brand("KEB하나은행", "주식회사 하나은행", "KEB Hana Bank", "KOEXKRSE", "#008485", "###-######-#####",
          era=(date(2015, 9, 1), date(2020, 1, 31)), family="hana"),
    # 개인정보보호법 시행(2011.9.30) 이후 ~ 통합 전날
    Brand("외환은행", "주식회사 한국외환은행", "Korea Exchange Bank", "KOEXKRSE", "#0a4a9c", "###-######-###",
          era=(date(2011, 10, 4), date(2015, 8, 31)), family="keb"),
    Brand("국민은행", "주식회사 국민은행", "KB Kookmin Bank", "CZNBKRSE", "#5e5446"),
    Brand("신한은행", "주식회사 신한은행", "Shinhan Bank", "SHBKKRSE", "#0046ff"),
    Brand("우리은행", "주식회사 우리은행", "Woori Bank", "HVBKKRSE", "#0067ac"),
    Brand("농협은행", "농협은행 주식회사", "NongHyup Bank", "NACFKRSE", "#14823c"),
    Brand("기업은행", "중소기업은행", "IBK", "IBKOKRSE", "#0d4ea2"),
    Brand("SC제일은행", "주식회사 한국스탠다드차타드은행", "Standard Chartered", "SCBLKRSE", "#0473ea"),
    Brand("부산은행", "주식회사 부산은행", "Busan Bank", "PUSBKR2P", "#d6001c"),
    Brand("iM뱅크", "주식회사 아이엠뱅크", "iM Bank", "DAEBKR22", "#00a19a"),
]}

LEGACY = [k for k, b in BRANDS.items() if b.era]

# 옛 은행 서식으로 만들지 않는 서류 (그 시기에 없던 제도)
#   실제소유자 확인(2016.1~), 금융거래목적확인서(2016~ 전 은행 확대), FATCA(2015.6 협정 발효)·CRS(2017~)
#   적합성·적정성 확인서, 대출상품설명서(권유용): 금융소비자보호법 시행(2021.3.25) 이후 서식
#   대출계약 철회신청서: 은행여신거래기본약관 개정(2016.10.19) 이후 서식
#   사전지정운용방법(디폴트옵션) 지정 신청서: 제도 시행(2022.7.12) 이후 서식 — 두 옛 은행 모두 없다
_FSCA_FORMS = {"suitability_check", "suitability_check_corp", "loan_product_description",
               "investor_profile_retirement"}
_NEW_FORMS = {"default_option_designation"}
LEGACY_EXCLUDE = {
    "외환은행": {"customer_due_diligence", "corporate_customer_due_diligence",
                 "financial_transaction_purpose", "fatca_crs",
                 "loan_withdrawal_request", *_FSCA_FORMS, *_NEW_FORMS},
    "KEB하나은행": {*_FSCA_FORMS, *_NEW_FORMS},
}


def brand(bank: str) -> Brand:
    return BRANDS.get(bank) or Brand(bank, f"주식회사 {bank}")


def supports(bank: str, doc_id: str) -> bool:
    return doc_id not in LEGACY_EXCLUDE.get(bank, set())


# ---------------------------------------------------------------------------
# 서식에 쓸 은행 고르기
# ---------------------------------------------------------------------------

def default_form_bank(p: Profile) -> str | None:
    """--bank 를 주지 않았을 때 은행 서식을 옛 은행으로 만들 고객 (프로필 단위로 고정).
    약 10% 외환은행, 6% KEB하나은행. 시나리오 생성에서는 서류 간 일관성을 위해 쓰지 않는다."""
    if "scenario" in p.extra:
        return None
    x = random.Random(f"form_bank:{p.seed}").random()
    return "외환은행" if x < 0.10 else "KEB하나은행" if x < 0.16 else None


def form_bank(p: Profile, doc_id: str) -> str:
    bank = p.extra.get("form_bank") or default_form_bank(p) or p.bank
    return bank if supports(bank, doc_id) else p.bank


# ---------------------------------------------------------------------------
# 옛 은행: 프로필 날짜를 그 시기로 옮긴다
# ---------------------------------------------------------------------------

def _minus_years(d: date, n: int) -> date:
    try:
        return d.replace(year=d.year - n)
    except ValueError:  # 2/29
        return d.replace(year=d.year - n, day=28)


def _shift(obj, n: int):
    if isinstance(obj, date):
        return _minus_years(obj, n)
    if isinstance(obj, Person):
        birth = _minus_years(obj.birth, n)
        rrn = K.rrn(random.Random(f"rrn:{obj.rrn}"), birth, obj.gender)
        return dataclasses.replace(obj, birth=birth, rrn=rrn, address=_shift(obj.address, n))
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        changes = {}
        for f in dataclasses.fields(obj):
            v = getattr(obj, f.name)
            nv = _shift(v, n)
            if nv is not v:
                changes[f.name] = nv
        return dataclasses.replace(obj, **changes) if changes else obj
    if isinstance(obj, list):
        return [_shift(v, n) for v in obj]
    if isinstance(obj, tuple):
        return tuple(_shift(v, n) for v in obj)
    return obj


def bank_view(p: Profile, bank: str) -> Profile:
    """은행 서식용 프로필. 옛 은행이면 모든 날짜를 그 은행 시기로 옮기고 주거래 계좌도 그 은행 계좌로 바꾼다."""
    if bank == p.bank:
        return p
    b = brand(bank)
    r = random.Random(f"bank_view:{p.seed}:{bank}")
    q = p
    if b.era:
        target = rand_date(r, *b.era)
        q = _shift(p, p.issue_date.year - target.year)
        q = dataclasses.replace(q, issue_date=target)
    fmt = b.acct_fmt or "###-##-######"
    number = "".join(str(r.randint(0, 9)) if c == "#" else c for c in fmt)
    main = q.accounts[0]
    acct = BankAccount(bank, q.bank_branch, number, main.holder,
                       min(main.opened, q.issue_date), main.balance)
    return dataclasses.replace(q, bank=bank, accounts=[acct] + list(q.accounts[1:]),
                               extra={**q.extra, "form_bank": bank})


# ---------------------------------------------------------------------------
# 시기별 제도 (옛 은행 서식에서 그 시기에 없던 문구·항목을 빼는 데 쓴다)
# ---------------------------------------------------------------------------

SINCE = {
    "borrowed_name": date(2014, 11, 29), # 개정 금융실명법 (차명거래 금지 설명 확인)
    "withdraw": date(2016, 10, 19),      # 대출계약 철회권 (은행여신거래기본약관)
    "late_3pct": date(2018, 4, 30),      # 연체가산이자율 연 3%p 상한
    "rate_cut_law": date(2019, 6, 12),   # 금리인하요구권 법정화 (은행법 제30조의2)
    "credinfo_2020": date(2020, 8, 5),   # 개정 신용정보법 (제36조의2 자동화평가 설명요구권 등)
    "credit_score": date(2021, 1, 1),    # 신용등급 → 신용평점
    "fsca": date(2021, 3, 25),           # 금융소비자 보호에 관한 법률 시행
    "mobile_otp": date(2017, 1, 1),
    "mobile_id": date(2022, 1, 1),       # 모바일 신분증으로 실명확인
    "default_option": date(2022, 7, 12), # 퇴직연금 사전지정운용제도(디폴트옵션) 시행
    "irp_expand": date(2017, 7, 26),     # 개인형IRP 가입대상 확대 (자영업자·퇴직금제도 근로자 등)
    "kakao_notice": date(2018, 1, 1),    # 알림톡(LMS) 통지
}


def since(d: date, key: str) -> bool:
    return d >= SINCE[key]


# ---------------------------------------------------------------------------
# 템플릿용: 서식번호 줄의 개정년월
# ---------------------------------------------------------------------------

def form_context(p: Profile, doc_id: str) -> dict:
    """은행 서식 템플릿에 bk 로 넘기는 값 (표시 전용, GT 아님)."""
    b = brand(p.bank)
    issue = p.issue_date
    r = random.Random(f"form_ctx:{p.seed}:{doc_id}:{p.bank}")

    def rev(base: str, sep: str = ".") -> str:
        """기본 개정년월(YYYY.MM)이 작성일보다 늦으면 작성일 이전 날짜로 바꾼다."""
        y, m = int(base[:4]), int(base[5:7])
        if (y, m) >= (issue.year, issue.month):
            k = issue.year * 12 + issue.month - 1 - r.randint(2, 30)
            y, m = divmod(k, 12)
            m += 1
        return f"{y}{sep}{m:02d}"

    comp_year = max(issue.year - r.randint(0, 2), 2012)
    return {
        "name": b.name, "legal": b.legal, "swift": b.swift, "family": b.family,
        "en": b.en if r.random() < (0.8 if b.era else 0.4) else "",  # 은행명 옆 영문 (워드마크 흉내)
        "paper": r.random() < 0.4,  # 서식번호 줄에 용지 규격 표기
        "legacy": bool(b.era), "rev": rev,
        **{k: since(issue, k) for k in SINCE},
        # 하나은행 약정서 하단 "준법감시인심사필 제 2017-약관-0085 호"
        "compliance": f"준법감시인심사필 제 {comp_year}-약관-{r.randint(1, 240):04d} 호" if r.random() < 0.6 else "",
    }


def brand_accent(bank: str, rng: random.Random) -> str | None:
    """서식 인쇄색: 대부분 은행 대표색, 가끔 흑백 인쇄."""
    a = brand(bank).accent
    return a if a and rng.random() < 0.8 else None
