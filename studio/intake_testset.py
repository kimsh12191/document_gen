"""④ 서류 넣기 시험 폴더 (studio/DESIGN.md 15.2·15.6 1번): 생성기로 시나리오마다 건 N개를 렌더링해
넣을 폴더 두 벌과 정답을 만든다. 실서류 대신 이 폴더로 묶기·판정·건/업무 추정·반영을 잰다.

  <out>/structured/  images/<업무>/<건>/<서류>/p1.png · ocr/<같은 경로>/p1.json · pred/<업무>/<건>/<서류>.json
  <out>/flat/        같은 서류를 구분 없이: images/<무작위 ID>/p1.png … (업무·건 추정 시험용)
  <out>/truth.json   서류마다 진짜 서식 ID·역할·건·업무와 두 벌의 경로, 빼 둔 서식(--hold-out), 넣은 추출 오류
  <out>/gt/<업무>/<건>/<서류>.json   오류 없는 추출 정답 {"items": …} (pred 와 같은 형식, 원래 키). 원본 데이터 내보내기 채점용

- OCR 은 쪽 전체 글자(합성 OCR 정답, docgen/ocr_set.py 와 같은 방법)를 사내 OCR 응답 형식으로 쓴다.
- 추출 결과(pred)는 생성 라벨의 값·위치에서 만들고, 일부러 틀린 값·다른 키 이름·빠진 항목·pred 없는 서류를 섞는다.
- 서류 폴더 이름(d01…)과 flat 의 ID 는 서식 ID 를 드러내지 않는다. 건마다 서류 하나가 빠질 수 있다(--missing).
- 외부 공개 문서(생성기에 없는 양식)는 기본으로 studio/testdata/external/bundle 을 합친다 (--external, 없애려면 --no-external).

  python -m studio.intake_testset <out> [--scenarios all|fx_remittance,…] [--cases 3] [--hold-out 서식ID,…]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shutil
import sys
from pathlib import Path

from docgen.bench.build import CONDITIONS, Builder, pick_condition
from docgen.bench.metrics import normalize_box
from docgen.registry import SCENARIO_SAMPLING, SCENARIOS, load_all

MARKS = ("seal", "signature", "checkbox", "checkbox_multi")
RENAME = {"customer.name": "name", "applicant.name": "name", "customer.rrn": "rrn", "applicant.rrn": "rrn",
          "customer.address": "address", "applicant.address": "address", "customer.mobile": "phone"}
DOC_RE = r"^(?P<document_id>.+)/p\d+\.(png|jpg)$"
EXTERNAL = Path(__file__).resolve().parent / "testdata" / "external" / "bundle"


def _write(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


def _link(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(src, dst)
    except OSError:
        shutil.copyfile(src, dst)


def pred_items(fields: list[dict], sizes: list[tuple[int, int]]) -> list[dict]:
    """생성 라벨 → 추출 결과 items (RESULTS_FORMAT.md 4절). 위치는 그 쪽 0~1000, 쪽은 1부터."""
    def where(f, box):
        pg = f.get("page", 0)
        return {"bbox_2d": normalize_box(box, *sizes[pg]), "page": pg + 1} if box and pg < len(sizes) else {}

    out = []
    for f in fields:
        if f.get("group") or f.get("value") is None or f["key"].startswith("seal.untagged"):
            continue
        base = {"key": f["key"], **({"label": f["label"]} if f.get("label") else {})}
        if f["type"] in ("checkbox", "checkbox_multi"):
            out += [{**base, "type": "checkbox", "value": o["text"], **where(f, o.get("box_bbox"))}
                    for o in f.get("options") or [] if o.get("checked")]
        elif f["type"] in ("seal", "signature"):
            if f.get("present"):
                out.append({**base, "type": f["type"], "value": True, **where(f, f.get("bbox"))})
        elif str(f["value"]).strip():
            out.append({**base, "value": str(f["value"]), **where(f, f.get("bbox"))})
    return out


def noisy(items: list[dict], rng: random.Random, p_wrong: float, p_drop: float) -> tuple[list[dict], list[dict]]:
    """추출 오류 섞기: 값 틀리기·항목 빠뜨리기·다른 키 이름. (새 items, 넣은 오류 목록)."""
    out, errs = [], []
    for it in items:
        if rng.random() < p_drop:
            errs.append({"kind": "drop", "key": it["key"]})
            continue
        it = dict(it)
        if it.get("type") is None and rng.random() < p_wrong and len(it["value"]) > 1:
            i = rng.randrange(len(it["value"]))
            old, it["value"] = it["value"], it["value"][:i] + rng.choice("0123456789가나다") + it["value"][i + 1:]
            if it["value"] != old:
                errs.append({"kind": "wrong", "key": it["key"], "true": old, "pred": it["value"]})
        if it["key"] in RENAME:
            it["key"] = RENAME[it["key"]]
        out.append(it)
    return out, errs


class Maker:
    def __init__(self, out: Path, scale: float, conditions):
        self.out, self.conditions = out, conditions
        self.reg = load_all()
        self.b = Builder(out / "_work", scale)

    def close(self):
        self.b.close()
        shutil.rmtree(self.out / "_work", ignore_errors=True)

    def doc(self, doc_id: str, profile, seed: int, key: str) -> dict:
        """서류 한 건: Builder.render_doc 와 같은 렌더링·증강에 쪽 전체 글자(OCR)를 더한다."""
        from PIL import Image

        from docgen.augment import augment
        from docgen.cli import _aug_fields
        from docgen.ocr_export import background_words, page_document, page_items, transform_texts
        from docgen.render import render
        from docgen.schema import build_fields

        spec = self.reg[doc_id]
        html, raw, data = render(spec, profile, seed)
        png = self.b.out / "pages" / f"{hashlib.md5(key.encode()).hexdigest()[:12]}.png"
        png.parent.mkdir(parents=True, exist_ok=True)
        info = self.b.renderer.render(html, png, texts=True)
        fields, texts = build_fields(raw, info), info["texts"]
        paths = [Path(p) for p in info["images"]]
        sizes = [(pg["width"], pg["height"]) for pg in info["pages"]]
        bg = background_words(doc_id) if spec.template == "_real_form.html.j2" else {}
        zoom = self.b.renderer.scale * 96 / 72
        cond = pick_condition(f"intake:{key}", self.conditions)
        if cond != "clean":
            arng = random.Random(f"intake:aug:{key}")
            new, tfs = [], []
            for p in paths:
                img, _, tf = augment(Image.open(p), arng, cond, with_transform=True)
                q = p.with_suffix(".jpg")
                img.save(q, quality=92)
                p.unlink()
                new.append(q)
                tfs.append(tf)
            sizes = [Image.open(q).size for q in new]
            fields, texts = _aug_fields(fields, tfs), transform_texts(texts, tfs)
            bg = {pg: [{**w, "bbox": tfs[pg].bbox([v * zoom for v in w["bbox"]])} for w in ws] for pg, ws in bg.items() if pg < len(tfs)}
            paths, zoom = new, 1.0
        ocr = [page_document(page_items([t for t in texts if t["page"] == k], bg.get(k, []), zoom, "word"), p.name)
               for k, p in enumerate(paths)]
        return {"form": doc_id, "name": spec.name, "condition": cond, "pages": paths, "sizes": sizes, "fields": fields, "ocr": ocr}


def build(out: Path, scenarios: list[str], cases: int, hold_out: list[str], seed_start: int = 70000, scale: float = 1.5,
          conditions=CONDITIONS, missing: float = 0.1, no_pred: float = 0.15, p_wrong: float = 0.1, p_drop: float = 0.05,
          external: Path | None = None, log=print) -> dict:
    from docgen.roles import resolve

    if out.exists():
        shutil.rmtree(out)
    S, Fl = out / "structured", out / "flat"
    truth = {"format": "studio-intake-truth/1", "documents": {}, "held_out": hold_out, "scenarios": {},
             "settings": {"cases": cases, "seed_start": seed_start, "scale": scale, "missing": missing, "no_pred": no_pred,
                          "p_wrong": p_wrong, "p_drop": p_drop}}
    m = Maker(out, scale, conditions)
    try:
        for si, sc in enumerate(scenarios):
            truth["scenarios"][sc] = {"name": SCENARIOS[sc][0], "roles": []}
            for c in range(cases):
                seed = seed_start + si * 1000 + c
                case = f"C{seed}"
                rng = random.Random(f"intake:{sc}:{seed}")
                sel = resolve(SCENARIOS[sc][1], SCENARIO_SAMPLING.get(sc), seed, sc)
                if c == 0:
                    truth["scenarios"][sc]["roles"] = [r["role"] for r in sel]
                keep = [r for r in sel if rng.random() >= missing] or sel[:1]
                rng.shuffle(keep)
                profile = Builder.bundle_profile(sc, seed)
                for n, r in enumerate(keep, 1):
                    rel = f"{sc}/{case}/d{n:02d}"
                    d = m.doc(r["id"], profile, seed, rel)
                    flat = "doc_" + hashlib.sha1(f"flat:{rel}".encode()).hexdigest()[:10]
                    for k, (p, oj) in enumerate(zip(d["pages"], d["ocr"]), 1):
                        name = f"p{k}{p.suffix}"
                        _link(p, S / "images" / rel / name)
                        _link(p, Fl / "images" / flat / name)
                        _write(S / "ocr" / rel / f"p{k}.json", oj)
                        _write(Fl / "ocr" / flat / f"p{k}.json", oj)
                    errs, has_pred = [], rng.random() >= no_pred
                    clean = pred_items(d["fields"], d["sizes"])
                    _write(out / "gt" / f"{rel}.json", {"items": clean})
                    if has_pred:
                        items, errs = noisy(clean, rng, p_wrong, p_drop)
                        _write(S / "pred" / f"{rel}.json", {"items": items})
                        _write(Fl / "pred" / f"{flat}.json", {"items": items})
                    truth["documents"][rel] = {"form": r["id"], "name": d["name"], "role": r["role"], "scenario": sc, "case": case,
                                               "seed": seed, "flat": flat, "pages": len(d["pages"]), "condition": d["condition"],
                                               "new_form": r["id"] in hold_out, "pred": has_pred, "pred_errors": errs}
                    for p in d["pages"]:
                        p.unlink(missing_ok=True)
                log(f"{sc} {case}: 서류 {len(keep)}/{len(sel)}")
    finally:
        m.close()
    if external:
        add_external(out, external, truth)
    for root, name in ((S, "구분 있음"), (Fl, "구분 없음")):
        _write(root / "meta.json", {"format": "studio-results/1", "name": f"서류 넣기 시험 ({name})", "real_data": False,
                                    "document_regex": DOC_RE, "model": "intake-testset"})
    _write(out / "truth.json", truth)
    return truth


def add_external(out: Path, ext: Path, truth: dict) -> None:
    """외부 공개 문서 묶음 합치기 (studio/intake_external.py 가 만든 <ext>/images·ocr·pred/<문서>/… + truth.json).
    truth 의 placement {종류: 업무} 대로 그 업무의 건에 차례로 끼워 넣는다(경로 <업무>/<건>/d<다음 번호>). 그 업무가 없으면
    external/<종류>/<ID> 그대로. 문서마다 출처 URL·라이선스·SHA-256 을 정답에 남긴다."""
    t = json.loads((ext / "truth.json").read_text(encoding="utf-8"))
    cases = {}
    for d in truth["documents"].values():
        if not d.get("external"):
            cases.setdefault(d["scenario"], []).append(d["case"])
    cases = {sc: list(dict.fromkeys(cs)) for sc, cs in cases.items()}
    used: dict = {}
    for src, d in t["documents"].items():
        sc = t.get("placement", {}).get(d.get("kind"))
        if sc in cases:
            n = used.get(sc, 0)
            used[sc] = n + 1
            case = cases[sc][n % len(cases[sc])]
            k = sum(1 for r in truth["documents"] if r.startswith(f"{sc}/{case}/")) + 1   # 생성 서류 다음 번호 (외부임이 드러나지 않게)
            rel, d = f"{sc}/{case}/d{k:02d}", {**d, "scenario": sc, "case": case}
        else:
            rel, d = src, {**d, "scenario": "external", "case": None}
        flat = "doc_" + hashlib.sha1(f"flat:{rel}".encode()).hexdigest()[:10]
        for sub in ("images", "ocr"):
            for f in sorted((ext / sub / src).glob("*")) if (ext / sub / src).is_dir() else []:
                _link(f, out / "structured" / sub / rel / f.name)
                _link(f, out / "flat" / sub / flat / f.name)
        pf = ext / "pred" / f"{src}.json"
        if pf.is_file():   # 외부 문서의 추출 결과는 손으로 단 라벨 그대로 (오류를 넣지 않는다)
            _link(pf, out / "gt" / f"{rel}.json")
            _link(pf, out / "structured" / "pred" / f"{rel}.json")
            _link(pf, out / "flat" / "pred" / f"{flat}.json")
        truth["documents"][rel] = {**d, "flat": flat, "external": True, "new_form": True, "external_id": src}


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="python -m studio.intake_testset", description=__doc__.split("\n")[0])
    ap.add_argument("out")
    ap.add_argument("--scenarios", default="all", help="all 또는 쉼표로 (docgen/scenarios.json 의 ID)")
    ap.add_argument("--cases", type=int, default=3, help="시나리오마다 건 수")
    ap.add_argument("--hold-out", default="", help="'새 서식'으로 다룰 서식 ID (쉼표). 정답에 표시만 하고, 판정 시험에서 기존 서식 지문에서 뺀다")
    ap.add_argument("--seed-start", type=int, default=70000)
    ap.add_argument("--scale", type=float, default=1.5)
    ap.add_argument("--clean", action="store_true", help="촬영 조건 증강 없이 원본만")
    ap.add_argument("--missing", type=float, default=0.1, help="건마다 서류가 빠질 확률")
    ap.add_argument("--no-pred", type=float, default=0.15, help="추출 결과가 없는 서류 비율")
    ap.add_argument("--wrong", type=float, default=0.1, help="추출 값을 틀리게 할 확률 (항목마다)")
    ap.add_argument("--drop", type=float, default=0.05, help="추출 항목을 빠뜨릴 확률")
    ap.add_argument("--external", default=str(EXTERNAL), help="외부 공개 문서 묶음 폴더 (studio/intake_external.py 가 만든 것)")
    ap.add_argument("--no-external", action="store_true", help="외부 문서를 섞지 않는다")
    a = ap.parse_args(argv)
    scenarios = list(SCENARIOS) if a.scenarios == "all" else [s.strip() for s in a.scenarios.split(",") if s.strip()]
    hold = [s.strip() for s in a.hold_out.split(",") if s.strip()]
    reg = load_all()
    bad = [s for s in scenarios if s not in SCENARIOS] + [h for h in hold if h not in reg]
    if bad:
        sys.exit(f"없는 시나리오·서식: {bad}")
    t = build(Path(a.out), scenarios, a.cases, hold, a.seed_start, a.scale, (("clean", 1.0),) if a.clean else CONDITIONS,
              a.missing, a.no_pred, a.wrong, a.drop, None if a.no_external else Path(a.external))
    docs = t["documents"].values()
    print(f"{a.out}: 업무 {len(t['scenarios'])} · 건 {len({(d['scenario'], d['case']) for d in docs})} · 서류 {len(t['documents'])}"
          f" · 쪽 {sum(d['pages'] for d in docs)} · 추출 결과 {sum(d['pred'] for d in docs)} · 새 서식 서류 {sum(d['new_form'] for d in docs)}"
          f" (외부 문서 {sum(bool(d.get('external')) for d in docs)})")


if __name__ == "__main__":
    main()
