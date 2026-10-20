"""studio 4단계 시험: 레시피·묶음 규칙 기본값, 시나리오 저장, 학습 설정 내보내기, 작업, 고객 일관성 검사."""
import argparse
import json
import sys
import time

import pytest

from docgen import registry as R
from docgen.bench import build as BUILD
from studio import bank_data as BD
from studio import datasets as DS
from studio import training_link as TL


def _args(**kw):
    a = argparse.Namespace(types="all", per_doc=1, scenarios="all", bundles=4, fields_per_doc=6, max_keys=40, scale=2.0,
                           start=0, split="test")
    for k, v in kw.items():
        setattr(a, k, v)
    return a


def test_empty_recipe_keeps_defaults(tmp_path):
    f = tmp_path / "r.json"
    f.write_text("{}", encoding="utf-8")
    a = _args()
    rc = BUILD.load_recipe(f, a)
    assert (a.types, a.per_doc, a.bundles) == ("all", 1, 4)
    b = BUILD.Builder.__new__(BUILD.Builder)   # 렌더러 없이 규칙만 본다
    b.rules = {**BUILD.BUNDLE_RULES, **(rc["rules"]["bundle"] or {})}
    assert b.rules == {"missing": [0.3, 0.5, 0.2], "other_customer": 0.3, "extra_doc": 0.35, "tamper": 0.5}
    assert rc["rules"]["conditions"] is None and rc["custom"] == []


def test_recipe_overrides(tmp_path):
    f = tmp_path / "r.json"
    f.write_text(json.dumps({"split": "train", "types": ["resident_id_card"], "scenarios": ["mortgage"],
                             "bundles": {"default": 2, "mortgage": 5}, "conditions": {"clean": 1.0},
                             "bundle": {"tamper": 0.9}, "custom_bundles": [{"scenario": "mortgage", "name": ""}]}), encoding="utf-8")
    a = _args()
    rc = BUILD.load_recipe(f, a)
    assert a.split == "train" and a.types == "resident_id_card" and a.scenarios == "mortgage"
    assert a.bundles == 2 and a.bundles_per == {"mortgage": 5}
    assert rc["rules"]["conditions"] == [("clean", 1.0)] and rc["rules"]["bundle"] == {"tamper": 0.9}
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"nope": 1}), encoding="utf-8")
    with pytest.raises(SystemExit):
        BUILD.load_recipe(bad, _args())


def test_pick_condition_default_unchanged():
    keys = [f"k{i}" for i in range(200)]
    assert [BUILD.pick_condition(k) for k in keys] == [BUILD.pick_condition(k, BUILD.CONDITIONS) for k in keys]


def test_validate_recipe():
    BD.validate_recipe(BD.TEMPLATES["bank-try"])
    with pytest.raises(ValueError):
        BD.validate_recipe({"types": ["no_such_form"]})
    with pytest.raises(ValueError):
        BD.validate_recipe({"conditions": {"clean": 0.5}})
    with pytest.raises(ValueError):
        BD.validate_recipe({"cases": {"nope": {"enabled": False}}})
    with pytest.raises(ValueError):
        BD.validate_recipe({"custom_bundles": [{"scenario": "nope"}]})


