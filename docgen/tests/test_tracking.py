import csv
import json

import pytest

from docgen.bench.tracking import composition, enrich, evaluate_groups
from train.score import score
from train.report import build


def text_item(ident, text, scenario=None):
    return {"id": ident, "task": "crop_ocr", "answer": {"text": text}, "eval": {},
            "meta": {"scenario": scenario} if scenario else {}}


def test_group_cer_recomputed_from_characters_not_item_mean():
    items = [text_item("short", "a", "mortgage"), text_item("long", "b" * 100, "mortgage")]
    result = evaluate_groups(items, {"short": "x", "long": "b" * 100})
    subset = result["breakdowns"]["scenario"]["mortgage"]["tasks"]["crop_ocr"]
    assert subset["n"] == 2
    assert subset["metrics"]["cer"] == pytest.approx(1 / 101)
    assert result["composition"]["by"]["label_format"] == {"text": 2}


def test_missing_scenario_and_field_units_are_explicit():
    items = [text_item("ocr", "a"), {"id": "work", "task": "doc_check", "meta": {}},
             {"id": "kie", "task": "kie", "meta": {"scenario": "mortgage"},
              "eval": {"fields": {"a": {"type": "amount"}, "b": {"kind": "date"}}}}]
    summary = composition(items)
    assert summary["n"] == 3
    assert summary["by"]["scenario"] == {"mortgage": 1, "not_applicable": 1, "unknown": 1}
    assert summary["field_kind_counts"] == {"amount": 1, "date": 1}
    enriched = enrich(items[0], "dataset-a")
    assert "source_dataset" not in items[0]["meta"]
    assert enriched["meta"]["source_dataset"] == "dataset-a"


def test_tracking_survives_train_mix_and_report(tmp_path):
    from train.mix import load_folder

    root = tmp_path / "evaluation"
    (root / "tasks").mkdir(parents=True)
    raw = [text_item("m", "abc", "mortgage"), text_item("j", "def", "jeonse_loan")]
    (root / "meta.json").write_text(json.dumps({"version": "test", "split": "test"}))
    (root / "tasks/crop_ocr.jsonl").write_text("\n".join(json.dumps(x) for x in raw))
    _, items = load_folder(root)
    assert all(it["meta"]["source_dataset"].startswith("evaluation@") for it in items)
    paths = []
    for label, predictions in (("start", {"m": "abc", "j": "xxx"}), ("sft", {"m": "abc", "j": "def"})):
        path = tmp_path / f"{label}.json"
        path.write_text(json.dumps({"label": label, "role": label, **score(items, predictions)}))
        paths.append(path)
    output = tmp_path / "benchmark.csv"
    build(paths, output)
    rows = list(csv.DictReader((tmp_path / "benchmark.breakdowns.csv").open(encoding="utf-8-sig")))
    row = next(r for r in rows if r["dimension"] == "scenario" and r["group"] == "jeonse_loan" and r["model"] == "sft")
    assert float(row["value"]) == 0
    assert float(row["delta_pp"]) == -100
    assert row["lower_is_better"] == "True"
    assert "mortgage" in output.with_suffix(".md").read_text(encoding="utf-8")
    assert (tmp_path / "benchmark.breakdowns.json").is_file()


def test_studio_respects_folder_train_split_without_row_split(tmp_path):
    from studio.datasets import items

    (tmp_path / "tasks").mkdir()
    (tmp_path / "meta.json").write_text(json.dumps({"split": "train"}))
    (tmp_path / "tasks/crop_ocr.jsonl").write_text(json.dumps(text_item("train-only", "a")))
    assert items({"path": str(tmp_path)}, evaluation=True) == {}


def test_ocr_provenance_survives_manifest_task_and_common_format(tmp_path, monkeypatch):
    from types import SimpleNamespace
    from docgen import ocr_set
    from docgen.bench.ocr_tasks import _row
    from docgen.bench.ocr_prepare import task_item

    recipe = tmp_path / "recipe.json"
    recipe.write_text(json.dumps({"track": "ocr", "split": "benchmark", "types": ["employment_certificate"], "per_doc": 1}))
    provenance = {"doc_type": "employment_certificate", "condition": "scan", "template_variant": {"id": "dense"}, "source_dataset": "original-source"}
    row = {"document_id": "document", "page_id": "page", "image": "page.png", "ocr_json": "page.json", "split": "benchmark", **provenance}
    monkeypatch.setattr(ocr_set, "_init", lambda scale: None)
    monkeypatch.setattr(ocr_set, "_one", lambda job: [row])
    ocr_set.build(SimpleNamespace(recipe=recipe, out=tmp_path / "output", workers=1, scale=1, no_prepare=True))
    manifest = json.loads((tmp_path / "output/manifest.jsonl").read_text(encoding="utf-8"))
    assert all(manifest[k] == v for k, v in provenance.items())
    view = {"kind": "clean", "id": "view", "ops": [], "image": "page.png"}
    prepared = _row(view, manifest, "crop_ocr", "read", "page.png", {"text": "a"}, [{"confidence": 1}])
    prepared["id"] = "example"
    common = task_item(prepared, tmp_path)
    assert all(common["meta"][k] == v for k, v in provenance.items())
    assert enrich(common, "container-source")["meta"]["source_dataset"] == "original-source"


def test_field_type_report_export_distinguishes_count_units(tmp_path):
    items = [{"id": "kie", "task": "kie", "answer": {"name": "Alice"},
              "eval": {"fields": {"name": {"type": "text", "kind": "name"}}}, "meta": {"group": "income", "condition": "clean"}}]
    report = score(items, {"kie": '{"name":"Alice"}'})
    path = tmp_path / "score.json"
    path.write_text(json.dumps({"label": "sft", **report}), encoding="utf-8")
    build([path], tmp_path / "report.csv")
    with (tmp_path / "report.breakdowns.csv").open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    field = next(r for r in rows if r["dimension"] == "field_kind")
    assert (field["group"], field["n"], field["unit"], field["value"]) == ("name", "1", "fields", "1.0")
    assert all(r["unit"] == "items" for r in rows if r["dimension"] != "field_kind")
    data = json.loads((tmp_path / "report.breakdowns.json").read_text(encoding="utf-8"))
    assert data["models"][0]["field_type_scores"]["kie"]["name"]["acc"] == 1
