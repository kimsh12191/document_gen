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


# 시군구 → 관할 세무서 (주소 데이터에 있는 지역만). 같은 구에 세무서가 여럿이면 동으로 나눈다.
_TAX_OFFICE = {
    ("서울특별시", "강남구"): {"역삼동": "역삼", "삼성동": "삼성", "대치동": "삼성", "개포동": "삼성", "논현동": "강남"},
    ("서울특별시", "서초구"): {"서초동": "서초", "반포동": "반포", "잠원동": "반포", "방배동": "서초"},
    ("서울특별시", "송파구"): {"잠실동": "잠실", "가락동": "송파", "문정동": "송파", "방이동": "잠실"},
    ("서울특별시", "마포구"): "마포", ("서울특별시", "영등포구"): {"여의도동": "영등포", "당산동": "영등포", "문래동": "영등포", "신길동": "영등포"},
    ("서울특별시", "노원구"): "노원", ("서울특별시", "종로구"): "종로", ("서울특별시", "중구"): "중부",
    ("부산광역시", "해운대구"): "해운대", ("부산광역시", "부산진구"): "부산진", ("대구광역시", "수성구"): "수성",
    ("인천광역시", "연수구"): "남인천", ("광주광역시", "서구"): "서광주", ("대전광역시", "유성구"): "북대전",
    ("울산광역시", "남구"): "울산", ("세종특별자치시", ""): "세종", ("경기도", "성남시 분당구"): "분당",
    ("경기도", "수원시 영통구"): "동수원", ("경기도", "고양시 일산동구"): "고양", ("경기도", "용인시 수지구"): "용인",
    ("경기도", "화성시"): "화성", ("강원특별자치도", "춘천시"): "춘천", ("충청북도", "청주시 흥덕구"): "청주",
    ("충청남도", "천안시 서북구"): "천안", ("전북특별자치도", "전주시 완산구"): "전주", ("전라남도", "여수시"): "여수",
    ("경상북도", "포항시 남구"): "포항", ("경상남도", "창원시 성산구"): "창원", ("제주특별자치도", "제주시"): "제주",
}


def tax_office(addr: Address) -> str:
    """관할 세무서장. 예) '역삼세무서장'"""
    v = _TAX_OFFICE.get((addr.sido, addr.sigungu))
    if isinstance(v, dict):
        v = v.get(addr.dong)
    if not v:  # 표에 없는 지역: 시군구 이름으로 대신한다
        last = addr.sigungu.split()[0] if addr.sigungu else addr.sido
        v = last.rstrip("시군구") or last
    return f"{v}세무서장"


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
