"""벤치마크 한 개(id/name)는 여러 경로를 합산한다. group은 표시 분류다."""
import hashlib
from pathlib import Path
import re


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
        result.append({"id": ident, "name": name.strip(), "group": group.strip(), "paths": paths, "legacy": legacy})
    return result


def paths(spec):
    return [p for item in normalize(spec) for p in item["paths"]]
