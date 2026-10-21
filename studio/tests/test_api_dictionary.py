"""키 사전 API (studio/api_dictionary.py): 저장소 파일 대신 사본으로 — 공통 키(누구의 × 무엇), 서식의 칸, 칸 정하기, 정리할 것, 문서·업무.
TestClient(httpx2) 없이 라우터의 함수를 바로 부른다."""
import inspect
import shutil

import pytest
from fastapi import HTTPException

from docgen import dictionary as DIC
from studio import api_dictionary as AD


class Api:
    def __init__(self, router):
        self.ep = {(m, rt.path): rt.endpoint for rt in router.routes for m in rt.methods}

    def __call__(self, method, path, **kw):
        return self.ep[(method, path)](**kw)

    def req(self, method, path, **kw):
        """그 API 의 요청 본문(pydantic 모델)."""
        return inspect.signature(self.ep[(method, path)]).parameters["req"].annotation(**kw)


@pytest.fixture
def api(tmp_path, monkeypatch):
    d = tmp_path / "dictionary"
    shutil.copytree(DIC.DIR, d)
    monkeypatch.setattr(DIC, "DIR", d)
    DIC._cache.clear()
    yield Api(AD.make_router(lambda fn, *a, **k: fn(*a, **k)))
    DIC._cache.clear()


def test_summary_and_common_table(api):
    s = api("GET", "/api/dictionary")
    assert 50 <= s["common"] <= 150 and s["cells"] > 10000 and 0 < s["common_cells"] < s["cells"]
    rows = {x["key"]: x for x in api("GET", "/api/dictionary/common")["rows"]}
    c = rows["customer.name"]
    assert (c["who"], c["what"], c["name"]) == ("customer", "name", "고객 성명") and c["forms"] > 100
    assert (rows["seal.customer"]["who"], rows["seal.customer"]["what"]) == ("customer", "seal")
    assert not any(k.startswith("bank.") for k in rows)                       # 은행 사용란은 공통 키가 아니다
    v = api("GET", "/api/dictionary/vocab")
    assert "unassigned" not in {w["id"] for w in v["who"]} and {"seal", "sign", "name"} <= {w["id"] for w in v["what"]}


def test_cells_and_set_who_what(api):
    rows = api("GET", "/api/dictionary/cells", form="loan_application")["rows"]
    name = next(r for r in rows if r["raw"] == ["applicant.name"])
    assert (name["key"], name["common"], name["who"]) == ("customer.name", True, "customer")
    assert any(not r["common"] for r in rows)                                 # 문서별로 남는 칸
    sign = next(r for r in api("GET", "/api/dictionary/cells", form="hf011")["rows"] if r["t"] == "sign")
    assert len(sign["raw"]) == 3                                               # 서명 칸 = 이름·도장·서명
    put = lambda who: api("PUT", "/api/dictionary/cells", req=api.req("PUT", "/api/dictionary/cells",  # noqa: E731
                                                                      items=[{"form": "hf011", "keys": sign["raw"]}], who=who, what="name"))
    assert {k["key"] for k in put("agent")["keys"]} == {"agent.name", "seal.agent", "sign.agent"}
    assert not any(k["common"] for k in put("bank")["keys"])                   # 은행·직원 칸은 문서별
    with pytest.raises(HTTPException):
        put("nobody")


def test_new_common_key_and_todo(api):
    new = lambda **kw: api("POST", "/api/dictionary/common", req=api.req("POST", "/api/dictionary/common", **kw))  # noqa: E731
    k = new(who="bank", what="branch_name", name="은행 취급점")
    assert k["key"] == "bank.branch_name" and DIC.common_of("bank", "branch_name") == "bank.branch_name"
    with pytest.raises(HTTPException):
        new(who="bank", what="branch_name")                                    # 이미 있음
    groups = {g["id"]: g for g in api("GET", "/api/dictionary/todo")["groups"]}
    assert set(groups) == {"candidate", "mark", "who", "broken"}
    assert all(r["suggest"]["key"] in DIC.load("common")["keys"] for r in groups["candidate"]["rows"])


def test_common_for_form_and_docs(api):
    keys = {x["key"]: x for x in api("GET", "/api/dictionary/common_for/{form_id}", form_id="loan_application")["keys"]}
    assert keys["customer.name"]["doc_key"] in ("applicant.name", "customer.name")
    tid = DIC.doc_type_of("commercial_invoice")
    ld = api("GET", "/api/dictionary/links/doc_type/{tid}", tid=tid)
    assert "fx_remittance" in [x["id"] for x in ld["tasks"]] and ld["keys"] > ld["common"] > 0
    lt = api("GET", "/api/dictionary/links/task/{tid}", tid="fx_remittance")
    assert {"foreign.name", "foreign.address"} <= {x["key"] for x in lt["shared"]}
