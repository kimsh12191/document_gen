"""표준 키 사전 중 사람이 정하는 부분 — docgen/key_rules.json (studio/DESIGN.md 15.7). studio 키 사전 화면이 고친다.

  synonyms     마지막 키 이름 통일 (dob → birth …). schema.canonical_key 가 쓴다
  label_rules  [정규식, 표준 키] — overlay 항목명(norm 한 것) → 표준 키. 위에서부터 처음 맞는 것 (realform.key_of)
  kind_rules   [정규식, 값 종류] — 표준 키가 아닌 항목명 → 값 종류 (realform.kind_of)
  keys         {표준 키: {meaning, kind, source?, aliases[], labels[], label_suggestions[]}}
               aliases = 외부 추출 결과의 키 이름 (서류 넣기 키 대응), labels = overlay 항목명(그대로 비교, label_rules 다음)
  kinds        {값 종류: {meaning, how: source|choices|pattern, source? | choices? | pattern?}} — 코드로 만드는 종류(CODE_KINDS) 밖의 것

값 만들기 방식: source = 프로필 경로 (foreign.swift …), choices = {값: 가중치}, pattern = # 숫자 · A 대문자 · a 소문자 · {가|나} 고르기.
코드로 만드는 종류(날짜·금액·주민번호처럼 앞뒤 관계나 형식이 있는 것)는 realform.Values 에 그대로 두고 화면에는 설명만 보인다.
"""
from __future__ import annotations

import json
import random
import re
from datetime import date
from pathlib import Path

PATH = Path(__file__).with_name("key_rules.json")

# realform.Values.by_kind 가 코드로 만드는 값 종류 (화면 설명용). 바꾸려면 코드를 고친다.
CODE_KINDS = {
    "text": "자유 글자 (값 출처가 없으면 비움)", "date": "날짜 (만기·기한이면 앞날짜)", "amount": "원화 금액", "fx_amount": "통화 + 외화 금액",
    "percent": "비율·이율", "rate": "환율", "currency": "통화 코드", "account": "국내 계좌번호", "number": "번호·코드", "count": "수량·건수·기간",
    "biz_no": "사업자등록번호", "passport": "여권번호", "check_no": "수표·어음 번호", "goods": "품목", "product": "금융 상품명",
    "check_kind": "수표 종류", "loan_subject": "대출 과목", "repay": "상환 방법", "reason": "사유·목적", "bank": "은행", "branch": "지점",
    "country": "국가", "address": "주소", "email": "이메일", "phone": "전화번호", "company": "회사명", "person": "사람 이름",
    "note": "비고 (해당 없음)", "skip": "값을 쓰지 않는 칸", "seal": "도장·서명 칸",
}
HOW = ("source", "choices", "pattern")
_cache: tuple[float, dict] | None = None


def load() -> dict:
    global _cache
    m = PATH.stat().st_mtime if PATH.exists() else 0.0
    if _cache is None or _cache[0] != m:
        d = json.loads(PATH.read_text(encoding="utf-8")) if PATH.exists() else {}
        for k in ("synonyms", "keys", "kinds"):
            d.setdefault(k, {})
        for k in ("label_rules", "kind_rules"):
            d.setdefault(k, [])
        _cache = (m, d)
    return _cache[1]


def dumps(d: dict) -> str:
    """사람이 읽기 좋게: 규칙·키·종류 하나가 한 줄."""
    def one(x):
        return json.dumps(x, ensure_ascii=False)

    parts = [f' "about": {one(d.get("about", ""))}', f' "synonyms": {one(d["synonyms"])}']
    for k in ("label_rules", "kind_rules"):
        parts.append(f' "{k}": [\n' + ",\n".join(f"  {one(r)}" for r in d[k]) + "\n ]")
    for k in ("keys", "kinds"):
        parts.append(f' "{k}": {{\n' + ",\n".join(f"  {one(n)}: {one(v)}" for n, v in d[k].items()) + "\n }")
    return "{\n" + ",\n".join(parts) + "\n}\n"


def save(d: dict) -> None:
    validate(d)
    tmp = PATH.with_suffix(".tmp")
    tmp.write_text(dumps(d), encoding="utf-8")
    tmp.replace(PATH)
    global _cache
    _cache = None


