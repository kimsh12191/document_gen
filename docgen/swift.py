"""ms-swift 학습 데이터(jsonl) 만들기 — Qwen-VL 계열 정보추출 학습용.

한 줄 형식 (ms-swift 표준 messages 형식):
  {"messages": [{"role": "user", "content": "<image>질문"}, {"role": "assistant", "content": "답(JSON)"}],
   "images": ["images/xxx.png", ...], "task": "...", "id": "..."}
여러 쪽 서류는 <image> 를 쪽 수만큼 넣고 images 에 순서대로 둔다.

과제 (같은 라벨에서 만든다):
  kie        전체 추출: 서류 종류 + 모든 값 (중첩 JSON, 빈 칸 null, 도장·서명 true/false)
  kie_keys   지정 키 추출: 요청한 키만 평탄 JSON 으로, 문서에 없는 키는 null
  grounding  위치 포함 추출: [{"key", "label", "value", "bbox_2d", "page"?}]
  marks      체크박스·도장·서명 판별 (위치 포함)
  qa         질의응답 한 문항
좌표: 기본은 Qwen-VL(Qwen2-VL, Qwen3-VL 계열) 방식의 0~1000 상대 좌표 정수 [x1, y1, x2, y2].
     coord="pixel" 이면 이미지 픽셀 좌표.
"""
from __future__ import annotations

import json
import random

TASKS = ("kie", "kie_keys", "grounding", "marks", "qa")

P_KIE = [
    "이 문서의 종류를 판별하고, 문서에 기재된 모든 정보를 JSON으로 추출하세요.",
    "이미지 속 서류에서 항목과 값을 빠짐없이 JSON 형식으로 뽑아주세요. 비어 있는 항목은 null, 도장·서명은 있으면 true로 표시하세요.",
    "다음 은행 제출 서류를 읽고 문서 종류와 기재 내용을 구조화된 JSON으로 정리해 주세요.",
    "Extract all fields from this Korean document as JSON, including the document type. Use null for empty fields.",
]
P_KEYS = [
    "이 문서에서 아래 항목의 값을 JSON으로 추출하세요. 문서에 없거나 비어 있으면 null로 답하세요.\n{keys}",
    "다음 키에 해당하는 값을 찾아 JSON 객체로 답하세요 (없으면 null).\n{keys}",
    "Extract the following keys from the document as a JSON object. Use null if a key is missing or empty.\n{keys}",
]
P_GROUND = [
    "문서의 모든 항목을 값과 위치(bbox_2d)와 함께 JSON 배열로 추출하세요.",
    "각 항목의 키, 항목명, 값, 위치(bbox_2d)를 JSON 리스트로 출력하세요.",
    "Extract every field with its key, label, value and bbox_2d as a JSON list.",
]
P_MARKS = [
    "이 문서의 체크박스 선택 상태와 도장·서명 여부를 위치와 함께 JSON으로 알려주세요.",
    "체크된 항목, 날인 여부, 서명 여부를 bbox_2d 와 함께 JSON으로 정리하세요.",
]
P_QA_VALUE = ["이 문서에서 '{label}' 값은 무엇인가요?", "'{label}' 항목에 적힌 내용을 알려주세요.", "{label}?"]
P_QA_SEAL = ["'{label}' 자리에 도장이 찍혀 있나요?", "{label} 날인이 되어 있습니까?"]
P_QA_SIGN = ["'{label}' 자리에 서명이 되어 있나요?", "{label} 서명이 있습니까?"]
P_QA_CHECK = ["'{label}' 항목에서 체크된 보기는 무엇인가요?", "{label}: 어떤 항목에 표시되어 있나요?"]


def _dump(x) -> str:
    return json.dumps(x, ensure_ascii=False, separators=(", ", ": "))


def _box(b, page_size, coord):
    if b is None:
        return None
    if coord == "pixel":
        return [round(v) for v in b]
    w, h = page_size
    return [max(0, min(1000, round(b[0] / w * 1000))), max(0, min(1000, round(b[1] / h * 1000))),
            max(0, min(1000, round(b[2] / w * 1000))), max(0, min(1000, round(b[3] / h * 1000)))]


def _user(n_images: int, text: str) -> str:
    return "<image>" * n_images + text


def _flat_values(fields: list[dict]) -> dict:
    """키 → 정답값 (도장·서명 bool, 체크박스 선택 보기, 빈 칸 null)."""
    out = {}
    for f in fields:
        if f.get("group"):
            continue
        out[f["key"]] = f["present"] if f["type"] in ("seal", "signature") else f["value"]
    return out


