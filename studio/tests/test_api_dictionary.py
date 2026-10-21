"""키 사전 API (studio/api_dictionary.py): 저장소 파일 대신 사본으로 — 공통 키·문서별 키, 잇기·끊기, 공통으로 올리기, 문서·업무."""
import shutil

import pytest

pytest.importorskip("httpx2", reason="fastapi TestClient 가 쓰는 httpx2 없음 (도커 이미지에는 넣지 않음)")
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from docgen import dictionary as DIC
from studio import api_dictionary as AD

REPO = AD.ROOT


@pytest.fixture
def client(tmp_path, monkeypatch):
    d = tmp_path / "dictionary"
    shutil.copytree(DIC.DIR, d)
    monkeypatch.setattr(DIC, "DIR", d)
    (tmp_path / "guide" / "fields").mkdir(parents=True)
    shutil.copyfile(REPO / "guide" / "fields" / "fields.json", tmp_path / "guide" / "fields" / "fields.json")
    monkeypatch.setattr(AD, "ROOT", tmp_path)
    DIC._cache.clear()
    app = FastAPI()
    app.include_router(AD.make_router(lambda fn, *a, **k: fn(*a, **k)))
    yield TestClient(app)
    DIC._cache.clear()


def test_common_keys_and_doc_keys(client):
    s = client.get("/api/dictionary").json()
    assert 50 <= s["common"] <= 150 and s["doc_keys"] > 5000 and s["linked"] > 0
    common = {x["key"]: x for x in client.get("/api/dictionary/keys?scope=common").json()["rows"]}
    assert common["customer.name"]["name"] == "고객 성명" and common["foreign.swift"]
    assert not any(k.startswith("bank.") for k in common)                      # 은행 사용란은 공통 키가 아니다
    loan = DIC.doc_type_of("loan_application")
    rows = client.get(f"/api/dictionary/keys?scope=doc&doc={loan}").json()["rows"]
    app_name = next(r for r in rows if r["key"] == "applicant.name")
    assert app_name["to"] == "customer.name" and app_name["state"] in ("이음", "제안")
    assert any(r["to"] is None for r in rows)                                  # 문서별로 남는 칸


def test_link_cut_and_promote(client):
    loan = DIC.doc_type_of("loan_application")
    item = {"doc": loan, "key": "branch"}
    assert client.post("/api/dictionary/link", json={"items": [item], "to": "nope.key"}).status_code == 400
    assert client.put("/api/dictionary/key/bank.branch_name", json={"name": "은행 취급점", "kind": "text"}).status_code == 200
    assert client.post("/api/dictionary/link", json={"items": [item], "to": "bank.branch_name", "state": "이음"}).json()["changed"] == 1
    assert DIC.common_key(loan, "branch") == "bank.branch_name"
    k = client.get("/api/dictionary/key/bank.branch_name").json()
    assert k["docs"][0]["keys"][0]["key"] == "branch"
    client.post("/api/dictionary/link", json={"items": [item], "state": "끊음"})
    assert DIC.common_key(loan, "branch") is None
    assert client.put("/api/dictionary/key/Bad Key", json={"name": "x"}).status_code == 400


def test_docs_tasks_and_links(client):
    tid = DIC.doc_type_of("commercial_invoice")
    t = client.get("/api/dictionary/doc_types").json()["types"][tid]
    assert client.put(f"/api/dictionary/doc_type/{tid}", json={"name": t["name"], "group": t["group"],
                                                              "aliases": ["Commercial Invoice"]}).status_code == 200
    assert DIC.find_doc_type("COMMERCIAL INVOICE") == tid
    task = client.get("/api/dictionary/tasks").json()["tasks"]["fx_remittance"]
    assert client.put("/api/dictionary/task/fx_remittance", json={**task, "aliases": task["aliases"] + ["무역송금"]}).status_code == 200
    assert DIC.task_of("무역송금") == "fx_remittance"
    lt = client.get("/api/dictionary/links/task/fx_remittance").json()
    shared = {x["key"] for x in lt["shared"]}
    assert {"foreign.name", "foreign.address"} <= shared and all(k in DIC.load("common")["keys"] for k in shared)
    ld = client.get(f"/api/dictionary/links/doc_type/{tid}").json()
    assert "fx_remittance" in [x["id"] for x in ld["tasks"]] and ld["keys"] > ld["common"] > 0


def test_common_for_form(client):
    r = client.get("/api/dictionary/common_for/loan_application").json()
    keys = {x["key"]: x for x in r["keys"]}
    assert keys["customer.name"]["doc_key"] in ("applicant.name", "customer.name")
