"""④ 서류 넣기 ❸ 반영 (studio/DESIGN.md 15.3·15.5): 정한 건·업무(intake_cases)로 시나리오 변경안을 계산하고, 고른 변경안·새 서식·원본 데이터를
한 번에 반영한다. 반영 전에는 서식·시나리오 파일을 바꾸지 않는다.

  proposals(묶음)        업무마다 변경안 [{id, kind, …, count, of, default}]
     add_required  업무 안 건 70% 이상에 나오는데 시나리오에 없는 서류 → 필수로
     add_optional  20~70% → 선택 서류로 (시나리오의 "optional", 구비 검사에서 필수가 아님)
     to_optional   필수인데 20~70% (건이 MIN_CASES 이상일 때만) → 선택으로     기본 꺼짐
     remove        필수인데 20% 미만 (건이 MIN_CASES 이상일 때만) → 빼기       기본 꺼짐
     sampling      자리의 실제 서식이 기준 서식과 다르거나 여럿 → 후보 서식·가중치(나온 건 수)
     compare       같은 공통 키가 한 건의 두 서류에 70% 이상 함께 나옴 → 기준 서류 ↔ 다른 서류 같다 비교 (공통 키마다 한 줄)
     new_scenario  기존 시나리오에 안 맞는 건 묶음(새 업무 후보, 건 NEW_MIN 이상) → 새 시나리오 초안 (필수 70%↑, 선택 20~70%)
     unmatched     그보다 적은 새 업무 후보 (반영하지 않음, 건을 손으로 옮기라는 표시)
  apply(묶음, …)         ❷에서 '서식으로'를 켠 새 서식 등록(지운 배경 + 값 칸) → 시나리오 변경안 → 원본 데이터 내보내기

  python -m studio.intake_plan <묶음 폴더> [--compare <다른 묶음 폴더>]   변경안 (두 묶음의 변경안이 같은지)
"""
from __future__ import annotations

import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

from . import importer as IM
from . import intake_cases as IC

REQUIRED = 0.7
OPTIONAL = 0.2
MIN_CASES = 5        # 필수를 낮추거나 빼자는 제안은 건이 이만큼 이상일 때만 (적으면 우연히 빠진 것과 구분이 안 됨)
MIN_COUNT = 2       # 시나리오에 더하자는 서류는 건 둘 이상에 나와야 (한 건에만 끼어 있는 것은 우연)
NEW_MIN = 3         # 새 시나리오 초안은 건이 이만큼 이상인 새 업무 후보만
COMPARE_PARTIES = {"customer", "corp", "family", "agent", "related", "employer"}


def _scenario_file() -> dict:
    from docgen.registry import SCENARIOS_JSON

    return json.loads(SCENARIOS_JSON.read_text(encoding="utf-8")) if SCENARIOS_JSON.exists() else {"scenarios": []}


def _case_facts(batch: dict, fx: dict) -> tuple[dict, dict, dict]:
    """건 → {역할: 서식}, 건 → {공통 키: {역할}}, 역할 → 이름."""
    from docgen import dictionary as DIC

    from .intake_raw import KeyMapper

    from docgen.registry import load_all

    reg = load_all()
    forms = IC.doc_forms(fx)
    keymaps = {f["id"]: (f.get("intake") or {}).get("keymap") or {} for f in fx["formats"]}
    roles: dict[str, dict] = defaultdict(dict)
    keys: dict[str, dict] = defaultdict(lambda: defaultdict(set))
    names, mappers = {}, {}
    for cid, c in batch["cases"]["cases"].items():
        for d in c["docs"]:
            fr = forms.get(d) or {}
            role = fr.get("role")
            if not role:
                continue
            names[role] = reg[fr["form"]].name if fr["form"] else fr["name"]
            roles[cid].setdefault(role, fr["form"] or role)
            form = fr["form"]
            dt = DIC.doc_type_of(form) if form else None
            if form and form not in mappers:
                mappers[form] = KeyMapper(form, keymaps[fr["format"]])
            for it in IC._pred_items(batch, d):
                if form:
                    fk = mappers[form](it["key"])
                    ck = DIC.common_key(dt, fk)
                else:
                    km = keymaps[fr["format"]]
                    ck = km[it["key"]] if it["key"] in km else DIC.match_extracted(it["key"])
                if ck and DIC.resolve(ck)["party"] in COMPARE_PARTIES:
                    keys[cid][ck].add(role)
    return roles, keys, names


