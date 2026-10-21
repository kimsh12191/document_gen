"""④ 서류 넣기 — 원본 데이터로 (studio/DESIGN.md 15.4): 넣은 서류의 원본 이미지 + 추출값을 표준 라벨 v1 폴더(studio/LABEL_FORMAT.md)로
내보낸다. 정답은 추출값 그대로라 `gt: pseudo`(의사정답)이고, 학습/평가는 건 단위로 나눠 두 폴더로 쓴다. 두 폴더는 그대로
④ 라벨 있는 데이터의 경로로 넣어 데이터셋(평가는 split test, 학습은 train)을 만든다.

저장 <real_data_dir>/labels/<묶음>-raw/
  train/  test/        각각 v1 폴더: meta.json(gt pseudo, model = 추출 결과를 낸 모델, split) · labels/ · images/ · ocr/(저장된 OCR 이 있으면)
                       · bundles.jsonl(업무가 등록된 시나리오이고 건이 정해진 것만)
  export.json          건 → 나뉜 쪽, 내보낸·뺀 서류와 까닭

- 내보내는 서류: ❷에서 '원본 데이터로'를 켠 모양의 서류 중 추출 결과가 있는 것. 서식 ID 는 기존 서식이면 그 서식, 새 서식은 ❸에서
  등록한 서식(결정의 form_id)이 생긴 뒤에 내보낸다(v1 은 등록된 서식만 받는다).
- 키: 그 서식에 있는 키는 그대로, 없는 키는 ❷ 잇기(또는 키 사전의 다른 이름)로 공통 키를 찾아 그 공통 키에 이은 서식 키로 바꾼다.
- 건 단위 나누기: 업무마다 건을 해시 순으로 놓고 앞 ratio 만큼을 평가로(건이 둘 이상이면 평가 하나 이상, 학습 하나 이상). 건을 모르는
  서류(구분 없는 폴더, ❸ 건 추정 전)는 서류 하나를 건 하나로 본다 — 같은 고객 서류가 양쪽에 들어갈 수 있어 경고한다.
  평가로 뺀 건의 서류는 새 서식 초안의 견본으로도 쓰지 않는다(intake_judge.draft).

  python -m studio.intake_raw <묶음 폴더> <real_data_dir> [--ratio 0.2]
  python -m studio.intake_raw <묶음 폴더> <real_data_dir> --score <시험 폴더>   내보낸 세트를 생성 정답(<시험 폴더>/gt)으로 채점
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

from . import importer as IM
from . import label_review as LR

RATIO = 0.2
MARKS = ("checkbox", "checkbox_multi", "seal", "signature")


def _load(bdir: Path):
    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    rows = {r["id"]: r for r in IM._jsonl(bdir / "pages.jsonl")}
    fx = json.loads((bdir / "formats.json").read_text(encoding="utf-8"))
    return batch, rows, fx


def out_root(real_root: Path, batch_name: str) -> Path:
    return LR.root(real_root, f"{batch_name}-raw")


# ---------------------------------------------------------------------------
# 건 단위 나누기
# ---------------------------------------------------------------------------

def case_of(batch: dict, doc: str) -> tuple[str, str | None]:
    """서류 → (업무, 건 키). 폴더·cases.csv 의 건, 없으면 ❸ 건 추정(batch["case_guess"]), 그것도 없으면 None."""
    info = batch.get("intake", {}).get("docs", {}).get(doc, {})
    sc = info.get("scenario") or "-"
    if info.get("case"):
        return sc, f"{sc}/{info['case']}"
    g = (batch.get("case_guess") or {}).get(doc)
    return ((g.get("scenario") or sc), f"guess:{g['case']}") if g else (sc, None)


def splits(batch: dict, ratio: float | None = None) -> dict[str, str]:
    """서류 → "train" | "test". 같은 건은 같은 쪽. 같은 묶음·비율이면 늘 같은 결과."""
    ratio = (batch.get("raw") or {}).get("ratio", RATIO) if ratio is None else ratio
    docs = list(batch.get("intake", {}).get("docs", {}))
    group, strata = {}, {}
    for d in docs:
        sc, case = case_of(batch, d)
        group[d] = case or f"doc:{d}"
        strata.setdefault(sc, set()).add(group[d])
    side = {}
    for sc, cases in strata.items():
        order = sorted(cases, key=lambda c: hashlib.sha1(f"{batch['name']}:{c}".encode()).hexdigest())
        n = len(order)
        k = round(n * ratio)
        if ratio > 0 and n >= 2:
            k = min(n - 1, max(1, k))
        side.update({c: "test" if i < k else "train" for i, c in enumerate(order)})
    return {d: side[group[d]] for d in docs}


def test_docs(bdir: Path) -> set[str]:
    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    return {d for d, s in splits(batch).items() if s == "test"}


def preview(bdir: Path, ratio: float | None = None) -> dict:
    """내보내기 전 미리보기: 쪽마다 서류·건 수, 내보낼 수 있는 서류와 못 내보내는 까닭, 건을 모르는 서류 수, 마지막 내보내기."""
    from docgen.registry import load_all

    batch, _, fx = _load(bdir)
    side = splits(batch, ratio)
    reg = load_all()
    ready, why = Counter(), Counter()
    has_pred = (batch.get("results") or {}).get("pred") or {}
    for f in fx["formats"]:
        d = f.get("intake")
        for doc in f["docs"]:
            if not d:
                why["양식 정리 전"] += 1
            elif d["kind"] == "skip" or not d["uses"].get("raw"):
                why["원본 데이터로를 끔"] += 1
            elif d.get("form_id") not in reg:
                why["새 서식 등록 전"] += 1
            elif doc not in has_pred:
                why["추출 결과 없음"] += 1
            else:
                ready[side[doc]] += 1
    cases = {s: len({case_of(batch, d)[1] or d for d, x in side.items() if x == s}) for s in ("train", "test")}
    return {"ratio": (batch.get("raw") or {}).get("ratio", RATIO) if ratio is None else ratio,
            "docs": dict(Counter(side.values())), "cases": cases, "ready": dict(ready), "not_ready": dict(why),
            "unknown_case": sum(1 for d in side if case_of(batch, d)[1] is None), "model": (batch.get("results") or {}).get("model"),
            "last": batch.get("raw")}


# ---------------------------------------------------------------------------
# 추출값 → v1 라벨
# ---------------------------------------------------------------------------

def _generic(k: str) -> str:
    return re.sub(r"\.\d+(?=\.|$)", "[]", k)


class KeyMapper:
    """추출 키 → 그 서식의 키. 서식에 있으면 그대로, 아니면 공통 키를 거쳐 그 공통 키에 이은(없으면 같은 당사자 값인) 서식 키 하나."""

    def __init__(self, form_id: str, keymap: dict):
        from docgen import dictionary as DIC

        self.DIC, self.keymap = DIC, keymap
        self.dt = DIC.doc_type_of(form_id)
        self.types = {k["key"]: k.get("type") or "text" for k in LR.form_keys(form_id)}
        self.by_common: dict[str, list[str]] = {}
        for fk in self.types:
            ck = DIC.common_key(self.dt, fk) or DIC.resolve(fk, self.dt)["party_key"]
            self.by_common.setdefault(ck, []).append(fk)

    def _bare(self, k: str) -> str | None:
        """역할 없이 속성만 온 키(name·phone …) → 이 서식에서 그 속성(없으면 같은 값 종류)을 가진 키가 하나면 그것.
        여럿이면 고객의 것 하나."""
        A = self.DIC.load("attributes").get("attributes", {})
        attr = next((a for a, v in A.items() if k in v.get("aliases", [])), self.DIC.merged("attribute", k))
        kind = (A.get(attr) or {}).get("kind")
        info = {fk: self.DIC.resolve(fk, self.dt) for fk in self.types}
        info = {fk: r for fk, r in info.items() if not r["sub"] and not r["mark"]}
        for pick in (lambda r: r["attribute"] == attr,
                     lambda r: kind not in (None, "text") and (A.get(r["attribute"]) or {}).get("kind") == kind):
            c = [fk for fk, r in info.items() if pick(r)]
            if len(c) > 1:
                c = [fk for fk in c if info[fk]["party"] == "customer"]
            if len(c) > 1:   # 고객 쪽 역할이 여럿(실제 소유자 등)이면 역할 이름이 고객인 것
                c = [fk for fk in c if info[fk]["role"] == "customer"]
            if len(c) == 1:
                return c[0]
        return None

    def known(self, k: str) -> bool:
        return k in self.types or _generic(k) in self.types

    def type_of(self, k: str) -> str | None:
        return self.types.get(k) or self.types.get(_generic(k))

    def __call__(self, k: str) -> str:
        if self.known(k) or not self.types:
            return k
        ck = self.keymap[k] if k in self.keymap else self.DIC.match_extracted(k, self.dt)
        if not ck:
            return (self._bare(k) if "." not in k and k not in self.keymap else None) or k
        if ck in self.types:
            return ck
        c = self.by_common.get(ck, [])
        return c[0] if len(c) == 1 else k


def v1_fields(items: list[dict], sizes: list[tuple[int, int]], km: KeyMapper) -> tuple[list[dict], list[str]]:
    """추출 결과 items (RESULTS_FORMAT.md 4절: bbox_2d 0~1000, page 1부터) → v1 fields (픽셀 bbox, page 0부터). (fields, 주의)."""
    out, notes, by_key = [], [], {}

    def where(it):
        pg = max(0, int(it.get("page", 1)) - 1)
        b = it.get("bbox_2d")
        if not b or pg >= len(sizes):
            return None, None
        W, H = sizes[pg]
        return pg, [round(b[0] * W / 1000, 1), round(b[1] * H / 1000, 1), round(b[2] * W / 1000, 1), round(b[3] * H / 1000, 1)]

    for it in items:
        key = km(it["key"])
        t = km.type_of(key) or it.get("type") or ("seal" if key.startswith("seal.") else "signature" if key.startswith("sign.") else "text")
        if it.get("type") in MARKS and t not in MARKS:
            t = it["type"]
        pg, box = where(it)
        if t in ("checkbox", "checkbox_multi"):
            f = by_key.get(key)
            if f is None:
                f = by_key[key] = {"key": key, "label": it.get("label") or key.split(".")[-1], "type": t, "value": None, "options": []}
                out.append(f)
            f["options"].append({"text": str(it.get("value")), "checked": True, **({"box_bbox": box} if box else {})})
            if pg is not None:
                f.setdefault("page", pg)
            continue
        if key in by_key:
            notes.append(f"같은 키가 두 번 나와 처음 것만 씁니다: {key}")
            continue
        f = {"key": key, "label": it.get("label") or key.split(".")[-1], "type": t}
        if t in ("seal", "signature"):
            f.update(value=None, present=bool(it.get("value")))
        else:
            v = it.get("value")
            f["value"] = None if v in (None, "") else str(v)
        if box and (f.get("value") is not None or f.get("present")):
            f.update(page=pg, bbox=box)
        by_key[key] = f
        out.append(f)
    for f in out:
        if f["type"] in ("checkbox", "checkbox_multi"):
            vals = [o["text"] for o in f["options"]]
            if len(vals) > 1:
                f["type"] = "checkbox_multi"
            f["value"] = None if f["type"] == "checkbox_multi" else vals[0]   # 복수 선택의 답은 options 의 checked (v1)
    return out, notes


# ---------------------------------------------------------------------------
# 내보내기
# ---------------------------------------------------------------------------

def export(bdir: Path, real_root: Path, ratio: float | None = None) -> dict:
    """원본 데이터로를 켠 모양의 서류를 train/ test/ 두 v1 폴더로 (전체를 새로 쓴다)."""
    from docgen.registry import SCENARIOS, load_all

    from .intake_judge import _pred

    batch, rows, fx = _load(bdir)
    ratio = (batch.get("raw") or {}).get("ratio", RATIO) if ratio is None else ratio
    side = splits(batch, ratio)
    reg = load_all()
    rt = out_root(real_root, batch["name"])
    if rt.exists():
        shutil.rmtree(rt)
    skipped: Counter = Counter()
    labels: dict[str, list[dict]] = {"train": [], "test": []}
    notes, has_ocr, n_pages = [], {"train": True, "test": True}, Counter()
    for f in fx["formats"]:
        d = f.get("intake")
        if not d:
            skipped["양식 정리 전"] += len(f["docs"])
            continue
        if d["kind"] == "skip" or not d["uses"].get("raw"):
            skipped["원본 데이터로를 끔"] += len(f["docs"])
            continue
        form_id = d.get("form_id")
        if form_id not in reg:
            skipped["새 서식 등록 전"] += len(f["docs"])
            continue
        km = KeyMapper(form_id, d.get("keymap") or {})
        for doc, pids in f["docs"].items():
            items = _pred(batch, doc)
            if not items:
                skipped["추출 결과 없음"] += 1
                continue
            s = side[doc]
            sid = LR.safe(doc)
            pr = [rows[p] for p in pids]
            fields, ns = v1_fields(items, [(r["width"], r["height"]) for r in pr], km)
            notes += [f"{doc}: {n}" for n in ns]
            imgs = []
            for k, r in enumerate(pr, 1):
                src = Path(r.get("image") or r["source"])
                rel = f"images/{sid}_p{k}{src.suffix.lower() or '.png'}"
                (rt / s / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, rt / s / rel)
                imgs.append(rel)
                if r.get("ocr_json") and Path(r["ocr_json"]).is_file():
                    o = rt / s / "ocr" / f"{sid}_p{k}.json"
                    o.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(r["ocr_json"], o)
                else:
                    has_ocr[s] = False
                n_pages[s] += 1
            label = {"id": sid, "doc_type": form_id, "doc_name": reg[form_id].name, "images": imgs,
                     "pages": [{"width": r["width"], "height": r["height"]} for r in pr], "fields": fields,
                     "source": {"batch": batch["name"], "document": doc, "format": f["id"], "case": case_of(batch, doc)[1]}}
            LR._write(rt / s / "labels" / f"{sid}.json", label)
            labels[s].append(label)
    unknown_case = sum(1 for d in side if case_of(batch, d)[1] is None)
    model = (batch.get("results") or {}).get("model")
    out = {"root": str(rt), "ratio": ratio, "splits": {}, "skipped": dict(skipped), "notes": notes[:50],
           "unknown_case": unknown_case, "at": time.strftime("%Y-%m-%d %H:%M")}
    for s, ls in labels.items():
        if not ls:
            continue
        meta = {"format": "docgen-labels/1", "name": f"{batch['name']} 원본 데이터 ({'평가' if s == 'test' else '학습'})",
                "real_data": bool(batch.get("real_data")), "gt": "pseudo", "from_batch": batch["name"], "model": model, "split": s}
        if has_ocr[s]:
            meta["ocr_scope"] = "full_page"
        LR._write(rt / s / "meta.json", meta)
        bundles = _bundles(batch, ls, SCENARIOS)
        if bundles:
            (rt / s / "bundles.jsonl").write_text("".join(json.dumps(b, ensure_ascii=False) + "\n" for b in bundles), encoding="utf-8")
        out["splits"][s] = {"path": str(rt / s), "documents": len(ls), "pages": n_pages[s], "fields": sum(len(x["fields"]) for x in ls),
                            "cases": len({x["source"]["case"] or x["id"] for x in ls}), "bundles": len(bundles), "ocr": has_ocr[s]}
    LR._write(rt / "export.json", {**out, "documents": {x["source"]["document"]: {"split": s, "id": x["id"], "doc_type": x["doc_type"]}
                                                        for s, ls in labels.items() for x in ls}})
    batch["raw"] = {"ratio": ratio, "root": str(rt), "at": out["at"], "documents": sum(len(v) for v in labels.values())}
    IM._write_json(bdir / "batch.json", batch)
    return out


def _bundles(batch: dict, labels: list[dict], scenarios: dict) -> list[dict]:
    """건 = 업무 묶음 (v1 bundles.jsonl). 업무가 ③에 등록된 시나리오이고, 건 안에 같은 서식이 한 건씩일 때만."""
    by: dict[str, list[dict]] = {}
    for x in labels:
        if x["source"]["case"]:
            by.setdefault(x["source"]["case"], []).append(x)
    out = []
    for case, xs in sorted(by.items()):
        sc = case_of(batch, xs[0]["source"]["document"])[0]
        kinds = [x["doc_type"] for x in xs]
        if sc not in scenarios or len(set(kinds)) != len(kinds):
            continue
        out.append({"bundle_id": LR.safe(case), "scenario": sc, "documents": [x["id"] for x in xs]})
    return out


# ---------------------------------------------------------------------------
# 채점 (시험 폴더의 생성 정답으로)
# ---------------------------------------------------------------------------

def _answer_items(label: dict) -> set[tuple]:
    """v1 라벨 → 모델 답 꼴 (키, 값, 쪽 1부터, bbox_2d). 시험 폴더 gt 의 items 와 같은 꼴."""
    from docgen.bench.metrics import normalize_box

    sizes = [(p["width"], p["height"]) for p in label["pages"]]
    out = set()
    for f in label["fields"]:
        def box(b, pg):
            return tuple(normalize_box(b, *sizes[pg])) if b is not None and pg is not None else None
        if f["type"] in ("checkbox", "checkbox_multi"):
            out |= {(f["key"], o["text"], (f.get("page") or 0) + 1, box(o.get("box_bbox"), f.get("page"))) for o in f["options"] if o["checked"]}
        elif f["type"] in ("seal", "signature"):
            if f.get("present"):
                out.add((f["key"], True, (f.get("page") or 0) + 1, box(f.get("bbox"), f.get("page"))))
        elif f.get("value") is not None:
            out.add((f["key"], f["value"], (f.get("page") or 0) + 1, box(f.get("bbox"), f.get("page"))))
    return out


def score(real_root: Path, batch_name: str, testset: Path) -> dict:
    """내보낸 라벨 ↔ 생성 정답(<시험 폴더>/gt/<서류>.json). 서식 ID, 항목(키·값·쪽·위치가 모두 같아야 맞음), 건 나누기(한 건이 양쪽에 있으면 샘)."""
    truth = json.loads((testset / "truth.json").read_text(encoding="utf-8"))["documents"]
    by = {**{k: (k, v) for k, v in truth.items()}, **{v["flat"]: (k, v) for k, v in truth.items()}}
    rt = out_root(real_root, batch_name)
    tp = n_pred = n_gt = docs = form_ok = 0
    wrong, case_side = [], {}
    for s in ("train", "test"):
        for lf in sorted((rt / s / "labels").glob("*.json")) if (rt / s / "labels").is_dir() else []:
            label = json.loads(lf.read_text(encoding="utf-8"))
            rel, t = by[label["source"]["document"]]
            docs += 1
            form_ok += label["doc_type"] == t["form"]
            case_side.setdefault((t["scenario"], t["case"]), set()).add(s)
            gt_items = json.loads((testset / "gt" / f"{rel}.json").read_text(encoding="utf-8"))["items"]
            g = {(it["key"], it["value"], it.get("page", 1), tuple(it["bbox_2d"]) if it.get("bbox_2d") else None) for it in gt_items}
            p = _answer_items(label)
            tp += len(g & p)
            n_pred += len(p)
            n_gt += len(g)
            if g != p and len(wrong) < 20:
                wrong.append({"doc": rel, "form": t["form"], "doc_type": label["doc_type"], "missing": sorted(map(str, g - p))[:5], "extra": sorted(map(str, p - g))[:5]})
    leak = [c for c, ss in case_side.items() if len(ss) > 1]
    return {"documents": docs, "form_acc": round(form_ok / docs, 4) if docs else None,
            "precision": round(tp / n_pred, 4) if n_pred else None, "recall": round(tp / n_gt, 4) if n_gt else None,
            "items": n_gt, "leaked_cases": len(leak), "wrong": wrong}


def main(argv=None) -> None:
    import argparse

    ap = argparse.ArgumentParser(prog="python -m studio.intake_raw", description=__doc__.split("\n")[0])
    ap.add_argument("batch")
    ap.add_argument("real_root")
    ap.add_argument("--ratio", type=float, default=None)
    ap.add_argument("--score", help="시험 폴더 (truth.json · gt/)")
    a = ap.parse_args(argv)
    r = export(Path(a.batch), Path(a.real_root), a.ratio)
    print(json.dumps({k: r[k] for k in ("splits", "skipped", "unknown_case")}, ensure_ascii=False))
    if a.score:
        s = score(Path(a.real_root), json.loads((Path(a.batch) / "batch.json").read_text(encoding="utf-8"))["name"], Path(a.score))
        print(json.dumps({k: v for k, v in s.items() if k != "wrong"}, ensure_ascii=False))
        for w in s["wrong"][:10]:
            print(" ", json.dumps(w, ensure_ascii=False))
        sys.exit(0 if s["precision"] == s["recall"] == s["form_acc"] == 1.0 and not s["leaked_cases"] else 1)


if __name__ == "__main__":
    main()
