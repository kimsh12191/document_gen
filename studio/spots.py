"""① 서식 › 자리·템플릿 (html·코드 서식): 값이 나올 수 있는 모든 자리, 그 자리를 정한 곳, 템플릿·값 출처 고치기.

  spots(doc_id, render, seed, heavy, template=None, variant="default", values=None)
      → {label: 공란으로 그린 그림 (+ texts: 인쇄된 글자 박스), spots: 그 그림의 자리, keys: 키마다 (이 그림에 몇 번 · 다른 고객·
         특수 상황에서만 나옴 · 한 번도 안 나옴, 예시 값, 정한 곳 = 템플릿 줄·fields.json 줄·값 출처, 이 키가 없는 레이아웃),
         template: 템플릿 글, file, layouts, diff: 초안이면 저장본 대비 빠진·생긴 키}
      template·values 는 저장하지 않은 초안 (values: [{pattern, source, text?, choices?}] = 바꿀 값 출처)
  save(doc_id, render, template, variant, values) → 문법·그리기 검사 뒤 템플릿과 값 출처를 함께 저장

html 서식의 자리는 템플릿의 f("키") 가 정한다. 문서마다 글꼴·행 수·쪽이 바뀌어 위치를 다시 계산하므로, 이 화면은 자리를 끌어
옮기지 않고 그 자리를 정한 템플릿 줄로 데려간다 (원본 서식은 그림 위 고정 자리라 영역 편집, studio/editor.py).
레이아웃 변형(template_variants)이 있으면 고른 레이아웃의 템플릿을 그리고 고친다 (기본 = look/template.html.j2).
render 는 docgen.preview.Previewer.render 꼴.
"""
from __future__ import annotations

import copy
import re

# 기본 그림 말고 더 그려 보는 것: 고객 seed 를 바꿔 (조건 칸), 내용 많음·특수 상황을 켜서 (반복 행·드문 칸)
PROBES = [(1, "default", "default"), (2, "default", "default"), (3, "default", "default"), (0, "on", "on")]
_ARG = re.compile(r"""\b(?:f|choice|agree)\(\s*["']([^"']+)["']""")


def raw_pattern(key: str) -> str:
    """반복 행 번호만 * (템플릿에 적힌 이름 그대로)."""
    return re.sub(r"(?<=\.)\d+(?=\.|$)", "*", key)


def template_file(doc_id: str, variant: str = "default"):
    """그 레이아웃의 템플릿 파일. 기본은 서식 폴더의 look/template.html.j2, 변형은 variants/<변형>.html.j2."""
    from docgen import formdir
    from docgen.registry import load_all

    spec = load_all().get(doc_id)
    if spec is None:
        raise KeyError(f"알 수 없는 서식: {doc_id}")
    if spec.template == "_real_form.html.j2":
        raise ValueError("원본 서식은 템플릿이 없습니다. 영역 편집에서 그림 위 자리를 고칩니다")
    if variant != "default":
        from docgen import template_variants as T

        if variant not in {r["id"] for r in T.load(doc_id)["variants"]}:
            raise ValueError(f"없는 레이아웃: {variant}")
        return T.folder(doc_id) / f"{variant}.html.j2"
    p = formdir.template(doc_id)
    if p is None or not p.exists():
        raise ValueError("템플릿 파일이 없습니다")
    return p


def layouts(doc_id: str) -> list[dict]:
    from docgen import template_variants as T

    return [{"id": r["id"], "name": r.get("name") or r["id"], "enabled": r.get("enabled", True)} for r in T.load(doc_id)["variants"]] \
        or [{"id": "default", "name": "기본 레이아웃", "enabled": True}]


