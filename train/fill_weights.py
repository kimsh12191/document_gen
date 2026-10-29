"""합친 모델에 빠진 가중치를 출발 모델에서 채운다 (예: Qwen3.5 의 MTP 머리 mtp.*).

ms-swift 는 transformers 로 모델을 읽어 학습·합치기(swift export --merge_lora)를 하므로, transformers 모델 구조에 없는 가중치는
읽을 때 버려지고 합친 폴더에도 저장되지 않는다. 그 부분은 학습되지 않았으니 출발 모델 것을 그대로 붙이면 된다.
붙인 가중치가 MTP 처럼 추측용이면 답은 바뀌지 않는다 (vLLM 이 본 모델로 검사), 빨라지는 정도만 출발 모델 기준.

  python -m train.fill_weights <출발 모델> <합친 폴더>                    무엇이 빠졌는지만 본다
  python -m train.fill_weights <출발 모델> <합친 폴더> --out <새 폴더>     새 폴더에 채운다 (합친 폴더 파일은 링크, 원본은 그대로)
  python -m train.fill_weights <출발 모델> <합친 폴더> --in-place          합친 폴더에 바로 (학습 실행이 막 만든 폴더에만)

채우는 조건: 출발 모델에만 있는 가중치 이름. 합친 모델에만 있는 이름이 하나라도 있으면 이름 규칙이 바뀐 것일 수 있어
(같은 가중치가 두 번 들어갈 위험) 채우지 않고 보고한다. 그래도 채울 묶음은 --prefix mtp 처럼 직접 고른다.
config.json 은 출발 모델에만 있는 칸을 더한다 (있는 칸은 바꾸지 않음). 가중치를 채웠을 때만.
가중치는 safetensors 파일에서 바이트 그대로 옮긴다 (torch 없이, dtype 그대로). 채운 것은 filled_from_base.json 에 남긴다.
"""
from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path

INDEX = "model.safetensors.index.json"
SINGLE = "model.safetensors"
FILLED = "model-filled-from-base.safetensors"
RECORD = "filled_from_base.json"


def _header(path: Path) -> tuple[dict, int]:
    """safetensors 머리 (이름 → dtype·shape·data_offsets) 와 데이터 시작 위치."""
    with path.open("rb") as f:
        n = struct.unpack("<Q", f.read(8))[0]
        head = json.loads(f.read(n))
    head.pop("__metadata__", None)
    return head, 8 + n


def weight_map(model: Path) -> dict[str, str]:
    """가중치 이름 → 파일 이름. index 가 없으면 model.safetensors 하나."""
    idx = model / INDEX
    if idx.exists():
        return json.loads(idx.read_text(encoding="utf-8"))["weight_map"]
    if (model / SINGLE).exists():
        return {k: SINGLE for k in _header(model / SINGLE)[0]}
    raise ValueError(f"{model} 에 {INDEX} 도 {SINGLE} 도 없습니다")


def _groups(keys) -> dict[str, list[str]]:
    """보고용 묶음: 이름의 첫 마디 (mtp.layers.0… → mtp)."""
    out: dict[str, list[str]] = {}
    for k in sorted(keys):
        out.setdefault(k.split(".", 1)[0], []).append(k)
    return out


def _missing_config(base: dict, merged: dict, path: str = "") -> dict:
    """출발 모델 config 에만 있는 칸 (점 경로 → 값). 양쪽 다 있는 칸은 값이 달라도 건드리지 않는다."""
    out = {}
    for k, v in base.items():
        if k not in merged:
            out[path + k] = v
        elif isinstance(v, dict) and isinstance(merged[k], dict):
            out |= _missing_config(v, merged[k], path + k + ".")
    return out


def plan(base: Path, merged: Path, prefixes: list[str] | None = None) -> dict:
    """{"fill": [이름], "missing": {묶음: 개수}, "extra": {묶음: 개수}, "config": {칸: 값}, "blocked": 이유?}"""
    b, m = weight_map(base), weight_map(merged)
    missing = sorted(set(b) - set(m))
    extra = sorted(set(m) - set(b))
    out = {"missing": {g: len(v) for g, v in _groups(missing).items()}, "extra": {g: len(v) for g, v in _groups(extra).items()}}
    if prefixes:
        fill = [k for k in missing if any(k == p or k.startswith(p + ".") for p in prefixes)]
    elif extra:
        fill = []
        out["blocked"] = ("합친 모델에만 있는 가중치 이름이 있어 이름 규칙이 바뀐 것일 수 있습니다. 채우지 않습니다. "
                          "빠진 묶음이 확실히 따로 떨어진 부분(예: mtp)이면 --prefix 로 고르세요.")
    else:
        fill = missing
    out["fill"] = fill
    bc = json.loads((base / "config.json").read_text(encoding="utf-8")) if (base / "config.json").exists() else {}
    mc = json.loads((merged / "config.json").read_text(encoding="utf-8")) if (merged / "config.json").exists() else {}
    out["config"] = _missing_config(bc, mc) if fill else {}
    return out


