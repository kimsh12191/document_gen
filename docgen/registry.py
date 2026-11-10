"""서류 종류 레지스트리.

각 서류는 docgen/docs/*.py 에서 @doc(...) 데코레이터로 등록한다.
생성 함수는 (Profile, random.Random) -> dict 이며, dict 값은 화면에 표시될 문자열이다.
"""
from __future__ import annotations

import importlib
import json
import pkgutil
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .entities import Profile

GROUPS = {
    "identity": "신원·신분",
    "family": "가족관계",
    "income": "소득·재직",
    "tax": "세금·보험",
    "finance": "금융거래",
    "real_estate": "부동산",
    "business": "개인사업자",
    "corporate": "법인",
    "fx": "외환·무역",
    "bank_form": "은행 서식",
    "hana": "하나은행 서식(원본)",
    "imported": "가져온 서식(이미지)",
}

# 은행이 직접 쓰는 서식 그룹. 이 그룹의 서류는 렌더링할 때
#   - 서식을 낸 은행(옛 은행 포함)에 맞춰 프로필·표기를 바꾸고 (banks.bank_view)
#   - 템플릿에 서식 문맥 bk 를 넘긴다 (banks.form_context)
BANK_FORM_GROUPS = {"bank_form"}

@dataclass
class DocSpec:
    id: str
    name: str
    group: str
    category: str  # "external"(외부 발급) / "internal"(은행 자체 서식)
    template: str
    generate: Callable[[Profile, random.Random], dict]
    page: str = "a4"  # "a4" | "a4_landscape" | "card" | "passport"
    sample_mark: bool = False  # 신분증 등: '견본' 표시 강제
    description: str = ""
    origin: str = "builtin"  # html 서식의 출처: builtin(코드) / copy(복제) / analyzer(분석기). overlay 는 catalog.kind_of 가 정함


REGISTRY: dict[str, DocSpec] = {}


def doc(id: str, name: str, group: str, category: str = "external", page: str = "a4",
        template: str | None = None, sample_mark: bool = False, description: str = ""):
    assert group in GROUPS, group

    def deco(fn):
        if id in REGISTRY:
            raise ValueError(f"duplicate doc id: {id}")
        REGISTRY[id] = DocSpec(id, name, group, category, template or f"{group}/{id}.html.j2", fn,
                               page, sample_mark, description or (fn.__doc__ or "").strip())
        return fn

    return deco


FORMS_DIR = Path(__file__).resolve().parent / "forms"


def register_folder_forms(module: str, ids) -> None:
    """코드 서식의 값 만드는 함수(서식 폴더 docgen/forms/<ID>/generate.py 의 @doc)를 등록한다.
    그룹 모듈(docgen/docs/<그룹>.py) 끝에서 부른다 — 예전에 그 모듈 안에 @doc 이 있던 차례 그대로 (서식 목록·데이터셋 순서)."""
    import importlib.util

    for doc_id in ids:
        if doc_id in REGISTRY:   # 같은 프로세스에서 두 번 불려도 (모듈 다시 읽기) 한 번만
            continue
        path = FORMS_DIR / doc_id / "generate.py"
        name = f"docgen.forms_code.{doc_id}"
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception:
            sys.modules.pop(name, None)
            raise
        if doc_id not in REGISTRY:
            raise ValueError(f"{path}: @doc(\"{doc_id}\", …) 로 등록하지 않았습니다 ({module} 의 FORMS)")


_EXTRA_DONE = False
_SCANNED = False


def load_all() -> dict[str, DocSpec]:
    """서류 전부: docgen/docs/*.py 의 @doc(코드 서식, 원본 서식) + 화면에서 만든 html 서식(docgen/htmlform.py, 처음 한 번)."""
    global _EXTRA_DONE, _SCANNED
    from . import docs

    if not _SCANNED:   # 폴더는 처음 한 번만 훑는다 (서식 목록 한 번에 수천 번 불린다). 실행 중 새 서식은 각 등록 함수가 넣는다
        for m in pkgutil.iter_modules(docs.__path__):
            importlib.import_module(f"{docs.__name__}.{m.name}")
        _SCANNED = True
    if not _EXTRA_DONE:   # 코드 서식을 모두 등록한 뒤라 ID 가 겹치면 코드 서식이 이긴다
        _EXTRA_DONE = True
        from .htmlform import register_forms

        register_forms()
    return REGISTRY


