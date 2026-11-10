"""평가 세트 (또는 같은 과제의 학습 데이터) 만들기.

  python -m docgen.bench build --out bench_out [--types all] [--per-doc 1]
  python -m docgen.bench build --split train --out bank_train --per-doc 20 --workers 8
  python -m docgen.bench build --recipe docgen/recipes/<이름>.json --out <폴더>     (studio 레시피, 아래 RECIPE_KEYS)

출력:
  bench_out/
    meta.json                 만든 설정, 과제별 문항 수, 서류명 목록
    images/                   서류 이미지
    crops/                    ocr_field 용 값 칸 이미지
    tasks/<과제>.jsonl         문항: {"id", "task", "images", "prompt", "answer", "eval"?, "meta"}
    swift/<과제>.jsonl, all.jsonl   (--split train 만) ms-swift 학습 레코드: 같은 문항을 질문·정답 대화로
    dataset.json              (--recipe 로 만들 때) 레시피, 생성기 커밋, 평가 세트 버전, 서식 파일 해시

같은 설정이면 언제 만들어도 같은 세트가 나온다 (seed 고정). 평가 세트(test)와 학습 데이터(train)는 서로,
그리고 `python -m docgen generate` 의 seed(0부터)와도 겹치지 않는 seed 범위를 쓴다 (아래 SPLITS).
만든 폴더는 studio 데이터셋(과제 폴더)으로 학습(train/)·평가에 쓴다. 평가 세트와 학습 데이터를 한 번에 만드는 것은 docgen/scripts/make_bank_data.sh,
studio 는 레시피로 이 명령(--recipe)을 돌려 데이터셋으로 등록한다.
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
import time
from pathlib import Path

from ..entities import doc_seed, make_profile
from ..registry import GROUPS, load_all
from ..render import render
from ..schema import build_fields
from . import absent, perturb
from .. import formquestions as FQ
from . import tasks as TASKS
from .tasks import MARK_TYPES, field_kind  # noqa: F401  (field_kind: 예전 import 자리 build.field_kind)

VERSION = "5.1"  # 1.1: 증강 노이즈를 이미지마다 고정 (작업 순서·프로세스 수와 무관), 1.2: 원본 서식 결재란에 직원 도장·서명,
#                  2.0: kie·marks 답에 위치(bbox_2d 0~1000, page) — 값·위치·값+위치 점수. 건강보험료 납부확인서 정산 분할납부
#                       변형이 정한 확률(15%)대로 나오게 고침
#                  3.0: 키 사전(docgen/dictionary) 적용 — 공통 키에 이은 칸은 서식이 달라도 공통 키로 묻고 답함(customer.name …),
#                       분류 정답 = 문서명(같은 문서의 서식이 여러 개여도 하나, 다른 이름도 맞음). 10단계의 공식 대조 html 69종·
#                       값 채우기 변경(빈 칸 무작위 비우기 끔, 금액 단위)도 이 판부터. 2.0 과 kie·marks·분류 점수는 바로 비교하지 않는다
#                  3.1: 원본·가져온 서식의 기타·비고·사유·용도 칸 일부(40%)에 자유 기재 글 + freetext(기타 칸 정리) 과제
#                       (docgen/freetext.py). 그 칸이 있는 서식의 이미지·kie 정답이 3.0 과 다르다
#                  4.0: 표(반복 묶음)를 kie 에서 빼고 표 과제 넷(table 표 추출·table_read 표 그대로 옮기기·table_find 표 찾기·
#                       table_qa 표 질의, guide/reference/benchmark.md "표의 정의"). 빈 답 배우기: kie·table 에 없는 키·열 섞기,
#                       비어 있기도 한 칸 비우기(blank), 값 칸 가림(mask) — NULLS. 서류 한 건 과제의 그림·kie 정답이 3.1 과 다르고
#                       kie 점수는 표 칸이 빠져 3.1 과 바로 비교하지 않는다. 업무 묶음 과제는 그대로
#                  4.1: 원본 서식(hf·img)과 그것을 옮긴 공식 대조 html 서식: 한 묶음(목록)으로 섞이던 표 77종을 표마다 나눔
#                       (키 <묶음>_목록.<행>.<열>), 표가 인쇄된 줄을 넘치면 별지(계속) 쪽에 이어 적음 (realform MORE_ROWS).
#                       그 서식들의 표 문항·쪽 수가 4.0 과 다르다
#                  4.2: 여러 쪽 서류의 서류 한 건 과제를 두 경우로 나눔 — 한 쪽만(view "page": 그 쪽 이미지 하나, 정답도 그 쪽만,
#                       레시피 page_view 비율, 기본 0.5)과 모든 쪽(view "all"). table·table_read 는 넣은 이미지에 보이는 행을
#                       늘 전부 묻는다 ("N쪽에 있는 행만"·"앞에서부터 30행까지만" 으로 자르던 것 없앰). 한 쪽 서류도 30행 넘는
#                       표의 문항이 4.1 과 다르다
#                  5.0: 키는 서식의 키 그대로 (공통 키·키 사전 없앰 — 3.0 에서 공통 키로 바꾸던 칸이 서식의 키로 돌아감).
#                       질문 항목 줄의 괄호는 키 설명이 아니라 표의 행·같은 설명 칸 순번만 ("누구의 무엇" 설명 없앰)
#                  5.1: 서식마다 다른 가짜 고객 (5.0 까지는 같은 순번 k 의 모든 서식이 같은 고객 — entities.doc_seed).
#                       키 동의어 통일(tel→phone, dob→birth 등 6개) 없앰 — 정답 키가 서식 키 그대로. 가린 표 칸(mask)은
#                       table_read 정답에서도 null. 모든 문항의 값이 5.0 과 다르다
# 1.x 세트(값만 있는 답)도 같은 채점기로 채점된다 (evaluate.py 가 두 형식을 다 읽음). 값 점수는 1.x 와 뜻이 같다.
SEED_SINGLE = 1_000_000   # 평가 세트 서류의 고객 seed 시작
# split → (seed 시작,). 서식마다 k 번째 건의 seed = 시작 + start + k, 고객은 그 seed 와 서식 ID 로 (entities.doc_seed)
SPLITS = {"test": (SEED_SINGLE,), "train": (10_000_000,)}

# 촬영 조건 비율: 절반은 깨끗한 원본, 나머지는 스캔·촬영·팩스 증강 (docgen/augment.py)
CONDITIONS = (("clean", 0.5), ("scan", 0.2), ("photo", 0.15), ("fax", 0.15))
# 빈 답 배우기: blank 비어 있기도 한 칸(용도·비고·발급번호 …, docgen/render.py
# OPTIONAL_LABEL)을 칸마다 이 비율로 비움 / mask 서류를 이 비율로 골라 값 칸 1~3개를 검은 상자로 가리고 정답 null.
# 없는 키·열 섞기는 과제 파일의 ABSENT_RATE (kie.py·table.py). 레시피의 "nulls": {"blank": …, "mask": …} 로 바꾼다 (0 이면 끔)
NULLS = {"blank": 0.3, "mask": 0.1}
MASK_FIELDS = (1, 3)
MASK_KINDS = ("name", "rrn", "phone", "account_no", "address", "reg_no")   # 비식별 처리로 흔히 가리는 값 (먼저 고름)
# 레시피(JSON)에서 읽는 항목. 나머지 명령줄 인자와 같은 이름은 그 인자를 덮어쓴다.
RECIPE_KEYS = ("split", "types", "per_doc", "fields_per_doc", "max_keys", "scale", "start",
               "conditions", "exclude", "reviewed_only", "nulls", "page_view")



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


def single_profile(seed: int, nulls: dict | None, doc_id: str):
    """서류 한 건 과제의 고객 (서식마다 다른 고객: entities.doc_seed). 빈 칸 비우기 비율(nulls["blank"])을
    profile.extra 로 렌더링에 넘긴다 (docgen/render.py)."""
    p = make_profile(doc_seed(seed, doc_id))
    if nulls and nulls.get("blank"):
        p.extra["blank_optional"] = nulls["blank"]
    return p


def mask_fields(fields: list[dict], paths: list[Path], key: str, data: dict | None, anchors: list[dict] | None = None) -> list[str]:
    """값 칸 1~3개를 검은 상자로 가리고(그림) 정답을 null 로 (칸 dict 를 바꿈). 가린 키 목록.
    비식별 처리에서 흔히 가리는 값(이름·주민번호·연락처·계좌·주소·등록번호)을 먼저, 자유 기재 글 칸은 빼고.
    같은 칸이 여러 곳에 찍혔으면(anchors, 렌더러가 잰 칸마다의 자리) 모두 가린다 — 한 곳이라도 보이면 정답 null 이 틀리므로."""
    from PIL import Image, ImageDraw

    from .tasks import MARK_TYPES, field_kind

    rng = random.Random(f"bench:mask:{key}")
    written = (data or {}).get("_freetext") or {}
    cand = [f for f in fields if f.get("value") is not None and f.get("bbox") and f["type"] not in MARK_TYPES
            and not f.get("group") and f["value"] not in written and f.get("page", 0) < len(paths)]
    if not cand:
        return []
    pref = [f for f in cand if field_kind(f) in MASK_KINDS] or cand
    pick = rng.sample(pref, min(len(pref), rng.randint(*MASK_FIELDS)))
    by_page: dict[int, list] = {}
    for f in pick:
        spots = [a for a in anchors or [] if a.get("target") == "field" and a.get("key") == f["key"] and a.get("bbox")]
        for a in spots or [f]:
            by_page.setdefault(a.get("page", 0), []).append(a["bbox"])
    for pg, boxes in by_page.items():
        if pg >= len(paths):
            continue
        img = Image.open(paths[pg]).convert("RGB")
        d = ImageDraw.Draw(img)
        for x0, y0, x1, y1 in boxes:
            d.rectangle([x0 - 3, y0 - 3, x1 + 3, y1 + 3], fill=(0, 0, 0))
        img.save(paths[pg])
    for f in pick:
        f["value"], f["masked"] = None, True
        f.pop("norm", None)
    return [f["key"] for f in pick]


class Builder:
    exclude: frozenset = frozenset()
    nulls: dict | None = None   # 빈 답 배우기 (NULLS). bench build 만 켠다 — 카드·studio 미리보기는 None
    page_view: float = 0.0      # 여러 쪽 서류에서 한 쪽만 묻는 비율 (tasks.PAGE_VIEW). bench build 만 켠다 — 카드·미리보기는 모든 쪽
    def __init__(self, out: Path, scale: float, rules: dict | None = None):
        from ..image import ImageRenderer

        self.out = out
        self.conditions = tuple((rules or {}).get("conditions") or CONDITIONS)
        self.exclude = frozenset((rules or {}).get("exclude") or ())   # 레시피의 빼는 서식
        self.nulls = (rules or {}).get("nulls")
        self.page_view = (rules or {}).get("page_view", 0.0)
        self.reg = load_all()
        self.renderer = ImageRenderer(scale=scale).__enter__()
        self.buf: list[dict] = []
        for d in ("crops", "tasks"):
            (out / d).mkdir(parents=True, exist_ok=True)

    def close(self):
        self.renderer.__exit__(None, None, None)

    def emit(self, rec: dict):
        from .tracking import enrich

        self.buf.append(enrich(rec))

    def take(self) -> list[dict]:
        out, self.buf = self.buf, []
        return out

    # ------------------------------------------------------------------
    def render_doc(self, doc_id: str, profile, seed: int, stem: str, cond: str, single: bool = False) -> dict:
        """서류 한 건을 렌더링해 이미지(조건에 따라 증강)와 라벨 필드를 만든다.
        single=True (서류 한 건 과제): 표 구조(tables, table_read 과제)도 읽고, 가림 증강(mask)을 할 수 있다."""
        from PIL import Image

        from ..augment import augment
        from ..cli import _aug_fields

        spec = self.reg[doc_id]
        html, raw, data = render(spec, profile, seed)
        png = self.out / f"{stem}.png"
        png.parent.mkdir(parents=True, exist_ok=True)
        info = self.renderer.render(html, png, tables=single)
        fields = build_fields(raw, info)
        tables = info.get("tables") or []
        masked = []
        if single and self.nulls and random.Random(f"bench:maskdoc:{stem}").random() < self.nulls.get("mask", 0):
            masked = mask_fields(fields, [Path(p) for p in info["images"]], stem, data, info.get("anchors"))
        paths = [Path(p) for p in info["images"]]
        sizes = [(pg["width"], pg["height"]) for pg in info["pages"]]
        if cond != "clean":
            arng = random.Random(f"bench:aug:{stem}")
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
            tables = _aug_tables(tables, tfs)
        hand = spec.group in ("hana", "imported") and bool((data or {}).get("style", {}).get("hand"))
        return {"doc_id": doc_id, "name": spec.name, "group": spec.group, "seed": seed, "condition": cond, "stem": stem,
                "template_variant": (data or {}).get("_template_variant", {"id":"default","name":"기본 레이아웃"}),
                "images": [str(p.relative_to(self.out)) for p in paths], "sizes": sizes, "fields": fields, "tables": tables,
                "raw": raw, "raw_keys": [r["key"] for r in raw], "visible": perturb.visible_keys(html),
                "html": html, "data": data, "writing": "hand" if hand else "print", "masked": masked}

    # ------------------------------------------------------------------
    # 단일 서류 과제
    # ------------------------------------------------------------------
    def single(self, r: dict, stem: str, fields_per_doc: int, max_keys: int):
        """서류 한 건의 과제 문항: 과제 파일(docgen/bench/tasks/<과제>.py)을 차례로 부른다. 질문·정답 만드는 법은 그 파일에."""
        for rec in TASKS.make_single(r, stem, self.out, fields_per_doc, max_keys, self.page_view):
            self.emit(rec)

def _aug_tables(tables: list[dict], tfs: list) -> list[dict]:
    """증강 변환을 표 구조(표·칸 상자)에 적용한 사본 (docgen/cli._aug_fields 와 같게)."""
    out = []
    for t in tables:
        tf = tfs[t["page"]] if t["page"] < len(tfs) else None
        if not tf:
            out.append(t)
            continue
        out.append({**t, "bbox": tf.bbox(t["bbox"]), "rows": [{**r, "cells": [{**c, "bbox": c["bbox"] and tf.bbox(c["bbox"])}
                                                                              for c in r["cells"]]} for r in t["rows"]]})
    return out


def swift_record(rec: dict) -> dict:
    """문항 하나 → ms-swift 학습 레코드 (질문 = 평가 프롬프트, 답 = 정답을 모델 출력 형식으로)."""
    from .runner import oracle_output

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
    """작업 하나(서류 한 건)를 만들고 그 문항들을 돌려준다."""
    _, doc_id, seed, fields_per_doc, max_keys = job
    stem = f"images/{doc_id}_{seed}"
    r = _BD.render_doc(doc_id, single_profile(seed, _BD.nulls, doc_id), seed, stem, pick_condition(f"{doc_id}:{seed}", _BD.conditions),
                       single=True)
    _BD.single(r, stem, fields_per_doc, max_keys)
    return _BD.take()


def load_recipe(path: str | Path, args) -> dict:
    """레시피 JSON 을 읽어 args 를 덮어쓰고, 만들기 규칙(rules: 촬영 조건·빼는 서식·빈 답·한 쪽 보기)을 돌려준다."""
    recipe = json.loads(Path(path).read_text(encoding="utf-8"))
    unknown = set(recipe) - set(RECIPE_KEYS) - {"name", "about", "track", "kind"}
    if unknown:
        sys.exit(f"레시피에 모르는 항목: {sorted(unknown)} (쓸 수 있는 것: {RECIPE_KEYS})")
    for k in ("split", "per_doc", "fields_per_doc", "max_keys", "scale", "start"):
        if k in recipe:
            setattr(args, k, recipe[k])
    if "types" in recipe:
        v = recipe["types"]
        args.types = v if isinstance(v, str) else ",".join(v)
    conds = recipe.get("conditions")
    if isinstance(conds, dict):
        conds = list(conds.items())
    rules = {"conditions": [tuple(c) for c in conds] if conds else None}
    if rules["conditions"] and abs(sum(p for _, p in rules["conditions"]) - 1) > 1e-6:
        sys.exit("레시피 conditions 비율의 합은 1 이어야 합니다")
    rules["exclude"] = sorted(recipe.get("exclude") or [])
    nulls = recipe.get("nulls") or {}
    if not isinstance(nulls, dict) or set(nulls) - set(NULLS) or not all(isinstance(v, (int, float)) and 0 <= v <= 1 for v in nulls.values()):
        sys.exit(f'레시피 nulls 는 {{"blank": 0~1, "mask": 0~1}} 꼴이어야 합니다 (기본 {NULLS})')
    rules["nulls"] = nulls
    if "page_view" in recipe:
        pv = recipe["page_view"]
        if not isinstance(pv, (int, float)) or isinstance(pv, bool) or not 0 <= pv <= 1:
            sys.exit(f"레시피 page_view 는 0~1 이어야 합니다 (여러 쪽 서류에서 한 쪽만 묻는 비율, 기본 {TASKS.PAGE_VIEW})")
        rules["page_view"] = pv
    return {"recipe": recipe, "rules": rules, "exclude": set(recipe.get("exclude") or []),
            "reviewed_only": bool(recipe.get("reviewed_only"))}


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
    rules = dict(rc["rules"]) if rc else {}
    rules["nulls"] = {**NULLS, **(rules.get("nulls") or {}),
                      **{k: v for k, v in (("blank", getattr(args, "blank", None)), ("mask", getattr(args, "mask", None))) if v is not None}}
    rules.setdefault("page_view", TASKS.PAGE_VIEW)
    reg = load_all()
    if args.types == "all":
        ids = list(reg)
    else:
        ids = []
        for t in args.types.split(","):
            t = t.strip()
            if t:
                ids += [s.id for s in reg.values() if s.group == t] if t in GROUPS else [t]
    named = {t.strip() for t in args.types.split(",")}
    ok = reviewed_forms()   # 가져온 서식(실서류 견본 배경)은 검수한 것만 "all"·그룹으로 들어온다. ID 를 직접 적으면 시험용으로 허용
    ids = [i for i in ids if i not in reg or reg[i].group != "imported" or i in ok or i in named]
    if rc and rc["exclude"]:
        ids = [i for i in ids if i not in rc["exclude"]]
    if rc and rc["reviewed_only"]:
        ok = reviewed_forms()
        ids = [i for i in ids if i in ok]
    bad = [i for i in ids if i not in reg]
    if bad:
        sys.exit(f"알 수 없는 서류: {bad}")
    split = getattr(args, "split", "test")
    held_out = sorted(test_only_forms() & set(ids)) if split == "train" else []
    if held_out:   # 평가 전용 서식은 학습 데이터에 넣지 않는다
        ids = [i for i in ids if i not in held_out]
        print(f"평가 전용 서식 {len(held_out)}종은 학습 데이터에서 뺍니다: {', '.join(held_out[:10])}", file=sys.stderr)
    start = getattr(args, "start", 0)
    workers = max(1, getattr(args, "workers", 1))
    seed_single = SPLITS[split][0]
    out.mkdir(parents=True, exist_ok=True)
    for d in ("tasks", "swift"):
        for t in (out / d).glob("*.jsonl") if (out / d).exists() else []:
            t.unlink()

    jobs = [("single", doc_id, seed_single + start + k, args.fields_per_doc, args.max_keys)
            for k in range(args.per_doc) for doc_id in ids]
    n_single = len(ids) * args.per_doc

    t0 = time.time()
    counts: dict[str, int] = {}
    from .tracking import Composition

    tracking = Composition()
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
        for i, recs in enumerate(results):
            for rec in recs:
                write("tasks", rec["task"], rec)
                tracking.add(rec)
                if split == "train":
                    sr = swift_record(rec)
                    write("swift", rec["task"], sr)
                    write("swift", "all", sr)
                counts[rec["task"]] = counts.get(rec["task"], 0) + 1
            print(f"\r서류 {i + 1}/{n_single}", end="", file=sys.stderr)
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
            "settings": {"types": args.types, "n_doc_types": len(ids), "per_doc": args.per_doc, "start": start, "fields_per_doc": args.fields_per_doc,
                         "max_keys": args.max_keys, "scale": args.scale, "seed_single": seed_single,
                         "conditions": dict(CONDITIONS), "held_out_test_only": held_out,
                         "nulls": rules["nulls"], "page_view": rules["page_view"]},
            "counts": dict(sorted(counts.items())), "composition": tracking.result(),
            "doc_names": {i: reg[i].name for i in ids}}
    if rc and rc["exclude"]:
        meta["settings"]["exclude"] = sorted(rc["exclude"])
    if rc:
        meta["recipe"] = rc["recipe"].get("name") or Path(args.recipe).stem
        if rules["conditions"]:
            meta["settings"]["conditions"] = dict(rules["conditions"])
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    if rc:   # 버전 정보 (studio 데이터셋 등록부·설명서가 읽는다)
        from ..preview import source_hash

        used = sorted(set(ids) - rc["exclude"])
        info = {"recipe": rc["recipe"], "recipe_path": str(args.recipe), "generator_commit": meta["generator_commit"],
                "version": VERSION, "created": meta["created"], "counts": meta["counts"], "split": split,
                "form_hashes": {i: source_hash(i, common=False) for i in used if i in reg},
                "question_hashes": FQ.hashes([i for i in used if i in reg]),   # 서식별 질문·답 파일 (그림은 안 바꾼다)
                "absent_catalog_hash": absent.catalog_hash(),   # 없는 키·열 후보 (guide/fields/fields.json)
                "composition": tracking.result()}
        (out / "dataset.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    what = "학습 데이터" if split == "train" else "평가 세트"
    print(f"{what} → {out} ({time.time() - t0:.0f}초)" + (f", ms-swift 학습 파일: {out / 'swift'}" if split == "train" else ""))
    for t, c in meta["counts"].items():
        print(f"  {t:12s} {c}")