def template_line(text: str, pat: str) -> int | None:
    """그 키를 정한 템플릿 줄 (1부터). 반복 행 키는 끝 이름이 따옴표로 적힌 줄, 없으면 목록 이름이 적힌 줄."""
    lines = text.splitlines()

    def find(rx):
        return next((n for n, ln in enumerate(lines, 1) if re.search(rx, ln)), None)
    if "*" not in pat:
        hit = find(r"""["']%s["']""" % re.escape(pat))
        if hit is None and pat.startswith(("seal.", "sign.")):   # m.seal(…, key="company") → seal.company
            hit = find(r"""key\s*=\s*["']%s["']""" % re.escape(pat.split(".", 1)[1]))
        return hit
    last, head = pat.rsplit("*.", 1)[-1], pat.split(".*")[0].rsplit(".", 1)[-1]
    return find(r"""["']\.?%s["']""" % re.escape(last)) or find(r"""["']%s["']""" % re.escape(head))


def _keys_of(label: dict) -> set[str]:
    return {raw_pattern(k) for k in label.get("raw_keys", [])} | {raw_pattern(a["key"]) for a in label.get("anchors", [])}


# ---------------------------------------------------------------------------
# 값 출처 (칸 목록 fields.json)
# ---------------------------------------------------------------------------

def apply_value(body: dict, pattern: str, source: str, text: str | None = None, choices: list | None = None,
                code: bool = False) -> dict:
    """칸 목록 body 에 키 하나의 값 출처를 적는다 (반복 행 키 '목록.*.칸' 은 lists.<목록>.fields.<칸>). body 를 고쳐 돌려준다.
    source: profile.<경로> · rule:<종류> (rule:fixed 는 text, rule:choice 는 choices) · code (코드 서식: 생성 함수 값 그대로)."""
    if not (source.startswith(("profile.", "rule:")) or (code and source == "code")):
        raise ValueError("값 출처는 profile.<경로> · rule:<종류>" + (" · code" if code else ""))
    if source == "rule:fixed" and not (text or "").strip():
        raise ValueError(f"{pattern}: rule:fixed 는 고정 글자가 필요합니다")
    if source == "rule:choice" and not [c for c in choices or [] if str(c).strip()]:
        raise ValueError(f"{pattern}: rule:choice 는 보기가 하나 이상 필요합니다")
    if ".*." in pattern:
        name, leaf = pattern.split(".*.", 1)
        lst = (body.get("lists") or {}).get(name)
        if lst is None:
            raise ValueError(f"반복 표 '{name}' 이 칸 목록에 없습니다. 템플릿의 반복 행과 fields.json 의 lists 를 먼저 맞추세요")
        slot = lst.setdefault("fields", {}).setdefault(leaf, {})
    else:
        slot = body.setdefault("fields", {}).setdefault(pattern, {})
    slot["source"] = source
    for k, v in (("text", text if source == "rule:fixed" else None),
                 ("choices", [str(c).strip() for c in choices or [] if str(c).strip()] if source == "rule:choice" else None)):
        if v:
            slot[k] = v
        else:
            slot.pop(k, None)
    return body


def _with_values(doc_id: str, values: list | None) -> dict | None:
    """저장된 칸 목록에 바꿀 값 출처(values)를 얹은 것. values 가 없으면 None."""
    from docgen import formfields
    from docgen.registry import load_all

    if not values:
        return None
    code = not load_all()[doc_id].template.startswith("@form/")
    body = copy.deepcopy(formfields.read(doc_id) or {"fields": {}})
    for v in values:
        apply_value(body, v["pattern"], v["source"], v.get("text"), v.get("choices"), code)
    return body


def set_value(doc_id: str, pattern: str, source: str, text: str | None = None, choices: list | None = None) -> dict:
    """값 출처 하나를 바로 저장 (API 호환). 화면은 save() 로 템플릿과 함께 저장한다."""
    from docgen import formfields

    template_file(doc_id)   # html·코드 서식만
    formfields.write(doc_id, _with_values(doc_id, [{"pattern": pattern, "source": source, "text": text, "choices": choices}]))
    return {"saved": True, "pattern": pattern, "source": source}


# ---------------------------------------------------------------------------
# 자리 모으기
# ---------------------------------------------------------------------------

