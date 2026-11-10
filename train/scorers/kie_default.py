"""채점 함수 견본: docgen studio 기본 정보 추출(kie) 채점의 값 점수와 같은 계산을 풀어 쓴 것. 복사해서 고쳐 쓴다.
(합성 세트 전체는 bank_default.py, 쪽 OCR 은 ocr_default.py. 이 파일은 실서류 추출 세트처럼 값만 볼 때.)
(다른 점: 질문 꼴과 상관없이 답 꼴 세 가지를 다 읽는다, 날짜는 아래 ymd 로 비교. 위치 점수는 없음.)

설정 (data.benchmark 의 평가 세트 하나에):
  {"id": "real-fx-po", "format": "swift-fields", "paths": ["…/eval_qa_PO.jsonl"],
   "scorer": "scorers/my_po.py:score"}          ← 설정 파일 기준 상대 경로, ':함수' 를 빼면 score
고친 뒤에는 학습 없이 다시 채점: python -m train report <결과 폴더> --rescore (guide/train/steps.md).

함수 꼴
  score(item, output) -> {"metrics": {이름: 0~1, …}, "main": 주 지표 이름, "parse_fail": bool}
  - item: 평가 문항. item["answer"] 정답 ({키: 값}, [{"key", "value"}, …], 또는 swift 답 글 그대로), item["eval"]["fields"][키]["type"], item["meta"]
  - output: 모델 답 (앞의 <think>…</think> 는 뗀 것). 답이 없으면 "".
  - metrics: 문항마다 0~1. 평가 세트 점수는 문항 평균. 비교표에는 main 이 주 지표로 나온다.
  - parse_fail=True 면 그 문항은 모든 지표가 0 (답을 못 읽음 비율에 따로 잡힘).
  - 위치(bbox) 점수는 내지 않는다. 그림 위치까지 보려면 studio 기본 채점(scorer 없음)을 쓴다.
"""
import re

from docgen.bench.metrics import is_null, parse_json, value_match

# 항목별 비교 기준. 정답 파일의 타입보다 우선. 키 이름 → text | amount | number | date | digits (밑의 설명)
#   text   대소문자·공백·문장부호를 빼고 같으면 맞음 (기본)     amount·number  숫자 값이 같으면 (58,546.70 = 58546.7)
#   date   같은 날짜면 (2025 05 21 = 2025-05-21 = 20250521)      digits         숫자만 비교 (NO:IL-0120 = 0120)
FIELD_TYPES: dict[str, str] = {}
# 예: FIELD_TYPES = {"AMT_VALUE": "amount", "DATE": "date", "DATE_FORMAT": "digits"}


def ymd(text):
    """날짜 글자 → (년, 월, 일). '2025 05 21', '2025-05-21', '2025.5.21', '20250521', '2025년 5월 21일'. 못 읽으면 None."""
    nums = re.findall(r"\d+", str(text or ""))
    if len(nums) == 1 and len(nums[0]) == 8:
        nums = [nums[0][:4], nums[0][4:6], nums[0][6:]]
    if len(nums) != 3:
        return None
    y, m, d = (int(x) for x in nums)
    return (y + 2000 if y < 100 else y, m, d)


def same(p, gt, kind, key, norm=None):
    """항목 하나가 맞았는지. 날짜는 위 ymd 로, 그 밖은 docgen 기본 비교 (docgen.bench.metrics.value_match)."""
    if kind == "date" and gt is not None and not is_null(p):
        return ymd(gt) is not None and ymd(p) == ymd(gt)
    return value_match(p, gt, {"digits": "account_no"}.get(kind, kind), norm, key)   # digits: 숫자만 비교하는 docgen 타입


def read_answer(output):
    """모델 답 → {키: 값}. 목록 [{"key", "value"}], 객체 {키: 값}, 값만 순서대로 ["값", …] (swift 원래 꼴) 모두."""
    pred = parse_json(output)
    if isinstance(pred, list) and pred and all(isinstance(x, dict) and "key" in x for x in pred):
        out = {}
        for x in pred:
            out.setdefault(x["key"], x.get("value"))   # 같은 키는 첫 번째만
        return out
    if isinstance(pred, dict):
        return pred
    return pred   # 순서 배열이거나 못 읽음 (score 가 처리)


def score(item, output):
    gold = item["answer"]
    if isinstance(gold, str):     # 정답이 글 그대로인 세트 (swift 답이 기본 꼴이 아닐 때): 모델 답과 같은 방법으로 읽는다
        gold = read_answer(gold)
    gold = {g["key"]: g["value"] for g in gold} if isinstance(gold, list) else gold
    if not isinstance(gold, dict):
        raise ValueError("정답을 {키: 값} 으로 읽지 못했습니다. 이 세트에 맞게 score 를 고치세요")
    pred = read_answer(output)
    order = (item.get("eval") or {}).get("order")
    if isinstance(pred, list) and order and len(pred) == len(order):   # ["값", …]: 질문의 필드 순서로 짝짓기
        pred = dict(zip(order, [x["value"] if isinstance(x, dict) and set(x) == {"value"} else x for x in pred]))
    elif isinstance(pred, list) and not order:   # 목록 꼴로 물었는데 키 없는 목록: 읽기는 했지만 맞은 칸 없음
        pred = {}
    if not isinstance(pred, dict):
        return {"metrics": {"f1": 0.0, "field_acc": 0.0, "doc_exact": 0.0}, "main": "f1", "parse_fail": True}
    fields = (item.get("eval") or {}).get("fields", {})
    tp = fp = fn = 0
    oks = []
    for key, gt in gold.items():
        kind = FIELD_TYPES.get(key.split("#")[0]) or fields.get(key, {}).get("type", "text")
        p = pred.get(key)
        ok = same(p, gt, kind, key, fields.get(key, {}).get("norm"))
        oks.append(ok)
        if gt is not None:            # 값이 있는 칸: 맞으면 tp, 틀리면 fn (+ 틀린 값을 썼으면 fp)
            tp += ok
            fn += not ok
            fp += (not ok) and not is_null(p)
        elif not is_null(p):          # 빈 칸에 값을 지어냄
            fp += 1
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"metrics": {"f1": f1, "precision": precision, "recall_f": recall,
                        "field_acc": sum(oks) / len(oks) if oks else 1.0, "doc_exact": float(all(oks))},
            "main": "f1"}
