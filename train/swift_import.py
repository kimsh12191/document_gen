"""ms-swift .jsonl 읽기.

평가 (data.benchmark 의 "format": "swift-fields", load_swift): 한 줄이 문항 하나.
한 줄: {"messages": [{"role": "user", "content": "<image>…질문…"}, {"role": "assistant", "content": "…정답…"}], "images": ["/절대/경로.png"]}
질문은 그대로 묻고, 정답 글은 그대로 그 평가 세트의 채점 함수(scorer)에 넘긴다. scorer 를 적지 않으면
train/scorers/swift_default.py (질문의 'in order: [필드…]' 와 답 배열을 짝지어 필드마다 채점) — train/benchmarks.py 가 붙인다.
같은 그림의 문항은 meta.document_id 가 같다 (학습 데이터와 겹치는지 섞기 단계가 본다 — 파일이 달라도 그림 경로로도 본다).
읽을 수 없는 줄은 건너뛰고 경고와 함께 meta.skipped 에 남긴다 (평가 세트 DONE.json 의 sources).

학습 (data.train 의 "format": "swift", load_swift_train): 줄 {"messages": [...], "images"?: [...]} 을 그대로 SFT 에 넣는다
(여러 턴·system 도 그대로, 그림만 예산에 맞춰 줄임). 밖에서 가져온 학습 데이터용.
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


def load_swift_train(path: Path) -> tuple[dict, list[dict]]:
    """학습용 ms-swift .jsonl → (meta, 줄). 줄: {"id", "task": "swift:<파일 이름>", "images", "messages", "swift": True}."""
    path = Path(path).resolve()
    rows, skipped = [], []
    for line, rec in enumerate(read_jsonl(path), 1):
        try:
            msgs = rec.get("messages")
            if not isinstance(msgs, list) or not msgs or any(not isinstance(m, dict) or not isinstance(m.get("content"), str)
                                                              or m.get("role") not in ("system", "user", "assistant") for m in msgs):
                raise ValueError("messages 는 {role: system|user|assistant, content: 글} 목록이어야 합니다")
            if msgs[-1]["role"] != "assistant":
                raise ValueError("마지막 메시지가 assistant 가 아닙니다")
            images = rec.get("images") or []
            if not isinstance(images, list) or sum(m["content"].count("<image>") for m in msgs) != len(images):
                raise ValueError("images 수와 <image> 수가 다릅니다")
            images = [str(p if Path(p).is_absolute() else (path.parent / p).resolve()) for p in images]
            missing = [p for p in images if not Path(p).is_file()]
            if missing:
                raise ValueError(f"이미지가 없습니다: {missing[0]}")
            rows.append({"id": f"{path.stem}/{line:05d}", "task": f"swift:{path.stem}", "images": images,
                         "messages": [{"role": m["role"], "content": m["content"]} for m in msgs], "swift": True})
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            skipped.append({"line": line, "why": str(exc)})
    if not rows:
        raise ValueError(f"{path}: 읽은 줄이 없습니다 (건너뜀 {len(skipped)}줄, 첫 이유: {skipped[0]['why'] if skipped else '빈 파일'})")
    if skipped:
        print(f"WARNING: {path.name}: {len(skipped)}줄을 읽지 못해 학습에서 뺍니다 (예: {skipped[0]['line']}번째 줄 {skipped[0]['why']})",
              flush=True)
    return {"name": path.stem, "source": "swift", "file": str(path), "rows": len(rows), "skipped": skipped}, rows
