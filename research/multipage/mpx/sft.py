"""ms-swift 학습 데이터 만들기. training/train.py 가 그대로 읽는 폴더 두 개를 만든다 (이미지는 절대 경로).

  <out>/swift_page/train_sft.jsonl  쪽 단위 문항. 앞 쪽까지의 정답으로 상태를 만들고(--state, mix 면 none/doc/tail/context 를 고루),
              --noise 확률로 상태를 일부러 틀리게 해서(행 수 ±1, 마지막 행 바꿔치기, 목록 정보 빠뜨림) 틀린 상태에서도
              이 쪽을 바르게 읽도록 가르친다. 정답은 언제나 이 쪽의 실제 내용.
  <out>/swift_all/train_sft.jsonl   한 번에 넣기 비교 방법의 학습 문항. 쪽 이미지를 예산(--budget)에 맞춰 줄인 사본을 images_b<예산>/ 에 저장.
"""
from __future__ import annotations

import copy
import json
import random
from pathlib import Path

from .common import dumps, load_resized, page_budget
from .gen import load
from .pages import STATES, all_prompt, build_state, merge_pages, page_prompt
from .run import oracle_documents, oracle_page


def corrupt(state: dict, rng: random.Random) -> dict:
    s = copy.deepcopy(state)
    lists = s.get("lists") or {}
    choice = rng.random()
    if lists and choice < 0.4:
        path = rng.choice(sorted(lists))
        lists[path]["count"] = max(0, lists[path]["count"] + rng.choice([-1, 1]))
    elif lists and choice < 0.7:
        path = rng.choice(sorted(lists))
        lists[path]["last"] = {k: None for k in lists[path]["last"]}
    elif lists:
        s.pop("lists")
    else:
        s["document"]["pages_read"] = max(1, s["document"]["pages_read"] + rng.choice([-1, 1]))
    return s


def page_records(bundle: dict, labels: dict, data_dir: Path, state_mode: str, noise: float, rng: random.Random):
    cache: dict = {}
    answers = [oracle_page(bundle, labels, i, cache) for i in range(len(bundle["pages"]))]
    for i, p in enumerate(bundle["pages"]):
        kind = rng.choice(STATES) if state_mode == "mix" else state_mode
        docs = merge_pages(answers[:i]) if i else []
        st = build_state(docs[-1] if docs else None, kind)
        noisy = bool(st) and rng.random() < noise
        if noisy:
            st = corrupt(st, rng)
        yield {"id": f"{bundle['id']}:p{i + 1}", "task": "page", "state": kind, "noisy": noisy,
               "images": [str((data_dir / p["image"]).resolve())],
               "messages": [{"role": "user", "content": "<image>\n" + page_prompt(st)},
                            {"role": "assistant", "content": dumps(answers[i])}]}


def all_record(bundle: dict, labels: dict, data_dir: Path, budget: int) -> dict:
    n = len(bundle["pages"])
    per = page_budget(n, budget)
    sub = f"images_b{budget}"
    images = []
    for p in bundle["pages"]:
        rel = f"{sub}/{Path(p['image']).stem}.png"
        if not (data_dir / rel).exists():
            (data_dir / sub).mkdir(parents=True, exist_ok=True)
            load_resized(data_dir / p["image"], per).save(data_dir / rel)
        images.append(str((data_dir / rel).resolve()))
    return {"id": f"{bundle['id']}:all", "task": "all", "images": images,
            "messages": [{"role": "user", "content": "<image>" * n + "\n" + all_prompt(n)},
                         {"role": "assistant", "content": dumps({"documents": oracle_documents(bundle, labels)})}]}


def build(data_dir, out=None, methods=("pagewise", "allatonce"), state: str = "mix", noise: float = 0.2,
          budget: int = 12000, seed: int = 0) -> dict:
    data_dir = Path(data_dir)
    out = Path(out) if out else data_dir
    bundles, labels = load(data_dir)
    rng = random.Random(seed)
    stats = {}
    jobs = []
    if "pagewise" in methods:
        jobs.append(("swift_page", lambda b: page_records(b, labels, data_dir, state, noise, rng)))
    if "allatonce" in methods:
        jobs.append(("swift_all", lambda b: [all_record(b, labels, data_dir, budget)]))
    for name, make in jobs:
        d = out / name
        d.mkdir(parents=True, exist_ok=True)
        lens = []
        with (d / "train_sft.jsonl").open("w", encoding="utf-8") as f:
            for b in bundles:
                for r in make(b):
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
                    lens.append(len(r["messages"][1]["content"]))
        stats[name] = _len_stats(lens)
        # training/train.py 가 확인하는 완료 표시. 이미지 상한은 1부·2부와 같다 (IMAGE_MAX_TOKEN_NUM 3600 으로 계산됨)
        (d / "DONE.json").write_text(json.dumps({"image_max_size": [2300, 1600], "source": str(data_dir.resolve()),
                                                 "state": state, "noise": noise, "budget": budget, **stats[name]},
                                                ensure_ascii=False, indent=1), encoding="utf-8")
    return stats


def _len_stats(lens: list[int]) -> dict:
    s = sorted(lens)
    return {"records": len(s), "answer_chars_p50": s[len(s) // 2] if s else 0,
            "answer_chars_p95": s[int(len(s) * 0.95)] if s else 0, "answer_chars_max": s[-1] if s else 0}
