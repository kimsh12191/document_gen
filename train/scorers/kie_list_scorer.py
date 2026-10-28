"""채점 함수 견본: 학습과 같은 kie 꼴로 바꾼 실서류 .jsonl (temp/swift_to_kie_v3_tmp.py, data.benchmark 의 "format": "swift-fields").

바꾼 파일의 꼴
  질문: 합성 kie 와 같은 문장 (docgen/bench/prompts.py 의 P_KIE) + '- 키: 항목명' 줄들
  정답: [{"key": 키, "value": 값 또는 null}, …] 목록 — 위치(bbox_2d·page)는 없다 (실서류에 위치 정답이 없어서)
채점은 합성 kie 와 같은 함수 (docgen.bench.evaluate.s_kie 의 목록 꼴): 키마다 값이 같은 뜻인지, 주 지표 f1.
정답에 위치가 없으므로 위치 점수(loc_f1·vl_f1)는 빼고 값 점수만 남긴다 — 그대로 두면 모델이 위치까지 답할 때 값+위치 점수가
0 으로 계산되어 주 지표가 0 이 된다. 정답에 위치가 있는 줄은 합성과 똑같이 값+위치 점수(vl_f1)가 주 지표.

item 은 두 꼴을 다 받는다 (swift_kie_scorer.py 와 같다): 파이프라인 평가 문항, .jsonl 한 줄 그대로.

설정 (경로는 설정 파일 기준):
  {"id": "real-fx-po-v3", "format": "swift-fields", "paths": ["<v3 .jsonl>"], "scorer": "../scorers/kie_list_scorer.py:score"}
"""
from docgen.bench.evaluate import s_kie, _has_box
from docgen.bench.metrics import parse_json
from train.scorers.swift_kie_scorer import question_answer

LOC = ("loc_f1", "vl_f1", "loc_precision", "loc_recall")


def gold_of(answer):
    gold = parse_json(answer) if isinstance(answer, str) else answer
    if not isinstance(gold, list) or not gold or not all(isinstance(g, dict) and isinstance(g.get("key"), str) for g in gold):
        raise ValueError('정답이 [{"key": 키, "value": 값}, …] 목록이 아닙니다 (swift_to_kie_v3_tmp.py 로 바꾼 파일인지 확인)')
    return gold


def score(item, output):
    _, answer = question_answer(item)
    gold = gold_of(answer)
    r = s_kie({"answer": gold, "eval": {"fields": {g["key"]: {"type": "text"} for g in gold}}}, output)
    if any(_has_box(g) for g in gold):
        return {**r, "main": "vl_f1"}
    return {**r, "metrics": {k: v for k, v in r["metrics"].items() if k not in LOC}, "main": "f1"}
