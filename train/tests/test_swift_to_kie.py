"""swift 추출 데이터의 질문·답을 합성 kie 꼴로 (train/swift_to_kie.py), 고친 파일도 swift-fields 평가로 읽기."""
import contextlib
import io
import json

import pytest
from PIL import Image

from docgen.bench import evaluate as E
from docgen.bench.ocr_data import read_jsonl, write_jsonl
from docgen.bench.runner import oracle_output
from train import swift_to_kie as K
from train.swift_import import load_swift

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
        K.main([str(tmp_path / "eval_qa_PO.jsonl"), "--out", str(tmp_path / "eval_qa_PO_kie.jsonl"), "--labels", str(tmp_path / "labels.json")])
    assert "1줄 건너뜀" in log.getvalue()
    (rec,) = read_jsonl(tmp_path / "eval_qa_PO_kie.jsonl")
    user, assistant = rec["messages"]
    assert rec["images"] == [str(tmp_path / "a.png")] and user["content"].startswith("<image>이 문서에서")
    assert "- NEGO_CLCT: 매입추심구분\n- DATE: -" in user["content"] and "- DATE#2: -" in user["content"] and "bbox_2d" not in user["content"]
    ans = json.loads(assistant["content"])
    assert ans[3] == {"key": "TENOR", "value": None} and ans[4] == {"key": "DATE#2", "value": "2025 06 01"}
    # 고친 파일도 지금처럼 swift-fields 로 평가: 정답 꼴로 답하면 만점, 주 지표는 값 점수
    _, (it,) = load_swift(tmp_path / "eval_qa_PO_kie.jsonl")
    assert E.reward("kie", oracle_output(it), it) == 1.0 and E.reward("kie", assistant["content"], it) == 1.0
    r = E.s_kie(it, json.dumps([{"key": "NEGO_CLCT", "value": "EOA"}, {"key": "DATE", "value": "2025.05.21"}]))["metrics"]
    assert "vl_f1" not in r and E.main_metric("kie", r) == "f1" and 0 < r["f1"] < 1
    with pytest.raises(SystemExit, match="이미 있습니다"):
        K.main([str(tmp_path / "eval_qa_PO.jsonl"), "--out", str(tmp_path / "eval_qa_PO_kie.jsonl")])
