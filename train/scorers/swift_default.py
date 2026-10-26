"""채점 함수 견본: 실서류 swift 추출 데이터 (data.benchmark 의 "format": "swift-fields"). scorer 를 적지 않은 swift 세트는 이것으로 채점.

swift 세트는 정답(assistant) 글이 그대로 item["answer"] 로 오고, 질문은 item["eval"]["prompt"] 에 있다.
이 견본이 읽는 꼴:
  질문에 'in order: ["필드", …]' 가 있고 정답이 같은 순서의 문자열 배열 ["값", …]   (같은 필드가 두 번이면 두 번째부터 '필드#2')
  또는 정답이 {키: 값} JSON 객체
모델 답은 배열(질문의 필드 순서), {키: 값} 객체, [{"key", "value"}] 목록, [{"value": …}] 로 감싼 배열 모두 읽는다.
배열인데 개수가 필드 수와 다르면 못 읽은 답 (parse_fail → 전부 0).

채점 (docgen studio 기본 정보 추출의 값 점수와 같은 계산)
  필드마다 대소문자·공백·문장부호를 빼고 같으면 맞음 (NO:ILHLR… = NO.ILHLR…). 빈 값("" 또는 null)은 빈 답이어야 맞음.
  f1 (주 지표) = 정밀도(쓴 값 중 맞은 것)·재현율(정답 값 중 맞힌 것)의 조화평균, field_acc 맞은 필드 비율,
  doc_exact 문항 전체 일치, field_exact 글자 하나까지 같은 필드 비율.
다른 기준이 필요하면 이 파일을 복사해 고치고 그 세트에 "scorer": "<복사한 파일>:score" (guide/training.md 3.1절).
"""
import json
import re

from docgen.bench.metrics import is_null, parse_json, value_match

ORDER = re.compile(r"in order:\s*(\[.*?\])", re.S)


def keys_in(prompt):
    """질문의 'in order: [...]' 필드 목록, 같은 필드는 두 번째부터 '#2'. 없으면 None."""
    m = ORDER.search(prompt or "")
    if not m:
        return None
    seen, keys = {}, []
    for f in json.loads(m.group(1)):
        seen[f] = seen.get(f, 0) + 1
        keys.append(f if seen[f] == 1 else f"{f}#{seen[f]}")
    return keys


def as_dict(value, keys):
    """정답·모델 답 → {키: 값}. 못 읽으면 None."""
    if isinstance(value, dict):
        return value
    if isinstance(value, list) and value and all(isinstance(x, dict) and "key" in x for x in value):
        out = {}
        for x in value:
            out.setdefault(x["key"], x.get("value"))
        return out
    if isinstance(value, list) and keys and len(value) == len(keys):
        return dict(zip(keys, [x["value"] if isinstance(x, dict) and set(x) == {"value"} else x for x in value]))
    return None


def score(item, output):
    keys = keys_in((item.get("eval") or {}).get("prompt") or item.get("prompt"))
    gold = as_dict(parse_json(item["answer"]) if isinstance(item["answer"], str) else item["answer"], keys)
    if gold is None:
        raise ValueError("정답을 읽지 못했습니다 ('in order' 질문 + 배열, 또는 {키: 값} 객체가 아님). 이 세트에 맞는 scorer 를 붙이세요")
    pred = as_dict(parse_json(output), keys)
    if pred is None:
        return {"metrics": {"f1": 0.0, "field_acc": 0.0, "doc_exact": 0.0, "field_exact": 0.0}, "main": "f1", "parse_fail": True}
    tp = fp = fn = 0
    oks, exact = [], []
    for key, gt in gold.items():
        p = pred.get(key)
        ok = value_match(p, gt, "text", None, key)
        oks.append(ok)
        exact.append(p == gt)
        if gt is not None:
            tp += ok
            fn += not ok
            fp += (not ok) and not is_null(p)
        elif not is_null(p):
            fp += 1
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"metrics": {"f1": f1, "precision": precision, "recall_f": recall, "field_acc": sum(oks) / len(oks) if oks else 1.0,
                        "doc_exact": float(all(oks)), "field_exact": sum(exact) / len(exact) if exact else 1.0},
            "main": "f1"}
