"""평가 세트마다 채점 함수 (data.benchmark[].scorer), 견본 train/scorers/kie_default.py."""
import json
from pathlib import Path

import pytest

from docgen.bench import evaluate as E
from train.benchmarks import normalize
from train.cli import resolve_data
from train.score import score

SAMPLE = str(Path(__file__).resolve().parents[1] / "scorers" / "kie_default.py")
SWIFT = {"id": "po/00001", "task": "kie", "answer": {"NEGO_CLCT": "EOA", "DATE": "2025 05 21", "TENOR": ""}, "meta": {},
         "eval": {"order": ["NEGO_CLCT", "DATE", "TENOR"], "fields": {k: {"type": "text"} for k in ("NEGO_CLCT", "DATE", "TENOR")}}}
LISTED = {**SWIFT, "id": "po/00002", "answer": [{"key": "NEGO_CLCT", "value": "EOA"}, {"key": "DATE", "value": "2025 05 21"},
                                                {"key": "TENOR", "value": None}], "eval": {"fields": SWIFT["eval"]["fields"]}}
OUTPUTS = ['["EOA", "2025 05 21", ""]', '["EOA", "2025-05-21", ""]', '["X", "2025 05 21", "1"]', '["EOA"]', "모름",
           '[{"key": "NEGO_CLCT", "value": "EOA"}, {"key": "DATE", "value": "2025 05 21"}]',
           '[{"key": "NEGO_CLCT", "value": "eoa"}, {"key": "TENOR", "value": "90 DAYS"}]', '{"NEGO_CLCT": "EOA"}']


def test_sample_is_studio_default():
    """견본 = studio 기본 kie 값 점수 (FIELD_TYPES 를 비우면)."""
    fn = E.load_scorer(SAMPLE)
    for it in (SWIFT, LISTED):
        for out in OUTPUTS:
            mine, base = fn(it, out), E.SCORERS["kie"](it, out)
            if base["parse_fail"] and not mine.get("parse_fail"):   # 견본은 질문 꼴과 다른 답 꼴도 읽는다 (그 밖은 같음)
                continue
            assert bool(mine.get("parse_fail")) == bool(base["parse_fail"]), (it["id"], out)
            if not base["parse_fail"]:
                assert {k: mine["metrics"][k] for k in ("f1", "field_acc", "doc_exact")} == \
                       {k: base["metrics"][k] for k in ("f1", "field_acc", "doc_exact")}, (it["id"], out)


def test_benchmark_scorer_used_and_main(tmp_path):
    (tmp_path / "loose.py").write_text(
        "def score(item, output):\n"
        "    hit = sum(str(v) in output for v in item['answer'].values() if v)\n"
        "    return {'metrics': {'hit': hit / 2}, 'main': 'hit'}\n", encoding="utf-8")
    items = [{**SWIFT, "eval": {**SWIFT["eval"], "scorer": str(tmp_path / "loose.py")}}]
    res = score(items, {"po/00001": "<think>\n\n</think>\n\nEOA 2025 05 21"})
    assert res["tasks"]["kie"]["main"] == "hit" and res["tasks"]["kie"]["metrics"]["hit"] == 1.0
    assert score(items, {})["tasks"]["kie"]["metrics"]["hit"] == 0.0   # 답 없음 = 0 (함수에는 "" 로)
    # 설정: 상대 경로는 설정 파일 기준, 없는 파일·함수는 돌리기 전에
    data = resolve_data({"data": {"train": [], "output_dir": "o", "benchmark": [
        {"id": "po", "paths": ["po.jsonl"], "format": "swift-fields", "scorer": "loose.py:score"}]}}, tmp_path)
    (b,) = normalize(data["benchmark"])
    assert b["scorer"] == f"{tmp_path / 'loose.py'}:score"
    with pytest.raises(ValueError, match="함수 nope"):
        normalize([{**data["benchmark"][0], "scorer": f"{tmp_path / 'loose.py'}:nope"}])
    with pytest.raises(ValueError, match="파일이 없습니다"):
        normalize([{**data["benchmark"][0], "scorer": str(tmp_path / "none.py")}])
    # 함수가 깨지면 어느 문항인지
    (tmp_path / "bad.py").write_text("def score(item, output):\n    return 1 / 0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="po/00001"):
        score([{**SWIFT, "eval": {**SWIFT["eval"], "scorer": str(tmp_path / "bad.py")}}], {"po/00001": "x"})


def test_sample_field_types(tmp_path):
    """견본을 복사해 FIELD_TYPES 만 바꾸면 날짜 표기 차이를 맞게 본다."""
    src = Path(SAMPLE).read_text(encoding="utf-8").replace("FIELD_TYPES: dict[str, str] = {}", 'FIELD_TYPES = {"DATE": "date"}')
    (tmp_path / "po.py").write_text(src, encoding="utf-8")
    out = '["EOA", "2025.5.21", ""]'
    assert E.load_scorer(str(tmp_path / "po.py"))(SWIFT, out)["metrics"]["f1"] == 1.0
    assert E.SCORERS["kie"](SWIFT, out)["metrics"]["f1"] < 1.0
    json.dumps(E.load_scorer(SAMPLE)(SWIFT, out))   # 결과는 JSON 으로 쓸 수 있어야 (보고서)
