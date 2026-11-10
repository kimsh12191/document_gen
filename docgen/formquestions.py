"""서식의 질문 껍데기 questions.json (서식 폴더, docgen/formdir.py): 기본과 **다르게** 할 것만 적는다.

질문·답 한 건 = 질문 문장(이 파일 ⊕ 공통) + 칸마다 한 줄(칸 목록 fields.json 의 칸, 질문 설정 "q") → 답(그린 칸의 값·위치를 답 틀로).
  - 서식 단위(기본 과제의 질문 문장·항목 줄 틀·답 틀·분류 정답)는 이 파일.
  - 이 서식만의 질문은 서식 폴더 qa.py (docgen/formqa.py).
  - 칸 단위(묻지 않기·질문의 항목명·괄호 설명·OCR 빼기)는 fields.json 의 그 칸 "q" (docgen/fieldinfo.py) — 칸 하나 = 한 줄.
기본은 docgen/forms/_common/questions.json 과 칸의 항목명. 아무것도 바꾸지 않은 서식은 파일이 없다.
합친 전체는 서식 카드 FORM.md (docgen/formcard.py) 와 python -m docgen.formdir questions <ID> --show.

  {"kie":   {"prompt": "이 증명서에서 … \\n{items}",                 질문 전문. {items} 자리에 항목 줄들 (없으면 공통)
             "item": "- {key}: {label}{note}",                     질문의 항목 한 줄 틀. {note} = " (괄호 설명)" 또는 빈칸
             "answer": {"key": "{key}", "value": "{value}"},       답 목록의 항목 하나 틀 (공통: + "bbox_2d": "{bbox_2d}", "page": "{page}")
             "answer_empty": {"key": "{key}", "value": null}},     빈 칸(값 없음)일 때의 항목 틀
             (답 틀이 글자면 줄글 답: "answer": "{label}: {value}" → 칸마다 한 줄. 빈 칸 틀이 없으면 {value} 자리에 "없음")
   "marks": {"prompt", "item", "answer", "answer_empty"},          같은 꼴 (체크박스 value = 보기 글자, 도장·서명 = true/false)
   "ocr_field": {"prompt"?}, "ocr_page": {"prompt"?},
   "classify":  {"prompt"?, "answer": "…", "aliases": [...]},     분류 정답·다른 이름 (없으면 키 사전의 문서명)
   "table":     {"<묶음>": {"title"?: "표 제목", "ask"?: false}}}  표(반복 묶음, 키의 행 번호 앞 이름 rows.0.x → rows)마다:
                 질문에서 표를 가리킬 제목 / ask false = 개수가 정해진 격자라 표가 아니라 kie 로 묻기 (guide/benchmark.md 표의 정의)

- 정답 값·위치는 문서를 그릴 때마다 그 칸에서 온다 (파일에 적지 않는다).
- 답 틀을 바꾸면 질문 문장도 그 꼴로 고친다 (위치를 빼면 위치 이야기도 뺌). check 가 안 맞아 보이면 알려 준다.
  python -m docgen.formdir check <ID>                 서식 검사 (질문 설정 포함)
  python -m docgen.formdir questions <ID> --show      합친 전체 (기본 / 이 서식에서 바꿈 표시)
  python -m docgen.formdir questions --all --slim [--write]   기본과 같은 것을 파일에서 지운다 (예전 꼴의 전체 사본 정리)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

NAME = "questions.json"
TOP = ("kie", "marks", "ocr_field", "ocr_page", "classify", "table")
WITH_ITEMS = ("kie", "marks")
PLACES = ("key", "value", "bbox_2d", "page")   # 답 틀에 쓰는 자리 — "{key}" 처럼 값 칸 전체로
TASK_KEYS = {"kie": ("prompt", "item", "answer", "answer_empty"), "marks": ("prompt", "item", "answer", "answer_empty"),
             "ocr_field": ("prompt",), "ocr_page": ("prompt",), "classify": ("prompt", "answer", "aliases")}
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
    """과제의 기본 {"prompt", "item"?, "answer"?, "answer_empty"?}. prompt 는 사람이 읽는 글 (kie·marks 는 {items} 자리)."""
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
    fq: 칸마다 질문 설정 (fields.json 의 q)."""
    if not fq:
        return fields
    out = []
    for f in fields:
        it = field_q(fq, f)
        if it is None:
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


