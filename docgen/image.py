"""HTML → PNG 렌더링 (Playwright/Chromium). 필드·항목명·체크박스·도장 위치(bbox)도 함께 추출한다.

서류 한 건이 여러 쪽(.page 여러 개)이면 쪽마다 이미지를 따로 저장한다.
페이지 나눔은 paginate.js 가 브라우저에서 처리한다 (A4 서류 .page.a4 · .page.a4_landscape 가 넘치면 다음 쪽으로).
원본 서식 배경·손글씨 글꼴·표시 요소 그림은 https://docgen.local/ 요청을 가로채 realform.serve() 가 넘겨 준다.
docgen generate --png, docgen.bench build, docgen.ocr_set, preview(studio), docgen/scripts/make_samples.py 가 쓴다.
"""
from __future__ import annotations

import os
from pathlib import Path

_PAGINATE_JS = (Path(__file__).resolve().parent / "paginate.js").read_text(encoding="utf-8")
_HTML_REGIONS_JS = (Path(__file__).resolve().parent / "html_regions.js").read_text(encoding="utf-8")

_JS_COLLECT = """
() => {
  const pages = Array.from(document.querySelectorAll('.page'));
  const bases = pages.map(p => p.getBoundingClientRect());
  const box = el => {
    const rects = Array.from(el.getClientRects()).filter(r => r.width > 0 && r.height > 0);
    if (!rects.length) return null;
    const page = pages.indexOf(el.closest('.page'));
    if (page < 0) return null;
    const b = bases[page];
    return {page, bbox: [Math.min(...rects.map(r => r.left)) - b.left, Math.min(...rects.map(r => r.top)) - b.top,
                         Math.max(...rects.map(r => r.right)) - b.left, Math.max(...rects.map(r => r.bottom)) - b.top]};
  };
  const collect = (sel, attr) => {
    const out = [];
    for (const el of document.querySelectorAll(sel)) {
      const r = box(el);
      if (r) out.push({key: el.getAttribute(attr), ...r});
    }
    return out;
  };
  // 항목명 위치: data-label 이 없으면 같은 줄 바로 앞 칸(th) 또는 같은 열의 머리글(th)을 쓴다.
  const autoLabels = [];
  for (const el of document.querySelectorAll('[data-field]')) {
    const td = el.closest('td');
    if (!td) continue;
    let th = td.previousElementSibling;
    if (!(th && th.tagName === 'TH')) {
      th = null;
      const table = td.closest('table'), tr = td.parentElement;
      if (table && tr) {
        let col = 0;
        for (const c of tr.children) { if (c === td) break; col += c.colSpan || 1; }
        for (const row of table.rows) {
          if (row === tr) break;
          const cells = Array.from(row.cells);
          if (!cells.length || !cells.every(c => c.tagName === 'TH')) continue;
          let x = 0;
          for (const c of cells) { if (x <= col && col < x + (c.colSpan || 1)) { th = c; break; } x += c.colSpan || 1; }
        }
      }
    }
    if (th) { const r = box(th); if (r) autoLabels.push({key: el.dataset.field, src: 'th', text: th.innerText.replace(/\\s+/g, ''), ...r}); }
  }
  // 표 밖 항목명: 값(또는 값을 감싼 요소) 바로 앞의 짧은 글자 요소 (예: <div class="lbl">성명</div><div>값</div>)
  const done = new Set(autoLabels.map(a => a.key).concat(Array.from(document.querySelectorAll('[data-label]')).map(e => e.dataset.label)));
  for (const el of document.querySelectorAll('[data-field]')) {
    if (done.has(el.dataset.field)) continue;
    let cur = el;
    for (let up = 0; up < 3 && cur && !cur.classList.contains('page'); up++, cur = cur.parentElement) {
      const prev = cur.previousElementSibling;
      if (!prev) continue;
      const t = prev.innerText.replace(/\\s+/g, '');
      if (t.length >= 1 && t.length <= 24 && !prev.querySelector('[data-field]') && !prev.matches('[data-field], .seal, br')) {
        const r = box(prev), v = box(el);
        if (r && v && r.page === v.page && (r.bbox[2] <= v.bbox[0] + 4 || r.bbox[3] <= v.bbox[1] + 4)) {
          autoLabels.push({key: el.dataset.field, src: 'sib', text: t, ...r});
          break;
        }
      }
    }
  }
  const untagged = [];
  for (const el of document.querySelectorAll('.seal:not([data-mark]):not(.corr-seal)')) {
    const r = box(el);
    if (r) untagged.push({text: el.innerText.replace(/\\s+/g, ''), square: el.classList.contains('square'), ...r});
  }
  const seen = new Map(), anchors = [];
  for (const el of document.querySelectorAll('[data-field]')) {
    const key = el.dataset.field, count = seen.get(key) || 0;
    const occurrence = el.dataset.regionOccurrence === undefined ? count : Number(el.dataset.regionOccurrence);
    seen.set(key, count + 1);
    let r = box(el);
    if (!r || r.bbox[2] - r.bbox[0] < 1) r = box(el.closest('.entry, td, .value') || el.parentElement);
    if (r) anchors.push({key, occurrence, target:'field', text: el.innerText, ...r});
  }
  const specialSeen = new Map();
  const special = (target,key,option,el) => {
    const id=JSON.stringify([target,key,option]), count=specialSeen.get(id) || 0;
    const occurrence=el.__regionOccurrences?.[id] ?? count;
    specialSeen.set(id,count+1);
    const r=box(el);if(r) anchors.push({target,key,option,occurrence,text:el.innerText,...r});
  };
  for(const el of document.querySelectorAll('[data-mark],[data-mark2]')) for(const attr of ['data-mark','data-mark2']) if(el.hasAttribute(attr)) special('mark',el.getAttribute(attr),0,el);
  for(const el of document.querySelectorAll('[data-box]')) {const [key,opt]=el.dataset.box.split('#');special('box',key,Number(opt || 0),el);}
  return {
    anchors,
    fields: collect('[data-field]', 'data-field'),
    labels: collect('[data-label]', 'data-label'),
    auto_labels: autoLabels,
    boxes: collect('[data-box]', 'data-box'),
    opts: collect('[data-opt]', 'data-opt'),
    marks: collect('[data-mark]', 'data-mark').concat(collect('[data-mark2]', 'data-mark2')),
    untagged_seals: untagged,
    overflow: pages.some(p => p.scrollHeight > p.clientHeight + 1 || p.scrollWidth > p.clientWidth + 1),
    pages: bases.map(b => ({width: b.width, height: b.height})),
  };
}
"""


