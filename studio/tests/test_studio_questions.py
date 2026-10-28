"""① 문항 Q/A 시험 (studio/questions.py): 실제 Builder.single 문항과 같고 정답을 답으로 넣으면 만점, 공통 형식 목록, 시나리오 Q/A."""
from PIL import Image

from docgen.bench.build import Builder
from docgen.bench.contracts import contracts
from docgen.bench import prompts
from docgen.bench.evaluate import SCORERS, main_metric
from docgen.bench.runner import oracle_output
from studio.questions import form_items
from studio.scenario_processing import run


def label(root):
    Image.new("RGB", (100, 200), "white").save(root / "doc.png")
    fields = [
        {"key": "name", "label": "성명", "type": "text", "value": "홍길동", "norm": "홍길동", "bbox": [10, 20, 60, 40]},
        {"key": "amount", "label": "금액", "type": "amount", "value": "1,000", "norm": 1000, "bbox": [10, 50, 60, 70]},
        {"key": "consent", "label": "동의", "type": "checkbox", "value": "동의", "options": [
            {"text": "동의", "checked": True, "box_bbox": [10, 80, 20, 90]}]},
        {"key": "seal", "label": "도장", "type": "seal", "value": None, "present": False},
    ]
    return {"doc_type": "resident_id_card", "doc_name": "주민등록증", "seed": 42, "group": "identity", "condition": "clean",
            "writing": "print", "pages": [{"width": 100, "height": 200}], "images": ["doc.png"], "fields": fields,
            "raw_keys": [f["key"] for f in fields], "visible": ["name", "amount", "consent"]}


def test_form_qa_matches_real_single_builder_and_scores_perfectly(tmp_path):
    l = label(tmp_path)
    (tmp_path / "crops").mkdir()
    b = Builder.__new__(Builder)
    b.out, b.buf = tmp_path, []
    b.single({**l, "doc_id": l["doc_type"], "name": l["doc_name"], "sizes": [(100, 200)], "visible": set(l["visible"])},
             "images/resident_id_card_42", 6, 40)
    expected = b.take()
    actual = form_items(l, tmp_path)
    assert {x["task"] for x in actual} == {"classify", "ocr_page", "ocr_field", "kie", "marks"}
    assert len(actual) == len(expected)
    for a, e in zip(actual, expected):
        assert all(a[k] == e[k] for k in ("id", "task", "prompt", "answer", "meta"))
        assert a.get("eval") == e.get("eval")
        assert a["model_answer"] == oracle_output(e)
        assert all((tmp_path / p).is_file() for p in a["images"])
        assert all(url.startswith("/preview/") for url in a["image_urls"])
        scores = SCORERS[a["task"]](a, a["model_answer"])["metrics"]
        assert scores[main_metric(a["task"], scores)] == 1
    ocr = next(x for x in actual if x["task"] == "ocr_page")
    assert isinstance(ocr["answer"], list) and isinstance(ocr["model_answer"], str)


def test_format_catalog_uses_generator_prompts_and_all_tasks():
    c = contracts()
    assert set(c) == set(SCORERS)
    assert c["kie"]["prompt_template"] == prompts.P_KIE
    assert c["review"]["prompt_template"] == prompts.P_REVIEW
    assert c["kie"]["answer_schema"]["items"]["properties"]["page"]["minimum"] == 1


def test_scenario_qa_exposes_real_kie_array_and_wrapped_review(tmp_path):
    l = label(tmp_path)
    conf = {"id": "account_opening", "name": "계좌개설", "docs": ["resident_id_card"],
            "processing": {"cross_check": False, "review": False, "operations": [
                {"id": "extract_name", "kind": "extract", "left": {"doc": "resident_id_card", "key": "name"}},
                {"id": "same_name", "kind": "compare", "left": {"doc": "resident_id_card", "key": "name"},
                 "right": {"doc": "resident_id_card", "key": "name"}, "operator": "equal"}]}}
    result = run(conf, 42, lambda *args, **kw: l)
    doc_check, extract, compare = result["rows"][:3]
    assert "필수 제출 서류:" in doc_check["qa"][0]["prompt"]
    assert isinstance(extract["answer"], str)
    assert isinstance(extract["qa"][0]["answer"], list)
    assert extract["qa"][0]["answer"][0]["page"] == 1
    assert compare["qa"][0]["prompt"].startswith("고객이 '계좌개설'")
    for row in (doc_check, extract, compare):
        item = row["qa"][0]
        scores = SCORERS[item["task"]](item, item["model_answer"])["metrics"]
        assert scores[main_metric(item["task"], scores)] == 1
