"""하나은행 공개 서식 PDF → '수정 영역(기재란)' 명세 뽑기.

  python scripts/extract_form_fields.py            # 전체
  python scripts/extract_form_fields.py --no 171   # 한 건만 (확인용)

서식 PDF 에는 AcroForm 필드가 없다. 대신 인쇄된 레이아웃 자체가 명세이므로
텍스트 레이어와 표 구조에서 다음을 뽑는다.

  meta      서식코드·개정년월·보존년한 (상단 줄) → _loan_parts.j2 의 FORMS 표에 넣을 값
  sections  "1. 기본정보" 같은 번호 붙은 섹션 제목
  fields    표에서 (라벨 셀, 빈 값 셀) 쌍 — 고객이 채우는 칸
  choices   체크박스 묶음 (□ 로 시작하는 보기들)
  marks     서명·날인 자리 ("서명 또는 (인)", 결재란)

결과는 add_template/field_specs/<분류>/<No>.json 에 저장한다.
이 JSON 이 템플릿을 만들 때의 작업지시서가 된다.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "add_template" / "하나은행_서식자료"
OUT = ROOT / "add_template" / "field_specs"

# 상단 서식번호 줄:  5-14-0020(3-1) (2026.06 개정) (보존년한 : 해지일로부터 10년)
RE_CODE = re.compile(r"(\d-\d\d-\d{4})\s*\((\d+)-(\d+)\)")
RE_REV = re.compile(r"\((\d{4})[.\s]*(\d{1,2})\s*개정\)")
RE_KEEP = re.compile(r"보존년한\s*[:：]\s*([가-힣]+)일로부터\s*(\d+)\s*년")
RE_SECTION = re.compile(r"^\s*(\d{1,2})\.\s*(\S.{0,60})$")
RE_SIGN = re.compile(r"서명\s*(또는)?\s*[(（]?인[)）]?|\(서명\)|\(인\)")

# 결재·전산 칸 (고객 기재란이 아니다)
BANK_ONLY = {"담당", "담당자", "책임자", "관리자", "부점장", "지점장", "검인", "판매직원", "본인확인",
             "전산인자란", "접수일자", "접수번호", "실명확인", "확인자", "취급자"}
# 라벨로 보기 어려운 셀
NOT_LABEL = re.compile(r"^[\s□■○●·\-–—]*$|^[0-9,.\s%]+$")
# 라벨이 아니라 설명 문장인 셀 (서식 본문 안내 문구가 표 안에 들어가 있는 경우)
SENTENCE = re.compile(r"(합니다|바랍니다|하였|합은|경우|입니다|가능|제출|신청하)")


def clean(s: str | None) -> str:
    return " ".join((s or "").replace("\xa0", " ").split())


def options(text: str) -> list[str]:
    """'□ 가 □ 나 ※ 주석' → ['가', '나']. 보기 뒤에 붙은 주석·설명은 떼어낸다."""
    out = []
    for o in re.split(r"[□■]", text)[1:]:
        o = clean(re.split(r"[※*]|\s{2,}", o)[0])
        o = re.sub(r"\s*[:：].*$", "", o)
        if 1 <= len(o) <= 30:
            out.append(o)
    return out


def parse_meta(text: str) -> dict:
    meta: dict = {}
    if m := RE_CODE.search(text):
        meta["code"] = m.group(1)
        meta["pages_in_set"] = int(m.group(2))
    if m := RE_REV.search(text):
        meta["revised"] = f"{m.group(1)}.{int(m.group(2)):02d}"
    if m := RE_KEEP.search(text):
        meta["keep_from"] = m.group(1)   # 완제 / 해지 ...
        meta["keep_years"] = int(m.group(2))
    return meta


def parse_choices(text: str) -> list[dict]:
    """□ 로 시작하는 보기 묶음. 한 줄에 여러 개면 한 묶음으로 본다."""
    out = []
    for line in text.splitlines():
        line = clean(line)
        if line.count("□") + line.count("■") < 1:
            continue
        if opts := options(line):
            out.append({"options": opts})
    return out


def parse_tables(page) -> tuple[list[dict], list[str]]:
    """(기재란, 은행 전용칸). 표의 빈 셀 왼쪽에 라벨이 있으면 고객 기재란으로 본다."""
    fields, bank = [], []
    try:
        tables = page.find_tables().tables
    except Exception:  # noqa: BLE001 - 표 인식 실패한 페이지는 건너뛴다
        return fields, bank
    for t in tables:
        try:
            rows = t.extract()
        except Exception:  # noqa: BLE001
            continue
        for row in rows:
            cells = [clean(c) for c in row]
            for i, c in enumerate(cells):
                if not c or NOT_LABEL.match(c) or len(c) > 24:
                    continue
                if c.startswith(("□", "■")) or SENTENCE.search(c) or "%" in c:
                    continue                        # 보기 칸·안내 문장은 라벨이 아니다
                if c in BANK_ONLY:
                    bank.append(c)
                    continue
                nxt = cells[i + 1] if i + 1 < len(cells) else None
                if nxt == "":                       # 라벨 + 빈 칸 = 기재란
                    fields.append({"label": c, "kind": "text"})
                elif nxt and ("□" in nxt or "■" in nxt):
                    if opts := options(nxt):
                        fields.append({"label": c, "kind": "choice", "options": opts})
    return fields, bank


def extract(pdf: Path, no: int, cls: str, name: str) -> dict:
    doc = pymupdf.open(pdf)
    n_pages = doc.page_count
    full = ""
    sections: list[str] = []
    fields: list[dict] = []
    bank_cols: list[str] = []
    for page in doc:
        text = page.get_text().replace("\xa0", " ")
        full += text + "\n"
        for line in text.splitlines():
            if m := RE_SECTION.match(clean(line)):
                sections.append(f"{m.group(1)}. {m.group(2)}")
        f, b = parse_tables(page)
        fields += f
        bank_cols += b
    doc.close()

    seen, uniq = set(), []
    for f in fields:
        k = (f["label"], f["kind"])
        if k not in seen:
            seen.add(k)
            uniq.append(f)
    return {
        "no": no, "class": cls, "name": name, "file": str(pdf.relative_to(ROOT)),
        "pages": n_pages,
        "meta": parse_meta(full[:400]),
        "sections": sections,
        "fields": uniq,
        "choices": parse_choices(full),
        "bank_only": sorted(set(bank_cols)),
        "has_signature": bool(RE_SIGN.search(full)),
        "text_chars": len(full),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no", type=int, help="이 번호의 서식만 처리")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    import csv
    rows = list(csv.DictReader((SRC / "다운로드_결과.csv").read_text(encoding="utf-8-sig").splitlines(True)))
    out = Path(args.out)
    done = skipped = 0
    for r in rows:
        no = int(r["No"])
        if args.no and no != args.no:
            continue
        if r["형식"] != "PDF":
            skipped += 1
            continue
        pdf = SRC / r["저장 파일"].replace("\\", "/")
        if not pdf.exists():
            skipped += 1
            continue
        try:
            spec = extract(pdf, no, r["분류"], " ".join(r["서식명"].split()))
        except Exception as e:  # noqa: BLE001 - 깨진 PDF 는 건너뛰고 계속한다
            print(f"  !! {no} {pdf.name}: {type(e).__name__} {e}", file=sys.stderr)
            skipped += 1
            continue
        d = out / r["분류"]
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{no:03d}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
        done += 1
        print(f"{no:4d} {spec['class']:8s} {len(spec['fields']):3d} fields "
              f"{len(spec['choices']):3d} choice-lines {spec['pages']}p  {spec['name'][:50]}")
    print(f"\n완료 {done}건, 건너뜀 {skipped}건 → {out}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
