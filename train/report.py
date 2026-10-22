"""모델끼리 나란히 놓은 벤치마크 보고서 (CSV, Markdown, HTML) — train.cli score 결과들로 (옛 bank_task/report.py + 1부 benchmark_report).
OCR·문서 이해·업무 과제를 한 표에, 과제 묶음 순서로."""
import csv
import html
import json
import re
from pathlib import Path

from docgen.bench.ocr_data import read_json
from docgen.bench.tracking import DIMENSIONS, SCORE_DIMENSIONS

# (task, metric, column title, lower is better)
COLUMNS = [
    ("crop_ocr", "cer", "칸 잘라 읽기 CER", True),
    ("bbox_ocr", "em", "좌표→글자 일치", False),
    ("bbox_ocr", "numeric_em", "좌표→숫자 일치", False),
    ("region_ocr", "cer", "영역 받아쓰기 CER", True),
    ("grounding", "f1_iou50", "글자→좌표 F1@0.5", False),
    ("grounding", "negative_accuracy", "글자→좌표 없음 정확도", False),
    ("spotting", "f1_iou50", "글자 찾기 위치 F1@0.5", False),
    ("spotting", "e2e_f1", "글자 찾기 위치+글자 F1", False),
    ("relation", "e2e_f1", "항목명→값 위치+글자 F1", False),
    ("marked_ocr", "em", "그린 박스→글자 일치", False),
    ("marked_box", "f1_iou75", "그린 박스→좌표 F1@0.75", False),
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
SLICES = [("spotting", "view", "글자 찾기 — 깨끗한 쪽 / 변형한 쪽"),
          ("crop_ocr", "view", "칸 잘라 읽기 — 깨끗한 쪽 / 변형한 쪽"),
          ("cross_check", "category", "서류 대조 — 불일치 분류별 종합 점수"),
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
    return _build_reports(reports, Path(output))


def _build_reports(reports, output):
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
    if any("benchmarks" in r for r in reports):
        return _build_suite(reports, base, Path(output))
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
    # 생성 때의 분류를 그대로 사용한다. CER 등은 원본 문항 집합으로 다시 집계한 점수다.
    detail_rows = []
    for dimension in SCORE_DIMENSIONS:
        keys = sorted({(group, task) for r in reports
                       for group, bucket in r.get("breakdowns", {}).get(dimension, {}).items()
                       for task in bucket["tasks"]})
        body = []
        for group, task in keys:
            cells = [r.get("breakdowns", {}).get(dimension, {}).get(group, {}).get("tasks", {}).get(task) for r in reports]
            known = [c for c in cells if c]
            if len({c["membership_sha256"] for c in known}) > 1:
                raise ValueError(f"Different group membership: {dimension}/{group}/{task}")
            baseline = base.get("breakdowns", {}).get(dimension, {}).get(group, {}).get("tasks", {}).get(task)
            metric = known[0]["main"]
            n = known[0]["n"]
            values = []
            for r, c in zip(reports, cells):
                value_ = c["metrics"].get(metric) if c else None
                base_ = baseline["metrics"].get(metric) if baseline else None
                values += [_pct(value_), "—" if _delta(value_, base_) is None else f"{_delta(value_, base_):+.1f}"]
                detail_rows.append({"model": r["label"], "dimension": dimension, "group": group, "task": task,
                                    "metric": metric, "lower_is_better": metric in {"cer", "false_alarm", "matched_label_cer"},
                                    "n": c["n"] if c else 0, "unit": "items", "value": value_, "delta_pp": _delta(value_, base_),
                                    "missing": c["missing"] if c else None, "parse_fail": c["parse_fail"] if c else None,
                                    "membership_sha256": c["membership_sha256"] if c else None})
            body.append([group, task, metric, str(n)] + values)
        if body:
            slices.append((f"{DIMENSIONS[dimension]}별 평가 · 과제별 주 지표", [DIMENSIONS[dimension], "과제", "지표", "문항 수"] +
                           [title for label in labels for title in (label, label + " Δpp")], body))
    # 필드 타입 점수의 n은 문항이 아니라 추출/표시 항목 수다.
    for task, key in (("kie", "kind"), ("marks", "type")):
        groups = sorted({g for r in reports for g in r["tasks"].get(task, {}).get("slices", {}).get(key, {})})
        if groups:
            body = []
            for group in groups:
                cells = [r["tasks"].get(task, {}).get("slices", {}).get(key, {}).get(group, {}) for r in reports]
                body.append([group, str(next(c["n"] for c in cells if c))] + [_pct(c.get("acc")) for c in cells])
                baseline = base["tasks"].get(task, {}).get("slices", {}).get(key, {}).get(group, {})
                for r, c in zip(reports, cells):
                    detail_rows.append({"model": r["label"], "dimension": "field_kind", "group": group, "task": task,
                                        "metric": "acc", "lower_is_better": False, "n": c.get("n", 0), "unit": "fields",
                                        "value": c.get("acc"), "delta_pp": _delta(c.get("acc"), baseline.get("acc")),
                                        "missing": None, "parse_fail": None, "membership_sha256": None})
            slices.append((f"{task} 필드 타입별 값 정확도 · 항목 단위", ["필드 타입", "항목 수"] + labels, body))
    if detail_rows:
        detail_path = output.with_name(output.stem + ".breakdowns.csv")
        with detail_path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(detail_rows[0]))
            writer.writeheader()
            writer.writerows(detail_rows)
    output.with_name(output.stem + ".breakdowns.json").write_text(json.dumps({
        "items_sha256": reports[0]["items_sha256"], "dimensions": {**DIMENSIONS, "field_kind": "필드 타입 (항목 단위)"},
        "models": [{"label": r["label"], "composition": r.get("composition"), "breakdowns": r.get("breakdowns", {}),
                    "field_type_scores": {task: r["tasks"].get(task, {}).get("slices", {}).get(key, {}) for task,key in (("kie","kind"),("marks","type"))}} for r in reports]},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    notes = [f"기준(Δ의 0): {base['label']}. 점수는 %, Δ는 기준 대비 %p. ↓ 표시는 낮을수록 좋음.",
             "문항 수: " + ", ".join(f"{t} {n}" for t, n in counts.items()),
             "합성 서류(docgen) 평가는 학습 데이터와 같은 생성기라 실제 서류 성능보다 높게 나옵니다. "
             "OCR 과제의 정답이 사내 OCR 그대로(의사정답)면 점수는 '그것과 얼마나 같은지'입니다.",
             "unknown은 메타데이터 누락, not_applicable은 업무 시나리오가 없는 단일 서류/OCR 문항입니다. 다른 과제의 점수는 평균내지 않습니다.",
             "구분별 상세 CSV·JSON: benchmark.breakdowns.* (CSV 값은 원 지표, delta_pp는 %p). 필드 타입 표의 n은 항목 수입니다.",
             "읽는 법: guide/results.md"]

    def md(head, body):
        def escaped(row):
            return " | ".join(str(x).replace("|", "\\|").replace("\n", " ") for x in row)
        return "\n".join(["| " + escaped(head) + " |", "|" + "---|" * len(head)] +
                         ["| " + escaped(row) + " |" for row in body])

    parts = ["# 벤치마크 비교\n", md(*score_t), "\n## 기준 대비 변화 (%p)\n", md(*delta_t),
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
    page = ("<!doctype html><html lang=ko><meta charset=utf-8><title>벤치마크 비교</title><style>"
            "body{font-family:sans-serif;margin:24px;color:#222}table{border-collapse:collapse;margin:8px 0 24px}"
            "th,td{border:1px solid #ccc;padding:4px 8px;text-align:right}th:first-child,td:first-child{text-align:left}"
            "th{background:#f3f3f3}</style><h1>벤치마크 비교</h1>" + "".join(sections)
            + "<ul>" + "".join(f"<li>{html.escape(n)}</li>" for n in notes) + "</ul></html>")
    output.with_suffix(".html").write_text(page, encoding="utf-8")
    return {"models": labels, "output": str(output)}


def _build_suite(reports, base, output):
    """각 id를 독립 채점한 보고서를 먼저 보여 준다. group끼리는 합산하지 않는다."""
    if output.suffix.lower() != ".csv":
        raise ValueError("--out must end with .csv")
    definitions = base.get("benchmarks", {})
    if not definitions or any(set(r.get("benchmarks", {})) != set(definitions) for r in reports):
        raise ValueError("Reports use different benchmark IDs; rescore every model with the same configuration")
    for ident, definition in definitions.items():
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", ident):
            raise ValueError(f"Invalid benchmark ID: {ident}")
        for report in reports:
            other = report["benchmarks"][ident]
            if any(other.get(k) != definition.get(k) for k in ("name", "group", "items_sha256")):
                raise ValueError(f"Benchmark {ident} changed its name/group/items")
    output.parent.mkdir(parents=True, exist_ok=True)
    labels = [r["label"] for r in reports]
    csv_rows, detail_rows, markdown, sections = [], [], ["# 벤치마크별 모델 비교", "", "각 id의 paths를 합쳐 과제별로 계산합니다. group은 표시 분류이며 합산 점수가 없습니다.", ""], []
    for group in dict.fromkeys(b["group"] for b in definitions.values()):
        markdown += [f"## {group}", ""]
        sections.append(f"<h2>{html.escape(group)}</h2>")
        for ident, definition in definitions.items():
            if definition["group"] != group:
                continue
            scoped = []
            for report in reports:
                child = {**report, **report["benchmarks"][ident]}
                child.pop("benchmarks", None)
                scoped.append(child)
            child_output = output.parent / "benchmarks" / ident / output.name
            _build_reports(scoped, child_output)
            rel = child_output.relative_to(output.parent).with_suffix(".html").as_posix()
            markdown += [f"### {definition['name']} · {ident}", "", f"경로 {len(definition.get('paths', []))}개 · 평가 문항 {definition['n']}개 · [상세 보고서]({rel})", ""]
            head = ["과제", "지표", "문항 수"] + [t for label in labels for t in (label, label + " Δpp")]
            body = []
            baseline = base["benchmarks"][ident]
            for task, task_base in baseline["tasks"].items():
                metric = task_base["main"]
                values = []
                for report in scoped:
                    result = report["tasks"][task]
                    value = result["metrics"].get(metric)
                    before = task_base["metrics"].get(metric)
                    values += [_pct(value), "—" if _delta(value, before) is None else f"{_delta(value, before):+.1f}"]
                    for key, val in sorted(result["metrics"].items()):
                        csv_rows.append({"benchmark_group": group, "benchmark_id": ident, "benchmark_name": definition["name"],
                                         "model": report["label"], "task": task, "metric": key, "n": result["n"], "value": val,
                                         "delta_pp": _delta(val, task_base["metrics"].get(key)),
                                         "lower_is_better": key in {"cer", "false_alarm", "matched_label_cer"}})
                body.append([task, metric + (" ↓" if metric in {"cer", "false_alarm", "matched_label_cer"} else ""), str(task_base["n"])] + values)
            def md_row(row):
                return "| " + " | ".join(str(v).replace("|", "\\|").replace("\n", " ") for v in row) + " |"
            markdown += [md_row(head), "|" + "---|" * len(head), *[md_row(row) for row in body], ""]
            table = "<table><thead><tr>" + "".join(f"<th>{html.escape(v)}</th>" for v in head) + "</tr></thead><tbody>"
            table += "".join("<tr>" + "".join(f"<td>{html.escape(v)}</td>" for v in row) + "</tr>" for row in body) + "</tbody></table>"
            sections += [f"<h3>{html.escape(definition['name'])} · {html.escape(ident)}</h3><p>경로" +
                         f" {len(definition.get('paths', []))}개 · 평가 문항 {definition['n']}개 · <a href='{rel}'>시나리오·서식·필드별 상세</a></p>", table]
            detail = child_output.with_name(child_output.stem + ".breakdowns.csv")
            if detail.exists():
                with detail.open(encoding="utf-8-sig", newline="") as f:
                    detail_rows += [{"benchmark_id": ident, "benchmark_name": definition["name"], "benchmark_group": group, **row} for row in csv.DictReader(f)]
    def write_csv(path, rows):
        if rows:
            with path.open("w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
    write_csv(output, csv_rows)
    write_csv(output.with_name(output.stem + ".breakdowns.csv"), detail_rows)
    output.with_suffix(".md").write_text("\n".join(markdown), encoding="utf-8")
    output.with_suffix(".html").write_text("<!doctype html><html lang=ko><meta charset=utf-8><title>벤치마크별 비교</title><style>body{font-family:sans-serif;margin:24px}table{border-collapse:collapse;margin-bottom:24px}td,th{border:1px solid #ccc;padding:7px}th{background:#f3f3f3}</style><h1>벤치마크별 모델 비교</h1><p>각 id의 paths를 합산합니다. group은 표시 분류이며 합산 점수가 없습니다. 점수는 %, 변화는 %p입니다.</p>" + "".join(sections) + "</html>", encoding="utf-8")
    output.with_name(output.stem + ".breakdowns.json").write_text(json.dumps({
        "items_sha256": reports[0]["items_sha256"], "models": [{"label": r["label"], "benchmarks": r["benchmarks"]} for r in reports]}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return {"models": labels, "output": str(output), "benchmarks": list(definitions)}
