"""채점 — OCR 8과제(ocr_metrics)와 은행 업무 8과제 모두 여기서 (studio/DESIGN.md 17절). GRPO 보상도 reward() 하나.

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
from . import ocr_metrics as OM
from .metrics import (cer, is_null, loose_text, match, norm_text, parse_json, strip_answer, substring_distance, to_number,
                      valid_box, value_match, yes_no)

OCR_TASKS = list(OM.TASKS)   # 쪽 OCR (옛 1부): 문항마다가 아니라 과제 전체로 지표를 낸다 (CER = 틀린 글자 합 / 글자 합)
TASK_ORDER = [*OCR_TASKS, "ocr_field", "ocr_page", "classify", "kie", "marks", "doc_check", "cross_check", "review"]
TASK_TITLE = {"crop_ocr": "OCR - 칸 잘라 읽기", "bbox_ocr": "OCR - 좌표 → 글자", "region_ocr": "OCR - 영역 받아쓰기",
              "marked_ocr": "OCR - 그린 박스 → 글자", "grounding": "OCR - 글자 → 좌표", "spotting": "OCR - 글자 찾기(좌표+글자)",
              "relation": "OCR - 항목명 → 값(좌표+글자)", "marked_box": "OCR - 그린 박스 → 좌표",
              "ocr_field": "OCR - 값 칸 인식", "ocr_page": "OCR - 전체 받아쓰기", "classify": "서류 분류",
              "kie": "정보 추출", "marks": "체크·도장·서명", "doc_check": "서류 구비 확인",
              "cross_check": "서류 간 대조", "review": "심사 질의"}
TASK_GROUP = {**{t: "ocr" for t in [*OCR_TASKS, "ocr_field", "ocr_page"]}, "classify": "doc", "kie": "doc", "marks": "doc",
              "doc_check": "work", "cross_check": "work", "review": "work"}
GROUP_TITLE = {"ocr": "OCR", "doc": "문서 이해", "work": "업무 처리"}
WORST = {"cer": 1.0, "false_alarm": 1.0}
LOWER_IS_BETTER = {"cer", "false_alarm", "matched_label_cer"}
# OCR 과제의 대표 지표는 옛 1부 비교표(REPORT_METRICS)와 같다
MAIN = {"crop_ocr": "cer", "bbox_ocr": "em", "region_ocr": "cer", "marked_ocr": "em", "grounding": "f1_iou50",
        "spotting": "e2e_f1", "relation": "e2e_f1", "marked_box": "f1_iou75",
        "ocr_field": "exact", "ocr_page": "recall", "classify": "acc", "kie": "vl_f1", "marks": "vl_f1",
        "doc_check": "exact", "cross_check": "score", "review": "acc"}
# 평가 세트 1.x 의 kie·marks 는 값만 답한다 → 주 지표가 값 점수 (f1 / acc). 2.0 부터 값+위치 (vl_f1).
MAIN_V1 = {"kie": "f1", "marks": "acc"}


def main_metric(task: str, metrics: dict) -> str:
    """그 과제의 주 지표 이름. 위치가 없는 1.x 문항이면 값 점수."""
    m = MAIN[task]
    return m if m in metrics else MAIN_V1.get(task, m)
METRIC_TITLE = {"exact": "완전 일치", "cer": "CER(낮을수록 좋음)", "recall": "값 재현율", "recall_fuzzy": "값 재현율(오차 20% 허용)",
                "acc": "정확도", "acc_lenient": "정확도(포함 허용)", "field_acc": "항목 정확도", "f1": "F1",
                "precision": "정밀도", "recall_f": "재현율", "doc_exact": "서류 전체 일치", "set_f1": "F1",
                "score": "종합 점수", "detect": "탐지 정확도", "localize": "위치 정확도(변조 문항)",
                "false_alarm": "오탐률(정상 문항)", "parse_fail": "출력 파싱 실패", "missing_exact": "빠진 서류 일치",
                "not_required_exact": "불필요 서류 일치", "not_customer_exact": "타인 서류 일치",
                "loc_f1": "위치 F1 (IoU 0.5)", "vl_f1": "값+위치 F1", "loc_precision": "위치 정밀도", "loc_recall": "위치 재현율",
                "em": "완전 일치", "numeric_em": "숫자 일치", "word_f1": "단어 F1(순서 무관)", "f1_iou50": "위치 F1 (IoU 0.5)",
                "f1_iou75": "위치 F1 (IoU 0.75)", "e2e_f1": "위치+글자 F1", "f1_center": "위치 F1 (가운데 포함)",
                "precision_iou50": "위치 정밀도", "recall_iou50": "위치 재현율", "mean_iou_matched": "맞은 박스 평균 IoU",
                "count_accuracy": "박스 수 일치", "negative_accuracy": "없음 정확도", "valid_json_rate": "형식 맞음",
                "matched_label_cer": "맞은 박스 글자 CER"}
SLICES = {"ocr_field": ["writing", "condition", "kind", "corrected"], "ocr_page": ["condition", "writing", "group"],
          "classify": ["group", "condition"], "kie": ["group", "condition", "writing", "@kind"],
          "marks": ["group", "condition", "@type"], "doc_check": ["n_missing", "not_customer", "not_required", "scenario"],
          "cross_check": ["category", "case", "perturbed", "scenario"], "review": ["skill", "rule"],
          **{t: ["view", "confidence", "size"] for t in OCR_TASKS}}


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
    """정답 문서명 또는 그 다른 이름(eval.aliases, 키 사전의 문서명 다른 이름)과 같으면 맞음."""
    p = loose_text(strip_answer(out).split("\n")[0])
    gts = [loose_text(x) for x in [item["answer"], *(item.get("eval") or {}).get("aliases", [])] if x]
    return {"metrics": {"acc": float(p in gts), "acc_lenient": float(bool(p) and any(g in p for g in gts))}}


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


def _entries(pred) -> list[dict] | None:
    """모델 답 → [{"key", "value", "bbox_2d"?, "page"?}]. 목록 답(2.0)과 값만 있는 객체 답(1.x 꼴) 둘 다 받는다."""
    if isinstance(pred, list):
        return [x for x in pred if isinstance(x, dict) and isinstance(x.get("key"), str)]
    if isinstance(pred, dict):
        return [{"key": k, "value": v} for k, v in _flatten(pred).items()]
    return None


def _has_box(e) -> bool:
    return valid_box(e.get("bbox_2d"))


def _page(e) -> int:
    try:
        return int(e.get("page") or 1)
    except (TypeError, ValueError):
        return 1


def _located(gts: list[dict], preds: list[dict], value_ok) -> dict:
    """위치 점수: 같은 키·같은 쪽에서 IoU 0.5 이상인 짝 (OCR 과제와 같은 짝짓기). value_ok(pred, gt) 면 값+위치도 맞음.
    정답 박스가 없는 항목(빈 칸, 찍히지 않은 도장)은 위치 점수에 넣지 않는다."""
    g = [x for x in gts if _has_box(x)]
    p = [x for x in preds if _has_box(x)]
    pairs = match(p, g, lambda a, b, v: v >= 0.5 and a["key"] == b["key"] and _page(a) == _page(b))
    vl = sum(1 for i, j, _ in pairs if value_ok(p[i], g[j]))

    def f1(hit):
        prec = hit / len(p) if p else (1.0 if not g else 0.0)
        rec = hit / len(g) if g else 1.0
        return 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return {"loc_f1": f1(len(pairs)), "vl_f1": f1(vl), "loc_precision": len(pairs) / len(p) if p else None,
            "loc_recall": len(pairs) / len(g) if g else None}


def s_kie(item, out):
    if isinstance(item["answer"], list):
        return _s_kie2(item, out)
    pred = parse_json(out)
    order = item["eval"].get("order")
    if order is not None and isinstance(pred, list):   # 값만 순서대로 답하는 꼴 (train.swift_import): 개수가 다르면 못 읽은 것
        pred = dict(zip(order, pred)) if len(pred) == len(order) else None
    fail = not isinstance(pred, dict)
    flat = _flatten(pred) if isinstance(pred, dict) else {}
    tp = fp = fn = 0
    correct_all, sub, exact = [], [], []
    for key, gt in item["answer"].items():
        info = item["eval"]["fields"][key]
        p = flat.get(key)
        ok = value_match(p, gt, info["type"], info.get("norm"), key)
        correct_all.append(ok)
        exact.append(p == gt)
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
    metrics = {"field_acc": sum(correct_all) / len(correct_all), "f1": f1, "precision": prec, "recall_f": rec,
               "doc_exact": float(all(correct_all))}
    if order is not None:   # "문서에 적힌 그대로" 를 묻는 질문: 글자 하나까지 같은 비율도 따로
        metrics["field_exact"] = sum(exact) / len(exact)
    return {"metrics": metrics, "parse_fail": fail, "sub": sub}


def _s_kie2(item, out):
    """2.0: 답이 [{"key", "value", "bbox_2d", "page"}] 목록. 값 점수는 1.x 와 같은 계산, 위치·값+위치는 박스로."""
    gts = item["answer"]
    pe = _entries(parse_json(out))
    fail = pe is None
    pe = pe or []
    first: dict[str, dict] = {}
    for e in pe:
        first.setdefault(e["key"], e)
    tp = fp = fn = 0
    correct_all, sub = [], []
    for g in gts:
        key, gt = g["key"], g["value"]
        info = item["eval"]["fields"][key]
        p = first.get(key, {}).get("value")
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
    info = item["eval"]["fields"]
    loc = _located(gts, [e for e in pe if e["key"] in info],
                   lambda a, b: value_match(a.get("value"), b["value"], info[b["key"]]["type"], info[b["key"]].get("norm"), b["key"]))
    return {"metrics": {"field_acc": sum(correct_all) / len(correct_all), "f1": f1, "precision": prec, "recall_f": rec,
                        "doc_exact": float(all(correct_all)), **loc}, "parse_fail": fail, "sub": sub}


def _bool(v):
    if isinstance(v, bool):
        return v
    if v is None:
        return False
    return yes_no(str(v))


def s_marks(item, out):
    if isinstance(item["answer"], list):
        return _s_marks2(item, out)
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


def _s_marks2(item, out):
    """2.0: 답이 목록. 체크박스는 체크된 보기마다 {key, value: 보기 글자, bbox_2d}, 도장·서명은 {key, value: bool, bbox_2d}."""
    types = item["eval"]["types"]
    pe = _entries(parse_json(out))
    fail = pe is None
    pe = pe or []
    by_key: dict[str, list] = {}
    for e in pe:
        by_key.setdefault(e["key"], []).append(e)
    gt_by: dict[str, list] = {}
    for g in item["answer"]:
        gt_by.setdefault(g["key"], []).append(g)
    oks, sub = [], []
    for key, t in types.items():
        gv = [g["value"] for g in gt_by.get(key, [])]
        pv = [e.get("value") for e in by_key.get(key, [])]
        if t in ("seal", "signature"):
            ok = _bool(pv[0] if pv else None) == bool(gv[0])
        elif t == "checkbox_multi":   # 줄마다 보기 하나, 또는 값만 답한 목록 ["A", "C"]
            flat = [y for x in pv for y in (x if isinstance(x, list) else [x])]
            ok = sorted(loose_text(x) for x in flat if not is_null(x)) == sorted(loose_text(x) for x in gv if x is not None)
        else:
            p = next((x for x in pv if not is_null(x)), None)
            ok = value_match(p, gv[0] if gv else None)
        oks.append(ok)
        sub.append(("type", t, ok))

    def value_ok(a, b):
        if types.get(b["key"]) in ("seal", "signature"):
            return _bool(a.get("value")) is True
        return value_match(a.get("value"), b["value"])
    loc = _located(item["answer"], [e for e in pe if e["key"] in types], value_ok)
    return {"metrics": {"acc": sum(oks) / len(oks), **loc}, "parse_fail": fail, "sub": sub}


DOC_CHECK_KEYS = ("missing", "not_required", "not_customer")


def s_doc_check(item, out):
    pred = parse_json(out)
    fail = not isinstance(pred, (dict, list))
    if isinstance(pred, list):  # 목록만 답하면 missing 으로 본다
        pred = {"missing": pred}
    pred = pred if isinstance(pred, dict) else {}
    names = item["eval"].get("names") or item["eval"]["required"]
    tp = fp = fn = 0
    exact = {}
    for k in DOC_CHECK_KEYS:
        gt = set(item["answer"].get(k, []))
        lst = [x for x in (pred.get(k) or []) if not is_null(x)] if isinstance(pred.get(k) or [], list) else [pred.get(k)]
        got = {m for m in (_name_match(str(x), names) for x in lst) if m}
        unmatched = sum(1 for x in lst if _name_match(str(x), names) is None)
        tp += len(got & gt)
        fp += len(got - gt) + unmatched
        fn += len(gt - got)
        exact[k] = got == gt and not unmatched
    f1 = 1.0 if not (tp + fp + fn) else 2 * tp / (2 * tp + fp + fn)
    return {"metrics": {"exact": float(all(exact.values())), "set_f1": f1, "missing_exact": float(exact["missing"]),
                        "not_required_exact": float(exact["not_required"]),
                        "not_customer_exact": float(exact["not_customer"])}, "parse_fail": fail}


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
        ok_docs = {want["document"], *want.get("alt_documents", [])}
        hit = False
        for x in issues:
            doc = _name_match(str(x.get("document") or ""), item["eval"]["documents"])
            if doc not in ok_docs:
                continue
            if (value_match(x.get("value"), want["value"]) or value_match(x.get("expected"), want["value"])
                    or value_match(x.get("value"), want["expected"])
                    or similar_label(want["field"], str(x.get("field") or ""))):
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


def _ocr_slice(item: dict, name: str):
    m = item.get("meta") or {}
    if name == "confidence":
        c = m.get("confidence")
        return None if c is None else ("high" if c >= OM.HIGH_CONFIDENCE else "low")
    return m.get(name)


def _score_ocr(task: str, items: list[dict], preds: dict[str, str]) -> dict:
    """OCR 과제: 옛 1부와 같은 계산 (빈 답·없는 답은 빈 글자, 지표는 과제 전체로). 문항 점수는 GRPO 보상."""
    have = {it["id"]: OM.answer(preds[it["id"]]) for it in items if preds.get(it["id"])}
    rows = [{"id": it["id"], "task": task, "target": it["answer"]} for it in items]
    full = {r["id"]: have.get(r["id"], "") for r in rows}
    calc = OM._text_metrics if task in OM.TEXT_TASKS else OM._box_metrics
    metrics = calc(rows, full)
    main = MAIN[task]
    slices = {}
    for s in SLICES[task]:
        groups: dict = {}
        for it, r in zip(items, rows):
            v = _ocr_slice(it, s)
            if v is not None:
                groups.setdefault(str(v), []).append(r)
        slices[s] = {k: {"n": len(v), main: calc(v, full).get(main)} for k, v in sorted(groups.items(), key=lambda kv: -len(kv[1]))}
    fails = sum(1 for i in have if task in OM.BOX_TASKS and OM.parse_boxes(have[i]) is None)
    per = [{"id": it["id"], main: (rw := OM.reward(preds.get(it["id"]) or "", task, it["answer"])), "reward": rw} for it in items]
    return {"n": len(items), "missing": sum(1 for it in items if it["id"] not in preds), "parse_fail": fails / len(items) if items else 0.0,
            "main": main, "metrics": metrics, "slices": slices, "per_item": per}


def score_task(task: str, items: list[dict], preds: dict[str, str]) -> dict:
    if task in OCR_TASKS:
        return _score_ocr(task, items, preds)
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
    main = main_metric(task, metrics)
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


def reward(task: str, output: str | None, item: dict) -> float:
    """GRPO 보상 [0, 1] — 모든 과제 하나 (train/reward_plugin.py). 답이 없거나 읽을 수 없으면 0.

    OCR 과제: 옛 1부 보상 그대로 (글자 유사도 + 숫자, 박스는 IoU 부드러운 F1).
    업무 과제: 평가 채점기 그대로, 여러 부분 중 다 맞아야 하는 지표는 부분 점수를 준다:
      doc_check    0.5 × 완전 일치 + 0.5 × 세 목록 F1
      cross_check  정상 문항: 맞다고 하면 1 / 변조 문항: 0.5 × (다르다고 함) + 0.5 × (서류·값까지 맞힘)
      ocr_field    1 − CER,  ocr_page 오차 20% 허용 재현율,  그 밖은 주 지표 (kie·marks 값+위치 F1, classify·review 정확도)
    """
    if task in OCR_TASKS:
        return OM.reward(output or "", task, item["answer"])
    if output is None:
        return 0.0
    result = SCORERS[task](item, output)
    if result.get("parse_fail"):
        return 0.0
    m = result["metrics"]
    if task == "doc_check":
        value = 0.5 * m["exact"] + 0.5 * m["set_f1"]
    elif task == "cross_check":
        value = m["score"] if item["answer"]["consistent"] else 0.5 * m["detect"] + 0.5 * m["score"]
    elif task == "ocr_field":
        value = 1.0 - m["cer"]
    elif task == "ocr_page":
        value = m.get("recall_fuzzy", m["recall"])
    else:
        value = m[main_metric(task, m)]
    return float(min(1.0, max(0.0, value)))


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
        from .tracking import evaluate_groups, DIMENSIONS

        tracking = evaluate_groups([it for rows in items.values() for it in rows], preds, res)
        (pred / "report.breakdowns.json").write_text(json.dumps(tracking, ensure_ascii=False, indent=1), encoding="utf-8")
        for dimension, groups in tracking["breakdowns"].items():
            md += f"\n## {DIMENSIONS[dimension]}별 평가\n\n| 구분 | 과제 | 문항 수 | 지표 | 점수 (%) |\n|---|---|---:|---|---:|\n"
            for name, bucket in groups.items():
                for task, result in bucket["tasks"].items():
                    value = result["metrics"].get(result["main"])
                    clean_name = str(name).replace("|", "\\|").replace("\n", " ")
                    md += f"| {clean_name} | {task} | {result['n']} | {result['main']} | {_fmt(value)} |\n"
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
                main = summary[names[0]][t]["main"]
                print(f"| {TASK_TITLE[t]} | {METRIC_TITLE[main]} | "
                      + " | ".join(_fmt(summary[n][t]["metrics"].get(main)) for n in names) + " |")
