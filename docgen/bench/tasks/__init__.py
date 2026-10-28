"""서류 한 건 과제: 과제 하나 = 파일 하나. 그 파일에 질문·정답 만드는 법·답 형식 설명이 함께 있다.

  classify.py   서류 분류        ocr_page.py  전체 받아쓰기     ocr_field.py  값 칸 읽기
  kie.py        정보 추출        freetext.py  기타 칸 정리      marks.py      체크·도장·서명
  form_qa.py    서식 전용 질문 (서식 폴더 qa.py)

공통은 여기, 서식마다 다른 것은 서식 폴더 (칸마다 묻기·항목명 fields.json 의 q, 질문 문장·답 틀 questions.json, 서식 전용 질문 qa.py)
(docgen/formquestions.py). 과제 파일은 doc.q 로 그것을 읽어 따른다. 파일이 없는 서식은 공통 규칙 그대로.

과제 파일의 꼴 (kie.py 를 견본으로 보면 된다)
  TASK, NAME          과제 ID, 이름
  PROMPT              질문 문장 (원본은 prompts.py — guide/questions.md 와 같은지 테스트가 본다)
  ANSWER, EXAMPLE, NOTES   답 형식(JSON schema)·예시·설명 — studio 질문 형식 화면(contracts.py)이 그대로 보여 준다
  make(doc)           서류 한 건(Doc) → 문항 목록 [{"id", "task", "prompt", "answer", "eval"?, "images", "meta"}]
                      정답은 서식을 그릴 때 칸마다 넣은 값·위치(doc.fields)에서 만든다

차례는 SINGLE 순서 그대로다. 과제들이 같은 난수(doc.rng)를 이어서 쓰므로 순서를 바꾸거나 중간에 난수를 더 쓰면
같은 설정으로 만든 세트가 달라진다 — 새 과제는 끝에 붙이고, 세트가 달라지면 build.py 의 VERSION 을 올린다.
채점은 docgen/bench/evaluate.py 의 s_<과제>. 업무 묶음 과제(doc_check·cross_check·review)는 build.py·cases.py·rules.py.
"""
from __future__ import annotations

import random
from pathlib import Path

from ... import dictionary as DIC
from ... import fieldinfo
from ... import formquestions as FQ
from .. import perturb
from ..metrics import normalize_box

MARK_TYPES = ("checkbox", "checkbox_multi", "seal", "signature")
# 답 형식(JSON schema) 조각 — 과제 파일의 ANSWER 와 contracts.py 가 같이 쓴다
BOX = {"type": "array", "items": {"type": "integer", "minimum": 0, "maximum": 1000}, "minItems": 4, "maxItems": 4}
LOCATION = {"bbox_2d": BOX, "page": {"type": "integer", "minimum": 1}}
STRINGS = {"type": "array", "items": {"type": "string"}}
ENTRY = {"type": "object", "required": ["key", "value"], "properties": {
    "key": {"type": "string"}, "value": {"type": ["string", "number", "null"]}, **LOCATION}}


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


class Doc:
    """과제 파일의 make(doc) 가 받는 서류 한 건 (build.Builder.render_doc 결과를 과제가 쓰기 좋게).

    r          render_doc 결과 그대로 (doc_id, name, images, sizes, data …)
    sid        문항 ID 의 서류 부분 (<서류ID>_<seed>)
    fields     칸 목록: {"key", "label", "type", "value", "bbox", "page", …}. 공통 키로 정한 칸은 공통 키로 (키 사전)
    visible    이미지에 보이고 값이 있는 칸 (체크·도장·서명, 묶음 칸 제외) — 받아쓰기·값 칸 읽기의 정답 재료
    meta, base 문항 meta / 문항에 공통으로 붙는 {"images", "meta"}
    rng        과제들이 차례로 같이 쓰는 난수
    out        세트 폴더 (잘라낸 그림을 저장할 곳)
    q          이 서식의 질문 껍데기 (서식 폴더의 questions.json: 문장·답 꼴·전용 질문). 없으면 None = 공통
    fq         칸마다 질문 설정 {서식 키: {ask, label, note, ocr}} (칸 목록 fields.json 의 q, docgen/fieldinfo.py)
    """

    def __init__(self, r: dict, stem: str, out: Path, fields_per_doc: int, max_keys: int):
        self.r, self.out, self.fields_per_doc, self.max_keys = r, out, fields_per_doc, max_keys
        self.meta = {"doc_type": r["doc_id"], "doc_name": r["name"], "group": r["group"], "condition": r["condition"],
                     "writing": r["writing"], "n_pages": len(r["images"])}
        self.base = {"images": r["images"], "meta": self.meta}
        self.rng = random.Random(f"bench:single:{stem}")
        self.sid = Path(stem).name
        self.q = FQ.read(r["doc_id"])
        self.fq = fieldinfo.questions(r["doc_id"])   # 칸마다 질문 설정 (fields.json 의 q)
        self.fields = DIC.apply(r["doc_id"], r["fields"])   # 공통 키로 정한 칸은 공통 키로 (3.0)
        raw_key = dict(zip(range(len(r["raw_keys"])), r["raw_keys"]))
        self.visible = [f for i, f in enumerate(self.fields)
                        if not (f.get("value") is None or f["type"] in MARK_TYPES or f.get("group")
                                or raw_key.get(i) not in r["visible"])]

    def where(self, f: dict, box) -> dict:
        """정답 위치: 그 쪽 이미지 기준 0~1000, 쪽은 1부터. 위치가 없으면 {}."""
        pg, sizes = f.get("page", 0), self.r["sizes"]
        if not box or pg >= len(sizes):
            return {}
        return {"bbox_2d": normalize_box(box, *sizes[pg]), "page": pg + 1}

    def writing(self, key: str) -> str:
        """칸의 글씨: hand(손글씨) / print."""
        if self.r["group"] == "hana" and key.startswith("handwritten"):
            return "hand"
        return self.r["writing"]

    def sample(self, fields: list[dict], n: int) -> list[dict]:
        """n 개를 넘으면 n 개만 고른다 (문서 순서 유지)."""
        if len(fields) > n:
            return sorted(self.rng.sample(fields, n), key=fields.index)
        return fields


from . import classify, form_qa, freetext, kie, marks, ocr_field, ocr_page  # noqa: E402

SINGLE = (classify, ocr_page, ocr_field, kie, freetext, marks, form_qa)   # 만드는 차례 (난수를 이어 쓴다)


def make_single(r: dict, stem: str, out: Path, fields_per_doc: int, max_keys: int) -> list[dict]:
    """서류 한 건의 모든 과제 문항."""
    doc = Doc(r, stem, out, fields_per_doc, max_keys)
    return [rec for t in SINGLE for rec in t.make(doc)]


def contract(t) -> dict:
    """studio 질문 형식 화면용 (contracts.py)."""
    return {"name": t.NAME, "prompt_template": t.PROMPT, "answer_schema": t.ANSWER, "example": t.EXAMPLE, "notes": t.NOTES}