# 쪽 전체 글자 박스 (합성 OCR 정답용, docgen/ocr_export.py). 화면에 보이는 글자를 단어마다 잰다.
#   kind: text (보통 글자) / watermark (견본 표시) / seal (도장 안 글자) / struck (정정으로 두 줄 그은 글자)
#   blk: 같은 칸(td·th·p·li·div·span.ov)이면 같은 번호 — 줄로 묶을 때 쓴다
_JS_TEXTS = r"""
() => {
  const pages = Array.from(document.querySelectorAll('.page'));
  const bases = pages.map(p => p.getBoundingClientRect());
  const blocks = new Map();
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    const el = node.parentElement, t = node.textContent;
    if (!el || !t.trim()) continue;
    const page = pages.indexOf(el.closest('.page'));
    if (page < 0) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.fontSize) < 4) continue;
    const m = cs.color.match(/rgba?\(([^)]+)\)/);
    if (cs.color === 'transparent' || (m && m[1].split(',').length === 4 && parseFloat(m[1].split(',')[3]) === 0)) continue;
    let op = 1;
    for (let a = el; a && a !== document.body; a = a.parentElement) op *= parseFloat(getComputedStyle(a).opacity || '1');
    if (op < 0.15) continue;
    const kind = el.closest('.sample-mark') ? 'watermark' : el.closest('.seal, .corr-seal') ? 'seal'
      : el.closest('s, .corr-old') ? 'struck' : 'text';
    const blkEl = el.closest('td, th, p, li, .ov, div') || el;
    if (!blocks.has(blkEl)) blocks.set(blkEl, blocks.size);
    const b = bases[page];
    const re = /\S+/g;
    let w;
    while ((w = re.exec(t))) {
      const rg = document.createRange();
      rg.setStart(node, w.index);
      rg.setEnd(node, w.index + w[0].length);
      const rects = Array.from(rg.getClientRects()).filter(x => x.width > 0.5 && x.height > 0.5);
      if (!rects.length) continue;
      let x0 = Math.min(...rects.map(x => x.left)) - b.left, y0 = Math.min(...rects.map(x => x.top)) - b.top;
      let x1 = Math.max(...rects.map(x => x.right)) - b.left, y1 = Math.max(...rects.map(x => x.bottom)) - b.top;
      x0 = Math.max(0, x0); y0 = Math.max(0, y0); x1 = Math.min(b.width, x1); y1 = Math.min(b.height, y1);
      if (x1 - x0 < 1 || y1 - y0 < 1) continue;
      out.push({page, text: w[0], kind, blk: blocks.get(blkEl), bbox: [x0, y0, x1, y1]});
    }
  }
  return out;
}
"""