OLD_SHAPES = ("list_box", "list", "object")   # 예전 꼴의 답 꼴 이름 (읽으면 기본 틀)
TEXT_PLACES = ("key", "label", "value")       # 줄글 답 틀에 쓰는 자리


def shell(q: dict | None, task: str) -> tuple[str, dict | str, dict | str]:
    """kie·marks 의 (질문 항목 줄 틀, 답 항목 틀, 빈 칸 답 항목 틀). 서식 파일에 없으면 공통.
    답 틀이 글자면 줄글 답: 칸마다 한 줄 ("{label}: {value}"). 빈 칸 틀이 없으면 {value} 자리에 "없음"."""
    spec, base = (q or {}).get(task) or {}, defaults(task)
    item = spec.get("item") or spec.get("line") or base["item"]
    ans = spec.get("answer")
    if isinstance(ans, str) and ans not in OLD_SHAPES:
        empty = spec.get("answer_empty")
        return item, ans, empty if isinstance(empty, str) else ans.replace("{value}", "없음")
    tpl = lambda k: spec[k] if isinstance(spec.get(k), dict) else base[k]
    return item, tpl("answer"), tpl("answer_empty")


def text_value(value) -> str:
    """줄글 답에 넣는 값: true/false → 있음/없음 (도장·서명), 그 밖은 글자 그대로."""
    return ("있음" if value else "없음") if isinstance(value, bool) else str(value)


def fill_text(tpl: str, empty: str, key: str, label: str | None, value) -> str:
    """줄글 답 한 줄: 틀의 {key}·{label}(없으면 -)·{value} 를 채운다. 값이 None 이면 빈 칸 틀."""
    t = empty if value is None else tpl
    t = t.replace("{key}", key).replace("{label}", label or "-")
    return t if value is None else t.replace("{value}", text_value(value))


def _line_rx(tpl: str, key: str, label: str | None) -> re.Pattern:
    """줄글 틀 → 정규식 ({value} 자리를 잡는다, 띄어쓰기는 느슨하게). 줄 처음이나 문장 끝(. ! ?) 뒤에서 시작하는 것만
    (항목명 '성명' 이 '대표자 성명' 줄에 맞지 않게)."""
    parts = [p for p in re.split(r"(\{(?:key|label|value)\})", tpl.strip()) if p]
    out = []
    for i, part in enumerate(parts):
        if part == "{value}":
            out.append(r"(?P<v>.*?)" if i < len(parts) - 1 else r"(?P<v>[^\n]*?)[ \t]*$")
        elif part in ("{key}", "{label}"):
            out.append(re.escape(key if part == "{key}" else label or "-"))
        else:
            out.append(r"[ \t]*" + r"\s*".join(re.escape(w) for w in part.split()) + r"[ \t]*")   # 띄어쓰기 차이는 봐준다
    return re.compile(r"(?:^|(?<=[.!?。])|(?<=[.!?。] ))[ \t]*" + "".join(out), re.M)


def read_text(text: str, tpl: str, empty: str, labels: dict) -> list[dict]:
    """줄글 답 → [{"key", "value"}] (채점이 JSON 답처럼 읽게). labels: 물은 키 → 항목명 (물은 차례).
    빈 칸 틀에 맞으면 value None. 항목명이 같은 칸(반복 행)이 여럿이면 맞은 줄을 차례대로 하나씩,
    하나뿐이면 맞은 줄 모두 (체크된 보기가 여럿인 칸)."""
    groups: dict = {}
    for key, label in labels.items():
        groups.setdefault(label if "{key}" not in tpl else key, []).append(key)
    out = []
    for keys in groups.values():
        k0, label = keys[0], labels[keys[0]]
        hits = sorted([(m.start(), None) for m in _line_rx(empty, k0, label).finditer(text)]
                      + [(m.start(), m.group("v").strip()) for m in _line_rx(tpl, k0, label).finditer(text)],
                      key=lambda h: (h[0], h[1] is not None))
        seen, vals = set(), []
        for pos, v in hits:   # 빈 칸 틀과 답 틀이 같은 줄에 맞으면 (예: "비고: 없음") 빈 칸으로
            if pos not in seen:
                seen.add(pos)
                vals.append(v)
        if len(keys) == 1:
            out += [{"key": k0, "value": v} for v in vals]
        else:
            out += [{"key": k, "value": v} for k, v in zip(keys, vals)]
    return out


