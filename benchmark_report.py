"""Side-by-side benchmark report; no model invocation and no invented scores.
Needs the installed bank_ocr package (metric definitions are shared with evaluation)."""
import csv
import html
import math
from pathlib import Path

import json

from bank_ocr.metrics import LOWER_IS_BETTER, REPORT_METRICS


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


METRICS = REPORT_METRICS


def build_report(paths, output, labels=None):
    reports = [read_json(p) for p in paths]
    if not reports:
        raise ValueError("At least one report is required")
    if len({r["tasks_sha256"] for r in reports}) != 1:
        raise ValueError("Reports use different benchmark tasks; do not compare them")
    if any(r.get("reference_type") != "ocr_pseudo_unreviewed" for r in reports):
        raise ValueError("Unexpected reference type")
    signatures = [{k: (v["count"], v.get("numeric_count")) for k, v in r["tasks"].items()} for r in reports]
    if any(s != signatures[0] for s in signatures):
        raise ValueError("Reports use different evaluation counts")
    infos = [r.get("inference") or {} for r in reports]
    for key in ("images_sha256", "temperature", "max_tokens", "enable_thinking", "request_options"):
        known = [i.get(key, {}) if key == "request_options" else i[key] for i in infos if key == "request_options" or key in i]
        if any(value != known[0] for value in known):
            raise ValueError(f"Reports use different {key}")
    strict = labels is not None
    if strict and any(i.get("with_ocr") is True for i in infos):
        raise ValueError("Base/SFT/GRPO comparison requires vision-only runs; remove --with-ocr")
    names = list(labels) if labels is not None else [r["model_label"] for r in reports]
    if len(names) != len(reports) or len(set(names)) != len(names):
        raise ValueError("Model labels must be unique and match report count")
    records = []
    for name, report, info in zip(names, reports, infos):
        record = {"model": name, "teacher_context": info.get("with_ocr", "unknown"),
                  "reference_type": report["reference_type"]}
        for key, _, task, metric in METRICS:
            value = report["tasks"].get(task, {}).get(metric)
            if value is not None and (type(value) not in (int, float) or not math.isfinite(value)):
                raise ValueError(f"Invalid metric {key}")
            record[key] = value
        records.append(record)
    baseline = records[0]
    for record in records:
        for key, *_ in METRICS:
            value, base = record[key], baseline[key]
            record[key + "_delta_pp"] = (value - base) * 100 if value is not None and base is not None else None
    output = Path(output)
    if output.suffix.lower() != ".csv":
        raise ValueError("--out must end with .csv; .md and .html are generated alongside it")
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["model", "teacher_context", "reference_type"] + [m[0] for m in METRICS] + [m[0] + "_delta_pp" for m in METRICS]
    with output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)
    fmt = lambda v: "—" if v is None else f"{v * 100:.2f}%"
    fmt_delta = lambda v: "—" if v is None else f"{v:+.2f} pp"
    headings = ["Model"] + [m[1] for m in METRICS]
    scores = [[r["model"]] + [fmt(r[m[0]]) for m in METRICS] for r in records]
    changes = [[r["model"]] + [fmt_delta(r[m[0] + "_delta_pp"]) for m in METRICS] for r in records]
    context = [f"{r['model']}: {r['teacher_context']}" for r in records]
    notes = [
        "기준: 사람 검수 없는 내부 OCR 의사정답과의 일치도. 실제 문서 정답률이 아닙니다.",
        "GRPO model은 SFT 체크포인트에서 GRPO를 이어 학습한 모델입니다." if strict else "첫 번째 행을 변화량의 기준으로 사용합니다.",
        "점수는 %, 변화량은 해당 모델 − 기준 모델의 퍼센트포인트(pp)입니다. " + ", ".join(sorted(LOWER_IS_BETTER)) + "는 음수 변화가 개선이고 나머지는 양수가 개선입니다.",
        "F1@0.5는 IoU 0.5 이상으로 짝지은 박스 기준이며, 위치+글자 F1은 글자까지 정확히 같아야 맞은 것으로 셉니다.",
        "—는 해당 평가 항목이 없거나 숫자 대상이 없어 계산하지 못한 값입니다.",
        "OCR context 제공 여부: " + "; ".join(context),
        "추론 메타데이터가 없는 보고서는 동일 추론 조건을 검증할 수 없습니다." if any(not i for i in infos) else "기록된 이미지 해시·temperature·max_tokens·thinking·추가 요청 옵션 조건의 일치를 확인했습니다.",
        "이미지 토큰 예산과 서버에 로드한 실제 체크포인트는 실행 환경에서 동일 조건 및 올바른 모델 여부를 확인해야 합니다.",
        "벤치마크 SHA256: " + reports[0]["tasks_sha256"],
        "평가 건수: " + "; ".join(f"{k}={v[0]}" + (f", 숫자 대상={v[1]}" if v[1] is not None else "") for k, v in signatures[0].items()),
    ]
    def md_table(data):
        escape = lambda s: str(s).replace("|", "\\|").replace("\n", " ")
        return "\n".join(["| " + " | ".join(map(escape, headings)) + " |", "| " + " | ".join(["---"] * len(headings)) + " |"] + ["| " + " | ".join(map(escape, row)) + " |" for row in data])
    def view_rows(view):
        rows = []
        for name, report in zip(names, reports):
            tasks = report.get("breakdown", {}).get("view", {}).get(view, {})
            rows.append([name] + [fmt(tasks.get(task, {}).get(metric)) for _, _, task, metric in METRICS])
        return rows
    views = [("clean", "원본 크기 조정 이미지(clean)"), ("aug", "노이즈·기하 증강 이미지(aug)")]
    markdown = "# Benchmark comparison\n\n" + md_table(scores) + "\n\n## " + names[0] + " 대비 변화\n\n" + md_table(changes)
    markdown += "".join("\n\n## " + title + "\n\n" + md_table(view_rows(view)) for view, title in views)
    markdown += "\n\n" + "\n\n".join(notes) + "\n"
    output.with_suffix(".md").write_text(markdown, encoding="utf-8")
    esc = lambda s: html.escape(str(s), quote=True)
    def html_table(data):
        return "<div class='scroll'><table><thead><tr>" + "".join("<th>" + esc(s) + "</th>" for s in headings) + "</tr></thead><tbody>" + "".join("<tr>" + "".join("<td>" + esc(s) + "</td>" for s in row) + "</tr>" for row in data) + "</tbody></table></div>"
    document = """<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Benchmark comparison</title>
<style>body{font-family:system-ui,sans-serif;background:#f4f6fa;color:#18243a;margin:0;padding:36px}main{max-width:1300px;margin:auto}h1{margin-bottom:8px}h2{margin-top:36px;font-size:20px}.scroll{overflow:auto;border:1px solid #dbe1eb;border-radius:12px;background:white}table{width:100%;border-collapse:collapse;white-space:nowrap}th,td{padding:18px 14px;text-align:right;border-bottom:1px solid #e8edf4}th{background:#edf2fb;font-size:13px}th:first-child,td:first-child{text-align:left;font-weight:700}tbody tr:last-child td{border-bottom:0}p{font-size:14px;line-height:1.7;overflow-wrap:anywhere}.subtitle{color:#53627c;margin-bottom:24px}</style><main><h1>Benchmark comparison</h1><p class="subtitle">동일 벤치마크 · 내부 OCR 의사정답 기준</p>"""
    document += html_table(scores) + "<h2>" + esc(names[0]) + " 대비 변화</h2>" + html_table(changes)
    document += "".join("<h2>" + esc(title) + "</h2>" + html_table(view_rows(view)) for view, title in views)
    document += "<h2>평가 조건</h2>" + "".join("<p>" + esc(n) + "</p>" for n in notes) + "</main></html>"
    output.with_suffix(".html").write_text(document, encoding="utf-8")
    return {"models": len(records), "csv": str(output), "markdown": str(output.with_suffix('.md')), "html": str(output.with_suffix('.html'))}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Base / SFT / GRPO benchmark comparison (no model is run)")
    parser.add_argument("--base", required=True, help="Existing Base evaluation JSON")
    parser.add_argument("--sft", required=True, help="Existing SFT evaluation JSON")
    parser.add_argument("--grpo", required=True, help="Existing SFT+GRPO evaluation JSON")
    parser.add_argument("--out", default="reports/benchmark.csv", help="CSV path; Markdown and HTML are also created")
    args = parser.parse_args()
    inputs = [Path(p).resolve() for p in (args.base, args.sft, args.grpo)]
    if len(set(inputs)) != 3:
        parser.error("Provide three different evaluation report files")
    try:
        result = build_report(inputs, args.out, ["Base model", "SFT model", "GRPO model"])
    except (ValueError, KeyError, OSError) as error:
        parser.exit(2, "Report error: " + str(error) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
