"""값 출처·좌표 수정이 이미지와 정답, 생성 경로까지 함께 바꾸는 회귀 검사."""
import json

import pytest

from docgen import html_regions as HR
from docgen.tests.sandbox import forms_sandbox
from docgen.entities import make_profile
from docgen.registry import load_all
from docgen.render import render
from docgen.schema import build_fields


def test_invalid_sources_and_duplicate_occurrences():
    for rows in ([{"key":"x","source":"profile.no_such_path"}],
                 [{"key":"x","rect":[0,0,5,0],"page":0}],
                 [{"key":"x"},{"key":"x"}],
                 [{"key":"x","font_size":float("nan")}],
                 [{"key":"x","source":"rule:guess"}]):
        with pytest.raises(ValueError):
            HR.validate({"regions":rows})


def test_binding_and_addition_preserve_original(tmp_path, monkeypatch):
    forms_sandbox(monkeypatch,tmp_path,"gov_income")
    spec=load_all()["gov_income"]
    p=make_profile(7)
    html,raw,_=render(spec,p,7)
    config={"regions":[{"key":"official.name","source":"rule:fixed","text":"영역 검증","page":0,"rect":[80,80,180,100]},
                       {"key":"added.test","source":"profile.person.mobile","label":"연락처","page":0,"rect":[80,110,240,130]}]}
    with HR.draft(spec.id,config):
        changed,after,_=render(spec,p,7)
    assert next(f for f in after if f["key"]=="official.name")["value"]=="영역 검증"
    assert next(f for f in after if f["key"]=="added.test")["value"]==p.person.mobile
    from docgen.bench.perturb import visible_keys
    assert "added.test" in visible_keys(changed)
    assert HR.load(spec.id)=={"regions":[]}   # 미리보기 초안은 파일에 쓰지 않는다
    assert render(spec,p,7)[0]==html


def test_amount_cell_does_not_use_person_name():
    import random
    from docgen.realform import build_form

    d=build_form("hf055",make_profile(0),random.Random(0))
    values=[i for i in d["items"] if i.get("label")=="본인"]
    assert values and all(i["unit"]=="백만원" and float(i["value"].replace(",",""))<1000 for i in values)


def test_units_normalize_to_won():
    a,b=build_fields([{"key":"amount","label":"금액","value":"12.5","unit":"백만원"},
                      {"key":"amount2","label":"금액","value":"12,500,000","unit":"원"}])
    assert a["value"]=="12.5" and a["norm"]==12500000 and b["norm"]==12500000


def test_actual_image_placement_and_extraction(tmp_path,monkeypatch):
    from docgen.image import ImageRenderer

    forms_sandbox(monkeypatch,tmp_path,"gov_income")
    spec=load_all()["gov_income"]
    config={"regions":[{"key":"official.name","occurrence":0,"source":"rule:fixed","text":"영역 검증","page":0,"rect":[60,80,200,105]},
                       {"key":"added.test","source":"profile.person.mobile","label":"연락처","page":0,"rect":[60,115,250,140]}]}
    with HR.draft(spec.id,config):
        html,raw,_=render(spec,make_profile(7),7)
    with ImageRenderer(scale=1) as r:
        info=r.render(html,tmp_path/"page.png")
    fields=build_fields(raw,info)
    name=next(f for f in fields if f["key"]=="official.name")
    assert name["value"]=="영역 검증" and 59 <= name["bbox"][0] <= 62 and 80<=name["bbox"][1]<=105
    added=next(f for f in fields if f["key"]=="added.test")
    assert added["bbox"] and added["value"]==make_profile(7).person.mobile
    HR.save(spec.id,config)
    saved=json.loads(HR.path(spec.id).read_text(encoding="utf-8"))   # 칸 목록 fields.json (값 선언 fields 와 함께)
    assert saved["engine"]=="html" and saved["regions"]==config["regions"] and saved["fields"]
