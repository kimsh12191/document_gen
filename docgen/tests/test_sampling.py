"""두 단계 샘플링의 재현성·키 연결·실제 이미지/정답 일치."""

import pytest

from docgen import registry as R
from docgen import template_variants as T
from docgen import html_regions as HR
from docgen import regions
from docgen.tests.sandbox import forms_sandbox
from docgen.entities import make_profile
from docgen.render import render
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
    forms_sandbox(monkeypatch,tmp_path,"employment_certificate")   # 레이아웃 변형 없이 복사
    T.add("employment_certificate","letter_copy","회사별 양식")
    cfg=T.load("employment_certificate");cfg["mode"]="fixed";cfg["fixed"]="letter_copy"
    T.save("employment_certificate",cfg)
    assert T.choose(R.load_all()["employment_certificate"],42,{})["id"]=="letter_copy"
    assert HR.path("employment_certificate","letter_copy")==HR.path("employment_certificate")   # 변형도 같은 파일의 variants 칸
    row={"key":"x","source":"rule:fixed","text":"변형","page":0,"rect":[10,10,50,20]}
    HR.save("employment_certificate",{"regions":[row]},"letter_copy")
    assert HR.load("employment_certificate","letter_copy")=={"regions":[row]} and HR.load("employment_certificate")=={"regions":[]}
    assert regions.read("employment_certificate")=={"variants":{"letter_copy":{"regions":[row]}}}
    with pytest.raises(ValueError):HR.path("employment_certificate","no_such_layout")
    for bad in ("../outside","UPPER","default"):
        with pytest.raises(ValueError):T.add("employment_certificate",bad,"잘못된 ID")
    cfg["variants"][1]["weight"]=float("nan")
    with pytest.raises(ValueError):T.save("employment_certificate",cfg)


def test_marks_and_checks_can_move_and_change_presence(tmp_path,monkeypatch):
    from docgen.image import ImageRenderer

    forms_sandbox(monkeypatch,tmp_path,"loan_application")
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
