"""정답 필드의 타입·정규화 값·통일 키, 그리고 렌더러가 잰 위치(bbox)를 합쳐 최종 라벨을 만든다.

라벨 필드 형식 (labels/*.json 의 fields 원소):
  {"key": 통일 키, "label": 문서의 항목명, "type": 타입, "value": 화면 표시값(빈 칸이면 null),
   "norm": 정규화 값, "page": 쪽 번호(0부터), "bbox": 값 위치, "label_bbox": 항목명 위치,
   "options": [{"text", "checked", "box_bbox", "bbox"}],          체크박스
   "present": bool, "kind": 도장 종류, "anchor": 관련 값의 키}     도장·서명
좌표는 이미지 픽셀 [x0, y0, x1, y1] (해당 쪽 왼쪽 위 기준).

타입: text, date, month, datetime, amount, amount_korean, number, percent, rrn, biz_no, corp_reg_no,
      phone, account_no, checkbox, checkbox_multi, seal, signature
"""
from __future__ import annotations

import re
from datetime import date

# ---------------------------------------------------------------------------
# 키 통일: 서류마다 다르게 붙은 같은 뜻의 마지막 키 이름을 하나로 맞춘다.
# 규칙: 영어 snake_case, 역할(applicant/employee/company ...) 아래에 속성(name/rrn/address ...).
# ---------------------------------------------------------------------------
LEAF_SYNONYMS = {
    "dob": "birth",
    "date_of_birth": "birth",
    "sex": "gender",
    "corp_no": "corp_reg_no",
    "ceo_name": "ceo",
    "tel": "phone",
}


def canonical_key(key: str) -> str:
    parts = key.split(".")
    parts[-1] = LEAF_SYNONYMS.get(parts[-1], parts[-1])
    return ".".join(parts)


# ---------------------------------------------------------------------------
# 타입 추론 + 정규화
# ---------------------------------------------------------------------------
_MONTHS = {m: i + 1 for i, m in enumerate(["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"])}
_RE_DATE = re.compile(r"^\s*(\d{4})\s*[.\-/년]\s*(\d{1,2})\s*[.\-/월]\s*(\d{1,2})\s*[.일]?\s*$")
_RE_DATE_SHORT = re.compile(r"^\s*(\d{2})\.(\d{2})\.(\d{2})\.?\s*$")  # 25.03.02
_RE_MONTH = re.compile(r"^\s*(\d{4})\s*[.\-/년]\s*(\d{1,2})\s*월?\.?\s*$")
_RE_DATETIME = re.compile(r"^\s*(\d{4})\s*[.\-/년]\s*(\d{1,2})\s*[.\-/월]\s*(\d{1,2})\s*[.일]?\s*(\d{1,2})\s*[:시]\s*(\d{2})")
_RE_EN1 = re.compile(r"^\s*(\d{1,2})\s+([A-Za-z]{3})[A-Za-z]*\.?\s+(\d{4})\s*$")  # 03 MAR 2025
_RE_US = re.compile(r"^\s*(\d{1,2})/(\d{1,2})/(\d{4})\s*$")  # 03/19/2025
_RE_KAMT_PAREN = re.compile(r"^(?:일금|금)?\s*[가-힣]+원(?:정|整)?\s*\(\s*(?:₩|\\)?\s*([\d,]+)\s*원?\s*\)$")
_CUR = "USD|EUR|JPY|CNY|KRW|GBP|SGD|VND|HKD|AUD|CAD"
_RE_EN2 = re.compile(r"^\s*([A-Za-z]{3})[A-Za-z]*\.?\s+(\d{1,2}),?\s+(\d{4})\s*$")  # March 3, 2025
_RE_RRN = re.compile(r"^\d{6}-[\d*]{7}$")
_RE_BIZ = re.compile(r"^\d{3}-\d{2}-\d{5}$")
_RE_CORP = re.compile(r"^\d{6}-\d{7}$")
_RE_PHONE = re.compile(r"^(?:\(?0\d{1,2}\)?[-\s.]?\d{3,4}[-\s.]\d{4}|1[5-9]\d{2}-\d{4})$")
_RE_NUM = re.compile(r"^[₩$€¥£]?\s*[-+]?\d{1,3}(?:,\d{3})+(?:\.\d+)?$|^[₩$€¥£]?\s*[-+]?\d+(?:\.\d+)?$")
_RE_AMOUNT = re.compile(rf"^(?:(?:{_CUR})\s*|[₩$€¥£]\s*|금\s*)?[-+]?\d{{1,3}}(?:,\d{{3}})*(?:\.\d+)?\s*(?:원(?:정|整)?|천원|백만원|{_CUR})?$")
_RE_PERCENT = re.compile(r"^(?:연\s*)?[-+]?\d+(?:\.\d+)?\s*%$")

