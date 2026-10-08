"""채점.

  python -m docgen.bench eval --bench bench_out --pred preds/model_a [--pred preds/model_b ...]

예측 파일: <pred 폴더>/*.jsonl, 한 줄에 {"id": 문항 id, "output": 모델 출력 문자열}.
예측이 없는 문항은 틀린 것으로 센다 (보고서에 '예측 없음'으로 따로 표시).
결과: <pred 폴더>/report.json, report.md. 예측 폴더가 여러 개면 과제별 주 지표를 비교표로 출력한다.
"""
from __future__ import annotations

import difflib
import json
import sys
from pathlib import Path

from ..schema import similar_label
from .metrics import (cer, is_null, loose_text, norm_text, parse_json, strip_answer, substring_distance, to_number,
                      value_match, yes_no)

TASK_ORDER = ["ocr_field", "ocr_page", "classify", "kie", "marks", "doc_check", "cross_check", "review"]
TASK_TITLE = {"ocr_field": "OCR - 값 칸 인식", "ocr_page": "OCR - 전체 받아쓰기", "classify": "서류 분류",
              "kie": "정보 추출", "marks": "체크·도장·서명", "doc_check": "서류 구비 확인",
              "cross_check": "서류 간 대조", "review": "심사 질의"}
WORST = {"cer": 1.0, "false_alarm": 1.0}
MAIN = {"ocr_field": "exact", "ocr_page": "recall", "classify": "acc", "kie": "f1", "marks": "acc",
        "doc_check": "exact", "cross_check": "score", "review": "acc"}
METRIC_TITLE = {"exact": "완전 일치", "cer": "CER(낮을수록 좋음)", "recall": "값 재현율", "recall_fuzzy": "값 재현율(오차 20% 허용)",
                "acc": "정확도", "acc_lenient": "정확도(포함 허용)", "field_acc": "항목 정확도", "f1": "F1",
                "precision": "정밀도", "recall_f": "재현율", "doc_exact": "서류 전체 일치", "set_f1": "F1",
                "score": "종합 점수", "detect": "탐지 정확도", "localize": "위치 정확도(변조 문항)",
                "false_alarm": "오탐률(정상 문항)", "parse_fail": "출력 파싱 실패"}
SLICES = {"ocr_field": ["writing", "condition", "kind", "corrected"], "ocr_page": ["condition", "writing", "group"],
          "classify": ["group", "condition"], "kie": ["group", "condition", "writing", "@kind"],
          "marks": ["group", "condition", "@type"], "doc_check": ["n_missing", "scenario"],
          "cross_check": ["perturbed", "kind", "scenario"], "review": ["rule", "skill"]}


# ---------------------------------------------------------------------------
# 과제별 채점: (문항, 출력) -> {"metrics": {...}, "parse_fail"?: bool, "sub": [(slice, value, correct)]?}
# ---------------------------------------------------------------------------

def _name_match(pred: str, names: list[str]) -> str | None:
    """예측한 서류명을 후보 서류명 중 하나에 대응시킨다."""
    lp = loose_text(pred)
    if not lp:
        return None
    for n in names:
        if loose_text(n) == lp:
            return n
    inside = [n for n in names if loose_text(n) in lp or lp in loose_text(n)]
    if len(inside) == 1:
        return inside[0]
    best = max(names, key=lambda n: difflib.SequenceMatcher(None, loose_text(n), lp).ratio(), default=None)
    if best and difflib.SequenceMatcher(None, loose_text(best), lp).ratio() >= 0.6:
        return best
    return None


def s_classify(item, out):
    p = strip_answer(out).split("\n")[0]
    gt = item["answer"]
    return {"metrics": {"acc": float(loose_text(p) == loose_text(gt)),
                        "acc_lenient": float(bool(loose_text(p)) and (loose_text(gt) in loose_text(p)))}}


def s_ocr_field(item, out):
    p = strip_answer(out) if out is not None else ""
    return {"metrics": {"exact": float(norm_text(p) == norm_text(item["answer"])), "cer": min(1.0, cer(p, item["answer"]))}}


def s_ocr_page(item, out):
    hay = norm_text(out or "")
    exact = fuzzy = 0
    for v in item["answer"]:
        n = norm_text(v)
        if n in hay:
            exact += 1
            fuzzy += 1
        elif hay and substring_distance(n, hay) <= 0.2 * len(n):
            fuzzy += 1
    k = len(item["answer"]) or 1
    return {"metrics": {"recall": exact / k, "recall_fuzzy": fuzzy / k}}


def _flatten(obj, prefix="") -> dict:
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}{k}"
            if isinstance(v, dict) or (isinstance(v, list) and v and isinstance(v[0], (dict, list))):
                out.update(_flatten(v, key + "."))
            out[key] = v
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(_flatten(v, f"{prefix}{i}."))
            out[f"{prefix}{i}"] = v
    return out