def build_records(label: dict, images: list[str], sizes: list[tuple[int, int]], rng: random.Random,
                  tasks=TASKS, coord: str = "norm1000", key_pool: list[str] | None = None,
                  fields: list[dict] | None = None) -> list[dict]:
    """라벨 하나(이미지 한 벌)에서 과제별 학습 레코드를 만든다.

    images/sizes: 쪽 순서대로의 이미지 경로와 (가로, 세로). fields 를 주면 label["fields"] 대신 쓴다 (증강 좌표).
    key_pool: 지정 키 추출에서 '문서에 없는 키'로 섞을 후보 (같은 그룹 다른 서류의 키)."""
    fields = fields if fields is not None else label["fields"]
    n = len(images)
    multi = n > 1
    gt = {"document_type": label["doc_name"], **label["gt"]}
    flat = _flat_values(fields)
    out = []

    def rec(task, q, a):
        out.append({"id": f"{label['id']}:{task}", "task": task, "images": images,
                    "messages": [{"role": "user", "content": _user(n, q)}, {"role": "assistant", "content": a}]})

    def page_of(f):
        return f.get("page", 0)

    def located(f, b):
        return _box(b, sizes[page_of(f)], coord)

    if "kie" in tasks:
        rec("kie", rng.choice(P_KIE), _dump(gt))

    if "kie_keys" in tasks and flat:
        keys = list(flat)
        pick = rng.sample(keys, min(len(keys), rng.randint(3, 10)))
        absent = [k for k in (key_pool or []) if k not in flat]
        pick += rng.sample(absent, min(len(absent), rng.choice([0, 0, 1, 2])))
        rng.shuffle(pick)
        rec("kie_keys", rng.choice(P_KEYS).format(keys="\n".join(f"- {k}" for k in pick)),
            _dump({k: flat.get(k) for k in pick}))

    if "grounding" in tasks:
        items = []
        for f in fields:
            if f.get("group") or f["type"] in ("seal", "signature") or f.get("bbox") is None:
                continue
            it = {"key": f["key"], "label": f.get("label"), "value": f["value"], "bbox_2d": located(f, f["bbox"])}
            if multi:
                it["page"] = page_of(f) + 1
            items.append(it)
        if items:
            rec("grounding", rng.choice(P_GROUND), _dump(items))

    if "marks" in tasks:
        checks, seals, signs = [], [], []
        for f in fields:
            pg = {"page": page_of(f) + 1} if multi else {}
            if f["type"] in ("checkbox", "checkbox_multi") and f.get("options"):
                checks.append({"key": f["key"], "label": f.get("label"), **pg,
                               "checked": [o["text"] for o in f["options"] if o["checked"]],
                               "options": [{"text": o["text"], "checked": o["checked"],
                                            "bbox_2d": located(f, o.get("box_bbox"))} for o in f["options"]]})
            elif f["type"] == "seal":
                seals.append({"key": f["key"], "label": f.get("label"), "present": f["present"], **pg,
                              **({"kind": f["kind"]} if f.get("kind") else {}),
                              "bbox_2d": located(f, f.get("bbox"))})
            elif f["type"] == "signature":
                signs.append({"key": f["key"], "label": f.get("label"), "present": f["present"], **pg,
                              "bbox_2d": located(f, f.get("bbox"))})
        if checks or seals or signs:
            rec("marks", rng.choice(P_MARKS), _dump({"checkboxes": checks, "seals": seals, "signatures": signs}))

    if "qa" in tasks:
        cnt: dict = {}
        for f in fields:
            cnt[f.get("label")] = cnt.get(f.get("label"), 0) + 1
        cands = [f for f in fields if not f.get("group") and f.get("label") and cnt[f["label"]] == 1]  # 항목명이 유일한 것만
        if cands:
            f = rng.choice(cands)
            lab = f["label"]
            if f["type"] == "seal":
                q, a = rng.choice(P_QA_SEAL), "예" if f["present"] else "아니오"
            elif f["type"] == "signature":
                q, a = rng.choice(P_QA_SIGN), "예" if f["present"] else "아니오"
            elif f["type"] == "checkbox":
                q, a = rng.choice(P_QA_CHECK), f["value"] or "체크된 항목 없음"
            else:
                q, a = rng.choice(P_QA_VALUE), f["value"] if f["value"] is not None else "기재되어 있지 않습니다."
            rec("qa", q.format(label=lab), a)
    return out
