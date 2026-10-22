"""Studio 안내와 guide 정적 문서가 공유하는 데이터 카탈로그.

python -m studio.guidebook 으로 현재 설정의 Markdown·JSON 스냅샷을 갱신한다.
렌더링 브라우저 없이 등록부·필드 스키마·시나리오 처리 설정을 읽는다.
"""
from __future__ import annotations

import json
from pathlib import Path

from docgen import dictionary as DIC
from docgen.bench.contracts import contracts
from docgen.bench.processing import validate, RULE_TITLES
from docgen.bench.cases import CASES
from docgen.registry import GROUPS, load_all, load_scenarios, SCENARIOS, SCENARIO_PROCESSING, SCENARIO_SAMPLING

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = {
    "README.md": "사용 설명서 · 시작하기",
    "studio.md": "Studio 사용법 · 데이터 만들기·넣기·채점",
    "ocr.md": "내 이미지로 OCR 데이터 준비",
    "training.md": "학습 설정·실행",
    "results.md": "결과 해석",
    "agent-workflow.md": "agent 작업 절차 · 생성→학습→보고",
    "catalog.md": "서류별 추출 항목 · 연결 시나리오",
    "questions.md": "질문과 정답 형식",
    "tasks.md": "실제 데이터 예시",
    "benchmark.md": "업무 과제 · 사례 · 채점",
    "benchmark-tracking.md": "벤치마크 구성 · 구분별 평가 추적",
    "documents.md": "서류 이름 목록",
    "fields/README.md": "필드 목록 안내",
    "overview.md": "프로젝트 개요",
}
# 추가 참고 문서도 guide 내부에서 이동할 수 있다. 경로는 서버가 수집한 목록만 허용한다.
for _path in sorted((ROOT / "guide").rglob("*.md")):
    _name = _path.relative_to(ROOT / "guide").as_posix()
    if _name not in DOCUMENTS:
        DOCUMENTS[_name] = _path.read_text(encoding="utf-8").splitlines()[0].lstrip("# ") or _name


def catalog() -> dict:
    # 저장 후의 시나리오를 읽고, 필드는 build_schema가 수집한 스냅샷을 사용한다.
    load_scenarios()
    reg = load_all()
    path = ROOT / "guide/fields/fields.json"
    schema = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    scenarios = []
    for sid, (name, docs) in SCENARIOS.items():
        scenarios.append({"id": sid, "name": name, "docs": docs,
                          "sampling": SCENARIO_SAMPLING.get(sid, {}),
                          "processing": validate(SCENARIO_PROCESSING.get(sid), docs)})
    forms = []
    for spec in reg.values():
        fields = schema.get(spec.id, {}).get("keys", [])
        mapped = DIC.apply(spec.id, fields)
        uses = []
        for scenario in scenarios:
            roles = [d for d in scenario["docs"] if d == spec.id or
                     spec.id in scenario["sampling"].get(d, {}).get("forms", [])]
            if not roles:
                continue
            ops = [op for op in scenario["processing"]["operations"]
                   if any((op.get(side) or {}).get("doc") in roles for side in ("left", "right"))]
            uses.append({"id": scenario["id"], "name": scenario["name"], "roles": roles,
                         "operations": ops, "processing": scenario["processing"]})
        forms.append({"id": spec.id, "name": spec.name, "group": spec.group,
                      "group_name": GROUPS.get(spec.group, spec.group), "description": spec.description,
                      "schema_available": spec.id in schema,
                      "fields": [{**f, "question_key": m["key"]} for f, m in zip(fields, mapped)],
                      "scenarios": uses})
    return {"format": "docgen-guide/1", "forms": forms, "scenarios": scenarios,
            "tasks": contracts(), "rules": RULE_TITLES,
            "cases": [{"id": c.id, "title": c.title, "basis": c.basis} for c in CASES],
            "notes": "필드는 build_schema 수집 결과이며 가능한 항목 목록이다. 실제 문항·값·유효한 사례는 생성 결과로 확인한다."}


