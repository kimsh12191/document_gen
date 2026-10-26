"""생각 블록이 붙은 답 채점, 이미 낸 답으로 다시 채점 (train/rescore.py)."""
import contextlib
import io

from docgen.bench import evaluate as E
from docgen.bench.ocr_data import read_json, write_json, write_jsonl
from train import rescore as R
from train.tests.test_train import _item

T = "<think>\n\n</think>\n\n"
CLS = {"id": "classify/a", "task": "classify", "answer": "외화송금신청서", "eval": {}, "meta": {}}
FIELD = {"id": "ocr_field/a", "task": "ocr_field", "answer": "AT SIGHT", "eval": {}, "meta": {}}
BL = {"id": "kie/bl", "task": "kie", "answer": {"a": "AT SIGHT", "b": "MAIL TO"}, "meta": {},
      "eval": {"order": ["a", "b"], "fields": {"a": {"type": "text"}, "b": {"type": "text"}}}}


def test_think_block_and_wrapped_values():
    """생각 블록(비어 있어도)을 떼고 채점, swift-fields 의 [{"value": …}] 도 값으로."""
    assert E.reward("classify", T + "외화송금신청서", CLS) == 1.0
    assert E.reward("classify", "<think>\n고민\n</think>\n외화송금신청서", CLS) == 1.0
    assert E.reward("classify", "<think>\n끝나지 않은 생각", CLS) == 0.0
    assert E.reward("ocr_field", T + "AT SIGHT", FIELD) == 1.0
    assert E.reward("kie", T + '[{"value": "AT SIGHT"}, {"value": "MAIL TO"}]', BL) == 1.0
    assert E.score_task("classify", [CLS], {CLS["id"]: T + "외화송금신청서"})["metrics"]["acc"] == 1.0


def test_rescore_workdir(tmp_path):
    items = [CLS, FIELD, BL, _item("kie", "k")]
    data, wd = tmp_path / "data", tmp_path / "wd"
    write_jsonl(data / "benchmark_items.jsonl", items)
    write_jsonl(data / "benchmark_tasks.jsonl", [{"id": it["id"]} for it in items])
    write_json(wd / "config.json", {"data": {"output_dir": str(data)}})
    preds = wd / "predictions" / "sft-x.jsonl"
    write_jsonl(preds, [{"id": CLS["id"], "prediction": T + "외화송금신청서"}, {"id": FIELD["id"], "prediction": T + "AT SIGHT"},
                        {"id": BL["id"], "prediction": '["AT SIGHT", "MAIL TO"]'}, {"id": "kie/k", "prediction": '{"name": "김나우"}'}])
    from train.score import score
    old = score(items, {})   # 예전 채점 결과인 척: 다 틀림
    write_json(wd / "reports" / "sft.json", {"label": "SFT", "role": "sft", "model": "/m", "predictions": str(preds), **old})
    with contextlib.redirect_stdout(io.StringIO()):
        R.rescore_workdir(wd)
    new = read_json(wd / "reports" / "sft.json")
    assert new["label"] == "SFT" and new["tasks"]["classify"]["metrics"]["acc"] == 1.0 and new["tasks"]["kie"]["metrics"]["f1"] == 1.0
    (backup,) = (wd / "reports").glob("before-rescore-*")
    assert read_json(backup / "sft.json")["tasks"]["classify"]["metrics"]["acc"] == 0.0
