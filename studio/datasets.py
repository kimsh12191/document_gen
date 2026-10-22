"""⑥ 데이터셋 · ⑦ 평가의 서버 쪽: 데이터셋 등록부, 문항 보기, 모델 답 붙이기·채점, 데이터셋 설명서, 학습 기록.
API 는 studio/api_datasets.py, 화면은 static/js/datasets.js·dataset-builds.js.

등록부 <workspace_dir>/registry.json
  {"datasets": {"<ID>": {groups, kind, source, gt, real_data, path, format, name, created, frozen, split, runs: [...], card: {...}}},
   "trainings": [...]}

형식은 하나 (studio/DESIGN.md 17절): docgen-tasks — meta.json + tasks/<과제>.jsonl, 문항 {id, task, images, prompt, answer, eval, meta}.
  docgen.bench build(합성 업무·문서 과제), OCR 준비(docgen.bench.ocr_prepare: 쪽 OCR 8과제, 문항 meta.split 이 train·val·benchmark),
  라벨 있는 데이터·원본 데이터 내보내기가 모두 이 형식을 쓴다. tasks/ 가 없는 옛 OCR 준비 폴더는 등록할 때 tasks/ 를 만들어 준다.
  과제 묶음(groups: ocr·doc·work)은 들어 있는 과제로 정한다 (옛 track 대신).

모델 답
  학습 실행(train/): runs/<실험>/predictions/<run>.jsonl  {"id", "prediction"}, 점수 runs/<실험>/reports/*.json
  docgen.bench run:  <예측 폴더>/*.jsonl                  {"id", "output"}, 점수 <예측 폴더>/report.json
채점은 모든 과제가 docgen.bench.evaluate (학습 보상과 같은 함수). 평가 문항 = 문항 meta.split 이 train·val 이 아닌 것.
등록한 폴더에는 쓰지 않는다. studio 가 낸 점수는 <workspace_dir>/scores/<ID>/<답 ID>.json.
"""
from __future__ import annotations

import hashlib
import json
import re
import threading
import time
from functools import lru_cache
from pathlib import Path

_LOCK = threading.Lock()
FORMAT = "docgen-tasks"
SOURCES = ("synthetic", "images", "results")
GTS = ("exact", "pseudo", "reviewed")
SOURCE_NAME = {"synthetic": "합성", "images": "이미지 묶음", "results": "결과 폴더"}
GROUP_NAME = {"ocr": "OCR", "doc": "문서 이해", "work": "업무 처리"}
GT_NAME = {"exact": "생성 정답", "pseudo": "의사정답 (사내 OCR·추론 그대로)", "reviewed": "사람 검수 정답"}


