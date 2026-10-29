"""채점 함수 견본: VQA 꼴 swift .jsonl (qa_to_swift 로 만든 것, data.benchmark·data.train 의 "format": "swift-fields").
정답(assistant)이 글, JSON 객체·배열·스칼라 어느 것이든 그대로 비교한다.

설정 (경로는 설정 파일 기준, train/configs/ 의 설정이면 ../scorers/…):
  {"id": "vqa-valid", "format": "swift-fields", "paths": ["<vqa .jsonl>"], "scorer": "../scorers/vqa_scorer.py:score"}
학습 데이터(data.train)의 swift .jsonl 에 붙이면 깨진 줄 거르기와 GRPO 보상도 이 함수로 (guide/eval.md 2절).

비교 규칙
  - 정답이 JSON 으로 읽히면 말단 값마다 경로(객체 키·배열 번호)로 비교한다. 객체 키 순서는 무시, 배열 순서는 지킨다.
    빈 객체·빈 배열도 값 하나로 본다 ([] 와 {}·null·없음은 다름). 누락·추가 값도 F1 에 들어간다.
  - 문자열은 Unicode NFC 와 공백(연속·앞뒤)만 맞춘다. 대소문자·문장부호·마스킹([날인] 등)·값 타입(1 과 1.0, "1" 과 1)은 구분한다.
  - 모델 답은 JSON 으로 읽는다 (```json 코드 블록도). 정답이 객체·배열인데 답을 JSON 으로 못 읽으면 parse_fail (모든 지표 0).
    정답이 하나짜리 값(글·숫자·참거짓·null)이면 못 읽은 답은 글 그대로 비교한다: "정례 지원형" 정답에 따옴표 없이
    정례 지원형 이라고 답해도 맞고, 숫자 3 에 "3개" 는 틀림 (못 읽음이 아님).
  - 정답이 JSON 이 아닌 글이면 답도 글로 비교한다 (답이 따옴표로 감싼 글이면 벗겨서).
지표 (문항마다 0~1)
  f1 (주 지표) 정밀도·재현율의 조화평균, precision 쓴 값 중 맞은 것, recall_f·field_acc 정답 값 중 맞힌 것,
  doc_exact 문항 전체 일치, field_exact 공백·NFC 도 맞추지 않고 그대로 같은 값의 비율.
"""
import json
import re
import unicodedata


def _reject_constant(value):
    raise ValueError(f"invalid JSON constant: {value}")


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _parse(text):
    text = text.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*\n?(.*?)\s*```", text, re.S)
    if fenced:
        text = fenced.group(1)
    return json.loads(text, parse_constant=_reject_constant, object_pairs_hook=_object)


def _leaves(value, path=(), normalize=True):
    if isinstance(value, dict) and value:
        result = {}
        for key, child in value.items():
            result.update(_leaves(child, path + (("key", key),), normalize))
        return result
    if isinstance(value, list) and value:
        result = {}
        for index, child in enumerate(value):
            result.update(_leaves(child, path + (("index", index),), normalize))
        return result
    if isinstance(value, str) and normalize:
        value = " ".join(unicodedata.normalize("NFC", value).split())
    # Empty containers are leaves too: [] is different from {}, null and missing.
    return {path: (type(value).__name__, value)}


def score(item, output):
    if "answer" in item:
        answer = item["answer"]
    else:
        answers = [m["content"] for m in item.get("messages", []) if m.get("role") == "assistant"]
        if len(answers) != 1:
            raise ValueError("VQA 정답(assistant)이 하나 있어야 합니다")
        answer = answers[0]
    gold = answer
    structured = not isinstance(answer, str)
    if isinstance(answer, str):
        try:
            gold = _parse(answer)
            structured = True
        except (ValueError, TypeError):
            pass
    parse_fail = not isinstance(output, str) or not output.strip()
    pred = None
    if not parse_fail:
        try:
            pred = _parse(output)
        except (ValueError, TypeError):
            if structured and isinstance(gold, (dict, list)):
                parse_fail = True
            else:   # 하나짜리 값 정답(따옴표 글·숫자 …)이면 답 글 그대로: 따옴표 없이 쓴 같은 글은 맞음, 다른 글은 틀림
                pred = output
        if not structured and not isinstance(pred, str):
            pred = output
    # An explicitly empty string answer must still pass the pipeline oracle check.
    if (not structured and isinstance(answer, str) and not answer.strip()
            and isinstance(output, str) and not output.strip()):
        pred, parse_fail = output, False
    gt = _leaves(gold)
    predicted = {} if parse_fail else _leaves(pred)
    matches = sum(path in predicted and predicted[path] == value for path, value in gt.items())
    precision = matches / len(predicted) if predicted else 0.0
    recall = matches / len(gt)
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    exact_gt = _leaves(gold, normalize=False)
    exact_pred = {} if parse_fail else _leaves(pred, normalize=False)
    exact = sum(path in exact_pred and exact_pred[path] == value for path, value in exact_gt.items())
    return {"metrics": {"f1": f1, "precision": precision, "recall_f": recall,
                        "field_acc": recall, "doc_exact": float(gt == predicted),
                        "field_exact": exact / len(exact_gt)},
            "main": "f1", "parse_fail": parse_fail}
