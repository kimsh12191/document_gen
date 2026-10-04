"""서식 현실화 진행현황 관리.

  python scripts/realism_status.py init     # docs/realism/<담당>.md 표 초기화 (없는 파일만)
  python scripts/realism_status.py build    # docs/REALISM_STATUS.md 집계본 생성

각 담당 파일의 표 한 줄 = 서류 1종. 상태 칸 값:
  대기 / 조사중 / 반영(원본대조) / 반영(검색근거) / 보류
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from docgen.registry import GROUPS, load_all  # noqa: E402

DIR = ROOT / "docs" / "realism"
OWNERS = {  # 담당 파일 → 서류 ID 목록 결정 규칙
    "identity_family": lambda s: s.group in ("identity", "family"),
    "income_finance": lambda s: s.group in ("income", "finance"),
    "tax_business": lambda s: s.group in ("tax", "business"),
    "realestate_fx": lambda s: s.group in ("real_estate", "fx"),
    "corporate": lambda s: s.group == "corporate",
    "bank_loan": lambda s: s.group == "bank_form" and "bank_form_loan" in s.generate.__module__,
    "bank_account": lambda s: s.group == "bank_form" and "bank_form_account" in s.generate.__module__,
}
HEADER = "| 서류 | ID | 근거 서식·출처 | 상태 | 주요 수정 |\n|---|---|---|---|---|\n"
STATES = ["반영(원본대조)", "반영(검색근거)", "조사중", "보류", "대기"]


def init() -> None:
    reg = load_all()
    DIR.mkdir(parents=True, exist_ok=True)
    for owner, pred in OWNERS.items():
        path = DIR / f"{owner}.md"
        if path.exists():
            continue
        rows = [s for s in reg.values() if pred(s)]
        body = "".join(f"| {s.name} | `{s.id}` |  | 대기 |  |\n" for s in rows)
        path.write_text(f"# 서식 현실화 — {owner}\n\n{HEADER}{body}\n## 메모\n\n", encoding="utf-8")
        print(f"{path.relative_to(ROOT)}: {len(rows)}종")


def parse(path: Path) -> list[list[str]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| ") and "`" in line:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cells)
    return rows


def build() -> None:
    reg = load_all()
    all_rows = []
    for owner in OWNERS:
        p = DIR / f"{owner}.md"
        if p.exists():
            all_rows += [(owner, r) for r in parse(p)]
    cnt = Counter(r[3] for _, r in all_rows)
    out = ["# 서식 현실화 진행현황\n",
           "`python scripts/realism_status.py build` 로 `docs/realism/*.md` 를 집계해 만든 파일입니다.\n",
           "| 상태 | 건수 |\n|---|---|"]
    out += [f"| {s} | {cnt.get(s, 0)} |" for s in STATES if cnt.get(s, 0)]
    out.append(f"| **합계** | **{len(all_rows)} / {len(reg)}** |\n")
    by_group: dict[str, list] = {}
    for owner, r in all_rows:
        sid = re.sub(r"[`\s]", "", r[1])
        g = reg[sid].group if sid in reg else "?"
        by_group.setdefault(g, []).append(r)
    for g, title in GROUPS.items():
        rows = by_group.get(g, [])
        if not rows:
            continue
        out.append(f"## {title}\n\n{HEADER.rstrip()}")
        out += ["| " + " | ".join(r) + " |" for r in rows]
        out.append("")
    (ROOT / "docs" / "REALISM_STATUS.md").write_text("\n".join(out), encoding="utf-8")
    print(", ".join(f"{s} {cnt[s]}" for s in STATES if cnt.get(s)), f"/ 총 {len(all_rows)}")


if __name__ == "__main__":
    {"init": init, "build": build}[sys.argv[1]]()
