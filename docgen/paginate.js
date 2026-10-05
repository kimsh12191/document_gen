// 페이지 나눔: A4 서류(.page.a4)의 내용이 한 장을 넘치면 다음 쪽(.page)으로 나눈다.
//  - 블록(문단, 표, 섹션) 단위로 넘기고, 표는 줄(tr) 단위로 자른다. 표 머리글 줄은 다음 쪽에 반복한다.
//  - rowspan 이 걸친 줄 사이에서는 자르지 않는다.
//  - 절대 위치 장식(견본 워터마크 등)은 쪽마다 복사한다.
//  - .pg-repeat 요소(발급번호 줄 등)는 다음 쪽 맨 위에 복사한다.
//  - 여러 쪽이 되면 쪽 번호(- 1 / 3 -)와 "다음 쪽에 계속"을 넣는다. 문구는 .page 의 data-pg-* 속성으로 바꿀 수 있다.
() => {
  const MAX_PAGES = 12;
  const RESERVE = 26; // 쪽 번호 자리
  const pages = Array.from(document.querySelectorAll('.page.a4, .page.a4_landscape'));
  let made = 0;

  const isAbs = el => { const p = getComputedStyle(el).position; return p === 'absolute' || p === 'fixed'; };
  const limitOf = page => {
    const r = page.getBoundingClientRect(), cs = getComputedStyle(page);
    return r.top + page.clientHeight - parseFloat(cs.paddingBottom) - RESERVE;
  };
  const bottom = el => {
    const rects = Array.from(el.getClientRects());
    return rects.length ? Math.max(...rects.map(r => r.bottom)) : el.getBoundingClientRect().bottom;
  };

  // 표 머리글 줄: thead 의 줄, 또는 맨 위에서부터 이어지는 '모든 칸이 th 인' 줄
  const headerRows = table => {
    if (table.tHead) return Array.from(table.tHead.rows);
    const out = [];
    for (const row of table.rows) {
      const cells = Array.from(row.cells);
      if (cells.length && cells.every(c => c.tagName === 'TH') && out.length < 3) out.push(row); else break;
    }
    return out;
  };

  // 표를 줄 단위로 자른다. 잘린 뒷부분(새 표)을 돌려주며, 자를 수 없으면 null.
  const splitTable = (table, limit) => {
    const rows = Array.from(table.rows);
    const heads = headerRows(table);
    const body = rows.filter(r => !heads.includes(r));
    if (body.length < 2) return null;
    // 각 줄에서 위쪽 rowspan 이 끝나는지
    const covered = new Array(rows.length).fill(false);
    rows.forEach((r, i) => { for (const c of r.cells) for (let k = 1; k < (c.rowSpan || 1); k++) if (i + k < rows.length) covered[i + k] = true; });
    let cut = -1;
    for (let i = 0; i < rows.length; i++) {
      if (heads.includes(rows[i])) continue;
      if (bottom(rows[i]) > limit) { cut = i; break; }
    }
    if (cut < 0) return null;
    while (cut > 0 && covered[cut]) cut--;
    const firstBody = rows.indexOf(body[0]);
    if (cut <= firstBody) return 'whole';
    const clone = table.cloneNode(false);
    if (table.tHead) clone.appendChild(table.tHead.cloneNode(true));
    const tb = document.createElement('tbody');
    if (!table.tHead) heads.forEach(h => tb.appendChild(h.cloneNode(true)));
    rows.slice(cut).forEach(r => tb.appendChild(r));
    clone.appendChild(tb);
    // 원래 표에서 빈 tbody 정리
    for (const b of Array.from(table.tBodies)) if (!b.rows.length) b.remove();
    return clone;
  };

  // container 안에서 limit 을 넘는 첫 자식부터 뒤를 잘라 새 컨테이너(같은 태그·속성)에 담아 돌려준다.
  const splitContainer = (container, limit, depth) => {
    const kids = Array.from(container.children).filter(k => !isAbs(k) && getComputedStyle(k).display !== 'none');
    let idx = kids.findIndex(k => bottom(k) > limit);
    if (idx < 0) return null;
    const out = container.cloneNode(false);
    const k = kids[idx];
    let movedFirst = null;
    if (k.tagName === 'TABLE') {
      const rest = splitTable(k, limit);
      if (rest && rest !== 'whole') movedFirst = rest;
    } else if (depth < 4 && k.children.length && ['DIV', 'SECTION', 'OL', 'UL', 'TBODY'].includes(k.tagName)
               && getComputedStyle(k).display !== 'flex') {
      const rest = splitContainer(k, limit, depth + 1);
      if (rest && rest.childNodes.length && k.children.length) movedFirst = rest;
    }
    // 제목(.pg-keep-with-next, h2/h3, .bf-sec 등)이 다음 블록과 떨어져 쪽 끝에 홀로 남지 않게 함께 넘긴다
    const keep = el => el && (el.matches('.pg-keep-with-next, h2, h3, h4, .sec, .bf-sec, caption'));
    if (!movedFirst) { while (idx > 1 && keep(kids[idx - 1])) idx--; }
    if (movedFirst) { out.appendChild(movedFirst); idx += 1; }
    else if (idx === 0 && depth === 0) {
      // 첫 블록부터 안 들어가면(한 덩어리가 너무 큼) 그대로 둔다
      return null;
    }
    for (const rest of kids.slice(idx)) out.appendChild(rest);
    // 남은 형제 텍스트 노드는 그대로 둔다
    return out.childNodes.length ? out : null;
  };

  for (const first of pages) {
    if (first.scrollHeight <= first.clientHeight + 1) continue;
    const decor = Array.from(first.children).filter(k => isAbs(k) && !k.querySelector('[data-field]') && !k.matches('[data-field], [data-mark]'));
    const repeat = Array.from(first.querySelectorAll('.pg-repeat'));
    const group = [first];
    let page = first;
    while (group.length < MAX_PAGES && page.scrollHeight > page.clientHeight + 1) {
      const limit = limitOf(page);
      const moved = splitContainer(page, limit, 0);
      if (!moved) break;
      const next = page.cloneNode(false);
      next.removeAttribute('id');
      repeat.forEach(r => { const c = r.cloneNode(true); c.classList.add('pg-repeated'); next.appendChild(c); });
      while (moved.firstChild) next.appendChild(moved.firstChild);
      decor.forEach(d => next.appendChild(d.cloneNode(true)));
      page.after(next);
      group.push(next);
      page = next;
      made++;
    }
    if (group.length > 1) {
      const n = group.length;
      const fmt = first.dataset.pgFormat || '- {i} / {n} -';
      const cont = first.dataset.pgCont ?? '다음 쪽에 계속';
      group.forEach((p, i) => {
        p.dataset.pageIndex = i;
        const no = document.createElement('div');
        no.className = 'pg-no';
        no.textContent = fmt.replace('{i}', i + 1).replace('{n}', n);
        no.style.cssText = 'position:absolute;left:0;right:0;bottom:14px;text-align:center;font-size:11px;color:#444;';
        p.appendChild(no);
        if (i < n - 1 && cont) {
          const c = document.createElement('div');
          c.className = 'pg-cont';
          c.textContent = cont;
          c.style.cssText = 'position:absolute;right:' + getComputedStyle(p).paddingRight + ';bottom:14px;font-size:11px;color:#444;';
          p.appendChild(c);
        }
      });
    }
  }
  return made;
}