def cell(value) -> str:
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", " ").replace("\r", "")


def markdown(data: dict, form_id: str | None = None) -> str:
    lines = ["# 서류별 추출 항목과 시나리오 카탈로그", "",
             "이 문서는 `python -m studio.guidebook`으로 현재 등록부·필드 스키마·시나리오 설정에서 생성합니다. 직접 수정하지 않습니다.", "",
             "Studio의 **사용 가이드 → 서류·추출 카탈로그**와 서식 상세의 **추출·시나리오** 탭은 같은 구조의 현재 데이터를 보여 줍니다. 이 파일과 catalog.json은 갱신 시점의 스냅샷입니다.", "",
             "필드 스키마를 바꿨다면 `python docgen/scripts/build_schema.py` 후 이 문서를 갱신하세요. 필드가 미수집인 서식은 추출 불가가 아니라 목록 갱신이 필요한 상태입니다. 필드별 예시는 가상 값이며 고정 출력값이 아닙니다.", "",
             "단일 서류 KIE는 해당 서식의 필드를 사용합니다. 업무 시나리오의 명시적 추출·비교 작업은 별도 설정입니다. 작업이 없더라도 켜진 기본 구비·대조·심사 과제는 유효한 서류·규칙에 따라 생성됩니다.", ""]
    if form_id is None:
        lines += ["## 업무별 서류와 처리 설정", ""]
        for s in data["scenarios"]:
            lines += [f"### {s['id']} · {s['name']}", "", "필수 역할/기준 서식: " + ", ".join(s["docs"]), "",
                      "처리·추출·비교 및 후보 서식 설정 (현재 설정):", "", "```json",
                      json.dumps({"sampling": s["sampling"], "processing": s["processing"]}, ensure_ascii=False, indent=2), "```", ""]
        lines += ["## 기본 대조 사례", "", "| ID | 사례 | 근거 |", "|---|---|---|"]
        lines += [f"| {c['id']} | {cell(c['title'])} | {cell(c['basis'])} |" for c in data["cases"]]
        lines += ["", "## 기본 심사 규칙", "", "| ID | 계산·판단 |", "|---|---|"]
        lines += [f"| {k} | {cell(v)} |" for k, v in data["rules"].items()]
        lines += ["", "## 서류별 목록", ""]
    for f in data["forms"]:
        if form_id is not None and f["id"] != form_id:
            continue
        lines += [f"### {f['id']} · {f['name']}", "", f"그룹: {f['group_name']} (`{f['group']}`)", "", cell(f["description"]), "",
                  "연결 업무: " + (", ".join(f"{s['name']} ({s['id']})" for s in f["scenarios"]) or "없음 · 단일 서류 과제로 사용 가능"), ""]
        if not f["schema_available"]:
            lines += ["필드 목록 미수집. Studio 문항 Q/A로 실제 문항을 확인하고 필드 스키마를 갱신하세요.", ""]
        else:
            lines += ["| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |", "|---|---|---|---|---|"]
            lines += ["| " + " | ".join(cell(x.get(k)) for k in ("key", "question_key", "label", "type", "example")) + " |" for x in f["fields"]]
            lines += [""]
        for s in f["scenarios"]:
            lines += [f"연결 업무 {s['id']} · 추출/비교 작업:", ""]
            if not s["operations"]:
                lines += ["명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.", ""]
            for op in s["operations"]:
                lines += ["```json", json.dumps(op, ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)


def document(name: str) -> str:
    if name not in DOCUMENTS:
        raise KeyError(name)
    return markdown(catalog()) if name == "catalog.md" else (ROOT / "guide" / name).read_text(encoding="utf-8")


def export() -> None:
    data = catalog()
    (ROOT / "guide/catalog.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (ROOT / "guide/catalog.md").write_text(markdown(data), encoding="utf-8")
    print(f"Exported {len(data['forms'])} forms and {len(data['scenarios'])} scenarios.")


if __name__ == "__main__":
    export()
