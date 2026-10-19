"""파일 입출력과 이미지 크기 맞추기."""
from __future__ import annotations

import base64
import io
import json
import math
from pathlib import Path

PATCH = 32          # Qwen3.5: 16px 패치 2×2 병합 → 언어 모델 토큰 하나가 32×32px
MAX_SIDE = (2300, 1600)  # 1부·2부 학습 입력과 같은 상한 (긴 변, 짧은 변)


def read_jsonl(path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(ln) for ln in f if ln.strip()]


def write_jsonl(path, rows) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def dumps(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


def tokens_of(w: int, h: int) -> int:
    return math.ceil(w / PATCH) * math.ceil(h / PATCH)


def fit(w: int, h: int, budget: int | None = None) -> tuple[int, int]:
    """학습 입력 상한(긴 변 2300, 짧은 변 1600)에 맞추고, budget(토큰)이 있으면 그 안으로 더 줄인 크기. 키우지는 않는다."""
    s = min(1.0, MAX_SIDE[0] / max(w, h), MAX_SIDE[1] / min(w, h))
    if budget:
        while s > 0.05 and tokens_of(round(w * s), round(h * s)) > budget:
            s *= 0.97
    return max(PATCH, round(w * s)), max(PATCH, round(h * s))


def load_resized(path, budget: int | None = None):
    from PIL import Image

    img = Image.open(path).convert("RGB")
    size = fit(*img.size, budget)
    return img if size == img.size else img.resize(size, Image.LANCZOS)


def data_url(img) -> str:
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def page_budget(n_pages: int, total: int) -> int:
    """모든 쪽을 한 번에 넣을 때 쪽마다 같은 비율로 나눈 토큰 상한 (2부 prepare 의 max_image_tokens_per_sample 과 같은 방식)."""
    return max(64, total // max(1, n_pages))
