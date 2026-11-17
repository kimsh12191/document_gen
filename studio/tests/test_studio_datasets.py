"""studio 데이터셋 등록부·채점 시험: 손으로 만든 작은 OCR 준비(옛 형식)·docgen.bench 폴더로, 명령줄 채점 함수와 같은 숫자가 나오는지.
과제 형식은 하나(docgen-tasks)이고, tasks/ 가 없는 옛 OCR 준비 폴더는 등록할 때 tasks/ 를 만든다 (archive/studio/DESIGN.md 17절)."""
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
    assert DS.detect(root) is None and DS.legacy_ocr(root)
    assert DS.detect(bench_folder) == DS.FORMAT
    assert DS.detect(tmp_path) is None
    reg = DS.Registry(tmp_path / "ws")
    o = reg.register(str(root), "ocr")
    assert o["format"] == DS.FORMAT and o["groups"] == ["ocr"] and o["gt"] == "pseudo"
    assert o["counts"]["benchmark_items"] == 3 and o["counts"]["crop_ocr"] == 2
    b = reg.register(str(bench_folder))
    assert b["groups"] == ["doc"] and b["id"] == "bench"
    with pytest.raises(ValueError):
        reg.register(str(bench_folder))   # 같은 폴더 두 번
    with pytest.raises(ValueError):
        reg.register(str(tmp_path))       # 모르는 형식


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
    md = DS.card_markdown(reg.get(ds["id"]))
    assert "# bench" in md and "문항이 적다" in md
