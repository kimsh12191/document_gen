"""서류별 정답 키 목록(스키마)을 만든다 → guide/fields/fields.json (studio 카탈로그·키 목록의 재료. 키 이름 규칙은 docgen/forms/_common/README.md)

  python docgen/scripts/build_schema.py            # 서류당 프로필 30개로 집계 (--n 으로 바꾼다)

서류를 더하거나 키를 바꾸면 다시 돌린다. 결과 fields.json 은 docgen/scripts/build_keys.py 의 재료다.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]   # 저장소 최상위 (이 파일은 docgen/scripts/)
sys.path.insert(0, str(ROOT))

from docgen.entities import make_profile  # noqa: E402
from docgen.registry import load_all  # noqa: E402
from docgen.render import render  # noqa: E402
from docgen.schema import build_fields  # noqa: E402

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
                                          "n": 0, "example": None, "null": 0, "options": []})
                if k not in seen and not forced:
                    st["n"] += 1
                    seen.add(k)
                st["labels"][f.get("label")] += 1
                st["types"][f["type"]] += 1
                if f["value"] is None and f["type"] not in ("seal", "signature"):
                    st["null"] += 1
                if st["example"] is None and f["value"] is not None:
                    st["example"] = f["value"]
                for o in f.get("options") or []:  # 체크박스 보기 (marks 질문에 그대로 쓴다)
                    if o["text"] not in st["options"]:
                        st["options"].append(o["text"])
        for k in ("DOCGEN_HEAVY", "DOCGEN_SPECIAL"):
            os.environ.pop(k, None)
        schema[spec.id] = {
            "name": spec.name, "group": spec.group,
            "keys": [{"key": k, "label": st["labels"].most_common(1)[0][0], "type": st["types"].most_common(1)[0][0],
                      "fill_rate": round(st["n"] / args.n, 2), "example": st["example"],
                      **({"options": st["options"]} if st["options"] else {})} for k, st in stats.items()],
        }
    out = ROOT / "guide" / "fields"
    out.mkdir(parents=True, exist_ok=True)
    (out / "fields.json").write_text(json.dumps(schema, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(schema)}종 → guide/fields/fields.json")


if __name__ == "__main__":
    main()
