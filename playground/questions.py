"""고를 수 있는 질문: 벤치마크와 같은 문장 (docgen/bench/prompts.py·ocr_tasks.py, 서식의 questions.json·fields.json 의 q).
서식의 칸 목록은 guide/fields/fields.json (studio 카탈로그와 같은 자동 생성 파일, 그리지 않고 읽음)."""
from __future__ import annotations

import datetime
import json
from functools import lru_cache
from pathlib import Path

from docgen import fieldinfo, formquestions as FQ
from docgen.bench import prompts
from docgen.bench.ocr_data import dumps
from docgen.bench.ocr_tasks import DIRECTIONS, PROMPTS as OCR
from docgen.bench.tasks import MARK_TYPES

from .images import COLORS, marker_rect, norm

CATALOG = Path(__file__).resolve().parents[1] / "guide" / "fields" / "fields.json"
MAX_KEYS = 40   # 벤치마크 kie·marks 도 서류 하나에 40개까지 묻는다

# needs: 질문을 만들려면 화면에서 정할 것. box 끌기 / text 찾을 글자 / anchor 기준(글자 또는 상자)+방향 / marker 색 상자 /
#        form 서식(항목 목록) / field 칸 이름·기준일. image: 보내는 그림 (crop 자른 것, marker 상자를 그린 것, 없으면 고른 그림 그대로)
# answer: 답 꼴 — text 글, boxes [{bbox_2d, label}], entries [{key, value, bbox_2d, page}], json 객체
TASKS = [
    {"id": "ocr_page", "group": "OCR", "name": "전체 받아쓰기", "needs": [], "answer": "text", "pages": True},
    {"id": "spotting", "group": "OCR", "name": "모든 글자와 위치", "needs": [], "answer": "boxes"},
    {"id": "crop_ocr", "group": "OCR", "name": "잘라서 읽기 (짧은 글)", "needs": ["box"], "image": "crop", "answer": "text"},
    {"id": "ocr_field", "group": "OCR", "name": "값 칸 잘라서 읽기", "needs": ["box"], "image": "crop", "answer": "text"},
    {"id": "bbox_ocr", "group": "OCR", "name": "좌표 영역의 글자", "needs": ["box"], "answer": "text"},
    {"id": "region_ocr", "group": "OCR", "name": "좌표 영역의 여러 줄", "needs": ["box"], "answer": "text"},
    {"id": "grounding", "group": "OCR", "name": "이 글자는 어디에", "needs": ["text"], "answer": "boxes"},
    {"id": "relation", "group": "OCR", "name": "기준 글자 옆 글자", "needs": ["anchor"], "answer": "boxes"},
    {"id": "marked_ocr", "group": "OCR", "name": "그린 상자 안 글자", "needs": ["marker"], "image": "marker", "answer": "text"},
    {"id": "marked_box", "group": "OCR", "name": "그린 상자의 위치와 글자", "needs": ["marker"], "image": "marker", "answer": "boxes"},
    {"id": "classify", "group": "문서 이해", "name": "서류 분류", "needs": [], "answer": "text", "pages": True},
    {"id": "kie", "group": "문서 이해", "name": "값 뽑기", "needs": ["form"], "answer": "entries", "pages": True},
    {"id": "marks", "group": "문서 이해", "name": "체크·도장·서명", "needs": ["form"], "answer": "entries", "pages": True},
    {"id": "freetext", "group": "문서 이해", "name": "기타 칸 정리", "needs": ["field"], "answer": "json", "pages": True},
    {"id": "custom", "group": "직접", "name": "직접 쓰기", "needs": [], "answer": "auto", "pages": True},
]
BY_ID = {t["id"]: t for t in TASKS}


@lru_cache(maxsize=1)
def _catalog(mtime: float) -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def catalog() -> dict:
    try:
        return _catalog(CATALOG.stat().st_mtime)
    except OSError:
        return {}


def forms() -> list[dict]:
    return [{"id": k, "name": v.get("name") or k, "group": v.get("group")} for k, v in sorted(catalog().items())]


def _fields(form: str, task: str) -> list[dict]:
    keys = (catalog().get(form) or {}).get("keys") or []
    fields = [{"key": k["key"], "label": k.get("label"), "type": k.get("type"), "options": k.get("options") or []} for k in keys]
    if task == "kie":
        return [f for f in fields if f["type"] not in MARK_TYPES and not f["key"].startswith(("seal.", "sign."))]
    return [f for f in fields if f["type"] in MARK_TYPES]


