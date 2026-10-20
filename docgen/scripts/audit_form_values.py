"""전 서식을 실제 이미지로 다시 그려 값/위치/빈 칸을 기록한다.

python -m docgen.scripts.audit_form_values --out studio_cache/value_audit/rendered
설명서·미사용 행·빈 체크/도장은 값 누락과 구분한다. 자동 검사는 사람의 원문 대조 검수를 대체하지 않는다.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from docgen.entities import make_profile
from docgen.image import ImageRenderer
from docgen.registry import load_all
from docgen.render import render
from docgen.schema import build_fields
from docgen.preview import source_hash


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--ids", default="all")
    ap.add_argument("--seeds", default="0")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    reg = load_all()
    ids = list(reg) if a.ids == "all" else a.ids.split(",")
    rows = []
    start = time.time()
    with ImageRenderer(scale=1) as renderer:
        for n, did in enumerate(ids):
            spec = reg[did]
            for seed in map(int, a.seeds.split(",")):
                row = {"id": did, "name": spec.name, "kind": "overlay" if spec.template == "_real_form.html.j2" else "html", "seed": seed,
                       "source_hash": source_hash(did), "checked_at": time.strftime("%Y-%m-%d %H:%M"), "human_reviewed": False}
                try:
                    p = make_profile(seed, bank="하나은행")
                    html, raw, data = render(spec, p, seed)
                    folder = a.out / did / str(seed)
                    folder.mkdir(parents=True, exist_ok=True)
                    info = renderer.render(html, folder / "page.png")
                    fields = build_fields(raw, info)
                    text = [f for f in fields if f.get("type") not in ("checkbox", "checkbox_multi", "seal", "signature") and not f.get("group")]
                    empty = [f for f in text if f.get("value") in (None, "")]
                    missing = [f for f in text if f.get("value") not in (None, "") and not f.get("bbox")]
                    offpage = [f for f in fields if f.get("bbox") and (f["bbox"][0] < -1 or f["bbox"][1] < -1 or f["bbox"][2] > info["pages"][f.get("page", 0)]["width"] + 1 or f["bbox"][3] > info["pages"][f.get("page", 0)]["height"] + 1)]
                    details = {"fields": fields, "anchors": info.get("anchors", []), "pages": info["pages"]}
                    (folder / "fields.json").write_text(json.dumps(details, ensure_ascii=False, indent=1), encoding="utf-8")
                    row.update(pages=len(info["images"]), images=[str(Path(im).relative_to(a.out)).replace("\\", "/") for im in info["images"]],
                               text_fields=len(text), filled=len(text)-len(empty), empty=[{"key": f["key"], "label": f.get("label")} for f in empty],
                               missing_positions=[f["key"] for f in missing], offpage=[f["key"] for f in offpage], overflow=info["overflow"])
                    if did.startswith("gov_") or did in {"hana_personal_agreement", "hana_corporate_agreement", "hana_collateral_agreement", "hana_specific_guarantee", "hana_official_003"}:
                        row["coverage_note"] = "주요 기재란을 연결한 상태입니다. 인쇄된 모든 입력칸의 값 출처 연결은 완료되지 않았습니다."
                    if did == "hf407":
                        row["coverage_note"] = "FATCA/CRS 본문 설명서입니다. 자동 검출한 문장 조각 23개를 기재란으로 오인하고 있어 영역 검토가 필요합니다."
                    # 한 장에 전 쪽을 담아 빈 설명 페이지/후속 양식을 빠뜨리지 않는다.
                    thumbs = []
                    for im in info["images"]:
                        pic = Image.open(im).convert("RGB"); pic.thumbnail((220, 310)); thumbs.append(pic.copy())
                    sheet = Image.new("RGB", (240 * min(5, len(thumbs)), 335 * ((len(thumbs)+4)//5)), "#ddd")
                    draw = ImageDraw.Draw(sheet)
                    for j, pic in enumerate(thumbs):
                        x,y=(j%5)*240,(j//5)*335;sheet.paste(pic,(x+10,y+20));draw.text((x+10,y+3),f"{did} / p{j+1}",fill="black")
                    sheet.save(folder / "all_pages.jpg")
                except Exception as e:
                    row["error"] = f"{type(e).__name__}: {e}"
                rows.append(row)
            (a.out / "audit.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"{n+1}/{len(ids)} {did} filled={row.get('filled')} empty={len(row.get('empty', []))} {row.get('error', '')}", flush=True)
    summary = {"forms": len(ids), "renders": len(rows), "pages": sum(r.get("pages", 0) for r in rows),
               "errors": sum("error" in r for r in rows), "empty_fields": sum(len(r.get("empty", [])) for r in rows),
               "elapsed_seconds": round(time.time()-start)}
    (a.out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