def _executable() -> str | None:
    env = os.environ.get("CHROMIUM_PATH")
    if env:
        return env
    default = Path("/opt/pw-browsers/chromium")
    return str(default) if default.exists() else None


def page_paths(png_path: str | Path, n: int) -> list[Path]:
    """1쪽이면 그대로, 여러 쪽이면 <이름>_p1.png, <이름>_p2.png ..."""
    p = Path(png_path)
    return [p] if n == 1 else [p.with_name(f"{p.stem}_p{i + 1}{p.suffix}") for i in range(n)]


def _serve_local(route) -> None:
    """원본 서식 배경·손글씨 글꼴 (docgen/realform.py) 을 브라우저에 넘긴다."""
    from .realform import serve

    hit = serve(route.request.url)
    if hit is None:
        route.fulfill(status=404, body="")
    else:
        route.fulfill(status=200, body=hit[0], content_type=hit[1])


class ImageRenderer:
    """with ImageRenderer(scale=2) as r: r.render(html_str, "out.png")"""

    def __init__(self, scale: float = 2.0):
        self.scale = scale

    def __enter__(self):
        from playwright.sync_api import sync_playwright

        self._pw = sync_playwright().start()
        try:
            self._browser = self._pw.chromium.launch()
        except Exception:
            exe = _executable()
            if not exe:
                raise
            self._browser = self._pw.chromium.launch(executable_path=exe)
        self._page = self._browser.new_page(device_scale_factor=self.scale, viewport={"width": 1200, "height": 1200})
        self._page.route("https://docgen.local/**", _serve_local)
        return self

    def finish(self, rest: list, stop=lambda: False) -> bool:
        """render(first_only=True) 의 남은 쪽을 지금 화면에서 찍는다. stop() 이 참이면 거기서 멈추고 False."""
        els = self._page.locator(".page").all()
        for i, path in rest:
            if stop():
                return False
            els[i].screenshot(path=str(path))
        return True

    def __exit__(self, *exc):
        self._browser.close()
        self._pw.stop()

    def render(self, html: str, png_path: str | Path, texts: bool = False, first_only: bool = False) -> dict:
        """PNG 저장 후 위치 정보를 돌려준다 (좌표는 이미지 픽셀, 각 쪽 왼쪽 위 기준).

        {'images': [경로...], 'pages': [{width, height}], 'fields'|'labels'|'boxes'|'marks': [{key, page, bbox}],
         'untagged_seals': [...], 'overflow': bool, 'width', 'height'(1쪽 크기)}
        texts=True 면 'texts': 쪽 전체 글자 단어 박스 [{page, text, kind, blk, bbox}] 도 (배경 그림 속 글자는 없음)
        first_only=True 면 1쪽 그림만 찍고, 남은 쪽은 info['rest'] 로 돌려준다 → 다른 html 을 넣기 전에 finish(info['rest'])
        """
        self._page.set_content(html, wait_until="load")
        self._page.evaluate("document.fonts.ready")
        self._page.evaluate("(" + _PAGINATE_JS + ")()")  # 넘친 쪽 나누기
        self._page.evaluate("(" + _HTML_REGIONS_JS + ")()")
        info = self._page.evaluate(_JS_COLLECT)
        if texts:
            info["texts"] = self._page.evaluate(_JS_TEXTS)
        s = self.scale
        paths = page_paths(png_path, len(info["pages"]))
        for i, (el, path) in enumerate(zip(self._page.locator(".page").all(), paths)):
            if first_only and i:
                info.setdefault("rest", []).append([i, str(path)])
                continue
            el.screenshot(path=str(path))
        for k in ("fields", "labels", "auto_labels", "boxes", "opts", "marks", "untagged_seals", "texts", "anchors"):
            for it in info.get(k, []):
                it["bbox"] = [round(v * s, 1) for v in it["bbox"]]
        info["pages"] = [{"width": round(p["width"] * s), "height": round(p["height"] * s)} for p in info["pages"]]
        info["images"] = [str(p) for p in paths]
        info["width"], info["height"] = info["pages"][0]["width"], info["pages"][0]["height"]
        return info