def proposals(bdir: Path) -> dict:
    from docgen import dictionary as DIC
    from docgen.registry import SCENARIOS, load_all
    from docgen.roles import index

    batch, _, fx = IC._load(bdir)
    if not batch.get("cases"):
        IC.infer(bdir)
        batch, _, fx = IC._load(bdir)
    reg, rindex = load_all(), index()
    roles, keys, names = _case_facts(batch, fx)
    names.update({r["id"]: reg[r["id"]].name if r["id"] in reg else r["name"] for r in rindex.values()})
    by_task: dict[str, list[str]] = defaultdict(list)
    for cid, c in batch["cases"]["cases"].items():
        by_task[c["scenario"] or f"new:{c['new']}"].append(cid)
    sfile = {s["id"]: s for s in _scenario_file()["scenarios"]}
    common = DIC.load("common").get("keys", {})
    will_form = {f"new:{f['id']}" for f in fx["formats"] if (f.get("intake") or {}).get("kind") == "new"
                 and ((f["intake"].get("uses") or {}).get("template"))}
    usable = lambda r: not r.startswith("new:") or r in will_form  # noqa: E731   원본 데이터로만 쓰는 새 양식은 서식이 되지 않는다
    out = []
    for task, cids in sorted(by_task.items()):
        n = len(cids)
        sc = None if task.startswith("new:") else task
        role_cnt = Counter(r for c in cids for r in roles.get(c, {}))
        form_cnt: dict[str, Counter] = defaultdict(Counter)
        for c in cids:
            for r, f in roles.get(c, {}).items():
                form_cnt[r][f] += 1
        changes = []

        def ch(kind, default=True, **kw):
            ident = ":".join([task, kind, *(str(kw[k]) for k in ("role", "key") if k in kw)])
            changes.append({"id": ident, "kind": kind, "default": default, "of": n, **kw})

        def role_form(r):
            return form_cnt[r].most_common(1)[0][0]

        if sc:
            slots = SCENARIOS[sc][1]
            slot_of = {rindex[d]["id"]: d for d in slots if d in rindex}
            optional = set(sfile.get(sc, {}).get("optional", []))
            opt_roles = {rindex[d]["id"] for d in optional if d in rindex}
            for r, k in role_cnt.most_common():
                if r in slot_of or not usable(r) or k < MIN_COUNT:
                    continue
                share = k / n
                if share >= REQUIRED:
                    ch("add_required", role=r, role_name=names.get(r, r), form=role_form(r), count=k)
                elif share >= OPTIONAL and r not in opt_roles:
                    ch("add_optional", role=r, role_name=names.get(r, r), form=role_form(r), count=k)
            for r, slot in slot_of.items():
                k = role_cnt.get(r, 0)
                if n >= MIN_CASES and k / n < OPTIONAL:
                    ch("remove", default=False, role=r, role_name=names.get(r, r), form=slot, count=k)
                elif n >= MIN_CASES and k / n < REQUIRED:
                    ch("to_optional", default=False, role=r, role_name=names.get(r, r), form=slot, count=k)
                seen = {f: c for f, c in form_cnt[r].items() if f in reg}
                cur = (sfile.get(sc, {}).get("sampling") or {}).get(slot)
                cur_forms = set(cur["forms"]) if cur and cur.get("mode") == "sample" else {slot}
                if seen and set(seen) - cur_forms:
                    forms = sorted(set(seen) | cur_forms, key=lambda f: -seen.get(f, 0))
                    ch("sampling", role=r, role_name=names.get(r, r), slot=slot, forms=forms,
                       weights={f: seen.get(f, 0) or 1 for f in forms}, count=sum(seen.values()))
            ops = (sfile.get(sc, {}).get("processing") or {}).get("operations", [])
            have = {(o["left"].get("doc"), o["right"].get("doc"), o["left"].get("common")) for o in ops
                    if o.get("kind") == "compare" and o.get("left", {}).get("common")}
            in_slots = lambda r: r in slot_of  # noqa: E731
        elif n < NEW_MIN or not [r for r, k in role_cnt.items() if usable(r) and k / n >= REQUIRED]:   # 건이 적거나 필수가 없는 새 업무 후보는 시나리오로 만들지 않고 '어디에도 안 맞는 건'으로만 보인다
            ch("unmatched", default=False, cases=cids, count=n, roles=[names.get(r, r) for r in role_cnt])
            slot_of, have = {}, set()
            in_slots = lambda r: False  # noqa: E731
        else:
            req = [(r, k) for r, k in role_cnt.most_common() if usable(r) and k / n >= REQUIRED]
            opt = [(r, k) for r, k in role_cnt.most_common() if usable(r) and k >= MIN_COUNT and OPTIONAL <= k / n < REQUIRED]
            ch("new_scenario", name=task[4:], cases=n,
               required=[{"role": r, "role_name": names.get(r, r), "form": role_form(r), "count": k} for r, k in req],
               optional=[{"role": r, "role_name": names.get(r, r), "form": role_form(r), "count": k} for r, k in opt],
               count=n)
            slot_of, have = {r: role_form(r) for r, _ in req}, set()
            in_slots = lambda r: r in slot_of  # noqa: E731
        # 비교: 공통 키마다 기준 서류(그 키가 가장 많은 건에 나오는 자리) ↔ 다른 자리
        key_roles: dict[str, Counter] = defaultdict(Counter)
        pair: dict[tuple, int] = Counter()
        for c in cids:
            for ck, rs in keys.get(c, {}).items():
                rs = sorted(r for r in rs if in_slots(r))
                for r in rs:
                    key_roles[ck][r] += 1
                for i, a in enumerate(rs):
                    for b in rs[i + 1:]:
                        pair[(ck, a, b)] += 1
        for ck, rc in sorted(key_roles.items()):
            if len(rc) < 2:
                continue
            anchor = max(rc, key=lambda r: (rc[r], -list(slot_of).index(r) if r in slot_of else 0))
            pairs = []
            for r in sorted(rc, key=lambda r: list(slot_of).index(r)):
                if r == anchor:
                    continue
                k = pair[(ck, *sorted((anchor, r)))]
                if k / n >= REQUIRED and (slot_of[anchor], slot_of[r], ck) not in have:
                    pairs.append({"role": r, "role_name": names.get(r, r), "count": k})
            if pairs:
                ch("compare", key=ck, key_name=(common.get(ck) or {}).get("name", ck), anchor=anchor,
                   anchor_name=names.get(anchor, anchor), pairs=pairs, count=max(p["count"] for p in pairs))
        out.append({"task": task, "scenario": sc, "name": SCENARIOS[sc][0] if sc else task[4:], "cases": n,
                    "sure_cases": sum(1 for c in cids if batch["cases"]["cases"][c]["sure"]), "changes": changes})
    out.sort(key=lambda t: (t["scenario"] is None, -t["cases"]))
    return {"basis": batch["cases"]["basis"], "tasks": out}


