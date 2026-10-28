"""화면·정적 문서의 연결 정보와 경로 제한을 확인한다. 브라우저 렌더링은 불필요하다."""
import json

import pytest

from studio import guidebook as G


def test_export_matches_current_catalog():
    data = G.catalog()
    saved = json.loads((G.ROOT / "guide/catalog.json").read_text(encoding="utf-8"))
    assert saved == data
    assert (G.ROOT / "guide/catalog.md").read_text(encoding="utf-8") == G.markdown(data)
    form = next(f for f in data["forms"] if f["id"] == "employment_certificate")
    assert form["fields"] and form["scenarios"]
    assert all("question_key" in f for f in form["fields"])
    assert "kie" in data["tasks"] and "ltv" in data["rules"]


def test_candidate_forms_inherit_role_operations(monkeypatch):
    monkeypatch.setattr(G, "load_scenarios", lambda: None)
    monkeypatch.setattr(G, "SCENARIOS", {"example": ("Example", ["employment_certificate"])})
    op = {"id": "extract-name", "kind": "extract", "left": {"doc": "employment_certificate", "key": "name"}}
    monkeypatch.setattr(G, "SCENARIO_PROCESSING", {"example": {"operations": [op]}})
    monkeypatch.setattr(G, "SCENARIO_SAMPLING", {"example": {"employment_certificate": {"mode": "sample", "forms": ["income_certificate"]}}})
    data = G.catalog()
    candidate = next(f for f in data["forms"] if f["id"] == "income_certificate")
    assert candidate["scenarios"][0]["roles"] == ["employment_certificate"]
    assert candidate["scenarios"][0]["operations"] == [op]
    assert "extract-name" in G.markdown(data, "income_certificate")


def test_document_allowlist():
    assert "agent-workflow.md" in G.DOCUMENTS
    assert "remote_build.py" in G.document("agent-workflow.md")
    with pytest.raises(KeyError):
        G.document("../studio/config.json")
