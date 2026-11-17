"""설정의 평가 세트(data.benchmark)·학습 데이터(data.train) 칸 읽기.

평가 세트 하나: {"id", "name"?, "group"?, "paths": [...], "format"?, "gt"?, "scorer"?} — 세트마다 점수가 따로 나온다.
  format: "tasks"(기본, studio 과제 폴더) | "swift-fields"(ms-swift .jsonl, train/swift_import.py — 정답 글을 그대로 채점 함수에)
  gt: 정답 출처 "exact"·"reviewed"·"pseudo" (폴더의 meta.json 보다 우선)
  scorer: 이 세트만 다르게 채점 "<파일.py>:<함수>" (설정 파일 기준 상대 경로). swift-fields 는 적지 않으면 train/scorers/swift_default.py
학습 데이터 하나: 경로(과제 폴더) 또는 {"path", "count"?, "format"?}
  format: "tasks"(기본) | "swift"(ms-swift .jsonl 그대로 학습, 밖에서 가져온 데이터. "swift-fields" 로 적어도 같음)
"""
import hashlib
import re
from pathlib import Path

FORMATS = ("tasks", "swift-fields")
GTS = ("exact", "reviewed", "pseudo")
SWIFT_DEFAULT = str(Path(__file__).resolve().parent / "scorers" / "swift_default.py") + ":score"


def normalize(spec):
    entries = spec if isinstance(spec, list) else [spec]
    result, ids, paths_seen = [], set(), set()
    for entry in entries:
        value = {"path": entry} if isinstance(entry, str) else entry
        if not isinstance(value, dict) or ("path" in value and "paths" in value):
            raise ValueError("benchmark: path 또는 paths 중 하나를 적으세요")
        paths = value.get("paths", [value["path"]] if "path" in value else [])
        if not isinstance(paths, list) or not paths or any(not isinstance(p, str) or not p.strip() for p in paths):
            raise ValueError("benchmark.paths 는 비어 있지 않은 경로 목록이어야 합니다")
        ident = value.get("id") or "set-" + hashlib.sha256(str(Path(paths[0]).resolve()).encode()).hexdigest()[:8]
        if not isinstance(ident, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", ident) or ident in ids:
            raise ValueError(f"benchmark.id 는 겹치지 않는 영문·숫자·점·밑줄·하이픈이어야 합니다: {ident}")
        ids.add(ident)
        for p in paths:
            key = str(Path(p).resolve())
            if key in paths_seen:
                raise ValueError(f"평가 경로를 두 번 적었습니다: {p}")
            paths_seen.add(key)
        name, group = value.get("name", ident), value.get("group", "ungrouped")
        if any(not isinstance(v, str) or not v.strip() for v in (name, group)):
            raise ValueError("benchmark.name·group 은 비어 있지 않은 글이어야 합니다")
        fmt, gt = value.get("format", "tasks"), value.get("gt")
        if fmt not in FORMATS:
            raise ValueError(f"benchmark.format 은 {', '.join(FORMATS)} 중 하나입니다: {fmt}")
        if gt is not None and gt not in GTS:
            raise ValueError(f"benchmark.gt 는 {', '.join(GTS)} 중 하나입니다: {gt}")
        for p in paths:
            if (fmt == "swift-fields") != p.endswith(".jsonl"):
                raise ValueError(f"{p}: swift .jsonl 은 \"format\": \"swift-fields\" 와 함께, 그 밖의 경로는 과제 폴더로 적습니다")
        scorer = value.get("scorer") or (SWIFT_DEFAULT if fmt == "swift-fields" else None)
        if scorer is not None:
            if not isinstance(scorer, str) or not scorer.partition(":")[0].endswith(".py"):
                raise ValueError(f"benchmark {ident}: scorer 는 \"<파일.py>:<함수>\" 입니다: {scorer}")
            from docgen.bench.evaluate import load_scorer

            load_scorer(scorer)   # 파일·함수가 있는지 돌리기 전에
        result.append({"id": ident, "name": name.strip(), "group": group.strip(), "paths": paths,
                       **({"format": fmt} if fmt != "tasks" else {}), **({"gt": gt} if gt else {}),
                       **({"scorer": scorer} if scorer else {})})
    return result


def train_entries(spec) -> list[dict]:
    """data.train 칸 → [{"path", "format"?: "swift", "count"?}]."""
    out = []
    for e in spec if isinstance(spec, list) else [spec]:
        e = dict(e) if isinstance(e, dict) else {"path": e}
        if not isinstance(e.get("path"), str) or not e["path"].strip():
            raise ValueError(f"data.train: 경로(path)가 없습니다: {e}")
        unknown = set(e) - {"path", "format", "count"}
        if unknown:
            raise ValueError(f"data.train {e['path']}: 모르는 칸 {sorted(unknown)} (path · format · count)")
        fmt = {"swift-fields": "swift"}.get(e.get("format", "tasks"), e.get("format", "tasks"))
        if fmt not in ("tasks", "swift"):
            raise ValueError(f"data.train {e['path']}: format 은 tasks · swift 중 하나입니다: {fmt}")
        if (fmt == "swift") != e["path"].endswith(".jsonl"):
            raise ValueError(f"data.train {e['path']}: ms-swift .jsonl 은 \"format\": \"swift\" 와 함께, 그 밖의 경로는 과제 폴더로 적습니다")
        out.append({"path": e["path"], **({"format": "swift"} if fmt == "swift" else {}),
                    **({"count": e["count"]} if e.get("count") is not None else {})})
    return out


def resolve(entries, base: Path):
    """설정 파일 기준 상대 경로 → 절대 경로 (평가 세트의 paths·scorer 파일, 학습 데이터의 path)."""
    def res(p):
        return str((base / p).resolve()) if p and not Path(p).is_absolute() else p

    out = []
    for e in entries if isinstance(entries, list) else [entries]:
        if isinstance(e, str):
            out.append(res(e))
            continue
        e = dict(e)
        if "paths" in e:
            e["paths"] = [res(p) for p in e["paths"]]
        if "path" in e:
            e["path"] = res(e["path"])
        if e.get("scorer"):
            path, colon, name = e["scorer"].partition(":")
            e["scorer"] = res(path) + colon + name
        out.append(e)
    return out
