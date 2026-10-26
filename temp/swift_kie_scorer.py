"""채점 함수 예시: swift_to_kie_tmp.py 로 바꾼 swift .jsonl (data.benchmark 의 "format": "swift-fields" + "scorer").

바꾼 파일의 꼴
  질문: 한국어 안내 + '항목 (키: 서식의 항목명)' 아래 '- 키: -' 줄들   (in order: 줄은 없다)
  정답: {"키": "값" 또는 null, …} JSON 객체
이 함수는 질문의 '- 키: -' 줄에서 키 순서를 읽어, 모델이 {키: 값} 객체 대신 값만 순서대로 담은 배열로 답해도 읽는다.
점수는 swift_default 와 같다 (필드마다 대소문자·공백·문장부호 무시, null 은 빈 답이어야 맞음, 주 지표 f1).

설정 (train/configs/pipeline.example.json 의 real_po_kie 처럼, 경로는 설정 파일 기준):
  {"id": "real-po-kie", "format": "swift-fields", "paths": ["<바꾼 .jsonl>"], "scorer": "../../temp/swift_kie_scorer.py:score"}
"""
import re

from docgen.bench.metrics import parse_json
from train.scorers.swift_default import as_dict, compare

ITEM = re.compile(r"^- (.+): -\s*$", re.M)


def keys_in(prompt):
    """질문의 '- 키: -' 줄들 → 키 목록 (없으면 None)."""
    return ITEM.findall(prompt or "") or None


def score(item, output):
    keys = keys_in((item.get("eval") or {}).get("prompt"))
    gold = as_dict(parse_json(item["answer"]) if isinstance(item["answer"], str) else item["answer"], keys)
    if gold is None:
        raise ValueError("정답이 {키: 값} 객체가 아닙니다 (swift_to_kie_tmp.py 로 바꾼 파일인지 확인)")
    return compare(gold, as_dict(parse_json(output), keys))
