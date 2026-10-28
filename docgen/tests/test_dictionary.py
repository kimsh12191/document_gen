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
    fk = json.loads((out / "form_keys.json").read_text(encoding="utf-8"))
    fk["forms"]["loan_application"]["applicant.name"] = {"who": None, "what": None, "by": "사람"}   # 문서별로 정함
    (out / "form_keys.json").write_text(json.dumps(fk, ensure_ascii=False), encoding="utf-8")
    B.build()
    fk2 = json.loads((out / "form_keys.json").read_text(encoding="utf-8"))["forms"]
    assert fk2["loan_application"]["applicant.name"] == {"who": None, "what": None, "by": "사람"}
    assert fk2["loan_application"]["applicant.rrn"] == {"who": "customer", "what": "rrn", "by": "자동"}
    again = json.loads((out / "roles.json").read_text(encoding="utf-8"))["roles"]["signer"]
    assert again["party"] == "related" and again["by"] == "사람"
    m2 = json.loads((out / "merges.json").read_text(encoding="utf-8"))["items"]
    assert next(x for x in m2 if (x["dict"], x["from"], x["into"]) == (pick["dict"], pick["from"], pick["into"]))["status"] == "rejected"


def test_common_key_resolution():
    loan = DIC.doc_type_of("loan_application")
    assert DIC.common_key(None, "customer.name") == "customer.name"          # 그 자체가 공통 키
    assert DIC.common_key(loan, "applicant.name") == "customer.name"          # 서식에서 고객 · 성명으로 정한 칸
    assert DIC.scope(loan, "bank") == "문서별"
    common = DIC.load("common")["keys"]
    assert common["customer.name"]["name"] == "고객 성명" and common["corp.name"]["name"] == "법인·사업자 상호"


def test_match_extracted_keys():
    assert DIC.match_extracted("customer.name") == "customer.name"
    assert DIC.match_extracted("BIC") == "foreign.swift" and DIC.match_extracted("swift_code") == "foreign.swift"
    assert DIC.match_extracted("applicant.name", DIC.doc_type_of("loan_application")) == "customer.name"
    assert DIC.match_extracted("mandate_id") is None


def test_field_key_is_who_and_what():
    """칸의 키 = 누구의 · 무엇이 공통 키이면 공통 키, 아니면 서식의 키 그대로 (문서별)."""
    assert DIC.key_for("customer", "name") == "customer.name" and DIC.key_for("customer", "seal") == "seal.customer"
    assert DIC.who_what("seal.customer") == ("customer", "seal") and DIC.who_what("corp.biz_no") == ("corp", "biz_no")
    f = DIC.field_key("loan_application", "applicant.name")
    assert (f["key"], f["common"], f["who"], f["what"]) == ("customer.name", True, "customer", "name")
    assert DIC.field_key("loan_application", "bank") == {"raw": "bank", "key": "bank", "common": False, "who": None, "what": None, "by": "없음"}
    fields = [{"key": "applicant.name", "value": "홍길동"}, {"key": "bank", "value": "하나은행"}]
    assert [(x["key"], x.get("doc_key")) for x in DIC.apply("loan_application", fields)] == [("customer.name", "applicant.name"), ("bank", None)]


def test_set_field_keeps_document_scope_and_clear_resets(tmpdict):
    f = DIC.set_field("loan_application", "applicant.name", None, None)       # 문서별로 정함 — 자동 초안이 다시 잇지 않게 남는다
    assert (f["key"], f["common"], f["by"]) == ("applicant.name", False, "사람")
    f = DIC.set_field("loan_application", "applicant.name", "agent", "name")
    assert (f["key"], f["common"]) == ("agent.name", True)
    f = DIC.set_field("loan_application", "applicant.name", "bank", "name")   # 은행·직원 · 성명은 공통 키가 아니다
    assert (f["key"], f["common"], f["who"]) == ("applicant.name", False, "bank")
    f = DIC.set_field("loan_application", "applicant.name", None, None, clear=True)
    assert f["by"] == "없음" and f["key"] == "applicant.name"
