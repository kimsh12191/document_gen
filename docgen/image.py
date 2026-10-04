"""HTML → PNG 렌더링 (Playwright/Chromium). 각 필드의 bbox 도 함께 추출한다."""
from __future__ import annotations

import os
from pathlib import Path

_JS_COLLECT = """
() => {
  const page = document.querySelector('.page');
  const base = page.getBoundingClientRect();
  const out = [];
  for (const el of document.querySelectorAll('[data-field]')) {
    const rects = Array.from(el.getClientRects()).filter(r => r.width > 0 && r.height > 0);
    if (!rects.length) continue;
    const x0 = Math.min(...rects.map(r => r.left)) - base.left, y0 = Math.min(...rects.map(r => r.top)) - base.top;
    const x1 = Math.max(...rects.map(r => r.right)) - base.left, y1 = Math.max(...rects.map(r => r.bottom)) - base.top;
    out.push({key: el.dataset.field, bbox: [x0, y0, x1, y1]});
  }
  return {fields: out, overflow: page.scrollHeight > page.clientHeight + 1 || page.scrollWidth > page.clientWidth + 1,
          width: base.width, height: base.height};
}
"""


def _executable() -> str | None:
    env = os.environ.get("CHROMIUM_PATH")
    if env:
        return env
    default = Path("/opt/pw-browsers/chromium")
    return str(default) if default.exists() else None


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
        """PNG 저장 후 {'fields': [{key, bbox(px, 이미지 좌표)}], 'overflow', 'width', 'height'} 반환."""
        self._page.set_content(html, wait_until="load")
        self._page.evaluate("document.fonts.ready")
        info = self._page.evaluate(_JS_COLLECT)
        self._page.locator(".page").screenshot(path=str(png_path))
        s = self.scale
        for fld in info["fields"]:
            fld["bbox"] = [round(v * s, 1) for v in fld["bbox"]]
        info["width"], info["height"] = round(info["width"] * s), round(info["height"] * s)
        return info
