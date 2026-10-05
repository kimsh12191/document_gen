"""서류별 정답 키 목록(스키마)을 만든다 → docs/SCHEMA.md, schema/schema.json

  python scripts/build_schema.py            # 서류당 프로필 30개로 집계
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from docgen.entities import make_profile  # noqa: E402
from docgen.registry import GROUPS, load_all  # noqa: E402
from docgen.render import render  # noqa: E402
from docgen.schema import LEAF_SYNONYMS, build_fields  # noqa: E402

HEAD = """# 정답 키 스키마

`python scripts/build_schema.py` 로 자동 생성된 문서입니다. 서류별로 프로필 {n}개를 렌더링해 집계했습니다.
기계용 목록은 [schema/schema.json](../schema/schema.json) 에 있습니다.

## 키 규칙

- **형식:** 영어 snake_case, 점(.)으로 중첩합니다. `역할.속성` 순서입니다 (예: `applicant.name`, `company.biz_no`, `loan.amount`).
- **반복 항목:** 리스트 순번이 들어갑니다 (`rows.0.amount`, `rows.1.amount`). 이 문서에서는 `rows[].amount` 로 적습니다.
- **같은 뜻은 같은 속성 이름:** 성명 `name`, 주민번호 `rrn`, 생년월일 `birth`, 성별 `gender`, 주소 `address`, 전화 `phone`/`mobile`,
  사업자번호 `biz_no`, 법인등록번호 `corp_reg_no`, 대표자 `ceo`, 발급일 `issue_date`, 발급기관 `issuer`, 발급번호 `issue_no`.
  내보낼 때 바꾸는 동의어: {syn}
- **도장·서명:** `seal.<자리>` (도장), `sign.<자리>` (서명). 정답 값은 있으면 `true`, 없으면 `false` 입니다.
  자리 이름 예: `issuer` 발급기관 직인, `corp` 법인인감, `applicant` 신청인, `debtor` 채무자, `guarantor` 보증인, `staff.clerk` 담당 행원.
- **빈 칸:** 문서에 항목명은 있는데 값이 비어 있으면 `null` 입니다.
- **체크박스:** 정답 값은 체크된 보기의 글자입니다 (없으면 `null`). 보기 전체와 체크 여부·위치는 라벨의 `options` 에 있습니다.
  복수 선택은 리스트입니다 (`marketing.channels[]`).

## 값 타입

| 타입 | 정규화 값(norm) |
|---|---|
| text | 표시값 그대로 |
| date / month / datetime | `YYYY-MM-DD` / `YYYY-MM` / `YYYY-MM-DDTHH:MM` |
| amount / number / percent | 숫자 (원 단위 정수, 외화는 소수) |
| amount_korean | 한글 금액을 숫자로 (`금 이억일천사백만원정` → 214000000) |
| rrn / biz_no / corp_reg_no | 표시값 그대로 (마스킹 `*` 포함) |
| phone | 숫자만 |
| account_no | 표시값 그대로 |
| checkbox / checkbox_multi | 체크된 보기 |
| seal / signature | `present` (bool) |

"채움률"은 프로필 {n}개 중 그 키가 문서에 나온 비율입니다 (선택 항목·반복 항목은 100% 미만).
채움률 0% 인 키는 드문 변형(내용이 많은 경우·특수 상황)에서만 나오는 키입니다 (변형을 모두 켠 생성에서 수집). 변형 목록은 [docs/variants/](variants/) 에 있습니다.
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=30)
    args = ap.parse_args()
    reg = load_all()
    schema = {}
    for spec in reg.values():
        stats: dict[str, dict] = {}
        # 보통 분포로 n건 (fill_rate) + 긴 경우·특수 상황을 모두 켠 n/3건 (드문 변형 키 수집, fill_rate 에는 안 셈)
        runs = [(seed, False) for seed in range(args.n)] + [(seed, True) for seed in range(max(1, args.n // 3))]
        for seed, forced in runs:
            for k in ("DOCGEN_HEAVY", "DOCGEN_SPECIAL"):
                os.environ.pop(k, None)
            if forced:
                os.environ.update(DOCGEN_HEAVY="1", DOCGEN_SPECIAL="all")
            _, raw, _ = render(spec, make_profile(seed), seed)
            seen = set()
            for f in build_fields(raw):
                k = re.sub(r"\.\d+(?=\.|$)", "[]", f["key"])
                st = stats.setdefault(k, {"labels": collections.Counter(), "types": collections.Counter(),
                                          "n": 0, "example": None, "null": 0})
                if k not in seen and not forced:
                    st["n"] += 1
                    seen.add(k)
                st["labels"][f.get("label")] += 1
                st["types"][f["type"]] += 1
                if f["value"] is None and f["type"] not in ("seal", "signature"):
                    st["null"] += 1
                if st["example"] is None and f["value"] is not None:
                    st["example"] = f["value"]
        for k in ("DOCGEN_HEAVY", "DOCGEN_SPECIAL"):
            os.environ.pop(k, None)
        schema[spec.id] = {
            "name": spec.name, "group": spec.group,
            "keys": [{"key": k, "label": st["labels"].most_common(1)[0][0], "type": st["types"].most_common(1)[0][0],
                      "fill_rate": round(st["n"] / args.n, 2), "example": st["example"]} for k, st in stats.items()],
        }
    (ROOT / "schema").mkdir(exist_ok=True)
    (ROOT / "schema" / "schema.json").write_text(json.dumps(schema, ensure_ascii=False, indent=1), encoding="utf-8")

    syn = ", ".join(f"`{a}`→`{b}`" for a, b in LEAF_SYNONYMS.items())
    lines = [HEAD.format(n=args.n, syn=syn)]
    by_group = collections.defaultdict(list)
    for sid, s in schema.items():
        by_group[s["group"]].append((sid, s))
    for g, title in GROUPS.items():
        if g not in by_group:
            continue
        lines.append(f"\n## {title}\n")
        for sid, s in by_group[g]:
            lines.append(f"\n### {s['name']} (`{sid}`) — 키 {len(s['keys'])}개\n")
            lines.append("| 키 | 항목명 | 타입 | 채움률 | 예시 |\n|---|---|---|---|---|")
            for k in s["keys"]:
                ex = str(k["example"] or "").replace("\n", " ").replace("|", "\\|")
                ex = ex[:40] + "…" if len(ex) > 40 else ex
                lines.append(f"| `{k['key']}` | {k['label'] or ''} | {k['type']} | {k['fill_rate']:.0%} | {ex} |")
    (ROOT / "docs" / "SCHEMA.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(schema)}종 → docs/SCHEMA.md, schema/schema.json")


if __name__ == "__main__":
    main()
