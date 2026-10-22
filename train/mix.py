"""데이터셋 섞기 (옛 bank_task/prepare.py + 1부 OCR SFT 묶기 + OCR replay 를 하나로): 과제 폴더(docgen-tasks) 여러 개
→ 학습이 읽는 폴더. OCR·문서 이해·업무 과제가 같은 규칙으로 섞인다.

  <output_dir>/
    DONE.json              이미지 예산, 수, 원본 데이터셋 (마지막에 쓴다)
    train_sft.jsonl        SFT 표본 {"messages", "images"} (같은 그림의 질문은 한 대화로 묶음)
    val_sft.jsonl
    train_grpo.jsonl       GRPO 후보 {"id", "split": "train", "task", "bench_item", "n_images", "messages", "images"}
    benchmark_tasks.jsonl  평가 질문 (train.predict 가 읽음, 그림은 PNG)
    benchmark_items.jsonl  평가 정답 (채점용, 그림 없음)
    image_items.jsonl      (OCR 평가가 있으면) 그림별 사내 OCR — predict --with-ocr 용
    images/                토큰 예산을 넘거나 PNG 가 아닌 그림의 줄인 사본

설정 (파이프라인 설정의 data 칸)
  train       학습 데이터셋 [경로 또는 {"path", "count": 이 데이터셋에서 쓸 SFT 문항 수(무작위)}]. 문항 meta.split 이 train 인
              것(폴더 meta.split 이 train 이면 표시 없는 문항도)이 학습, val 은 검증
  benchmark   평가 데이터셋 [경로 …] — 문항 meta.split 이 train·val 이 아닌 것
  task_mix    {과제: 비율} — 적힌 과제는 sft_max_examples 안에서 그 비율, 적히지 않은 과제는 있는 만큼 다 (예: OCR 은 count 로만 줄임).
              없으면 있는 비율대로 sft_max_examples 까지
  grpo_holdout 학습 문항 중 이 비율의 고객(업무 묶음)·문서는 SFT 에 넣지 않고 GRPO 후보로
평가 세트와 같은 고객·문서가 학습에 있으면 멈춘다. 이미지 예산: 그림 하나는 image_max_size 의 토큰까지, 문항 하나는 모든 그림 합쳐
max_image_tokens_per_sample 까지 (여러 서류는 고르게 줄임). 평가도 같은 규칙이라 학습·평가가 같은 픽셀을 본다.
"""
import hashlib
import json
import math
import os
import random
import time
from pathlib import Path

from PIL import Image

from docgen.bench.evaluate import reward
from docgen.bench.ocr_data import read_json, read_jsonl, write_json, write_jsonl
from docgen.bench.runner import oracle_output

from .settings import image_tokens, image_tokens_for

DEFAULTS = {
    "image_max_size": [2300, 1600],
    "max_image_tokens_per_sample": 12000,
    "sft_max_length": 16384,
    "sft_max_examples": 20000,
    "task_mix": None,
    "val_count": 200,
    "grpo_holdout": 0.2,
    "pack_turns": 8,
    "workers": min(16, os.cpu_count() or 1),
    "seed": 42,
}
BENCH_ITEM_KEYS = ("id", "task", "answer", "eval", "meta")
CHARS_PER_TOKEN = 0.67  # conservative for Korean text: assume 1.5 tokens per character


def load_folder(path: Path) -> tuple[dict, list[dict]]:
    """과제 폴더 → (meta, 문항). 문항의 images 는 절대 경로로."""
    meta_path = path / "meta.json"
    if not meta_path.is_file() or not (path / "tasks").is_dir():
        raise ValueError(f"{path}: 과제 폴더(meta.json + tasks/)가 아닙니다 — studio 데이터셋 폴더를 쓰세요")
    from docgen.bench.tracking import enrich, source_id

    meta = read_json(meta_path)
    origin = source_id(path.name, meta)
    items = []
    for f in sorted((path / "tasks").glob("*.jsonl")):
        for it in read_jsonl(f):
            it["images"] = [str(p if Path(p).is_absolute() else path / p) for p in it.get("images", [])]
            if (it.get("meta") or {}).get("context_image") and not Path(it["meta"]["context_image"]).is_absolute():
                it["meta"]["context_image"] = str(path / it["meta"]["context_image"])
            items.append(enrich(it, origin))
    return meta, items


