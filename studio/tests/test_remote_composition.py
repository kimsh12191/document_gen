import importlib.util
import json
from pathlib import Path
import sys


def test_remote_composition_command_saves_actual_api_response(tmp_path, monkeypatch):
    path = Path(__file__).resolve().parents[2] / "docker/remote_build.py"
    spec = importlib.util.spec_from_file_location("remote_tracking_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    calls = []
    expected = {"all": {"n": 10}, "evaluation": {"n": 4}, "provenance": {"recipe": "주택담보"}}
    monkeypatch.setattr(module, "call", lambda path: calls.append(path) or expected)
    output = tmp_path / "composition.json"
    monkeypatch.setattr(sys, "argv", [str(path), "--url", "http://studio", "composition", "loan set/#", "--out", str(output)])
    module.main()
    assert calls == ["/api/datasets/loan%20set%2F%23/composition"]
    assert json.loads(output.read_text(encoding="utf-8")) == expected
