"""swift 형식 실서류 추출 데이터(.jsonl)의 질문·답을 합성 정보 추출(kie)과 같은 꼴로 고친 swift .jsonl 을 만든다.

  python -m train.swift_to_kie <swift.jsonl> --out <새 .jsonl> [--labels 항목명.json]

- 들어오는 것: 질문에 'in order: ["필드", …]', 답은 같은 순서의 문자열 배열 (train/swift_import.py 와 같은 꼴).
- 나가는 것: 같은 swift .jsonl (messages·images 그대로), 질문과 답만 바뀜. 평가는 지금처럼 "format": "swift-fields" 로 넣는다.
    질문: 합성 kie 질문(docgen.bench.prompts.P_KIE)과 같은 꼴에서 위치만 뺀 것 (아래 P_KIE_VALUE)
    답:   [{"key": "NEGO_CLCT", "value": "EOA"}, …]   빈 값("")은 null, 같은 필드가 두 번이면 두 번째부터 '필드#2'
- 채점은 값 점수(f1)만 (위치 정답이 없는 kie 는 evaluate 가 위치 점수를 내지 않는다).
- --labels: {"필드": "항목명"} JSON. 주면 항목 줄이 '- NEGO_CLCT: 매입추심구분', 없으면 '- NEGO_CLCT: -'. 학습용·평가용은 같은 것으로.
- 읽을 수 없는 줄은 건너뛰고 수를 알려 준다. 원본 파일은 고치지 않는다.
"""
import argparse
import json
from pathlib import Path

from docgen.bench.ocr_data import read_jsonl, write_jsonl

from .swift_import import fields_of, keys_of

# 합성 kie 질문(docgen.bench.prompts.P_KIE)과 같은 목록 꼴에서 위치만 뺀 것. swift_import 가 이 꼴도 읽는다.
P_KIE_VALUE = ("이 문서에서 아래 항목의 값을 찾아 JSON 목록으로 답하세요. 항목마다 "
               '{{"key": 키, "value": 문서에 적힌 값 그대로}} 를 쓰세요. 값이 여러 개면 줄바꿈으로 이어 한 문자열로 쓰세요. '
               '키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {{"key": 키, "value": null}} 로 답하세요.\n항목 (키: 서식의 항목명)\n{items}')


def convert(rec: dict, labels: dict) -> dict:
    """swift 한 줄 → 질문·답을 바꾼 swift 한 줄."""
    msgs = rec["messages"]
    if len(msgs) != 2 or [m.get("role") for m in msgs] != ["user", "assistant"]:
        raise ValueError("messages 는 user·assistant 두 개여야 합니다")
    prompt, answer = msgs[0]["content"], msgs[1]["content"]
    keys = keys_of(fields_of(prompt))
    values = json.loads(answer)
    if not isinstance(values, list) or len(values) != len(keys) or not all(isinstance(v, str) for v in values):
        raise ValueError(f"답이 필드 {len(keys)}개와 같은 수의 문자열 배열이 아닙니다")
    items = "\n".join(f"- {k}: {labels.get(k.split('#')[0]) or '-'}" for k in keys)
    new_answer = [{"key": k, "value": v if v.strip() else None} for k, v in zip(keys, values)]
    return {**rec, "messages": [{"role": "user", "content": "<image>" * prompt.count("<image>") + P_KIE_VALUE.format(items=items)},
                                {"role": "assistant", "content": json.dumps(new_answer, ensure_ascii=False)}]}


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m train.swift_to_kie", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="swift .jsonl")
    p.add_argument("--out", required=True, help="만들 .jsonl (새 이름)")
    p.add_argument("--labels", help='필드 → 항목명 JSON ({"NEGO_CLCT": "매입추심구분", …})')
    a = p.parse_args(argv)
    out = Path(a.out)
    if out.exists():
        raise SystemExit(f"{out} 가 이미 있습니다. 새 이름으로 만드세요")
    labels = json.loads(Path(a.labels).read_text(encoding="utf-8")) if a.labels else {}
    rows, skipped = [], []
    for line, rec in enumerate(read_jsonl(a.input), 1):
        try:
            rows.append(convert(rec, labels))
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            skipped.append((line, str(exc)))
    if not rows:
        raise SystemExit(f"바꾼 줄이 없습니다 (첫 이유: {skipped[0] if skipped else '빈 파일'})")
    write_jsonl(out, rows)
    print(f"{len(rows)}줄 → {out}" + (f" ({len(skipped)}줄 건너뜀, 예: {skipped[0][0]}번째 줄 {skipped[0][1]})" if skipped else ""))


if __name__ == "__main__":
    main()