def s_kie(item, out):
    pred = parse_json(out)
    fail = not isinstance(pred, dict)
    flat = _flatten(pred) if isinstance(pred, dict) else {}
    tp = fp = fn = 0
    correct_all, sub = [], []
    for key, gt in item["answer"].items():
        info = item["eval"]["fields"][key]
        p = flat.get(key)
        ok = value_match(p, gt, info["type"], info.get("norm"), key)
        correct_all.append(ok)
        sub.append(("kind", info.get("kind", "text"), ok))
        if gt is not None:
            tp += ok
            fn += not ok
            fp += (not ok) and not is_null(p)
        elif not is_null(p):
            fp += 1
    prec = tp / (tp + fp) if tp + fp else 1.0
    rec = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return {"metrics": {"field_acc": sum(correct_all) / len(correct_all), "f1": f1, "precision": prec, "recall_f": rec,
                        "doc_exact": float(all(correct_all))}, "parse_fail": fail, "sub": sub}


def _bool(v):
    if isinstance(v, bool):
        return v
    if v is None:
        return False
    return yes_no(str(v))


def s_marks(item, out):
    pred = parse_json(out)
    fail = not isinstance(pred, dict)
    flat = _flatten(pred) if isinstance(pred, dict) else {}
    oks, sub = [], []
    for key, gt in item["answer"].items():
        t = item["eval"]["types"][key]
        p = flat.get(key)
        if isinstance(p, dict):  # {"checked": ...} / {"present": ...} 같은 꼴도 받아 준다
            p = next((p[k] for k in ("checked", "value", "present", "selected") if k in p), p)
        if t in ("seal", "signature"):
            ok = _bool(p) == gt
        elif t == "checkbox_multi":
            ps = p if isinstance(p, list) else ([] if is_null(p) else [p])
            ok = sorted(loose_text(x) for x in ps) == sorted(loose_text(x) for x in gt)
        else:
            if isinstance(p, list):
                p = p[0] if len(p) == 1 else (None if not p else p)
            ok = value_match(p, gt) if not isinstance(p, list) else False
        oks.append(ok)
        sub.append(("type", t, ok))
    return {"metrics": {"acc": sum(oks) / len(oks)}, "parse_fail": fail, "sub": sub}


def s_doc_check(item, out):
    pred = parse_json(out)
    fail = not isinstance(pred, (dict, list))
    lst = pred.get("missing", []) if isinstance(pred, dict) else (pred if isinstance(pred, list) else [])
    req = item["eval"]["required"]
    got = {m for m in (_name_match(str(x), req) for x in lst if not is_null(x)) if m}
    unmatched = sum(1 for x in lst if not is_null(x) and _name_match(str(x), req) is None)
    gt = set(item["answer"]["missing"])
    tp, fp, fn = len(got & gt), len(got - gt) + unmatched, len(gt - got)
    f1 = 1.0 if not (tp + fp + fn) else 2 * tp / (2 * tp + fp + fn)
    return {"metrics": {"exact": float(got == gt and not unmatched), "set_f1": f1}, "parse_fail": fail}


def s_cross_check(item, out):
    pred = parse_json(out)
    fail = not isinstance(pred, dict)
    pred = pred if isinstance(pred, dict) else {}
    issues = [x for x in (pred.get("issues") or []) if isinstance(x, dict)]
    cons = pred.get("consistent")
    cons = _bool(cons) if cons is not None else (not issues if not fail else None)
    gt = item["answer"]
    detect = float(cons is not None and cons == gt["consistent"])
    m = {"detect": detect}
    if gt["consistent"]:
        m["false_alarm"] = float(cons is False)
        m["score"] = detect
    else:
        want = gt["issues"][0]
        hit = False
        for x in issues:
            doc = _name_match(str(x.get("document") or ""), item["eval"]["documents"])
            if doc != want["document"]:
                continue
            if value_match(x.get("value"), want["value"]) or similar_label(want["field"], str(x.get("field") or "")):
                hit = True
                break
        m["localize"] = float(hit and cons is False)
        m["score"] = m["localize"]
    return {"metrics": m, "parse_fail": fail}


def s_review(item, out):
    ev, gt = item["eval"], item["answer"]
    a = strip_answer(out)
    if ev["answer_type"] == "yesno":
        p = yes_no(a)
        return {"metrics": {"acc": float(p is not None and p == (gt == "예"))}, "parse_fail": p is None}
    p = to_number(a.rstrip("%").replace("배", "").replace("세", "").replace("년", "").replace("원", "").strip())
    if p is None:
        p = to_number(a)
    ok = p is not None and abs(p - float(gt)) <= ev.get("tol", 0) + 1e-9
    return {"metrics": {"acc": float(ok)}, "parse_fail": p is None}


SCORERS = {"classify": s_classify, "ocr_field": s_ocr_field, "ocr_page": s_ocr_page, "kie": s_kie, "marks": s_marks,
           "doc_check": s_doc_check, "cross_check": s_cross_check, "review": s_review}


# ---------------------------------------------------------------------------
# 집계
# ---------------------------------------------------------------------------

def load_items(bench: Path, tasks=None) -> dict[str, list[dict]]:
    items = {}
    for path in sorted((bench / "tasks").glob("*.jsonl")):
        t = path.stem
        if tasks and t not in tasks:
            continue
        items[t] = [json.loads(ln) for ln in path.open(encoding="utf-8") if ln.strip()]
    return items


