"""학습 앞단 OCR (파이프라인 ocr 단계): 그림 폴더 → 사내 OCR → OCR 준비(docgen.bench.ocr_prepare) → 과제 폴더.
그 폴더는 data.train(count 만큼)·data.benchmark(떼어 둔 평가 문서)에 저절로 들어간다 (resolve_data).

설정 (파이프라인 설정의 data.ocr_images)
  folders      그림 폴더 [경로 또는 {"path", "split": "train"(기본)|"benchmark", "ocr_dir": 이미 돌린 OCR JSON 폴더}].
               하위 폴더까지 png·jpg·tif 를 읽는다. 모두 benchmark 면 평가 전용
  documents    문서 나누기: "folder"(기본, 같은 하위 폴더의 그림이 한 문서, 최상위 그림은 하나씩) · "page"(그림 하나가 한 문서)
               · 정규식 ((?P<document_id>…) 를 상대 경로에). 같은 문서의 쪽은 학습·평가에 갈라지지 않는다
  ocr          {"callable", "revision", "base_url"} — 사내 OCR 함수(기본 studio.internal_ocr_adapter:ocr_from_file)·버전(캐시 열쇠)·주소
               (INTERNAL_OCR_BASE_URL). ocr_dir 로 모든 그림의 OCR 이 있으면 없어도 된다
  count        학습에 쓸 OCR SFT 문항 수 (없으면 task_mix·sft_max_examples 규칙대로)
  benchmark    false 면 평가에 넣지 않는다 (기본 true: 떼어 둔 문서로 OCR 8과제 평가)
  output_dir   준비 폴더 (기본 <data.output_dir>-ocr)
  cache_dir    그림·OCR 캐시 (기본 data.output_dir 옆 ocr-cache, 실험끼리 같이 써서 OCR 을 다시 부르지 않는다)
  prepare      OCR 준비 설정 덮어쓰기 (docgen/bench/ocr_config.example.json 의 val_fraction·benchmark_fraction·views·tasks_per_view·filters 등)
"""
import os
from pathlib import Path

from docgen.bench.ocr_data import read_json, scan, write_json, write_jsonl

EXAMPLE = Path(__file__).resolve().parents[1] / "docgen" / "bench" / "ocr_config.example.json"
DEFAULT_CALLABLE = "studio.internal_ocr_adapter:ocr_from_file"


def resolve(spec: dict, data_output: str, res) -> dict:
    """경로를 설정 파일 기준으로 풀고 기본값을 채운다."""
    if not isinstance(spec, dict) or not spec.get("folders"):
        raise ValueError("data.ocr_images.folders 에 그림 폴더를 적으세요")
    folders = []
    for f in spec["folders"] if isinstance(spec["folders"], list) else [spec["folders"]]:
        f = dict(f) if isinstance(f, dict) else {"path": f}
        f["path"] = res(f["path"])
        f["split"] = f.get("split", "train")
        if f["split"] not in ("train", "benchmark"):
            raise ValueError(f"data.ocr_images.folders: split 은 train·benchmark ({f['path']})")
        if f.get("ocr_dir"):
            f["ocr_dir"] = res(f["ocr_dir"])
        folders.append(f)
    out = Path(data_output)
    return {**spec, "folders": folders, "documents": spec.get("documents", "folder"),
            "output_dir": res(spec.get("output_dir")) or str(out.parent / f"{out.name}-ocr"),
            "cache_dir": res(spec.get("cache_dir")) or str(out.parent / "ocr-cache")}


def entries(spec: dict) -> tuple[dict | None, str | None]:
    """준비 폴더를 학습·평가 목록의 무엇으로 넣는지."""
    out = spec["output_dir"]
    only_eval = all(f["split"] == "benchmark" for f in spec["folders"])
    train = None if only_eval else {"path": out, **({"count": spec["count"]} if spec.get("count") is not None else {})}
    return train, (out if spec.get("benchmark", True) else None)


def build(spec: dict) -> dict:
    """그림 폴더 읽기 → manifest·OCR 준비 설정 → 준비 (OCR 은 캐시에 없는 그림만 부른다)."""
    from docgen.bench.ocr_prepare import prepare

    out = Path(spec["output_dir"])
    if (out / "DONE.json").exists():
        return read_json(out / "DONE.json")
    work = out.parent / f"{out.name}.inputs"   # manifest·설정 (준비 폴더는 비어 있어야 해서 옆에)
    docs = spec["documents"]
    rows = []
    for i, f in enumerate(spec["folders"]):
        for r in scan(f["path"], f["split"], None if docs in ("folder", "page") else docs, docs == "page",
                      f.get("ocr_dir"), docs == "folder"):
            if len(spec["folders"]) > 1:   # 폴더마다 같은 상대 경로가 있어도 다른 문서·쪽으로
                r["document_id"], r["page_id"] = f"{i}:{r['document_id']}", f"{i}:{r['page_id']}"
            rows.append(r)
    ocr = spec.get("ocr") or {}
    if any("ocr_json" not in r for r in rows) and not ocr.get("revision"):
        raise ValueError("data.ocr_images.ocr.revision 을 적으세요 (사내 OCR 버전, 캐시 열쇠). OCR 을 이미 돌렸으면 folders 의 ocr_dir")
    if ocr.get("base_url"):
        os.environ["INTERNAL_OCR_BASE_URL"] = ocr["base_url"]
    cfg = read_json(EXAMPLE)
    cfg.update({"manifest": str((work / "manifest.jsonl").resolve()), "output_dir": str(out.resolve()),
                "cache_dir": str(Path(spec["cache_dir"]).resolve()), "ocr_callable": ocr.get("callable") or DEFAULT_CALLABLE,
                "ocr_revision": ocr.get("revision") or "saved-ocr"})
    if ocr.get("mapping"):
        cfg["mapping"] = ocr["mapping"]
    cfg.update(spec.get("prepare") or {})
    if all(f["split"] == "benchmark" for f in spec["folders"]):
        cfg["benchmark_only"] = True
    cfg["studio"] = {"source": "train.ocr_images", "folders": [f["path"] for f in spec["folders"]], "documents": docs}
    write_jsonl(work / "manifest.jsonl", rows)
    write_json(work / "config.json", cfg)
    print(f"OCR 준비: 그림 {len(rows)}장, 문서 {len({r['document_id'] for r in rows})}개 → {out}", flush=True)
    return prepare(str(work / "config.json"))