def split_of(item: dict, folder_split: str) -> str:
    s = (item.get("meta") or {}).get("split")
    if s in ("train", "val"):
        return s
    if s in ("benchmark", "test"):
        return "test"
    return "train" if folder_split == "train" else "test"


def group_key(item: dict) -> str:
    """같은 고객·문서의 문항끼리 같은 값: OCR 은 문서 ID, 업무 과제는 묶음 ('cross_check/<묶음>/<사례>' → '<묶음>')."""
    doc = (item.get("meta") or {}).get("document_id")
    if doc:
        return f"doc:{doc}"
    parts = item["id"].split("/")
    return parts[1] if len(parts) > 1 else item["id"].split(":")[0]


def bucket(key: str, seed: int) -> float:
    return int(hashlib.sha1(f"{seed}:{key}".encode()).hexdigest()[:8], 16) / 0x100000000


def _write(job):
    src, dst, size = job
    with Image.open(src) as im:
        img = im.convert("RGB")
        if img.size != tuple(size):
            img = img.resize(tuple(size), Image.LANCZOS)
        tmp = dst.with_name(dst.stem + ".tmp" + dst.suffix)
        if dst.suffix == ".png":
            img.save(tmp, compress_level=1)
        else:
            img.save(tmp, quality=95)
        tmp.replace(dst)


def fit_size(w: int, h: int, cap: int, factor: int) -> tuple[int, int]:
    """Largest size (same aspect) whose visual tokens, ceil(w/factor) x ceil(h/factor), fit `cap`."""
    def tokens(a, b):
        return math.ceil(a / factor) * math.ceil(b / factor)
    if tokens(w, h) <= cap:
        return w, h
    s = min(1.0, math.sqrt(cap * factor ** 2 / (w * h)))
    while tokens(max(1, int(w * s)), max(1, int(h * s))) > cap:
        s *= 0.98
    return max(1, int(w * s)), max(1, int(h * s))


