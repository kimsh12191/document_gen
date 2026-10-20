"""시나리오별 처리 설정과 추출·필드 비교. studio 시험 실행과 실제 build가 함께 쓴다."""
from __future__ import annotations

import math
import operator
import re

from .cases import CASES
from .metrics import normalize_box, norm_text
from .prompts import P_KIE

RULE_TITLES = {
    "ltv": "대출신청금액 ÷ 매매대금 (LTV)", "collateral_ratio": "채권최고액 ÷ 약정금액",
    "jeonse_ratio": "전세대출금 ÷ 보증금", "income_multiple": "대출금 ÷ 연소득",
    "age": "신청일 기준 만 나이", "tenure": "신청일 기준 재직기간", "net_pay": "지급액 − 공제액",
    "sales_rest": "매매대금 − 계약금 − 중도금", "invoice_sum": "송장 품목 금액 합계",
    "tuition_due": "이전 잔액 + 청구액 − 납부액", "debt_ratio": "부채총계 ÷ 자본총계",
    "doc_valid": "신청일 기준 발급 후 90일 이내",
}
COMPARE_OPS = {"equal": "같다", "not_equal": "다르다", "lte": "이하", "gte": "이상", "lt": "미만", "gt": "초과"}
DEFAULTS = {"doc_check": True, "cross_check": True, "review": True, "case_ids": None, "rule_ids": None, "operations": []}
MARKS = {"checkbox", "checkbox_multi", "seal", "signature"}


def validate(value: dict | None, docs: list[str]) -> dict:
    if value is None:
        value = {}
    if not isinstance(value, dict) or set(value) - set(DEFAULTS):
        raise ValueError("처리 설정에 모르는 항목이 있거나 JSON 객체가 아닙니다")
    out = {**DEFAULTS, **value}
    for key in ("doc_check", "cross_check", "review"):
        if not isinstance(out[key], bool):
            raise ValueError(f"{key}: 켜기/끄기를 지정하세요")
    for key, choices in (("case_ids", {c.id for c in CASES}), ("rule_ids", set(RULE_TITLES))):
        ids = out[key]
        if ids is not None and (not isinstance(ids, list) or any(not isinstance(x, str) or x not in choices for x in ids)):
            raise ValueError(f"{key}: 모르는 사례·규칙입니다")
    if not isinstance(out["operations"], list):
        raise ValueError("처리 작업은 목록이어야 합니다")
    seen = set()
    for op in out["operations"]:
        if not isinstance(op, dict) or set(op) - {"id", "kind", "name", "enabled", "left", "right", "operator"}:
            raise ValueError("처리 작업의 형식이 잘못되었습니다")
        oid = op.get("id")
        if not isinstance(oid, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", oid) or oid in seen:
            raise ValueError("처리 작업 ID는 중복 없는 영문·숫자·밑줄·하이픈이어야 합니다")
        seen.add(oid)
        if op.get("kind") not in ("extract", "compare") or not isinstance(op.get("enabled", True), bool):
            raise ValueError(f"{oid}: 추출 또는 비교 작업을 지정하세요")
        if "name" in op and not isinstance(op["name"], str):
            raise ValueError(f"{oid}: 작업 이름은 문자열이어야 합니다")
        for side in ("left", "right") if op["kind"] == "compare" else ("left",):
            ref = op.get(side)
            if not isinstance(ref, dict) or ref.get("doc") not in docs or not isinstance(ref.get("key"), str) or not ref["key"].strip():
                raise ValueError(f"{oid}: 묶음 안의 문서와 항목을 지정하세요 ({side})")
        if op["kind"] == "compare" and op.get("operator") not in COMPARE_OPS:
            raise ValueError(f"{oid}: 비교 조건을 지정하세요")
    return out


def selected(conf: dict, key: str, ident: str) -> bool:
    return conf.get(key) is None or ident in conf[key]


def source(doc_id: str, field: dict, docs: dict) -> dict:
    return {"doc": doc_id, "name": docs[doc_id]["name"],
            **{k: field[k] for k in ("key", "label", "type", "value", "norm", "page", "bbox") if k in field}}


def compare(a: dict, b: dict, op: str) -> bool | None:
    """숫자는 norm, 날짜는 ISO, 나머지는 공백 정규화 후 전체 일치. 가린 글자는 추측하지 않는다."""
    av, bv = a.get("norm"), b.get("norm")
    if any(re.search(r"[*●•]", str(f.get("value", ""))) for f in (a, b)):
        return None
    numeric = all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in (av, bv))
    dates = a.get("type") == b.get("type") == "date" and isinstance(av, str) and isinstance(bv, str)
    if op not in ("equal", "not_equal"):
        if not numeric and not dates:
            return None
        return {"lte": operator.le, "gte": operator.ge, "lt": operator.lt, "gt": operator.gt}[op](av, bv)
    if numeric or dates:
        same = av == bv
    else:
        same = norm_text(a.get("value")) == norm_text(b.get("value"))
    return same if op == "equal" else not same