def _renders(doc_id: str, render, seed: int, heavy: str, draft: dict, form: bool, variant: str):
    """(기본 그림 라벨, [(이름, 라벨)…]). html 서식(복제·분석기)은 내용 많음 대신 반복 행 최대."""
    extra = {"template_variants": {doc_id: variant}}

    def one(s, h, sp, texts=False):
        return render(doc_id, s, "default" if form else h, sp, draft={**draft, **({"texts": True} if texts else {})},
                      extra=extra, rows="max" if (form and h == "on") else None)
    base = one(seed, heavy, heavy, texts=True)   # 내용 많음이면 특수 상황도 (드문 칸까지)
    return base, [(f"고객 seed {seed + d}" + (" · 내용 많음" if h == "on" else ""), one(seed + d, h, sp)) for d, h, sp in PROBES
                  if (d, h) != (0, heavy)]


def _draft(text: str | None, saved: str, variant: str, fields: dict | None) -> dict:
    d = {"blank": True}
    if text is not None and text != saved:
        d["template"] = text
        if variant != "default":
            d["variant"] = variant
    if fields is not None:
        d["fields"] = fields
    return d


def spots(doc_id: str, render, seed: int = 0, heavy: str = "default", template: str | None = None,
          variant: str = "default", values: list | None = None) -> dict:
    from docgen import fieldinfo, formfields
    from docgen.registry import load_all

    spec = load_all()[doc_id]
    form = spec.template.startswith("@form/")
    path = template_file(doc_id, variant)
    saved = path.read_text(encoding="utf-8")
    text = saved if template is None else template
    fields = _with_values(doc_id, values)
    base, probes = _renders(doc_id, render, seed, heavy, _draft(text, saved, variant, fields), form, variant)
    scale = base.get("scale", 2)
    spot_list = [{"key": a["key"], "pattern": raw_pattern(a["key"]), "target": a.get("target", "field"),
                  "occurrence": a.get("occurrence", 0), "option": a.get("option"), "page": a["page"],
                  "rect": [round(v / scale, 1) for v in a["bbox"]], "text": a.get("text") or "", "label": a.get("label")}
                 for a in base.get("anchors", [])]
    texts = [{"page": t["page"], "text": t["text"], "blk": t.get("blk"), "rect": [round(v / scale, 1) for v in t["bbox"]]}
             for t in base.get("texts", [])]
    info = {}   # 키마다 항목명·종류·예시 값
    for name, lab in [("기본", base), *probes]:
        for f in lab.get("fields", []) + [{"key": k} for k in lab.get("raw_keys", [])]:
            pat = raw_pattern(f["key"])
            e = info.setdefault(pat, {"label": None, "type": None, "examples": [], "seen": []})
            e["label"] = e["label"] or f.get("label")
            e["type"] = e["type"] or f.get("type")
            v = f.get("value")
            if v not in (None, "") and len(e["examples"]) < 3 and str(v) not in e["examples"]:
                e["examples"].append(str(v))
            if name not in e["seen"]:
                e["seen"].append(name)
    declared = {raw_pattern(a) for a in _ARG.findall(text)}
    entries = fieldinfo.entries(doc_id)
    for pat in declared | {raw_pattern(p) for p in entries}:
        info.setdefault(pat, {"label": None, "type": None, "examples": [], "seen": []})
    in_base = {}
    for s in spot_list:
        in_base[s["pattern"]] = in_base.get(s["pattern"], 0) + 1
    body = fields if fields is not None else (formfields.read(doc_id) or {})

    def stored(pat):   # 칸 목록에 적힌 값 출처 (반복 행 키는 lists.<목록>.fields.<칸>)
        if ".*." in pat:
            name, leaf = pat.split(".*.", 1)
            return ((((body.get("lists") or {}).get(name) or {}).get("fields") or {}).get(leaf) or {}).get("source")
        return ((body.get("fields") or {}).get(pat) or {}).get("source")

    # 레이아웃이 여럿이면: 다른 레이아웃마다 한 번 그려 이 키가 없는 레이아웃을 적는다
    lays = layouts(doc_id)
    missing = {}
    if len(lays) > 1:
        here = _keys_of(base).union(*(_keys_of(lab) for _, lab in probes))
        for lay in lays:
            if lay["id"] == variant:
                continue
            other = render(doc_id, seed, "on" if not form else "default", "on", draft=_draft(None, "", lay["id"], fields),
                           extra={"template_variants": {doc_id: lay["id"]}}, rows="max" if form else None)
            for pat in here - _keys_of(other):
                missing.setdefault(pat, []).append(lay["name"])
    keys = []
    for pat, e in info.items():
        ent = entries.get(fieldinfo.pattern(pat)) or entries.get(pat) or {}
        status = "base" if in_base.get(pat) or "기본" in e["seen"] else ("other" if e["seen"] else "never")
        keys.append({"pattern": pat, "label": e["label"], "type": e["type"], "examples": e["examples"], "status": status,
                     "spots": in_base.get(pat, 0), "seen": [s for s in e["seen"] if s != "기본"],
                     "template_line": template_line(text, pat), "fields_line": ent.get("where"),
                     "key_from": ent.get("key_from"), "value_from": ent.get("value_from"), "source": stored(pat),
                     "missing_in": missing.get(pat, [])})
    keys.sort(key=lambda k: ({"base": 0, "other": 1, "never": 2}[k["status"]], k["template_line"] or 10 ** 6, k["pattern"]))
    out = {"label": {**base, "texts": texts}, "spots": spot_list, "keys": keys, "template": text, "file": _rel(path),
           "kind": "copy" if form else "code", "seed": seed, "heavy": heavy, "variant": variant, "layouts": lays}
    if template is not None and template != saved:
        old_base, old_probes = _renders(doc_id, render, seed, heavy, _draft(None, saved, variant, fields), form, variant)
        before = _keys_of(old_base).union(*(_keys_of(lab) for _, lab in old_probes))
        after = _keys_of(base).union(*(_keys_of(lab) for _, lab in probes))
        out["diff"] = {"lost": sorted(before - after), "added": sorted(after - before)}
    return out