def signature(p: dict) -> set:
    """변경안을 묶음과 상관없이 견줄 꼴 (건 ID·새 업무 이름·모양 ID 를 빼고, 새 서식 역할은 이름으로)."""
    def role(r, nm):
        return f"new:{nm}" if str(r).startswith("new:") else r

    out = set()
    for t in p["tasks"]:
        for c in t["changes"]:
            if c["kind"] == "unmatched":   # 반영할 변경이 아니라 손으로 옮길 건 목록
                continue
            if c["kind"] == "new_scenario":
                out.add(("new_scenario", tuple(sorted(role(x["role"], x["role_name"]) for x in c["required"])),
                         tuple(sorted(role(x["role"], x["role_name"]) for x in c["optional"]))))
            elif c["kind"] == "compare":
                out.add((t["scenario"], "compare", c["key"], role(c["anchor"], c["anchor_name"]),
                         tuple(sorted(role(x["role"], x["role_name"]) for x in c["pairs"]))))
            elif c["kind"] == "sampling":
                out.add((t["scenario"], "sampling", c["role"], tuple(c["forms"])))
            else:
                out.add((t["scenario"], c["kind"], role(c["role"], c["role_name"])))
    return out


# ---------------------------------------------------------------------------
# 반영
# ---------------------------------------------------------------------------

def _form_id(batch: str, fmt: str, name: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "_", f"{batch}_{fmt}".lower()).strip("_")[:34] or "form"
    return f"img_{base}"