_AMOUNT_KEYS = ("amount", "price", "salary", "wage", "pay", "tax", "balance", "fee", "deposit", "income", "revenue",
                "capital", "total", "sum", "cost", "charge", "credit", "debit", "limit", "value", "payment", "bonus",
                "allowance", "deduction", "principal", "interest", "loan", "assets", "liabilities", "equity", "profit",
                "expense", "rent", "duty", "vat", "krw", "usd", "cash", "max", "down", "middle", "base")
_ACCOUNT_KEYS = ("account", "account_no", "passbook_no", "loan_account", "debit_account", "linked_account", "deposit_account")


def _iso(y: int, m: int, d: int) -> str | None:
    try:
        return date(y, m, d).isoformat()
    except ValueError:
        return None


_KDIG = {"영": 0, "일": 1, "이": 2, "삼": 3, "사": 4, "오": 5, "육": 6, "칠": 7, "팔": 8, "구": 9}
_KSMALL = {"십": 10, "백": 100, "천": 1000}
_KBIG = {"만": 10 ** 4, "억": 10 ** 8, "조": 10 ** 12}


def korean_number(s: str) -> int | None:
    """'금 이억일천사백만원정' → 214000000. 한글 숫자가 아니면 None."""
    body = re.sub(r"^(?:일금|금)\s*|\s|원(?:정|整)?$|정$|整$", "", s)
    if not body or any(c not in _KDIG and c not in _KSMALL and c not in _KBIG for c in body):
        return None
    if not any(c in _KSMALL or c in _KBIG for c in body):  # '사원' 같은 단어 제외
        return None
    total = section = num = 0
    for c in body:
        if c in _KDIG:
            num = _KDIG[c]
        elif c in _KSMALL:
            section += (num or 1) * _KSMALL[c]
            num = 0
        else:
            section += num
            total += (section or 1) * _KBIG[c]
            section = num = 0
    return total + section + num


def _number(s: str) -> int | float | None:
    t = re.sub(r"[^\d.\-+]", "", s)
    if not t or t in "-+.":
        return None
    try:
        v = float(t)
    except ValueError:
        return None
    return int(v) if v == int(v) and "." not in t else v


def infer(key: str, value: str | None, typ: str | None = None) -> tuple[str, object]:
    """(타입, 정규화 값). 정규화가 의미 없으면 norm 은 value 그대로."""
    if typ in ("checkbox", "checkbox_multi", "seal", "signature"):
        return typ, value
    if value is None:
        return typ or _type_from_key(key), None
    v = value.strip()
    leaf = key.split(".")[-1]
    if m := _RE_DATETIME.match(v):
        y, mo, d, hh, mm = map(int, m.groups())
        iso = _iso(y, mo, d)
        if iso:
            return "datetime", f"{iso}T{hh:02d}:{mm:02d}"
    if m := _RE_DATE.match(v):
        iso = _iso(*map(int, m.groups()))
        if iso:
            return "date", iso
    if m := _RE_EN1.match(v):
        d, mon, y = m.groups()
        if mon.upper() in _MONTHS and (iso := _iso(int(y), _MONTHS[mon.upper()], int(d))):
            return "date", iso
    if m := _RE_EN2.match(v):
        mon, d, y = m.groups()
        if mon.upper() in _MONTHS and (iso := _iso(int(y), _MONTHS[mon.upper()], int(d))):
            return "date", iso
    if m := _RE_US.match(v):
        mo, d, y = map(int, m.groups())
        if iso := _iso(y, mo, d):
            return "date", iso
    if (m := _RE_DATE_SHORT.match(v)) and "date" in leaf:
        y, mo, d = map(int, m.groups())
        if iso := _iso(2000 + y if y < 50 else 1900 + y, mo, d):
            return "date", iso
    if m := _RE_MONTH.match(v):
        y, mo = map(int, m.groups())
        if 1 <= mo <= 12:
            return "month", f"{y}-{mo:02d}"
    if _RE_RRN.match(v) and leaf not in ("corp_reg_no", "corp_no", "reg_no"):
        return "rrn", v
    if _RE_BIZ.match(v):
        return "biz_no", v
    if _RE_CORP.match(v):
        return "corp_reg_no", v
    if _RE_PHONE.match(v) and "account" not in leaf:
        return "phone", re.sub(r"\D", "", v)
    if ((any(a == leaf or leaf.endswith("_" + a) for a in _ACCOUNT_KEYS) or leaf.startswith("account"))
            and re.search(r"\d{2,}-\d+|\d{8,}", v)):
        return "account_no", v
    if _RE_PERCENT.match(v):
        return "percent", _number(v)
    if m := _RE_KAMT_PAREN.match(v):
        return "amount", _number(m.group(1))
    if (k := korean_number(v)) is not None and ("원" in v or v.startswith("금") or "korean" in leaf or "words" in leaf):
        return "amount_korean", k
    if _RE_AMOUNT.match(v) and ("원" in v or "₩" in v or re.search(_CUR, v)
                                or any(a in leaf for a in _AMOUNT_KEYS)):
        return "amount", _number(v)
    if _RE_NUM.match(v):
        return "number", _number(v)
    return typ or "text", v


