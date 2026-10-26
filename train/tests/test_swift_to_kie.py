"""swift 추출 데이터 → 값만 묻는 kie 과제 폴더 (train/swift_to_kie.py)."""
import contextlib
import io
import json

from PIL import Image

from docgen.bench import evaluate as E
from docgen.bench.ocr_data import read_jsonl, write_jsonl
from docgen.bench.runner import oracle_output
from train import swift_to_kie as K
from train.mix import load_folder

FIELDS = ["NEGO_CLCT", "DATE", "AMT_VALUE", "TENOR", "DATE"]


def test_convert_and_score(tmp_path):
    Image.new("RGB", (40, 60), "white").save(tmp_path / "a.png")
    q = "<image>\nWhat are the values of the following fields in this document, in order: " + json.dumps(FIELDS) + "\nReturn only …"
    write_jsonl(tmp_path / "eval_qa_PO.jsonl", [
        {"messages": [{"role": "user", "content": q},
                      {"role": "assistant", "content": json.dumps(["EOA", "2025 05 21", "58,546.70", "", "2025 06 01"])}],
         "images": [str(tmp_path / "a.png")]},
        {"messages": [{"role": "user", "content": "깨진 줄"}], "images": []}])
    (tmp_path / "labels.json").write_text(json.dumps({"NEGO_CLCT": "매입추심구분"}), encoding="utf-8")
    with contextlib.redirect_stdout(io.StringIO()) as log:
        K.main([str(tmp_path / "eval_qa_PO.jsonl"), "--out", str(tmp_path / "po"), "--labels", str(tmp_path / "labels.json")])
    assert "1줄 건너뜀" in log.getvalue()
    (it,) = read_jsonl(tmp_path / "po" / "tasks" / "kie.jsonl")
    assert "- NEGO_CLCT: 매입추심구분\n- DATE: -" in it["prompt"] and "- DATE#2: -" in it["prompt"] and "bbox_2d" not in it["prompt"]
    assert it["answer"][3] == {"key": "TENOR", "value": None} and it["answer"][4] == {"key": "DATE#2", "value": "2025 06 01"}
    _, (loaded,) = load_folder(tmp_path / "po")
    assert loaded["meta"]["split"] == "test"
    # 정답 꼴로 답하면 만점, 주 지표는 값 점수 (위치 점수 없음)
    assert E.reward("kie", oracle_output(it), it) == 1.0
    r = E.s_kie(it, json.dumps([{"key": "NEGO_CLCT", "value": "EOA"}, {"key": "DATE", "value": "2025.05.21"}]))["metrics"]
    assert "vl_f1" not in r and E.main_metric("kie", r) == "f1" and 0 < r["f1"] < 1
