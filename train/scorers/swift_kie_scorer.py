"""채점 함수 견본: temp/swift_to_kie_tmp.py 로 kie 꼴로 바꾼 swift .jsonl (data.benchmark 의 "format": "swift-fields" + "scorer").

바꾼 파일의 꼴
  질문: 한국어 안내 + '항목 (키: 서식의 항목명)' 아래 '- 키: -' 줄들   (in order: 줄은 없다)
  정답: {"키": "값" 또는 null, …} JSON 객체
질문의 '- 키: -' 줄에서 키 순서를 읽어, 모델이 {키: 값} 객체 대신 값만 순서대로 담은 배열로 답해도 읽는다.
점수는 swift_default 와 같다 (필드마다 대소문자·공백·문장부호 무시, null 은 빈 답이어야 맞음, 주 지표 f1).

item 은 두 꼴을 다 받는다
  파이프라인이 넘기는 평가 문항: {"answer": 정답 글, "eval": {"prompt": 질문}, …}   (train/swift_import.py)
  .jsonl 한 줄 그대로:           {"messages": [{"role": "user", …}, {"role": "assistant", …}], "images": […]}  (손으로 확인할 때)

설정 (경로는 설정 파일 기준, train/configs/ 에서는 ../scorers/…):
  {"id": "real_po_kie", "format": "swift-fields", "paths": ["<바꾼 .jsonl>"], "scorer": "../scorers/swift_kie_scorer.py:score"}
"""
import re

from docgen.bench.metrics import parse_json
from train.scorers.swift_default import as_dict, compare

ITEM = re.compile(r"^- (.+): -\s*$", re.M)


def keys_in(prompt):
    """질문의 '- 키: -' 줄들 → 키 목록 (없으면 None)."""
    return ITEM.findall(prompt or "") or None


def question_answer(item):
    """(질문, 정답 글) — 평가 문항이든 .jsonl 한 줄이든."""
    if "answer" in item:
        return (item.get("eval") or {}).get("prompt") or item.get("prompt") or "", item["answer"]
    messages = item.get("messages") or []
    user = next((m["content"] for m in messages if m.get("role") == "user"), "")
    assistant = next((m["content"] for m in messages if m.get("role") == "assistant"), None)
    return user, assistant


def score(item, output):
    prompt, answer = question_answer(item)
    keys = keys_in(prompt)
    gold = as_dict(parse_json(answer) if isinstance(answer, str) else answer, keys)
    if not gold:   # 정답을 못 읽었는데 빈 {} 로 두면 모든 답이 만점이 된다
        raise ValueError("정답이 {키: 값} 객체가 아닙니다 (swift_to_kie_tmp.py 로 바꾼 파일인지 확인)")
    return compare(gold, as_dict(parse_json(output), keys))