@pytest.fixture()
def scenarios_file(tmp_path, monkeypatch):
    original = R.SCENARIOS_JSON
    f = tmp_path / "scenarios.json"
    f.write_text(original.read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(R, "SCENARIOS_JSON", f)
    yield f
    R.SCENARIOS_JSON = original
    R.load_scenarios()


def test_save_scenarios_keeps_order(scenarios_file):
    items = [{"id": k, "name": n, "docs": d} for k, (n, d) in R.SCENARIOS.items()]
    with pytest.raises(ValueError):   # 순서 바꾸기 금지
        BD.save_scenarios_list(items[::-1])
    with pytest.raises(ValueError):   # 모르는 서식
        BD.save_scenarios_list(items + [{"id": "x", "name": "x", "docs": ["nope"]}])
    BD.save_scenarios_list(items + [{"id": "new_one", "name": "새 업무", "docs": ["resident_id_card"]}])
    assert list(R.SCENARIOS)[-1] == "new_one" and R.SCENARIOS["new_one"][1] == ["resident_id_card"]
    assert json.loads(scenarios_file.read_text(encoding="utf-8"))["scenarios"][-1]["id"] == "new_one"


def _bench(tmp_path, name, split):
    root = tmp_path / name
    (root / "tasks").mkdir(parents=True)
    (root / "meta.json").write_text(json.dumps({"version": "1.2", "split": split, "counts": {}}), encoding="utf-8")
    return root


def test_bank_training_config_and_status(tmp_path, monkeypatch):
    monkeypatch.setitem(TL.DIRS, "bank", tmp_path / "bank")
    (tmp_path / "bank" / "configs").mkdir(parents=True)
    (tmp_path / "bank" / "configs" / "bank_pipeline.example.json").write_text(
        json.dumps({"workdir": "../runs/bank1", "model": "/m", "data": {"sft_max_examples": 20000}}), encoding="utf-8")
    reg = DS.Registry(tmp_path / "ws", {str(tmp_path): "/share/x"})
    t = reg.register(str(_bench(tmp_path, "train1", "train")))
    b = reg.register(str(_bench(tmp_path, "bench1", "test")))
    with pytest.raises(ValueError):
        BD.bank_training_config(reg, [b["id"]], b["id"], None, "t")   # 평가 세트를 학습에
    info = BD.bank_training_config(reg, [t["id"]], b["id"], None, "exp 1")
    assert info["config"]["data"]["train"] == ["/share/x/train1"] and info["config"]["data"]["benchmark"] == "/share/x/bench1"
    assert info["file"] == "configs/studio-exp-1.json" and "고정" in info["warnings"][0]
    rec = TL.write_training(reg, info, [t["id"], b["id"]], b["id"], "exp 1")
    written = json.loads((tmp_path / "bank" / "configs" / "studio-exp-1.json").read_text(encoding="utf-8"))
    assert written["model"] == "/m" and written["data"]["sft_max_examples"] == 20000 and written["data"]["train"] == ["/share/x/train1"]
    st = TL.status(reg, rec)
    assert not st["started"] and not st["finished"]
    wd = (tmp_path / "bank" / "runs" / "exp-1")
    (wd / "predictions").mkdir(parents=True)
    (wd / "predictions" / "base.jsonl").write_text('{"id": "x", "prediction": "a"}\n', encoding="utf-8")
    (wd / "state.json").write_text(json.dumps({"done": TL.STAGES}), encoding="utf-8")
    st = TL.status(reg, rec)
    assert st["finished"] and st["attached"]
    assert [r["label"] for r in reg.get(b["id"])["runs"]] == ["학습 exp-1"]


def test_jobs_run_and_on_done(tmp_path):
    from studio.jobs import Jobs

    jobs = Jobs(tmp_path, tmp_path)
    j = jobs.start("t", "시험", [sys.executable, "-c", "import sys; print('1/2'); print('2/2')"], on_done=lambda job: {"ok": 1})
    for _ in range(300):
        if jobs.get(j["id"])["status"] != "running":
            break
        time.sleep(0.1)
    got = jobs.get(j["id"])
    assert got["status"] == "done" and got["result"] == {"ok": 1} and "2/2" in got["log_tail"]


def test_consistency_flags_wrong_name():
    from docgen.entities import make_profile

    p = make_profile(5)
    b = {"customer_seed": 5, "scenario": "mortgage", "docs": [
        {"doc_id": "a", "name": "A", "fields": [{"key": "applicant.name", "value": p.person.name},
                                                 {"key": "applicant.rrn", "value": p.person.rrn}]},
        {"doc_id": "b", "name": "B", "fields": [{"key": "customer.name", "value": "다른사람"}]},
        {"doc_id": "c", "name": "C", "why": "other_customer", "fields": [{"key": "customer.name", "value": "다른사람"}]}]}
    w = BD.consistency(b)
    assert [x["doc_id"] for x in w] == ["b"]
    prof = {x["what"]: x for x in BD.profile_view(b)}
    assert len(prof["성명"]["where"]) == 1 and len(prof["주민등록번호"]["where"]) == 1