def execute(conf: dict, docs: dict) -> list[dict]:
    """실행 결과와 생성할 문항 item을 반환한다. 값이 없으면 건너뛴 사유를 남긴다."""
    idx = {did: {f["key"]: f for f in d["fields"] if not f.get("group")} for did, d in docs.items()}
    out = []
    for op in conf["operations"]:
        row = {"id": op["id"], "kind": op["kind"], "name": op.get("name") or op["id"], "sources": [], "status": "ready"}
        out.append(row)
        if not op.get("enabled", True):
            row.update(status="disabled", reason="꺼진 작업")
            continue
        refs = [op["left"]] + ([op["right"]] if op["kind"] == "compare" else [])
        fields = [idx.get(ref["doc"], {}).get(ref["key"]) for ref in refs]
        row["sources"] = [source(ref["doc"], f, docs) for ref, f in zip(refs, fields) if f]
        if any(f is None or f.get("value") in (None, "") or not f.get("bbox") or f.get("type") in MARKS for f in fields):
            row.update(status="skipped", reason="이 고객의 문서에 값·근거 위치가 없거나 텍스트 추출 대상이 아닙니다")
            continue
        if op["kind"] == "extract":
            did, f = refs[0]["doc"], fields[0]
            sizes = docs[did].get("sizes") or [(p["width"], p["height"]) for p in docs[did].get("pages", [])]
            page = f.get("page", 0)
            if page >= len(sizes):
                row.update(status="skipped", reason="근거 쪽이 없습니다")
                continue
            answer = [{"key": f["key"], "value": f["value"], "bbox_2d": normalize_box(f["bbox"], *sizes[page]), "page": page + 1}]
            row.update(answer=f["value"], question=f"{docs[did]['name']}의 {f.get('label') or f['key']} 추출")
            row["item"] = {"task": "kie", "docs": [did], "prompt": P_KIE.format(items=f"- {f['key']}: {f.get('label') or '-'}"),
                           "answer": answer, "eval": {"fields": {f["key"]: {"type": f["type"], "norm": f.get("norm")}}}}
        else:
            answer = compare(*fields, op["operator"])
            if answer is None:
                row.update(status="skipped", reason="가려진 값은 비교할 수 없으며, 대소 비교에는 숫자 또는 날짜 항목 두 개가 필요합니다")
                continue
            names = [f"'{docs[r['doc']]['name']}'의 {f.get('label') or f['key']}" for r, f in zip(refs, fields)]
            condition = COMPARE_OPS[op["operator"]]
            question = (f"{names[0]}이(가) {names[1]}과(와) '{condition}' 조건을 만족합니까? "
                        "숫자는 수치, 날짜는 날짜로 비교하고, 그 밖의 값은 공백을 제외한 전체 문자열이 같아야 같습니다. "
                        "가려진 글자는 추측하지 마세요. ('예' 또는 '아니오'로만 답하세요)")
            row.update(answer="예" if answer else "아니오", question=question)
            row["item"] = {"task": "review", "docs": list(dict.fromkeys(r["doc"] for r in refs)), "question": question,
                           "answer": row["answer"], "eval": {"answer_type": "yesno", "tol": 0}}
    return out
