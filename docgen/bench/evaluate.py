"""채점 — OCR 8과제(ocr_metrics)와 은행 업무 8과제 모두 여기서 (archive/studio/DESIGN.md 17절). GRPO 보상도 reward() 하나.

  python -m docgen.bench eval --bench bench_out --pred preds/model_a [--pred preds/model_b ...]

예측 파일: <pred 폴더>/*.jsonl, 한 줄에 {"id": 문항 id, "output": 모델 출력 문자열}.
예측이 없는 문항은 틀린 것으로 센다 (보고서에 '예측 없음'으로 따로 표시).
결과: <pred 폴더>/report.json, report.md. 예측 폴더가 여러 개면 과제별 주 지표를 비교표로 출력한다.
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

from ..schema import similar_label
from . import ocr_metrics as OM
from .metrics import (cer, is_null, loose_text, match, norm_text, parse_json, strip_answer, substring_distance, to_number,
                      valid_box, value_match, yes_no)

OCR_TASKS = list(OM.TASKS)   # 쪽 OCR (옛 1부): 문항마다가 아니라 과제 전체로 지표를 낸다 (CER = 틀린 글자 합 / 글자 합)
TABLE_TASKS = ["table", "table_read", "table_find", "table_qa"]
TASK_ORDER = [*OCR_TASKS, "ocr_field", "ocr_page", "classify", "kie", "marks", "freetext", "form_qa", *TABLE_TASKS]
TASK_TITLE = {"crop_ocr": "OCR - 칸 잘라 읽기", "bbox_ocr": "OCR - 좌표 → 글자", "region_ocr": "OCR - 영역 받아쓰기",
              "marked_ocr": "OCR - 그린 박스 → 글자", "grounding": "OCR - 글자 → 좌표", "spotting": "OCR - 글자 찾기(좌표+글자)",
              "relation": "OCR - 항목명 → 값(좌표+글자)", "marked_box": "OCR - 그린 박스 → 좌표",
              "ocr_field": "OCR - 값 칸 인식", "ocr_page": "OCR - 전체 받아쓰기", "classify": "서류 분류",
              "kie": "정보 추출", "marks": "체크·도장·서명", "freetext": "기타 칸 정리", "form_qa": "서식 전용 질문",
              "table": "표 추출", "table_read": "표 그대로 옮기기", "table_find": "표 찾기", "table_qa": "표 질의"}
TASK_GROUP = {**{t: "ocr" for t in [*OCR_TASKS, "ocr_field", "ocr_page"]}, "classify": "doc", "kie": "doc", "marks": "doc",
              "freetext": "doc", "form_qa": "doc", **{t: "doc" for t in TABLE_TASKS}}
GROUP_TITLE = {"ocr": "OCR", "doc": "문서 이해"}
WORST = {"cer": 1.0, "false_alarm": 1.0, "extra_key": 1.0}
LOWER_IS_BETTER = {"cer", "false_alarm", "matched_label_cer", "extra_key"}
# OCR 과제의 대표 지표는 옛 1부 비교표(REPORT_METRICS)와 같다
MAIN = {"crop_ocr": "cer", "bbox_ocr": "em", "region_ocr": "cer", "marked_ocr": "em", "grounding": "f1_iou50",
        "spotting": "e2e_f1", "relation": "e2e_f1", "marked_box": "f1_iou75",
        "ocr_field": "exact", "ocr_page": "recall", "classify": "acc", "kie": "vl_f1", "marks": "vl_f1", "freetext": "f1",
        "form_qa": "acc", "table": "cell_f1", "table_read": "cell_f1", "table_find": "f1_iou50", "table_qa": "acc"}
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
                "matched_label_cer": "맞은 박스 글자 CER", "extra_key": "지어낸 키 비율(낮을수록 좋음)",
                "approx_acc": "대략 표시 일치", "cell_f1": "칸 F1", "cell_precision": "칸 정밀도", "cell_recall": "칸 재현율",
                "row_exact": "행 완전 일치", "count_acc": "행 수 일치", "header_f1": "머리글 F1", "rows_acc": "행 수 맞춤(찾은 표)",
                "absent_null": "없는 열·칸 null 비율"}
SLICES = {"ocr_field": ["writing", "condition", "kind", "corrected"], "ocr_page": ["condition", "writing", "group"],
          "classify": ["group", "condition"], "kie": ["group", "condition", "writing", "@kind"],
          "marks": ["group", "condition", "@type"], "freetext": ["group", "writing", "level", "@key"],
          "form_qa": ["doc_type", "question"],
          "table": ["group", "condition", "ref", "scope", "absent", "@kind"], "table_read": ["group", "condition", "ref", "scope"],
          "table_find": ["group", "condition"], "table_qa": ["group", "kind"],
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


def _no_loc(item, loc: dict) -> dict:
    """서식의 답 틀(questions.json 의 answer)에 위치(bbox_2d)가 없는 문항은 위치 점수를 빼고 값 점수가 주 지표."""
    names = (item.get("eval") or {}).get("answer_fields")
    return {} if names and "bbox_2d" not in names else loc


def _from_text(item, out):
    """줄글 답 문항 (서식 questions.json 의 답 틀이 글자, eval.text): 정답은 eval.gold, 모델 답은 틀로 줄글에서 값을 찾아
    [{"key", "value"}] 로 — 그다음은 JSON 답과 같은 채점 (위치 점수 없음)."""
    from .. import formquestions as FQ

    t = item["eval"]["text"]
    pred = FQ.read_text(out or "", t["answer"], t["answer_empty"], t["labels"]) if out is not None else None
    item = {**item, "answer": item["eval"]["gold"], "eval": {**item["eval"], "answer_fields": {"key": "key", "value": "value"}}}
    return item, (None if pred is None else json.dumps(pred, ensure_ascii=False))


def _canonical(item, out):
    """서식의 답 틀이 칸 이름을 바꿨으면 (eval.answer_fields: {"key": "항목", …}) 정답·모델 답을 기본 이름으로 읽는다."""
    names = (item.get("eval") or {}).get("answer_fields")
    if not names:
        return item, out
    inv = {name: place for place, name in names.items()}

    def ren(e):
        return {inv.get(k, k): v for k, v in e.items()} if isinstance(e, dict) else e
    if isinstance(item.get("answer"), list):
        item = {**item, "answer": [ren(e) for e in item["answer"]]}
    pred = parse_json(out)
    if isinstance(pred, list):
        out = json.dumps([ren(e) for e in pred], ensure_ascii=False)
    return item, out


def s_kie(item, out):
    if (item.get("eval") or {}).get("text"):
        return _s_kie2(*_from_text(item, out))
    item, out = _canonical(item, out)
    if isinstance(item["answer"], list):
        return _s_kie2(item, out)
    pred = parse_json(out)
    order = item["eval"].get("order")
    if order is not None and isinstance(pred, list):   # 값만 순서대로 답하는 꼴 (train.swift_import): 개수가 다르면 못 읽은 것
        pred = [x["value"] if isinstance(x, dict) and set(x) == {"value"} else x for x in pred]   # [{"value": …}] 로 감싼 답도 값으로
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
                        "doc_exact": float(all(correct_all)), **_no_loc(item, loc)}, "parse_fail": fail, "sub": sub}


def _bool(v):
    if isinstance(v, bool):
        return v
    if v is None:
        return False
    return yes_no(str(v))


def s_marks(item, out):
    if (item.get("eval") or {}).get("text"):
        return _s_marks2(*_from_text(item, out))
    item, out = _canonical(item, out)
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
    return {"metrics": {"acc": sum(oks) / len(oks), **_no_loc(item, loc)}, "parse_fail": fail, "sub": sub}


# ---------------------------------------------------------------------------
# 표 (docgen/bench/tasks/table*.py): 답 {"columns", "rows": [[…]], "row_boxes": [{"bbox_2d", "page"}]}
# ---------------------------------------------------------------------------

def _table_pred(pred, columns: list[str]):
    """모델 답 → (행 [[정답 열 순서의 값]], 행 상자 [dict]). 읽을 수 없으면 None.
    받는 꼴: {"columns", "rows": [[…]]} (열 이름으로 맞춤), 행마다 객체 {"rows": [{열: 값}]} 또는 [{열: 값}] 목록."""
    if isinstance(pred, list):
        pred = {"rows": pred}
    if not isinstance(pred, dict) or not isinstance(pred.get("rows"), list):
        return None
    norm = {re.sub(r"\s+", "", str(c)).lower(): c for c in columns}
    cols = pred.get("columns")
    order = [norm.get(re.sub(r"\s+", "", str(c)).lower()) for c in cols] if isinstance(cols, list) else None
    rows, boxes = [], []
    for r in pred["rows"]:
        if isinstance(r, dict):
            m = {norm.get(re.sub(r"\s+", "", str(k)).lower()): v for k, v in r.items()}
            rows.append([m.get(c) for c in columns])
            boxes.append({"bbox_2d": r.get("bbox_2d"), "page": r.get("page")})
        elif isinstance(r, list):
            if order is not None:
                m = {c: v for c, v in zip(order, r) if c}
                rows.append([m.get(c) for c in columns])
            else:
                rows.append([r[i] if i < len(r) else None for i in range(len(columns))])
        else:
            return None
    rb = pred.get("row_boxes")
    if isinstance(rb, list):
        boxes = [b if isinstance(b, dict) else {} for b in rb]
    return rows, boxes


def _align_rows(gold: list[list], pred: list[list], same) -> list[tuple[int, int]]:
    """정답 행과 답한 행을 순서대로 짝짓기 (빠지거나 더 들어간 행 허용): 맞은 칸 비율의 합이 가장 큰 짝들.
    same(i, j, c) → 칸이 맞는지. 맞은 칸이 하나도 없는 짝은 짓지 않는다."""
    m, n = len(gold), len(pred)
    if not m or not n:
        return []
    sc = [[0.0] * n for _ in range(m)]
    for i in range(m):
        want = [c for c, v in enumerate(gold[i]) if v is not None] or list(range(len(gold[i])))
        for j in range(n):
            sc[i][j] = sum(same(i, j, c) for c in want) / len(want)
    best = [[0.0] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            best[i][j] = max(best[i + 1][j], best[i][j + 1], (sc[i][j] + best[i + 1][j + 1]) if sc[i][j] > 0 else 0.0)
    pairs, i, j = [], 0, 0
    while i < m and j < n:
        if sc[i][j] > 0 and abs(best[i][j] - (sc[i][j] + best[i + 1][j + 1])) < 1e-9:
            pairs.append((i, j))
            i, j = i + 1, j + 1
        elif best[i][j] == best[i + 1][j]:
            i += 1
        else:
            j += 1
    return pairs


def _row_loc(gb: list[dict], pb: list[dict], pairs) -> float:
    """행 위치 F1: 짝지은 행끼리 같은 쪽·IoU 0.5 이상. 상자가 없는 정답 행은 세지 않는다."""
    from .metrics import iou

    g = sum(1 for b in gb if valid_box((b or {}).get("bbox_2d")))
    p = sum(1 for b in pb if valid_box((b or {}).get("bbox_2d")))
    hit = 0
    for i, j in pairs:
        a, b = (gb[i] if i < len(gb) else {}) or {}, (pb[j] if j < len(pb) else {}) or {}
        if valid_box(a.get("bbox_2d")) and valid_box(b.get("bbox_2d")) and _page(a) == _page(b) and iou(a["bbox_2d"], b["bbox_2d"]) >= 0.5:
            hit += 1
    if not g:
        return None
    prec = hit / p if p else 0.0
    rec = hit / g
    return 2 * prec * rec / (prec + rec) if prec + rec else 0.0


def _cells(gold: list[list], pred: list[list], pairs, ok, kinds: list[str]):
    """칸 단위 (tp, fp, fn, 행 완전 일치 수, sub). ok(i, j, c) → 그 칸이 맞는지 (정답 null 이면 답도 비어야 맞음)."""
    tp = fp = fn = exact = 0
    sub = []
    got = {i: j for i, j in pairs}
    used = set(got.values())
    for i, grow in enumerate(gold):
        j = got.get(i)
        all_ok = j is not None
        for c, g in enumerate(grow):
            p = pred[j][c] if j is not None else None
            good = ok(i, j, c) if j is not None else g is None
            all_ok &= good
            if g is not None:
                tp += good
                fn += not good
                fp += (not good) and j is not None and not is_null(p)
                sub.append(("kind", kinds[c], good))
            elif j is not None and not is_null(p):
                fp += 1
                sub.append(("kind", kinds[c], False))
        exact += all_ok
    for j, prow in enumerate(pred):
        if j not in used:
            fp += sum(1 for v in prow if not is_null(v))
    return tp, fp, fn, exact, sub


def s_table(item, out):
    """표 추출: 행을 순서대로 짝지은 뒤 칸 F1 (주 지표). 행 완전 일치, 행 수 일치, 행 위치 F1, 없는 열을 null 로 둔 비율."""
    gold = item["answer"]
    columns = gold["columns"]
    info = item["eval"]["fields"]
    parsed = _table_pred(parse_json(out), columns)
    fail = parsed is None
    prows, pboxes = parsed or ([], [])
    grows = gold["rows"]

    def ok(i, j, c):
        k = columns[c]
        return value_match(prows[j][c], grows[i][c], info[k]["type"], None, k)
    pairs = _align_rows(grows, prows, lambda i, j, c: grows[i][c] is not None and ok(i, j, c))
    tp, fp, fn, exact, sub = _cells(grows, prows, pairs, ok, [info[k].get("kind", "text") for k in columns])
    prec = tp / (tp + fp) if tp + fp else 1.0
    rec = tp / (tp + fn) if tp + fn else 1.0
    m = {"cell_f1": 2 * prec * rec / (prec + rec) if prec + rec else 0.0, "cell_precision": prec, "cell_recall": rec,
         "row_exact": exact / len(grows) if grows else float(not prows), "count_acc": float(len(prows) == len(grows))}
    loc = _row_loc(gold.get("row_boxes") or [], pboxes, pairs)
    if loc is not None:
        m["loc_f1"] = loc
    absent = (item.get("eval") or {}).get("absent") or []
    if absent and prows:
        idx = [columns.index(a) for a in absent if a in columns]
        m["absent_null"] = sum(is_null(r[c]) for r in prows for c in idx) / (len(prows) * len(idx)) if idx else 1.0
    return {"metrics": m, "parse_fail": fail, "sub": sub}


def _head_key(h) -> str:
    return norm_text(str(h or "")).replace(">", "")


def s_table_read(item, out):
    """표 그대로 옮기기: 머리글을 글자로 짝지은 뒤(같은 글자 → 비슷한 글자 → 같은 개수면 자리) table 과 같은 칸 F1. 머리글 F1 도."""
    gold = item["answer"]
    gcols = gold["columns"]
    pred = parse_json(out)
    pcols = pred.get("columns") if isinstance(pred, dict) and isinstance(pred.get("columns"), list) else None
    names = [f"c{i}" for i in range(len(gcols))]
    mapped = None
    if pcols is not None:
        gk = [_head_key(h) for h in gcols]
        used, mapped = set(), []
        for h in pcols:
            k = _head_key(h)
            j = next((j for j, x in enumerate(gk) if x == k and j not in used), None)
            if j is None:
                best = max(((difflib.SequenceMatcher(None, k, x).ratio(), j) for j, x in enumerate(gk) if j not in used), default=(0, None))
                j = best[1] if best[0] >= 0.8 else None
            if j is None and len(pcols) == len(gcols) and len(mapped) not in used:
                j = len(mapped)
            if j is not None:
                used.add(j)
            mapped.append(names[j] if j is not None else f"x{len(mapped)}")
        pred = {**pred, "columns": mapped}
        hit = len(used)
        prec, rec = (hit / len(pcols) if pcols else 0.0), (hit / len(gcols) if gcols else 1.0)
        head = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    else:
        head = 0.0
    item2 = {**item, "answer": {**gold, "columns": names},
             "eval": {"fields": {n: {"type": "text", "kind": "text"} for n in names}}}
    r = s_table(item2, json.dumps(pred, ensure_ascii=False) if pred is not None else out)
    r["metrics"]["header_f1"] = head
    return r


def s_table_find(item, out):
    """표 찾기: 같은 쪽·IoU 0.5 이상 짝 F1 (주 지표), 표 수 일치, 짝지은 표의 행 수 일치, 머리글 F1(짝지은 표의 평균)."""
    gold = item["answer"]
    pred = parse_json(out)
    fail = not isinstance(pred, list)
    p = [x for x in (pred or []) if isinstance(x, dict) and valid_box(x.get("bbox_2d"))] if not fail else []
    pairs = match(p, gold, lambda a, b, v: v >= 0.5 and _page(a) == _page(b))

    def f1(hit):
        prec = hit / len(p) if p else (1.0 if not gold else 0.0)
        rec = hit / len(gold) if gold else (1.0 if not p else 0.0)
        return 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    rows_ok = [to_number(p[i].get("n_rows")) == gold[j]["n_rows"] for i, j, _ in pairs]
    heads = []
    for i, j, _ in pairs:
        g = {_head_key(h) for h in gold[j].get("columns") or []}
        q = {_head_key(h) for h in p[i].get("columns") or []} if isinstance(p[i].get("columns"), list) else set()
        hit = len(g & q)
        heads.append(2 * hit / (len(g) + len(q)) if g or q else 1.0)
    m = {"f1_iou50": f1(len(pairs)), "count_acc": float(len(p) == len(gold)),
         "rows_acc": sum(rows_ok) / len(rows_ok) if rows_ok else (1.0 if not gold and not p else 0.0)}
    if heads:
        m["header_f1"] = sum(heads) / len(heads)
    return {"metrics": m, "parse_fail": fail}


def s_table_qa(item, out):
    """표 질의: 숫자는 같은 수, 칸 값은 kie 와 같은 비교 (정답이 빈 칸이면 답도 비어야). 주 지표 acc."""
    ev = item["eval"]
    if out is None:
        return {"metrics": {"acc": 0.0}, "parse_fail": True}
    a = strip_answer(out) if isinstance(out, str) else out
    if ev["answer_type"] == "number":
        n = to_number(a)
        ok = n is not None and abs(n - float(item["answer"])) < 1e-6
    else:
        ok = value_match(a, item["answer"], ev.get("type"), None, ev.get("key") or "")
    return {"metrics": {"acc": float(ok)}}


def s_number_yesno(item, out):
    """숫자 답 (단위 %·배·세·년·원을 떼고 eval.tol 안이면 정답) 또는 예/아니오 답 (네·아니요도 인정)."""
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


def s_form_qa(item, out):
    """서식 전용 질문 (서식 폴더 qa.py, docgen/formqa.py): 정답 꼴(eval.answer_type)로 기본 채점.
    number·yesno 는 s_number_yesno, text 는 띄어쓰기·문장부호를 맞춰 같은지, json 은 칸(목록은 항목)마다 같은지."""
    kind = item["eval"]["answer_type"]
    if kind in ("number", "yesno"):
        return s_number_yesno(item, out)
    gt = item["answer"]
    if kind == "json":
        pred = parse_json(out)
        if not isinstance(pred, (dict, list)):
            return {"metrics": {"acc": 0.0}, "parse_fail": True}
        if isinstance(gt, dict):
            flat = pred if isinstance(pred, dict) else {}
            oks = [_same_value(flat.get(k), v) for k, v in gt.items()]
            extra = [k for k in flat if k not in gt]
            return {"metrics": {"acc": sum(oks) / (len(oks) + len(extra)) if oks or extra else 1.0}}
        ps = [json.dumps(x, ensure_ascii=False, sort_keys=True) for x in (pred if isinstance(pred, list) else [pred])]
        gs = [json.dumps(x, ensure_ascii=False, sort_keys=True) for x in gt]
        return {"metrics": {"acc": float(sorted(map(loose_text, ps)) == sorted(map(loose_text, gs)))}}
    p = (out or "") if "\n" in str(gt) else strip_answer(out) if out is not None else ""
    return {"metrics": {"acc": float(loose_text(p) == loose_text(str(gt)))}}


def _same_value(p, g) -> bool:
    """JSON 정답의 칸 하나: 숫자는 숫자로, 글은 띄어쓰기·문장부호를 맞춰, 그 밖(목록·객체)은 같은 꼴로."""
    if isinstance(g, bool) or isinstance(p, bool):
        return _bool(p) == _bool(g)
    if isinstance(g, (int, float)):
        n = to_number(p) if not isinstance(p, (int, float)) else p
        return n is not None and abs(n - g) < 1e-9
    if g is None:
        return is_null(p)
    if isinstance(g, (dict, list)):
        return loose_text(json.dumps(p, ensure_ascii=False, sort_keys=True)) == loose_text(json.dumps(g, ensure_ascii=False, sort_keys=True))
    return p is not None and loose_text(str(p)) == loose_text(str(g))


def _freetext_ok(key: str, pred, gt) -> bool:
    """기타 칸 정리: 금액·기간·날짜·보기는 정확히 같아야 맞음, memo 만 띄어쓰기·문장부호 차이 허용."""
    if is_null(pred):
        return False
    if key in ("amount", "period_months"):
        n = to_number(str(pred))
        return n is not None and abs(n - gt) < 1e-6
    if key == "memo":
        return loose_text(str(pred)) == loose_text(gt)
    return norm_text(str(pred)) == norm_text(str(gt))


def s_freetext(item, out):
    """답: {"purpose", "amount", …, "approx": [키]}. 적히지 않은 키는 정답에 없다 → 그 키를 답하면 지어낸 것 (extra_key)."""
    gt = {k: v for k, v in item["answer"].items() if k != "approx"}
    pred = parse_json(out)
    fail = not isinstance(pred, dict)
    pred = pred if isinstance(pred, dict) else {}
    said = {k: v for k, v in pred.items() if k != "approx" and not is_null(v)}
    ok = {k: _freetext_ok(k, said.get(k), v) for k, v in gt.items()}
    tp = sum(ok.values())
    extra = [k for k in said if k not in gt]
    fp = len(extra) + sum(1 for k in gt if k in said and not ok[k])
    prec = tp / (tp + fp) if tp + fp else 1.0
    rec = tp / len(gt) if gt else 1.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    approx = pred.get("approx") if isinstance(pred.get("approx"), list) else []
    approx_ok = sorted(map(str, approx)) == sorted(item["answer"].get("approx", []))
    return {"metrics": {"f1": f1, "field_acc": tp / len(gt) if gt else 1.0, "precision": prec, "recall_f": rec,
                        "extra_key": len(extra) / len(said) if said else 0.0, "approx_acc": float(approx_ok),
                        "doc_exact": float(tp == len(gt) and not extra and approx_ok)},
            "parse_fail": fail, "sub": [("key", k, v) for k, v in ok.items()]}


SCORERS = {"classify": s_classify, "ocr_field": s_ocr_field, "ocr_page": s_ocr_page, "kie": s_kie, "marks": s_marks,
           "freetext": s_freetext, "form_qa": s_form_qa, "table": s_table, "table_read": s_table_read,
           "table_find": s_table_find, "table_qa": s_table_qa}


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


def answer_text(out):
    """모델 출력에서 앞의 생각 블록(<think>…</think>, 비어 있어도)을 뗀 답. 생각을 끄고 학습한 모델도 빈 블록을 낸다.
    OCR 과제(ocr_metrics.answer)와 같은 규칙."""
    return OM.answer(out) if isinstance(out, str) else out


_CUSTOM: dict = {}


def load_scorer(spec: str):
    """평가 세트마다 넣는 채점 함수 '<파일.py>:<함수>' (함수를 빼면 score). 꼴은 train/scorers/kie_default.py.
    함수(item, output) -> {"metrics": {이름: 0~1}, "main"?: 주 지표 이름, "parse_fail"?: bool}. output 은 생각 블록을 뗀 답."""
    import importlib.util

    path, _, name = spec.partition(":")
    key = (path, Path(path).stat().st_mtime if Path(path).is_file() else None, name or "score")
    if key not in _CUSTOM:
        if not Path(path).is_file():
            raise ValueError(f"채점 함수 파일이 없습니다: {path}")
        mod_spec = importlib.util.spec_from_file_location(f"docgen_scorer_{abs(hash(key))}", path)
        mod = importlib.util.module_from_spec(mod_spec)
        mod_spec.loader.exec_module(mod)
        fn = getattr(mod, name or "score", None)
        if not callable(fn):
            raise ValueError(f"{path} 에 함수 {name or 'score'} 가 없습니다")
        _CUSTOM[key] = fn
    return _CUSTOM[key]


def score_task(task: str, items: list[dict], preds: dict[str, str]) -> dict:
    custom = any((it.get("eval") or {}).get("scorer") for it in items)
    if task in OCR_TASKS and not custom:
        return _score_ocr(task, items, preds)
    rows, missing, fails = [], 0, 0
    for it in items:
        spec = (it.get("eval") or {}).get("scorer")
        fn = load_scorer(spec) if spec else SCORERS[task]
        out = answer_text(preds.get(it["id"]))
        if it["id"] not in preds:
            missing += 1
        try:
            r = fn(it, out if out is not None or not spec else "")
        except Exception as exc:  # noqa: BLE001  사용자 채점 함수의 오류는 어느 문항인지와 함께
            raise ValueError(f"채점 함수 {spec or task} 가 문항 {it['id']} 에서 실패: {type(exc).__name__}: {exc}") from exc
        fails += bool(r.get("parse_fail")) and out is not None
        if out is None or r.get("parse_fail"):  # 예측 없음·파싱 실패는 최악 점수 (빈 답이 null 칸·'도장 없음'을 맞히지 않게)
            r = {"metrics": {k: WORST.get(k, 0.0) for k in r["metrics"]},
                 "sub": [(n, v, False) for n, v, _ in r.get("sub", [])], **({"main": r["main"]} if r.get("main") else {})}
        rows.append((it, r))
    metrics = {}
    for k in {k for _, r in rows for k in r["metrics"]}:
        metrics[k] = _mean([r["metrics"].get(k) for _, r in rows])
    slices = {}
    mains = {r.get("main") for _, r in rows}
    main = mains.pop() if len(mains) == 1 and None not in mains else main_metric(task, metrics)   # 채점 함수가 정한 주 지표
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
    """문항 점수 [0, 1] — 모든 과제 하나 (train/mix.py 의 정답 만점 검사). 답이 없거나 읽을 수 없으면 0.

    OCR 과제: 옛 1부 보상 그대로 (글자 유사도 + 숫자, 박스는 IoU 부드러운 F1).
    그 밖: ocr_field 1 − CER,  ocr_page 오차 20% 허용 재현율,  나머지는 주 지표 (kie·marks 값+위치 F1, classify 정확도)
    채점 함수를 붙인 문항(eval.scorer — swift .jsonl 학습 데이터): 그 함수의 주 지표 (낮을수록 좋은 지표는 1 − 값).
    """
    spec = (item.get("eval") or {}).get("scorer")
    if task in OCR_TASKS and not spec:
        return OM.reward(output or "", task, item["answer"])
    if output is None:
        return 0.0
    if spec:   # 채점 함수를 붙인 학습 문항 (swift .jsonl 학습 데이터): 그 함수의 주 지표
        result = load_scorer(spec)(item, answer_text(output))
        if result.get("parse_fail"):
            return 0.0
        m = result["metrics"]
        main = result.get("main") or main_metric(task, m)
        v = m.get(main)
        if v is None:
            return 0.0
        return float(min(1.0, max(0.0, 1.0 - v if main in LOWER_IS_BETTER else v)))
    result = SCORERS[task](item, answer_text(output))
    if result.get("parse_fail"):
        return 0.0
    m = result["metrics"]
    if task == "ocr_field":
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
