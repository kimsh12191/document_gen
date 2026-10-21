"""③ 처리 설정 시험: 추출·비교 작업과 설정 검사(docgen/bench/processing.py), 예시 실행(studio/scenario_processing.py)이
빌드(docgen.bench build)와 같은 입력·답을 내는지, 생략 사유가 남는지. 브라우저 없이."""
import copy
import json

import pytest

from docgen import registry as R
from docgen.bench import processing as P
from docgen.bench import build as BUILD
from docgen.bench.build import Builder
from docgen.bench.evaluate import SCORERS
from docgen.bench.runner import oracle_output
from studio import bank_data as BD
from studio.scenario_processing import run


IDS = ["loan_application", "lease_contract"]


def field(key, value, norm=None, kind="text", page=0):
    return {"key": key, "label": key, "value": value, "norm": value if norm is None else norm,
            "type": kind, "page": page, "bbox": [10, 20, 50, 40]}


def docs():
    return {
        "loan_application": {"name": "신청서", "fields": [field("loan.amount", "50,000,000원", 50000000, "amount")],
                             "sizes": [(100, 200)], "images": ["loan.png"]},
        "lease_contract": {"name": "계약서", "fields": [field("deposit", "100,000,000", 100000000, "amount")],
                           "sizes": [(100, 200)], "images": ["lease.png"]},
    }


def operations():
    return [{"id": "loan", "kind": "extract", "left": {"doc": IDS[0], "key": "loan.amount"}},
            {"id": "limit", "kind": "compare", "left": {"doc": IDS[0], "key": "loan.amount"},
             "operator": "lte", "right": {"doc": IDS[1], "key": "deposit"}}]


def test_extract_compare_and_evidence_use_existing_scorers():
    conf = P.validate({"operations": operations()}, IDS)
    rows = P.execute(conf, docs())
    assert rows[0]["answer"] == "50,000,000원"
    assert rows[0]["item"]["answer"][0]["bbox_2d"] == [100, 100, 500, 200]
    assert rows[1]["answer"] == "예"
    assert [s["doc"] for s in rows[1]["sources"]] == IDS
    for row in rows:
        item = row["item"]
        scored = SCORERS[item["task"]](item, oracle_output(item))["metrics"]
        assert scored["vl_f1" if item["task"] == "kie" else "acc"] == 1


@pytest.mark.parametrize("change", ["absent", "invisible", "masked", "not_numeric"])
def test_unavailable_comparison_is_skipped_with_reason(change):
    data = docs()
    f = data[IDS[1]]["fields"][0]
    if change == "absent":
        data[IDS[1]]["fields"] = []
    elif change == "invisible":
        f.pop("bbox")
    elif change == "masked":
        f["value"] = "100,***,***"
    else:
        f.update(type="text", value="미정", norm="미정")
    row = P.execute(P.validate({"operations": operations()}, IDS), data)[1]
    assert row["status"] == "skipped" and row["reason"]
    assert "item" not in row


def test_numeric_dates_and_text_comparison_are_explicit():
    assert P.compare(field("n", "1,000원", 1000), field("n", "1000", 1000), "equal") is True
    assert P.compare(field("d", "2026.10.20", "2026-10-20", "date"), field("d", "2026-10-19", "2026-10-19", "date"), "gt") is True
    assert P.compare(field("n", "김 하나"), field("n", "김하나"), "equal") is True
    assert P.compare(field("n", "김하나"), field("n", "이하나"), "equal") is False
    assert P.compare(field("n", "김*나"), field("n", "김*나"), "equal") is None


def test_config_validation_catches_stale_documents_and_unknown_options():
    assert P.validate(None, IDS)["case_ids"] is None
    assert P.selected(P.validate({"case_ids": []}, IDS), "case_ids", "typo") is False
    for conf in ({"rule_ids": ["unknown"]}, {"case_ids": "typo"}, {"review": 1},
                 {"operations": operations() + operations()}, {"operations": operations()}):
        with pytest.raises(ValueError):
            P.validate(conf, IDS[:1])


