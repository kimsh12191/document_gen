"""서식의 질문·답 questions.json (서식 폴더, docgen/formdir.py). 이 서식에서 무엇을 어떤 항목명으로 묻고 답이 어느 칸인지.

공통은 공통에: 질문 지시문(docgen/bench/prompts.py), 답 구조·고르는 규칙(docgen/bench/tasks/<과제>.py), 채점(evaluate.py).
서식마다 다른 것만 여기에. 파일이 없으면 공통 규칙 그대로 묻는다 (지금 규칙으로 만든 파일과 결과가 같다).

  {"kie":   {"others": "ask",                                       목록에 없는 칸: ask 기본대로 묻기 | skip 묻지 않기
             "items": [{"key": "customer.name",                     질문에 쓰는 키 (반복 행은 rows.*.amount)
                        "label": "성명",                            질문의 항목명 (고치면 질문이 바뀜)
                        "note"?: "고객 성명",                        괄호 설명 (없으면 키 사전에서 자동)
                        "ask"?: false,                              이 칸은 묻지 않음
                        "from"?: "applicant.name"}]},               (읽기용) 답을 가져오는 서식 칸 — 키 사전이 정한다
   "marks": {"others": "ask", "items": [{"key", "label", "ask"?, "kind", "options"}]},   kind·options 는 읽기용
   "ocr_field": {"exclude": ["customer.rrn"]},                      값 칸 읽기에서 뺄 칸
   "ocr_page":  {"exclude": []},                                    받아쓰기 정답에서 뺄 칸
   "classify":  {"answer": "대출거래신청서", "aliases": [...]},       분류 정답·다른 이름
   "extra": [{"id": "amount", "prompt": "대출 신청금액은 얼마입니까? 원 단위 숫자로만 답하세요.",
              "type": "number", "answer": "{loan.amount}", "tol"?: 0},          서식 전용 질문 (과제 form_qa)
             {"id": "guarantor", "prompt": "보증인 성명이 적혀 있습니까? 예/아니오로 답하세요.",
              "type": "yesno", "when": "guarantor.name"},                       적혀 있으면 예
             {"id": "bank", "prompt": "…", "type": "text", "answer": "{bank} {branch}"}]}

- 키의 숫자 칸은 * 로 (rows.0.amount, rows.1.amount → rows.*.amount). 정답 값·위치는 문서를 그릴 때마다 그 칸에서 온다.
- 처음 만들기·새 칸 더하기: python -m docgen.formdir questions <ID>… | --all [--write]   (있는 파일은 새 칸만 더함)
  검사:                       python -m docgen.formdir questions <ID> --check
- 질문 목록은 칸 목록(fields.json·템플릿)과 따로 적힌다. 칸의 항목명을 고쳐도 질문은 그대로이니 여기서도 고친다 (--check 가 알려 줌).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

NAME = "questions.json"
TOP = ("kie", "marks", "ocr_field", "ocr_page", "classify", "extra")
EXTRA_TYPES = ("text", "number", "yesno")
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
# 과제가 쓰는 것 (docgen/bench/tasks)
# ---------------------------------------------------------------------------

def pick(q: dict | None, task: str, fields: list[dict]) -> list[dict]:
    """kie·marks: 물을 칸만 남기고 항목명·설명을 이 서식의 것으로. 문서 순서 그대로."""
    spec = (q or {}).get(task)
    if not spec:
        return fields
    by = {it["key"]: it for it in spec.get("items", [])}
    skip_others = spec.get("others", "ask") == "skip"
    out = []
    for f in fields:
        it = by.get(f["key"]) or by.get(pattern(f["key"]))
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


def excluded(q: dict | None, task: str, fields: list[dict]) -> list[dict]:
    """ocr_field·ocr_page: exclude 에 적은 칸을 뺀다."""
    ex = set(((q or {}).get(task) or {}).get("exclude") or ())
    return [f for f in fields if not _match(f["key"], ex)] if ex else fields


def field_value(fields: list[dict], key: str):
    """extra 의 {키}: 질문 키(공통 키)나 서식의 원래 키(doc_key)로 찾은 칸."""
    for f in fields:
        if f["key"] == key or f.get("doc_key") == key:
            return f
    return None


# ---------------------------------------------------------------------------
# 만들기 (지금 규칙 그대로)
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


def _items(task: str, docs: list[list[dict]]) -> list[dict]:
    from .bench.tasks import kie, marks

    choose = {"kie": kie.items, "marks": marks.items}[task]
    order, labels, extra = [], {}, {}
    for fields in docs:
        for f in choose(fields):
            k = pattern(f["key"])
            if k not in labels:
                order.append(k)
                labels[k] = set()
                extra[k] = {}
            labels[k].add(f.get("label"))
            if f.get("doc_key") and f["doc_key"] != f["key"]:
                extra[k].setdefault("from", pattern(f["doc_key"]))
            if task == "marks":
                extra[k].setdefault("kind", {"checkbox": "체크박스", "checkbox_multi": "복수 선택", "seal": "도장",
                                             "signature": "서명"}[f["type"]])
                if f.get("options"):
                    extra[k].setdefault("options", [o["text"] for o in f["options"]])
    rows = []
    for k in order:
        lab = labels[k]
        # 그릴 때마다 항목명이 같은 칸만 적는다 (레이아웃 변형마다 다르면 비워 두고 그린 대로 묻는다)
        rows.append({"key": k, **({"label": next(iter(lab))} if len(lab) == 1 and None not in lab else {}), **extra[k]})
    return rows


def default(doc_id: str, seeds: int = 8, docs: list[list[dict]] | None = None) -> dict:
    """지금 규칙 그대로의 questions.json (이 파일을 두어도 문항이 바뀌지 않는다)."""
    from . import dictionary as DIC
    from .registry import load_all

    docs = docs if docs is not None else seen_fields(doc_id, seeds)
    name, aliases = DIC.doc_name(doc_id, load_all()[doc_id].name)
    return {"classify": {"answer": name, "aliases": aliases},
            "kie": {"others": "ask", "items": _items("kie", docs)},
            "marks": {"others": "ask", "items": _items("marks", docs)},
            "ocr_field": {"exclude": []}, "ocr_page": {"exclude": []}, "extra": []}


def add_new(body: dict, fresh: dict) -> tuple[dict, list[str]]:
    """있는 파일에 새로 생긴 칸만 더한다 (사람이 고친 줄은 그대로). → (새 본문, 더한 키)."""
    out, added = json.loads(json.dumps(body)), []
    for task in ("kie", "marks"):
        spec = out.setdefault(task, {"others": "ask", "items": []})
        have = {it["key"] for it in spec.setdefault("items", [])}
        for it in fresh[task]["items"]:
            if it["key"] not in have:
                spec["items"].append(it)
                added.append(f"{task}:{it['key']}")
    for k in TOP:
        out.setdefault(k, fresh[k])
    return out, added


def hashes(ids) -> dict[str, str]:
    """데이터셋 기록용: 서식마다 questions.json 내용 해시 (없는 서식은 빠짐). 그림을 바꾸지 않으므로 서식 해시와 따로 둔다."""
    import hashlib

    out = {}
    for i in ids:
        p = path(i)
        if p.exists():
            out[i] = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    return out


def write(doc_id: str, body: dict) -> Path:
    p = path(doc_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(dump(body), encoding="utf-8")
    tmp.replace(p)
    return p


def dump(body: dict) -> str:
    """사람이 읽기 좋게: 항목 하나가 한 줄."""
    def one(v):
        return json.dumps(v, ensure_ascii=False)

    lines = ["{"]
    keys = [k for k in TOP if k in body] + [k for k in body if k not in TOP]
    for n, k in enumerate(keys):
        v, end = body[k], "," if n < len(keys) - 1 else ""
        if isinstance(v, dict) and isinstance(v.get("items"), list):
            head = {x: y for x, y in v.items() if x != "items"}
            lines.append(f' {one(k)}: {{' + "".join(f"{one(x)}: {one(y)}, " for x, y in head.items()) + '"items": [')
            lines += [f"   {one(it)}" + ("," if i < len(v["items"]) - 1 else "") for i, it in enumerate(v["items"])]
            lines.append(f"  ]}}{end}")
        elif isinstance(v, list) and v:
            lines.append(f" {one(k)}: [")
            lines += [f"   {one(it)}" + ("," if i < len(v) - 1 else "") for i, it in enumerate(v)]
            lines.append(f"  ]{end}")
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
    for task in ("kie", "marks"):
        spec = body.get(task)
        if spec is None:
            continue
        if not isinstance(spec, dict) or not isinstance(spec.get("items", []), list):
            bad.append(f"{task}: {{\"others\", \"items\": [...]}} 꼴이어야 합니다")
            continue
        if spec.get("others", "ask") not in ("ask", "skip"):
            bad.append(f"{task}.others 는 ask 또는 skip")
        keys = [it.get("key") if isinstance(it, dict) else None for it in spec.get("items", [])]
        if None in keys or not all(isinstance(k, str) and k for k in keys):
            bad.append(f"{task}.items 의 줄마다 \"key\" 가 있어야 합니다")
        dup = sorted({k for k in keys if keys.count(k) > 1 and k})
        if dup:
            bad.append(f"{task}.items 에 같은 키가 두 번: {dup}")
    for task in ("ocr_field", "ocr_page"):
        spec = body.get(task)
        if spec is not None and not (isinstance(spec, dict) and isinstance(spec.get("exclude", []), list)):
            bad.append(f"{task}: {{\"exclude\": [키…]}} 꼴이어야 합니다")
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


def check(doc_id: str, seeds: int = 8) -> dict:
    """형식 + 지금 칸과 맞는지: {"problems": [...], "notes": [...]}. problems 는 고쳐야 하는 것, notes 는 알아 둘 것."""
    body = read(doc_id)
    if body is None:
        return {"problems": [], "notes": ["questions.json 이 없습니다 (공통 규칙 그대로 묻습니다)"]}
    problems, notes = check_body(body), []
    docs = seen_fields(doc_id, seeds)
    fresh = default(doc_id, docs=docs)
    for task in ("kie", "marks"):
        now = {it["key"]: it for it in fresh[task]["items"]}
        mine = {it["key"]: it for it in (body.get(task) or {}).get("items", []) if isinstance(it, dict)}
        gone = [k for k in mine if k not in now]
        if gone:
            problems.append(f"{task}: 지금 칸에 없는 키 {len(gone)}개: {', '.join(gone[:8])}")
        new = [k for k in now if k not in mine]
        if new:
            how = "묻지 않습니다 (others: skip)" if (body.get(task) or {}).get("others") == "skip" else "기본대로 묻습니다"
            notes.append(f"{task}: 질문 목록에 없는 칸 {len(new)}개 — {how}: {', '.join(new[:8])}"
                         " (더하려면 python -m docgen.formdir questions <ID> --write)")
        diff = [k for k, it in mine.items() if k in now and it.get("label") and now[k].get("label")
                and it["label"] != now[k]["label"]]
        if diff:
            notes.append(f"{task}: 칸의 항목명과 다르게 묻는 칸 {len(diff)}개: "
                         + ", ".join(f"{k} ('{mine[k]['label']}' ← 칸 '{now[k]['label']}')" for k in diff[:5]))
    c = body.get("classify") or {}
    if c.get("answer") and c["answer"] != fresh["classify"]["answer"]:
        notes.append(f"classify: 정답 '{c['answer']}' 가 키 사전의 문서명 '{fresh['classify']['answer']}' 와 다릅니다")
    keys = {f["key"] for fs in docs for f in fs} | {f.get("doc_key") for fs in docs for f in fs}
    for x in body.get("extra") or []:
        if not isinstance(x, dict):
            continue
        refs = PLACE.findall(x.get("answer") or "") + ([x["when"]] if x.get("when") else [])
        miss = [r for r in refs if r not in keys]
        if miss:
            problems.append(f"extra {x.get('id')}: 칸에 없는 키 {miss}")
    return {"problems": problems, "notes": notes}
