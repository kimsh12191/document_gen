"""서식의 질문 껍데기 questions.json (서식 폴더, docgen/formdir.py): 기본과 **다르게** 할 것만 적는다.

질문·답 한 건 = 질문 문장(이 파일 ⊕ 공통) + 칸마다 한 줄(칸 목록 fields.json 의 칸, 질문 설정 "q") → 답(그린 칸의 값·위치를 답 꼴로).
  - 서식 단위(문장·항목 줄 꼴·답 꼴·전용 질문·분류 정답)는 이 파일.
  - 칸 단위(묻지 않기·질문의 항목명·괄호 설명·OCR 빼기)는 fields.json 의 그 칸 "q" (docgen/fieldinfo.py) — 칸 하나 = 한 줄.
기본은 docgen/forms/_common/questions.json 과 칸의 항목명. 아무것도 바꾸지 않은 서식은 파일이 없다.
합친 전체는 서식 카드 FORM.md (docgen/formcard.py) 와 python -m docgen.formdir questions <ID> --show.

  {"kie":   {"prompt": "이 증명서에서 … \\n{items}",                 질문 전문. {items} 자리에 항목 줄들 (없으면 공통)
             "line": "* {label} → {key}",                          항목 한 줄 꼴. {note} = " (괄호 설명)" 또는 빈칸 (없으면 공통)
             "answer": "object",                                   답 꼴: list_box [{key, value, bbox_2d, page}] (값+위치 채점, 공통)
                                                                          list [{key, value}] / object {키: 값} (값 채점)
             "others": "skip"},                                    q 를 적은 칸만 묻기 (기본 ask: 모든 칸)
   "marks": {"prompt", "line", "answer": "list_box"|"list", "others"},
   "ocr_field": {"prompt"?}, "ocr_page": {"prompt"?},
   "classify":  {"prompt"?, "answer": "…", "aliases": [...]},       분류 정답·다른 이름 (없으면 키 사전의 문서명)
   "extra": [{"id": "amount", "prompt": "대출 신청금액은 얼마입니까? 원 단위 숫자로만 답하세요.",
              "type": "number", "answer": "{loan.amount}", "tol"?: 0},          서식 전용 질문 (과제 form_qa)
             {"id": "guarantor", "prompt": "…", "type": "yesno", "when": "guarantor.name"},   적혀 있으면 예
             {"id": "bank", "prompt": "…", "type": "text", "answer": "{bank} {branch}"}]}

- 정답 값·위치는 문서를 그릴 때마다 그 칸에서 온다 (파일에 적지 않는다).
- 답 꼴을 바꾸면 질문 문장도 그 꼴로 고친다 (list 면 위치 이야기를 뺌). check 가 안 맞아 보이면 알려 준다.
  python -m docgen.formdir check <ID>                 서식 검사 (질문 설정 포함)
  python -m docgen.formdir questions <ID> --show      합친 전체 (기본 / 이 서식에서 바꿈 표시)
  python -m docgen.formdir questions --all --slim [--write]   기본과 같은 것을 파일에서 지운다 (예전 꼴의 전체 사본 정리)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

NAME = "questions.json"
TOP = ("kie", "marks", "ocr_field", "ocr_page", "classify", "extra")
EXTRA_TYPES = ("text", "number", "yesno")
ANSWERS = {"kie": ("list_box", "list", "object"), "marks": ("list_box", "list")}   # 채점이 읽는 답 꼴
WITH_ITEMS = ("kie", "marks")
READ_ONLY = ("from", "kind", "options")   # 예전 꼴 파일의 읽기용 칸 (정리할 때 지움)
PLACE = re.compile(r"\{([^{}]+)\}")
_cache: dict = {}


def path(doc_id: str) -> Path:
    from . import formdir

    return (formdir.folder(doc_id) or formdir.copy_dir(doc_id) or formdir.home(doc_id)) / NAME


def read(doc_id: str) -> dict | None:
    """이 서식의 questions.json (없으면 None). 파일이 바뀌면 다시 읽는다."""
    p = path(doc_id)
    try:
        mt = p.stat().st_mtime_ns
    except OSError:
        return None
    hit = _cache.get(p)
    if hit and hit[0] == mt:
        return hit[1]
    body = json.loads(p.read_text(encoding="utf-8"))
    _cache[p] = (mt, body)
    return body


def pattern(key: str) -> str:
    """반복 행 번호를 * 로: rows.0.amount → rows.*.amount."""
    return re.sub(r"(?<=\.)\d+(?=\.|$)", "*", key)


def _match(key: str, keys) -> bool:
    return key in keys or pattern(key) in keys


# ---------------------------------------------------------------------------
# 기본 (모든 서식 공통: docgen/forms/_common/questions.json)
# ---------------------------------------------------------------------------

def defaults(task: str) -> dict:
    """과제의 기본 {"prompt", "line"?, "answer"?}. prompt 는 사람이 읽는 글 (kie·marks 는 {items} 자리)."""
    from .bench.prompts import DEFAULTS

    return DEFAULTS[task]


def common_prompt(task: str) -> str:
    return defaults(task)["prompt"]


# ---------------------------------------------------------------------------
# 과제가 쓰는 것 (docgen/bench/tasks)
# ---------------------------------------------------------------------------

def field_q(fq: dict | None, f: dict) -> dict | None:
    """그린 칸 f 의 질문 설정 (칸 목록 fields.json 의 q, docgen/fieldinfo.questions)."""
    if not fq:
        return None
    from .fieldinfo import doc_key_of

    return fq.get(doc_key_of(f))


def pick(q: dict | None, task: str, fields: list[dict], fq: dict | None = None) -> list[dict]:
    """kie·marks: 물을 칸만 남기고 항목명·설명을 칸의 q 대로. 문서 순서 그대로.
    fq: 칸마다 질문 설정 (fields.json 의 q). questions.json 의 others: skip 이면 q 를 적은 칸만 묻는다."""
    skip_others = ((q or {}).get(task) or {}).get("others", "ask") == "skip"
    if not fq and not skip_others:
        return fields
    out = []
    for f in fields:
        it = field_q(fq, f)
        if it is None:
            if not skip_others:
                out.append(f)
            continue
        if it.get("ask") is False:
            continue
        g = f
        if it.get("label") and it["label"] != f.get("label"):
            g = {**g, "label": it["label"]}
        if "note" in it:
            g = {**g, "_note": it["note"]}
        out.append(g)
    return out


def prompt(q: dict | None, task: str, items: str | None = None) -> str:
    """이 서식의 질문 전문. 파일에 prompt 가 없으면 공통 문장. items 는 {items} 자리에 (글자 그대로 바꿔 넣음)."""
    text = ((q or {}).get(task) or {}).get("prompt") or common_prompt(task)
    return text if items is None else text.replace("{items}", items)


def shell(q: dict | None, task: str) -> tuple[str | None, str]:
    """kie·marks 의 (항목 줄 꼴, 답 꼴). 없으면 (None = 공통 꼴, 공통 답 꼴)."""
    spec = (q or {}).get(task) or {}
    return spec.get("line"), spec.get("answer") or defaults(task).get("answer", "list_box")


def excluded(q: dict | None, task: str, fields: list[dict], fq: dict | None = None) -> list[dict]:
    """ocr_field·ocr_page: 칸의 q 에 "ocr": false 인 칸을 뺀다."""
    if not fq:
        return fields
    return [f for f in fields if (field_q(fq, f) or {}).get("ocr") is not False]


def field_value(fields: list[dict], key: str):
    """extra 의 {키}: 질문 키(공통 키)나 서식의 원래 키(doc_key)로 찾은 칸."""
    for f in fields:
        if f["key"] == key or f.get("doc_key") == key:
            return f
    return None


# ---------------------------------------------------------------------------
# 합친 전체 (서식 카드·--show·검사)
# ---------------------------------------------------------------------------

def seen_fields(doc_id: str, seeds: int = 8) -> list[list[dict]]:
    """여러 seed 로 그린 칸 목록 (공통 키 적용, 위치 없이). 평가·학습 세트의 seed 범위에서 고른다."""
    from . import dictionary as DIC
    from .bench.build import SPLITS
    from .entities import make_profile
    from .registry import load_all
    from .render import render
    from .schema import build_fields

    spec = load_all()[doc_id]
    out = []
    for start in (SPLITS["test"][0], SPLITS["train"][0]):
        for k in range(seeds):
            _, raw, _ = render(spec, make_profile(start + k), start + k)
            out.append(DIC.apply(doc_id, build_fields(raw)))
    return out


MARK_KIND = {"checkbox": "체크박스", "checkbox_multi": "복수 선택", "seal": "도장", "signature": "서명"}


def field_rows(task: str, docs: list[list[dict]]) -> list[dict]:
    """여러 번 그린 문서에서 kie·marks 로 물을 수 있는 칸 (문서 순서, 반복 행은 *):
    [{"key", "label"(그릴 때마다 같으면), "labels", "from"?, "kind"?, "options"?, "seen": 나온 문서 수, "of": 그린 수}]."""
    from .bench.tasks import kie, marks

    choose = {"kie": kie.items, "marks": marks.items}[task]
    rows: dict[str, dict] = {}
    for fields in docs:
        seen_here = set()
        for f in choose(fields):
            k = pattern(f["key"])
            r = rows.setdefault(k, {"key": k, "labels": [], "seen": 0, "of": len(docs)})
            if f.get("label") not in r["labels"]:
                r["labels"].append(f.get("label"))
            if f.get("doc_key") and f["doc_key"] != f["key"]:
                r.setdefault("from", pattern(f["doc_key"]))
            if task == "marks":
                r.setdefault("kind", MARK_KIND[f["type"]])
                if f.get("options"):
                    r.setdefault("options", [o["text"] for o in f["options"]])
            if k not in seen_here:
                r["seen"] += 1
                seen_here.add(k)
    for r in rows.values():
        r["label"] = r["labels"][0] if len(r["labels"]) == 1 else None
    return list(rows.values())


def resolved(doc_id: str, docs: list[list[dict]] | None = None, seeds: int = 8) -> dict:
    """기본 + 이 서식에서 바꾼 것 = 실제로 쓰이는 전체. 값마다 "바꿈" 여부를 붙인다 (카드·--show)."""
    from . import dictionary as DIC
    from .registry import load_all

    from . import fieldinfo

    q = read(doc_id) or {}
    fq = fieldinfo.questions(doc_id)
    docs = docs if docs is not None else seen_fields(doc_id, seeds)
    out = {}
    for task in WITH_ITEMS:
        base, mine = defaults(task), q.get(task) or {}
        asked_default = mine.get("others", "ask") == "ask"
        items = []
        for r in field_rows(task, docs):
            it = fq.get(r.get("from") or r["key"], {})
            items.append({**r, "ask": it.get("ask", asked_default or bool(it)),
                          "q_label": it.get("label") or r["label"], "note": it.get("note"),
                          "changed": sorted(k for k in ("label", "note", "ask") if k in it)})
        out[task] = {"prompt": mine.get("prompt") or base["prompt"], "line": mine.get("line") or base.get("line"),
                     "answer": mine.get("answer") or base.get("answer", "list_box"), "others": mine.get("others", "ask"),
                     "changed": sorted(k for k in ("prompt", "line", "answer", "others") if k in mine), "items": items}
    no_ocr = sorted(k for k, it in fq.items() if it.get("ocr") is False)
    for task in ("ocr_field", "ocr_page"):
        mine = q.get(task) or {}
        out[task] = {"prompt": mine.get("prompt") or defaults(task)["prompt"], "exclude": no_ocr,
                     "changed": sorted(k for k in ("prompt",) if k in mine)}
    name, aliases = DIC.doc_name(doc_id, load_all()[doc_id].name)
    mine = q.get("classify") or {}
    out["classify"] = {"prompt": mine.get("prompt") or defaults("classify")["prompt"], "answer": mine.get("answer") or name,
                       "aliases": mine.get("aliases", aliases), "changed": sorted(k for k in ("prompt", "answer", "aliases") if k in mine)}
    out["extra"] = q.get("extra") or []
    return out


def slim(doc_id: str, body: dict, docs: list[list[dict]] | None = None) -> dict:
    """기본과 같은 것을 지운 본문 (예전 꼴의 전체 사본 → 바꾼 것만). 빈 dict 면 파일이 필요 없다."""
    from . import dictionary as DIC
    from .registry import load_all

    out = {}
    for task in WITH_ITEMS:
        spec, base = dict(body.get(task) or {}), defaults(task)
        for k, d in (("prompt", base["prompt"]), ("line", base.get("line")), ("answer", base.get("answer", "list_box")),
                     ("others", "ask")):
            if spec.get(k) == d:
                spec.pop(k)
        if spec.get("items"):
            docs = docs if docs is not None else seen_fields(doc_id)
            labels = {r["key"]: r["label"] for r in field_rows(task, docs)}
            items = []
            for it in spec["items"]:
                it = {k: v for k, v in it.items() if k not in READ_ONLY}
                if it.get("label") is not None and it["label"] == labels.get(it["key"]):
                    it.pop("label")
                if it.get("ask") is True:
                    it.pop("ask")
                if set(it) - {"key"}:
                    items.append(it)
            spec["items"] = items
        if not spec.get("items"):
            spec.pop("items", None)
        if spec:
            out[task] = spec
    for task in ("ocr_field", "ocr_page"):
        spec = dict(body.get(task) or {})
        if spec.get("prompt") == defaults(task)["prompt"]:
            spec.pop("prompt")
        if not spec.get("exclude"):
            spec.pop("exclude", None)
        if spec:
            out[task] = spec
    spec = dict(body.get("classify") or {})
    name, aliases = DIC.doc_name(doc_id, load_all()[doc_id].name)
    for k, d in (("prompt", defaults("classify")["prompt"]), ("answer", name), ("aliases", aliases)):
        if spec.get(k) == d:
            spec.pop(k)
    if spec:
        out["classify"] = spec
    if body.get("extra"):
        out["extra"] = body["extra"]
    return out


def hashes(ids) -> dict[str, str]:
    """데이터셋 기록용: 서식마다 questions.json 내용 해시 (없는 서식은 빠짐). 그림을 바꾸지 않으므로 서식 해시와 따로 둔다."""
    import hashlib

    out = {}
    for i in ids:
        p = path(i)
        if p.exists():
            out[i] = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    return out


def write(doc_id: str, body: dict) -> Path | None:
    """본문을 쓴다. 비었으면 (기본과 같으면) 파일을 지운다 → None."""
    p = path(doc_id)
    if not body:
        if p.exists():
            p.unlink()
        return None
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(dump(body), encoding="utf-8")
    tmp.replace(p)
    return p


def dump(body: dict) -> str:
    """사람이 읽기 좋게: 과제 칸마다 한 줄, 묻는 칸·서식 전용 질문은 하나가 한 줄."""
    def one(v):
        return json.dumps(v, ensure_ascii=False)

    def many(items, indent):
        return [f"{indent}{one(it)}" + ("," if i < len(items) - 1 else "") for i, it in enumerate(items)]

    lines = ["{"]
    keys = [k for k in TOP if k in body] + [k for k in body if k not in TOP]
    for n, k in enumerate(keys):
        v, end = body[k], "," if n < len(keys) - 1 else ""
        if isinstance(v, dict) and v:
            lines.append(f" {one(k)}: {{")
            for m, (x, y) in enumerate(v.items()):
                comma = "," if m < len(v) - 1 else ""
                if isinstance(y, list) and y and isinstance(y[0], dict):
                    lines += [f"   {one(x)}: [", *many(y, "     "), f"   ]{comma}"]
                else:
                    lines.append(f"   {one(x)}: {one(y)}{comma}")
            lines.append(f" }}{end}")
        elif isinstance(v, list) and v:
            lines += [f" {one(k)}: [", *many(v, "   "), f" ]{end}"]
        else:
            lines.append(f" {one(k)}: {one(v)}{end}")
    return "\n".join(lines) + "\n}\n"


# ---------------------------------------------------------------------------
# 검사
# ---------------------------------------------------------------------------

def check_body(body) -> list[str]:
    """형식 검사 (그리지 않고). 문제 목록."""
    if not isinstance(body, dict):
        return ["questions.json 은 JSON 객체여야 합니다"]
    bad = []
    unknown = [k for k in body if k not in TOP]
    if unknown:
        bad.append(f"모르는 항목 {unknown} (쓸 수 있는 것: {list(TOP)})")
    for task in WITH_ITEMS:
        spec = body.get(task)
        if spec is None:
            continue
        if not isinstance(spec, dict) or not isinstance(spec.get("items", []), list):
            bad.append(f"{task}: {{\"prompt\"?, \"answer\"?, \"items\": [...]}} 꼴이어야 합니다")
            continue
        if spec.get("others", "ask") not in ("ask", "skip"):
            bad.append(f"{task}.others 는 ask 또는 skip")
        if "prompt" in spec and not (isinstance(spec["prompt"], str) and "{items}" in spec["prompt"]):
            bad.append(f"{task}.prompt 에 항목 줄이 들어갈 자리 {{items}} 가 있어야 합니다")
        if "line" in spec and not (isinstance(spec["line"], str) and "{key}" in spec["line"]):
            bad.append(f"{task}.line 에 {{key}} 가 있어야 합니다 (답의 key 와 맞춰 볼 키)")
        if spec.get("answer", "list_box") not in ANSWERS[task]:
            bad.append(f"{task}.answer 는 {' / '.join(ANSWERS[task])}")
        if spec.get("items"):
            bad.append(f"{task}.items: 칸마다 묻기·항목명·설명은 칸 목록 fields.json 의 그 칸에 \"q\" 로 적습니다 "
                       "(예: {\"q\": {\"ask\": false}}, {\"q\": {\"label\": \"발급 용도\"}})")
    for task in ("ocr_field", "ocr_page"):
        spec = body.get(task)
        if spec is not None and not isinstance(spec, dict):
            bad.append(f"{task}: {{\"prompt\": 질문}} 꼴이어야 합니다")
        elif spec and spec.get("exclude"):
            bad.append(f"{task}.exclude: 뺄 칸은 칸 목록 fields.json 의 그 칸에 \"q\": {{\"ocr\": false}} 로 적습니다")
    for task in ("ocr_field", "ocr_page", "classify"):
        spec = body.get(task)
        if isinstance(spec, dict) and "prompt" in spec and not (isinstance(spec["prompt"], str) and spec["prompt"].strip()):
            bad.append(f"{task}.prompt 가 비었습니다")
    c = body.get("classify")
    if c is not None and not (isinstance(c, dict) and isinstance(c.get("answer", ""), str)
                              and isinstance(c.get("aliases", []), list)):
        bad.append('classify: {"answer": 문서명, "aliases": [다른 이름…]} 꼴이어야 합니다')
    ids = []
    for i, x in enumerate(body.get("extra") or []):
        where = f"extra {i + 1}번째"
        if not isinstance(x, dict):
            bad.append(f"{where}: 객체여야 합니다")
            continue
        ids.append(x.get("id"))
        if not x.get("id") or not re.fullmatch(r"[A-Za-z0-9_.-]+", str(x["id"])):
            bad.append(f"{where}: id 가 없거나 영문·숫자·_.- 가 아닙니다")
        if not x.get("prompt"):
            bad.append(f"{where}: prompt(질문 문장)가 없습니다")
        if x.get("type") not in EXTRA_TYPES:
            bad.append(f"{where}: type 은 {'/'.join(EXTRA_TYPES)}")
        elif x["type"] == "yesno" and not x.get("when"):
            bad.append(f"{where}: yesno 는 when(적혀 있으면 예인 칸 키)이 있어야 합니다")
        elif x["type"] != "yesno" and not (isinstance(x.get("answer"), str) and PLACE.search(x["answer"])):
            bad.append(f"{where}: answer 에 {{칸 키}} 가 있어야 합니다 (예: \"{{loan.amount}}\")")
    dup = sorted({i for i in ids if i and ids.count(i) > 1})
    if dup:
        bad.append(f"extra 에 같은 id 가 두 번: {dup}")
    return bad


def check_dir(d: Path) -> list[str]:
    """서식 폴더의 questions.json 형식 검사 (서식 다시 읽기). 없으면 []."""
    p = Path(d) / NAME
    if not p.exists():
        return []
    try:
        body = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{NAME} JSON 오류: {e.lineno}번째 줄 {e.msg}"]
    return [f"{NAME}: {b}" for b in check_body(body)]


def check(doc_id: str, seeds: int = 8, docs: list[list[dict]] | None = None) -> dict:
    """questions.json 과 칸 목록의 질문 설정(q)이 맞는지: {"problems": [...], "notes": [...]}.
    problems 는 고쳐야 하는 것, notes 는 알아 둘 것."""
    from . import fieldinfo

    body = read(doc_id)
    problems = (check_body(body) if body is not None else []) + fieldinfo.check_q(doc_id)
    notes = [] if body is not None else ["questions.json 없음 (질문 문장·답 꼴은 모두 기본)"]
    if problems:
        return {"problems": problems, "notes": notes}
    body = body or {}
    docs = docs if docs is not None else seen_fields(doc_id, seeds)
    view = resolved(doc_id, docs)
    for task in WITH_ITEMS:
        v = view[task]
        if "prompt" in v["changed"]:
            notes.append(f"{task}: 질문 문장이 공통 문장과 다릅니다 (학습한 문장과 달라 점수가 흔들릴 수 있음)")
        boxed = v["answer"] == "list_box"
        if boxed and "bbox_2d" not in v["prompt"]:
            problems.append(f"{task}: 답 꼴이 list_box(위치 포함)인데 질문에 bbox_2d(위치) 요청이 없습니다")
        elif not boxed and "bbox_2d" in v["prompt"]:
            problems.append(f"{task}: 답 꼴이 {v['answer']}(위치 없음)인데 질문이 bbox_2d(위치)를 요청합니다")
        relabel = [it for it in v["items"] if "label" in it["changed"]]
        if relabel:
            notes.append(f"{task}: 칸의 항목명과 다르게 묻는 칸 {len(relabel)}개: "
                         + ", ".join(f"{it['key']} ('{it['q_label']}' ← 칸 '{it['label']}')" for it in relabel[:5]))
        off = [it["key"] for it in v["items"] if not it["ask"]]
        if off:
            notes.append(f"{task}: 묻지 않는 칸 {len(off)}개: {', '.join(off[:8])}")
    for task in ("ocr_field", "ocr_page", "classify"):
        if "prompt" in view[task]["changed"]:
            notes.append(f"{task}: 질문 문장이 공통 문장과 다릅니다")
    keys = {f["key"] for fs in docs for f in fs} | {f.get("doc_key") for fs in docs for f in fs}
    for x in body.get("extra") or []:
        refs = PLACE.findall(x.get("answer") or "") + ([x["when"]] if x.get("when") else [])
        miss = [r for r in refs if r not in keys]
        if miss:
            problems.append(f"extra {x.get('id')}: 칸에 없는 키 {miss}")
    if body and slim(doc_id, body, docs) != body:
        notes.append("questions.json 에 기본과 같은 줄이 있습니다 (정리: python -m docgen.formdir questions <ID> --slim --write)")
    return {"problems": problems, "notes": notes}