def register_new_forms(bdir: Path, private_dir: str | None, only: set[str] | None = None) -> list[dict]:
    """❷에서 '새 서식'·'서식으로'를 켠 모양을 overlay 서식으로: 견본 쪽 그림 + 지울 자리(추출값·남은 값 후보) + 값 칸(추출값 위치, 키는
    이은 공통 키 또는 추출 키). 미검수 서식이라 영역 편집기에서 확인해야 데이터셋에 들어간다(8.5). 결정에 form_id 를 남긴다."""
    from docgen import realform as RF

    from .intake_judge import draft

    batch, _, fx = IC._load(bdir)
    out = []
    for f in fx["formats"]:
        d = f.get("intake") or {}
        if d.get("kind") != "new" or not (d.get("uses") or {}).get("template") or d.get("form_id") or (only is not None and f["id"] not in only):
            continue
        dr = draft(bdir, f["id"])
        fid = _form_id(batch["name"], f["id"], d.get("name") or f["name"])
        res = IM.create_template(bdir, f["id"], dr["pages"], fid, d.get("name") or f["name"], private_dir, drafts=False)
        to_pt = lambda r: [round(v / RF.BG_ZOOM, 2) for v in r]  # noqa: E731
        erase, add, keys = [], [], set()
        for g in [*dr["regions"], *dr["leftover"]]:
            pad = max(1.5, 0.12 * (g["rect"][3] - g["rect"][1]))
            erase.append({"page": g["page"], "rect": to_pt([g["rect"][0] - pad, g["rect"][1] - pad, g["rect"][2] + pad, g["rect"][3] + pad]),
                          "fill": "auto"})
        for g in dr["regions"]:
            if g["type"] not in ("text", None) or g["key"] in keys:
                continue
            key = g.get("common") or g["key"]
            keys.add(g["key"])
            add.append({"t": "text", "page": g["page"], "label": g.get("label") or g["key"], "rect": to_pt(g["rect"]), "key": key})
        for g in dr["leftover"]:
            add.append({"t": "text", "page": g["page"], "label": g.get("label") or "값", "rect": to_pt(g["rect"]), "note": "남은 값 후보"})
        Path(res["dir"], "overrides.json").write_text(json.dumps({"erase": erase, "add": add}, ensure_ascii=False, indent=1) + "\n",
                                                      encoding="utf-8")
        _set_intake(bdir, f["id"], form_id=fid)
        out.append({"format": f["id"], "form_id": fid, "name": d.get("name") or f["name"], "dir": res["dir"], "private": res["private"],
                    "slots": len(add), "erase": len(erase)})
    if out:
        RF.register_images()
    return out


def _set_intake(bdir: Path, fid: str, **kw) -> None:
    fx = json.loads((bdir / "formats.json").read_text(encoding="utf-8"))
    for f in fx["formats"]:
        if f["id"] == fid:
            f["intake"] = {**(f.get("intake") or {}), **kw}
    IM._write_json(bdir / "formats.json", fx)


