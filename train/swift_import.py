"""swift 형식(ms-swift) .jsonl 을 문항으로 읽는다. pipeline.json 의 data.benchmark(평가)·data.train(학습)에 파일 경로를 그대로 넣는다
("format": "swift-fields").

한 줄: {"messages": [{"role": "user", "content": "<image>…질문…"}, {"role": "assistant", "content": "…정답…"}], "images": ["/절대/경로.png"]}
질문은 그대로 묻고, 정답 글은 그대로 그 평가 세트의 채점 함수(scorer)에 넘긴다. scorer 를 적지 않으면
train/scorers/swift_default.py (질문의 'in order: [필드…]' 와 답 배열을 짝지어 필드마다 채점) — train/benchmarks.py 가 붙인다.
같은 그림의 문항은 meta.document_id 가 같다 (학습 데이터와 겹치는지 섞기 단계가 본다 — 파일이 달라도 그림 경로로도 본다).
학습에 넣으면 정답 글을 그대로 SFT 답으로 가르치고, GRPO 보상은 그 학습 데이터의 채점 함수로 낸다 (docgen.bench.evaluate.reward).
읽을 수 없는 줄은 건너뛰고 경고와 함께 meta.skipped 에 남긴다 (섞은 폴더 DONE.json 의 sources).
"""
from pathlib import Path

from docgen.bench.ocr_data import read_jsonl


def item_of(rec: dict, source: str, line: int, base: Path, split: str = "test") -> dict:
    msgs = rec.get("messages")
    if not isinstance(msgs, list) or len(msgs) != 2 or [m.get("role") for m in msgs] != ["user", "assistant"]:
        raise ValueError("messages 는 user·assistant 두 개여야 합니다")
    prompt, answer = msgs[0].get("content"), msgs[1].get("content")
    if not isinstance(prompt, str) or not isinstance(answer, str):
        raise ValueError("질문·답(content)이 글이 아닙니다")
    images = rec.get("images")
    if not isinstance(images, list) or not images or prompt.count("<image>") != len(images):
        raise ValueError("images 수와 질문의 <image> 수가 다릅니다")
    images = [str(p if Path(p).is_absolute() else (base / p).resolve()) for p in images]
    missing = [p for p in images if not Path(p).is_file()]
    if missing:
        raise ValueError(f"이미지가 없습니다: {missing[0]}")
    return {"id": f"{source}/{line:05d}", "task": "kie", "images": images,
            "prompt": prompt.replace("<image>", "").strip(), "answer": answer,
            "eval": {"raw": True, "prompt": prompt.replace("<image>", "").strip()},   # 채점 함수가 질문을 볼 수 있게 (섞은 폴더의 문항에는 prompt 칸이 없음)
            "meta": {"source": source, "line": line, "document_id": f"{source}:{Path(images[0]).stem}", "split": split}}


def load_swift(path: Path, split: str = "test") -> tuple[dict, list[dict]]:
    """swift .jsonl → (meta, 문항). split: "test"(평가, data.benchmark) | "train"(학습, data.train)."""
    path = Path(path).resolve()
    items, skipped = [], []
    for line, rec in enumerate(read_jsonl(path), 1):
        try:
            items.append(item_of(rec, path.stem, line, path.parent, split))
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            skipped.append({"line": line, "why": str(exc)})
    if not items:
        raise ValueError(f"{path}: 읽은 문항이 없습니다 (건너뜀 {len(skipped)}줄, 첫 이유: {skipped[0]['why'] if skipped else '빈 파일'})")
    if skipped:
        print(f"WARNING: {path.name}: {len(skipped)}줄을 읽지 못해 건너뜁니다 (예: {skipped[0]['line']}번째 줄 {skipped[0]['why']})",
              flush=True)
    meta = {"name": path.stem, "split": split, "source": "swift", "real_data": True, "file": str(path),
            "counts": {"kie": len(items)}, "documents": len({it["meta"]["document_id"] for it in items}),
            "skipped": skipped}
    return meta, items
