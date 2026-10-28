"""표준 키 사전 초안 docgen/keys.json 을 만든다 (studio 영역 편집기가 키를 고를 때 쓴다).

  python docgen/scripts/build_keys.py

- 재료: guide/fields/fields.json (서식마다 30번 렌더링해 모은 키, docgen/scripts/build_schema.py) 과 docgen/realform.py 의 KEY_RULES.
- 영어 키만 사전에 넣는다. 반복 행 번호는 * 로 묶는다 (rows.3.amount → rows.*.amount).
- 키마다 항목명(한글) 예시, 타입, 쓰는 서식 수, 그룹을 남긴다.
- 같은 뜻인데 이름이 두 벌인 키는 duplicates 에 모은다. 이름을 실제로 바꾸는 일은 평가 세트 버전을 올릴 때 한다
  (studio/DESIGN.md 5.3). 사전을 다시 만들어도 duplicates 의 decision(사람이 정한 것)은 유지한다.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]   # 저장소 최상위
sys.path.insert(0, str(ROOT))

from docgen.realform import KEY_RULES  # noqa: E402
from docgen.schema import LEAF_SYNONYMS  # noqa: E402

FIELDS = ROOT / "guide" / "fields" / "fields.json"
OUT = ROOT / "docgen" / "keys.json"
ASCII = re.compile(r"^[A-Za-z0-9_.]+$")

# 사람이 확인한 이름 두 벌. decision 은 아직 정하지 않은 것은 null.
DUPLICATES = [
    {"keys": ["company.name", "employer.name"],
     "meaning": "직장(회사) 이름",
     "where": "html 재직·소득 서식은 company.* (employee 의 회사), overlay 규칙(realform.KEY_RULES)은 employer.*. "
              "overlay 의 company.* 는 법인·사업자 고객 자신",
     "proposal": "직장은 employer.*, 고객 자신인 법인·사업자는 company.* 로 나눈다 (html 서식의 직장 키를 employer.* 로 바꿈)"},
    {"keys": ["company.address", "employer.address"], "meaning": "직장 주소", "where": "위와 같다",
     "proposal": "위와 같다"},
    {"keys": ["company.phone", "employer.phone"], "meaning": "직장 전화", "where": "위와 같다", "proposal": "위와 같다"},
    {"keys": ["company.corp_reg_no", "company.corp_no"], "meaning": "법인등록번호",
     "where": "overlay 규칙은 corp_no 를 만들지만 라벨에서는 이미 corp_reg_no 로 바뀐다 (schema.LEAF_SYNONYMS)",
     "proposal": "corp_reg_no (이미 통일됨)", "decision": "corp_reg_no"},
    {"keys": ["customer.name", "applicant.name"], "meaning": "신청 고객 성명",
     "where": "overlay 규칙은 고객을 늘 customer.*, html 은행 서식은 신청서마다 applicant.* / holder.* / customer.*",
     "proposal": "서식 안에서의 역할이 다르면(신청인·예금주·차주) 그대로 두고, 같은 역할이면 customer.* 로"},
]


def generic(key: str) -> str:
    """rows.3.amount → rows.*.amount, customer.address2 → customer.address (같은 서식에 두 번째로 나온 칸)."""
    key = re.sub(r"\.\d+(?=\.|$)", ".*", key)
    return re.sub(r"(?<=[a-z_])\d+$", "", key)


def main() -> None:
    fields = json.loads(FIELDS.read_text(encoding="utf-8"))
    acc: dict[str, dict] = defaultdict(lambda: {"labels": Counter(), "types": Counter(), "forms": set(), "groups": set(),
                                                "example": None})
    for doc_id, info in fields.items():
        for k in info.get("keys", []):
            key = generic(k["key"].replace("[]", ""))
            if not ASCII.match(key.replace("*", "0")):
                continue
            a = acc[key]
            if k.get("label"):
                a["labels"][k["label"]] += 1
            a["types"][k.get("type") or "text"] += 1
            a["forms"].add(doc_id)
            a["groups"].add(info.get("group", ""))
            if a["example"] is None and k.get("example"):
                a["example"] = k["example"]
    for rx, key in KEY_RULES:   # overlay 규칙의 키는 렌더링에서 안 나왔어도 넣는다
        a = acc[key]
        a["groups"].add("hana")
        for lab in re.findall(r"[가-힣A-Za-z]+", rx.split("$")[0])[:4]:
            a["labels"][lab] += 0
    keys = []
    for key, a in sorted(acc.items()):
        keys.append({"key": key, "labels": [x for x, _ in a["labels"].most_common(6)],
                     "type": a["types"].most_common(1)[0][0] if a["types"] else "text",
                     "forms": len(a["forms"]), "groups": sorted(g for g in a["groups"] if g),
                     **({"example": a["example"]} if a["example"] else {})})
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    decided = {tuple(d["keys"]): d.get("decision") for d in old.get("duplicates", [])}
    dups = [{**d, "decision": decided.get(tuple(d["keys"]), d.get("decision"))} for d in DUPLICATES]
    out = {"about": "표준 키 사전 초안. docgen/scripts/build_keys.py 가 만든다. 키 형식: snake_case, 역할.속성, 반복 행은 목록.*.칸",
           "synonyms": LEAF_SYNONYMS, "duplicates": dups, "keys": keys}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(keys)}개 키 → {OUT.relative_to(ROOT)} (이름 두 벌 {len(dups)}건)")


if __name__ == "__main__":
    main()