def validate(d: dict) -> None:
    for rx, _ in d["label_rules"] + d["kind_rules"]:
        re.compile(rx)
    known = set(CODE_KINDS) | set(d["kinds"])
    for name, k in d["kinds"].items():
        if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
            raise ValueError(f"값 종류 이름은 영어 소문자·숫자·밑줄: {name}")
        if name in CODE_KINDS:
            raise ValueError(f"{name} 은 코드로 만드는 종류라 고칠 수 없습니다")
        if k.get("how") not in HOW:
            raise ValueError(f"{name}: how 는 {HOW} 중 하나")
        if k["how"] == "choices" and not (isinstance(k.get("choices"), dict) and k["choices"]
                                         and all(isinstance(w, (int, float)) and w > 0 for w in k["choices"].values())):
            raise ValueError(f"{name}: choices 는 {{값: 양수 가중치}}")
        if k["how"] == "pattern" and not k.get("pattern"):
            raise ValueError(f"{name}: pattern 이 비었습니다")
        if k["how"] == "source" and not k.get("source"):
            raise ValueError(f"{name}: source 가 비었습니다")
    aliases: dict[str, str] = {}
    for key, v in d["keys"].items():
        if not re.fullmatch(r"[a-z][a-z0-9_]*(\.[a-z0-9_*]+)*", key):
            raise ValueError(f"표준 키 형식: 영어 소문자 snake_case, 역할.속성 ({key})")
        if v.get("kind") and v["kind"] not in known:
            raise ValueError(f"{key}: 모르는 값 종류 {v['kind']}")
        for a in v.get("aliases", []):
            if aliases.get(a, key) != key:
                raise ValueError(f"추출 키 {a} 가 {aliases[a]} 와 {key} 둘에 있습니다")
            aliases[a] = key


def alias_index() -> dict[str, str]:
    """추출 키 이름 → 표준 키 (키 자신 포함)."""
    d = load()
    out = {k: k for k in d["keys"]}
    for k, v in d["keys"].items():
        out.update({a: k for a in v.get("aliases", [])})
    return out


def label_index() -> dict[str, str]:
    """overlay 항목명(norm) → 표준 키. label_rules 다음에 본다."""
    return {lab: k for k, v in load()["keys"].items() for lab in v.get("labels", [])}


def resolve_source(profile, path: str):
    """프로필 경로 → 값 (date 는 yyyy.mm.dd). 'profile.' 은 붙여도 되고 안 붙여도 된다."""
    obj = profile
    for part in path.removeprefix("profile.").split("."):
        if obj is None:
            return None
        obj = obj[int(part)] if isinstance(obj, (list, tuple)) and part.isdigit() else getattr(obj, part, None)
    if isinstance(obj, date):
        return obj.strftime("%Y.%m.%d")
    return obj if obj is None or isinstance(obj, (str, int, float)) else str(obj)


def from_pattern(pattern: str, r: random.Random) -> str:
    out = []
    for tok in re.findall(r"\{[^}]*\}|.", pattern):
        if tok.startswith("{") and tok.endswith("}"):
            out.append(r.choice(tok[1:-1].split("|")))
        elif tok == "#":
            out.append(str(r.randint(0, 9)))
        elif tok == "A":
            out.append(chr(r.randint(65, 90)))
        elif tok == "a":
            out.append(chr(r.randint(97, 122)))
        else:
            out.append(tok)
    return "".join(out)


def make_value(kind: str, profile, r: random.Random):
    """데이터로 정한 값 종류의 값 하나. 데이터 종류가 아니면 None (코드 종류는 realform 이 만든다)."""
    k = load()["kinds"].get(kind)
    if not k:
        return None
    if k["how"] == "source":
        return resolve_source(profile, k["source"])
    if k["how"] == "choices":
        vals = list(k["choices"])
        return r.choices(vals, weights=[k["choices"][v] for v in vals])[0]
    return from_pattern(k["pattern"], r)


def profile_sources(profile, prefix: str = "", depth: int = 0) -> list[dict]:
    """화면의 값 출처 고르기: 프로필의 글자·숫자·날짜 경로와 예시 값."""
    import dataclasses

    out = []
    if depth > 3 or profile is None:
        return out
    for f in dataclasses.fields(profile):
        if f.name in ("extra", "seed"):
            continue
        v = getattr(profile, f.name)
        p = f"{prefix}{f.name}"
        if dataclasses.is_dataclass(v):
            out += profile_sources(v, p + ".", depth + 1)
        elif isinstance(v, (str, int, float, date)) and not isinstance(v, bool):
            out.append({"path": p, "example": v.strftime("%Y.%m.%d") if isinstance(v, date) else v})
    return out
