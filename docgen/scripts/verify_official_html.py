"""공식 대조 HTML 전부를 렌더링하고 원문/HTML 비교 그림을 만든다.

python -m docgen.scripts.verify_official_html --out studio_cache/official_html/verification
생성 데이터셋에는 쓰지 않는 검증용 출력이다.
"""
import argparse
import json
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFont

from docgen.entities import make_profile
from docgen.htmlform import check, load_form
from docgen.image import ImageRenderer
from docgen.registry import load_all
from docgen.render import render
from docgen.schema import build_fields

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, default=Path('studio_cache/official_html/verification'))
    ap.add_argument('--id', action='append')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT/'manual/official_html_sources.json').read_text(encoding='utf8'))
    rows = []
    thumbnails = []
    try:
        font = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 13)
    except OSError:
        font = ImageFont.load_default()
    profile = make_profile(3, bank='하나은행')
    with ImageRenderer(scale=1) as renderer:
        for entry in manifest['forms']:
            if args.id and entry['id'] not in args.id:
                continue
            doc_id = entry['id']
            folder = args.out/doc_id
            folder.mkdir(exist_ok=True)
            html, raw, data = render(load_all()[doc_id], profile, 3)
            (folder/'preview.html').write_text(html, encoding='utf8')
            info = renderer.render(html, folder/'page.png', texts=True)
            fields = build_fields(raw, info)
            warnings = check(load_form(doc_id), raw, data, info['overflow'])
            pdf = pymupdf.open(ROOT/entry['source_file'])
            pages = entry.get('source_pages', list(range(len(pdf))))
            assert len(pages) == len(info['pages']), (doc_id, 'page count')
            assert not info['overflow'], (doc_id, 'overflow')
            assert not warnings, (doc_id, warnings)
            for pno, source_pno in enumerate(pages):
                pdf[source_pno].get_pixmap(matrix=pymupdf.Matrix(96/72, 96/72)).save(folder/f'source_{pno+1}.png')
            for f in fields:
                if not f.get('bbox'):
                    continue
                pg = info['pages'][f.get('page', 0)]
                x0, y0, x1, y1 = f['bbox']
                assert 0 <= x0 <= x1 <= pg['width']+1 and 0 <= y0 <= y1 <= pg['height']+1, (doc_id, f)
            row = {'id': doc_id, 'pages': len(pages), 'fields': len(fields), 'ocr_words': len(info['texts']),
                   'warnings': warnings, 'overflow': info['overflow']}
            rows.append(row)
            (args.out/'checks.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf8')
            tile = Image.new('RGB', (400, 330), '#eee')
            ImageDraw.Draw(tile).text((5, 4), doc_id+' / 원문 · HTML', font=font, fill='black')
            for col, path in enumerate([folder/'source_1.png', Path(info['images'][0])]):
                im = Image.open(path).convert('RGB')
                im.thumbnail((196, 300))
                tile.paste(im, (col*200+(200-im.width)//2, 25))
            thumbnails.append(tile)
            print(f'{doc_id}: {len(pages)}p / {len(fields)} fields / OK', flush=True)
            pdf.close()
    for offset in range(0, len(thumbnails), 6):
        sheet = Image.new('RGB', (1200, 660), 'white')
        for i, tile in enumerate(thumbnails[offset:offset+6]):
            sheet.paste(tile, ((i%3)*400, (i//3)*330))
        sheet.save(args.out/f'comparison_{offset//6+1:02d}.png')
    print(f'Checked {len(rows)} forms, {sum(r["pages"] for r in rows)} pages', flush=True)


if __name__ == '__main__':
    main()
