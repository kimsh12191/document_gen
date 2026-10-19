"""5단계 — 채점 결과 모으기와 비교 보고서 (report.md, 방법별 json).

주 지표는 대상 서류(등기부·등본·거래내역·인보이스·패킹리스트·재무제표)만으로 낸다. 문서 나누기(쪽 배정)는 묶음 전체 기준.
"""
from __future__ import annotations

import json
from pathlib import Path

from .common import read_jsonl
from .gen import load
from .run import failed
from .score import cost, score_bundle, summarize

KEY_METRICS = [
    ("page_assign_acc", "쪽 배정"), ("doc_pages_exact", "문서 나누기 정확"), ("field_f1", "항목 F1"),
    ("row_f1", "행 F1"), ("row_recall", "행 재현율"), ("row_dropped", "빠진 행 ↓"), ("cell_recall", "칸 재현율"),
    ("boundary_row_recall", "경계 행"), ("cont_row_recall", "이어지는 행"), ("check_balance_chain", "잔액 흐름"),
    ("check_items_sum", "품목 합계"),
]
COST_METRICS = [("requests_per_bundle", "요청/묶음"), ("image_tokens_per_bundle", "이미지 토큰/묶음"),
                ("max_prompt_tokens", "최대 입력 토큰"), ("completion_tokens_per_bundle", "출력 토큰/묶음"),
                ("latency_per_bundle", "초/묶음")]


def fmt(v, pct=True) -> str:
    if v is None:
        return "—"
    if isinstance(v, float) and pct:
        return f"{v * 100:.1f}"
    return f"{v:,.0f}" if isinstance(v, (int, float)) else str(v)


def _pages_group(d):
    return f"{min(d['n_pages'], 4)}{'+' if d['n_pages'] >= 4 else ''}쪽"


def score_run(data_dir, pred_path) -> tuple[dict, list[dict]]:
    """예측 파일 하나 → (요약, 묶음별 채점 결과)."""
    bundles, labels = load(data_dir)
    by_id = {b["id"]: b for b in bundles}
    preds = [p for p in read_jsonl(pred_path) if p["bundle"] in by_id and not failed(p)]
    results = [score_bundle(by_id[p["bundle"]], labels, p["docs"]) for p in preds]
    target_only = [{**r, "docs": [d for d in r["docs"] if d["target"]]} for r in results]
    overall = summarize(target_only)["all"]
    overall["page_assign_acc"] = summarize(results)["all"]["page_assign_acc"]  # 쪽 배정은 묶음 전체
    res = {"bundles": len(results), "overall": overall, "cost": cost(preds),
           "all_docs": summarize(results)["all"],
           "by_type": summarize(target_only, lambda d: d["type"]),
           "by_no_repeat_header": summarize(target_only, lambda d: "머리글 반복 없음" if d["no_repeat_header"] else "머리글 반복"),
           "by_pages": summarize(target_only, _pages_group),
           "by_augment": summarize(target_only, lambda d: d["augment"] or "clean")}
    return res, results


def compare(data_dir, pred_paths, out) -> str:
    """여러 예측 파일을 채점해 <out>/report.md 와 방법별 json 을 쓰고 report.md 내용을 돌려준다."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    table = {}
    for p in pred_paths:
        res, results = score_run(data_dir, p)
        name = Path(p).stem
        (out / f"{name}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        (out / f"{name}.bundles.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in results),
                                                    encoding="utf-8")
        table[name] = res
    md = report_md(table)
    (out / "report.md").write_text(md, encoding="utf-8")
    return md


def report_md(table: dict) -> str:
    lines = ["# 여러 쪽 문서 추출 비교", "",
             "점수는 % (↓ 는 낮을수록 좋음). 쪽 배정은 묶음 전체, 나머지는 대상 서류(여러 쪽 문서) 기준. 비용은 묶음 하나 기준.", ""]
    lines += ["| 방법 | 묶음 | " + " | ".join(n for _, n in KEY_METRICS) + " |", "|---|---:|" + "---:|" * len(KEY_METRICS)]
    for name, res in table.items():
        o = res["overall"]
        lines.append(f"| {name} | {res['bundles']} | " + " | ".join(fmt(o.get(k)) for k, _ in KEY_METRICS) + " |")
    lines += ["", "| 방법 | " + " | ".join(n for _, n in COST_METRICS) + " |", "|---|" + "---:|" * len(COST_METRICS)]
    for name, res in table.items():
        c = res["cost"]
        lines.append(f"| {name} | " + " | ".join(
            f"{c.get(k, 0):.1f}" if k == "latency_per_bundle" else fmt(c.get(k), pct=False) for k, _ in COST_METRICS) + " |")
    for section, title in (("by_type", "서류별"), ("by_pages", "서류 쪽 수별"),
                           ("by_no_repeat_header", "머리글 반복 여부별"), ("by_augment", "촬영 조건별")):
        lines += ["", f"## {title} (행 F1 / 이어지는 행 / 항목 F1)", ""]
        groups = sorted({g for res in table.values() for g in res[section] if g != "all"})
        lines += ["| 방법 | " + " | ".join(groups) + " |", "|---|" + "---:|" * len(groups)]
        for name, res in table.items():
            cells = []
            for g in groups:
                s = res[section].get(g)
                cells.append("—" if not s else f"{fmt(s.get('row_f1'))} / {fmt(s.get('cont_row_recall'))} / {fmt(s.get('field_f1'))}")
            lines.append(f"| {name} | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"
