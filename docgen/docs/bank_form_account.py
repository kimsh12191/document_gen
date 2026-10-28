"""은행 자체 서식 — 수신·고객확인·외환 (계좌개설, 고객확인, 동의서, 해외송금, FATCA/CRS).

이 파일에는 그룹 서식들이 같이 쓰는 도우미만 있다. 서식마다 값 만드는 함수(@doc)는 서식 폴더
docgen/forms/<ID>/generate.py 에 있고, 끝의 FORMS 차례로 등록한다.
"""
from ..banks import since
from ._common import *  # noqa: F401,F403
from . import bank_form_loan  # noqa: F401  (이 그룹 서식들이 쓰는 bank_form_loan 를 먼저 읽는다 — 서식 등록 차례가 예전과 같게)
from ..registry import register_folder_forms


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

CDD_PURPOSES = ["급여 및 생활비", "저축 및 투자", "보험료 납부결제", "공과금 납부결제", "카드대금 결제",
                "대출원리금 상환결제", "사업상 거래", "기타"]


# ---------------------------------------------------------------------------
# 고객확인서 (법인·단체)
# ---------------------------------------------------------------------------


_INVESTORS = ["한국투자파트너스", "에이티넘인베스트먼트", "KB인베스트먼트", "스틱벤처스", "IBK기업은행", "산업은행",
              "미래에셋벤처투자", "카카오벤처스", "우리사주조합", "신한벤처투자", "LB인베스트먼트", "중소기업진흥공단"]


# ---------------------------------------------------------------------------
# 개인(신용)정보 수집·이용·제공·조회 동의서
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 예금거래신청서
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 금융거래목적확인서
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 해외송금신청서 (당발송금)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 해외금융계좌 납세자 확인서 (FATCA/CRS)
# ---------------------------------------------------------------------------


# 이 그룹의 코드 서식. 값 만드는 함수는 서식 폴더 docgen/forms/<ID>/generate.py 에 있다 (여기는 같이 쓰는 도우미).
FORMS = ('customer_due_diligence', 'corporate_customer_due_diligence', 'privacy_consent', 'account_opening_application', 'financial_transaction_purpose', 'overseas_remittance_application', 'fatca_crs',)
register_folder_forms(__name__, FORMS)   # 예전 @doc 차례 그대로 등록 (서식 목록·데이터셋 순서)
