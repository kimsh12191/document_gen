"""두 단계 샘플링의 재현성·키 연결·실제 이미지/정답 일치."""
import copy
import random

import pytest

from docgen import registry as R
from docgen import template_variants as T
from docgen import html_regions as HR
from docgen.entities import make_profile
from docgen.render import render
from docgen.roles import resolve,resolve_processing,validate_sampling
from docgen.schema import build_fields


def test_layout_sampling_preserves_semantic_values():
    spec=R.load_all()["employment_certificate"]
    chosen=set()
    for seed in range(8):
        reference=None
        for variant in ("default","letter","record"):
            p=make_profile(seed);p.extra["template_variants"]={spec.id:variant}
            html,fields,data=render(spec,p,seed)
            actual={f["key"]:f.get("value") for f in fields}
            if reference is None:reference=actual
            assert actual==reference
            assert data["_template_variant"]["id"]==variant
        first=render(spec,make_profile(seed),seed)
        assert first[0]==render(spec,make_profile(seed),seed)[0]
        chosen.add(first[2]["_template_variant"]["id"])
    assert chosen=={"default","letter","record"}


def test_variant_files_and_validation(tmp_path,monkeypatch):
    monkeypatch.setattr(T,"ROOT",tmp_path)
    T.add("employment_certificate","letter_copy","회사별 양식")
    cfg=T.load("employment_certificate");cfg["mode"]="fixed";cfg["fixed"]="letter_copy"
    T.save("employment_certificate",cfg)
    assert T.choose(R.load_all()["employment_certificate"],42,{})["id"]=="letter_copy"
    assert HR.path("employment_certificate","letter_copy")!=HR.path("employment_certificate")
    for bad in ("../outside","UPPER","default"):
        with pytest.raises(ValueError):T.add("employment_certificate",bad,"잘못된 ID")
    cfg["variants"][1]["weight"]=float("nan")
    with pytest.raises(ValueError):T.save("employment_certificate",cfg)


def test_role_sampling_one_per_slot_and_no_cross_role():
    docs=["loan_application","employment_certificate"]
    sampling={"loan_application":{"mode":"sample","forms":["loan_application","hana_official_049"],"weights":{"loan_application":1,"hana_official_049":2}}}
    chosen=set()
    for seed in range(30):
        rows=resolve(docs,sampling,seed,"test")
        assert rows==resolve(docs,sampling,seed,"test")
        assert len(rows)==2 and len({r["role"] for r in rows})==2
        chosen.add(rows[0]["id"])
    assert chosen=={"loan_application","hana_official_049"}
    with pytest.raises(ValueError):validate_sampling(docs,{"loan_application":{"mode":"sample","forms":["gov_income"]}})
    with pytest.raises(ValueError):validate_sampling(docs,{"loan_application":{"mode":"sample","forms":[]}})
    with pytest.raises(ValueError):resolve(["loan_application","hf049"],None,0,"test")


def test_preview_and_builder_select_same_document_and_keys(monkeypatch):
    from docgen.bench.build import Builder
    from studio.scenario_processing import run

    sid="sample_test";docs=["loan_application"]
    sampling={"loan_application":{"mode":"sample","forms":["hana_official_049"]}}
    processing={"doc_check":False,"cross_check":False,"review":False,"operations":[{"id":"amount","kind":"extract","left":{"doc":"loan_application","key":"loan.amount","keys":{"hana_official_049":"native.amount"}}}]}
    monkeypatch.setitem(R.SCENARIOS,sid,("시험",docs));monkeypatch.setitem(R.SCENARIO_SAMPLING,sid,sampling);monkeypatch.setitem(R.SCENARIO_PROCESSING,sid,processing)
    def fake(did,seed):
        return {"doc_id":did,"doc_name":R.load_all()[did].name,"name":R.load_all()[did].name,"images":["page.png"],"seed":seed,"condition":"clean","pages":[{"width":100,"height":200}],"sizes":[(100,200)],"fields":[{"key":"native.amount","label":"금액","value":"100","norm":100,"type":"amount","page":0,"bbox":[10,10,50,25]}]}
    b=Builder.__new__(Builder);b.buf=[];b.conditions=[("clean",1)];b.render_doc=lambda did,p,seed,stem,cond:fake(did,seed)
    b.bundle(sid,7)
    result=run({"id":sid,"docs":docs,"sampling":sampling,"processing":processing},7,lambda did,seed,extra:fake(did,seed))
    assert result["selections"]==b.buf[-1]["selections"]
    assert b.buf[-1]["docs"][0]["doc_id"]=="hana_official_049"
    assert b.buf[0]["answer"][0]["key"]=="native.amount"
    assert next(r for r in result["rows"] if r["id"]=="amount")["status"]=="ready"
    no_mapping=copy.deepcopy(processing);no_mapping["operations"][0]["left"].pop("keys")
    result=run({"id":sid,"docs":docs,"sampling":sampling,"processing":no_mapping},7,lambda did,seed,extra:fake(did,seed))
    assert next(r for r in result["rows"] if r["id"]=="amount")["status"]=="skipped"


def test_marks_and_checks_can_move_and_change_presence(tmp_path,monkeypatch):
    from docgen.image import ImageRenderer

    monkeypatch.setattr(HR,"ROOT",tmp_path/"regions")
    spec=R.load_all()["loan_application"];p=make_profile(3)
    original,raw,_=render(spec,p,3)
    present=next(f for f in raw if f.get("type") in ("seal","signature") and f.get("present"))
    checkbox=next(f for f in raw if f.get("type")=="checkbox" and f.get("options"))
    conf={"regions":[{"target":"mark","key":present["key"],"present":False,"page":0,"rect":[30,30,80,80]},
                     {"target":"mark","key":"sign.added1","mark_type":"signature","source":"profile.person.name","present":True,"page":0,"rect":[100,30,240,70]},
                     {"target":"box","key":checkbox["key"],"option":0,"page":0,"rect":[270,30,285,45]}]}
    with HR.draft(spec.id,conf):html,changed,_=render(spec,p,3)
    with ImageRenderer(scale=1) as renderer:info=renderer.render(html,tmp_path/"page.png")
    fields=build_fields(changed,info)
    assert next(f for f in fields if f["key"]==present["key"])["present"] is False
    sign=next(f for f in fields if f["key"]=="sign.added1")
    assert sign["present"] is True and sign["bbox"]==pytest.approx([100,30,240,70],abs=.5)
    box=next(x for x in info["boxes"] if x["key"]==checkbox["key"]+"#0")
    assert box["bbox"]==pytest.approx([270,30,285,45],abs=.5)
    assert any(a["target"]=="mark" for a in info["anchors"])
