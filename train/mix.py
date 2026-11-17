"""학습 데이터 섞기와 평가 세트 준비 (python -m train 의 prepare 단계).

평가 세트 (prepare_sets): data.benchmark 의 세트마다 <cache_dir>/sets/<id>-<지문>/
  tasks.jsonl   평가 질문 {id, task, messages, images(PNG), source_images}  (train/predict.py 가 읽음)
  items.jsonl   정답 {id, task, answer, eval, meta}  (채점용)
  images/       예산에 맞춰 줄인 그림
  DONE.json     세트 칸, 문항 수, 그림 예산, 원본 (마지막에 쓴다)
  지문 = 세트 칸(경로·format·gt·scorer·이름) + 원본 파일의 크기·시각 + 채점 함수 파일 + 평가 그림 예산.
  같으면 다른 실행·실험도 이 폴더를 그대로 쓰고 (모델 답 캐시도 이 폴더 기준), 원본이 바뀌면 새 폴더를 만든다.

학습 (mix): data.train → <data.output_dir>/train_sft.jsonl · val_sft.jsonl · DONE.json. 줄인 그림은 <cache_dir>/images/ (실험끼리 같이 씀).
  train      [경로 | {"path", "count"?, "format"?}]
             과제 폴더(studio 데이터셋, meta.json + tasks/): 문항 meta.split 이 train 이면 학습, val 이면 검증
             (폴더 meta.split 이 train 이면 표시 없는 문항도 학습). count: 이 데이터셋에서 쓸 문항 수 (무작위)
             ms-swift .jsonl ("format": "swift"): 줄 {"messages", "images"} 를 그대로 학습 (과제 이름 swift:<파일 이름>)
  task_mix   {과제: 비율} — 적힌 과제는 sft_max_examples 안에서 그 비율, 0 이면 뺌, 적히지 않은 과제는 있는 만큼 다.
             없으면 있는 비율대로 sft_max_examples 까지
평가 세트와 같은 문서·그림이 학습에 있으면 멈춘다. 그림 예산: 그림 하나는 image_max_size 의 토큰까지, 문항 하나는 모든 그림 합쳐
max_image_tokens_per_sample 까지 (여러 서류는 고르게 줄임). 평가 세트도 같은 규칙 (실험 묶음은 base 값으로 고정).
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

from .settings import image_tokens_for, locked, log

DEFAULTS = {
    "image_max_size": [2300, 1600],
    "max_image_tokens_per_sample": 12000,
    "sft_max_length": 16384,
    "sft_max_examples": 20000,
    "task_mix": None,
    "val_count": 200,
    "pack_turns": 8,
    "workers": min(16, os.cpu_count() or 1),
    "seed": 42,
}
BENCH_ITEM_KEYS = ("id", "task", "answer", "eval", "meta")
CHARS_PER_TOKEN = 0.67  # conservative for Korean text: assume 1.5 tokens per character
SET_VERSION = 2         # 평가 세트 폴더 꼴이 바뀌면 올린다 (지문에 들어감)


def load_folder(path: Path, fmt: str = "tasks", split: str = "test") -> tuple[dict, list[dict]]:
    """과제 폴더 → (meta, 문항). 문항의 images 는 절대 경로로. fmt "swift-fields": 실서류 swift .jsonl (train/swift_import.py),
    split 은 swift 문항의 쓰임 ("test" 평가, "train" 학습)."""
    from docgen.bench.tracking import enrich, source_id

    if fmt == "swift-fields":
        from .swift_import import load_swift

        meta, items = load_swift(path, split)
        origin = source_id(path.stem, meta)
        return meta, [enrich(it, origin) for it in items]
    meta_path = path / "meta.json"
    if not meta_path.is_file() or not (path / "tasks").is_dir():
        raise ValueError(f"{path}: 과제 폴더(meta.json + tasks/)가 아닙니다 — studio 데이터셋 폴더를 쓰세요 "
                         '(swift .jsonl 은 "format": "swift-fields" 와 함께)')

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


def perfect(it: dict) -> bool:
    """정답을 답으로 넣으면 만점인지. 채점 함수를 붙인 세트는 그 함수의 주 지표로 (낮을수록 좋은 지표는 0)."""
    spec = (it.get("eval") or {}).get("scorer")
    if not spec:
        return reward(it["task"], oracle_output(it), it) >= 1.0
    from docgen.bench.evaluate import LOWER_IS_BETTER, load_scorer

    r = load_scorer(spec)(it, oracle_output(it))
    main = r.get("main") or "f1"
    v = r["metrics"].get(main)
    return not r.get("parse_fail") and v is not None and (v <= 0.0 if main in LOWER_IS_BETTER else v >= 1.0)


def unreadable(items: list[dict]) -> tuple[list[dict], list[dict]]:
    """채점 함수가 정답을 읽지 못하거나 정답에 만점을 주지 않는 문항을 가른다 (swift 의 깨진 줄)."""
    good, bad = [], []
    for it in items:
        try:
            ok, why = perfect(it), "정답을 답으로 넣어도 만점이 아님"
        except Exception as exc:  # noqa: BLE001  사용자 채점 함수
            ok, why = False, f"{type(exc).__name__}: {exc}"
        (good if ok else bad).append(it if ok else {"id": it["id"], "line": it["meta"].get("line"), "why": why})
    return good, bad


def split_of(item: dict, folder_split: str) -> str:
    s = (item.get("meta") or {}).get("split")
    if s in ("train", "val"):
        return s
    if s in ("benchmark", "test"):
        return "test"
    return "train" if folder_split == "train" else "test"


def group_key(item: dict) -> str:
    """같은 문서의 문항끼리 같은 값: meta.document_id 가 있으면 그것, 없으면 문항 ID 의 서류 부분 ('kie/<서류>' → '<서류>')."""
    doc = (item.get("meta") or {}).get("document_id")
    if doc:
        return f"doc:{doc}"
    parts = item["id"].split("/")
    return parts[1] if len(parts) > 1 else item["id"].split(":")[0]


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
    """Image path under a token cap: the original if it already fits, else a resized copy in `folder`
    (PNG for inference, which sends PNG; JPEG quality 95 for training). Paths are planned first and
    the copies written together in parallel by run(). Existing copies are reused."""

    def __init__(self, folder: Path, factor: int):
        self.folder, self.factor, self.cache, self.jobs, self.size = Path(folder), factor, {}, {}, {}
        self.folder.mkdir(parents=True, exist_ok=True)

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
            st = src.stat()   # 원본이 바뀌면 새 이름 (실험끼리 같이 쓰는 폴더)
            name = hashlib.sha1(f"{src.resolve()}|{st.st_size}|{st.st_mtime_ns}|{cap}|{self.factor}".encode()).hexdigest()[:20]
            dst = self.folder / (name + (".png" if png else ".jpg"))
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




# -- 평가 세트 ---------------------------------------------------------------------------------
def _files(p):
    p = Path(p)
    files = [p] if p.is_file() else [p / "meta.json", *sorted((p / "tasks").glob("*.jsonl"))]
    return [[str(f.resolve()), f.stat().st_size, f.stat().st_mtime_ns] for f in files if f.is_file()]


def set_name(b: dict, size, budget, factor) -> str:
    scorer_file = (b.get("scorer") or "").partition(":")[0]
    sig = {"v": SET_VERSION, "set": {k: b.get(k) for k in ("id", "name", "group", "paths", "format", "gt", "scorer")},
           "files": [_files(p) for p in b["paths"]], "scorer": _files(scorer_file) if scorer_file else None,
           "image": [list(size), budget, factor]}
    return f"{b['id']}-{hashlib.sha256(json.dumps(sig, sort_keys=True).encode()).hexdigest()[:12]}"


def prepare_sets(benchmark: list[dict], cache_dir, size, budget, factor, workers=DEFAULTS["workers"]) -> dict:
    """정리한 평가 세트 목록(benchmarks.normalize) → {세트 id: 준비한 폴더}. 이미 있으면 그대로."""
    return {b["id"]: prepare_set(b, Path(cache_dir), size, budget, factor, workers) for b in benchmark}


def prepare_set(b: dict, cache_dir: Path, size, budget, factor, workers) -> Path:
    out = cache_dir / "sets" / set_name(b, size, budget, factor)
    if (out / "DONE.json").is_file():
        return out
    with locked(out, f"평가 세트 {b['id']}"):
        if (out / "DONE.json").is_file():
            return out
        log(f"평가 세트 {b['id']} 준비 → {out}")
        started = time.time()
        items, sources, references = [], {}, set()
        for path in b["paths"]:
            meta, rows = load_folder(Path(path), b.get("format", "tasks"))
            if b.get("gt"):
                meta = {**meta, "gt": b["gt"]}
            test = [it for it in rows if split_of(it, meta.get("split", "test")) == "test"]
            if not test:
                raise ValueError(f"benchmark {b['id']}: {path} 에 평가 문항이 없습니다 (학습 전용 데이터셋)")
            ref = meta.get("reference_type") or (meta.get("studio") or {}).get("gt") or meta.get("gt")
            ref = {"exact": "synthetic_exact", "reviewed": "human_reviewed", "pseudo": "ocr_pseudo_unreviewed"}.get(ref, ref)
            if ref:
                references.add(ref)
            test = [{**it, "meta": {**it["meta"], "benchmark_id": b["id"], "benchmark_name": b["name"],
                                    "benchmark_group": b["group"], "benchmark_path": path}} for it in test]
            if b.get("scorer"):   # 이 세트만 다른 채점 함수
                test = [{**it, "eval": {**(it.get("eval") or {}), "scorer": b["scorer"]}} for it in test]
            if any((it.get("eval") or {}).get("raw") for it in test):   # swift: 채점 함수가 정답을 못 읽는 줄은 건너뜀
                test, skipped = unreadable(test)
                if skipped:
                    log(f"WARNING: {Path(path).name}: 채점 함수({b['scorer']})가 정답을 읽지 못한 {len(skipped)}줄을 건너뜁니다 "
                        f"(예: {skipped[0]['id']} {skipped[0]['why']})")
                    meta = {**meta, "skipped": [*meta.get("skipped", []), *skipped]}
                if not test:
                    raise ValueError(f"benchmark {b['id']}: {path} 에서 채점 함수가 읽은 정답이 없습니다 (예: {skipped[0]['why']})")
            items += test
            sources[path] = {k: v for k, v in meta.items() if k != "doc_names"}
        if len(references) > 1:
            raise ValueError(f"benchmark {b['id']}: 정답 출처가 다릅니다. id 를 나누세요: {sorted(references)}")
        if len({it["id"] for it in items}) != len(items):
            raise ValueError(f"benchmark {b['id']}: 경로끼리 문항 ID 가 겹칩니다")
        # 정답을 답으로 넣으면 만점이어야 한다 (데이터와 채점 코드가 맞는지)
        bad = [it["id"] for it in random.Random(0).sample(items, min(200, len(items))) if not perfect(it)]
        if bad:
            raise ValueError(f"benchmark {b['id']}: 정답을 답으로 넣어도 만점이 아닙니다 (예: {bad[:3]}). 데이터를 만든 docgen 코드인지, "
                             "채점 함수를 붙인 세트면 그 함수가 정답에 만점을 주는지 보세요")
        per_image = image_tokens_for(size, factor)
        fit = Fitter(out / "images", factor)
        rows = []
        for it in items:
            cap = sample_caps(len(it["images"]), per_image, budget)
            imgs = [fit(p, cap, png=True) for p in it["images"]]
            row = {"id": it["id"], "task": it["task"], "images": imgs, "source_images": it["images"],
                   "messages": [{"role": "user", "content": "<image>" * len(imgs) + it["prompt"]}]}
            rows.append(row)
        fit.run(workers)
        write_jsonl(out / "tasks.jsonl", rows)
        write_jsonl(out / "items.jsonl", [{k: it[k] for k in BENCH_ITEM_KEYS if k in it} for it in items])
        by_task = {}
        for it in items:
            by_task[it["task"]] = by_task.get(it["task"], 0) + 1
        write_json(out / "DONE.json", {**{k: v for k, v in b.items()}, "n": len(items), "by_task": dict(sorted(by_task.items())),
                                       "reference": sorted(references), "image_max_size": list(size),
                                       "max_image_tokens_per_sample": budget, "pixels_per_token_side": factor,
                                       "sources": sources, "seconds": round(time.time() - started)})
        return out


def task_rows(set_dir, ids=None):
    """준비한 평가 세트의 (질문 줄, 정답 문항). ids 를 주면 그 문항만."""
    set_dir = Path(set_dir)
    rows = [r for r in read_jsonl(set_dir / "tasks.jsonl") if ids is None or r["id"] in ids]
    keep = {r["id"] for r in rows}
    return rows, [it for it in read_jsonl(set_dir / "items.jsonl") if it["id"] in keep]


# -- 학습 --------------------------------------------------------------------------------------
def mix(data_cfg: dict, factor: int, set_dirs, image_dir) -> dict:
    """학습 데이터 섞기 → data_cfg["output_dir"]. set_dirs: 준비한 평가 세트 폴더 (겹침 검사)."""
    from .benchmarks import train_entries
    from .swift_import import load_swift_train

    cfg = {**DEFAULTS, **{k: v for k, v in data_cfg.items() if v is not None}}
    out = Path(cfg["output_dir"])
    if (out / "DONE.json").exists():
        raise ValueError(f"{out} 은 이미 섞었습니다; 새 output_dir 를 쓰세요")
    out.mkdir(parents=True, exist_ok=True)
    started = time.time()
    seed = cfg["seed"]
    per_image = image_tokens_for(cfg["image_max_size"], factor)
    budget = cfg["max_image_tokens_per_sample"]
    fit = Fitter(Path(image_dir), factor)

    def cap(n):
        return sample_caps(n, per_image, budget)

    bench_keys, bench_images = set(), set()
    for d in set_dirs:
        rows, items = task_rows(d)
        bench_keys |= {group_key(it) for it in items}
        bench_images |= {str(Path(p).resolve()) for r in rows for p in r["source_images"]}

    pools, val_rows, sources, overlaps = {}, [], {}, []
    for e in train_entries(cfg["train"]):
        path = Path(e["path"])
        if e.get("format") == "swift":
            meta, items = load_swift_train(path)
            rows, n_val = [], 0
            for it in items:
                if bench_images & {str(Path(p).resolve()) for p in it["images"]}:
                    overlaps.append(f"{path.name} {it['id']}")
                else:
                    rows.append(it)
        else:
            meta, items = load_folder(path, "tasks", split="train")
            rows, n_val = [], 0
            for it in items:
                s = split_of(it, meta.get("split", "test"))
                if s == "test":
                    continue
                if group_key(it) in bench_keys or bench_images & {str(Path(p).resolve()) for p in it["images"]}:
                    overlaps.append(f"{path.name} {it['id']}")
                elif s == "val":
                    val_rows.append(it)
                    n_val += 1
                else:
                    rows.append(it)
            if not rows and not n_val:
                raise ValueError(f"train {path}: 학습 문항이 없습니다 (평가 전용 데이터셋이면 data.benchmark 에)")
        if e.get("count") is not None:
            rows.sort(key=lambda it: it["id"])
            random.Random(f"{seed}:{e['path']}").shuffle(rows)
            rows = rows[:int(e["count"])]
        for it in rows:
            pools.setdefault(it["task"], []).append(it)
        sources[e["path"]] = {"rows": len(rows), "val": n_val, "count": e.get("count"), "format": e.get("format", "tasks"),
                              "meta": {k: v for k, v in meta.items() if k != "doc_names"}}
    if overlaps:
        raise ValueError(f"학습 문항 {len(overlaps)}개가 평가 세트와 같은 문서·그림입니다 (예: {overlaps[:3]}). "
                         "학습 데이터를 따로 만드세요 (docgen.bench build --split train, OCR 준비의 문서 나누기)")
    if not pools:
        raise ValueError("SFT 문항이 없습니다: data.train 을 확인하세요")

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
        messages = it["messages"] if it.get("swift") else sft_record(it)["messages"]
        return {"messages": messages, "images": [fit(p, cap(len(it["images"])), png=False) for p in it["images"]],
                "pack": not it.get("swift")}

    def room_chars(images):
        return int((cfg["sft_max_length"] - sum(fit.image_tokens(p) for p in images) - 256) * CHARS_PER_TOKEN)

    packable, single, too_long = [], [], 0
    for it in chosen:
        s = to_sample(it)
        if sum(len(m["content"]) for m in s["messages"]) > room_chars(s["images"]):
            too_long += 1   # sft_max_length 를 넘음: 자르지 않고 뺀다
        else:
            (packable if s.pop("pack") else single).append(s)
    sft = (pack(packable, cfg["pack_turns"], room_chars) if cfg["pack_turns"] > 1 else packable) + single
    random.Random(seed).shuffle(sft)
    vals = [to_sample(it) for it in val]
    for s in vals:
        s.pop("pack")
    resized = fit.run(cfg["workers"])
    write_jsonl(out / "train_sft.jsonl", sft)
    write_jsonl(out / "val_sft.jsonl", vals)
    done = {
        "image_max_size": cfg["image_max_size"], "pixels_per_token_side": factor,
        "max_image_tokens_per_image": per_image, "max_image_tokens_per_sample": budget, "sft_max_length": cfg["sft_max_length"],
        "counts": {"sft_rows_by_task": {t: n for t, n in take.items() if n}, "sft_available_by_task": avail,
                   "sft_samples": len(sft), "sft_dropped_too_long": too_long, "val": len(vals), "resized_images": resized},
        "excluded_tasks": sorted(t for t in avail if not take.get(t)),
        "sources": sources, "benchmark_sets": [Path(d).name for d in set_dirs],
        "settings": {k: cfg[k] for k in DEFAULTS}, "seconds": round(time.time() - started),
    }
    write_json(out / "DONE.json", done)
    return {"output": str(out), **done["counts"]}
