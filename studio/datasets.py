"""⑥ 데이터셋 · ⑦ 평가의 서버 쪽: 데이터셋 등록부, 문항 보기, 모델 답 붙이기·채점, 데이터셋 설명서, 학습 기록.

등록부 <workspace_dir>/registry.json
  {"datasets": {"<ID>": {track, source, gt, real_data, path, format, name, created, frozen, runs: [...], card: {...}}},
   "trainings": [...]}

형식 (폴더 안의 파일로 알아낸다)
  bank_ocr/prepared   1부 OCR prepare 결과: DONE.json + pages.jsonl + benchmark_tasks.jsonl (8과제, 정답 = target)
  docgen.bench        은행 업무 평가 세트·학습 데이터: meta.json(version) + tasks/<과제>.jsonl
  bank_task/prepared  2부 prepare 결과: benchmark_items.jsonl(정답) + benchmark_tasks.jsonl(질문·이미지)

모델 답
  1부·2부 파이프라인: runs/<실험>/predictions/<run>.jsonl  {"id", "prediction"}, 점수 runs/<실험>/reports/*.json
  docgen.bench run:   <예측 폴더>/*.jsonl                  {"id", "output"}, 점수 <예측 폴더>/report.json
채점은 1부 bank_ocr.metrics, 은행 업무는 docgen.bench.evaluate (= 2부 bank_task.score 가 쓰는 것) 를 그대로 부른다.
등록한 폴더에는 쓰지 않는다. studio 가 낸 점수는 <workspace_dir>/scores/<ID>/<답 ID>.json.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import threading
import time
from functools import lru_cache
from pathlib import Path

from .config import ROOT

TRAINING = ROOT / "training"
if str(TRAINING) not in sys.path:   # 1부·2부 코드 (표준 라이브러리 + PIL)
    sys.path.insert(0, str(TRAINING))

_LOCK = threading.Lock()
TRACKS = ("ocr", "bank")
SOURCES = ("synthetic", "images", "results")
GTS = ("exact", "pseudo", "reviewed")
SOURCE_NAME = {"synthetic": "합성", "images": "이미지 묶음", "results": "결과 폴더"}
GT_NAME = {"exact": "생성 정답", "pseudo": "의사정답 (사내 OCR·추론 그대로)", "reviewed": "사람 검수 정답"}


class Registry:
    def __init__(self, workspace: Path, path_map: dict | None = None):
        self.ws = Path(workspace)
        self.file = self.ws / "registry.json"
        self.path_map = path_map or {}

    # -- 파일 ---------------------------------------------------------------
    def load(self) -> dict:
        if not self.file.exists():
            return {"datasets": {}, "trainings": []}
        d = json.loads(self.file.read_text(encoding="utf-8"))
        d.setdefault("datasets", {})
        d.setdefault("trainings", [])
        return d

    def save(self, d: dict) -> None:
        self.ws.mkdir(parents=True, exist_ok=True)
        tmp = self.file.with_suffix(".tmp")
        tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        tmp.replace(self.file)

    def get(self, ds_id: str) -> dict:
        d = self.load()["datasets"].get(ds_id)
        if d is None:
            raise KeyError(ds_id)
        return {"id": ds_id, **d}

    def update(self, ds_id: str, fn) -> dict:
        with _LOCK:
            d = self.load()
            if ds_id not in d["datasets"]:
                raise KeyError(ds_id)
            fn(d["datasets"][ds_id])
            self.save(d)
            return {"id": ds_id, **d["datasets"][ds_id]}

    # -- 등록 ---------------------------------------------------------------
    def register(self, path: str, name: str = "", **meta) -> dict:
        root = Path(path).expanduser()
        if not root.is_dir():
            raise ValueError(f"폴더가 없습니다: {root}")
        fmt = detect(root)
        if fmt is None:
            raise ValueError(f"{root}: 1부 prepare 결과(DONE.json + pages.jsonl), docgen.bench 결과(meta.json + tasks/), "
                             "2부 prepare 결과(benchmark_items.jsonl) 중 어느 것도 아닙니다")
        track = "ocr" if fmt == "bank_ocr/prepared" else "bank"
        info = describe(root, fmt)
        base = re.sub(r"[^\w.-]+", "-", name or root.name).strip("-") or "dataset"
        with _LOCK:
            d = self.load()
            for k, v in d["datasets"].items():
                if Path(v["path"]).resolve() == root.resolve():
                    raise ValueError(f"이미 등록된 폴더입니다 ({k})")
            ds_id, n = base, 2
            while ds_id in d["datasets"]:
                ds_id, n = f"{base}-{n}", n + 1
            entry = {
                "name": name or root.name, "track": track, "format": fmt, "path": str(root.resolve()),
                "source": meta.get("source") or info.get("source") or ("synthetic" if fmt != "bank_ocr/prepared" else "results"),
                "gt": meta.get("gt") or info.get("gt") or ("exact" if fmt != "bank_ocr/prepared" else "pseudo"),
                "real_data": bool(meta.get("real_data", info.get("real_data", False))),
                "registered": not meta.get("made_by_studio", False),
                "created": time.strftime("%Y-%m-%d %H:%M"), "frozen": bool(meta.get("frozen", False)),
                "version": info.get("version"), "counts": info.get("counts", {}), "runs": [],
                "card": {"purpose": meta.get("purpose", ""), "limits": meta.get("limits", ""), "not_for": ""},
            }
            for k in ("recipe", "dataset_json"):
                if meta.get(k):
                    entry[k] = meta[k]
            d["datasets"][ds_id] = entry
            self.save(d)
        return {"id": ds_id, **entry}

    def unregister(self, ds_id: str) -> None:
        with _LOCK:
            d = self.load()
            if ds_id not in d["datasets"]:
                raise KeyError(ds_id)
            del d["datasets"][ds_id]
            self.save(d)

    def attach_run(self, ds_id: str, path: str, label: str = "") -> dict:
        p = Path(path).expanduser()
        if not p.exists():
            raise ValueError(f"없는 경로: {p}")
        preds = find_predictions(p)
        if not preds:
            raise ValueError(f"{p}: 모델 답 파일(*.jsonl)을 찾지 못했습니다")

        def fn(e):
            if any(Path(r["path"]).resolve() == p.resolve() for r in e["runs"]):
                raise ValueError("이미 붙인 결과입니다")
            e["runs"].append({"path": str(p.resolve()), "label": label or p.name, "attached": time.strftime("%Y-%m-%d %H:%M")})
        return self.update(ds_id, fn)

    def set_card(self, ds_id: str, card: dict) -> dict:
        def fn(e):
            e["card"] = {k: str(card.get(k, e.get("card", {}).get(k, ""))) for k in ("purpose", "limits", "not_for")}
        return self.update(ds_id, fn)

    def set_frozen(self, ds_id: str, frozen: bool) -> dict:
        def fn(e):
            e["frozen"] = bool(frozen)
        return self.update(ds_id, fn)

    def set_meta(self, ds_id: str, meta: dict) -> dict:
        def fn(e):
            for k in ("name", "source", "gt", "real_data"):
                if k in meta:
                    v = meta[k]
                    if k == "source" and v not in SOURCES or k == "gt" and v not in GTS:
                        raise ValueError(f"{k}: 알 수 없는 값 {v}")
                    e[k] = bool(v) if k == "real_data" else v
        return self.update(ds_id, fn)

    # -- 경로 ---------------------------------------------------------------
    def resolve_file(self, ds: dict, p: str) -> Path | None:
        """문항에 적힌 이미지 경로를 이 컨테이너에서 찾는다: 그대로 → path_map 거꾸로 → 데이터셋 폴더 기준."""
        root = Path(ds["path"])
        cand = Path(p)
        if not cand.is_absolute():
            cand = root / cand
        if cand.exists():
            return cand
        for here, there in self.path_map.items():   # 학습 컨테이너 경로 → studio 경로
            if str(p).startswith(there):
                q = Path(here + str(p)[len(there):])
                if q.exists():
                    return q
        parts = Path(p).parts   # 다른 곳에서 만든 폴더: 데이터셋 폴더 이름 다음부터 붙여 본다
        if root.name in parts:
            q = root.joinpath(*parts[parts.index(root.name) + 1:])
            if q.exists():
                return q
        return None

    def allowed(self, ds: dict, f: Path) -> bool:
        """화면에 내줄 수 있는 파일: 이 데이터셋 폴더, 붙인 결과, 다른 등록 데이터셋 폴더 안의 것만
        (2부 prepare 결과가 docgen.bench 폴더의 이미지를 그대로 가리킬 때가 있다)."""
        f = f.resolve()
        roots = [Path(ds["path"]).resolve()] + [Path(r["path"]).resolve() for r in ds.get("runs", [])]
        roots += [Path(v["path"]).resolve() for v in self.load()["datasets"].values()]
        return any(f == r or r in f.parents for r in roots)


# ---------------------------------------------------------------------------
# 형식 알아내기·요약
# ---------------------------------------------------------------------------

def detect(root: Path) -> str | None:
    if (root / "DONE.json").is_file() and (root / "pages.jsonl").is_file():
        return "bank_ocr/prepared"
    if (root / "benchmark_items.jsonl").is_file():
        return "bank_task/prepared"
    meta = root / "meta.json"
    if meta.is_file() and (root / "tasks").is_dir():
        try:
            if "version" in json.loads(meta.read_text(encoding="utf-8")):
                return "docgen.bench"
        except ValueError:
            return None
    return None


def _read_jsonl(p: Path) -> list[dict]:
    return [json.loads(s) for s in p.read_text(encoding="utf-8-sig").splitlines() if s.strip()]


def describe(root: Path, fmt: str) -> dict:
    out: dict = {"counts": {}}
    if fmt == "bank_ocr/prepared":
        done = json.loads((root / "DONE.json").read_text(encoding="utf-8-sig"))
        out["version"] = done.get("ocr_revision") or (done.get("config") or {}).get("ocr_revision")
        snap = root / "config.snapshot.json"
        if snap.exists():
            cfg = json.loads(snap.read_text(encoding="utf-8-sig"))
            out["version"] = cfg.get("ocr_revision") or out["version"]
            if cfg.get("studio"):
                out.update({k: cfg["studio"][k] for k in ("source", "gt", "real_data") if k in cfg["studio"]})
        for split in ("train", "val", "benchmark"):
            f = root / f"{split}_tasks.jsonl"
            if f.exists():
                out["counts"][f"{split}_tasks"] = sum(1 for s in f.open(encoding="utf-8") if s.strip())
        pages = _read_jsonl(root / "pages.jsonl")
        out["counts"]["pages"] = len(pages)
        out["counts"]["documents"] = len({p.get("document_id") for p in pages})
    elif fmt == "docgen.bench":
        meta = json.loads((root / "meta.json").read_text(encoding="utf-8"))
        out["version"] = meta.get("version")
        out["counts"] = dict(meta.get("counts", {}))
        out["split"] = meta.get("split", "test")
        st = meta.get("studio") or {}
        out.update({k: st[k] for k in ("source", "gt", "real_data") if k in st})
    else:
        items = _read_jsonl(root / "benchmark_items.jsonl")
        c: dict = {}
        for it in items:
            c[it["task"]] = c.get(it["task"], 0) + 1
        out["counts"] = c
        done = root / "DONE.json"
        if done.exists():
            out["version"] = json.loads(done.read_text(encoding="utf-8-sig")).get("bench_version")
    return out


# ---------------------------------------------------------------------------
# 문항
# ---------------------------------------------------------------------------

@lru_cache(maxsize=16)
def _items_cached(path: str, fmt: str, mtime: float) -> dict[str, list[dict]]:
    root = Path(path)
    by_task: dict[str, list[dict]] = {}
    if fmt == "bank_ocr/prepared":
        for r in _read_jsonl(root / "benchmark_tasks.jsonl"):
            by_task.setdefault(r["task"], []).append(r)
    elif fmt == "docgen.bench":
        for f in sorted((root / "tasks").glob("*.jsonl")):
            by_task[f.stem] = _read_jsonl(f)
    else:
        tasks = {r["id"]: r for r in _read_jsonl(root / "benchmark_tasks.jsonl")} if (root / "benchmark_tasks.jsonl").exists() else {}
        for it in _read_jsonl(root / "benchmark_items.jsonl"):
            t = tasks.get(it["id"], {})
            prompt = next((m["content"] for m in t.get("messages", []) if m.get("role") == "user"), "")
            by_task.setdefault(it["task"], []).append({**it, "images": t.get("images", []),
                                                         "prompt": re.sub(r"^(<image>)+", "", prompt)})
    return by_task


def _mtime(ds: dict) -> float:
    root = Path(ds["path"])
    files = {"bank_ocr/prepared": [root / "benchmark_tasks.jsonl"], "bank_task/prepared": [root / "benchmark_items.jsonl"],
             "docgen.bench": list((root / "tasks").glob("*.jsonl"))}[ds["format"]]
    return max((f.stat().st_mtime for f in files if f.exists()), default=0.0)


def items(ds: dict) -> dict[str, list[dict]]:
    return _items_cached(ds["path"], ds["format"], _mtime(ds))


_BOX = re.compile(r"bbox_2d\s*=\s*\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]")


def view_item(ds: dict, it: dict) -> dict:
    """화면에 보일 모양으로: 질문, 이미지(주소), 정답(보기 좋게), 정답 박스(0~1000, 이미지마다)."""
    if ds["format"] == "bank_ocr/prepared":
        prompt = next((m["content"] for m in it.get("messages", []) if m.get("role") == "user"), "").replace("<image>\n", "")
        from bank_ocr.metrics import parse_target

        target = parse_target(it["target"])
        boxes = [{"img": 0, "box": t["bbox_2d"], "label": t.get("label", ""), "cls": "gt"} for t in target.get("boxes") or []]
        m = _BOX.search(prompt)
        if m:
            boxes.append({"img": 0, "box": [int(x) for x in m.groups()], "label": "질문 영역", "cls": "ask"})
        meta = {k: it.get(k) for k in ("document_id", "page_id", "view", "size", "confidence") if it.get(k) is not None}
        return {"id": it["id"], "task": it["task"], "images": it.get("images", []), "prompt": prompt,
                "answer": target["text"] if "text" in target else target.get("boxes"),
                "boxes": boxes, "meta": meta, "unit": 1000}
    boxes = []
    ans = it.get("answer")
    if isinstance(ans, list):   # 6단계 이후 kie·marks 답: [{"key","value","bbox_2d","page"}]
        for a in ans:
            if isinstance(a, dict) and a.get("bbox_2d"):
                boxes.append({"img": max(0, int(a.get("page", 1)) - 1), "box": a["bbox_2d"],
                              "label": f"{a.get('key', '')} = {a.get('value', '')}", "cls": "gt"})
    return {"id": it["id"], "task": it["task"], "images": it.get("images", []), "prompt": it.get("prompt", ""),
            "answer": ans, "boxes": boxes, "meta": it.get("meta", {}), "eval": it.get("eval"), "unit": 1000}


# ---------------------------------------------------------------------------
# 모델 답
# ---------------------------------------------------------------------------

def find_predictions(p: Path) -> list[Path]:
    """붙인 경로 안의 답 묶음. 파일 하나 = 한 묶음, runs/<실험>/predictions/*.jsonl = 파일마다 한 묶음 (1부·2부 파이프라인),
    그 밖의 폴더(docgen.bench run 의 예측 폴더: 과제마다 파일 하나) = 폴더 전체가 한 묶음."""
    if p.is_file():
        return [p] if p.suffix == ".jsonl" else []
    if (p / "predictions").is_dir():
        return sorted(f for f in (p / "predictions").glob("*.jsonl"))
    return [p] if any(p.glob("*.jsonl")) else []


def pred_id(path: Path) -> str:
    return hashlib.sha1(str(path.resolve()).encode()).hexdigest()[:10]


def predictions_of(ds: dict) -> list[dict]:
    out = []
    for run in ds.get("runs", []):
        rp = Path(run["path"])
        for f in find_predictions(rp):
            reports = rp / "reports" if (rp / "reports").is_dir() else None
            label = f.name if f.is_dir() else f.stem
            meta = f.with_suffix(f.suffix + ".meta.json")
            out.append({"pid": pred_id(f), "run": run["label"], "label": label, "path": str(f),
                        "meta": json.loads(meta.read_text(encoding="utf-8")) if meta.exists() else None,
                        "reports_dir": str(reports) if reports else None})
    return out


@lru_cache(maxsize=32)
def _load_pred(path: str, mtime: float) -> dict[str, str | None]:
    p = Path(path)
    out: dict[str, str | None] = {}
    for f in (sorted(p.glob("*.jsonl")) if p.is_dir() else [p]):
        for s in f.read_text(encoding="utf-8-sig").splitlines():
            if not s.strip():
                continue
            r = json.loads(s)
            v = r.get("prediction", r.get("output"))
            if v is not None or r["id"] not in out:
                out[r["id"]] = v
    return out


def load_pred(path: str) -> dict[str, str | None]:
    p = Path(path)
    mt = max((f.stat().st_mtime for f in p.glob("*.jsonl")), default=0.0) if p.is_dir() else p.stat().st_mtime
    return _load_pred(path, mt)


# ---------------------------------------------------------------------------
# 채점 (명령줄과 같은 함수)
# ---------------------------------------------------------------------------

def score(ds: dict, preds: dict[str, str | None]) -> dict:
    """과제별 점수와 문항별 점수. 답이 없는 문항은 명령줄과 같이 최악 점수로 센다."""
    by_task = items(ds)
    if ds["track"] == "ocr":
        from bank_ocr import metrics as OM

        rows = [r for rs in by_task.values() for r in rs]
        have = {r["id"]: OM.answer(preds[r["id"]]) for r in rows if preds.get(r["id"])}   # 빈 답은 답 없음으로 센다
        full = {r["id"]: have.get(r["id"], "") for r in rows}
        tasks = OM.evaluate_tasks(rows, full)
        per = {r["id"]: OM.reward(preds.get(r["id"]) or "", r["task"], r["target"]) for r in rows}
        return {"track": "ocr", "reference_type": "ocr_pseudo_unreviewed" if ds.get("gt") == "pseudo" else ds.get("gt"),
                "n": len(rows), "answered": len(have), "tasks": tasks, "main": {t: _ocr_main(t, m) for t, m in tasks.items()},
                "per_item": per}
    from docgen.bench import evaluate as E

    tasks, per = {}, {}
    for t in E.TASK_ORDER:
        if t in by_task:
            res = E.score_task(t, by_task[t], preds)
            for row in res.pop("per_item"):
                per[row["id"]] = row.get(E.MAIN[t])
            tasks[t] = res
    answered = sum(1 for rs in by_task.values() for r in rs if preds.get(r["id"]))
    return {"track": "bank", "n": sum(len(v) for v in by_task.values()), "answered": answered, "tasks": tasks,
            "main": {t: {"metric": r["main"], "value": r["metrics"].get(r["main"])} for t, r in tasks.items()},
            "per_item": per}


# 1부 비교표(bank_ocr.metrics.REPORT_METRICS)와 같은 대표 지표. cer 은 낮을수록 좋다.
_OCR_MAIN = {"crop_ocr": "cer", "bbox_ocr": "em", "region_ocr": "cer", "marked_ocr": "em",
             "grounding": "f1_iou50", "spotting": "e2e_f1", "relation": "e2e_f1", "marked_box": "f1_iou75"}
LOWER_IS_BETTER = {"cer"}


def _ocr_main(task: str, m: dict) -> dict:
    k = _OCR_MAIN.get(task)
    if k not in m:
        k = next((x for x in ("cer", "e2e_f1", "f1_iou50", "f1_iou75", "exact") if x in m), None)
    return {"metric": k, "value": m.get(k) if k else None}


def report_files(pred: dict) -> list[dict]:
    """파이프라인이 낸 점수 파일 (runs/<실험>/reports/*.json, 또는 예측 폴더의 report.json)."""
    out = []
    if pred.get("reports_dir"):
        for f in sorted(Path(pred["reports_dir"]).glob("*.json")):
            out.append({"path": str(f), "name": f.stem})
    else:
        p = Path(pred["path"])
        f = (p if p.is_dir() else p.parent) / "report.json"
        if f.exists():
            out.append({"path": str(f), "name": "report"})
    return out


# ---------------------------------------------------------------------------
# 데이터셋 설명서
# ---------------------------------------------------------------------------

def card_markdown(ds: dict, scores: list[dict], trainings: list[dict]) -> str:
    c = ds.get("card", {})
    lines = [f"# {ds['name']}", "",
             f"- ID: `{ds['id']}` · 벤치마크: {'OCR' if ds['track'] == 'ocr' else '은행 업무'} · 형식: `{ds['format']}`",
             f"- 출처: {SOURCE_NAME.get(ds['source'], ds['source'])} · 정답: {GT_NAME.get(ds['gt'], ds['gt'])}"
             f"{' · **실서류** (저장소·외부 분석기 금지)' if ds.get('real_data') else ''}",
             f"- 폴더: `{ds['path']}`" + (" (등록만 한 폴더, studio 는 읽기만)" if ds.get("registered") else ""),
             f"- 버전: {ds.get('version') or '-'} · 등록: {ds.get('created')} · {'고정됨' if ds.get('frozen') else '고정 전'}",
             "", "## 목적", c.get("purpose") or "(사람이 적는다)", "",
             "## 쓰면 안 되는 곳", c.get("not_for") or "(사람이 적는다)", "",
             "## 알려진 한계", c.get("limits") or "(사람이 적는다)"]
    if ds.get("gt") == "pseudo":
        lines.append("- 정답이 사내 OCR·추론 그대로라 점수는 '그것과 얼마나 같은지'다 (실제 정확도 아님).")
    lines += ["", "## 구성", "", "| 항목 | 수 |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted((ds.get("counts") or {}).items())]
    if scores:
        lines += ["", "## 점수 요약", ""]
        tasks = sorted({t for s in scores for t in s["main"]})
        lines.append("| 모델 답 | " + " | ".join(tasks) + " |")
        lines.append("|---|" + "---:|" * len(tasks))
        for s in scores:
            cells = []
            for t in tasks:
                m = s["main"].get(t) or {}
                v = m.get("value")
                cells.append("-" if v is None else f"{v * 100:.1f} ({m.get('metric')})")
            lines.append(f"| {s['label']} | " + " | ".join(cells) + " |")
    if trainings:
        lines += ["", "## 이 데이터셋을 쓴 학습", ""]
        lines += [f"- {t['name']} ({t['pipeline']}, {t['created']}){' → ' + t['run'] if t.get('run') else ''}" for t in trainings]
    return "\n".join(lines) + "\n"