# ---------------------------------------------------------------------------
# 저장
# ---------------------------------------------------------------------------

def save(doc_id: str, render, template: str | None = None, variant: str = "default", values: list | None = None) -> dict:
    """템플릿(바뀌었으면)과 값 출처(values)를 함께 저장. 문법 → 그 레이아웃으로 그려 보기 → 저장. 오류면 아무것도 저장하지 않는다."""
    from jinja2 import TemplateSyntaxError

    from docgen import formfields
    from docgen.render import env

    path = template_file(doc_id, variant)
    saved = path.read_text(encoding="utf-8")
    if template is not None:
        if not isinstance(template, str) or not template.strip():
            raise ValueError("템플릿이 비어 있습니다")
        try:
            env().parse(template)
        except TemplateSyntaxError as e:
            raise ValueError(f"템플릿 문법 오류 ({e.lineno}행): {e.message}") from None
    fields = _with_values(doc_id, values)
    if (template is None or template == saved) and fields is None:
        return {"saved": False, "file": _rel(path)}
    draft = {k: v for k, v in _draft(template, saved, variant, fields).items() if k != "blank"}
    try:
        render(doc_id, 0, draft=draft or None, extra={"template_variants": {doc_id: variant}})
    except Exception as e:  # noqa: BLE001  템플릿 실행 오류 (없는 값 등)
        raise ValueError(f"그리기 오류: {type(e).__name__}: {e}") from None
    if template is not None and template != saved:
        path.write_text(template, encoding="utf-8")
    if fields is not None:
        formfields.write(doc_id, fields)
    return {"saved": True, "file": _rel(path), "values": len(values or [])}


def save_template(doc_id: str, text: str, render) -> dict:
    """기본 레이아웃 템플릿만 저장 (save 의 줄임)."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("템플릿이 비어 있습니다")
    return save(doc_id, render, text)


def _rel(p) -> str:
    from .config import ROOT

    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)
