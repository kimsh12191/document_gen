"""채점에 쓰는 비교·거리 함수.

- 모델 출력에서 JSON 꺼내기 (코드 블록·앞뒤 설명이 섞여 있어도)
- 글자 정규화 (NFKC, 공백 제거) 와 편집 거리(CER)
- 값 비교: 정답 필드의 타입에 맞춰 날짜·금액·번호를 정규화해 비교한다.
  예) 정답 '2025년 9월 20일' ↔ 예측 '2025-09-20' 일치, 정답 '금 오억원정 (₩500,000,000)' ↔ 예측 '500000000' 일치
"""
from __future__ import annotations

import json
import re
import unicodedata

from ..schema import infer, korean_number

NULLS = {"", "null", "none", "n/a", "na", "없음", "기재없음", "미기재", "빈칸", "공란", "-", "해당없음"}
YES = {"예", "네", "yes", "y", "true", "o", "있음", "맞음", "맞습니다", "일치", "적합", "충족"}
NO = {"아니오", "아니요", "아니", "no", "n", "false", "x", "없음", "틀림", "불일치", "부적합", "미충족"}


# ---------------------------------------------------------------------------
# 출력 파싱
# ---------------------------------------------------------------------------

def parse_json(text: str | None):
    """모델 출력에서 JSON 값을 꺼낸다. 못 꺼내면 None."""
    if text is None:
        return None
    if not isinstance(text, str):
        return text
    t = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", t, re.S)
    if m:
        t = m.group(1).strip()
    try:
        return json.loads(t)
    except (ValueError, TypeError):
        pass
    for open_, close in (("{", "}"), ("[", "]")):
        i, j = t.find(open_), t.rfind(close)
        if 0 <= i < j:
            try:
                return json.loads(t[i:j + 1])
            except ValueError:
                continue
    return None


def strip_answer(text: str | None) -> str:
    """짧은 답 출력 정리: 코드 블록·따옴표·'답:' 머리말 제거, 여러 줄이면 첫 줄."""
    if text is None:
        return ""
    t = text.strip()
    m = re.search(r"```(?:\w+)?\s*(.*?)```", t, re.S)
    if m:
        t = m.group(1).strip()
    t = re.sub(r"^(?:답|정답|answer|결과)\s*[:：]\s*", "", t, flags=re.I)
    return t.strip().strip("\"'`“”‘’").strip()


# ---------------------------------------------------------------------------
# 글자 정규화·편집 거리
# ---------------------------------------------------------------------------

def norm_text(s) -> str:
    """NFKC + 공백 제거 + 소문자. OCR 비교의 기본 정규화 (한국어 띄어쓰기 차이는 무시)."""
    if s is None:
        return ""
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", str(s))).lower()


def loose_text(s) -> str:
    """norm_text 에서 문장부호까지 뺀 것 (항목명·서류명 비교용)."""
    return re.sub(r"[\W_]+", "", norm_text(s))


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def cer(pred: str, gt: str) -> float:
    """글자 오류율 = 편집 거리 / 정답 길이 (정규화 후). 1 을 넘을 수 있다."""
    p, g = norm_text(pred), norm_text(gt)
    if not g:
        return 0.0 if not p else 1.0
    return levenshtein(p, g) / len(g)


def substring_distance(needle: str, hay: str) -> int:
    """needle 과 hay 의 어떤 부분 문자열 사이의 최소 편집 거리 (Sellers 알고리즘)."""
    if not needle:
        return 0
    if needle in hay:
        return 0
    prev = [0] * (len(hay) + 1)
    for i, cn in enumerate(needle, 1):
        cur = [i] + [0] * len(hay)
        for j, ch in enumerate(hay, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (cn != ch))
        prev = cur
    return min(prev)


# ---------------------------------------------------------------------------
# 값 비교
# ---------------------------------------------------------------------------

def is_null(v) -> bool:
    return v is None or (isinstance(v, str) and norm_text(v) in NULLS) or v == [] or v == {}


def to_number(v) -> float | None:
    """'1,234원', '₩ 5,000', '금 이억원정', '120.5%', 3 → 숫자. 못 읽으면 None."""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if not isinstance(v, str):
        return None
    s = unicodedata.normalize("NFKC", v).strip()
    m = re.search(r"\(\s*[₩\\]?\s*([\d,]+(?:\.\d+)?)\s*원?\s*\)", s)  # '금 오억원정 (₩500,000,000)'
    if m:
        s = m.group(1)
    if (k := korean_number(s)) is not None:
        return float(k)
    mult = 1
    if re.search(r"\d\s*억", s) or re.search(r"\d\s*만\s*원?$", s):  # '3억 2천만원' 같은 혼용 표기
        total, rest = 0.0, s.replace(",", "")
        for num, unit in re.findall(r"(\d+(?:\.\d+)?)\s*(조|억|천만|백만|십만|만|천|백)?", rest):
            total += float(num) * {"조": 1e12, "억": 1e8, "천만": 1e7, "백만": 1e6, "십만": 1e5, "만": 1e4,
                                   "천": 1e3, "백": 1e2}.get(unit, 1)
        return total if total else None
    if re.search(r"천원\s*$", s):
        mult = 1000
    elif re.search(r"백만원\s*$", s):
        mult = 10 ** 6
    nums = re.findall(r"[-+]?\d[\d,]*(?:\.\d+)?", s)
    if len(nums) != 1:
        return None
    try:
        return float(nums[0].replace(",", "")) * mult
    except ValueError:
        return None


_DIGITS_TYPES = {"phone", "rrn", "biz_no", "corp_reg_no", "account_no"}
_NUM_TYPES = {"amount", "amount_korean", "number", "percent"}
_DATE_TYPES = {"date", "month", "datetime"}


def value_match(pred, gt_value, gt_type: str | None = None, gt_norm=None, key: str = "") -> bool:
    """예측값이 정답값과 같은 뜻인지. 정답이 빈 칸(None)이면 예측도 비어 있어야 한다."""
    if gt_value is None:
        return is_null(pred)
    if isinstance(pred, str) and norm_text(pred) == norm_text(gt_value):  # 문서에 실제로 '없음'·'-' 이라고 적힌 칸
        return True
    if is_null(pred):
        return False
    if isinstance(pred, (list, dict)):
        pred = json.dumps(pred, ensure_ascii=False)
    p = str(pred)
    if norm_text(p) == norm_text(gt_value):
        return True
    t = gt_type or "text"
    if t in _NUM_TYPES:
        a = to_number(p)
        b = gt_norm if isinstance(gt_norm, (int, float)) else to_number(gt_value)
        return a is not None and b is not None and abs(a - float(b)) < 1e-6  # 금액은 1원·1센트 차이도 틀림
    if t in _DATE_TYPES:
        pt, pn = infer(key or "date", p)
        gn = gt_norm if gt_norm is not None else infer(key or "date", gt_value)[1]
        return pt in _DATE_TYPES and pn == gn
    if t in _DIGITS_TYPES:
        return re.sub(r"[^\d*]", "", p) == re.sub(r"[^\d*]", "", str(gt_value))
    return loose_text(p) == loose_text(gt_value) and loose_text(p) != ""


def yes_no(v) -> bool | None:
    if isinstance(v, bool):
        return v
    s = norm_text(strip_answer(v) if isinstance(v, str) else v).rstrip(".")
    if s in YES:
        return True
    if s in NO:
        return False
    if s.startswith(("예", "네", "yes")):
        return True
    if s.startswith(("아니", "no")):
        return False
    return None