def apply_scenarios(plan: dict, selected: set[str], names: dict[str, dict] | None = None) -> dict:
    """고른 변경안을 시나리오 목록에 반영해 저장 (studio/bank_data.save_scenarios_list 의 검사를 그대로 거친다).
    names = {새 업무 변경안 id: {id, name}}. 등록되지 않은 새 서식 역할(new:…)은 시나리오에 넣지 못해 건너뛴다."""
    from docgen.registry import load_all

    from . import bank_data as BD

    reg = load_all()
    data = _scenario_file()["scenarios"]
    by = {s["id"]: s for s in data}
    done, skipped = [], []
    ok = lambda f: f in reg  # noqa: E731
    for t in plan["tasks"]:
        for c in t["changes"]:
            if c["id"] not in selected or c["kind"] == "unmatched":
                continue
            s = by.get(t["scenario"]) if t["scenario"] else None
            k = c["kind"]
            if k in ("add_required", "add_optional", "to_optional", "remove") and not ok(c["form"]):
                skipped.append({"id": c["id"], "why": "등록되지 않은 서식"})
                continue
            if k == "add_required":
                s["docs"].append(c["form"])
                if c["form"] in s.get("optional", []):
                    s["optional"].remove(c["form"])
            elif k == "add_optional":
                s.setdefault("optional", []).append(c["form"])
            elif k in ("to_optional", "remove"):
                s["docs"].remove(c["form"])
                (s.get("sampling") or {}).pop(c["form"], None)
                if k == "to_optional":
                    s.setdefault("optional", []).append(c["form"])
            elif k == "sampling":
                s.setdefault("sampling", {})[c["slot"]] = {"mode": "sample", "forms": [f for f in c["forms"] if ok(f)],
                                                          "weights": {f: w for f, w in c["weights"].items() if ok(f)}}
            elif k == "compare":
                p = s.setdefault("processing", {})
                ops = p.setdefault("operations", [])
                slot = {r: f for r, f in ((x, next((d for d in s["docs"] if _role(d) == x), None)) for x in
                                          [c["anchor"], *(q["role"] for q in c["pairs"])])}
                for q in c["pairs"]:
                    a, b = slot.get(c["anchor"]), slot.get(q["role"])
                    if not a or not b:
                        continue
                    oid = re.sub(r"[^A-Za-z0-9_-]", "_", f"cmp_{c['key']}_{a}_{b}")[:80]
                    if oid not in {o["id"] for o in ops}:
                        ops.append({"id": oid, "kind": "compare", "name": f"{c['key_name']}: {c['anchor_name']} ↔ {q['role_name']}",
                                    "enabled": True, "left": {"doc": a, "common": c["key"], "key": c["key"]},
                                    "right": {"doc": b, "common": c["key"], "key": c["key"]}, "operator": "equal"})
            elif k == "new_scenario":
                nm = (names or {}).get(c["id"]) or {}
                docs = [x["form"] for x in c["required"] if ok(x["form"])]
                if not docs:
                    skipped.append({"id": c["id"], "why": "필수 서류 중 등록된 서식이 없음"})
                    continue
                sid = nm.get("id") or f"intake_{len(data) + 1}"
                s = {"id": sid, "name": nm.get("name") or c["name"], "docs": docs,
                     **({"optional": o} if (o := [x["form"] for x in c["optional"] if ok(x["form"])]) else {})}
                data.append(s)
                by[sid] = s
            done.append(c["id"])
    if done:
        BD.save_scenarios_list(data)
    return {"applied": done, "skipped": skipped}


def _role(form: str) -> str | None:
    from docgen.roles import index

    r = index().get(form)
    return r["id"] if r else None


def apply(bdir: Path, real_root: Path, private_dir: str | None, selected: list[str] | None = None, names: dict | None = None,
          forms: bool = True, raw: bool = True, ratio: float | None = None) -> dict:
    """❸ 반영: 새 서식 등록 → (등록된 서식으로) 변경안 다시 계산 → 고른 변경안(없으면 기본으로 켠 것) → 원본 데이터 내보내기."""
    from .intake_raw import export

    out: dict = {"at": time.strftime("%Y-%m-%d %H:%M")}
    if forms:
        out["forms"] = register_new_forms(bdir, private_dir)
        if out["forms"]:
            IC.infer(bdir, IC._load(bdir)[0]["cases"]["basis"] if IC._load(bdir)[0].get("cases") else None)
    plan = proposals(bdir)
    sel = set(selected) if selected is not None else {c["id"] for t in plan["tasks"] for c in t["changes"] if c["default"]}
    out["scenarios"] = apply_scenarios(plan, sel, names)
    if raw:
        out["raw"] = export(bdir, real_root, ratio)
    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    batch.setdefault("applied", []).append({k: (v if k != "raw" else {"root": v["root"], "splits": {s: x["documents"] for s, x in v["splits"].items()}})
                                            for k, v in out.items()})
    batch["stage"] = "applied"
    IM._write_json(bdir / "batch.json", batch)
    return out


def main(argv=None) -> None:
    import argparse

    ap = argparse.ArgumentParser(prog="python -m studio.intake_plan", description=__doc__.split("\n")[0])
    ap.add_argument("batch")
    ap.add_argument("--compare")
    a = ap.parse_args(argv)
    p = proposals(Path(a.batch))
    for t in p["tasks"]:
        print(f"{t['name']} ({t['task']}) 건 {t['cases']} (확실 {t['sure_cases']})")
        for c in t["changes"]:
            print(f"   {'☑' if c['default'] else '☐'} {c['kind']} {c.get('role_name') or c.get('key_name') or ''} {c.get('count')}/{c['of']}")
    if a.compare:
        q = proposals(Path(a.compare))
        sa, sb = signature(p), signature(q)
        print(json.dumps({"same": sa == sb, "only_first": sorted(map(str, sa - sb)), "only_second": sorted(map(str, sb - sa))},
                         ensure_ascii=False, indent=1))
    sys.exit(0)


if __name__ == "__main__":
    main()
