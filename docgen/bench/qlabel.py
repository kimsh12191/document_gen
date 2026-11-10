"""qlabel 라벨(JSON) → ms-swift 학습 데이터 + 과제 폴더 (정보 추출 kie, 값과 위치).

  python -m docgen.bench.qlabel qlabel_json_final.json --img-dir /data/bank --out data/qlabel-kie
  python -m docgen.bench.qlabel a.json b.json --img-dir /data/bank --out data/qlabel-kie --val-ratio 0.05

입력 꼴 (그림마다 [경로, {태그: [칸, ...]}] 한 쌍의 목록; {경로: {태그: ...}} 사전도 받는다):
  [["/{img_dir}/images/xxx_1_3.png",
    {"BANK_ISSUE_CODE": [{"text": "KOEXKRSE", "bbox_2d": [[1658, 2346], [303.2, 1785.1], [410.6, 1785.1],
                                                            [410.6, 1807.0], [303.2, 1807.0]]}],
     "APPLICANT_NAME": [...]}], ...]
  - 경로의 {img_dir} 은 --img-dir 로 바꾼다.
  - bbox_2d 첫 점은 그림 크기 [너비, 높이], 나머지는 칸의 꼭짓점(픽셀). 꼭짓점의 최소·최대로 [x1, y1, x2, y2] 를 만든다.
    그림 파일을 열 수 있으면 실제 크기를 쓰고, 라벨의 크기와 다르면 꼭짓점을 그 비율로 맞춘다 (다르다고 알림).
    첫 점 없이 꼭짓점만 있거나 [x1, y1, x2, y2] 네 수만 있어도 된다 (그때는 그림 크기를 파일에서 읽는다).

질문: studio·평가 세트의 kie 질문(docgen.bench.prompts.P_KIE)을 그대로 쓴다. 묻는 항목은 그 그림에 있는 태그만.
답:   [{"key": 태그, "value": 적힌 값, "bbox_2d": [x1, y1, x2, y2], "page": 1}, ...] — 좌표는 그 그림 기준 0~1000 정수
      (--coord pixel 이면 픽셀). 글자가 빈 태그는 {"key": 태그, "value": null}.
      한 태그에 칸이 여럿이면 기본은 글자를 공백으로 이어 한 값, 위치는 칸들을 감싸는 박스 (--multi each 면 칸마다 한 줄).

나오는 것 (--out 폴더):
  train.jsonl / val.jsonl   ms-swift 표준 {"messages": [user, assistant], "images": [그림 절대 경로], "id", "task"}
                            → swift sft --dataset <out>/train.jsonl --val_dataset <out>/val.jsonl
  meta.json + tasks/kie.jsonl  과제 폴더 (docgen-tasks/1) → train/configs 파이프라인 설정의 data.train·data.benchmark 에
                            경로로 넣으면 섞기·평가(kie 채점: 값·위치·값+위치)에 그대로 쓰인다.
  REPORT.json               그림·문항·태그 수, 건너뛴 그림(파일 없음 등)과 이유
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

from .metrics import normalize_box
from .prompts import P_KIE


def load_labels(paths: list[Path]) -> list[tuple[str, dict]]:
    pairs = []
    for p in paths:
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data = list(data.items())
        for row in data:
            if not (isinstance(row, (list, tuple)) and len(row) == 2 and isinstance(row[1], dict)):
                raise ValueError(f"{p}: [그림 경로, {{태그: [...]}}] 꼴이 아닌 줄: {str(row)[:120]}")
            pairs.append((str(row[0]), row[1]))
    return pairs


def image_path(raw: str, img_dir: str) -> Path:
    if "{img_dir}" in raw:
        rest = raw.split("{img_dir}", 1)[1].lstrip("/\\")
        return Path(img_dir) / rest
    p = Path(raw)
    return p if p.is_absolute() else Path(img_dir) / p


def parse_box(b) -> tuple[tuple[float, float] | None, list[float]]:
    """라벨 bbox_2d → (라벨에 적힌 그림 크기 또는 None, 픽셀 [x1, y1, x2, y2])."""
    if not b:
        raise ValueError("bbox_2d 없음")
    if all(isinstance(v, (int, float)) for v in b):
        if len(b) != 4:
            raise ValueError(f"bbox_2d 수 {len(b)}개")
        x1, y1, x2, y2 = map(float, b)
        return None, [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]
    pts = [tuple(map(float, q)) for q in b]
    size = None
    if len(pts) in (3, 5):   # 첫 점 = 그림 크기 [너비, 높이]
        size, pts = pts[0], pts[1:]
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    return size, [min(xs), min(ys), max(xs), max(ys)]


def _union(boxes):
    return [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)]


def _text(c) -> str | None:
    t = c.get("text")
    t = "" if t is None else str(t).strip()
    return t or None


def entries_for(tags: dict, real_size, coord: str, multi: str, notes: list) -> list[dict]:
    """한 그림의 태그들 → 답 목록 (태그 순서는 라벨 순서)."""
    out = []
    for key, cells in tags.items():
        cells = cells if isinstance(cells, list) else [cells]
        parsed = []
        for c in cells:
            if not isinstance(c, dict):
                continue
            label_size, box = parse_box(c.get("bbox_2d")) if c.get("bbox_2d") else (None, None)
            size = real_size or label_size
            if box is not None and size is None:
                raise ValueError("그림 크기를 모름 (파일도 없고 bbox_2d 첫 점도 없음)")
            if box is not None and real_size and label_size and tuple(map(round, label_size)) != tuple(real_size):
                sx, sy = real_size[0] / label_size[0], real_size[1] / label_size[1]
                box = [box[0] * sx, box[1] * sy, box[2] * sx, box[3] * sy]
                notes.append(f"크기 다름: 라벨 {label_size} → 파일 {real_size}")
            parsed.append((_text(c), box, size))
        filled = [p for p in parsed if p[0] is not None]
        if not filled:
            out.append({"key": key, "value": None})
            continue
        groups = [[p] for p in filled] if multi == "each" else [filled]
        for g in groups:
            boxes = [p[1] for p in g if p[1] is not None]
            e = {"key": key, "value": " ".join(p[0] for p in g)}
            if boxes:
                b, (w, h) = _union(boxes), g[0][2]
                e["bbox_2d"] = [round(v) for v in b] if coord == "pixel" else normalize_box(b, w, h)
                e["page"] = 1
            out.append(e)
    return out


def _split(name: str, val_ratio: float, seed: int) -> str:
    h = int(hashlib.sha1(f"{seed}:{name}".encode()).hexdigest()[:8], 16) / 0x100000000
    return "val" if h < val_ratio else "train"


def _chunks(keys: list[str], n: int) -> list[list[str]]:
    return [keys] if n <= 0 else [keys[i:i + n] for i in range(0, len(keys), n)]


def convert(label_files, img_dir: str, out: Path, *, coord="norm1000", multi="join", max_keys=0, val_ratio=0.0,
            split="train", labels: dict | None = None, seed=42, check_images=True) -> dict:
    labels = labels or {}
    out.mkdir(parents=True, exist_ok=True)
    rows, items, skipped, notes = {"train": [], "val": []}, [], [], []
    tag_count, n_images = Counter(), 0
    for raw, tags in load_labels([Path(p) for p in label_files]):
        img = image_path(raw, img_dir)
        real_size = None
        if check_images:
            if not img.is_file():
                skipped.append({"image": str(img), "reason": "그림 파일 없음"})
                continue
            from PIL import Image

            with Image.open(img) as im:
                real_size = im.size
        if not tags:
            skipped.append({"image": str(img), "reason": "태그 없음"})
            continue
        try:
            my_notes: list[str] = []
            ans = entries_for(tags, real_size, coord, multi, my_notes)
        except (ValueError, TypeError, IndexError) as e:
            skipped.append({"image": str(img), "reason": f"라벨 오류: {e}"})
            continue
        notes += [f"{img.name}: {m}" for m in dict.fromkeys(my_notes)]
        n_images += 1
        tag_count.update(tags.keys())
        stem = img.stem
        part = "val" if split == "train" and _split(stem, val_ratio, seed) == "val" else ("test" if split == "test" else "train")
        keys = list(dict.fromkeys(e["key"] for e in ans))
        for ci, ks in enumerate(_chunks(keys, max_keys)):
            sub = [e for e in ans if e["key"] in ks]
            items_txt = "\n".join(f"- {k}: {labels.get(k) or '-'}" for k in ks)
            prompt = P_KIE.format(items=items_txt)
            rid = f"kie/qlabel/{stem}" + (f"/{ci}" if len(_chunks(keys, max_keys)) > 1 else "")
            answer_text = json.dumps(sub, ensure_ascii=False)
            if part in rows:
                rows[part].append({"id": rid, "task": "kie", "images": [str(img.resolve())],
                                   "messages": [{"role": "user", "content": "<image>" + prompt},
                                                {"role": "assistant", "content": answer_text}]})
            items.append({"id": rid, "task": "kie", "images": [str(img.resolve())], "prompt": prompt, "answer": sub,
                          "eval": {"fields": {k: {"type": "text", "norm": None, "kind": "text"} for k in ks}},
                          "meta": {"split": part if part != "test" else "benchmark", "document_id": f"qlabel:{stem}",
                                   "source": "qlabel", "n_pages": 1}})

    def dump(path, recs):
        with open(path, "w", encoding="utf-8") as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    if split == "train":
        dump(out / "train.jsonl", rows["train"])
        if rows["val"]:
            dump(out / "val.jsonl", rows["val"])
    (out / "tasks").mkdir(exist_ok=True)
    dump(out / "tasks" / "kie.jsonl", items)
    meta = {"format": "docgen-tasks/1", "kind": "qlabel", "version": "qlabel:1",
            "split": "test" if split == "test" else "mixed", "created": time.strftime("%Y-%m-%d %H:%M:%S"),
            "counts": {"kie": len(items)}, "split_counts": dict(Counter(i["meta"]["split"] for i in items)),
            "reference_type": "human_label", "coord": coord}
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    report = {"images": n_images, "records": len(items), "split_counts": meta["split_counts"],
              "tags": dict(tag_count.most_common()), "skipped": skipped, "notes": notes[:200]}
    (out / "REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m docgen.bench.qlabel", description=__doc__.split("\n")[0])
    ap.add_argument("labels", nargs="+", help="qlabel JSON 파일 (여러 개 가능)")
    ap.add_argument("--img-dir", required=True, help="경로의 {img_dir} 을 바꿀 폴더")
    ap.add_argument("--out", required=True, help="결과 폴더")
    ap.add_argument("--coord", choices=["norm1000", "pixel"], default="norm1000",
                    help="norm1000: 0~1000 정수 (Qwen2-VL·Qwen3-VL, 평가 세트와 같음) / pixel: 그림 픽셀")
    ap.add_argument("--multi", choices=["join", "each"], default="join",
                    help="한 태그에 칸이 여럿일 때: join 은 글자를 이어 한 값·감싸는 박스, each 는 칸마다 한 줄")
    ap.add_argument("--max-keys", type=int, default=0, help="한 질문에 묻는 태그 수 상한 (넘으면 질문을 나눔, 0 = 모두)")
    ap.add_argument("--val-ratio", type=float, default=0.0, help="검증으로 뺄 그림 비율 (그림 이름으로 고정 분할)")
    ap.add_argument("--split", choices=["train", "test"], default="train",
                    help="test 면 모두 평가용 (과제 폴더만, 파이프라인 data.benchmark 에 넣기)")
    ap.add_argument("--key-labels", help="태그 → 항목명 JSON (질문의 '- 키: 항목명'; 없으면 '-')")
    ap.add_argument("--no-check-images", action="store_true", help="그림 파일을 열지 않음 (크기는 bbox_2d 첫 점)")
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args(argv)
    key_labels = json.loads(Path(a.key_labels).read_text(encoding="utf-8")) if a.key_labels else None
    rep = convert(a.labels, a.img_dir, Path(a.out), coord=a.coord, multi=a.multi, max_keys=a.max_keys,
                  val_ratio=a.val_ratio, split=a.split, labels=key_labels, seed=a.seed,
                  check_images=not a.no_check_images)
    print(json.dumps({k: v for k, v in rep.items() if k not in ("tags", "notes")} | {"tag_kinds": len(rep["tags"]),
                                                                                    "skipped": len(rep["skipped"])},
                     ensure_ascii=False, indent=2))
    return 0 if rep["records"] else 1


if __name__ == "__main__":
    sys.exit(main())