def items(form: str, task: str, max_keys: int = MAX_KEYS) -> tuple[str, int]:
    """kie·marks 질문의 항목 줄 (벤치마크와 같은 줄 틀·설명) 과 전체 항목 수. 앞에서부터 max_keys 개 (0 이면 전부)."""
    q, fq = FQ.read(form), fieldinfo.questions(form)
    picked = FQ.pick(q, task, _fields(form, task), fq)
    line, _, _ = FQ.shell(q, task)
    use = picked[:max_keys] if max_keys else picked
    out = []
    for f in use:
        extra = ""
        if task == "marks":
            if f["type"] in ("checkbox", "checkbox_multi"):
                kind = "체크박스" if f["type"] == "checkbox" else "복수 선택"
                extra = f"{kind}, 보기: {' / '.join(f['options'])}"
            else:
                extra = "도장" if f["type"] == "seal" else "서명"
        out.append(prompts.kie_line(form, f["key"], f.get("label"), None, extra, picked, note=f.get("_note"), line=line))
    return "\n".join(out), len(picked)


def _ocr(task: str, lang: str) -> str:
    return OCR[task][0 if lang == "en" else 1]


def build(spec: dict) -> dict:
    """질문 하나. spec: task, form?, lang(ko|en), size?([w,h] 고른 그림), box?(픽셀), text?, anchor_text?, anchor_box?(픽셀),
    direction?, marker?: {color, box(픽셀, 글자 둘레)}, coords?, label?, basis?, max_keys?
    → {"prompt", "note"?}. 좌표는 질문에 넣을 때 그 그림 기준 0~1000. 화면이 정할 것이 비었으면 ValueError."""
    task, lang = spec.get("task"), spec.get("lang") or "ko"
    w, h = spec.get("size") or (0, 0)

    def n(box):
        if not (w and h):
            raise ValueError("그림을 먼저 고르세요")
        return norm(box, w, h)

    t = BY_ID.get(task)
    if not t:
        raise ValueError(f"모르는 과제: {task}")
    form = spec.get("form") or None
    q = FQ.read(form) if form else None
    note = None
    if task == "custom":
        return {"prompt": ""}
    if task in ("classify", "ocr_page", "ocr_field"):
        return {"prompt": FQ.prompt(q, task)}
    if task in ("kie", "marks"):
        if not form:
            return {"prompt": FQ.prompt(None, task, "- 키: 항목명"), "note": "서식을 고르면 그 서식의 항목이 들어갑니다. 아니면 항목 줄을 직접 고치세요."}
        lines, total = items(form, task, int(spec.get("max_keys", MAX_KEYS)))
        if not lines:
            return {"prompt": FQ.prompt(q, task, "- 키: 항목명"), "note": f"{form} 에는 이 과제로 물을 칸이 없습니다."}
        shown = lines.count("\n") + 1
        if shown < total:
            note = f"항목 {total}개 중 앞의 {shown}개 (벤치마크도 40개까지 묻습니다)"
        return {"prompt": FQ.prompt(q, task, lines), **({"note": note} if note else {})}
    if task == "freetext":
        return {"prompt": prompts.freetext_prompt(spec.get("label") or "비고", spec.get("basis") or datetime.date.today().isoformat())}
    if task in ("spotting",):
        return {"prompt": _ocr(task, lang).format()}
    if task == "crop_ocr":
        return {"prompt": _ocr(task, lang)}
    if task in ("bbox_ocr", "region_ocr"):
        if not spec.get("box"):
            raise ValueError("그림에서 네모를 끌어 영역을 정하세요")
        return {"prompt": _ocr(task, lang).format(box=dumps(n(spec["box"])))}
    if task == "grounding":
        if not spec.get("text"):
            raise ValueError("찾을 글자를 적으세요")
        return {"prompt": _ocr(task, lang).format(text=dumps(spec["text"]))}
    if task == "relation":
        direction = spec.get("direction") or "right"
        if direction not in DIRECTIONS:
            raise ValueError(f"방향은 {', '.join(DIRECTIONS)}")
        if spec.get("anchor_text"):
            ref = ref_ko = dumps(spec["anchor_text"])
        elif spec.get("anchor_box"):
            box = dumps(n(spec["anchor_box"]))
            ref, ref_ko = "the text at bbox_2d=" + box, "bbox_2d=" + box + " 글자"
        else:
            raise ValueError("기준 글자를 적거나 그림에서 기준 글자에 네모를 끄세요")
        return {"prompt": _ocr(task, lang).format(direction=DIRECTIONS[direction][0], direction_ko=DIRECTIONS[direction][1],
                                                  anchor=ref if lang == "en" else ref_ko)}
    if task in ("marked_ocr", "marked_box"):
        m = spec.get("marker") or {}
        if m.get("color") not in COLORS or not m.get("box"):
            raise ValueError("그림에서 네모를 끌고 색을 고르세요")
        en, ko, _ = COLORS[m["color"]]
        if task == "marked_box":
            return {"prompt": _ocr(task, lang).format(color=en, color_ko=ko)}
        drawn = dumps(n(marker_rect(m["box"], w, h))) if spec.get("coords") else None   # 그린 상자의 바깥 테두리
        return {"prompt": _ocr(task, lang).format(color=en, color_ko=ko, coords=f" at bbox_2d={drawn}" if drawn else "",
                                                  coords_ko=f"(bbox_2d={drawn})" if drawn else "")}
    raise ValueError(f"모르는 과제: {task}")
