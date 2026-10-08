"""평가 세트 만들기.

  python -m docgen.bench build --out bench_out [--types all] [--per-doc 1] [--bundles 4]

출력:
  bench_out/
    meta.json                 만든 설정, 과제별 문항 수, 서류명 목록
    images/                   서류 이미지 (단일 서류 과제)
    images/bundles/           업무 묶음 서류 이미지
    crops/                    ocr_field 용 값 칸 이미지
    tasks/<과제>.jsonl         문항: {"id", "task", "images", "prompt", "answer", "eval"?, "meta"}

같은 설정이면 언제 만들어도 같은 세트가 나온다 (seed 고정, 학습용 seed 와 겹치지 않는 범위).
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
import time
from pathlib import Path

from ..entities import make_profile
from ..registry import GROUPS, SCENARIO_EXTRA, SCENARIOS, load_all
from ..render import render
from ..schema import build_fields
from . import perturb
from .metrics import norm_text
from .rules import Bundle, questions, r_doc_valid, valid_candidates

VERSION = "1.0"
SEED_SINGLE = 1_000_000   # 단일 서류 과제 고객 seed 시작
SEED_BUNDLE = 2_000_000   # 업무 묶음 고객 seed 시작

# 촬영 조건 비율: 절반은 깨끗한 원본, 나머지는 스캔·촬영·팩스 증강 (docgen/augment.py)
CONDITIONS = (("clean", 0.5), ("scan", 0.2), ("photo", 0.15), ("fax", 0.15))
MARK_TYPES = ("checkbox", "checkbox_multi", "seal", "signature")

P_CLASSIFY = ("이 문서는 고객이 은행에 제출한 서류입니다. 서류의 정식 명칭(서류명)을 답하세요. "
              "설명 없이 서류명만 한 줄로 답하세요.")
P_OCR_PAGE = ("이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, "
              "표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.")
P_OCR_FIELD = "이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요."
P_KIE = ("이 문서에서 아래 항목의 값을 찾아 JSON 객체로 답하세요. 키는 그대로 쓰고, 값은 문서에 적힌 그대로 옮기세요. "
         "문서에 비어 있거나 없는 항목은 null 로 답하세요.\n항목 (키: 항목명)\n{items}")
P_MARKS = ("이 문서의 체크박스·도장·서명 상태를 확인해 JSON 객체로 답하세요.\n"
           "- 체크박스: 체크된 보기의 글자 (체크된 것이 없으면 null)\n"
           "- 복수 선택: 체크된 보기 글자의 목록 (없으면 [])\n"
           "- 도장·서명: 찍혀 있거나 서명되어 있으면 true, 비어 있으면 false\n항목\n{items}")
P_DOC_CHECK = ("고객이 '{task}' 업무를 위해 서류를 제출했습니다. 첨부 이미지는 제출된 서류의 첫 쪽입니다 (순서 무관).\n"
               "필수 제출 서류:\n{required}\n\n필수 서류 중 제출되지 않은 서류를 찾아 "
               '{{"missing": ["서류명", ...]}} 형식의 JSON 으로 답하세요. 모두 제출되었으면 {{"missing": []}} 입니다. '
               "서류명은 위 목록에 적힌 그대로 쓰세요.")
P_CROSS = ("고객이 '{task}' 업무를 위해 제출한 서류 {n}건입니다 (이미지 {pages}장). 서류들 사이에 서로 맞지 않는 정보"
           "(성명, 주민등록번호, 생년월일, 주소, 연락처, 계좌번호, 상호, 금액 등)가 있는지 대조하세요.\n"
           '{{"consistent": true 또는 false, "issues": [{{"document": "서류명", "field": "항목명", "value": "그 서류에 적힌 값", '
           '"expected": "다른 서류에 적힌 값"}}]}} 형식의 JSON 으로 답하세요. 모두 일치하면 {{"consistent": true, "issues": []}} 입니다.')
P_REVIEW = "고객이 '{task}' 업무를 위해 제출한 서류입니다 (이미지 {pages}장).\n{question}"


def _git_rev() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=Path(__file__).resolve().parents[2],
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:  # noqa: BLE001
        return None


def pick_condition(key: str) -> str:
    r = random.Random(f"bench:cond:{key}").random()
    acc = 0.0
    for name, p in CONDITIONS:
        acc += p
        if r < acc:
            return name
    return CONDITIONS[0][0]


def field_kind(f: dict) -> str:
    """cross_check·ocr_field 분석용 값 종류."""
    lab, t = f.get("label") or "", f.get("type")
    if t in ("rrn", "biz_no", "corp_reg_no", "phone", "account_no", "date", "amount", "amount_korean"):
        return {"amount_korean": "amount", "biz_no": "reg_no", "corp_reg_no": "reg_no"}.get(t, t)
    if perturb.NAME_LABEL.search(lab):
        return "name"
    if "주소" in lab or "소재지" in lab:
        return "address"
    if "계좌" in lab:
        return "account_no"
    if t in ("number",):
        return "number"
    return "text"


class Builder:
    def __init__(self, out: Path, scale: float):
        from ..image import ImageRenderer

        self.out = out
        self.reg = load_all()
        self.renderer = ImageRenderer(scale=scale).__enter__()
        self.files: dict[str, object] = {}
        self.counts: dict[str, int] = {}
        for d in ("images/bundles", "crops", "tasks"):
            (out / d).mkdir(parents=True, exist_ok=True)

    def close(self):
        self.renderer.__exit__(None, None, None)
        for fh in self.files.values():
            fh.close()

    def emit(self, rec: dict):
        t = rec["task"]
        if t not in self.files:
            self.files[t] = open(self.out / "tasks" / f"{t}.jsonl", "w", encoding="utf-8")
        self.files[t].write(json.dumps(rec, ensure_ascii=False) + "\n")
        self.counts[t] = self.counts.get(t, 0) + 1

    # ------------------------------------------------------------------
    def render_doc(self, doc_id: str, profile, seed: int, stem: str, cond: str, aug_key: str | None = None,
                   html: str | None = None, raw: list | None = None, data: dict | None = None) -> dict:
        """서류 한 건을 렌더링해 이미지(조건에 따라 증강)와 라벨 필드를 만든다."""
        from PIL import Image

        from ..augment import augment
        from ..cli import _aug_fields

        spec = self.reg[doc_id]
        if html is None:
            html, raw, data = render(spec, profile, seed)
        png = self.out / f"{stem}.png"
        png.parent.mkdir(parents=True, exist_ok=True)
        info = self.renderer.render(html, png)
        fields = build_fields(raw, info)
        paths = [Path(p) for p in info["images"]]
        sizes = [(pg["width"], pg["height"]) for pg in info["pages"]]
        if cond != "clean":
            arng = random.Random(f"bench:aug:{aug_key or stem}")
            new_paths, new_sizes, tfs = [], [], []
            for p in paths:
                img, _, tf = augment(Image.open(p), arng, cond, with_transform=True)
                q = p.with_suffix(".jpg")
                img.save(q, quality=92)
                p.unlink()
                new_paths.append(q)
                new_sizes.append(img.size)
                tfs.append(tf)
            paths, sizes, fields = new_paths, new_sizes, _aug_fields(fields, tfs)
        hand = spec.group == "hana" and bool((data or {}).get("style", {}).get("hand"))
        return {"doc_id": doc_id, "name": spec.name, "group": spec.group, "seed": seed, "condition": cond,
                "images": [str(p.relative_to(self.out)) for p in paths], "sizes": sizes, "fields": fields,
                "raw": raw, "raw_keys": [r["key"] for r in raw], "visible": perturb.visible_keys(html),
                "html": html, "data": data, "writing": "hand" if hand else "print",
                "bank": next((f["value"] for f in fields if f["key"] in ("bank", "bank.name")), None)}

    def field_writing(self, r: dict, key: str) -> str:
        if r["group"] == "hana" and key.startswith("handwritten"):
            return "hand"
        return r["writing"]

    # ------------------------------------------------------------------
    # 단일 서류 과제
    # ------------------------------------------------------------------
    def single(self, r: dict, stem: str, fields_per_doc: int, max_keys: int):
        meta = {"doc_type": r["doc_id"], "doc_name": r["name"], "group": r["group"], "condition": r["condition"],
                "writing": r["writing"], "n_pages": len(r["images"])}
        base = {"images": r["images"], "meta": meta}
        rng = random.Random(f"bench:single:{stem}")
        sid = Path(stem).name
        fields = r["fields"]
        raw_key = dict(zip(range(len(r["raw_keys"])), r["raw_keys"]))

        self.emit({"id": f"classify/{sid}", "task": "classify", "prompt": P_CLASSIFY, "answer": r["name"], **base})

        visible = []
        for i, f in enumerate(fields):
            if (f.get("value") is None or f["type"] in MARK_TYPES or f.get("group")
                    or raw_key.get(i) not in r["visible"]):
                continue
            visible.append(f)
        lines: list[str] = []
        for f in visible:
            for ln in str(f["value"]).split("\n"):
                if norm_text(ln) and ln.strip() not in lines:
                    lines.append(ln.strip())
        if lines:
            self.emit({"id": f"ocr_page/{sid}", "task": "ocr_page", "prompt": P_OCR_PAGE, "answer": lines, **base})

        # ocr_field: 값 칸 잘라내기
        from PIL import Image

        boxed = [f for f in visible if f.get("bbox") and f.get("page", 0) < len(r["images"])]
        for j, f in enumerate(sorted(rng.sample(boxed, min(len(boxed), fields_per_doc)), key=boxed.index)):
            img = Image.open(self.out / r["images"][f.get("page", 0)])
            x0, y0, x1, y1 = f["bbox"]
            pad = (y1 - y0) * 0.25 + 4
            box = (max(0, int(x0 - pad)), max(0, int(y0 - pad)), min(img.width, int(x1 + pad)), min(img.height, int(y1 + pad)))
            if box[2] - box[0] < 4 or box[3] - box[1] < 4:
                continue
            crop_path = f"crops/{sid}_{j}.png"
            img.crop(box).convert("RGB").save(self.out / crop_path)
            self.emit({"id": f"ocr_field/{sid}/{f['key']}", "task": "ocr_field", "images": [crop_path],
                       "prompt": P_OCR_FIELD, "answer": str(f["value"]).replace("\n", " "),
                       "meta": {**meta, "n_pages": 1, "key": f["key"], "label": f.get("label"), "kind": field_kind(f),
                                "writing": self.field_writing(r, f["key"]), "corrected": bool(f.get("corrected_from")),
                                "length": len(norm_text(f["value"]))}})

        # kie: 항목 목록을 주고 값 추출
        kf = [f for f in fields if f["type"] not in MARK_TYPES and not f.get("group")
              and not f["key"].startswith(("seal.", "sign."))]
        if len(kf) > max_keys:
            kf = sorted(rng.sample(kf, max_keys), key=kf.index)
        if kf:
            items = "\n".join(f"- {f['key']}: {f.get('label') or '-'}" for f in kf)
            self.emit({"id": f"kie/{sid}", "task": "kie", "prompt": P_KIE.format(items=items),
                       "answer": {f["key"]: f["value"] for f in kf},
                       "eval": {"fields": {f["key"]: {"type": f["type"], "norm": f.get("norm"), "kind": field_kind(f)}
                                           for f in kf}}, **base})

        # marks: 체크박스·도장·서명
        mf = [f for f in fields if f["type"] in MARK_TYPES and not f["key"].startswith("seal.untagged")
              and (f["type"] in ("seal", "signature") or f.get("options"))]
        if len(mf) > max_keys:
            mf = sorted(rng.sample(mf, max_keys), key=mf.index)
        if mf:
            lines, ans, types = [], {}, {}
            for f in mf:
                lab = f.get("label") or "-"
                if f["type"] == "checkbox":
                    lines.append(f"- {f['key']}: {lab} (체크박스, 보기: {' / '.join(o['text'] for o in f['options'])})")
                    ans[f["key"]] = f["value"]
                elif f["type"] == "checkbox_multi":
                    lines.append(f"- {f['key']}: {lab} (복수 선택, 보기: {' / '.join(o['text'] for o in f['options'])})")
                    ans[f["key"]] = [o["text"] for o in f["options"] if o["checked"]]
                else:
                    lines.append(f"- {f['key']}: {lab} ({'도장' if f['type'] == 'seal' else '서명'})")
                    ans[f["key"]] = bool(f["present"])
                types[f["key"]] = f["type"]
            self.emit({"id": f"marks/{sid}", "task": "marks", "prompt": P_MARKS.format(items="\n".join(lines)),
                       "answer": ans, "eval": {"types": types}, **base})

    # ------------------------------------------------------------------
    # 업무 묶음 과제
    # ------------------------------------------------------------------
    def bundle(self, scenario: str, seed: int, b: int):
        task_name, ids = SCENARIOS[scenario]
        p = make_profile(seed)
        p.extra.update(scenario=scenario, **SCENARIO_EXTRA.get(scenario, {}))
        p.extra["form_bank"] = "하나은행"  # 옛 은행 서식(과거 날짜)이 섞이지 않게
        bid = f"{scenario}_{seed}"
        docs = []
        for doc_id in ids:
            stem = f"images/bundles/{bid}/{doc_id}"
            docs.append(self.render_doc(doc_id, p, seed, stem, pick_condition(f"{bid}:{doc_id}")))
        meta = {"scenario": scenario, "task_name": task_name, "bundle": bid}

        # doc_check
        rng = random.Random(f"bench:doc_check:{bid}")
        n_missing = rng.choices([0, 1, 2], [0.3, 0.5, 0.2])[0]
        missing = rng.sample(docs, n_missing)
        present = [d for d in docs if d not in missing]
        rng.shuffle(present)
        required = "\n".join(f"{i + 1}. {d['name']}" for i, d in enumerate(docs))
        self.emit({"id": f"doc_check/{bid}", "task": "doc_check", "images": [d["images"][0] for d in present],
                   "prompt": P_DOC_CHECK.format(task=task_name, required=required),
                   "answer": {"missing": [d["name"] for d in missing]},
                   "eval": {"required": [d["name"] for d in docs]},
                   "meta": {**meta, "n_missing": n_missing, "n_docs": len(present)}})

        # cross_check
        self.cross_check(docs, p, seed, bid, meta, perturbed=(b % 2 == 0))

        # review
        B = Bundle(scenario, {d["doc_id"]: {"name": d["name"], "fields": d["fields"]} for d in docs})
        by_id = {d["doc_id"]: d for d in docs}
        qs = questions(B, random.Random(f"bench:review:{bid}"))
        if (dv := self.doc_valid(docs, B, p, seed, bid)) is not None:
            q, aged = dv
            by_id = {**by_id, q["docs"][0]: aged}
            qs.append(q)
        for q in qs:
            imgs = [im for did in dict.fromkeys(q["docs"]) for im in by_id[did]["images"]]
            self.emit({"id": f"review/{bid}/{q['rule']}", "task": "review", "images": imgs,
                       "prompt": P_REVIEW.format(task=task_name, pages=len(imgs), question=q["question"]),
                       "answer": q["answer"], "eval": {"answer_type": q["answer_type"], "tol": q["tol"], **q.get("info", {})},
                       "meta": {**meta, "rule": q["rule"], "skill": q["skill"]}})

    def doc_valid(self, docs: list[dict], B: Bundle, profile, seed: int, bid: str):
        """유효기간 문항: 서류 하나를 골라 신청일 기준 경과일이 0~88일(유효) 또는 93~400일(만료)이 되게
        발급일을 옮긴 사본을 렌더링한다. 반환 (문항, 사본 서류) 또는 None."""
        rng = random.Random(f"bench:valid:{bid}")
        app = B.app_date()
        cands = valid_candidates(B)
        if not app or not cands:
            return None
        did = rng.choice(cands)
        d = next(x for x in docs if x["doc_id"] == did)
        fi = next(i for i, f in enumerate(d["fields"]) if f["key"] == "issue_date")
        f = d["fields"][fi]
        if d["raw_keys"][fi] not in d["visible"]:
            return None
        old_days = (app[2] - B.date(did, "issue_date")).days
        target = rng.randint(93, 400) if rng.random() < 0.5 else rng.randint(0, 88)
        new = perturb.shift_date(f["value"], f["norm"], old_days - target)
        html = new and perturb.apply(d["html"], d["raw_keys"][fi], f["value"], new)
        if not html:
            return None
        raw = [dict(x) for x in d["raw"]]
        raw[fi]["value"] = new
        aged = self.render_doc(did, profile, seed, f"images/bundles/{bid}/{did}_aged", d["condition"],
                               aug_key=f"images/bundles/{bid}/{did}", html=html, raw=raw, data=d["data"])
        B2 = Bundle(B.scenario, {**B.docs, did: {"name": d["name"], "fields": aged["fields"]}})
        q = r_doc_valid(B2, rng, doc=did)
        if not q:
            return None
        q["rule"] = "doc_valid"
        return q, aged

    def cross_check(self, docs: list[dict], profile, seed: int, bid: str, meta: dict, perturbed: bool,
                    max_pages: int = 10):
        rng = random.Random(f"bench:cross:{bid}")
        groups = perturb.candidates(docs)
        if not groups:
            return
        rng.shuffle(groups)
        for g in groups[:20]:
            di, fi = rng.choice(g)
            others = sorted({d for d, _ in g} - {di})
            pick = [di] + rng.sample(others, min(len(others), rng.randint(1, 2)))
            rest = [i for i in range(len(docs)) if i not in pick]
            if rest and rng.random() < 0.5:  # 대조와 상관없는 서류 한 건
                pick.append(rng.choice(rest))
            while len(pick) > 2 and sum(len(docs[i]["images"]) for i in pick) > max_pages:
                pick.pop()
            if sum(len(docs[i]["images"]) for i in pick) > max_pages:
                continue
            sub = {i: docs[i] for i in pick}
            answer = {"consistent": True, "issues": []}
            kind = None
            if perturbed:
                d, f = docs[di], docs[di]["fields"][fi]
                new = perturb.mutate(f, rng)
                if not new or norm_text(new) == norm_text(f["value"]):
                    continue
                html = perturb.apply(d["html"], d["raw_keys"][fi], f["value"], new)
                if html is None:
                    continue
                raw = [dict(x) for x in d["raw"]]
                raw[fi]["value"] = new
                stem = f"images/bundles/{bid}/{d['doc_id']}_x"
                sub[di] = self.render_doc(d["doc_id"], profile, seed, stem, d["condition"],
                                          aug_key=f"images/bundles/{bid}/{d['doc_id']}", html=html, raw=raw, data=d["data"])
                kind = field_kind(f)
                answer = {"consistent": False,
                          "issues": [{"document": d["name"], "field": f.get("label"), "value": new, "expected": f["value"]}]}
            order = list(sub)
            rng.shuffle(order)
            imgs = [im for i in order for im in sub[i]["images"]]
            self.emit({"id": f"cross_check/{bid}", "task": "cross_check", "images": imgs,
                       "prompt": P_CROSS.format(task=meta["task_name"], n=len(order), pages=len(imgs)),
                       "answer": answer, "eval": {"documents": [sub[i]["name"] for i in order]},
                       "meta": {**meta, "perturbed": perturbed, "kind": kind or "-", "n_docs": len(order)}})
            return


def build(args) -> None:
    out = Path(args.out)
    if out.exists() and any(out.iterdir()) and not args.force:
        sys.exit(f"{out} 가 비어 있지 않습니다. 다시 만들려면 --force")
    reg = load_all()
    if args.types == "all":
        ids = list(reg)
    else:
        ids = []
        for t in args.types.split(","):
            t = t.strip()
            ids += [s.id for s in reg.values() if s.group == t] if t in GROUPS else [t]
    scenarios = list(SCENARIOS) if args.scenarios == "all" else [s.strip() for s in args.scenarios.split(",") if s.strip()]
    bad = [i for i in ids if i not in reg] + [s for s in scenarios if s not in SCENARIOS]
    if bad:
        sys.exit(f"알 수 없는 서류/시나리오: {bad}")
    out.mkdir(parents=True, exist_ok=True)
    for t in (out / "tasks").glob("*.jsonl") if (out / "tasks").exists() else []:
        t.unlink()

    t0 = time.time()
    bd = Builder(out, args.scale)
    try:
        n = len(ids) * args.per_doc
        for k in range(args.per_doc):
            seed = SEED_SINGLE + k
            profile = make_profile(seed)
            for j, doc_id in enumerate(ids):
                stem = f"images/{doc_id}_{seed}"
                r = bd.render_doc(doc_id, profile, seed, stem, pick_condition(f"{doc_id}:{seed}"))
                bd.single(r, stem, args.fields_per_doc, args.max_keys)
                print(f"\r서류 {k * len(ids) + j + 1}/{n}", end="", file=sys.stderr)
        print(file=sys.stderr)
        for si, sc in enumerate(scenarios):
            for b in range(args.bundles):
                bd.bundle(sc, SEED_BUNDLE + list(SCENARIOS).index(sc) * 1000 + b, b)
                print(f"\r업무 묶음 {si * args.bundles + b + 1}/{len(scenarios) * args.bundles}", end="", file=sys.stderr)
        print(file=sys.stderr)
    finally:
        bd.close()
    meta = {"version": VERSION, "generator_commit": _git_rev(), "created": time.strftime("%Y-%m-%d %H:%M:%S"),
            "settings": {"types": args.types, "n_doc_types": len(ids), "per_doc": args.per_doc, "scenarios": scenarios,
                         "bundles": args.bundles, "fields_per_doc": args.fields_per_doc, "max_keys": args.max_keys,
                         "scale": args.scale, "seed_single": SEED_SINGLE, "seed_bundle": SEED_BUNDLE,
                         "conditions": dict(CONDITIONS)},
            "counts": dict(sorted(bd.counts.items())),
            "doc_names": {i: reg[i].name for i in ids}}
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"평가 세트 → {out} ({time.time() - t0:.0f}초)")
    for t, c in meta["counts"].items():
        print(f"  {t:12s} {c}")
