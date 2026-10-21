"""키 사전 계층 API (studio/api_dictionary.py): 저장소 파일 대신 사본으로 — 역할 당사자 정하기, 업무별 역할, 합치기 결정."""
import json
import shutil

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from docgen import dictionary as DIC
from studio import api_dictionary as AD

REPO = AD.ROOT


@pytest.fixture
def client(tmp_path, monkeypatch):
    d = tmp_path / "dictionary"
    shutil.copytree(DIC.DIR, d)
    monkeypatch.setattr(DIC, "DIR", d)
    (tmp_path / "docgen").mkdir()
    shutil.copyfile(AD.ROOT / "docgen" / "keys.json", tmp_path / "docgen" / "keys.json")
    monkeypatch.setattr(AD, "ROOT", tmp_path)
    DIC._cache.clear()
    app = FastAPI()
    app.include_router(AD.make_router(lambda fn, *a, **k: fn(*a, **k)))
    yield TestClient(app), tmp_path
    DIC._cache.clear()


def test_summary_and_role(client):
    c, _ = client
    s = c.get("/api/dictionary").json()
    cust = next(p for p in s["parties"] if p["id"] == "customer")
    assert any(r["role"] == "applicant" for r in cust["roles"]) and s["unsure"] > 0
    r = c.get("/api/dictionary/role/applicant").json()
    assert any(k["key"] == "applicant.name" and k["party_key"] == "customer.name" for k in r["keys"])


def test_set_role_party_and_task_override(client):
    c, _ = client
    assert c.put("/api/dictionary/role/owner", json={"party": "related", "by_task": {"mortgage": "customer"}}).status_code == 200
    assert DIC.resolve("owner.name")["party"] == "related"
    assert DIC.resolve("owner.name", task="mortgage")["party"] == "customer"
    assert c.put("/api/dictionary/role/owner", json={"party": "nobody"}).status_code == 400


def test_accept_merge_and_duplicate_decision(client):
    c, root = client
    items = c.get("/api/dictionary/merges?q=employer.name").json()["items"]
    assert items and items[0]["into"] == "employer.name"
    r = c.post("/api/dictionary/merges", json={"items": items, "status": "accepted"}).json()
    assert r["changed"] == 1
    assert DIC.resolve("company.name")["canonical"] == "employer.name"
    dups = json.loads((root / "docgen" / "keys.json").read_text(encoding="utf-8"))["duplicates"]
    assert next(x for x in dups if set(x["keys"]) == {"company.name", "employer.name"})["decision"] == "employer.name"


def test_doc_type_and_task_edit(client):
    c, _ = client
    tid = DIC.doc_type_of("commercial_invoice")
    t = c.get("/api/dictionary/doc_types").json()["types"][tid]
    assert c.put(f"/api/dictionary/doc_type/{tid}", json={"name": t["name"], "group": t["group"],
                                                         "aliases": ["Commercial Invoice", "상업 인보이스"]}).status_code == 200
    assert DIC.find_doc_type("COMMERCIAL INVOICE") == tid
    task = c.get("/api/dictionary/tasks").json()["tasks"]["fx_remittance"]
    assert c.put("/api/dictionary/task/fx_remittance", json={**task, "aliases": task["aliases"] + ["무역송금"]}).status_code == 200
    assert DIC.task_of("무역송금") == "fx_remittance"


def test_links_task_doc_party_key(client):
    c, _ = client
    t = c.get("/api/dictionary/links/task/fx_remittance").json()
    assert len(t["doc_types"]) == 5
    shared = {x["party_key"]: x for x in t["shared"]}
    assert "foreign.name" in shared and len(shared["foreign.name"]["doc_types"]) >= 2     # 서류끼리 대조할 칸
    assert not any(k.startswith(("document.", "deal.", "issuer.", "unassigned.")) for k in shared)
    tid = DIC.doc_type_of("commercial_invoice")
    d = c.get(f"/api/dictionary/links/doc_type/{tid}").json()
    assert "fx_remittance" in [x["id"] for x in d["tasks"]] and any(x["party_key"] == "foreign.name" for x in d["party_keys"])
    pk = c.get("/api/dictionary/links/party_key/customer.name").json()
    assert len(pk["doc_types"]) > 20 and "mortgage" in [x["id"] for x in pk["tasks"]]


def test_single_keys_set_by_person(client):
    c, root = client
    (root / "guide" / "fields").mkdir(parents=True)
    shutil.copyfile(REPO / "guide" / "fields" / "fields.json", root / "guide" / "fields" / "fields.json")
    r = c.get("/api/dictionary/single?show=unassigned").json()
    assert r["counts"]["unassigned"] > 0 and r["rows"]
    attr = r["rows"][0]["attribute"]
    assert c.put("/api/dictionary/single", json={"parties": {attr: "document"}}).json()["changed"] == 1
    assert DIC.resolve(attr)["party"] == "document"
    assert attr in DIC.load("roles")["single_human"]