def fill_answer(tpl: dict, empty: dict, key: str, value, where: dict) -> dict:
    """답 항목 하나: 틀의 "{key}"·"{value}"·"{bbox_2d}"·"{page}" 자리를 채운다 (값은 그대로의 꼴: 글자·true/false·좌표 목록·쪽 번호).
    값이 None 이면 빈 칸 틀. 위치가 없으면 위치 자리의 칸은 뺀다."""
    vals = {"key": key, "value": value, **where}
    out = {}
    for name, v in (empty if value is None else tpl).items():
        if isinstance(v, str) and v.startswith("{") and v.endswith("}") and v[1:-1] in PLACES:
            if v[1:-1] in vals:
                out[name] = vals[v[1:-1]]
        else:
            out[name] = v
    return out


def answer_fields(tpl: dict) -> dict:
    """답 틀에서 자리마다 칸 이름: {"key": "key", "value": "value", "bbox_2d": …} (채점이 모델 답을 거꾸로 읽을 때)."""
    return {v[1:-1]: name for name, v in tpl.items() if isinstance(v, str) and v[1:-1] in PLACES and v == "{" + v[1:-1] + "}"}


def default_answer(task: str) -> bool:
    """이 과제의 공통 답 틀이 예전 꼴 그대로인지 (그러면 문항에 틀 표시를 남기지 않는다)."""
    return answer_fields(defaults(task)["answer"]) == {p: p for p in PLACES}


def excluded(q: dict | None, task: str, fields: list[dict], fq: dict | None = None) -> list[dict]:
    """ocr_field·ocr_page: 칸의 q 에 "ocr": false 인 칸을 뺀다."""
    if not fq:
        return fields
    return [f for f in fields if (field_q(fq, f) or {}).get("ocr") is not False]


# ---------------------------------------------------------------------------
# 합친 전체 (서식 카드·--show·검사)
# ---------------------------------------------------------------------------

def seen_fields(doc_id: str, seeds: int = 8) -> list[list[dict]]:
    """여러 seed 로 그린 칸 목록 (위치 없이). 평가·학습 세트의 seed 범위에서 고른다."""
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
            out.append(build_fields(raw))
    return out


MARK_KIND = {"checkbox": "체크박스", "checkbox_multi": "복수 선택", "seal": "도장", "signature": "서명"}


def field_rows(task: str, docs: list[list[dict]]) -> list[dict]:
    """여러 번 그린 문서에서 kie·marks 로 물을 수 있는 칸 (문서 순서, 반복 행은 *):
    [{"key", "label"(그릴 때마다 같으면), "labels", "kind"?, "options"?, "seen": 나온 문서 수, "of": 그린 수}]."""
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
        items = []
        for r in field_rows(task, docs):
            it = fq.get(r.get("from") or r["key"], {})
            items.append({**r, "ask": it.get("ask", True),
                          "q_label": it.get("label") or r["label"], "note": it.get("note"),
                          "changed": sorted(k for k in ("label", "note", "ask") if k in it)})
        item, ans, empty = shell(q, task)
        out[task] = {"prompt": mine.get("prompt") or base["prompt"], "item": item, "answer": ans, "answer_empty": empty,
                     "changed": sorted(k for k in ("prompt", "item", "answer", "answer_empty") if k in mine), "items": items}
    no_ocr = sorted(k for k, it in fq.items() if it.get("ocr") is False)
    for task in ("ocr_field", "ocr_page"):
        mine = q.get(task) or {}
        out[task] = {"prompt": mine.get("prompt") or defaults(task)["prompt"], "exclude": no_ocr,
                     "changed": sorted(k for k in ("prompt",) if k in mine)}
    name, aliases = DIC.doc_name(doc_id, load_all()[doc_id].name)
    mine = q.get("classify") or {}
    out["classify"] = {"prompt": mine.get("prompt") or defaults("classify")["prompt"], "answer": mine.get("answer") or name,
                       "aliases": mine.get("aliases", aliases), "changed": sorted(k for k in ("prompt", "answer", "aliases") if k in mine)}
    return out


