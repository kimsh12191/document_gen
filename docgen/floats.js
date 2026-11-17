// html 서식의 자유 위치 도장·번호 자리 (docgen/floats.py html_block). image.py 가 쪽 나눔(paginate.js) 뒤에 부른다.
// 요소마다 data-seed 로 정한 난수(같은 seed → 같은 자리): 쪽을 고르고, 쪽의 영역(data-area) 안에서 값 칸([data-field])과
// 겹치지 않는 자리(둘 중 작은 상자의 25% 이하)를 20번까지 찾는다. 인쇄 글자 위에는 겹쳐도 된다 (실제 서류처럼).
() => {
  const box = document.getElementById('dg-floats');
  if (!box) return;
  const areas = JSON.parse(box.dataset.areas);
  const pages = Array.from(document.querySelectorAll('.page'));
  if (!pages.length) return;
  const overlap = (a, b) => {
    const ix = Math.max(0, Math.min(a[2], b[2]) - Math.max(a[0], b[0])), iy = Math.max(0, Math.min(a[3], b[3]) - Math.max(a[1], b[1]));
    return ix * iy / Math.max(1, Math.min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1])));   // 둘 중 작은 상자 기준
  };
  for (const el of Array.from(box.children)) {
    let s = Number(el.dataset.seed) | 0;
    const rnd = () => { s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
    const page = pages[Math.floor(rnd() * pages.length)];
    const pb = page.getBoundingClientRect();
    el.style.visibility = 'hidden';
    el.style.left = '0px'; el.style.top = '0px';
    page.appendChild(el);
    const w = el.offsetWidth, h = el.offsetHeight;
    const a = areas[el.dataset.area] || areas.any;
    const x0 = a[0] * pb.width, y0 = a[1] * pb.height, x1 = Math.max(x0, a[2] * pb.width - w), y1 = Math.max(y0, a[3] * pb.height - h);
    const busy = Array.from(page.querySelectorAll('[data-field]')).filter(f => !el.contains(f) && f.textContent.trim()).map(f => {
      const r = f.getBoundingClientRect();
      return [r.left - pb.left, r.top - pb.top, r.right - pb.left, r.bottom - pb.top];
    });
    let best = null, bestOv = 2;
    for (let k = 0; k < 20; k++) {
      const x = x0 + rnd() * (x1 - x0), y = y0 + rnd() * (y1 - y0);
      const ov = Math.max(0, ...busy.map(b => overlap([x, y, x + w, y + h], b)));
      if (ov < bestOv) { best = [x, y]; bestOv = ov; }
      if (ov <= 0.25) break;
    }
    el.style.left = best[0].toFixed(1) + 'px'; el.style.top = best[1].toFixed(1) + 'px';
    el.style.visibility = ''; el.style.zIndex = 5;
  }
  box.remove();
}
