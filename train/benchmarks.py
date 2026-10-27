"""벤치마크 한 개(id/name)는 여러 경로를 합산한다. group은 표시 분류다.
format: "tasks"(기본, studio 과제 폴더) | "swift-fields"(실서류 swift .jsonl, train/swift_import.py).
gt: 정답 출처 "exact"·"reviewed"·"pseudo" (폴더의 meta.json 보다 우선).
scorer: 이 평가 세트만 다르게 채점할 때 "<파일.py>:<함수>" (설정 파일 기준 상대 경로, 함수를 빼면 score). 견본 train/scorers/.
  swift-fields 세트는 늘 채점 함수로 채점하고, 적지 않으면 train/scorers/swift_default.py.
학습 데이터(data.train)도 같은 format·scorer 를 받는다 (train_entries)."""
import hashlib
from pathlib import Path
import re

FORMATS = ("tasks", "swift-fields")
GTS = ("exact", "reviewed", "pseudo")
SWIFT_DEFAULT = str(Path(__file__).resolve().parent / "scorers" / "swift_default.py") + ":score"


def normalize(spec):
    entries = spec if isinstance(spec, list) else [spec]
    result, ids, paths_seen = [], set(), set()
    for entry in entries:
        legacy = isinstance(entry, str) or (isinstance(entry, dict) and "id" not in entry and "paths" not in entry)
        value = {"path": entry} if isinstance(entry, str) else entry
        if not isinstance(value, dict) or ("path" in value and "paths" in value):
            raise ValueError("benchmark: path 또는 paths 중 하나를 지정하세요")
        paths = value.get("paths", [value["path"]] if "path" in value else [])
        if not isinstance(paths, list) or not paths or any(not isinstance(p, str) or not p.strip() for p in paths):
            raise ValueError("benchmark.paths는 비어 있지 않은 경로 목록이어야 합니다")
        if not legacy and not value.get("id"):
            raise ValueError("benchmark.paths를 사용할 때는 id가 필요합니다")
        ident = value.get("id") or "legacy-" + hashlib.sha256(str(Path(paths[0]).resolve()).encode()).hexdigest()[:12]
        if not isinstance(ident, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", ident) or ident in ids:
            raise ValueError(f"benchmark.id는 중복 없는 영문·숫자·점·밑줄·하이픈이어야 합니다: {ident}")
        ids.add(ident)
        for p in paths:
            key = str(Path(p).resolve())
            if key in paths_seen:
                raise ValueError(f"평가 경로를 중복 선택했습니다: {p}")
            paths_seen.add(key)
        name, group = value.get("name", ident), value.get("group", "ungrouped")
        if any(not isinstance(v, str) or not v.strip() for v in (name, group)):
            raise ValueError("benchmark.name과 group은 비어 있지 않은 문자열이어야 합니다")
        fmt, gt = value.get("format", "tasks"), value.get("gt")
        if fmt not in FORMATS:
            raise ValueError(f"benchmark.format은 {', '.join(FORMATS)} 중 하나입니다: {fmt}")
        if gt is not None and gt not in GTS:
            raise ValueError(f"benchmark.gt는 {', '.join(GTS)} 중 하나입니다: {gt}")
        for p in paths:
            if (fmt == "swift-fields") != p.endswith(".jsonl"):
                raise ValueError(f"{p}: swift .jsonl 은 \"format\": \"swift-fields\" 와 함께, 그 밖의 경로는 과제 폴더로 적습니다")
        scorer = _scorer(value.get("scorer"), fmt, f"benchmark {ident}")
        result.append({"id": ident, "name": name.strip(), "group": group.strip(), "paths": paths, "legacy": legacy,
                       **({"format": fmt} if fmt != "tasks" else {}), **({"gt": gt} if gt else {}),
                       **({"scorer": scorer} if scorer else {})})
    return result


def _scorer(scorer, fmt, where):
    if scorer is None and fmt == "swift-fields":   # swift 는 늘 채점 함수로 (정답 글을 그대로 넘김)
        scorer = SWIFT_DEFAULT
    if scorer is not None:
        if not isinstance(scorer, str) or not scorer.partition(":")[0].endswith(".py"):
            raise ValueError(f"{where}: scorer 는 \"<파일.py>:<함수>\" 입니다: {scorer}")
        from docgen.bench.evaluate import load_scorer

        load_scorer(scorer)   # 파일·함수가 있는지 돌리기 전에
    return scorer


def train_entries(spec) -> list[dict]:
    """data.train 칸 → [{"path", "format"?, "scorer"?, "count"?}]. 경로만 적으면 studio 과제 폴더 (예전 그대로).
    swift .jsonl 은 "format": "swift-fields" 와 함께 — 채점 함수(scorer, 없으면 swift_default)가 깨진 줄을 거르고 GRPO 보상을 낸다."""
    out = []
    for e in spec if isinstance(spec, list) else [spec]:
        e = dict(e) if isinstance(e, dict) else {"path": e}
        if not isinstance(e.get("path"), str) or not e["path"].strip():
            raise ValueError(f"data.train: 경로(path)가 없습니다: {e}")
        fmt = e.get("format", "tasks")
        if fmt not in FORMATS:
            raise ValueError(f"data.train.format은 {', '.join(FORMATS)} 중 하나입니다: {fmt}")
        if (fmt == "swift-fields") != e["path"].endswith(".jsonl"):
            raise ValueError(f"{e['path']}: swift .jsonl 은 \"format\": \"swift-fields\" 와 함께, 그 밖의 경로는 과제 폴더로 적습니다")
        if fmt == "tasks" and e.get("scorer") is not None:
            raise ValueError(f"data.train {e['path']}: scorer 는 swift .jsonl 학습 데이터에만 붙입니다")
        scorer = _scorer(e.get("scorer"), fmt, f"data.train {e['path']}")
        out.append({**{k: v for k, v in e.items() if k not in ("format", "scorer")},
                    **({"format": fmt} if fmt != "tasks" else {}), **({"scorer": scorer} if scorer else {})})
    return out


def paths(spec):
    return [p for item in normalize(spec) for p in item["paths"]]