def slim(doc_id: str, body: dict, docs: list[list[dict]] | None = None) -> dict:
    """기본과 같은 것을 지운 본문 (예전 꼴의 전체 사본 → 바꾼 것만). 빈 dict 면 파일이 필요 없다."""
    from . import dictionary as DIC
    from .registry import load_all

    out = {}
    for task in WITH_ITEMS:
        spec, base = dict(body.get(task) or {}), defaults(task)
        for k in ("prompt", "item", "answer", "answer_empty"):
            if spec.get(k) == base[k]:
                spec.pop(k)
        if spec.get("line") == base["item"]:   # 예전 꼴 이름
            spec.pop("line")
        if spec.get("answer") == "list_box":
            spec.pop("answer")
        if spec.get("others") == "ask":
            spec.pop("others")
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
    tables = {g: v for g, v in (body.get("table") or {}).items() if v}
    if tables:
        out["table"] = tables
    for k, v in body.items():
        if k not in TOP and v not in ([], {}, None, ""):   # 모르는 항목은 그대로 둔다 (check 가 알려 줌)
            out[k] = v
    return out


def hashes(ids) -> dict[str, str]:
    """데이터셋 기록용: 서식마다 questions.json·qa.py 내용 해시 (둘 다 없는 서식은 빠짐).
    그림을 바꾸지 않으므로 서식 해시와 따로 둔다. qa.py 가 없으면 questions.json 만의 해시 (예전 기록과 같게)."""
    import hashlib

    from . import formqa

    out = {}
    for i in ids:
        p, qa = path(i), formqa.path(i)
        data = (p.read_bytes() if p.exists() else b"") + (b"\0qa.py\0" + qa.read_bytes() if qa.exists() else b"")
        if data:
            out[i] = hashlib.sha256(data).hexdigest()[:16]
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
    if "extra" in body:
        bad.append("extra: 서식 전용 질문은 서식 폴더의 qa.py 에 함수로 적습니다 (견본: python -m docgen.formdir qa <ID> --new)")
    unknown = [k for k in body if k not in TOP and k != "extra"]
    if unknown:
        bad.append(f"모르는 항목 {unknown} (쓸 수 있는 것: {list(TOP)}. 이 서식만의 질문은 qa.py)")
    for task, keys in TASK_KEYS.items():
        spec = body.get(task)
        if isinstance(spec, dict):
            odd = [k for k in spec if k not in keys and k not in ("items", "exclude")]
            if odd:
                hint = {"line": "item", "others": "칸마다 fields.json 의 q.ask"}
                bad.append(f"{task}: 모르는 칸 {odd} (쓸 수 있는 것: {list(keys)}"
                           + "".join(f"; {o} → {hint[o]}" for o in odd if o in hint) + ")")
    for task in WITH_ITEMS:
        spec = body.get(task)
        if spec is None:
            continue
        if not isinstance(spec, dict) or not isinstance(spec.get("items", []), list):
            bad.append(f"{task}: {{\"prompt\"?, \"answer\"?, \"items\": [...]}} 꼴이어야 합니다")
            continue
        if "prompt" in spec and not (isinstance(spec["prompt"], str) and "{items}" in spec["prompt"]):
            bad.append(f"{task}.prompt 에 항목 줄이 들어갈 자리 {{items}} 가 있어야 합니다")
        if "item" in spec and not (isinstance(spec["item"], str) and "{key}" in spec["item"]):
            bad.append(f"{task}.item 에 {{key}} 가 있어야 합니다 (답의 key 와 맞춰 볼 키)")
        if isinstance(spec.get("answer"), str) and spec["answer"] not in OLD_SHAPES:   # 줄글 답 틀
            for k in ("answer", "answer_empty"):
                t = spec.get(k)
                if t is None:
                    continue
                used = PLACE.findall(t) if isinstance(t, str) else []
                if not isinstance(t, str) or not ({"key", "label"} & set(used)) or (k == "answer" and "value" not in used):
                    bad.append(f'{task}.{k}: 줄글 답 틀은 글자이고 {{label}}(또는 {{key}})' + (" 와 {value}" if k == "answer" else "")
                               + ' 가 있어야 합니다 (예: "{label}: {value}")')
                elif set(used) - set(TEXT_PLACES):
                    bad.append(f"{task}.{k}: 줄글 답 틀의 자리는 {{key}}·{{label}}·{{value}} 만 (위치는 넣을 수 없음)")
            continue
        for k in ("answer", "answer_empty"):
            if k not in spec:
                continue
            t = spec[k]
            f = answer_fields(t) if isinstance(t, dict) else {}
            used = [v for v in (t.values() if isinstance(t, dict) else []) if isinstance(v, str) and v.startswith("{") and v.endswith("}")]
            if not isinstance(t, dict) or "key" not in f or (k == "answer" and "value" not in f):
                bad.append(f'{task}.{k} 는 답 항목 하나의 JSON 틀이고 "{{key}}"' + (' 와 "{value}"' if k == "answer" else "")
                           + ' 자리가 있어야 합니다 (예: {"key": "{key}", "value": "{value}"})')
            elif len(used) != len(set(used)) or any(u[1:-1] not in PLACES for u in used):
                bad.append(f"{task}.{k}: 자리는 {', '.join('{' + p + '}' for p in PLACES)} 를 한 번씩만")
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
    t = body.get("table")
    if t is not None:
        if not isinstance(t, dict) or not all(isinstance(v, dict) for v in t.values()):
            bad.append('table: {"<묶음>": {"title": "표 제목", "ask": false}} 꼴이어야 합니다 (묶음 = 키의 행 번호 앞 이름, rows.0.x → rows)')
        else:
            for g, v in t.items():
                odd = set(v) - {"title", "ask"}
                if odd:
                    bad.append(f"table.{g}: 모르는 칸 {sorted(odd)} (쓸 수 있는 것: title, ask)")
                if "title" in v and not (isinstance(v["title"], str) and v["title"].strip()):
                    bad.append(f"table.{g}.title 은 표 제목 글자")
                if "ask" in v and v["ask"] is not False:
                    bad.append(f"table.{g}.ask 는 false 만 (표가 아니라 kie 로 물을 때)")
    c = body.get("classify")
    if c is not None and not (isinstance(c, dict) and isinstance(c.get("answer", ""), str)
                              and isinstance(c.get("aliases", []), list)):
        bad.append('classify: {"answer": 문서명, "aliases": [다른 이름…]} 꼴이어야 합니다')
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
    notes = [] if body is not None else ["questions.json 없음 (질문 문장·답 틀은 모두 기본)"]
    if problems:
        return {"problems": problems, "notes": notes}
    body = body or {}
    docs = docs if docs is not None else seen_fields(doc_id, seeds)
    view = resolved(doc_id, docs)
    for task in WITH_ITEMS:
        v = view[task]
        if "prompt" in v["changed"]:
            notes.append(f"{task}: 질문 문장이 공통 문장과 다릅니다 (학습한 문장과 달라 점수가 흔들릴 수 있음)")
        if isinstance(v["answer"], str):   # 줄글 답
            if "bbox_2d" in v["prompt"]:
                problems.append(f"{task}: 줄글 답에는 위치가 없는데 질문이 bbox_2d(위치)를 요청합니다")
        else:
            names = answer_fields(v["answer"])   # 자리 → 답 틀의 칸 이름
            miss = [n for n in names.values() if f'"{n}"' not in v["prompt"]]
            if miss:
                problems.append(f"{task}: 답 틀의 칸 {miss} 이(가) 질문 문장에 없습니다 — 질문에 답 꼴을 같은 이름으로 적어야 모델이 그 꼴로 답합니다")
            if "bbox_2d" not in names and "bbox_2d" in v["prompt"]:
                problems.append(f"{task}: 답 틀에 위치(bbox_2d)가 없는데 질문이 bbox_2d(위치)를 요청합니다")
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
    from . import formqa

    qa = formqa.check(doc_id, docs)   # 서식 폴더 qa.py (이 서식만의 질문)
    problems += qa["problems"]
    notes += qa["notes"]
    if body and slim(doc_id, body, docs) != body:
        notes.append("questions.json 에 기본과 같은 줄이 있습니다 (정리: python -m docgen.formdir questions <ID> --slim --write)")
    return {"problems": problems, "notes": notes}
