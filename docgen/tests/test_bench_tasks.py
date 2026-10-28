"""과제 파일 (docgen/bench/tasks/<과제>.py): 과제마다 질문·정답 만드는 법·답 형식이 한 파일에, build 가 그 차례대로 부른다."""
from docgen.bench import prompts
from docgen.bench import tasks as T
from docgen.bench.build import Builder
from docgen.bench.contracts import contracts
from docgen.bench.runner import oracle_output
from docgen.bench.evaluate import SCORERS, main_metric


def _doc(tmp_path):
    from PIL import Image

    Image.new("RGB", (100, 200), "white").save(tmp_path / "doc.png")
    fields = [
        {"key": "name", "label": "성명", "type": "text", "value": "홍길동", "bbox": [10, 10, 60, 30], "page": 0},
        {"key": "amount", "label": "금액", "type": "amount", "value": "1,000원", "bbox": [10, 40, 60, 60], "page": 0},
        {"key": "memo", "label": "비고", "type": "text", "value": None, "page": 0},
        {"key": "consent", "label": "동의", "type": "checkbox", "value": "동의", "bbox": [10, 70, 20, 80], "page": 0,
         "options": [{"text": "동의", "checked": True, "box_bbox": [10, 70, 20, 80]}, {"text": "미동의", "checked": False}]},
        {"key": "seal", "label": "도장", "type": "seal", "value": None, "present": False},
    ]
    return {"doc_id": "resident_id_card", "name": "주민등록증", "seed": 42, "group": "identity", "condition": "clean",
            "writing": "print", "images": ["doc.png"], "sizes": [(100, 200)], "fields": fields,
            "raw_keys": [f["key"] for f in fields], "visible": {"name", "amount", "consent"}}


def test_every_task_file_has_its_parts_and_feeds_the_format_catalog():
    c = contracts()
    for t in T.SINGLE:
        assert callable(t.make) and t.TASK in SCORERS
        assert c[t.TASK] == {"name": t.NAME, "prompt_template": t.PROMPT, "answer_schema": t.ANSWER,
                             "example": t.EXAMPLE, "notes": t.NOTES}
    assert T.kie.PROMPT == prompts.P_KIE and [t.TASK for t in T.SINGLE] == [
        "classify", "ocr_page", "ocr_field", "kie", "freetext", "marks", "form_qa"]


def test_builder_single_is_the_task_files_in_order_and_answers_score_perfectly(tmp_path):
    (tmp_path / "crops").mkdir()
    r = _doc(tmp_path)
    b = Builder.__new__(Builder)
    b.out, b.buf = tmp_path, []
    b.single(r, "images/resident_id_card_42", 6, 40)
    built = b.take()
    direct = T.make_single(r, "images/resident_id_card_42", tmp_path, 6, 40)
    assert [x["id"] for x in built] == [x["id"] for x in direct]
    assert all(x["answer"] == y["answer"] and x["prompt"] == y["prompt"] for x, y in zip(built, direct))
    kie = next(x for x in direct if x["task"] == "kie")   # 성명은 키 사전의 공통 키로 묻는다
    assert kie["answer"] == [{"key": "customer.name", "value": "홍길동", "bbox_2d": [100, 50, 600, 150], "page": 1},
                             {"key": "amount", "value": "1,000원", "bbox_2d": [100, 200, 600, 300], "page": 1},
                             {"key": "memo", "value": None}]
    marks = next(x for x in direct if x["task"] == "marks")
    assert marks["answer"] == [{"key": "consent", "value": "동의", "bbox_2d": [100, 350, 200, 400], "page": 1},
                               {"key": "seal", "value": False}]
    for x in built:
        s = SCORERS[x["task"]](x, oracle_output(x))["metrics"]
        assert s[main_metric(x["task"], s)] == 1, x["task"]
