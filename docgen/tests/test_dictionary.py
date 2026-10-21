"""키 사전 (docgen/dictionary.py, docgen/dictionary/*.json): 당사자 풀이, 업무별 역할, 합치기 결정, 분류·업무 이름 찾기."""
import json
import shutil

import pytest

from docgen import dictionary as DIC


@pytest.fixture
def tmpdict(tmp_path, monkeypatch):
    d = tmp_path / "dictionary"
    shutil.copytree(DIC.DIR, d)
    monkeypatch.setattr(DIC, "DIR", d)
    DIC._cache.clear()
    yield d
    DIC._cache.clear()


def test_same_person_different_role_names_share_party_key():
    keys = ["customer.name", "applicant.name", "holder.name", "borrower.name", "debtor.name"]
    assert {DIC.resolve(k)["party_key"] for k in keys} == {"customer.name"}
    assert DIC.resolve("spouse.rrn")["party_key"] == "family.rrn"
    assert DIC.resolve("seal.applicant")["party_key"] == "seal.customer"      # 표시 요소도 같은 당사자
    assert DIC.resolve("rows.*.amount")["party_key"] == "deal.*.amount"


def test_task_overrides_role_party():
    assert DIC.resolve("buyer.name")["party"] == "counterparty"
    assert DIC.resolve("buyer.name", task="mortgage")["party"] == "customer"
    assert DIC.resolve("beneficiary.name", task="fx_remittance")["party"] == "foreign"


def test_accepted_merge_is_followed(tmpdict):
    assert DIC.resolve("company.corp_no")["canonical"] == "company.corp_reg_no"   # keys.json 에서 이미 정한 것
    m = json.loads((tmpdict / "merges.json").read_text(encoding="utf-8"))
    for x in m["items"]:
        if x["from"] == "SWIFTCode":
            x["status"] = "accepted"
    DIC.save("merges", m)
    assert DIC.resolve("SWIFTCode")["canonical"] == "foreign.swift"
    assert DIC.resolve("SWIFTCode")["party_key"] == "foreign.swift"


def test_doc_type_and_task_lookup():
    assert DIC.doc_type_of("hana_official_049") == DIC.doc_type_of("loan_application")
    assert DIC.find_doc_type("대출거래신청서") == DIC.doc_type_of("loan_application")
    assert DIC.task_of("주담대") == "mortgage" and DIC.task_of("주택담보대출") == "mortgage"


def test_every_role_has_a_known_party():
    parties = DIC.load("parties")["parties"]
    assert all(r["party"] in parties for r in DIC.load("roles")["roles"].values())


def test_rebuild_keeps_human_decisions(tmp_path, monkeypatch):
    import importlib.util

    spec = importlib.util.spec_from_file_location("build_dictionary", DIC.DIR.parent / "scripts" / "build_dictionary.py")
    B = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(B)
    out = tmp_path / "dictionary"
    shutil.copytree(DIC.DIR, out)
    monkeypatch.setattr(B, "OUT", out)
    roles = json.loads((out / "roles.json").read_text(encoding="utf-8"))
    roles["roles"]["signer"] = {**roles["roles"]["signer"], "party": "related", "by": "사람"}
    (out / "roles.json").write_text(json.dumps(roles, ensure_ascii=False), encoding="utf-8")
    m = json.loads((out / "merges.json").read_text(encoding="utf-8"))
    pick = next(x for x in m["items"] if x["status"] == "proposed")
    pick["status"] = "rejected"
    (out / "merges.json").write_text(json.dumps(m, ensure_ascii=False), encoding="utf-8")
    B.build()
    again = json.loads((out / "roles.json").read_text(encoding="utf-8"))["roles"]["signer"]
    assert again["party"] == "related" and again["by"] == "사람"
    m2 = json.loads((out / "merges.json").read_text(encoding="utf-8"))["items"]
    assert next(x for x in m2 if (x["dict"], x["from"], x["into"]) == (pick["dict"], pick["from"], pick["into"]))["status"] == "rejected"


def test_common_key_resolution():
    loan = DIC.doc_type_of("loan_application")
    assert DIC.common_key(None, "customer.name") == "customer.name"          # 그 자체가 공통 키
    assert DIC.common_key(loan, "applicant.name", include_suggested=True) == "customer.name"
    assert DIC.scope(loan, "bank") == "문서별"
    common = DIC.load("common")["keys"]
    assert common["customer.name"]["name"] == "고객 성명" and common["corp.name"]["name"] == "법인·사업자 상호"
