"""금융거래 관련 서류 (은행·카드사 발급).

이 파일에는 그룹 서식들이 같이 쓰는 도우미만 있다. 서식마다 값 만드는 함수(@doc)는 서식 폴더
docgen/forms/<ID>/generate.py 에 있고, 끝의 FORMS 차례로 등록한다.
"""
from ..entities import BANK_ACCT_FMT
from ._common import *  # noqa: F401,F403
from . import income  # noqa: F401  (이 그룹 서식들이 쓰는 income 를 먼저 읽는다 — 서식 등록 차례가 예전과 같게)
from ..registry import register_folder_forms

_CARD_COS = ["신한카드", "삼성카드", "KB국민카드", "현대카드", "롯데카드", "우리카드", "하나카드", "BC카드", "NH농협카드"]
_SHOPS = ["GS25", "CU", "세븐일레븐", "스타벅스", "이마트", "홈플러스", "올리브영", "다이소", "쿠팡", "배달의민족",
          "카카오T", "CGV", "교보문고", "파리바게뜨", "롯데마트", "네이버페이", "11번가", "무신사", "SK에너지", "GS칼텍스"]


def _acct_no(rng: random.Random, bank: str) -> str:
    fmt = BANK_ACCT_FMT.get(bank, "###-##-######")
    return "".join(str(rng.randint(0, 9)) if c == "#" else c for c in fmt)


def _korean_amount(n: int) -> str:
    return f"금 {K.won_korean(n)}원정"


# 이 그룹의 코드 서식. 값 만드는 함수는 서식 폴더 docgen/forms/<ID>/generate.py 에 있다 (여기는 같이 쓰는 도우미).
FORMS = ('bankbook_copy', 'bank_statement', 'balance_certificate', 'debt_certificate', 'card_statement',)
register_folder_forms(__name__, FORMS)   # 예전 @doc 차례 그대로 등록 (서식 목록·데이터셋 순서)