def sample_caps(n_images: int, per_image: int, per_sample: int) -> int:
    """Token cap of each image when a question has n_images: same share for every page."""
    return max(1, min(per_image, per_sample // max(1, n_images)))


class Fitter:
    """Image path under a token cap: the original if it already fits, else a resized copy
    (PNG for inference, which sends PNG; JPEG quality 95 for training). Paths are planned first and
    the copies written together in parallel by run()."""

    def __init__(self, out: Path, factor: int):
        self.out, self.factor, self.cache, self.jobs, self.size = out, factor, {}, {}, {}
        (out / "images").mkdir(parents=True, exist_ok=True)

    def tokens(self, w, h):
        return math.ceil(w / self.factor) * math.ceil(h / self.factor)

    def __call__(self, src, cap: int, png: bool) -> str:
        src = Path(src)
        key = (str(src), cap, png)
        if key in self.cache:
            return self.cache[key]
        with Image.open(src) as im:
            w, h = im.size
        if self.tokens(w, h) <= cap and (not png or src.suffix.lower() == ".png"):
            path, size = str(src), (w, h)
        else:
            size = fit_size(w, h, cap, self.factor)
            dst = self.out / "images" / (hashlib.sha1(f"{src}|{cap}".encode()).hexdigest()[:20] + (".png" if png else ".jpg"))
            path = str(dst)
            if not dst.exists():
                self.jobs[path] = (src, dst, size)
        self.cache[key] = path
        self.size[path] = size
        return path

    def image_tokens(self, path) -> int:
        if path not in self.size:
            with Image.open(path) as im:
                self.size[path] = im.size
        return self.tokens(*self.size[path])

    def run(self, workers: int) -> int:
        jobs = list(self.jobs.values())
        self.jobs = {}
        if workers > 1 and len(jobs) > 1:
            from concurrent.futures import ProcessPoolExecutor
            with ProcessPoolExecutor(workers) as pool:
                list(pool.map(_write, jobs, chunksize=8))
        else:
            for job in jobs:
                _write(job)
        return len(jobs)


def quotas(avail: dict, mix: dict | None, total: int) -> dict:
    """Rows to take per task. With `mix`: listed tasks share `total` in those proportions (filled up from
    listed tasks that still have rows when one runs short), unlisted tasks keep every row (limit them with a
    dataset's `count`). Without `mix`: proportional to what is available, up to `total`."""
    if mix:
        listed = {t: n for t, n in avail.items() if mix.get(t, 0) > 0}
        take = _share(listed, {t: mix[t] for t in listed}, total)
        take.update({t: n for t, n in avail.items() if t not in mix})
        return take
    return _share(avail, dict(avail), total)


def _share(avail: dict, weights: dict, total: int) -> dict:
    weights = {t: w for t, w in weights.items() if w > 0 and avail[t] > 0}
    total = min(total, sum(avail[t] for t in weights))
    take = {t: 0 for t in weights}
    left = total
    while left > 0 and weights:
        wsum = sum(weights.values())
        step = {t: min(avail[t] - take[t], max(1, math.floor(left * w / wsum))) for t, w in weights.items()}
        for t, n in sorted(step.items(), key=lambda kv: -kv[1]):
            n = min(n, left)
            take[t] += n
            left -= n
        weights = {t: w for t, w in weights.items() if take[t] < avail[t]}
    return take


def strip_images(text: str) -> str:
    while text.startswith("<image>"):
        text = text[len("<image>"):]
    return text.lstrip("\n")


def pack(rows: list[dict], max_turns: int, room_chars) -> list[dict]:
    """Questions on the same image(s) become one multi-turn conversation (images encoded once);
    image tags stay on the first question only."""
    groups = {}
    for r in rows:
        groups.setdefault(tuple(r["images"]), []).append(r)
    out = []
    for images, group in groups.items():
        turns, chars = [], 0
        limit = room_chars(images)
        for r in group:
            q, a = r["messages"]
            size = len(q["content"]) + len(a["content"])
            if turns and (len(turns) // 2 >= max_turns or chars + size > limit):
                out.append({"messages": turns, "images": list(images)})
                turns, chars = [], 0
            if turns:
                q = {**q, "content": strip_images(q["content"])}
            turns, chars = turns + [q, a], chars + size
        if turns:
            out.append({"messages": turns, "images": list(images)})
    return out


def sft_record(it: dict) -> dict:
    """문항 → 질문(그림 표시 + 평가 질문)과 답(정답을 모델 출력 꼴로) — docgen.bench.build.swift_record 와 같은 꼴."""
    from docgen.bench.build import swift_record

    return swift_record(it)


def _entries(spec) -> list[dict]:
    return [s if isinstance(s, dict) else {"path": s} for s in (spec if isinstance(spec, list) else [spec])]


def mix(data_cfg: dict, model_dir: str | None) -> dict:
    cfg = {**DEFAULTS, **data_cfg}
    out = Path(cfg["output_dir"])
    if (out / "DONE.json").exists():
        raise ValueError(f"{out} already prepared; use a new output_dir")
    out.mkdir(parents=True, exist_ok=True)
    started = time.time()
    seed = cfg["seed"]
    try:
        per_image, factor = image_tokens(model_dir, cfg["image_max_size"])
    except (OSError, ValueError, TypeError) as exc:
        factor = 32
        per_image = image_tokens_for(cfg["image_max_size"], factor)
        print(f"WARNING: {exc}; assuming 32x32 pixels per visual token")
    budget = cfg["max_image_tokens_per_sample"]
    fit = Fitter(out, factor)

    def cap(n):
        return sample_caps(n, per_image, budget)

    # -- 평가 -------------------------------------------------------------------------------
    from .benchmarks import normalize, paths as benchmark_paths

    benchmarks = normalize(cfg["benchmark"])
    named = any(not b["legacy"] for b in benchmarks)
    bench_items, bench_sources = [], {}
    for b in benchmarks:
        references = set()
        for path in b["paths"]:
            meta, items = load_folder(Path(path))
            test = [it for it in items if split_of(it, meta.get("split", "test")) == "test"]
            if not test:
                raise ValueError(f"benchmark {path}: 평가 문항이 없습니다 (학습 전용 데이터셋)")
            reference = meta.get("reference_type") or (meta.get("studio") or {}).get("gt") or meta.get("gt")
            reference = {"exact":"synthetic_exact", "reviewed":"human_reviewed", "pseudo":"ocr_pseudo_unreviewed"}.get(reference, reference)
            if reference:
                references.add(reference)
            if named:
                test = [{**it, "meta": {**it["meta"], "benchmark_id": b["id"], "benchmark_name": b["name"],
                                        "benchmark_group": b["group"], "benchmark_path": path}} for it in test]
            bench_items += test
            bench_sources[path] = {k: v for k, v in meta.items() if k not in ("doc_names",)}
        if len(references) > 1:
            raise ValueError(f"benchmark {b['id']}: 정답 출처가 다릅니다. 별도 id로 나누세요: {sorted(references)}")
    if len({it["id"] for it in bench_items}) != len(bench_items):
        raise ValueError("평가 데이터셋끼리 문항 ID 가 겹칩니다")
    bench_keys = {group_key(it) for it in bench_items}

    # -- 학습: SFT 풀·검증·GRPO 후보 ------------------------------------------------------------
    pools, val_rows, grpo, overlap, train_sources = {}, [], [], 0, {}
    for e in _entries(cfg["train"]):
        meta, items = load_folder(Path(e["path"]))
        rows, n_val, before = [], 0, overlap
        for it in items:
            s = split_of(it, meta.get("split", "test"))
            if s == "test":
                continue
            key = group_key(it)
            if key in bench_keys:
                overlap += 1
                continue
            if s == "val":
                val_rows.append(it)
                n_val += 1
            elif bucket(key, seed) < cfg["grpo_holdout"]:
                grpo.append(it)   # 이 고객·문서의 문항은 GRPO 후보로 (SFT 에 넣지 않음)
            else:
                rows.append(it)
        if not rows and not n_val and overlap == before:
            raise ValueError(f"train {e['path']}: 학습 문항이 없습니다 (평가 전용 데이터셋)")
        if e.get("count") is not None:
            rows.sort(key=lambda it: it["id"])
            random.Random(f"{seed}:{e['path']}").shuffle(rows)
            rows = rows[:int(e["count"])]
        for it in rows:
            pools.setdefault(it["task"], []).append(it)
        train_sources[e["path"]] = {"rows": len(rows), "val": n_val, "count": e.get("count"),
                                    "meta": {k: v for k, v in meta.items() if k not in ("doc_names",)}}
    if overlap:
        raise ValueError(f"{overlap} training rows share a customer or document with the benchmark; "
                         "build training data separately (docgen.bench build --split train, OCR 준비의 문서 나누기)")
    if not pools:
        raise ValueError("No SFT rows: check data.train")

    rng = random.Random(seed)
    for task in sorted(pools):
        pools[task].sort(key=lambda r: r["id"])
        rng.shuffle(pools[task])
    val = list(val_rows)
    rng.shuffle(val)
    val = val[:cfg["val_count"]]
    tasks = sorted(pools)
    for i in range(max(0, cfg["val_count"] - len(val))):   # 검증 문항이 모자라면 과제마다 하나씩 덜어 온다
        t = tasks[i % len(tasks)]
        if len(pools[t]) > 1:
            val.append(pools[t].pop())
    avail = {t: len(rows) for t, rows in pools.items()}
    take = quotas(avail, cfg["task_mix"], cfg["sft_max_examples"])
    chosen = [r for t, n in take.items() for r in pools[t][:n]]

    def to_sample(it):
        rec = sft_record(it)
        return {"messages": rec["messages"], "images": [fit(p, cap(len(it["images"])), png=False) for p in it["images"]]}

    def room_chars(images):
        return int((cfg["sft_max_length"] - sum(fit.image_tokens(p) for p in images) - 256) * CHARS_PER_TOKEN)

    samples, too_long = [], 0
    for it in chosen:
        s = to_sample(it)
        if sum(len(m["content"]) for m in s["messages"]) > room_chars(s["images"]):
            too_long += 1  # would pass sft_max_length: dropped rather than truncated
        else:
            samples.append(s)
    sft = pack(samples, cfg["pack_turns"], room_chars) if cfg["pack_turns"] > 1 else samples
    random.Random(seed).shuffle(sft)
    write_jsonl(out / "train_sft.jsonl", sft)
    write_jsonl(out / "val_sft.jsonl", [to_sample(it) for it in val])

    def question(it, png):
        imgs = [fit(p, cap(len(it["images"])), png=png) for p in it["images"]]
        return imgs, [{"role": "user", "content": "<image>" * len(imgs) + it["prompt"]}]

    # -- GRPO 후보 (PNG: SFT 모델이 평가와 같은 답 내기 코드로 답해 골라 뽑는다) ------------------------
    grpo_rows = []
    for it in grpo:
        imgs, messages = question(it, png=True)
        grpo_rows.append({"id": it["id"], "split": "train", "task": it["task"],
                          "bench_item": json.dumps({k: it[k] for k in BENCH_ITEM_KEYS if k in it}, ensure_ascii=False),
                          "n_images": len(imgs), "messages": messages, "images": imgs})
    grpo_rows.sort(key=lambda r: r["id"])
    write_jsonl(out / "train_grpo.jsonl", grpo_rows)

    # -- 평가 -------------------------------------------------------------------------------
    bench_rows, image_items = [], {}
    for it in bench_items:
        imgs, messages = question(it, png=True)
        row = {"id": it["id"], "split": "benchmark", "task": it["task"], "messages": messages, "images": imgs,
               "source_images": it["images"]}
        ctx = (it.get("meta") or {}).get("context_image")
        if ctx:
            row["context_image"] = ctx
        bench_rows.append(row)
    resized = fit.run(cfg["workers"])
    write_jsonl(out / "benchmark_tasks.jsonl", bench_rows)
    write_jsonl(out / "benchmark_items.jsonl", [{k: it[k] for k in BENCH_ITEM_KEYS if k in it} for it in bench_items])
    for src in {Path(p) for p in benchmark_paths(cfg["benchmark"])}:   # OCR 준비 폴더의 그림별 사내 OCR (--with-ocr)
        if (src / "image_items.jsonl").is_file():
            image_items.update({r["image"]: r for r in read_jsonl(src / "image_items.jsonl")})
    if image_items:
        write_jsonl(out / "image_items.jsonl", list(image_items.values()))

    # 정답을 답으로 넣으면 만점이어야 한다 (데이터와 채점 코드가 맞는지)
    sample = random.Random(0).sample(bench_items, min(200, len(bench_items)))
    bad = [it["id"] for it in sample if reward(it["task"], oracle_output(it), it) < 1.0]
    if bad:
        raise ValueError(f"Reference answers do not score 1.0 with this docgen code (e.g. {bad[:3]}); "
                         "use the docgen code the data was built with")

    def count(rows, key="task"):
        c = {}
        for r in rows:
            c[r[key]] = c.get(r[key], 0) + 1
        return dict(sorted(c.items()))

    done = {
        "image_max_size": cfg["image_max_size"], "pixels_per_token_side": factor,
        "max_image_tokens_per_image": per_image, "max_image_tokens_per_sample": budget,
        "sft_max_length": cfg["sft_max_length"],
        "counts": {"sft_rows_by_task": {t: n for t, n in take.items() if n}, "sft_available_by_task": avail,
                   "sft_samples": len(sft), "sft_packed_from": len(samples), "sft_dropped_too_long": too_long,
                   "val": len(val), "grpo_by_task": count(grpo_rows), "benchmark_by_task": count(bench_rows),
                   "resized_images": resized},
        "excluded_tasks": sorted(t for t in avail if not take.get(t)),
        "sources": {"train": train_sources, "benchmark": bench_sources},
        "benchmarks": [{k: v for k, v in b.items() if k != "legacy"} for b in benchmarks] if named else [],
        "settings": {k: cfg[k] for k in DEFAULTS},
        "seconds": round(time.time() - started),
    }
    write_json(out / "DONE.json", done)
    return {"output": str(out), **done["counts"]}
