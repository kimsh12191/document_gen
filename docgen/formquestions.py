"""서식의 질문·답 questions.json (서식 폴더, docgen/formdir.py). 이 서식의 질문 껍데기·답 껍데기·무엇을 어떤 항목명으로 묻는지.

질문 전문(prompt)·항목 줄 꼴(line)·답 꼴(answer)까지 서식마다 여기에 적힌다. 공통으로 남는 것은 새 서식의 기본값
(docgen/bench/prompts.py 의 문장), 정답 값·위치를 그린 문서에서 꺼내는 코드(docgen/bench/tasks/<과제>.py), 채점(evaluate.py).
파일이 없으면 공통 기본값 그대로 묻는다 (기본값으로 만든 파일과 결과가 같다).

  {"kie":   {"prompt": "이 문서에서 아래 항목의 값과 위치를 … \n{items}",   질문 전문. {items} 자리에 항목 줄들
             "line": "- {key}: {label}{note}",                     항목 한 줄 꼴. {note} = " (괄호 설명)" 또는 빈칸
             "answer": "list_box",                                 답 꼴: list_box [{key, value, bbox_2d, page}] (값+위치 채점)
                                                                          list [{key, value}] / object {키: 값} (값 채점)
             "others": "ask",                                       목록에 없는 칸: ask 기본대로 묻기 | skip 묻지 않기
             "items": [{"key": "customer.name",                     질문에 쓰는 키 (반복 행은 rows.*.amount)
                        "label": "성명",                            질문의 항목명 (고치면 질문이 바뀜)
                        "note"?: "고객 성명",                        괄호 설명 (없으면 키 사전에서 자동)
                        "ask"?: false,                              이 칸은 묻지 않음
                        "from"?: "applicant.name"}]},               (읽기용) 답을 가져오는 서식 칸 — 키 사전이 정한다
   "marks": {"prompt", "line", "answer": "list_box"|"list", "others", "items": [{"key", "label", "ask"?, "kind", "options"}]},
                                                                    kind·options 는 읽기용
   "ocr_field": {"prompt": "…", "exclude": ["customer.rrn"]},       질문 전문, 값 칸 읽기에서 뺄 칸 (답 = 칸 글자)
   "ocr_page":  {"prompt": "…", "exclude": []},                     질문 전문, 받아쓰기 정답에서 뺄 칸 (답 = 값 줄 목록)
   "classify":  {"prompt": "…", "answer": "대출거래신청서", "aliases": [...]},   질문 전문, 분류 정답·다른 이름
   "extra": [{"id": "amount", "prompt": "대출 신청금액은 얼마입니까? 원 단위 숫자로만 답하세요.",
              "type": "number", "answer": "{loan.amount}", "tol"?: 0},          서식 전용 질문 (과제 form_qa)
             {"id": "guarantor", "prompt": "보증인 성명이 적혀 있습니까? 예/아니오로 답하세요.",
              "type": "yesno", "when": "guarantor.name"},                       적혀 있으면 예
             {"id": "bank", "prompt": "…", "type": "text", "answer": "{bank} {branch}"}]}

- 키의 숫자 칸은 * 로 (rows.0.amount, rows.1.amount → rows.*.amount). 정답 값·위치는 문서를 그릴 때마다 그 칸에서 온다.
- 답 꼴을 바꾸면 질문 문장도 그 꼴로 고친다 (list 면 위치 이야기를 뺌). --check 가 안 맞아 보이면 알려 준다.
- 처음 만들기·새 칸 더하기: python -m docgen.formdir questions <ID>… | --all [--write]   (있는 파일은 새 칸·빠진 칸만 더함)
  공통 문장으로 되돌리기:     python -m docgen.formdir questions <ID>… | --all --write --common-prompt
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
ANSWERS = {"kie": ("list_box", "list", "object"), "marks": ("list_box", "list")}   # 채점이 읽는 답 꼴
WITH_ITEMS = ("kie", "marks")
SHELL = ("prompt", "line", "answer")   # 과제 칸 안에서 질문·답 껍데기 (나머지는 묻는 칸)
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


def common_prompt(task: str) -> str:
    """공통 질문 문장 (새 서식의 기본값). kie·marks 는 {items} 자리가 있는 글."""
    from .bench import prompts as P

    return P.text_of({"kie": P.P_KIE, "marks": P.P_MARKS, "classify": P.P_CLASSIFY,
                      "ocr_field": P.P_OCR_FIELD, "ocr_page": P.P_OCR_PAGE}[task])


def prompt(q: dict | None, task: str, items: str | None = None) -> str:
    """이 서식의 질문 전문. 파일에 prompt 가 없으면 공통 문장. items 는 {items} 자리에 (글자 그대로 바꿔 넣음)."""
    text = ((q or {}).get(task) or {}).get("prompt") or common_prompt(task)
    return text if items is None else text.replace("{items}", items)


def shell(q: dict | None, task: str) -> tuple[str | None, str]:
    """kie·marks 의 (항목 줄 꼴, 답 꼴). 없으면 (None = 공통 꼴, "list_box")."""
    spec = (q or {}).get(task) or {}
    return spec.get("line"), spec.get("answer") or "list_box"


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
    from .bench.prompts import LINE

    return {"kie": {"prompt": common_prompt("kie"), "line": LINE, "answer": "list_box", "others": "ask",
                    "items": _items("kie", docs)},
            "marks": {"prompt": common_prompt("marks"), "line": LINE, "answer": "list_box", "others": "ask",
                      "items": _items("marks", docs)},
            "ocr_field": {"prompt": common_prompt("ocr_field"), "exclude": []},
            "ocr_page": {"prompt": common_prompt("ocr_page"), "exclude": []},
            "classify": {"prompt": common_prompt("classify"), "answer": name, "aliases": aliases}, "extra": []}


def add_new(body: dict, fresh: dict, common_prompts: bool = False) -> tuple[dict, list[str]]:
    """있는 파일에 새로 생긴 칸과 빠진 칸(질문·답 껍데기 등)만 더한다 (사람이 고친 것은 그대로). → (새 본문, 더한 것).
    common_prompts: 질문 문장(prompt)·항목 줄 꼴(line)을 지금 공통 문장으로 바꾼다 (답 꼴은 그대로)."""
    out, added = json.loads(json.dumps(body)), []
    for k in TOP:
        if k not in out:
            out[k] = fresh[k]
            added.append(k)
    for task in ("ocr_field", "ocr_page", "classify", *WITH_ITEMS):
        spec = out[task]
        for k, v in fresh[task].items():
            if k not in spec:
                spec[k] = v
                added.append(f"{task}.{k}")
            elif common_prompts and k in ("prompt", "line") and spec[k] != v:
                spec[k] = v
                added.append(f"{task}.{k} (공통 문장으로)")
        out[task] = {**{k: spec[k] for k in fresh[task] if k in spec}, **spec}   # 칸 차례: 껍데기 먼저
    for task in WITH_ITEMS:
        have = {it["key"] for it in out[task]["items"]}
        for it in fresh[task]["items"]:
            if it["key"] not in have:
                out[task]["items"].append(it)
                added.append(f"{task}:{it['key']}")
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
    for task in ("kie", "marks"):
        spec = body.get(task)
        if spec is None:
            continue
        if not isinstance(spec, dict) or not isinstance(spec.get("items", []), list):
            bad.append(f"{task}: {{\"others\", \"items\": [...]}} 꼴이어야 합니다")
            continue
        if spec.get("others", "ask") not in ("ask", "skip"):
            bad.append(f"{task}.others 는 ask 또는 skip")
        if "prompt" in spec and not (isinstance(spec["prompt"], str) and "{items}" in spec["prompt"]):
            bad.append(f"{task}.prompt 에 항목 줄이 들어갈 자리 {{items}} 가 있어야 합니다")
        if "line" in spec and not (isinstance(spec["line"], str) and "{key}" in spec["line"]):
            bad.append(f"{task}.line 에 {{key}} 가 있어야 합니다 (답의 key 와 맞춰 볼 키)")
        if spec.get("answer", "list_box") not in ANSWERS[task]:
            bad.append(f"{task}.answer 는 {' / '.join(ANSWERS[task])}")
        keys = [it.get("key") if isinstance(it, dict) else None for it in spec.get("items", [])]
        if None in keys or not all(isinstance(k, str) and k for k in keys):
            bad.append(f"{task}.items 의 줄마다 \"key\" 가 있어야 합니다")
        dup = sorted({k for k in keys if keys.count(k) > 1 and k})
        if dup:
            bad.append(f"{task}.items 에 같은 키가 두 번: {dup}")
    for task in ("ocr_field", "ocr_page"):
        spec = body.get(task)
        if spec is not None and not (isinstance(spec, dict) and isinstance(spec.get("exclude", []), list)):
            bad.append(f"{task}: {{\"prompt\": 질문, \"exclude\": [키…]}} 꼴이어야 합니다")
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
    for task in ("kie", "marks", "ocr_field", "ocr_page", "classify"):
        spec = body.get(task) or {}
        if spec.get("prompt") and spec["prompt"] != fresh[task]["prompt"]:
            notes.append(f"{task}: 질문 문장이 공통 문장과 다릅니다 (학습한 문장과 달라 점수가 흔들릴 수 있음. "
                         "되돌리기: --write --common-prompt)")
    for task in WITH_ITEMS:
        spec = body.get(task) or {}
        boxed, text = spec.get("answer", "list_box") == "list_box", spec.get("prompt") or ""
        if boxed and "bbox_2d" not in text:
            problems.append(f"{task}: 답 꼴이 list_box(위치 포함)인데 질문에 bbox_2d(위치) 요청이 없습니다")
        elif not boxed and "bbox_2d" in text:
            problems.append(f"{task}: 답 꼴이 {spec['answer']}(위치 없음)인데 질문이 bbox_2d(위치)를 요청합니다")
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