def _type_from_key(key: str) -> str:
    leaf = key.split(".")[-1]
    if "date" in leaf or leaf in ("birth", "opened", "maturity"):
        return "date"
    if any(a in leaf for a in _AMOUNT_KEYS):
        return "amount"
    if leaf in ("rrn",):
        return "rrn"
    if leaf in ("phone", "mobile", "fax") or leaf.endswith("_phone"):
        return "phone"
    return "text"


# ---------------------------------------------------------------------------
# 렌더 정보 + 기록 필드 → 최종 라벨 필드
# ---------------------------------------------------------------------------

def _norm_label(t: str) -> str:
    return re.sub(r"[\s\W_①-⑳\d]+", "", t or "").lower()


def similar_label(label: str | None, text: str | None) -> bool:
    """문서에서 찾은 항목명 후보(text)가 기록된 항목명(label)과 같은 말인지 (공통 부분 문자열 2자 이상)."""
    a, b = _norm_label(label), _norm_label(text)
    if not a or not b:
        return False
    if a in b or b in a:
        return True
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    return any(short[i:i + 2] in long_ for i in range(len(short) - 1))


def _first(items: list[dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for it in items:
        out.setdefault(it["key"], it)
    return out


def build_fields(fields: list[dict], info: dict | None = None) -> list[dict]:
    """FieldRecorder 기록에 타입·정규화 값·통일 키·위치를 붙인다. info 는 ImageRenderer.render() 결과 (없으면 위치 생략)."""
    pos = _first(info["fields"]) if info else {}
    labels = _first(info["labels"]) if info else {}
    auto = _first(info.get("auto_labels", [])) if info else {}
    boxes = _first(info["boxes"]) if info else {}
    opts = _first(info.get("opts", [])) if info else {}
    marks = _first(info["marks"]) if info else {}
    out = []
    for f in fields:
        k = f["key"]
        typ, norm = infer(k, f["value"], f.get("type"))
        rec = {"key": canonical_key(k), "label": f.get("label"), "type": typ, "value": f["value"]}
        if typ not in ("seal", "signature", "checkbox_multi"):
            rec["norm"] = norm
        if f.get("group_only"):
            rec["group"] = True
        if typ in ("seal", "signature"):
            rec["present"] = f["present"]
            for x in ("kind", "anchor"):
                if f.get(x):
                    rec[x] = canonical_key(f[x]) if x == "anchor" else f[x]
            if info and k in marks:
                rec["page"], rec["bbox"] = marks[k]["page"], marks[k]["bbox"]
        elif info:
            p = pos.get(k)
            if p:
                rec["page"], rec["bbox"] = p["page"], p["bbox"]
            lab = labels.get(k) or labels.get(re.sub(r"\.\d+(?=\.|$)", ".*", k))
            if lab is None and k in auto and (auto[k].get("src") == "th" or similar_label(f.get("label"), auto[k].get("text"))):
                lab = auto[k]
            if lab and (p is None or lab["page"] == p["page"]):
                rec["label_bbox"] = lab["bbox"]
                rec.setdefault("page", lab["page"])
        if f.get("options"):
            rec["options"] = []
            for i, o in enumerate(f["options"]):
                oo = dict(o)
                if f"{k}#{i}" in boxes:
                    oo["box_bbox"] = boxes[f"{k}#{i}"]["bbox"]
                    rec.setdefault("page", boxes[f"{k}#{i}"]["page"])
                if f"{k}#{i}" in opts:
                    oo["bbox"] = opts[f"{k}#{i}"]["bbox"]
                rec["options"].append(oo)
        out.append(rec)
    if info:  # 키 없이 그려진 도장 (템플릿에서 m.seal 을 안 거친 것)
        for i, s in enumerate(info.get("untagged_seals", [])):
            out.append({"key": f"seal.untagged{i + 1}", "label": None, "type": "seal", "value": s["text"],
                        "present": True, "kind": "직인" if s["square"] else "도장", "page": s["page"], "bbox": s["bbox"]})
    return out


def gt_from_fields(fields: list[dict]) -> dict:
    """라벨 필드 → 중첩 정답 JSON (통일 키 기준). 도장·서명은 bool, 빈 칸은 null."""
    from .render import to_nested

    return to_nested([{**f, "type": f["type"]} for f in fields])
