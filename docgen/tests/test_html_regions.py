"""값 출처·좌표 수정이 이미지와 정답, 생성 경로까지 함께 바꾸는 회귀 검사."""
import json

import pytest

from docgen import html_regions as HR
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
    monkeypatch.setattr(HR,"ROOT",tmp_path)
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
    assert not HR.path(spec.id).exists()
    assert render(spec,p,7)[0]==html


def test_role_membership_and_distinct_scopes():
    from docgen.roles import catalog,index

    rows=catalog();idx=index()
    members=[did for r in rows for did in r["forms"]]
    assert len(members)==len(set(members))==len(load_all())
    assert idx["loan_application"]["id"]==idx["hana_official_049"]["id"]==idx["hf049"]["id"]
    assert idx["balance_certificate"]["id"]!=idx["hana_official_011"]["id"]
    assert idx["pension_enrollment_certificate"]["id"]!=idx["gov_pension"]["id"]
    assert idx["tax_payment_certificate_corp"]["id"]!=idx["gov_national_tax"]["id"]


def test_amount_cell_does_not_use_person_name():
    import random
    from docgen.realform import build_form

    d=build_form("hf055",make_profile(0),random.Random(0))
    values=[i for i in d["items"] if i.get("label")=="본인"]
    assert values and all(i["unit"]=="백만원" and float(i["value"].replace(",",""))<1000 for i in values)


def test_units_compare_in_won_and_role_selection_is_saved(monkeypatch):
    from docgen.bench.processing import compare
    from studio import bank_data

    a,b=build_fields([{"key":"amount","label":"금액","value":"12.5","unit":"백만원"},
                      {"key":"amount2","label":"금액","value":"12,500,000","unit":"원"}])
    assert a["value"]=="12.5" and a["norm"]==12500000
    assert compare(a,b,"equal") is True
    saved=[]
    monkeypatch.setattr(bank_data,"save_scenarios",lambda rows:saved.extend(rows))
    bank_data.save_scenarios_list([{"id":"role_selection_test","docs":["hana_official_049"],"name":"대출 신청"}])
    assert saved[0]["docs"]==["hana_official_049"]
    with pytest.raises(ValueError,match="같은 제출 역할"):
        bank_data.save_scenarios_list([{"id":"role_duplicate_test","docs":["loan_application","hana_official_049"]}])


def test_actual_image_placement_and_extraction(tmp_path,monkeypatch):
    from docgen.image import ImageRenderer
    from docgen.bench.processing import execute,validate

    monkeypatch.setattr(HR,"ROOT",tmp_path/"regions")
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
    conf=validate({"operations":[{"id":"phone","kind":"extract","left":{"doc":spec.id,"key":"added.test"}}]},[spec.id])
    result=execute(conf,{spec.id:{"name":spec.name,"fields":fields,"pages":info["pages"]}})
    assert result[0]["status"]=="ready" and result[0]["item"]["answer"][0]["value"]==added["value"]
    HR.save(spec.id,config)
    assert json.loads(HR.path(spec.id).read_text(encoding="utf-8"))==config
