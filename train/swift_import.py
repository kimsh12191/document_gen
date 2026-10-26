"""swift 형식 실서류 추출 데이터(.jsonl)를 평가 문항으로 읽는다. pipeline.json 의 data.benchmark 에 파일 경로를 그대로 넣는다.

한 줄: {"messages": [{"role": "user", "content": "<image>… in order: [\"필드\", …] …"},
                    {"role": "assistant", "content": "[\"값\", …]"}], "images": ["/절대/경로.png"]}
질문은 그대로 묻는다. 답(정답) 꼴에 따라:
  - 질문에 'in order: [...]', 답이 같은 수의 문자열 배열 → 필드와 짝지어 kie 로 채점 (eval.order)
  - 답이 {키: 값} JSON 객체 → 그 키로 kie 채점 (기본 채점기가 읽는 꼴)
  - 그 밖 (어떤 글이든) → 정답 글을 그대로 두고, 그 평가 세트의 채점 함수(scorer)로만 채점 (eval.raw)
같은 그림의 문항은 meta.document_id 가 같다 (학습 데이터와 겹치는지 섞기 단계가 본다).
읽을 수 없는 줄은 건너뛰고 경고와 함께 meta.skipped 에 남긴다 (섞은 폴더 DONE.json 의 sources).
"""
import json
import re
from pathlib import Path

from docgen.bench.ocr_data import read_jsonl

FIELDS = re.compile(r"in order:\s*(\[.*?\])", re.S)


def fields_of(prompt: str) -> list[str]:
    """질문에서 필드 목록: 'in order: [...]' 뒤의 JSON 배열."""
    m = FIELDS.search(prompt)
    if not m:
        raise ValueError("질문에 'in order: [필드, …]' 가 없습니다")
    fields = json.loads(m.group(1))
    if not fields or not all(isinstance(f, str) and f for f in fields):
        raise ValueError("필드 목록이 비었거나 문자열이 아닙니다")
    return fields


def keys_of(fields: list[str]) -> list[str]:
    """같은 필드가 두 번 나오면 두 번째부터 '#2' 를 붙여 칸을 나눈다."""
    seen, out = {}, []
    for f in fields:
        seen[f] = seen.get(f, 0) + 1
        out.append(f if seen[f] == 1 else f"{f}#{seen[f]}")
    return out


def item_of(rec: dict, source: str, line: int, base: Path) -> dict:
    msgs = rec.get("messages")
    if not isinstance(msgs, list) or len(msgs) != 2 or [m.get("role") for m in msgs] != ["user", "assistant"]:
        raise ValueError("messages 는 user·assistant 두 개여야 합니다")
    prompt, answer = msgs[0]["content"], msgs[1]["content"]
    images = rec.get("images")
    if not isinstance(images, list) or not images or prompt.count("<image>") != len(images):
        raise ValueError("images 수와 질문의 <image> 수가 다릅니다")
    images = [str(p if Path(p).is_absolute() else (base / p).resolve()) for p in images]
    missing = [p for p in images if not Path(p).is_file()]
    if missing:
        raise ValueError(f"이미지가 없습니다: {missing[0]}")
    if not isinstance(answer, str):
        raise ValueError("답(assistant content)이 글이 아닙니다")
    try:
        values = json.loads(answer)
    except ValueError:
        values = None
    try:
        fields = fields_of(prompt)
    except ValueError:
        fields = None
    if fields:   # 'in order' 질문인데 답이 안 맞으면 데이터 오류 (건너뜀)
        if not isinstance(values, list) or len(values) != len(fields) or not all(isinstance(v, str) for v in values):
            raise ValueError(f"답이 필드 {len(fields)}개와 같은 수의 문자열 배열이 아닙니다")
        keys = keys_of(fields)
        gold, ev = dict(zip(keys, values)), {"order": keys, "fields": {k: {"type": "text"} for k in keys}}
    elif isinstance(values, dict) and values and all(v is None or isinstance(v, str) for v in values.values()):
        keys = list(values)
        gold, ev = values, {"fields": {k: {"type": "text"} for k in keys}}
    else:   # 기본 채점기가 모르는 꼴: 정답 글 그대로, 채점 함수(scorer)가 있어야 한다 (train/mix.py 가 확인)
        keys, gold, ev = [], answer, {"raw": True}
    return {"id": f"{source}/{line:05d}", "task": "kie", "images": images,
            "prompt": prompt.replace("<image>", "").strip(),
            "answer": gold, "eval": ev,
            "meta": {"source": source, "line": line, "document_id": f"{source}:{Path(images[0]).stem}",
                     "n_fields": len(keys), "split": "test"}}


def load_swift(path: Path) -> tuple[dict, list[dict]]:
    """swift .jsonl → (meta, 문항). 평가 전용 (split test)."""
    path = Path(path).resolve()
    items, skipped = [], []
    for line, rec in enumerate(read_jsonl(path), 1):
        try:
            items.append(item_of(rec, path.stem, line, path.parent))
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            skipped.append({"line": line, "why": str(exc)})
    if not items:
        raise ValueError(f"{path}: 읽은 문항이 없습니다 (건너뜀 {len(skipped)}줄, 첫 이유: {skipped[0]['why'] if skipped else '빈 파일'})")
    if skipped:
        print(f"WARNING: {path.name}: {len(skipped)}줄을 읽지 못해 건너뜁니다 (예: {skipped[0]['line']}번째 줄 {skipped[0]['why']})",
              flush=True)
    meta = {"name": path.stem, "split": "test", "source": "swift", "real_data": True, "file": str(path),
            "counts": {"kie": len(items)}, "documents": len({it["meta"]["document_id"] for it in items}),
            "skipped": skipped}
    return meta, items
