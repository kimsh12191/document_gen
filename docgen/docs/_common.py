"""서류 생성 함수들이 공유하는 헬퍼."""
from __future__ import annotations

import random
from datetime import date, timedelta

from .. import korean as K
from ..entities import Address, Person, Profile, rand_date

D = K.fmt_date
won = K.won


def issue_no(rng: random.Random, digits: int = 16, sep: int = 4) -> str:
    """'1234-5678-9012-3456' 형태의 발급번호."""
    s = "".join(str(rng.randint(0, 9)) for _ in range(digits))
    return "-".join(s[i:i + sep] for i in range(0, digits, sep))


def district_office(addr: Address) -> str:
    """주소지 관할 시장/구청장/군수 명칭. 예) '서울특별시 강남구청장'"""
    if not addr.sigungu:
        return f"{addr.sido}장"
    last = addr.sigungu.split()[-1]
    if last.endswith("구"):
        city = addr.sigungu.split()[0] if " " in addr.sigungu else addr.sido
        return f"{city} {last}청장"
    if last.endswith("군"):
        return f"{addr.sido} {last}수"
    return f"{addr.sido} {last}장"


def community_center(addr: Address) -> str:
    return f"{addr.sigungu.split()[-1] if addr.sigungu else addr.sido} {addr.dong}장" if addr.dong.endswith("동") else f"{addr.dong}장"


def tax_office(addr: Address) -> str:
    """관할 세무서명. 예) '역삼세무서장'. 동 이름이 한 글자라 '달세무서장'처럼 되면 '울산남부세무서장' 식으로 바꾼다."""
    base = addr.dong[:-1] if addr.dong.endswith("동") else addr.sigungu.split()[-1][:-1]
    name = f"{base[:2]}세무서장"
    if len(name) >= 6:
        return name
    last = addr.sigungu.split()[-1] if addr.sigungu else addr.sido
    return f"{K.sido_short(addr.sido)}{last[:-1]}{'부' if len(last) == 2 else ''}세무서장"


def courthouse(addr: Address) -> str:
    """관할 등기소명. 예) '서울중앙지방법원 등기국'"""
    m = {"서울특별시": "서울중앙지방법원 등기국", "부산광역시": "부산지방법원 등기국", "대구광역시": "대구지방법원 등기과",
         "인천광역시": "인천지방법원 등기국", "광주광역시": "광주지방법원 등기국", "대전광역시": "대전지방법원 등기국",
         "울산광역시": "울산지방법원 등기과", "세종특별자치시": "대전지방법원 세종등기소", "경기도": "수원지방법원 등기과",
         "강원특별자치도": "춘천지방법원 등기과", "충청북도": "청주지방법원 등기과", "충청남도": "대전지방법원 천안지원 등기계",
         "전북특별자치도": "전주지방법원 등기과", "전라남도": "광주지방법원 순천지원 등기과", "경상북도": "대구지방법원 포항지원 등기과",
         "경상남도": "창원지방법원 등기과", "제주특별자치도": "제주지방법원 등기과"}
    return m[addr.sido]


def recent(rng: random.Random, p: Profile, max_days: int = 25) -> date:
    """발급일 기준 며칠 전 날짜."""
    return p.issue_date - timedelta(days=rng.randint(0, max_days))


def months_back(d: date, n: int) -> date:
    y, m = divmod(d.year * 12 + d.month - 1 - n, 12)
    return date(y, m + 1, 1)


__all__ = ["D", "won", "K", "issue_no", "district_office", "community_center", "tax_office", "courthouse",
           "recent", "months_back", "rand_date", "Person", "Profile", "Address", "date", "timedelta", "random"]