def load_preds(pred: Path) -> dict[str, str]:
    out = {}
    for path in sorted(pred.glob("*.jsonl")):
        for ln in path.open(encoding="utf-8"):
            if ln.strip():
                r = json.loads(ln)
                if r.get("output") is not None or r["id"] not in out:
                    out[r["id"]] = r.get("output")
    return out


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def score_task(task: str, items: list[dict], preds: dict[str, str]) -> dict:
    fn = SCORERS[task]
    rows, missing, fails = [], 0, 0
    for it in items:
        out = preds.get(it["id"])
        if it["id"] not in preds:
            missing += 1
        r = fn(it, out)
        fails += bool(r.get("parse_fail")) and out is not None
        if out is None or r.get("parse_fail"):  # 예측 없음·파싱 실패는 최악 점수 (빈 답이 null 칸·'도장 없음'을 맞히지 않게)
            r = {"metrics": {k: WORST.get(k, 0.0) for k in r["metrics"]},
                 "sub": [(n, v, False) for n, v, _ in r.get("sub", [])]}
        rows.append((it, r))
    metrics = {}
    for k in {k for _, r in rows for k in r["metrics"]}:
        metrics[k] = _mean([r["metrics"].get(k) for _, r in rows])
    slices = {}
    main = MAIN[task]
    for s in SLICES.get(task, []):
        groups: dict = {}
        if s.startswith("@"):  # 항목 단위 구분 (kie 의 값 종류 등)
            for _, r in rows:
                for name, val, ok in r.get("sub", []):
                    if name == s[1:]:
                        groups.setdefault(str(val), []).append(float(ok))
        else:
            for it, r in rows:
                v = it["meta"].get(s)
                groups.setdefault(str(v), []).append(r["metrics"].get(main))
        slices[s.lstrip("@")] = {k: {"n": len(v), main if not s.startswith("@") else "acc": _mean(v)}
                                 for k, v in sorted(groups.items(), key=lambda kv: -len(kv[1]))}
    return {"n": len(items), "missing": missing, "parse_fail": fails / len(items) if items else 0.0,
            "main": main, "metrics": metrics, "slices": slices,
            "per_item": [{"id": it["id"], **r["metrics"]} for it, r in rows]}


def _fmt(v, pct=True):
    if v is None:
        return "-"
    return f"{v * 100:.1f}" if pct else f"{v:.3f}"


def report_md(name: str, res: dict) -> str:
    lines = [f"# 벤치마크 결과 — {name}\n"]
    lines.append("| 과제 | 문항 | 주 지표 | 점수 | 예측 없음 | 파싱 실패 |\n|---|---:|---|---:|---:|---:|")
    for t in TASK_ORDER:
        if t not in res:
            continue
        r = res[t]
        lines.append(f"| {TASK_TITLE[t]} (`{t}`) | {r['n']} | {METRIC_TITLE[r['main']]} | "
                     f"{_fmt(r['metrics'].get(r['main']))} | {r['missing']} | {_fmt(r['parse_fail'])}% |")
    for t in TASK_ORDER:
        if t not in res:
            continue
        r = res[t]
        lines.append(f"\n## {TASK_TITLE[t]} (`{t}`)\n")
        lines.append(" · ".join(f"{METRIC_TITLE.get(k, k)} {_fmt(v, k != 'cer')}" for k, v in sorted(r["metrics"].items())))
        for s, groups in r["slices"].items():
            if len(groups) < 2:
                continue
            k = next(iter(next(iter(groups.values())).keys() - {"n"}))
            lines.append(f"\n| {s} | n | {METRIC_TITLE.get(k, k)} |\n|---|---:|---:|")
            for g, v in groups.items():
                lines.append(f"| {g} | {v['n']} | {_fmt(v[k], k != 'cer')} |")
    lines.append("\n점수는 % (CER 은 0~1, 낮을수록 좋음).")
    return "\n".join(lines) + "\n"


def evaluate(args) -> None:
    bench = Path(args.bench)
    tasks = [t.strip() for t in args.tasks.split(",")] if args.tasks != "all" else None
    items = load_items(bench, tasks)
    if not items:
        sys.exit(f"{bench}/tasks 에 문항이 없습니다")
    summary = {}
    for pd in args.pred:
        pred = Path(pd)
        preds = load_preds(pred)
        res = {t: score_task(t, its, preds) for t, its in items.items()}
        (pred / "report.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        md = report_md(pred.name, res)
        (pred / "report.md").write_text(md, encoding="utf-8")
        summary[pred.name] = res
        if len(args.pred) == 1:
            print(md)
        print(f"→ {pred / 'report.md'}", file=sys.stderr)
    if len(args.pred) > 1:
        names = list(summary)
        print("| 과제 | 주 지표 | " + " | ".join(names) + " |\n|---|---|" + "---:|" * len(names))
        for t in TASK_ORDER:
            if t in items:
                main = MAIN[t]
                print(f"| {TASK_TITLE[t]} | {METRIC_TITLE[main]} | "
                      + " | ".join(_fmt(summary[n][t]["metrics"].get(main)) for n in names) + " |")