def test_processing_settings_survive_save_reload(tmp_path, monkeypatch):
    original = R.SCENARIOS_JSON
    target = tmp_path / "scenarios.json"
    target.write_bytes(original.read_bytes())
    with monkeypatch.context() as m:
        m.setattr(R, "SCENARIOS_JSON", target)
        items = [{"id": sid, "name": name, "docs": ids} for sid, (name, ids) in R.SCENARIOS.items()]
        items.append({"id": "processing_test", "name": "시험", "docs": IDS, "processing": {"operations": operations(), "case_ids": [], "rule_ids": ["jeonse_ratio"]}})
        BD.save_scenarios_list(items)
        R.load_scenarios()
        assert R.SCENARIO_PROCESSING["processing_test"]["operations"] == operations()
        view = next(x for x in BD.scenarios_view({}, {}) if x["id"] == "processing_test")
        assert view["processing"]["case_ids"] == []
        assert json.loads(target.read_text(encoding="utf8"))["scenarios"][-1]["processing"]["rule_ids"] == ["jeonse_ratio"]
    R.load_scenarios()


def test_builder_uses_processing_and_records_skipped_reasons(monkeypatch):
    sid = "processing_test"
    conf = {"doc_check": False, "cross_check": False, "review": False, "operations": operations()}
    monkeypatch.setitem(R.SCENARIOS, sid, ("시험", IDS))
    monkeypatch.setitem(R.SCENARIO_PROCESSING, sid, conf)
    b = Builder.__new__(Builder)
    b.buf = []
    b.conditions = [("clean", 1)]

    def render_doc(did, profile, seed, stem, condition):
        return {**copy.deepcopy(docs()[did]), "doc_id": did, "seed": seed, "condition": condition}

    b.render_doc = render_doc
    b.bundle(sid, 42)
    items = [x for x in b.buf if x["task"] != "_bundle"]
    record = b.buf[-1]
    assert [x["task"] for x in items] == ["kie", "review"]
    assert record["processing"]["review"] is False
    assert record["items"] == [x["id"] for x in items]
    assert record["processing_results"][1]["answer"] == "예"
    conf["operations"][1]["right"]["key"] = "missing_variant"
    b.buf = []
    b.bundle(sid, 42)
    assert b.buf[-1]["processing_results"][1]["status"] == "skipped"
    assert [x["task"] for x in b.buf] == ["kie", "_bundle"]


def test_preview_rule_answers_and_custom_operations_match_builder_inputs():
    seen = []

    def render(did, seed, extra):
        seen.append(extra)
        d = docs()[did]
        return {**copy.deepcopy(d), "doc_name": d["name"], "pages": [{"width": 100, "height": 200}]}

    result = run({"id": "jeonse_loan", "docs": IDS, "extra": {"loan_kind": "jeonse"},
                  "processing": {"cross_check": False, "rule_ids": ["jeonse_ratio"], "operations": operations()}}, 42, render)
    ratio = next(x for x in result["rows"] if x["kind"] == "rule" and x["id"] == "jeonse_ratio")
    assert ratio["status"] == "ready" and ratio["answer"] == 50
    assert [s["key"] for s in ratio["sources"]] == ["loan.amount", "deposit"]
    assert all(e == {"loan_kind": "jeonse", "scenario": "jeonse_loan", "form_bank": "하나은행"} for e in seen)
    assert all(x["status"] == "disabled" for x in result["rows"] if x["kind"] == "case")


def test_builder_only_generates_selected_builtin_review(monkeypatch):
    sid = "processing_rule_test"
    monkeypatch.setitem(R.SCENARIOS, sid, ("시험", IDS))
    monkeypatch.setitem(R.SCENARIO_PROCESSING, sid, {"doc_check": False, "cross_check": False, "rule_ids": ["jeonse_ratio"]})
    b = Builder.__new__(Builder)
    b.buf, b.conditions = [], [("clean", 1)]
    b.render_doc = lambda did, profile, seed, stem, cond: {**copy.deepcopy(docs()[did]), "doc_id": did, "seed": seed, "condition": cond}
    b.doc_valid = lambda *args: pytest.fail("선택하지 않은 유효기간 문항을 생성했습니다")
    b.bundle(sid, 42)
    assert [(x["task"], x.get("answer")) for x in b.buf[:-1]] == [("review", 50)]
    assert b.buf[0]["meta"]["rule"] == "jeonse_ratio"


