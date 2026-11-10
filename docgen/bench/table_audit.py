"""표 점검 목록: 서식마다 표(반복 묶음)를 여러 seed 로 그려 보고 사람이 정할 것을 모은다 (guide/reference/benchmark.md 표의 정의).

  python -m docgen.bench.table_audit [--seeds 12] [--workers 4] [--out guide/reference/table-audit.md]

그림은 그리지 않는다 (템플릿만 렌더링해 칸 키·값을 본다). 서식마다 표 묶음별로:
  - 행 수 (seed 마다 최소~최대). 늘 같으면 "개수 고정" — 정해진 격자면 questions.json {"table": {"<묶음>": {"ask": false}}} 로 kie 에
  - 행 순서: 날짜 열이 있으면 오래된 순(asc) / 최신순(desc) / 섞임. 실서류와 다르면 그 서식의 generate.py 를 고친다
  - 표 안 합계 열 (항목명 합계·소계·총계): 표가 아니라 kie 칸이어야 함
  - 표 제목: questions.json 에 적힌 것 (없으면 머리글·위치로 가리킴)
그리고 표로 묶이지 않는 것:
  - 번호를 이름에 붙인 반복 칸 (guarantor1.name·guarantor2.name, 원본 서식의 Fund·Fund2·Fund3): 표 후보 — 키를 rows.0.x 꼴로 바꿔야 표가 된다
  - 겹친 목록 (items.0.specs.1.no): 묻지 않는다
결과는 사람이 보고 정한다. 이 목록은 아무것도 고치지 않는다.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOTAL = re.compile(r"합계|소계|총계|총액|^계$")
NUMBERED = re.compile(r"^(.*?[A-Za-z가-힣_])(\d+)((?:\..+)?)$")


def _date(v):
    from .metrics import infer

    t, n = infer("date", str(v)) if v else (None, None)
    return n if t in ("date", "datetime") and isinstance(n, str) else None


def audit_form(args) -> dict:
    """서식 하나: {"id", "name", "group", "tables": {묶음: {...}}, "numbered": [...], "nested": [...]}"""
    doc_id, seeds = args
    from .. import formquestions as FQ
    from ..entities import make_profile
    from ..registry import load_all
    from ..render import render
    from .tasks import MARK_TYPES, table_cell

    spec = load_all()[doc_id]
    tcfg = (FQ.read(doc_id) or {}).get("table") or {}
    groups: dict = defaultdict(lambda: {"rows": [], "orders": [], "columns": {}, "totals": set()})
    numbered: dict = defaultdict(set)
    nested: set = set()
    for k in range(seeds):
        seed = 1_000_000 + k
        try:
            _, raw, _ = render(spec, make_profile(seed), seed)
        except Exception as exc:  # noqa: BLE001  서식 하나가 안 그려져도 목록은 만든다
            return {"id": doc_id, "name": spec.name, "group": spec.group, "error": f"{type(exc).__name__}: {exc}"}
        multi = {f["key"] for f in raw if f.get("group_only")}
        rows: dict = defaultdict(dict)
        for f in raw:
            if f.get("type") in MARK_TYPES or f.get("group_only") or f["key"].startswith(("seal.", "sign.")):
                continue
            tc = table_cell(f["key"])
            if tc is None:
                m = NUMBERED.match(f["key"])
                if m:
                    numbered[m.group(1) + "#" + m.group(3)].add(int(m.group(2)))
                continue
            if tc[1] < 0:
                nested.add(FQ.pattern(f["key"]))
                continue
            g, i, col = tc
            if g in multi:
                continue
            rows[g].setdefault(i, {})[col] = f.get("value")
            groups[g]["columns"].setdefault(col, f.get("label"))
            if f.get("label") and TOTAL.search(f["label"]):
                groups[g]["totals"].add(col)
        for g, rs in rows.items():
            filled = [r for _, r in sorted(rs.items()) if any(v is not None for v in r.values())]
            groups[g]["rows"].append(len(filled))
            dcol = next((c for c in groups[g]["columns"] if sum(1 for r in filled if _date(r.get(c))) >= 2), None)
            if dcol and len(filled) >= 3:
                ds = [d for d in (_date(r.get(dcol)) for r in filled) if d]
                groups[g]["orders"].append("asc" if ds == sorted(ds) else "desc" if ds == sorted(ds, reverse=True) else "mixed")
    tables = {}
    for g, v in groups.items():
        counts = v["rows"] + [0] * (seeds - len(v["rows"]))   # 표가 안 나온 seed 는 0 행
        orders = sorted(set(v["orders"]))
        tables[g] = {"min": min(counts), "max": max(counts), "seen": sum(1 for c in v["rows"] if c), "of": seeds,
                     "columns": v["columns"], "order": orders[0] if len(orders) == 1 else ("mixed" if orders else None),
                     "totals": sorted(v["totals"]), "title": (tcfg.get(g) or {}).get("title"),
                     "ask": (tcfg.get(g) or {}).get("ask", True)}
    rep = sorted(k for k, ns in numbered.items() if len(ns) >= 2 or (ns and min(ns) >= 2))
    return {"id": doc_id, "name": spec.name, "group": spec.group, "tables": tables,
            "numbered": [k.replace("#", "N") for k in rep], "nested": sorted(nested)}


def run(seeds: int = 12, workers: int = 1, ids: list[str] | None = None) -> list[dict]:
    from ..registry import load_all

    ids = ids or sorted(load_all())
    jobs = [(i, seeds) for i in ids]
    if workers > 1:
        import multiprocessing as mp

        with mp.get_context("spawn").Pool(workers) as pool:
            return list(pool.imap(audit_form, jobs, chunksize=4))
    return [audit_form(j) for j in jobs]


def markdown(res: list[dict], seeds: int) -> str:
    with_tables = [r for r in res if r.get("tables")]
    fixed = [(r, g, t) for r in with_tables for g, t in r["tables"].items() if t["min"] == t["max"] and t["ask"]]
    asc = [(r, g, t) for r in with_tables for g, t in r["tables"].items() if t["order"] == "asc"]
    totals = [(r, g, t) for r in with_tables for g, t in r["tables"].items() if t["totals"]]
    numbered = [r for r in res if r.get("numbered")]
    nested = [r for r in res if r.get("nested")]
    errors = [r for r in res if r.get("error")]
    L = ["# 표 점검 목록", "",
         f"<!-- 자동 생성 — python -m docgen.bench.table_audit --seeds {seeds} --out guide/reference/table-audit.md -->", "",
         "표(반복 묶음)의 정의와 질문은 [benchmark.md](benchmark.md#표의-정의). 이 목록은 사람이 보고 정할 것만 모읍니다 — 아무것도 고치지 않았습니다.",
         f"서식 {len(res)}종 중 표가 있는 서식 {len(with_tables)}종, 표 묶음 {sum(len(r['tables']) for r in with_tables)}개 "
         f"(seed {seeds}개로 그려 봄).", "",
         "| 점검 | 수 | 정할 것 | 고치는 곳 |", "|---|---:|---|---|",
         f"| 행 수가 늘 같은 표 | {len(fixed)} | 정해진 격자인가? 그러면 표가 아니라 kie | 서식 `questions.json` `{{\"table\": {{\"<묶음>\": {{\"ask\": false}}}}}}` |",
         f"| 오래된 순 표 (날짜 열) | {len(asc)} | 실서류도 오래된 순인가? 최신순이면 바꿈 | 그 서식 `generate.py` (행 순서) |",
         f"| 표 안 합계 열 | {len(totals)} | 합계는 표가 아니라 kie 칸 | 템플릿·`generate.py` 에서 합계를 행 밖 키로 |",
         f"| 번호를 이름에 붙인 반복 칸 | {len(numbered)} | 반복 레코드면 표로 | 키를 `<묶음>.0.<열>` 꼴로 (템플릿·`fields.json`) |",
         f"| 겹친 목록 | {len(nested)} | 묻지 않음 (그대로 둬도 됨) | — |", ""]
    if errors:
        L += [f"그리지 못한 서식 {len(errors)}종: " + ", ".join(f"`{r['id']}` ({r['error'][:60]})" for r in errors), ""]

    def md(x) -> str:   # 표 칸 안의 글자: markdown 링크·표 기호로 읽히지 않게
        return str(x).replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")

    def cols(t):
        return md(", ".join(f"{c}({lab})" if lab and lab != c else c for c, lab in list(t["columns"].items())[:6])
                  + (" …" if len(t["columns"]) > 6 else ""))
    L += ["## 행 수가 늘 같은 표", "", "| 서식 | 묶음 | 행 | 열 |", "|---|---|---:|---|"]
    L += [f"| `{r['id']}` {md(r['name'])} | `{g}` | {t['min']} | {cols(t)} |" for r, g, t in fixed] + [""]
    L += ["## 오래된 순 표", "", "날짜 열이 있는 3행 이상 표가 모든 seed 에서 오래된 순. 이력·내역 표는 실서류가 최신순인 경우가 많습니다 "
          "(예: 건강보험 자격득실확인서는 고침).", "", "| 서식 | 묶음 | 행 | 열 |", "|---|---|---|---|"]
    L += [f"| `{r['id']}` {md(r['name'])} | `{g}` | {t['min']}~{t['max']} | {cols(t)} |" for r, g, t in asc] + [""]
    L += ["## 표 안 합계 열", "", "| 서식 | 묶음 | 합계 열 |", "|---|---|---|"]
    L += [f"| `{r['id']}` {md(r['name'])} | `{g}` | {', '.join(t['totals'])} |" for r, g, t in totals] + [""]
    L += ["## 번호를 이름에 붙인 반복 칸", "", "`N` 자리에 번호가 붙은 키들 (예: `guarantorN.name` = guarantor1.name, guarantor2.name …).", "",
          "| 서식 | 키 |", "|---|---|"]
    L += [f"| `{r['id']}` {md(r['name'])} | {', '.join(f'`{k}`' for k in r['numbered'][:8])}{' …' if len(r['numbered']) > 8 else ''} |" for r in numbered] + [""]
    L += ["## 겹친 목록", "", "| 서식 | 키 |", "|---|---|"]
    L += [f"| `{r['id']}` {md(r['name'])} | {', '.join(f'`{k}`' for k in r['nested'])} |" for r in nested] + [""]
    L += ["## 모든 표", "", "| 서식 | 묶음 | 행 (최소~최대) | 나옴 | 순서 | 제목 | 열 |", "|---|---|---|---|---|---|---|"]
    for r in with_tables:
        for g, t in r["tables"].items():
            L.append(f"| `{r['id']}` | `{g}`{'' if t['ask'] else ' (kie)'} | {t['min']}~{t['max']} | {t['seen']}/{t['of']} | "
                     f"{t['order'] or '-'} | {t['title'] or '-'} | {cols(t)} |")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m docgen.bench.table_audit", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--ids", help="서식 ID 쉼표 목록 (기본 전부)")
    ap.add_argument("--out", help="markdown 저장 (기본 화면에)")
    ap.add_argument("--json", help="JSON 저장")
    a = ap.parse_args(argv)
    res = run(a.seeds, a.workers, a.ids.split(",") if a.ids else None)
    md = markdown(res, a.seeds)
    if a.out:
        Path(a.out).write_text(md, encoding="utf-8")
        print(f"→ {a.out}", file=sys.stderr)
    else:
        print(md)
    if a.json:
        Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
