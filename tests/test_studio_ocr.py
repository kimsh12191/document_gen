"""5단계 시험: 합성 OCR 정답 만들기(docgen/ocr_export.py), OCR 레시피, 1부 학습 설정. 브라우저 없이."""
import json
import random

import pytest

from docgen import ocr_export as X
from docgen import ocr_set
from studio import datasets as DS
from studio import ocr_data


def test_fields_items_matches_old_script_shape():
    lab = {"images": ["a.png"], "fields": [
        {"key": "x", "type": "text", "value": "홍길동", "bbox": [10, 10, 60, 30], "label": "성명", "label_bbox": [0, 10, 9, 30], "page": 0},
        {"key": "y", "type": "text", "value": "줄1\n줄2", "bbox": [10, 40, 60, 80], "page": 0},
        {"key": "s", "type": "seal", "value": "홍", "bbox": [1, 1, 5, 5], "page": 0}]}
    items = X.fields_items(lab, random.Random(0))[0]
    assert [i["text"] for i in items] == ["홍길동", "성명", "줄1", "줄2"]   # 칸마다 값 → 항목명 (도장은 뺌)
    assert items[2]["bounding"]["vertices"][2] == {"x": 60, "y": 60}
    doc = X.page_document(items, "a.png")
    assert doc["success"] == "Y" and doc["data"]["basicData"][0] == items


def test_page_items_words_lines_and_low_confidence():
    texts = [{"page": 0, "text": "성명", "kind": "text", "blk": 1, "bbox": [10, 10, 40, 30]},
             {"page": 0, "text": "홍길동", "kind": "text", "blk": 1, "bbox": [45, 11, 90, 30]},
             {"page": 0, "text": "견본", "kind": "watermark", "blk": 2, "bbox": [10, 100, 80, 140]},
             {"page": 0, "text": "주소", "kind": "text", "blk": 3, "bbox": [10, 50, 40, 70]}]
    bg = [{"text": "신청서", "bbox": [100, 2, 130, 8], "line": "pdf:0:0"}]
    words = X.page_items(texts, bg, 2.0, "word")
    assert [w["text"] for w in words] == ["신청서", "성명", "홍길동", "주소", "견본"]   # 위에서 아래, 왼쪽에서 오른쪽
    by = {w["text"]: w for w in words}
    assert by["성명"]["line_num"] == by["홍길동"]["line_num"] != by["주소"]["line_num"]
    assert by["견본"]["confidence"] == X.LOW_CONF and by["성명"]["confidence"] == X.TEXT_CONF
    assert by["신청서"]["bounding"]["vertices"][0] == {"x": 200, "y": 4}   # pt × 2
    lines = X.page_items(texts, [], 1.0, "line")
    assert "성명 홍길동" in [x["text"] for x in lines]


def test_bank_ocr_parses_export():
    """1부 parse_ocr 가 기본 mapping 으로 그대로 읽는다."""
    from bank_ocr.data import parse_ocr

    cfg = json.load(open(ocr_data.ROOT / "training" / "config.example.json", encoding="utf-8"))
    doc = X.page_document(X.page_items([{"page": 0, "text": "가나", "kind": "text", "blk": 0, "bbox": [10, 10, 50, 30]}], [], 1, "word"), "p.png")
    words = parse_ocr(doc, 200, 100, cfg["mapping"])
    assert words[0]["text"] == "가나" and words[0]["bbox_norm"] == [50, 100, 250, 300]


def test_pick_condition_and_select_ids():
    conds = {"clean": 0.5, "scan": 0.5}
    assert ocr_set.pick("a:1", conds) == ocr_set.pick("a:1", conds)
    assert ocr_set.select_ids({"types": ["resident_id_card", "hf169"], "exclude": ["hf169"]}) == ["resident_id_card"]
    with pytest.raises(SystemExit):
        ocr_set.select_ids({"types": ["no_such_form"]})


def test_ocr_recipe_validate():
    ocr_data.validate(ocr_data.TEMPLATES["ocr-try"])
    for bad in ({"track": "ocr", "split": "test"}, {"track": "ocr", "unit": "char"}, {"track": "ocr", "bundles": 3},
                {"track": "ocr", "conditions": {"clean": 0.3}}):
        with pytest.raises(ValueError):
            ocr_data.validate(bad)


def _ocr_ds(tmp_path, name, train_tasks):
    root = tmp_path / name
    root.mkdir()
    (root / "DONE.json").write_text("{}", encoding="utf-8")
    (root / "pages.jsonl").write_text('{"document_id": "d", "page_id": "p"}\n', encoding="utf-8")
    (root / "config.snapshot.json").write_text(json.dumps({"ocr_revision": "r1", "image_max_size": [2300, 1600], "studio": {"gt": "exact"}}),
                                               encoding="utf-8")
    if train_tasks:
        (root / "train_tasks.jsonl").write_text('{"id": "t"}\n', encoding="utf-8")
    (root / "benchmark_tasks.jsonl").write_text('{"id": "b", "task": "crop_ocr", "target": "{}"}\n', encoding="utf-8")
    return root


def test_ocr_training_config(tmp_path):
    reg = DS.Registry(tmp_path / "ws", {str(tmp_path): "/share/x"})
    a = reg.register(str(_ocr_ds(tmp_path, "syn", True)))
    b = reg.register(str(_ocr_ds(tmp_path, "evalonly", False)))
    assert a["gt"] == "exact"
    with pytest.raises(ValueError):
        ocr_data.ocr_training_config(reg, [b["id"]], b["id"], "t")   # 학습 문항 없음
    info = ocr_data.ocr_training_config(reg, [a["id"]], a["id"], "ocr exp")
    data = info["extra_files"]["configs/studio-ocr-exp-data.json"]
    assert data["output_dir"] == "/share/x/syn" and "studio" not in data
    assert info["config"] == {"workdir": "../runs/ocr-exp", "data_config": "studio-ocr-exp-data.json"}
    assert info["command"].endswith("--config configs/studio-ocr-exp.json")
