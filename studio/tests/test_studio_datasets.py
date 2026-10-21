"""studio 데이터셋 등록부·채점 시험: 손으로 만든 작은 1부·docgen.bench 폴더로, 명령줄 채점 함수와 같은 숫자가 나오는지."""
import json

import pytest

from studio import datasets as DS


def _jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


@pytest.fixture()
def ocr_folder(tmp_path):
    root = tmp_path / "ocr_prepared"
    root.mkdir()
    (root / "DONE.json").write_text(json.dumps({"ocr_revision": "t1"}), encoding="utf-8")
    _jsonl(root / "pages.jsonl", [{"document_id": "d1", "page_id": "p1"}])
    rows = [
        {"id": "a", "task": "crop_ocr", "images": ["img.png"], "messages": [{"role": "user", "content": "<image>\n읽기"}],
         "target": json.dumps({"text": "홍길동"}, ensure_ascii=False)},
        {"id": "b", "task": "crop_ocr", "images": ["img.png"], "messages": [{"role": "user", "content": "<image>\n읽기"}],
         "target": json.dumps({"text": "1,000원"}, ensure_ascii=False)},
        {"id": "c", "task": "grounding", "images": ["img.png"], "messages": [{"role": "user", "content": "<image>\n찾기"}],
         "target": json.dumps({"boxes": [{"bbox_2d": [10, 10, 100, 40], "label": "성명"}]}, ensure_ascii=False)},
    ]
    _jsonl(root / "benchmark_tasks.jsonl", rows)
    return root, rows


@pytest.fixture()
def bench_folder(tmp_path):
    root = tmp_path / "bench"
    (root / "tasks").mkdir(parents=True)
    (root / "meta.json").write_text(json.dumps({"version": "1.2", "split": "test", "counts": {"classify": 2}}), encoding="utf-8")
    _jsonl(root / "tasks" / "classify.jsonl", [
        {"id": "classify/x", "task": "classify", "images": ["images/x.jpg"], "prompt": "서류명?", "answer": "재직증명서",
         "meta": {"group": "income", "condition": "clean"}},
        {"id": "classify/y", "task": "classify", "images": ["images/y.jpg"], "prompt": "서류명?", "answer": "주민등록등본",
         "meta": {"group": "family", "condition": "scan"}},
    ])
    return root


def test_detect_and_register(tmp_path, ocr_folder, bench_folder):
    root, _ = ocr_folder
    assert DS.detect(root) == "bank_ocr/prepared"
    assert DS.detect(bench_folder) == "docgen.bench"
    assert DS.detect(tmp_path) is None
    reg = DS.Registry(tmp_path / "ws")
    o = reg.register(str(root), "ocr")
    assert o["track"] == "ocr" and o["gt"] == "pseudo" and o["counts"]["benchmark_tasks"] == 3
    b = reg.register(str(bench_folder))
    assert b["track"] == "bank" and b["id"] == "bench"
    with pytest.raises(ValueError):
        reg.register(str(bench_folder))   # 같은 폴더 두 번
    with pytest.raises(ValueError):
        reg.register(str(tmp_path))       # 모르는 형식


def test_ocr_score_matches_cli(tmp_path, ocr_folder):
    from docgen.bench import ocr_metrics as OM

    root, rows = ocr_folder
    reg = DS.Registry(tmp_path / "ws")
    ds = reg.register(str(root))
    preds = {"a": "홍길동", "b": "1,000", "c": '[{"bbox_2d": [12, 10, 98, 42], "label": "성명"}]'}
    s = DS.score(ds, preds)
    cli = OM.evaluate(rows, preds)["tasks"]
    assert s["tasks"] == cli
    assert s["main"]["crop_ocr"]["metric"] == "cer" and s["answered"] == 3
    assert 0 < s["per_item"]["b"] < 1 and s["per_item"]["a"] == 1.0


def test_bank_score_and_prediction_folder(tmp_path, bench_folder):
    from docgen.bench import evaluate as E

    pred_dir = tmp_path / "preds" / "m1"
    _jsonl(pred_dir / "classify.jsonl", [{"id": "classify/x", "output": "재직증명서"}, {"id": "classify/y", "output": "가족관계증명서"}])
    reg = DS.Registry(tmp_path / "ws")
    ds = reg.register(str(bench_folder))
    reg.attach_run(ds["id"], str(pred_dir))
    ds = reg.get(ds["id"])
    preds = DS.predictions_of(ds)
    assert len(preds) == 1 and preds[0]["label"] == "m1"   # 예측 폴더 전체가 한 묶음
    loaded = DS.load_pred(preds[0]["path"])
    s = DS.score(ds, loaded)
    cli = E.score_task("classify", DS.items(ds)["classify"], loaded)
    assert s["tasks"]["classify"]["metrics"] == cli["metrics"]
    assert s["main"]["classify"]["value"] == 0.5


def test_pipeline_runs_folder(tmp_path, ocr_folder):
    root, _ = ocr_folder
    run = tmp_path / "runs" / "exp1"
    _jsonl(run / "predictions" / "base.jsonl", [{"id": "a", "prediction": "홍길동"}])
    _jsonl(run / "predictions" / "sft.jsonl", [{"id": "a", "prediction": "홍길동"}])
    reg = DS.Registry(tmp_path / "ws")
    ds = reg.register(str(root))
    reg.attach_run(ds["id"], str(run))
    labels = sorted(p["label"] for p in DS.predictions_of(reg.get(ds["id"])))
    assert labels == ["base", "sft"]   # 파이프라인 결과는 파일마다 한 묶음


def test_resolve_file_with_path_map(tmp_path, ocr_folder):
    root, _ = ocr_folder
    (root / "views").mkdir()
    (root / "views" / "v.png").write_bytes(b"x")
    reg = DS.Registry(tmp_path / "ws", {str(root.parent): "/share/train_side"})
    ds = reg.register(str(root))
    assert reg.resolve_file(ds, "/share/train_side/ocr_prepared/views/v.png") == root / "views" / "v.png"
    assert reg.resolve_file(ds, "/elsewhere/ocr_prepared/views/v.png") == root / "views" / "v.png"
    assert reg.allowed(ds, root / "views" / "v.png") and not reg.allowed(ds, tmp_path / "secret.txt")


def test_card_markdown(tmp_path, bench_folder):
    reg = DS.Registry(tmp_path / "ws")
    ds = reg.register(str(bench_folder), purpose="시험")
    reg.set_card(ds["id"], {"limits": "문항이 적다"})
    md = DS.card_markdown(reg.get(ds["id"]), [{"label": "m1", "main": {"classify": {"metric": "acc", "value": 0.5}}}],
                          [{"name": "t1", "pipeline": "2부", "created": "2026-10-20"}])
    assert "# bench" in md and "문항이 적다" in md and "50.0 (acc)" in md and "t1" in md