def _write_tensors(base: Path, bmap: dict[str, str], names: list[str], dst: Path) -> int:
    """출발 모델의 그 가중치들을 바이트 그대로 새 safetensors 하나로. 쓴 데이터 바이트 수."""
    head, parts, offset = {}, [], 0
    by_file: dict[str, list[str]] = {}
    for k in names:
        by_file.setdefault(bmap[k], []).append(k)
    for fname, keys in sorted(by_file.items()):
        h, start = _header(base / fname)
        with (base / fname).open("rb") as f:
            for k in keys:
                a, z = h[k]["data_offsets"]
                f.seek(start + a)
                data = f.read(z - a)
                head[k] = {"dtype": h[k]["dtype"], "shape": h[k]["shape"], "data_offsets": [offset, offset + len(data)]}
                parts.append(data)
                offset += len(data)
    raw = json.dumps({"__metadata__": {"format": "pt"}, **head}, separators=(",", ":")).encode()
    raw += b" " * (-len(raw) % 8)
    tmp = dst.with_suffix(".tmp")
    with tmp.open("wb") as f:
        f.write(struct.pack("<Q", len(raw)) + raw)
        for p in parts:
            f.write(p)
    tmp.replace(dst)
    return offset


def _set_path(d: dict, dotted: str, value) -> None:
    *up, last = dotted.split(".")
    for k in up:
        d = d.setdefault(k, {})
    d[last] = value


def fill(base: str | Path, merged: str | Path, out: str | Path | None = None, in_place: bool = False,
         prefixes: list[str] | None = None) -> dict:
    """채운다. out 이면 새 폴더 (합친 폴더 파일은 링크), in_place 면 합친 폴더에. 둘 다 아니면 plan 만."""
    base, merged = Path(base), Path(merged)
    p = plan(base, merged, prefixes)
    result = {"base": str(base), "merged": str(merged), **{k: v for k, v in p.items() if k != "fill"}, "filled": len(p["fill"])}
    if not (out or in_place) or not p["fill"]:
        return result | {"written": None}
    if out and in_place:
        raise ValueError("--out 과 --in-place 는 하나만")
    target = merged
    if out:
        target = Path(out)
        target.mkdir(parents=True)   # 있으면 멈춤 (덮어쓰지 않음)
        for f in merged.iterdir():
            (target / f.name).symlink_to(f.resolve())
    if (target / FILLED).exists():
        raise ValueError(f"{target / FILLED} 가 이미 있습니다")
    size = _write_tensors(base, weight_map(base), p["fill"], target / FILLED)
    mmap = weight_map(merged)
    idx = json.loads((merged / INDEX).read_text(encoding="utf-8")) if (merged / INDEX).exists() else \
        {"metadata": {"total_size": sum(_size(merged / f) for f in set(mmap.values()))}, "weight_map": mmap}
    idx["weight_map"] = {**idx["weight_map"], **{k: FILLED for k in p["fill"]}}
    idx.setdefault("metadata", {})["total_size"] = int(idx["metadata"].get("total_size") or 0) + size
    _write_json(target / INDEX, idx)
    if p["config"]:
        cfg = json.loads((merged / "config.json").read_text(encoding="utf-8"))
        for k, v in p["config"].items():
            _set_path(cfg, k, v)
        _write_json(target / "config.json", cfg)
    _write_json(target / RECORD, {"base": str(base), "merged": str(merged), "file": FILLED, "groups": p["missing"] if not prefixes else
                                  {g: len(v) for g, v in _groups(p["fill"]).items()}, "keys": p["fill"], "config": p["config"]})
    return result | {"written": str(target)}


def _size(p: Path) -> int:
    h, start = _header(p)
    return max((v["data_offsets"][1] for v in h.values()), default=0)


def _write_json(p: Path, obj) -> None:
    """링크면 링크만 지우고 새 파일로 (링크 너머 원본은 그대로)."""
    if p.is_symlink():
        p.unlink()
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m train.fill_weights", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base", help="출발 모델 폴더")
    ap.add_argument("merged", help="합친 모델 폴더 (swift export --merge_lora 결과)")
    ap.add_argument("--out", help="채운 새 폴더 (없어야 함)")
    ap.add_argument("--in-place", action="store_true", help="합친 폴더에 바로 쓴다")
    ap.add_argument("--prefix", action="append", help="이 이름으로 시작하는 빠진 가중치만 채운다 (여러 번)")
    a = ap.parse_args(argv)
    try:
        r = fill(a.base, a.merged, a.out, a.in_place, a.prefix)
    except (ValueError, OSError) as exc:
        sys.exit(f"fill_weights: {exc}")
    print(json.dumps(r, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
