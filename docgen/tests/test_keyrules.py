"""키 사전 데이터 (docgen/key_rules.json, docgen/keyrules.py): 규칙이 overlay 생성에 쓰이고, 화면에서 더한 키·값 종류가 값을 만든다."""
import json
import random
import shutil

import pytest

from docgen import keyrules as KR
from docgen import realform as RF
from docgen.entities import make_profile
from docgen.schema import canonical_key


@pytest.fixture
def rules(tmp_path, monkeypatch):
    """저장소 파일 대신 사본으로 (고쳐도 저장소의 key_rules.json 은 그대로)."""
    p = tmp_path / "key_rules.json"
    shutil.copyfile(KR.PATH, p)
    monkeypatch.setattr(KR, "PATH", p)
    monkeypatch.setattr(KR, "_cache", None)
    yield p
    KR._cache = None


def test_rules_drive_overlay_keys_and_kinds():
    assert RF.key_of("성명") == "customer.name" and RF.key_of("예금주") == "customer.name"
    assert RF.kind_of("통화", None, None) == "currency" and RF.kind_of("만기일", None, None) == "date"
    assert RF.KEY_RULES == [tuple(x) for x in KR.load()["label_rules"]]
    assert canonical_key("customer.dob") == "customer.birth"


def test_data_kinds_make_values():
    p, r = make_profile(3), random.Random(1)
    assert KR.make_value("swift", p, r) == p.foreign.swift
    iban = KR.make_value("iban", p, r)
    assert iban[:2] in ("DE", "NL", "GB", "FR", "CH", "BE") and len(iban.replace(" ", "")) == 18   # 틀: 국가 2 + 검사 2 + 14자리
    assert KR.make_value("incoterms", p, r) in KR.load()["kinds"]["incoterms"]["choices"]
    assert KR.from_pattern("A#a-{X|Y}", random.Random(0))[3:] in ("-X", "-Y")
    assert KR.make_value("date", p, r) is None                       # 코드 종류는 realform 이 만든다
    assert RF.Values(p, r, "기본").by_kind("hs_code", "HS CODE").count("-") == 1   # 코드 종류가 아니면 데이터 종류로


def test_validate_rejects_bad_rules(rules):
    d = KR.load()
    bad = json.loads(json.dumps(d))
    bad["kinds"]["date"] = {"how": "pattern", "pattern": "#"}
    with pytest.raises(ValueError, match="코드로 만드는"):
        KR.save(bad)
    bad = json.loads(json.dumps(d))
    bad["keys"]["x.y"] = {"kind": "nope"}
    with pytest.raises(ValueError, match="모르는 값 종류"):
        KR.save(bad)
    bad = json.loads(json.dumps(d))
    bad["keys"]["a.b"] = {"aliases": ["bic"]}                       # bic 은 foreign.swift 의 동의어
    with pytest.raises(ValueError, match="둘에"):
        KR.save(bad)


def test_enabling_labels_maps_overlay_field(rules):
    assert RF.key_of("SWIFT Code") is None                           # 기본: 항목명 제안은 꺼져 있다 (생성 결과가 그대로)
    d = json.loads(json.dumps(KR.load()))
    d["keys"]["foreign.swift"]["labels"] = ["SWIFT Code"]
    KR.save(d)
    assert RF.key_of("SWIFT Code") == "foreign.swift" and RF.key_of("swiftcode") == "foreign.swift"
    p = make_profile(5)
    assert RF.Values(p, random.Random(0), "기본").std("foreign.swift") == p.foreign.swift
    assert KR.alias_index()["bic"] == "foreign.swift"


def test_affected_forms_counts_overlay_labels():
    from studio.api_keys import affected_forms

    assert affected_forms(["SWIFTCode"])                             # 그 항목명이 있는 overlay 서식이 있다
    assert affected_forms(["   "]) == []
