"""HTML → PNG 렌더링 (Playwright/Chromium). 필드·항목명·체크박스·도장 위치(bbox)도 함께 추출한다.

서류 한 건이 여러 쪽(.page 여러 개)이면 쪽마다 이미지를 따로 저장한다.
페이지 나눔은 paginate.js 가 브라우저에서 처리한다 (.page[data-paginate] 인 서류만).
"""
from __future__ import annotations

import os
from pathlib import Path

_PAGINATE_JS = (Path(__file__).resolve().parent / "paginate.js").read_text(encoding="utf-8")

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
  for (const el of document.querySelectorAll('.seal:not([data-mark])')) {
    const r = box(el);
    if (r) untagged.push({text: el.innerText.replace(/\\s+/g, ''), square: el.classList.contains('square'), ...r});
  }
  return {
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
        return self

    def __exit__(self, *exc):
        self._browser.close()
        self._pw.stop()

    def render(self, html: str, png_path: str | Path) -> dict:
        """PNG 저장 후 위치 정보를 돌려준다 (좌표는 이미지 픽셀, 각 쪽 왼쪽 위 기준).

        {'images': [경로...], 'pages': [{width, height}], 'fields'|'labels'|'boxes'|'marks': [{key, page, bbox}],
         'untagged_seals': [...], 'overflow': bool, 'width', 'height'(1쪽 크기)}
        """
        self._page.set_content(html, wait_until="load")
        self._page.evaluate("document.fonts.ready")
        self._page.evaluate(_PAGINATE_JS)
        info = self._page.evaluate(_JS_COLLECT)
        s = self.scale
        paths = page_paths(png_path, len(info["pages"]))
        for el, path in zip(self._page.locator(".page").all(), paths):
            el.screenshot(path=str(path))
        for k in ("fields", "labels", "auto_labels", "boxes", "opts", "marks", "untagged_seals"):
            for it in info[k]:
                it["bbox"] = [round(v * s, 1) for v in it["bbox"]]
        info["pages"] = [{"width": round(p["width"] * s), "height": round(p["height"] * s)} for p in info["pages"]]
        info["images"] = [str(p) for p in paths]
        info["width"], info["height"] = info["pages"][0]["width"], info["pages"][0]["height"]
        return info
