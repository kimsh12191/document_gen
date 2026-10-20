"""같은 서식·같은 생성값에 여러 HTML 레이아웃. 선택은 seed로 재현한다."""
from __future__ import annotations

import json
import math
import random
import re
from pathlib import Path

ROOT = Path(__file__).parent / "templates" / "variants"
RX = re.compile(r"[a-z][a-z0-9_]{0,50}")


def folder(doc_id):
    from .registry import load_all
    from .htmlform import form_dir, COPIES

    spec=load_all()[doc_id]
    if spec.template == "_real_form.html.j2":
        raise ValueError("HTML 서식의 레이아웃 변형 기능입니다")
    d=form_dir(doc_id)
    return d/"variants" if d and not d.is_relative_to(COPIES) else ROOT/doc_id


def load(doc_id):
    p=folder(doc_id)/"variants.json"
    return validate(json.loads(p.read_text(encoding="utf-8"))) if p.exists() else {"mode":"sample","fixed":"default","variants":[{"id":"default","name":"기본 레이아웃","weight":1,"enabled":True}]}


def validate(config):
    if not isinstance(config,dict) or set(config)-{"mode","fixed","variants"} or config.get("mode") not in ("sample","fixed") or not isinstance(config.get("variants"),list):
        raise ValueError("고정/샘플링과 레이아웃 목록을 지정하세요")
    ids=set()
    for row in config["variants"]:
        if not isinstance(row,dict) or set(row)-{"id","name","weight","enabled"} or not RX.fullmatch(str(row.get("id",""))) or row["id"] in ids:
            raise ValueError("중복 없는 레이아웃 ID를 지정하세요")
        ids.add(row["id"])
        if not isinstance(row.get("name"),str) or type(row.get("enabled",True)) is not bool or type(row.get("weight",1)) not in (int,float) or not math.isfinite(row.get("weight",1)) or row.get("weight",1)<=0:
            raise ValueError("레이아웃 이름·사용 여부·양수 가중치를 지정하세요")
    if "default" not in ids or not any(r.get("enabled",True) for r in config["variants"]) or config.get("fixed") not in ids:
        raise ValueError("기본 레이아웃과 사용할 레이아웃이 필요합니다")
    if config["mode"]=="fixed" and not next(r for r in config["variants"] if r["id"]==config["fixed"]).get("enabled",True):
        raise ValueError("고정 레이아웃이 꺼져 있습니다")
    return json.loads(json.dumps(config))


def save(doc_id,config):
    config=validate(config);d=folder(doc_id)
    for row in config["variants"]:
        if row["id"]!="default" and not (d/(row["id"]+".html.j2")).exists():
            raise ValueError(f"레이아웃 파일이 없습니다: {row['id']}")
    d.mkdir(parents=True,exist_ok=True)
    p=d/"variants.json";tmp=p.with_suffix(".tmp");tmp.write_text(json.dumps(config,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");tmp.replace(p)
    return config


def source(doc_id,variant):
    if variant=="default":
        from .registry import load_all
        from .htmlform import template_source
        spec=load_all()[doc_id]
        return template_source(doc_id) if spec.template.startswith("@form/") else (Path(__file__).parent/"templates"/spec.template).read_text(encoding="utf-8")
    if not RX.fullmatch(variant) or variant not in {r["id"] for r in load(doc_id)["variants"]}:
        raise ValueError("등록되지 않은 레이아웃입니다")
    return (folder(doc_id)/(variant+".html.j2")).read_text(encoding="utf-8")


def add(doc_id,variant,name,base="default"):
    if not isinstance(variant,str) or not RX.fullmatch(variant) or variant=="default":
        raise ValueError("새 레이아웃 ID는 영문 소문자·숫자·밑줄입니다")
    config=load(doc_id)
    if variant in {r["id"] for r in config["variants"]}:
        raise ValueError("이미 있는 레이아웃입니다")
    content=source(doc_id,base);d=folder(doc_id);d.mkdir(parents=True,exist_ok=True)
    p=d/(variant+".html.j2")
    with p.open("x",encoding="utf-8") as f:f.write(content)
    config["variants"].append({"id":variant,"name":name or variant,"weight":1,"enabled":True})
    save(doc_id,config)
    return config


def choose(spec,seed,extra):
    if spec.template=="_real_form.html.j2":
        return {"id":"default","name":"PDF·이미지 배경","template":spec.template}
    from .registry import load_all
    if spec.id not in load_all():
        return {"id":"default","name":"기본 레이아웃","template":spec.template}
    config=load(spec.id)
    forced=(extra.get("template_variants") or {}).get(spec.id)
    if forced is not None:
        row=next((r for r in config["variants"] if r["id"]==forced),None)
        if row is None:raise ValueError(f"없는 레이아웃: {spec.id}/{forced}")
    elif config["mode"]=="fixed":row=next(r for r in config["variants"] if r["id"]==config["fixed"])
    else:
        candidates=[r for r in config["variants"] if r.get("enabled",True)]
        row=random.Random(f"template:{spec.id}:{seed}").choices(candidates,weights=[r.get("weight",1) for r in candidates])[0]
    return {**row,"template":spec.template if row["id"]=="default" else f"@layout/{spec.id}/{row['id']}"}


def jinja_source(name):
    if not name.startswith("@layout/"):return None
    _,did,variant=name.split("/")
    p=folder(did)/(variant+".html.j2");mtime=p.stat().st_mtime_ns
    return source(did,variant),str(p),lambda:p.exists() and p.stat().st_mtime_ns==mtime
