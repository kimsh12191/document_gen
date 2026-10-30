import json

import pytest

from train.qa_to_swift import convert


def write_document(path, answers):
    document = {"image": "data/images/a.png", "qa": [
        {"question": f"질문 {i}\n공백 유지 ", "answer": answer}
        for i, answer in enumerate(answers)
    ]}
    path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8-sig")
    return document


def test_preserves_questions_and_all_answer_types(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    answers = ['문자열 "답"\n ', {"키": "[마스킹]", "빈칸": None}, ["서명", "날짜"], None, False, 7]
    document = write_document(source / "a.json", answers)
    output = tmp_path / "result.jsonl"
    assert convert(source, output) == (1, len(answers))
    rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
    for row, pair in zip(rows, document["qa"]):
        assert row["images"] == [document["image"]]
        assert row["messages"][0] == {"role": "user", "content": "<image>" + pair["question"]}
        content = row["messages"][1]["content"]
        assert row["messages"][1]["role"] == "assistant"
        assert (content if isinstance(pair["answer"], str) else json.loads(content)) == pair["answer"]


def test_recursive_and_image_root(tmp_path):
    source = tmp_path / "source"
    nested = source / "nested"
    nested.mkdir(parents=True)
    write_document(nested / "a.json", ["답"])
    image = tmp_path / "data/images/a.png"
    image.parent.mkdir(parents=True)
    image.touch()
    output = tmp_path / "result.jsonl"
    assert convert(source, output, recursive=True, image_root=tmp_path, check_images=True) == (1, 1)
    assert json.loads(output.read_text(encoding="utf-8"))["images"] == [str(image.resolve())]


def test_existing_output_is_untouched(tmp_path):
    write_document(tmp_path / "a.json", ["답"])
    output = tmp_path / "result.jsonl"
    output.write_text("original", encoding="utf-8")
    with pytest.raises(FileExistsError):
        convert(tmp_path, output)
    assert output.read_text(encoding="utf-8") == "original"


@pytest.mark.parametrize("bad", [
    {"image": "a.png", "qa": [{"question": "질문"}]},
    {"image": "a.png", "qa": []},
    {"image": "a.png", "qa": [{"question": "<image><image>질문", "answer": "답"}]},
])
def test_invalid_input_leaves_no_partial_output(tmp_path, bad):
    write_document(tmp_path / "a.json", ["답"])
    (tmp_path / "b.json").write_text(json.dumps(bad), encoding="utf-8")
    output = tmp_path / "result.jsonl"
    with pytest.raises(ValueError, match="b.json"):
        convert(tmp_path, output)
    assert not output.exists()


def test_missing_image_leaves_no_output(tmp_path):
    write_document(tmp_path / "a.json", ["답"])
    output = tmp_path / "result.jsonl"
    with pytest.raises(ValueError, match="image does not exist"):
        convert(tmp_path, output, check_images=True)
    assert not output.exists()
