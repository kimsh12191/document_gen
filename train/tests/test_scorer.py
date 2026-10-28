"""평가 세트마다 채점 함수 (data.benchmark[].scorer), 견본 train/scorers/kie_default.py."""
import json
from pathlib import Path

import pytest

from docgen.bench import evaluate as E
from train.benchmarks import normalize
from train.cli import resolve_data
from train.score import score
from train.tests.test_train import model, ocr_set  # noqa: F401  (pytest 준비물)

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


SCORERS_DIR = Path(__file__).resolve().parents[1] / "scorers"


def test_bank_and_ocr_samples_match_default(tmp_path, model, ocr_set):
    """합성 세트 견본(bank_default·ocr_default)은 기본 채점과 같은 문항 점수, 붙여서 섞어도 정답 만점 검사를 지난다."""
    import contextlib
    import io

    from docgen.bench.ocr_data import read_jsonl
    from docgen.bench.runner import oracle_output
    from train import mix as M
    from train.tests.test_train import _item, bank_folder, data_cfg

    bank = E.load_scorer(str(SCORERS_DIR / "bank_default.py"))
    for it in [_item(t, "a") for t in ("cross_check", "review", "doc_check", "kie")] + [SWIFT, LISTED]:
        for out in (oracle_output(it), "엉뚱한 답", '{"x": 1}'):
            assert bank(it, out)["metrics"] == E.SCORERS[it["task"]](it, out)["metrics"], (it["id"], out)
    ocr = E.load_scorer(str(SCORERS_DIR / "ocr_default.py"))
    items = [it for f in sorted((ocr_set / "tasks").glob("*.jsonl")) for it in read_jsonl(f)]
    assert {it["task"] for it in items} >= {"crop_ocr", "grounding"}
    for it in items[:40]:
        r = ocr(it, oracle_output(it))
        one = E.score_task(it["task"], [it], {it["id"]: oracle_output(it)})   # 문항 하나면 기본 채점(과제 전체 계산)과 같다
        assert r["main"] == one["main"] and r["metrics"][r["main"]] == one["metrics"][one["main"]], it["id"]
    bank_folder(tmp_path / "train", "train", [f"m_{i}" for i in range(6)], n_images=1, size=(400, 560))
    bank_folder(tmp_path / "bench", None, ["b_0", "b_1"], n_images=1, size=(400, 560))
    bench = [{"id": "syn", "paths": [str(tmp_path / "bench")], "scorer": str(SCORERS_DIR / "bank_default.py")},
             {"id": "ocr", "paths": [str(ocr_set)], "scorer": str(SCORERS_DIR / "ocr_default.py")}]
    with contextlib.redirect_stdout(io.StringIO()):
        M.mix(data_cfg(tmp_path, benchmark=bench), model)   # cer 처럼 낮을수록 좋은 주 지표도 정답 = 만점


def test_swift_default_matches_old_swift_scoring():
    """swift_default (정답 글 그대로 + 질문) = 예전 기본 채점 (필드 순서와 배열을 짝지은 kie)."""
    fn = E.load_scorer(str(SCORERS_DIR / "swift_default.py"))
    raw = {"id": "po/1", "task": "kie", "answer": json.dumps(["EOA", "2025 05 21", ""]), "meta": {},
           "eval": {"raw": True, "prompt": 'What are … in order: ["NEGO_CLCT", "DATE", "TENOR"] …'}}
    for out in OUTPUTS + ['[{"value": "EOA"}, {"value": "2025 05 21"}, {"value": ""}]']:
        mine, old = fn(raw, out), E.SCORERS["kie"](SWIFT, out)
        if old["parse_fail"]:   # 견본은 예전에 못 읽던 꼴([{"key", "value"}] 목록)도 읽는다
            continue
        assert not mine.get("parse_fail"), out
        if True:
            assert {k: mine["metrics"][k] for k in ("f1", "field_acc", "doc_exact", "field_exact")} == \
                   {k: old["metrics"][k] for k in ("f1", "field_acc", "doc_exact", "field_exact")}, out


def test_swift_kie_scorer_reads_converted_file_and_jsonl_line(tmp_path):
    """temp/swift_to_kie_tmp.py 로 바꾼 파일: 파이프라인 문항과 .jsonl 한 줄 둘 다, 배열 답도. 정답을 못 읽으면 만점이 아니라 에러."""
    import runpy

    from PIL import Image

    from train.swift_import import load_swift

    Image.new("RGB", (32, 32), "white").save(tmp_path / "x.png")
    src = {"messages": [{"role": "user", "content": '<image>Extract in order: ["NEGO No", "Amount", "NEGO No"]'},
                        {"role": "assistant", "content": '["NO:ILH1", "", "X2"]'}], "images": [str(tmp_path / "x.png")]}
    (tmp_path / "in.jsonl").write_text(json.dumps(src) + "\n", encoding="utf-8")
    conv = runpy.run_path(str(Path(__file__).resolve().parents[2] / "temp" / "swift_to_kie_tmp.py"))
    conv["main"](str(tmp_path / "in.jsonl"), str(tmp_path / "out.jsonl"))
    line = json.loads((tmp_path / "out.jsonl").read_text(encoding="utf-8"))
    _, (item,) = load_swift(tmp_path / "out.jsonl")
    fn = E.load_scorer(str(Path(__file__).resolve().parents[1] / "scorers" / "swift_kie_scorer.py"))
    for it in (item, line):   # 파이프라인이 넘기는 문항 · 파일 한 줄 그대로
        assert fn(it, it.get("answer") or line["messages"][1]["content"])["metrics"]["f1"] == 1.0
        assert fn(it, '["NO.ILH1", null, "x2"]')["metrics"]["f1"] == 1.0   # 값만 순서대로
        assert fn(it, '{"NEGO No": "zz", "Amount": null, "NEGO No#2": "X2"}')["metrics"]["f1"] == 0.5
        assert fn(it, "모름")["parse_fail"]
    # v2 (temp/swift_to_kie_v2_tmp.py): 질문만 바뀜 — 답 꼴 예시가 실제 키, 키 옆에 항목명. 정답·채점은 같다
    v2 = runpy.run_path(str(Path(__file__).resolve().parents[2] / "temp" / "swift_to_kie_v2_tmp.py"))
    (tmp_path / "labels.json").write_text(json.dumps({"NEGO No": "매입번호"}, ensure_ascii=False), encoding="utf-8")
    v2["cmd_convert"](str(tmp_path / "out.jsonl"), str(tmp_path / "v2.jsonl"), str(tmp_path / "labels.json"))
    line2 = json.loads((tmp_path / "v2.jsonl").read_text(encoding="utf-8"))
    q = line2["messages"][0]["content"]
    assert '답 꼴: {"NEGO No": "…", "Amount": "…", "NEGO No#2": "…"}' in q and "- NEGO No: 매입번호" in q and "- Amount: -" in q
    assert '"키"' not in q and line2["messages"][1]["content"] == line["messages"][1]["content"] and line2["images"] == line["images"]
    _, (item2,) = load_swift(tmp_path / "v2.jsonl")
    assert fn(item2, '["NO.ILH1", null, "x2"]')["metrics"]["f1"] == 1.0
    assert fn(item2, '{"NEGO No": "zz", "Amount": null, "NEGO No#2": "X2"}')["metrics"]["f1"] == 0.5
    with pytest.raises(ValueError, match="키: 값"):
        fn({"answer": "", "eval": {"prompt": ""}}, '{"a": 1}')
