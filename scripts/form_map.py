"""하나은행 공개 서식 441건 → docgen 서류 대응표.

  python scripts/form_map.py > docs/FORM_MAP.md

모든 서식은 원본 PDF 를 배경으로 쓰는 오버레이(docgen/realform.py)로 hf<No> 에 등록된다.
기재 자리는 scripts/extract_form_layout.py 가 뽑은 add_template/layouts/<분류>/<No>.json.
등록되지 않는 것은 PDF 가 아니거나(XLS·DOC·EXE), 고객이 쓰는 칸이 없는 인쇄물(약관·안내장 등)이다.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from docgen.realform import EXCLUDE_KW, EXCLUDE_NO, fillable, layout_path  # noqa: E402
from docgen.registry import load_all  # noqa: E402

CSV = ROOT / "add_template" / "하나은행_서식자료" / "다운로드_결과.csv"


def main() -> None:
    reg = load_all()
    rows = list(csv.DictReader(CSV.read_text(encoding="utf-8-sig").splitlines(True)))
    out = []
    for r in rows:
        no = int(r["No"])
        name = " ".join(r["서식명"].split())
        lp = layout_path(no)
        lay = json.loads(lp.read_text(encoding="utf-8")) if lp else None
        kinds = Counter(it["t"] for it in lay["items"]) if lay else Counter()
        doc_id = f"hf{no:03d}"
        if doc_id in reg:
            verdict, note = "등록", ""
        elif r["형식"] != "PDF":
            verdict, note = "제외", f"{r['형식']} 파일 — PDF 원본이 아니다"
        elif no in EXCLUDE_NO or any(k in name for k in EXCLUDE_KW):
            verdict, note = "제외", "고객 기재란이 없는 인쇄물 (약관·안내장·내부 점검표 등)"
        elif lay is not None and fillable(lay) < 2:
            verdict, note = "제외", "기재 자리를 2개 이상 찾지 못함"
        else:
            verdict, note = "제외", "레이아웃 없음"
        out.append({"no": no, "cls": r["분류"], "name": name, "url": r["원본 URL"], "fmt": r["형식"],
                    "verdict": verdict, "note": note, "pages": len(lay["pages"]) if lay else None,
                    "text": kinds["text"], "check": kinds["check"], "date": kinds["date"],
                    "sign": kinds["sign"] + kinds["copy"], "id": doc_id if verdict == "등록" else ""})

    cnt = Counter(x["verdict"] for x in out)
    p = print
    p("# 하나은행 공개 서식 441건 — 서류 대응표\n")
    p("`python scripts/form_map.py > docs/FORM_MAP.md` 로 자동 생성된다.\n")
    p("모든 서식은 **원본 PDF 를 그대로 배경으로 깔고** 손님이 쓴 것처럼 값을 얹는다 "
      "([docgen/realform.py](../docgen/realform.py)). 그래서 이미지 속 서식은 원본과 똑같다. "
      "값을 쓸 자리는 [scripts/extract_form_layout.py](../scripts/extract_form_layout.py) 가 PDF 의 글자·선에서 뽑아 "
      "`add_template/layouts/` 에 둔다.\n")
    p(f"- 등록: **{cnt['등록']}종** (서류 ID `hf<No>`, 그룹 `hana`)")
    p(f"- 제외: {cnt['제외']}종\n")
    p("열 설명: 칸 = 글자 기재란, 체크 = □ 보기 묶음, 날짜 = '년 월 일' 빈칸, 서명 = 서명·날인·자필 기재 자리\n")
    for cls in dict.fromkeys(x["cls"] for x in out):
        items = [x for x in out if x["cls"] == cls]
        p(f"## {cls} ({len(items)}건, 등록 {sum(1 for x in items if x['verdict'] == '등록')})\n")
        p("| No | 서식명 | 쪽 | 칸 | 체크 | 날짜 | 서명 | 서류 ID | 비고 |\n|---:|---|---:|---:|---:|---:|---:|---|---|")
        for x in items:
            p(f"| {x['no']} | [{x['name']}]({x['url']}) | {x['pages'] or ''} | {x['text'] or ''} | {x['check'] or ''} | "
              f"{x['date'] or ''} | {x['sign'] or ''} | {('`' + x['id'] + '`') if x['id'] else ''} | {x['note']} |")
        p("")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
