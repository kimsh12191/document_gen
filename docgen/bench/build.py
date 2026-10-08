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
from .cases import CASES, OTHER_OK, Ctx
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
P_DOC_CHECK = ("고객 '{customer}' 님이 '{task}' 업무를 위해 서류를 제출했습니다. 첨부 이미지는 제출된 서류의 첫 쪽입니다 "
               "(순서 무관).\n필수 제출 서류:\n{required}\n\n제출 서류를 확인해 다음을 JSON 으로 답하세요.\n"
               "- missing: 필수 서류 중 제출되지 않은 서류. 고객 본인 명의가 아닌 서류만 낸 경우도 제출되지 않은 것으로 봅니다.\n"
               "- not_required: 제출됐지만 필수 서류 목록에 없는 서류\n"
               "- not_customer: 고객 본인 명의가 아닌 서류\n"
               '{{"missing": ["서류명", ...], "not_required": [...], "not_customer": [...]}} 형식으로 답하고, 해당 없으면 빈 목록 [] 으로 '
               "두세요. 서류명은 목록에 있으면 목록 그대로, 없으면 서류에 적힌 제목대로 쓰세요.")
P_CROSS = ("고객 '{customer}' 님이 '{task}' 업무를 위해 제출한 서류 {n}건입니다 (이미지 {pages}장). 서류들을 서로 대조해 "
           "맞지 않는 정보(성명, 주민등록번호, 생년월일, 주소, 연락처, 계좌번호, 상호, 금액, 날짜 등), 업무상 맞지 않는 관계"
           "(계약 상대방이 등기부 소유자가 아님, 금액·날짜 관계 오류 등), 고객 본인 명의가 아닌 서류가 있는지 확인하세요. "
           "표기 방식만 다른 것(날짜 형식, 주민번호 뒷자리 가림, 하이픈 유무 등)은 불일치가 아닙니다.\n"
           '{{"consistent": true 또는 false, "issues": [{{"document": "문제가 있는 서류명", "field": "항목명", '
           '"value": "그 서류에 적힌 값", "expected": "다른 서류에 적힌 값"}}]}} 형식의 JSON 으로 답하세요. '
           '문제가 없으면 {{"consistent": true, "issues": []}} 입니다.')
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
        return {"doc_id": doc_id, "name": spec.name, "group": spec.group, "seed": seed, "condition": cond, "stem": stem,
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
    @staticmethod
    def bundle_profile(scenario: str, seed: int):
        p = make_profile(seed)
        p.extra.update(scenario=scenario, **SCENARIO_EXTRA.get(scenario, {}))
        p.extra["form_bank"] = "하나은행"  # 옛 은행 서식(과거 날짜)이 섞이지 않게
        return p

    def bundle(self, scenario: str, seed: int, b: int):
        task_name, ids = SCENARIOS[scenario]
        p = self.bundle_profile(scenario, seed)
        bid = f"{scenario}_{seed}"
        docs = []
        for doc_id in ids:
            stem = f"images/bundles/{bid}/{doc_id}"
            docs.append(self.render_doc(doc_id, p, seed, stem, pick_condition(f"{bid}:{doc_id}")))
        meta = {"scenario": scenario, "task_name": task_name, "bundle": bid, "customer": p.person.name}

        self.doc_check(docs, p, seed, bid, meta)
        self.cross_checks(docs, p, seed, bid, meta)

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

    def edited(self, d: dict, edits: dict[str, str], stem: str, all_same: bool) -> dict | None:
        """서류 d 의 값 몇 개를 바꿔 다시 렌더링한다 (같은 촬영 조건·증강). all_same 이면 같은 서류 안에서
        같은 값이 찍힌 다른 칸도 함께 바꾼다."""
        html, raw = d["html"], [dict(x) for x in d["raw"]]
        keys = {f["key"]: i for i, f in enumerate(d["fields"])}
        done: set[int] = set()
        for key, new in edits.items():
            if key not in keys or not new:
                return None
            old = d["fields"][keys[key]]["value"]
            idxs = [keys[key]]
            if all_same:
                idxs += [i for i, f in enumerate(d["fields"]) if i != keys[key] and f.get("value") == old
                         and f["type"] not in MARK_TYPES and i < len(d["raw_keys"]) and d["raw_keys"][i] in d["visible"]]
            for i in idxs:
                if i in done:
                    continue
                done.add(i)
                html = perturb.apply(html, d["raw_keys"][i], old, new)
                if html is None:
                    return None
                raw[i]["value"] = new
        return self.render_doc(d["doc_id"], None, d["seed"], stem, d["condition"], aug_key=d["stem"],
                               html=html, raw=raw, data=d["data"])

    def other_customer(self, scenario: str, seed: int):
        return self.bundle_profile(scenario, seed + 500_000)

    def doc_check(self, docs: list[dict], p, seed: int, bid: str, meta: dict):
        """빠진 서류 0~2건, 업무와 상관없는 서류 끼워 넣기, 필수 서류 하나를 다른 고객 것으로 바꾸기."""
        rng = random.Random(f"bench:doc_check:{bid}")
        n_missing = rng.choices([0, 1, 2], [0.3, 0.5, 0.2])[0]
        missing = rng.sample(docs, n_missing)
        present = [d for d in docs if d not in missing]
        not_customer, not_required = [], []
        swap = [d for d in present if d["doc_id"] in OTHER_OK]
        if swap and rng.random() < 0.3:
            d = rng.choice(swap)
            other = self.other_customer(meta["scenario"], seed)
            o = self.render_doc(d["doc_id"], other, other.seed, f"{d['stem']}_other", d["condition"])
            present[present.index(d)] = o
            not_customer.append(o)
        if rng.random() < 0.35:
            ids = {d["doc_id"] for d in docs}
            pool = sorted({x for _, (_, lst) in SCENARIOS.items() for x in lst} - ids)
            if pool:
                xid = rng.choice(pool)
                stem = f"images/bundles/{bid}/{xid}_extra"
                x = self.render_doc(xid, p, seed, stem, pick_condition(f"{bid}:{xid}"))
                present.append(x)
                not_required.append(x)
        rng.shuffle(present)
        required = "\n".join(f"{i + 1}. {d['name']}" for i, d in enumerate(docs))
        answer = {"missing": [d["name"] for d in docs if d in missing or d["doc_id"] in {o["doc_id"] for o in not_customer}],
                  "not_required": [d["name"] for d in not_required], "not_customer": [d["name"] for d in not_customer]}
        self.emit({"id": f"doc_check/{bid}", "task": "doc_check", "images": [d["images"][0] for d in present],
                   "prompt": P_DOC_CHECK.format(customer=meta["customer"], task=meta["task_name"], required=required),
                   "answer": answer,
                   "eval": {"required": [d["name"] for d in docs], "names": [d["name"] for d in docs + not_required]},
                   "meta": {**meta, "n_missing": n_missing, "not_customer": bool(not_customer),
                            "not_required": bool(not_required), "n_docs": len(present)}})

    def cross_checks(self, docs: list[dict], p, seed: int, bid: str, meta: dict, max_pages: int = 10):
        """불일치 사례(cases.py)마다 문항 하나: 절반은 변조, 절반은 정상. 사례에 예/아니오 질문이 있으면 review 문항도."""
        by_id = {d["doc_id"]: d for d in docs}
        ctx = Ctx(by_id, p.person.name)
        other = None
        for case in CASES:
            rng = random.Random(f"bench:case:{bid}:{case.id}")
            tamper = case.category != "format" and rng.random() < 0.5
            plan = case.fn(ctx, tamper, rng)
            if not plan or sum(len(by_id[x]["images"]) for x in plan["docs"]) > max_pages:
                continue
            shown = {}
            for did in plan["docs"]:
                d = by_id[did]
                stem = f"{d['stem']}_{case.id}"
                if plan["swap"] == did:
                    other = other or self.other_customer(meta["scenario"], seed)
                    shown[did] = self.render_doc(did, other, other.seed, stem, d["condition"])
                elif did in plan["edits"]:
                    shown[did] = self.edited(d, plan["edits"][did], stem, all_same=case.category in ("amount", "logic"))
                else:
                    shown[did] = d
            if any(v is None for v in shown.values()):
                continue
            issues = []
            if plan["issue"]:
                it = plan["issue"]
                new_f = next((f for f in shown[it["doc"]]["fields"] if f["key"] == it["key"]), None)
                old_f = next((f for f in by_id[it["doc"]]["fields"] if f["key"] == it["key"]), None)
                if not new_f or not old_f or norm_text(new_f["value"]) == norm_text(old_f["value"]):
                    continue
                issues.append({"document": by_id[it["doc"]]["name"], "field": old_f.get("label"),
                               "value": new_f["value"], "expected": old_f["value"],
                               "alt_documents": [by_id[a]["name"] for a in it.get("alt", [])]})
            order = list(plan["docs"])
            rng.shuffle(order)
            imgs = [im for x in order for im in shown[x]["images"]]
            m = {**meta, "case": case.id, "category": case.category, "perturbed": bool(issues), "n_docs": len(order)}
            self.emit({"id": f"cross_check/{bid}/{case.id}", "task": "cross_check", "images": imgs,
                       "prompt": P_CROSS.format(customer=meta["customer"], task=meta["task_name"], n=len(order),
                                                pages=len(imgs)),
                       "answer": {"consistent": not issues, "issues": issues},
                       "eval": {"documents": [shown[x]["name"] for x in order]}, "meta": m})
            if plan.get("question"):
                self.emit({"id": f"review/{bid}/case_{case.id}", "task": "review", "images": imgs,
                           "prompt": P_REVIEW.format(task=meta["task_name"], pages=len(imgs),
                                                     question=plan["question"] + " ('예' 또는 '아니오'로만 답하세요)"),
                           "answer": "예" if plan["yes"] else "아니오", "eval": {"answer_type": "yesno", "tol": 0},
                           "meta": {**m, "rule": f"case:{case.id}", "skill": "서류 대조"}})

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