def _migrate(e: dict) -> None:
    """옛 등록부 줄(track·옛 형식 이름)을 과제 형식으로 읽는다. tasks/ 없는 옛 OCR 준비 폴더는 그 자리에서 tasks/ 를 만든다."""
    if e.get("format") == FORMAT and "groups" in e:
        return
    root = Path(e.get("path", ""))
    if e.get("format") != FORMAT and root.is_dir() and detect(root) is None and legacy_ocr(root):
        try:
            upgrade_ocr(root)
        except (OSError, ValueError, KeyError):
            pass
    if detect(root) == FORMAT:
        info = describe(root, FORMAT)
        e.update(format=FORMAT, groups=info["groups"], kind=info.get("kind"), counts=info["counts"])
    else:
        e.setdefault("groups", ["ocr"] if e.get("track") == "ocr" else ["doc"])
    e.pop("track", None)


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
        for e in d["datasets"].values():
            _migrate(e)
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
        if detect(root) is None and legacy_ocr(root):
            upgrade_ocr(root)
        fmt = detect(root)
        if fmt is None:
            raise ValueError(f"{root}: 과제 폴더(meta.json + tasks/<과제>.jsonl)가 아닙니다 (docgen.bench build, OCR 준비 결과)")
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
                "name": name or root.name, "groups": info["groups"], "kind": info.get("kind"), "format": fmt, "path": str(root.resolve()),
                "source": meta.get("source") or info.get("source") or "synthetic",
                "gt": meta.get("gt") or info.get("gt") or "exact",
                "real_data": bool(meta.get("real_data", info.get("real_data", False))),
                "registered": not meta.get("made_by_studio", False),
                "created": time.strftime("%Y-%m-%d %H:%M"), "frozen": bool(meta.get("frozen", False)),
                "version": info.get("version"), "counts": info.get("counts", {}), "runs": [], "split": info.get("split"),
                "card": {"purpose": meta.get("purpose", ""), "limits": meta.get("limits", ""), "not_for": ""},
            }
            for k in ("recipe", "dataset_json"):
                if meta.get(k):
                    entry[k] = meta[k]
            if info.get("pseudo_model"):   # 의사정답을 낸 모델 (그 모델은 이 세트로 채점하지 않는다)
                entry["pseudo_model"] = info["pseudo_model"]
            dj = root / entry.get("dataset_json", "dataset.json")
            if dj.exists():   # studio 레시피로 만든 것: 생성기 커밋·버전·서식 해시
                info_dj = json.loads(dj.read_text(encoding="utf-8"))
                entry["build"] = {k: info_dj.get(k) for k in ("generator_commit", "version", "created", "unit", "split")
                                  if info_dj.get(k) is not None}
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
        (합친 데이터셋은 다른 과제 폴더의 이미지를 가리킬 때가 있다)."""
        f = f.resolve()
        roots = [Path(ds["path"]).resolve()] + [Path(r["path"]).resolve() for r in ds.get("runs", [])]
        roots += [Path(v["path"]).resolve() for v in self.load()["datasets"].values()]
        return any(f == r or r in f.parents for r in roots)


# ---------------------------------------------------------------------------
# 형식 알아내기·요약
# ---------------------------------------------------------------------------

def detect(root: Path) -> str | None:
    meta = root / "meta.json"
    if meta.is_file() and (root / "tasks").is_dir():
        try:
            if "version" in json.loads(meta.read_text(encoding="utf-8")):
                return FORMAT
        except ValueError:
            return None
    return None


def legacy_ocr(root: Path) -> bool:
    """tasks/ 없이 옛 1부 형식 문항만 있는 OCR 준비 폴더."""
    return (root / "DONE.json").is_file() and (root / "benchmark_tasks.jsonl").is_file() and not (root / "tasks").is_dir()


def upgrade_ocr(root: Path) -> None:
    from docgen.bench.ocr_prepare import write_tasks

    cfg = json.loads((root / "config.snapshot.json").read_text(encoding="utf-8")) if (root / "config.snapshot.json").exists() else {}
    cfg.setdefault("ocr_revision", "unknown")
    write_tasks(root, cfg, json.loads((root / "DONE.json").read_text(encoding="utf-8")))


def _read_jsonl(p: Path) -> list[dict]:
    return [json.loads(s) for s in p.read_text(encoding="utf-8-sig").splitlines() if s.strip()]


GT_OF_REFERENCE = {"synthetic_exact": "exact", "human_reviewed": "reviewed", "ocr_pseudo_unreviewed": "pseudo"}


def groups_of(counts: dict) -> list[str]:
    from docgen.bench.evaluate import TASK_GROUP

    return sorted({TASK_GROUP.get(t, "doc") for t, n in counts.items() if n}, key=["ocr", "doc", "work"].index)


def describe(root: Path, fmt: str) -> dict:
    meta = json.loads((root / "meta.json").read_text(encoding="utf-8"))
    out: dict = {"version": meta.get("version"), "counts": dict(meta.get("counts", {})), "split": meta.get("split", "test"),
                 "kind": meta.get("kind") or "bench"}
    if meta.get("split_counts"):
        out["counts"].update({f"{k}_items": v for k, v in meta["split_counts"].items()})
    st = meta.get("studio") or {}
    if meta.get("reference_type") in GT_OF_REFERENCE:
        out["gt"] = GT_OF_REFERENCE[meta["reference_type"]]
    out.update({k: st[k] for k in ("source", "gt", "real_data", "pseudo_model") if k in st})
    if (root / "pages.jsonl").is_file() and (root / "DONE.json").is_file():   # OCR 준비: 쪽·문서 수
        pages = _read_jsonl(root / "pages.jsonl")
        out["counts"]["pages"] = len(pages)
        out["counts"]["documents"] = len({p.get("document_id") for p in pages})
    out["groups"] = groups_of(meta.get("counts", {}))
    return out


def merge_tasks(dst: Path, src: Path) -> dict:
    """src 과제 폴더의 문항을 dst 과제 폴더에 더한다 (OCR·업무 과제를 한 데이터셋으로). src 는 dst 안에 있어야 하고, 그림 경로는
    dst 기준으로 고친다. dst 에 meta.json 이 없으면 src 것으로 시작한다. dataset.json 이 있으면 문항 수를 맞춘다."""
    dst, src = Path(dst).resolve(), Path(src).resolve()
    rel = src.relative_to(dst).as_posix()
    fix = lambda p: p if not p or Path(p).is_absolute() else f"{rel}/{p}"  # noqa: E731
    sm = json.loads((src / "meta.json").read_text(encoding="utf-8"))
    dm = json.loads((dst / "meta.json").read_text(encoding="utf-8")) if (dst / "meta.json").exists() else \
        {**{k: v for k, v in sm.items() if k not in ("counts", "split_counts")}, "counts": {}}
    (dst / "tasks").mkdir(exist_ok=True)
    added = {}
    for f in sorted((src / "tasks").glob("*.jsonl")):
        rows = _read_jsonl(f)
        for r in rows:
            r["images"] = [fix(i) for i in r.get("images", [])]
            if (r.get("meta") or {}).get("context_image"):
                r["meta"]["context_image"] = fix(r["meta"]["context_image"])
        with (dst / "tasks" / f.name).open("a", encoding="utf-8") as out:
            out.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        added[f.stem] = len(rows)
    for t, n in added.items():
        dm["counts"][t] = dm["counts"].get(t, 0) + n
    if dm is not sm and dm.get("split") != sm.get("split"):
        dm["split"] = "mixed"
    if sm.get("split_counts"):
        dm["split_counts"] = {k: dm.get("split_counts", {}).get(k, 0) + v for k, v in sm["split_counts"].items()}
    if dm.get("kind") and sm.get("kind") and dm["kind"] != sm["kind"]:
        dm["kind"] = "mixed"
    dm.setdefault("parts", []).append({"path": rel, "kind": sm.get("kind"), "version": sm.get("version"), "counts": added})
    (dst / "meta.json").write_text(json.dumps(dm, ensure_ascii=False, indent=1), encoding="utf-8")
    if (dst / "dataset.json").exists():
        dj = json.loads((dst / "dataset.json").read_text(encoding="utf-8"))
        dj["counts"] = dm["counts"]
        (dst / "dataset.json").write_text(json.dumps(dj, ensure_ascii=False, indent=1), encoding="utf-8")
    return added


# ---------------------------------------------------------------------------
# 문항
# ---------------------------------------------------------------------------

@lru_cache(maxsize=16)
def _items_cached(path: str, mtime: float) -> dict[str, list[dict]]:
    from docgen.bench.tracking import enrich, source_id

    root = Path(path)
    meta = json.loads((root / "meta.json").read_text(encoding="utf-8"))
    origin = source_id(root.name, meta)
    return {f.stem: [enrich(it, origin) for it in _read_jsonl(f)] for f in sorted((root / "tasks").glob("*.jsonl"))}


def _mtime(ds: dict) -> float:
    files = [Path(ds["path"]) / "meta.json", *(Path(ds["path"]) / "tasks").glob("*.jsonl")]
    return max((f.stat().st_mtime for f in files if f.exists()), default=0.0)


def items(ds: dict, evaluation: bool = False) -> dict[str, list[dict]]:
    """과제 → 문항. evaluation=True 면 평가 문항만 (문항 meta.split 이 train·val 인 것은 학습용이라 뺀다)."""
    by = _items_cached(ds["path"], _mtime(ds))
    if not evaluation:
        return by
    folder_split = ds.get("split") or json.loads((Path(ds["path"]) / "meta.json").read_text(encoding="utf-8")).get("split", "test")
    out = {t: [r for r in rs if ((r.get("meta") or {}).get("split") or folder_split) not in ("train", "val")] for t, rs in by.items()}
    return {t: rs for t, rs in out.items() if rs}


_BOX = re.compile(r"bbox_2d\s*=\s*\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]")


def view_item(ds: dict, it: dict) -> dict:
    """화면에 보일 모양으로: 질문, 이미지(주소), 정답(보기 좋게), 정답 박스(0~1000, 이미지마다). OCR·업무 과제 모두 같은 꼴."""
    boxes = []
    ans = it.get("answer")
    prompt = it.get("prompt", "")
    if isinstance(ans, dict) and ("boxes" in ans or "text" in ans):   # OCR 과제: {"text"} / {"boxes": [{bbox_2d, label}]}
        boxes = [{"img": 0, "box": b["bbox_2d"], "label": b.get("label", ""), "cls": "gt"} for b in ans.get("boxes") or []]
        ans = ans["text"] if "text" in ans else ans.get("boxes")
    elif isinstance(ans, list):   # kie·marks 답: [{"key","value","bbox_2d","page"}]
        for a in ans:
            if isinstance(a, dict) and a.get("bbox_2d"):
                boxes.append({"img": max(0, int(a.get("page", 1)) - 1), "box": a["bbox_2d"],
                              "label": f"{a.get('key', '')} = {a.get('value', '')}", "cls": "gt"})
    m = _BOX.search(prompt)
    if m:
        boxes.append({"img": 0, "box": [int(x) for x in m.groups()], "label": "질문 영역", "cls": "ask"})
    meta = {k: v for k, v in (it.get("meta") or {}).items() if v is not None and k not in ("context_image", "view_ops")}
    return {"id": it["id"], "task": it["task"], "images": it.get("images", []), "prompt": prompt,
            "answer": ans, "boxes": boxes, "meta": meta, "eval": it.get("eval"), "unit": 1000}


# ---------------------------------------------------------------------------
# 모델 답
# ---------------------------------------------------------------------------

def find_predictions(p: Path) -> list[Path]:
    """붙인 경로 안의 답 묶음. 파일 하나 = 한 묶음, runs/<실험>/predictions/*.jsonl = 파일마다 한 묶음 (학습 실행 train/),
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

def self_scoring(ds: dict, pred: dict) -> str | None:
    """의사정답 세트를 그 정답을 낸 모델의 답으로 채점하려 하면 까닭을 돌려준다 (DESIGN.md 15.4: 자기 답으로 자기를 채점하는 꼴)."""
    m = ds.get("pseudo_model") if ds.get("gt") == "pseudo" else None
    if not m:
        return None
    if m == ((pred.get("meta") or {}).get("model")) or m in (pred.get("label"), pred.get("run")):
        return f"이 세트의 정답은 {m} 의 추출 결과 그대로라 {m} 의 답은 채점할 수 없습니다. 검수한 정답(reviewed) 세트로 채점하세요"
    return None


def score(ds: dict, preds: dict[str, str | None]) -> dict:
    """과제별 점수와 문항별 점수 (평가 문항만). 모든 과제가 docgen.bench.evaluate.score_task — 명령줄·학습 보고서와 같은 함수.
    답이 없는 문항은 최악 점수로 센다 (OCR 과제는 빈 글자로)."""
    from docgen.bench import evaluate as E

    by_task = items(ds, evaluation=True)
    tasks, per = {}, {}
    for t in [*E.TASK_ORDER, *sorted(set(by_task) - set(E.TASK_ORDER))]:
        if t in by_task and t in E.MAIN:
            res = E.score_task(t, by_task[t], preds)
            for row in res.pop("per_item"):
                per[row["id"]] = row.get(res["main"])
            tasks[t] = res
    answered = sum(1 for t in tasks for r in by_task[t] if preds.get(r["id"]))
    refs = {(r.get("meta") or {}).get("reference_type") for t in tasks for r in by_task[t]} - {None}
    from docgen.bench.tracking import evaluate_groups

    tracking = evaluate_groups([r for t in tasks for r in by_task[t]], preds, tasks)
    return {"groups": ds.get("groups") or groups_of({t: 1 for t in tasks}), "reference_type": refs.pop() if len(refs) == 1 else None,
            "n": sum(len(by_task[t]) for t in tasks), "answered": answered, "tasks": tasks,
            "main": {t: {"metric": r["main"], "value": r["metrics"].get(r["main"])} for t, r in tasks.items()},
            "per_item": per, **tracking}


LOWER_IS_BETTER = {"cer", "false_alarm", "matched_label_cer"}   # docgen.bench.evaluate.LOWER_IS_BETTER 와 같음


def report_files(pred: dict) -> list[dict]:
    """파이프라인이 낸 점수 파일 (runs/<실험>/reports/*.json, 또는 예측 폴더의 report.json)."""
    out = []
    if pred.get("reports_dir"):
        for f in sorted(Path(pred["reports_dir"]).glob("*.json")):
            if f.name.endswith(".breakdowns.json"):
                continue
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
             f"- ID: `{ds['id']}` · 과제: {' · '.join(GROUP_NAME.get(g, g) for g in ds.get('groups') or [])} · 형식: `{ds['format']}`",
             f"- 출처: {SOURCE_NAME.get(ds['source'], ds['source'])} · 정답: {GT_NAME.get(ds['gt'], ds['gt'])}"
             f"{' · **실서류** (저장소·외부 분석기 금지)' if ds.get('real_data') else ''}",
             f"- 폴더: `{ds['path']}`" + (" (등록만 한 폴더, studio 는 읽기만)" if ds.get("registered") else ""),
             f"- 버전: {ds.get('version') or '-'} · 등록: {ds.get('created')} · {'고정됨' if ds.get('frozen') else '고정 전'}",
             "", "## 목적", c.get("purpose") or "(사람이 적는다)", "",
             "## 쓰면 안 되는 곳", c.get("not_for") or "(사람이 적는다)", "",
             "## 알려진 한계", c.get("limits") or "(사람이 적는다)"]
    if ds.get("gt") == "pseudo":
        lines.append("- 정답이 사내 OCR·추론 그대로라 점수는 '그것과 얼마나 같은지'다 (실제 정확도 아님)."
                     + (f" 정답을 낸 모델({ds['pseudo_model']})은 이 세트로 채점하지 않는다." if ds.get("pseudo_model") else ""))
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