SPEC_FIELDS = ("name", "group", "category", "page", "description", "origin")


def refresh() -> dict:
    """서식 폴더를 다시 훑어 서식 목록을 최신으로 (studio ① 서식 › 서식 다시 읽기). 다시 띄우지 않아도 된다.
    - 새 폴더(html 서식 docgen/forms/<ID>/ · 사내 서식, 이미지 서식 img_*)를 등록한다. 깨진 폴더는 등록하지 않고 이유를 남긴다.
    - 이미 있는 html·이미지 서식은 form.json·layout.json 의 이름·그룹 등을 다시 읽는다.
    - 폴더가 없어진 html·이미지 서식은 목록에서 뺀다 (검수 기록 catalog.json 은 그대로 — 폴더를 되돌리면 되살아난다).
    - 코드 서식(docs/*.py)과 하나은행 원본(hf###)은 건드리지 않는다. 레이아웃 파일은 다시 읽게 한다.
    템플릿·칸 목록의 내용은 원래 그릴 때마다 읽으므로 여기서 할 일이 없다.
    모든 서식 폴더의 questions.json(질문·답)·qa.py(서식 전용 질문) 형식도 검사해 problems 에 넣는다.
    → {"added", "updated", "removed": [ID…], "problems": [{"id", "reason"}],
       "with_script": 새로·바뀐 것 중 생성 스크립트(generate.py)가 있는 서식 — 사람이 읽고 넣었는지 확인용}"""
    from . import formdir, htmlform
    from . import realform as RF

    reg = load_all()
    out = {"added": [], "updated": [], "removed": [], "problems": []}
    html_dirs = {d.name: d for d in formdir.copy_dirs()}
    image_dirs = {d.name: d for d in formdir.image_dirs()}
    for doc_id, spec in list(reg.items()):
        if spec.template == htmlform.PREFIX + doc_id:
            gone = doc_id not in html_dirs
        elif spec.template == "_real_form.html.j2" and spec.group == "imported":
            gone = doc_id not in image_dirs
        else:
            continue
        if gone:
            del reg[doc_id]
            out["removed"].append(doc_id)

    def put(doc_id, make):
        try:
            new = make()
        except (OSError, ValueError, KeyError, IndexError, TypeError) as e:
            out["problems"].append({"id": doc_id, "reason": f"읽지 못했습니다: {e}"})
            return
        old = reg.get(doc_id)
        if old is None:
            reg[doc_id] = new
            out["added"].append(doc_id)
        elif any(getattr(old, k) != getattr(new, k) for k in SPEC_FIELDS):
            for k in SPEC_FIELDS:
                setattr(old, k, getattr(new, k))
            out["updated"].append(doc_id)

    for doc_id, d in html_dirs.items():
        spec = reg.get(doc_id)
        if spec is not None and spec.template != htmlform.PREFIX + doc_id:
            out["problems"].append({"id": doc_id, "reason": f"코드 서식과 ID 가 겹칩니다 — 코드 서식이 쓰입니다 ({d})"})
            continue
        why = htmlform.check_dir(d)
        if why:
            out["problems"].append({"id": doc_id, "reason": why})
            continue
        put(doc_id, lambda d=d: htmlform.spec_of(d))
    for doc_id, d in image_dirs.items():
        spec = reg.get(doc_id)
        if spec is not None and spec.template != "_real_form.html.j2":
            out["problems"].append({"id": doc_id, "reason": f"다른 서식과 ID 가 겹칩니다 ({d})"})
            continue
        put(doc_id, lambda d=d: RF.image_spec(d))
    RF.load_layout.cache_clear()
    from . import formqa, formquestions

    for doc_id in reg:   # 서식의 질문·답 파일 형식 (서식은 그대로 쓰이고, 문항을 만들 때 오류가 난다)
        d = formdir.folder(doc_id) or formdir.copy_dir(doc_id)
        for why in [*formquestions.check_dir(d), *formqa.check_dir(d)] if d else ():
            out["problems"].append({"id": doc_id, "reason": why})
    out["with_script"] = [i for i in out["added"] + out["updated"] if i in html_dirs and (html_dirs[i] / htmlform.SCRIPT).exists()]
    for k in out:
        out[k].sort(key=lambda x: x["id"] if isinstance(x, dict) else x)
    return out
