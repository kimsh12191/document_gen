"""Side-by-side banking benchmark report (CSV, Markdown, HTML) from `bank_task score` outputs."""
import csv
import html
from pathlib import Path

from bank_ocr.data import read_json

# (task, metric, column title, lower is better)
COLUMNS = [
    ("ocr_field", "exact", "값 칸 OCR 일치", False),
    ("ocr_field", "cer", "값 칸 CER", True),
    ("ocr_page", "recall", "전체 받아쓰기 재현율", False),
    ("classify", "acc", "서류 분류", False),
    ("kie", "f1", "정보 추출 F1", False),
    ("kie", "vl_f1", "정보 추출 값+위치 F1", False),
    ("marks", "acc", "체크·도장·서명", False),
    ("marks", "vl_f1", "체크·도장·서명 값+위치 F1", False),
    ("doc_check", "exact", "서류 구비 완전 일치", False),
    ("doc_check", "set_f1", "서류 구비 F1", False),
    ("cross_check", "score", "서류 대조 종합", False),
    ("cross_check", "detect", "서류 대조 탐지", False),
    ("cross_check", "localize", "서류 대조 위치(변조 문항)", False),
    ("cross_check", "false_alarm", "서류 대조 오탐률", True),
    ("review", "acc", "심사 질의 정확도", False),
]
SLICES = [("cross_check", "category", "서류 대조 — 불일치 분류별 종합 점수"),
          ("cross_check", "case", "서류 대조 — 사례별 종합 점수"),
          ("review", "skill", "심사 질의 — 능력별 정확도"),
          ("doc_check", "n_missing", "서류 구비 — 빠진 서류 수별 완전 일치"),
          ("kie", "group", "정보 추출 — 서식 그룹별 F1"),
          ("ocr_field", "writing", "값 칸 OCR — 인쇄체/손글씨별 일치")]


def _pct(v):
    return "—" if v is None else f"{v * 100:.1f}"


def _delta(v, base):
    return None if v is None or base is None else (v - base) * 100


def build(paths, output):
    reports = [read_json(p) for p in paths]
    if not reports:
        raise ValueError("No reports")
    if len({r["items_sha256"] for r in reports}) != 1:
        raise ValueError("Reports use different benchmark items; do not compare them")
    infos = [r.get("inference") or {} for r in reports]
    for key in ("images_sha256", "temperature", "max_tokens", "enable_thinking", "request_options"):
        known = [i.get(key) for i in infos if key in i]
        if any(v != known[0] for v in known):
            raise ValueError(f"Reports use different inference {key}")
    labels = [r["label"] for r in reports]
    if len(set(labels)) != len(labels):
        raise ValueError("Report labels must be unique")
    base = next((r for r in reports if r.get("role") == "start"), reports[0])
    cols = [c for c in COLUMNS if any(c[0] in r["tasks"] for r in reports)]

    def value(r, task, metric):
        return r["tasks"].get(task, {}).get("metrics", {}).get(metric)

    rows = []
    for r in reports:
        row = {"model": r["label"], "path": r.get("model")}
        for task, metric, title, _ in cols:
            row[title] = value(r, task, metric)
            row[title + " Δpp"] = _delta(value(r, task, metric), value(base, task, metric))
        rows.append(row)
    output = Path(output)
    if output.suffix.lower() != ".csv":
        raise ValueError("--out must end with .csv; .md and .html are written next to it")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    def table(fmt):
        head = ["모델"] + [t + (" ↓" if low else "") for _, _, t, low in cols]
        body = [[r["label"]] + [fmt(value(r, task, m), value(base, task, m), r is base)
                                for task, m, _, _ in cols] for r in reports]
        return head, body

    score_t = table(lambda v, b, is_base: _pct(v))
    delta_t = table(lambda v, b, is_base: "기준" if is_base else
                    ("—" if _delta(v, b) is None else f"{_delta(v, b):+.1f}"))
    counts = {t: base["tasks"][t]["n"] for t in base["tasks"]}
    tasks = [t for t in counts]
    # Answers the scorer could not read count as wrong; a high rate means the model does not know the format yet.
    fail_t = (["모델"] + tasks, [[r["label"]] + [_pct(r["tasks"].get(t, {}).get("parse_fail")) for t in tasks]
                               for r in reports])
    slices = []
    for task, key, title in SLICES:
        groups = []
        for r in reports:
            for g in r["tasks"].get(task, {}).get("slices", {}).get(key, {}):
                if g not in groups:
                    groups.append(g)
        if len(groups) < 2:
            continue
        head = [key, "n"] + labels
        body = []
        for g in groups:
            cells = [r["tasks"].get(task, {}).get("slices", {}).get(key, {}).get(g, {}) for r in reports]
            n = next((c["n"] for c in cells if c), 0)
            body.append([g, str(n)] + [_pct(next((v for k, v in c.items() if k != "n"), None)) if c else "—"
                                       for c in cells])
        slices.append((title, head, body))
    notes = [f"기준(Δ의 0): {base['label']}. 점수는 %, Δ는 기준 대비 %p. ↓ 표시는 낮을수록 좋음.",
             "문항 수: " + ", ".join(f"{t} {n}" for t, n in counts.items()),
             "합성 서류(docgen) 평가 세트입니다. 학습 데이터와 같은 생성기라 실제 서류 성능보다 높게 나옵니다.",
             "읽는 법: guide/results.md"]

    def md(head, body):
        return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] +
                         ["| " + " | ".join(row) + " |" for row in body])

    parts = ["# 은행 업무 벤치마크 비교\n", md(*score_t), "\n## 기준 대비 변화 (%p)\n", md(*delta_t),
             "\n## 답 형식 오류 (%, 낮을수록 좋음)\n", md(*fail_t)]
    for title, head, body in slices:
        parts += [f"\n## {title}\n", md(head, body)]
    parts += ["\n" + "\n".join(f"- {n}" for n in notes)]
    output.with_suffix(".md").write_text("\n".join(parts) + "\n", encoding="utf-8")

    def ht(head, body):
        h = "".join(f"<th>{html.escape(x)}</th>" for x in head)
        b = "".join("<tr>" + "".join(f"<td>{html.escape(x)}</td>" for x in row) + "</tr>" for row in body)
        return f"<table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>"

    sections = [f"<h2>점수</h2>{ht(*score_t)}", f"<h2>기준 대비 변화 (%p)</h2>{ht(*delta_t)}",
                f"<h2>답 형식 오류 (%, 낮을수록 좋음)</h2>{ht(*fail_t)}"]
    sections += [f"<h2>{html.escape(t)}</h2>{ht(h, b)}" for t, h, b in slices]
    page = ("<!doctype html><html lang=ko><meta charset=utf-8><title>은행 업무 벤치마크</title><style>"
            "body{font-family:sans-serif;margin:24px;color:#222}table{border-collapse:collapse;margin:8px 0 24px}"
            "th,td{border:1px solid #ccc;padding:4px 8px;text-align:right}th:first-child,td:first-child{text-align:left}"
            "th{background:#f3f3f3}</style><h1>은행 업무 벤치마크 비교</h1>" + "".join(sections)
            + "<ul>" + "".join(f"<li>{html.escape(n)}</li>" for n in notes) + "</ul></html>")
    output.with_suffix(".html").write_text(page, encoding="utf-8")
    return {"models": labels, "output": str(output)}