def test_case_selection_and_recipe_exclusions_are_both_respected(monkeypatch):
    from types import SimpleNamespace

    sid = "processing_case_test"
    calls = []
    monkeypatch.setitem(R.SCENARIO_PROCESSING, sid, {"case_ids": ["typo"]})
    monkeypatch.setattr(BUILD, "CASES", [SimpleNamespace(id=cid, category="typo", fn=lambda ctx, tamper, rng, cid=cid: calls.append(cid))
                                       for cid in ("typo", "loan_vs_agreement")])
    b = Builder.__new__(Builder)
    b.cases, b.rules = {"typo": {"enabled": False}}, BUILD.BUNDLE_RULES
    data = [{**d, "doc_id": did} for did, d in docs().items()]
    profile = Builder.bundle_profile("jeonse_loan", 42)
    b.cross_checks(data, profile, 42, "bid", {"scenario": sid})
    assert calls == []
    b.cases = {}
    b.cross_checks(data, profile, 42, "bid", {"scenario": sid})
    assert calls == ["typo"]


def test_table_calculation_links_each_amount_cell():
    def render(did, seed, extra):
        return {"doc_name": "송장", "images": ["invoice.png"], "pages": [{"width": 100, "height": 200}],
                "fields": [field("items.0.amount", "100", 100, "amount"), field("items.1.amount", "200", 200, "amount")]}

    result = run({"docs": ["commercial_invoice"], "processing": {"cross_check": False, "rule_ids": ["invoice_sum"]}}, 0, render)
    row = next(x for x in result["rows"] if x["id"] == "invoice_sum" and x["kind"] == "rule")
    assert row["answer"] == 300
    assert [x["key"] for x in row["sources"]] == ["items.0.amount", "items.1.amount"]


def test_common_key_operation_finds_linked_field():
    """공통 키 작업: 서식마다 키가 달라도(applicant.name · employee.name) 이은 칸을 찾아 비교한다 (키 사전 K3)."""
    ids = ["loan_application", "employment_certificate"]
    conf = P.validate({"operations": [{"id": "same_name", "kind": "compare", "operator": "equal",
                                       "left": {"doc": ids[0], "common": "customer.name"},
                                       "right": {"doc": ids[1], "common": "customer.name"}}]}, ids)
    d = {ids[0]: {"name": "대출신청서", "fields": [field("applicant.name", "홍길동")], "sizes": [(100, 200)]},
         ids[1]: {"name": "재직증명서", "fields": [field("employee.name", "홍길동")], "sizes": [(100, 200)]}}
    row = P.execute(conf, d)[0]
    assert row["status"] == "ready" and row["answer"] == "예" and [s["key"] for s in row["sources"]] == ["applicant.name", "employee.name"]
    d[ids[1]]["fields"] = [field("employee.name", "김철수")]
    assert P.execute(conf, d)[0]["answer"] == "아니오"
    d[ids[1]]["fields"] = [field("other.key", "홍길동")]
    assert P.execute(conf, d)[0]["status"] == "skipped"                   # 이은 칸이 없으면 건너뛴다
    with pytest.raises(ValueError, match="공통 키"):
        P.validate({"operations": [{"id": "x", "kind": "extract", "left": {"doc": ids[0], "common": "no.such"}}]}, ids)


def test_classify_accepts_aliases():
    item = {"answer": "재직증명서", "eval": {"aliases": ["Certificate of Employment", "경력·재직증명"]}}
    assert SCORERS["classify"](item, "Certificate of Employment")["metrics"]["acc"] == 1.0
    assert SCORERS["classify"](item, "주민등록증")["metrics"]["acc"] == 0.0
