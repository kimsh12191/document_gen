import json

import pytest

from docgen.bench.ocr_tasks import PROMPTS
from docgen.bench.ocr_metrics import answer_for
from studio import ocr_examples as E


def test_all_ocr_tasks_have_consistent_examples_and_images():
    data = E.examples()
    assert len(data["examples"]) == 8
    assert {x["task"] for x in data["examples"]} == set(PROMPTS)
    for x in data["examples"]:
        assert x["prompt"] == x["record"]["messages"][0]["content"]
        assert x["target"] == json.loads(x["record"]["target"])
        assert x["model_answer"] == answer_for(x["task"], x["record"]["target"])
        for url in [x["input_image"], *x["annotated_images"]]:
            assert (E.IMAGES / url.rsplit("/", 1)[1]).is_file()
        assert x["input_image"] not in x["annotated_images"]


def test_missing_task_fails_explicitly(tmp_path, monkeypatch):
    path = tmp_path / "tasks.md"
    path.write_text("# Empty guide\n", encoding="utf-8")
    monkeypatch.setattr(E, "SOURCE", path)
    with pytest.raises(ValueError):
        E.examples()
