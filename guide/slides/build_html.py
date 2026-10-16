"""project/ (deck.json + slides/*.html, the web deck's own files) -> index.html, one page that opens offline.

  python guide/slides/build_html.py
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSS = """
body{margin:0;background:#2b333b;font-family:'IBM Plex Sans KR',Arial,sans-serif}
.wrap{max-width:1280px;margin:0 auto;padding:24px 16px 64px}
h1.title{color:#F6F5F1;font-size:24px;font-weight:600;margin:8px 0 20px}
.frame{position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;border-radius:8px;box-shadow:0 4px 24px rgba(0,0,0,.35);margin-top:24px}
.frame>section{position:absolute;left:0;top:0;width:1920px;height:1080px;box-sizing:border-box;transform-origin:0 0;overflow:hidden}
.frame section *{box-sizing:border-box;margin:0}
.frame section ul{padding-left:1.2em}
.frame section table{border-collapse:collapse;width:100%}
.frame section th,.frame section td{border:1px solid #D5DBE1;padding:.35em .6em;text-align:left;vertical-align:top}
.frame section aside{display:none}
x-shape{display:block;flex:none}
x-shape[kind=arrow-right]{clip-path:polygon(0 30%,60% 30%,60% 0,100% 50%,60% 100%,60% 70%,0 70%)}
x-icon{display:inline-flex;align-items:center;justify-content:center;font-weight:700}
x-icon[name=CheckCircle]::before{content:"✔";font-size:32px}
x-icon[name=Clock]::before{content:"◷";font-size:36px}
.notes{color:#C9D1D9;font-size:15px;line-height:1.6;margin:10px 4px 0}
.num{color:#8A96A3;font-size:13px;margin:6px 4px 0}
"""
FIT = """
function fit(){document.querySelectorAll('.frame').forEach(f=>{const s=f.firstElementChild;s.style.transform='scale('+(f.clientWidth/1920)+')';});}
addEventListener('resize',fit);addEventListener('load',fit);fit();
"""


def main():
    deck = json.loads((HERE / "project" / "deck.json").read_text(encoding="utf-8"))
    links = "".join(f'<link rel="stylesheet" href="{html.escape(f["href"])}">' for f in deck.get("faces", {}).values()
                    if f.get("href"))
    parts = []
    for n, sid in enumerate(deck["order"], 1):
        path = HERE / "project" / "slides" / f"{sid}.html"
        if not path.exists():
            continue
        section = path.read_text(encoding="utf-8").strip()
        notes = re.search(r"<aside>(.*?)</aside>", section, re.S)
        parts.append(f'<div class="frame">{section}</div><p class="num">{n} / {len(deck["order"])}</p>'
                     + (f'<p class="notes">{notes.group(1)}</p>' if notes else ""))
    page = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(deck["title"])}</title>'
            f'{links}<style>{CSS}</style></head><body><div class="wrap"><h1 class="title">{html.escape(deck["title"])}</h1>'
            + "".join(parts) + f"</div><script>{FIT}</script></body></html>")
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print(f"{len(parts)} slides -> {HERE / 'index.html'}")


if __name__ == "__main__":
    main()
