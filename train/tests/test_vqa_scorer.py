import json
import pytest

from docgen.bench.evaluate import load_scorer
from train.mix import perfect
from train.qa_to_swift import records
from train.scorers.vqa_scorer import score
from train.swift_import import item_of


SCORER = "train/scorers/vqa_scorer.py:score"


@pytest.mark.parametrize("answer", ["정기예금", {"계좌번호": "[마스킹]", "날짜": "2023. 7. 12."},
                                  ["서명", "07월 20일", "[날인]"], [], {}, None, False, 7, "", " ", "123"])
def test_converter_import_scorer_oracle(answer, tmp_path):
    image = tmp_path / "a.png"
    image.touch()
    record = next(records({"image": str(image), "qa": [{"question": "질문", "answer": answer}]}))
    fn = load_scorer(SCORER)
    assert fn(record, record["messages"][1]["content"])["metrics"]["f1"] == 1
    item = item_of(record, "vqa", 1, tmp_path)
    item["eval"]["scorer"] = SCORER
    assert perfect(item)


def test_partial_missing_extra_and_null():
    item = {"answer": '{"a":"답", "b":null}'}
    assert score(item, '{"a":"답"}')["metrics"]["f1"] == pytest.approx(2 / 3)
    assert score(item, '{"a":"답", "b":null, "extra":"오답"}')["metrics"]["f1"] == pytest.approx(0.8)
    assert score(item, '{"b":null,"a":"답"}')["metrics"]["doc_exact"] == 1


def test_lists_preserve_order_duplicates_and_nested_structure():
    assert score({"answer": '["a","b"]'}, '["b","a"]')["metrics"]["f1"] == 0
    assert score({"answer": '["a","a"]'}, '["a"]')["metrics"]["f1"] == pytest.approx(2 / 3)
    assert score({"answer": '{"a":["b"]}'}, '{"a":{"0":"b"}}')["metrics"]["f1"] == 0
    assert score({"answer": '[]'}, '{}')["metrics"]["f1"] == 0


def test_text_normalization_preserves_meaningful_characters():
    assert score({"answer": " 정기  예금 "}, "정기\n예금")["metrics"]["f1"] == 1
    for gold, prediction in [("[마스킹]", "마스킹"), ("1,000", "1000"), ("ABC", "abc")]:
        assert score({"answer": gold}, prediction)["metrics"]["f1"] == 0


@pytest.mark.parametrize("output", ["", "설명입니다", '{"a":', '{"a":1,"a":2}', '{"a":NaN}'])
def test_invalid_json_is_zero(output):
    result = score({"answer": '{"a":1}'}, output)
    assert result["parse_fail"]
    assert result["metrics"]["f1"] == 0


def test_fenced_json_and_type_distinctions():
    assert score({"answer": '{"a":1}'}, '```json\n{"a":1}\n```')["metrics"]["f1"] == 1
    assert score({"answer": 'false'}, '0')["metrics"]["f1"] == 0
    assert score({"answer": '{"a":"1"}'}, '{"a":1}')["metrics"]["f1"] == 0
    assert score({"answer": "정기예금"}, json.dumps("정기예금"))["metrics"]["f1"] == 1
