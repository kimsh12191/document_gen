"""평가 세트 (또는 같은 과제의 학습 데이터) 만들기.

  python -m docgen.bench build --out bench_out [--types all] [--per-doc 1] [--bundles 4]
  python -m docgen.bench build --split train --out bank_train --per-doc 0 --bundles 100 --workers 8
  python -m docgen.bench build --recipe datasets/recipes/<이름>.json --out <폴더>     (studio 레시피, 아래 RECIPE_KEYS)

출력:
  bench_out/
    meta.json                 만든 설정, 과제별 문항 수, 서류명 목록
    images/                   서류 이미지 (단일 서류 과제)
    images/bundles/           업무 묶음 서류 이미지
    crops/                    ocr_field 용 값 칸 이미지
    tasks/<과제>.jsonl         문항: {"id", "task", "images", "prompt", "answer", "eval"?, "meta"}
    swift/<과제>.jsonl, all.jsonl   (--split train 만) ms-swift 학습 레코드: 같은 문항을 질문·정답 대화로
    bundles.jsonl             업무 묶음마다 한 줄: 시나리오, 고객 seed, 서류(이미지·값 위치), 변조 내역, 나온 문항 ID
    dataset.json              (--recipe 로 만들 때) 레시피, 생성기 커밋, 평가 세트 버전, 서식 파일 해시

같은 설정이면 언제 만들어도 같은 세트가 나온다 (seed 고정). 평가 세트(test)와 학습 데이터(train)는 서로,
그리고 `python -m docgen generate` 의 seed(0부터)와도 겹치지 않는 seed 범위를 쓴다.
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
import time
from pathlib import Path

from ..entities import make_profile
from ..registry import GROUPS, SCENARIO_EXTRA, SCENARIO_PROCESSING, SCENARIOS, load_all
from ..render import render
from ..schema import build_fields
from . import perturb
from . import processing as PROCESS
from .metrics import norm_text, normalize_box
from .cases import CASES, OTHER_OK, Ctx
from .prompts import P_CLASSIFY, P_CROSS, P_DOC_CHECK, P_KIE, P_MARKS, P_OCR_FIELD, P_OCR_PAGE, P_REVIEW
from .rules import Bundle, questions, r_doc_valid, valid_candidates

VERSION = "2.0"  # 1.1: 증강 노이즈를 이미지마다 고정 (작업 순서·프로세스 수와 무관), 1.2: 원본 서식 결재란에 직원 도장·서명,
#                  2.0: kie·marks 답에 위치(bbox_2d 0~1000, page) — 값·위치·값+위치 점수. 건강보험료 납부확인서 정산 분할납부
#                       변형이 정한 확률(15%)대로 나오게 고침
# 1.x 세트(값만 있는 답)도 같은 채점기로 채점된다 (evaluate.py 가 두 형식을 다 읽음). 값 점수는 1.x 와 뜻이 같다.
SEED_SINGLE = 1_000_000   # 단일 서류 과제 고객 seed 시작
SEED_BUNDLE = 2_000_000   # 업무 묶음 고객 seed 시작
# split → (단일 서류 seed 시작, 묶음 seed 시작, 시나리오 간 간격). 묶음 i 의 고객 seed = 시작 + 시나리오 번호 × 간격 + i,
# 다른 고객(타인 서류)은 그 seed + 500,000. 학습용은 묶음 수가 많아도 시나리오끼리 겹치지 않게 간격을 넓힌다.
SPLITS = {"test": (SEED_SINGLE, SEED_BUNDLE, 1000), "train": (10_000_000, 20_000_000, 1_000_000)}
OTHER_OFFSET = 500_000

# 촬영 조건 비율: 절반은 깨끗한 원본, 나머지는 스캔·촬영·팩스 증강 (docgen/augment.py)
CONDITIONS = (("clean", 0.5), ("scan", 0.2), ("photo", 0.15), ("fax", 0.15))
MARK_TYPES = ("checkbox", "checkbox_multi", "seal", "signature")
# 업무 묶음 구성 규칙 (레시피의 bundle 로 바꾼다). 기본값 = 예전 상수
BUNDLE_RULES = {
    "missing": [0.3, 0.5, 0.2],   # 빠진 서류 0 / 1 / 2건 비율
    "other_customer": 0.3,        # 필수 서류 하나를 다른 고객 것으로 바꿀 확률
    "extra_doc": 0.35,            # 업무와 상관없는 서류를 끼울 확률
    "tamper": 0.5,                # 대조 사례마다 변조 문항일 확률 (format 사례는 늘 정상)
}
# 레시피(JSON)에서 읽는 항목. 나머지 명령줄 인자와 같은 이름은 그 인자를 덮어쓴다.
RECIPE_KEYS = ("split", "types", "per_doc", "scenarios", "bundles", "fields_per_doc", "max_keys", "scale", "start",
               "conditions", "bundle", "cases", "custom_bundles", "exclude", "reviewed_only")



def test_only_forms() -> set[str]:
    """docgen/catalog.json 에서 '평가 전용'으로 배정한 서식 (studio 검수 탭). 학습 데이터에서 뺀다."""
    p = Path(__file__).resolve().parents[1] / "catalog.json"
    if not p.exists():
        return set()
    return {k for k, v in json.loads(p.read_text(encoding="utf-8")).items() if v.get("split") == "test_only"}


def _git_rev() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=Path(__file__).resolve().parents[2],
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:  # noqa: BLE001
        return None


def pick_condition(key: str, conditions=None) -> str:
    conds = conditions or CONDITIONS
    r = random.Random(f"bench:cond:{key}").random()
    acc = 0.0
    for name, p in conds:
        acc += p
        if r < acc:
            return name
    return conds[0][0]


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
    def __init__(self, out: Path, scale: float, rules: dict | None = None):
        from ..image import ImageRenderer

        self.out = out
        self.rules = {**BUNDLE_RULES, **((rules or {}).get("bundle") or {})}
        self.cases = (rules or {}).get("cases") or {}          # {사례ID: {"enabled": bool, "tamper": 확률}}
        self.conditions = tuple((rules or {}).get("conditions") or CONDITIONS)
        self.reg = load_all()
        self.renderer = ImageRenderer(scale=scale).__enter__()
        self.buf: list[dict] = []
        for d in ("images/bundles", "crops", "tasks"):
            (out / d).mkdir(parents=True, exist_ok=True)

    def close(self):
        self.renderer.__exit__(None, None, None)

    def emit(self, rec: dict):
        self.buf.append(rec)

    def take(self) -> list[dict]:
        out, self.buf = self.buf, []
        return out

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
        hand = spec.group in ("hana", "imported") and bool((data or {}).get("style", {}).get("hand"))
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

        sizes = r["sizes"]

        def where(f, box):   # 정답 위치: 그 쪽 이미지 기준 0~1000, 쪽은 1부터
            pg = f.get("page", 0)
            if not box or pg >= len(sizes):
                return {}
            return {"bbox_2d": normalize_box(box, *sizes[pg]), "page": pg + 1}

        # kie: 항목 목록을 주고 값과 위치 추출
        kf = [f for f in fields if f["type"] not in MARK_TYPES and not f.get("group")
              and not f["key"].startswith(("seal.", "sign."))]
        if len(kf) > max_keys:
            kf = sorted(rng.sample(kf, max_keys), key=kf.index)
        if kf:
            items = "\n".join(f"- {f['key']}: {f.get('label') or '-'}" for f in kf)
            self.emit({"id": f"kie/{sid}", "task": "kie", "prompt": P_KIE.format(items=items),
                       "answer": [{"key": f["key"], "value": f["value"], **(where(f, f.get("bbox")) if f["value"] is not None else {})}
                                  for f in kf],
                       "eval": {"fields": {f["key"]: {"type": f["type"], "norm": f.get("norm"), "kind": field_kind(f)}
                                           for f in kf}}, **base})

        # marks: 체크박스·도장·서명
        mf = [f for f in fields if f["type"] in MARK_TYPES and not f["key"].startswith("seal.untagged")
              and (f["type"] in ("seal", "signature") or f.get("options"))]
        if len(mf) > max_keys:
            mf = sorted(rng.sample(mf, max_keys), key=mf.index)
        if mf:
            lines, ans, types = [], [], {}
            for f in mf:
                lab = f.get("label") or "-"
                if f["type"] in ("checkbox", "checkbox_multi"):
                    kind = "체크박스" if f["type"] == "checkbox" else "복수 선택"
                    lines.append(f"- {f['key']}: {lab} ({kind}, 보기: {' / '.join(o['text'] for o in f['options'])})")
                    on = [o for o in f["options"] if o["checked"]]
                    ans += [{"key": f["key"], "value": o["text"], **where(f, o.get("box_bbox"))} for o in on] or \
                        [{"key": f["key"], "value": None}]
                else:
                    lines.append(f"- {f['key']}: {lab} ({'도장' if f['type'] == 'seal' else '서명'})")
                    ans.append({"key": f["key"], "value": bool(f["present"]), **(where(f, f.get("bbox")) if f["present"] else {})})
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

    def bundle(self, scenario: str, seed: int, plan: dict | None = None):
        """업무 묶음 하나. plan(직접 만든 묶음): {"name", "missing": [서류ID], "other": [서류ID], "extra": [서류ID],
        "cases": [사례ID], "tamper": {사례ID: bool}} — 정해 준 것은 난수 대신 그대로 쓴다."""
        task_name, ids = SCENARIOS[scenario]
        processing = PROCESS.validate(SCENARIO_PROCESSING.get(scenario), ids)
        p = self.bundle_profile(scenario, seed)
        bid = f"{scenario}_{seed}" if not plan or not plan.get("name") else f"{scenario}_{seed}_{plan['name']}"
        docs = []
        for doc_id in ids:
            stem = f"images/bundles/{bid}/{doc_id}"
            docs.append(self.render_doc(doc_id, p, seed, stem, pick_condition(f"{bid}:{doc_id}", self.conditions)))
        meta = {"scenario": scenario, "task_name": task_name, "bundle": bid, "customer": p.person.name}
        first = len(self.buf)
        self.record = {"task": "_bundle", "bundle_id": bid, "scenario": scenario, "task_name": task_name,
                       "customer_seed": seed, "customer": p.person.name, "plan": plan or None,
                       "docs": [self._doc_record(d) for d in docs], "variants": [], "doc_check": None,
                       "processing": processing}

        if processing["doc_check"]:
            self.doc_check(docs, p, seed, bid, meta, plan)
        if processing["cross_check"]:
            self.cross_checks(docs, p, seed, bid, meta, plan=plan)

        # review
        B = Bundle(scenario, {d["doc_id"]: {"name": d["name"], "fields": d["fields"]} for d in docs})
        by_id = {d["doc_id"]: d for d in docs}
        results = PROCESS.execute(processing, by_id)
        self.record["processing_results"] = [{k: v for k, v in row.items() if k != "item"} for row in results]
        for row in results:
            item = row.get("item")
            if not item:
                continue
            imgs = [im for did in item["docs"] for im in by_id[did]["images"]]
            task = item["task"]
            self.emit({"id": f"{task}/{bid}/operation_{row['id']}", "task": task, "images": imgs,
                       "prompt": item.get("prompt") or P_REVIEW.format(task=task_name, pages=len(imgs), question=item["question"]),
                       "answer": item["answer"], "eval": item["eval"],
                       "meta": {**meta, "operation": row["id"], "rule": f"operation:{row['id']}", "skill": "필드 추출" if task == "kie" else "필드 비교"}})
        qs = questions(B, random.Random(f"bench:review:{bid}")) if processing["review"] else []
        qs = [q for q in qs if PROCESS.selected(processing, "rule_ids", q["rule"])]
        if processing["review"] and PROCESS.selected(processing, "rule_ids", "doc_valid") and (dv := self.doc_valid(docs, B, p, seed, bid)) is not None:
            q, aged = dv
            by_id = {**by_id, q["docs"][0]: aged}
            qs.append(q)
        for q in qs:
            imgs = [im for did in dict.fromkeys(q["docs"]) for im in by_id[did]["images"]]
            self.emit({"id": f"review/{bid}/{q['rule']}", "task": "review", "images": imgs,
                       "prompt": P_REVIEW.format(task=task_name, pages=len(imgs), question=q["question"]),
                       "answer": q["answer"], "eval": {"answer_type": q["answer_type"], "tol": q["tol"], **q.get("info", {})},
                       "meta": {**meta, "rule": q["rule"], "skill": q["skill"]}})
        self.record["items"] = [x["id"] for x in self.buf[first:]]
        self.emit(self.record)

    @staticmethod
    def _doc_record(d: dict, why: str = "") -> dict:
        """bundles.jsonl 의 서류 한 건: 이미지와 값 위치 (묶음 상세·고객 일관성 검사에 쓴다)."""
        return {"doc_id": d["doc_id"], "name": d["name"], "images": d["images"], "condition": d["condition"],
                "seed": d["seed"], **({"why": why} if why else {}),
                "fields": [{k: f[k] for k in ("key", "label", "type", "value", "norm", "page", "bbox") if k in f}
                           for f in d["fields"] if not f.get("group")]}

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
        return self.bundle_profile(scenario, seed + OTHER_OFFSET)

    def doc_check(self, docs: list[dict], p, seed: int, bid: str, meta: dict, plan: dict | None = None):
        """빠진 서류 0~2건, 업무와 상관없는 서류 끼워 넣기, 필수 서류 하나를 다른 고객 것으로 바꾸기."""
        rng = random.Random(f"bench:doc_check:{bid}")
        R = self.rules
        if plan and plan.get("missing") is not None:
            missing = [d for d in docs if d["doc_id"] in set(plan["missing"])]
            n_missing = len(missing)
        else:
            n_missing = rng.choices([0, 1, 2], R["missing"])[0]
            n_missing = min(n_missing, len(docs))
            missing = rng.sample(docs, n_missing)
        present = [d for d in docs if d not in missing]
        not_customer, not_required = [], []
        swap = [d for d in present if d["doc_id"] in OTHER_OK]
        forced_other = plan.get("other") if plan and plan.get("other") is not None else None
        if forced_other is not None:
            swap_docs = [d for d in present if d["doc_id"] in set(forced_other)]
        else:
            swap_docs = [rng.choice(swap)] if swap and rng.random() < R["other_customer"] else []
        for d in swap_docs:
            other = self.other_customer(meta["scenario"], seed)
            o = self.render_doc(d["doc_id"], other, other.seed, f"{d['stem']}_other", d["condition"])
            present[present.index(d)] = o
            not_customer.append(o)
        forced_extra = plan.get("extra") if plan and plan.get("extra") is not None else None
        if forced_extra is not None:
            extra_ids = [x for x in forced_extra if x in self.reg]
        elif rng.random() < R["extra_doc"]:
            ids = {d["doc_id"] for d in docs}
            pool = sorted({x for _, (_, lst) in SCENARIOS.items() for x in lst} - ids)
            extra_ids = [rng.choice(pool)] if pool else []
        else:
            extra_ids = []
        for xid in extra_ids:
            stem = f"images/bundles/{bid}/{xid}_extra"
            x = self.render_doc(xid, p, seed, stem, pick_condition(f"{bid}:{xid}", self.conditions))
            present.append(x)
            not_required.append(x)
        rng.shuffle(present)
        required = "\n".join(f"{i + 1}. {d['name']}" for i, d in enumerate(docs))
        answer = {"missing": [d["name"] for d in docs if d in missing or d["doc_id"] in {o["doc_id"] for o in not_customer}],
                  "not_required": [d["name"] for d in not_required], "not_customer": [d["name"] for d in not_customer]}
        if getattr(self, "record", None) is not None:
            self.record["doc_check"] = {"present": [d["doc_id"] for d in present], "missing": [d["doc_id"] for d in missing],
                                        "not_customer": [d["doc_id"] for d in not_customer],
                                        "not_required": [d["doc_id"] for d in not_required]}
            self.record["docs"] += [self._doc_record(d, "other_customer") for d in not_customer]
            self.record["docs"] += [self._doc_record(d, "extra") for d in not_required]
        self.emit({"id": f"doc_check/{bid}", "task": "doc_check", "images": [d["images"][0] for d in present],
                   "prompt": P_DOC_CHECK.format(customer=meta["customer"], task=meta["task_name"], required=required),
                   "answer": answer,
                   "eval": {"required": [d["name"] for d in docs], "names": [d["name"] for d in docs + not_required]},
                   "meta": {**meta, "n_missing": n_missing, "not_customer": bool(not_customer),
                            "not_required": bool(not_required), "n_docs": len(present)}})

    def cross_checks(self, docs: list[dict], p, seed: int, bid: str, meta: dict, max_pages: int = 10,
                     plan: dict | None = None):
        """불일치 사례(cases.py)마다 문항 하나: 절반은 변조, 절반은 정상. 사례에 예/아니오 질문이 있으면 review 문항도."""
        by_id = {d["doc_id"]: d for d in docs}
        ctx = Ctx(by_id, p.person.name)
        other = None
        only = set(plan["cases"]) if plan and plan.get("cases") else None
        forced = (plan or {}).get("tamper") or {}
        processing = PROCESS.validate(SCENARIO_PROCESSING.get(meta["scenario"]), list(by_id))
        for case in CASES:
            conf = self.cases.get(case.id, {})
            if conf.get("enabled") is False or (only is not None and case.id not in only) or not PROCESS.selected(processing, "case_ids", case.id):
                continue
            rng = random.Random(f"bench:case:{bid}:{case.id}")
            if case.category == "format":   # 표기만 다른 사례는 늘 정상 (난수도 뽑지 않는다: 예전과 같은 순서)
                tamper = False
            else:
                x = rng.random()
                tamper = bool(forced[case.id]) if case.id in forced else x < conf.get("tamper", self.rules["tamper"])
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
            if getattr(self, "record", None) is not None:
                changed = []
                for did in plan["docs"]:
                    if shown[did] is not by_id[did]:
                        old = {f["key"]: f for f in by_id[did]["fields"]}
                        diff = [{"key": f["key"], "label": f.get("label"), "old": old.get(f["key"], {}).get("value"),
                                 "new": f.get("value"), "page": f.get("page"), "bbox": f.get("bbox")}
                                for f in shown[did]["fields"] if old.get(f["key"]) and old[f["key"]].get("value") != f.get("value")]
                        changed.append({"doc_id": did, "images": shown[did]["images"],
                                        "kind": "swap" if plan["swap"] == did else "edit", "changes": diff[:20]})
                self.record["variants"].append({"case": case.id, "category": case.category, "item": f"cross_check/{bid}/{case.id}",
                                                "perturbed": bool(issues), "docs": order, "changed": changed})
            self.emit({"id": f"cross_check/{bid}/{case.id}", "task": "cross_check", "images": imgs,
                       "prompt": P_CROSS.format(customer=meta["customer"], task=meta["task_name"], n=len(order),
                                                pages=len(imgs)),
                       "answer": {"consistent": not issues, "issues": issues},
                       "eval": {"documents": [shown[x]["name"] for x in order]}, "meta": m})
            if plan.get("question") and processing["review"]:
                self.emit({"id": f"review/{bid}/case_{case.id}", "task": "review", "images": imgs,
                           "prompt": P_REVIEW.format(task=meta["task_name"], pages=len(imgs),
                                                     question=plan["question"] + " ('예' 또는 '아니오'로만 답하세요)"),
                           "answer": "예" if plan["yes"] else "아니오", "eval": {"answer_type": "yesno", "tol": 0},
                           "meta": {**m, "rule": f"case:{case.id}", "skill": "서류 대조"}})


def swift_record(rec: dict) -> dict:
    """문항 하나 → ms-swift 학습 레코드 (질문 = 평가 프롬프트, 답 = 정답을 모델 출력 형식으로)."""
    from .runner import oracle_output

    if rec["task"] == "cross_check":  # alt_documents 는 채점용 (짝 서류도 정답으로 인정)
        rec = {**rec, "answer": {**rec["answer"], "issues": [
            {k: v for k, v in it.items() if k != "alt_documents"} for it in rec["answer"]["issues"]]}}
    return {"id": rec["id"], "task": rec["task"], "images": rec["images"],
            "messages": [{"role": "user", "content": "<image>" * len(rec["images"]) + rec["prompt"]},
                         {"role": "assistant", "content": oracle_output(rec)}]}


_BD: Builder | None = None


def _init_worker(out: str, scale: float, rules: dict | None = None):
    from multiprocessing.util import Finalize

    global _BD
    _BD = Builder(Path(out), scale, rules)
    Finalize(_BD, _BD.close, exitpriority=10)  # pool.close() 후 작업 프로세스가 끝날 때 브라우저 닫기


def _job(job: tuple) -> list[dict]:
    """작업 하나(서류 한 건 또는 고객 묶음 하나)를 만들고 그 문항들을 돌려준다."""
    if job[0] == "single":
        _, doc_id, seed, fields_per_doc, max_keys = job
        stem = f"images/{doc_id}_{seed}"
        r = _BD.render_doc(doc_id, make_profile(seed), seed, stem, pick_condition(f"{doc_id}:{seed}", _BD.conditions))
        _BD.single(r, stem, fields_per_doc, max_keys)
    else:
        _, sc, seed, *rest = job
        _BD.bundle(sc, seed, rest[0] if rest else None)
        _BD.record = None
    return _BD.take()


def load_recipe(path: str | Path, args) -> dict:
    """레시피 JSON 을 읽어 args 를 덮어쓰고, 묶음 규칙(rules)과 직접 만든 묶음 등을 돌려준다."""
    recipe = json.loads(Path(path).read_text(encoding="utf-8"))
    unknown = set(recipe) - set(RECIPE_KEYS) - {"name", "about", "track", "kind"}
    if unknown:
        sys.exit(f"레시피에 모르는 항목: {sorted(unknown)} (쓸 수 있는 것: {RECIPE_KEYS})")
    for k in ("split", "per_doc", "fields_per_doc", "max_keys", "scale", "start"):
        if k in recipe:
            setattr(args, k, recipe[k])
    for k in ("types", "scenarios"):
        if k in recipe:
            v = recipe[k]
            setattr(args, k, v if isinstance(v, str) else ",".join(v))
    b = recipe.get("bundles")
    if isinstance(b, dict):
        args.bundles = int(b.get("default", 4))
        args.bundles_per = {k: int(v) for k, v in b.items() if k != "default"}
    elif b is not None:
        args.bundles = int(b)
    conds = recipe.get("conditions")
    if isinstance(conds, dict):
        conds = list(conds.items())
    rules = {"bundle": recipe.get("bundle") or {}, "cases": recipe.get("cases") or {},
             "conditions": [tuple(c) for c in conds] if conds else None}
    if rules["conditions"] and abs(sum(p for _, p in rules["conditions"]) - 1) > 1e-6:
        sys.exit("레시피 conditions 비율의 합은 1 이어야 합니다")
    return {"recipe": recipe, "rules": rules, "custom": recipe.get("custom_bundles") or [],
            "exclude": set(recipe.get("exclude") or []), "reviewed_only": bool(recipe.get("reviewed_only"))}


def reviewed_forms() -> set[str]:
    p = Path(__file__).resolve().parents[1] / "catalog.json"
    if not p.exists():
        return set()
    return {k for k, v in json.loads(p.read_text(encoding="utf-8")).items() if v.get("reviewed")}


def build(args) -> None:
    global _BD
    out = Path(args.out)
    if out.exists() and any(out.iterdir()) and not args.force:
        sys.exit(f"{out} 가 비어 있지 않습니다. 다시 만들려면 --force")
    rc = load_recipe(args.recipe, args) if getattr(args, "recipe", None) else None
    rules = rc["rules"] if rc else None
    reg = load_all()
    if args.types == "all":
        ids = list(reg)
    else:
        ids = []
        for t in args.types.split(","):
            t = t.strip()
            if t:   # 빈 목록 = 단일 서류 과제 없이 묶음만
                ids += [s.id for s in reg.values() if s.group == t] if t in GROUPS else [t]
    named = {t.strip() for t in args.types.split(",")}
    ok = reviewed_forms()   # 가져온 서식(실서류 견본 배경)은 검수한 것만 "all"·그룹으로 들어온다. ID 를 직접 적으면 시험용으로 허용
    ids = [i for i in ids if i not in reg or reg[i].group != "imported" or i in ok or i in named]
    if rc and rc["exclude"]:
        ids = [i for i in ids if i not in rc["exclude"]]
    if rc and rc["reviewed_only"]:
        ok = reviewed_forms()
        ids = [i for i in ids if i in ok]
    scenarios = list(SCENARIOS) if args.scenarios == "all" else [s.strip() for s in args.scenarios.split(",") if s.strip()]
    bad = [i for i in ids if i not in reg] + [s for s in scenarios if s not in SCENARIOS]
    if bad:
        sys.exit(f"알 수 없는 서류/시나리오: {bad}")
    split = getattr(args, "split", "test")
    held_out = sorted(test_only_forms() & set(ids)) if split == "train" else []
    if held_out:   # 평가 전용 서식은 학습 데이터의 단일 서류 과제에 넣지 않는다 (업무 묶음의 서류는 시나리오가 정함)
        ids = [i for i in ids if i not in held_out]
        print(f"평가 전용 서식 {len(held_out)}종은 학습 데이터에서 뺍니다: {', '.join(held_out[:10])}", file=sys.stderr)
    start = getattr(args, "start", 0)
    workers = max(1, getattr(args, "workers", 1))
    seed_single, seed_bundle, stride = SPLITS[split]
    per_sc = getattr(args, "bundles_per", None) or {}
    if start + max([args.bundles, *per_sc.values()]) > min(stride, OTHER_OFFSET):
        sys.exit(f"--start + --bundles 는 {min(stride, OTHER_OFFSET)} 이하여야 합니다 (seed 범위)")
    out.mkdir(parents=True, exist_ok=True)
    for d in ("tasks", "swift"):
        for t in (out / d).glob("*.jsonl") if (out / d).exists() else []:
            t.unlink()

    jobs = [("single", doc_id, seed_single + start + k, args.fields_per_doc, args.max_keys)
            for k in range(args.per_doc) for doc_id in ids]
    jobs += [("bundle", sc, seed_bundle + list(SCENARIOS).index(sc) * stride + start + b)
             for sc in scenarios for b in range(per_sc.get(sc, args.bundles))]
    for k, cb in enumerate(rc["custom"] if rc else []):   # 직접 만든 묶음: 정해 준 대로 (DESIGN.md 9.5)
        sc = cb["scenario"]
        if sc not in SCENARIOS:
            sys.exit(f"직접 만든 묶음 {k + 1}: 알 수 없는 시나리오 {sc}")
        seed = int(cb.get("seed", seed_bundle + list(SCENARIOS).index(sc) * stride + start))
        # name 을 "" 로 주면 묶음 ID 가 보통 묶음과 같다 → 같은 seed 로 "다시 만들기" (서식을 고친 뒤 전후 비교)
        plan = {"name": cb.get("name", f"custom{k + 1}"), **{x: cb[x] for x in ("missing", "other", "extra", "cases", "tamper")
                                                             if x in cb}}
        jobs.append(("bundle", sc, seed, plan))
    n_single = len(ids) * args.per_doc

    t0 = time.time()
    counts: dict[str, int] = {}
    files: dict[tuple[str, str], object] = {}

    def write(d: str, t: str, rec: dict):
        if (d, t) not in files:
            (out / d).mkdir(parents=True, exist_ok=True)
            files[d, t] = open(out / d / f"{t}.jsonl", "w", encoding="utf-8")
        files[d, t].write(json.dumps(rec, ensure_ascii=False) + "\n")

    pool = None
    if workers > 1:
        import multiprocessing as mp

        pool = mp.get_context("spawn").Pool(workers, _init_worker, (str(out), args.scale, rules))
        results = pool.imap(_job, jobs)  # 순서 유지: 작업 수와 상관없이 같은 파일이 나온다
    else:
        _BD = Builder(out, args.scale, rules)
        results = map(_job, jobs)
    try:
        bundles_file = open(out / "bundles.jsonl", "w", encoding="utf-8")
        files["_", "bundles"] = bundles_file
        for i, recs in enumerate(results):
            for rec in recs:
                if rec["task"] == "_bundle":   # 묶음 기록은 문항이 아니다
                    bundles_file.write(json.dumps({k: v for k, v in rec.items() if k != "task"}, ensure_ascii=False) + "\n")
                    continue
                write("tasks", rec["task"], rec)
                if split == "train":
                    sr = swift_record(rec)
                    write("swift", rec["task"], sr)
                    write("swift", "all", sr)
                counts[rec["task"]] = counts.get(rec["task"], 0) + 1
            if i < n_single:
                print(f"\r서류 {i + 1}/{n_single}", end="", file=sys.stderr)
            else:
                print(f"\r업무 묶음 {i - n_single + 1}/{len(jobs) - n_single}", end="", file=sys.stderr)
        print(file=sys.stderr)
        if pool:
            pool.close()
            pool.join()
    finally:
        if pool:
            pool.terminate()
        elif _BD:
            _BD.close()
            _BD = None
        for fh in files.values():
            fh.close()
    meta = {"version": VERSION, "split": split, "generator_commit": _git_rev(), "created": time.strftime("%Y-%m-%d %H:%M:%S"),
            "settings": {"types": args.types, "n_doc_types": len(ids), "per_doc": args.per_doc, "scenarios": scenarios,
                         "bundles": args.bundles, "start": start, "fields_per_doc": args.fields_per_doc,
                         "max_keys": args.max_keys, "scale": args.scale, "seed_single": seed_single,
                         "seed_bundle": seed_bundle, "conditions": dict(CONDITIONS), "held_out_test_only": held_out},
            "counts": dict(sorted(counts.items())),
            "doc_names": {i: reg[i].name for i in ids}}
    if rc:
        meta["recipe"] = rc["recipe"].get("name") or Path(args.recipe).stem
        meta["settings"]["bundles_per"] = per_sc
        meta["settings"]["rules"] = {"bundle": {**BUNDLE_RULES, **rules["bundle"]}, "cases": rules["cases"],
                                     "custom_bundles": len(rc["custom"])}
        if rules["conditions"]:
            meta["settings"]["conditions"] = dict(rules["conditions"])
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    if rc:   # 버전 정보 (studio 데이터셋 등록부·설명서가 읽는다)
        from ..preview import source_hash

        used = sorted(set(ids) | {d for sc in scenarios for d in SCENARIOS[sc][1]})
        info = {"recipe": rc["recipe"], "recipe_path": str(args.recipe), "generator_commit": meta["generator_commit"],
                "version": VERSION, "created": meta["created"], "counts": meta["counts"], "split": split,
                "form_hashes": {i: source_hash(i, common=False) for i in used if i in reg}}
        (out / "dataset.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    what = "학습 데이터" if split == "train" else "평가 세트"
    print(f"{what} → {out} ({time.time() - t0:.0f}초)" + (f", ms-swift 학습 파일: {out / 'swift'}" if split == "train" else ""))
    for t, c in meta["counts"].items():
        print(f"  {t:12s} {c}")
