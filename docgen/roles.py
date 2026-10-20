"""제출 서류의 역할과 실제 서식 변형. 역할은 필드 스키마의 호환성을 뜻하지 않는다."""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

PATH = Path(__file__).with_name("document_roles.json")


def catalog() -> list[dict]:
    from .registry import load_all

    reg = load_all()
    rows = json.loads(PATH.read_text(encoding="utf-8"))["roles"] if PATH.exists() else []
    used = set()
    out = []
    for row in rows:
        members = [d for d in row["forms"] if d in reg]
        used.update(members)
        if members:
            out.append({**row, "forms": members})
    # 아직 대응본이 없는 서식도 독립 역할로 선택 가능하다.
    for did, spec in reg.items():
        if did not in used:
            if spec.template.startswith("@form/"):
                from .htmlform import load_form, form_dir

                parent = load_form(did).get("parent") if form_dir(did) else None
                role = next((r for r in out if parent in r["forms"]), None)
                if role:
                    role["forms"].append(did)
                    continue
            out.append({"id": did, "name": spec.name, "forms": [did]})
    return out


def index() -> dict[str, dict]:
    return {did: row for row in catalog() for did in row["forms"]}


def validate_sampling(docs: list[str], value: dict | None) -> dict:
    value={} if value is None else value
    if not isinstance(value,dict) or set(value)-set(docs):
        raise ValueError("샘플링 설정은 시나리오의 제출 역할에만 지정하세요")
    roles=index();out={}
    for slot,config in value.items():
        if not isinstance(config,dict) or set(config)-{"mode","forms","weights"} or config.get("mode") not in ("fixed","sample"):
            raise ValueError("제출 역할의 고정/샘플링 설정이 잘못되었습니다")
        forms=config.get("forms",[slot])
        if not isinstance(forms,list) or not forms or any(not isinstance(d,str) or d not in roles[slot]["forms"] for d in forms) or len(set(forms))!=len(forms):
            raise ValueError(f"{slot}: 같은 역할의 후보 서식을 하나 이상 선택하세요")
        if config["mode"]=="fixed" and forms!=[slot]:
            raise ValueError("고정 모드는 기준 서식 하나를 사용합니다")
        weights=config.get("weights",{})
        if not isinstance(weights,dict) or set(weights)-set(forms) or any(type(w) not in (int,float) or not math.isfinite(w) or w<=0 for w in weights.values()):
            raise ValueError("후보 가중치는 양수여야 합니다")
        out[slot]={"mode":config["mode"],"forms":list(forms),"weights":dict(weights)}
    return out


def resolve(docs: list[str], sampling: dict | None, seed: int, scenario: str) -> list[dict]:
    from .registry import load_all
    reg=load_all()
    if not isinstance(docs,list) or not docs or any(not isinstance(d,str) or d not in reg for d in docs):
        raise ValueError("묶음에 등록된 서류를 하나 이상 넣으세요")
    roles=index();config=validate_sampling(docs,sampling);out=[];used=set()
    for slot in docs:
        role=roles[slot]
        if role["id"] in used:raise ValueError("같은 제출 역할의 서식은 한 자리만 넣으세요")
        used.add(role["id"])
        conf=config.get(slot,{"mode":"fixed","forms":[slot]})
        did=slot if conf["mode"]=="fixed" else random.Random(f"role-form:{scenario}:{seed}:{role['id']}").choices(conf["forms"],weights=[conf.get("weights",{}).get(d,1) for d in conf["forms"]])[0]
        out.append({"slot":slot,"role":role["id"],"role_name":role["name"],"id":did,"name":reg[did].name,"mode":conf["mode"]})
    return out


def resolve_processing(processing: dict, selections: list[dict]) -> dict:
    out=json.loads(json.dumps(processing));mapping={r["slot"]:r["id"] for r in selections}
    for op in out.get("operations",[]):
        for side in ("left","right"):
            if side not in op:continue
            ref=op[side];slot=ref["doc"];did=mapping.get(slot,slot)
            ref["key"] = ref.get("keys",{}).get(did,ref["key"] if slot==did else "__unmapped_variant__")
            ref["doc"]=did
            ref.pop("keys",None)
    return out


