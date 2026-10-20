// ⑤ 검수 › OCR 검수: 가져온 묶음의 쪽마다 사내 OCR 글자·박스를 고치고 확인한다 → OCR 검수 정답 (사내 OCR 형식 그대로 저장).
// 설계: studio/DESIGN.md 8.7. 서버: studio/ocr_review.py (저장 위치 real_data_dir/ocr_reviewed/<묶음>/)
"use strict";

addRoute(/^#\/review\/([^/]+)\/(.+)$/, (b, p) => viewOcrPage(decodeURIComponent(b), decodeURIComponent(p)), "review");
addRoute(/^#\/review\/([^/]+)$/, b => viewReviewBatch(decodeURIComponent(b)), "review");

const REVIEW_NAME = { done: "확인", in_progress: "고치는 중" };

async function view_review() {
  const r = await api("/api/imports");
  main().innerHTML = `
    <h1>검수</h1>
    <div class="sub">OCR 검수: 가져온 묶음의 쪽마다 사내 OCR 이 읽은 글자와 박스를 고치고 "확인"합니다. 확인한 쪽은 OCR 검수 정답이 되어
      ④ 가져오기의 "OCR 벤치마크로"에서 정답으로 고를 수 있고, 원래 OCR 과의 차이가 사내 OCR 의 오류(글자 오류율·박스 F1)로 쌓입니다.
      라벨 검수·묶음 검수(결과 폴더, 실서류 업무 묶음)는 9단계에서 더해집니다.</div>
    ${realWarn(r)}
    ${r.imports.length ? table(r.imports, [
      ["name", "묶음", b => `<a href="#/review/${q(b.name)}">${esc(b.name)}</a>`],
      ["real_data", "실서류", b => b.real_data ? `<span class="tag warn">실서류</span>` : ""],
      ["n_ocr", "OCR 쪽", null, true],
      ["review", "확인", b => `${b.review.done}`, true], ["rv2", "고치는 중", b => `${b.review.in_progress || 0}`, true],
      ["cer", "사내 OCR 글자 오류율", b => b.review.done ? `${pct(b.review.ocr_cer)}%` : "-", true],
      ["f1", "박스 F1", b => b.review.done ? pct(b.review.box_f1) : "-", true],
      ["chg", "고친·더한·뺀 단어", b => b.review.done ? `${b.review.changed} · ${b.review.added} · ${b.review.deleted}` : "-"]])
      : `<p class="muted">가져온 묶음이 없습니다. <a href="#/import">④ 가져오기</a>에서 만듭니다.</p>`}`;
}

async function viewReviewBatch(name) {
  const b = await api(`/api/imports/${q(name)}`);
  const fmt = {};
  for (const f of b.formats) for (const p of f.pages) fmt[p] = f;
  const flt = store.get("rv.filter", { format: "", status: "" });
  const rows = b.pages.filter(p => p.has_ocr && (!flt.format || (fmt[p.id] && fmt[p.id].id === flt.format)) &&
    (!flt.status || (flt.status === "none" ? !p.review : p.review === flt.status)));
  const next = rows.find(p => p.review !== "done");
  main().innerHTML = `
    <div class="muted"><a href="#/review">검수</a> · <a href="#/import/${q(name)}">가져오기 › ${esc(name)}</a></div>
    <h1>OCR 검수 · ${esc(name)}</h1>
    <div class="sub">확인 ${b.review.done || 0} / OCR 쪽 ${b.pages.filter(p => p.has_ocr).length}${b.review.done ? ` · 사내 OCR 글자 오류율 ${pct(b.review.ocr_cer)}% · 박스 F1 ${pct(b.review.box_f1)}` : ""}</div>
    <div class="bar">
      <select id="rv-f"><option value="">포맷 전체</option>${b.formats.map(f => `<option value="${esc(f.id)}" ${flt.format === f.id ? "selected" : ""}>${esc(f.name)} (${f.pages.length})</option>`).join("")}</select>
      <select id="rv-s">${[["", "상태 전체"], ["none", "안 봄"], ["in_progress", "고치는 중"], ["done", "확인"]].map(([v, n]) =>
        `<option value="${v}" ${flt.status === v ? "selected" : ""}>${n}</option>`).join("")}</select>
      ${next ? `<button class="primary" onclick="location.hash='#/review/${q(name)}/${q(next.id)}'">다음 검수할 쪽부터</button>` : `<span class="tag ok">이 목록은 모두 확인했습니다</span>`}
    </div>
    ${table(rows, [["id", "쪽", p => `<a href="#/review/${q(name)}/${q(p.id)}">${esc(p.id)}</a>`],
      ["fmt", "포맷", p => esc(fmt[p.id] ? fmt[p.id].name : "-")], ["n_words", "단어", null, true],
      ["review", "상태", p => p.review ? `<span class="tag ${p.review === "done" ? "ok" : ""}">${REVIEW_NAME[p.review]}</span>` : `<span class="muted">안 봄</span>`]])}`;
  const save = () => { store.set("rv.filter", { format: $("#rv-f").value, status: $("#rv-s").value }); viewReviewBatch(name); };
  $("#rv-f").onchange = save; $("#rv-s").onchange = save;
}

// ---------------------------------------------------------------------------
// 쪽 하나 고치기
// ---------------------------------------------------------------------------

async function viewOcrPage(name, pid) {
  const [pg, b] = await Promise.all([api(`/api/imports/${q(name)}/ocr?p=${q(pid)}`), api(`/api/imports/${q(name)}`)]);
  const rv = {
    name, pid, pg, batch: b, words: pg.words.map(w => ({ ...w })), sel: new Set(), tool: "select",
    order: store.get("rv.order", "suspicious"), showOrig: false, showText: store.get("rv.text", false), dirty: false, ghost: null,
    zoom: store.get("rv.zoom", "fit"),
  };
  const ids = b.pages.filter(p => p.has_ocr).map(p => p.id);
  rv.next = ids.slice(ids.indexOf(pid) + 1).find(i => (b.pages.find(p => p.id === i) || {}).review !== "done") || null;
  rv.prev = ids[ids.indexOf(pid) - 1] || null;
  rv.nextAny = ids[ids.indexOf(pid) + 1] || null;
  const st = pg.state && pg.state.status;
  main().innerHTML = `
    <div class="muted"><a href="#/review">검수</a> › <a href="#/review/${q(name)}">${esc(name)}</a></div>
    <h1>${esc(pid)} ${st ? `<span class="tag ${st === "done" ? "ok" : ""}">${REVIEW_NAME[st]}</span>` : ""}</h1>
    <div class="bar">
      <button data-tool="select" title="고르기·옮기기 (Esc)">고르기</button><button data-tool="draw" title="새 박스 그리기 (N)">새 박스</button>
      <span class="sep"></span>
      <button id="rv-merge" title="고른 단어 합치기 (M)">합치기</button><button id="rv-split" title="글자 칸의 커서 자리에서 나누기 (S)">나누기</button>
      <button id="rv-del" title="지우기 (Delete)">지우기</button>
      <span class="sep"></span>
      <label><input type="checkbox" id="rv-orig"> 원래 OCR 겹쳐 보기</label>
      <label><input type="checkbox" id="rv-text" ${rv.showText ? "checked" : ""}> 글자 보기</label>
      <label>크기 <select id="rv-zoom"><option value="fit">맞춤</option><option value="100">원래 크기</option></select></label>
      <span style="flex:1"></span>
      ${rv.prev ? `<a href="#/review/${q(name)}/${q(rv.prev)}">← 앞 쪽</a>` : ""}
      ${rv.nextAny ? `<a href="#/review/${q(name)}/${q(rv.nextAny)}">뒤 쪽 →</a>` : ""}
      <button id="rv-save" title="Ctrl+S">저장</button>
      <button class="primary" id="rv-done" title="Ctrl+Enter: 확인하고 다음 검수할 쪽으로">확인 (검수 끝)</button>
    </div>
    <div class="viewer ed-viewer">
      <div id="rv-wrap"><div class="ed-stage tool-select" id="rv-stage"><img src="/api/imports/${q(name)}/page?p=${q(pid)}" alt=""><svg viewBox="0 0 ${pg.width} ${pg.height}" preserveAspectRatio="none"></svg><div class="tip"></div></div></div>
      <div class="side" id="rv-side"></div>
    </div>`;
  $("#rv-zoom").value = rv.zoom;
  rvBind(rv);
  rvDraw(rv);
  rvSideDraw(rv);
  state.keyHandler = e => rvKey(rv, e);
  state.leave = unload => !rv.dirty || (unload ? false : confirm("저장하지 않은 OCR 수정이 있습니다. 버릴까요?"));
}

const lowConf = w => !w.edited && w.confidence < 0.9;

function rvDraw(rv) {
  const svg = $("#rv-stage svg");
  if (!svg) return;
  const fs = w => Math.max(8, (w.bbox[3] - w.bbox[1]) * 0.8);
  const out = [];
  if (rv.showOrig) for (const w of rv.pg.original) {
    const [x0, y0, x1, y1] = w.bbox;
    out.push(`<rect class="rv-orig" x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}"></rect>`);
  }
  rv.words.forEach((w, i) => {
    const [x0, y0, x1, y1] = w.bbox;
    const cls = ["rv-w", w.added ? "added" : w.edited ? "edited" : lowConf(w) ? "low" : "", rv.sel.has(i) ? "sel" : ""].join(" ");
    out.push(`<rect data-i="${i}" class="${cls}" x="${x0}" y="${y0}" width="${Math.max(1, x1 - x0)}" height="${Math.max(1, y1 - y0)}"></rect>`);
    if (rv.showText) out.push(`<text x="${x0}" y="${y0 - 2}" font-size="${fs(w)}" class="rv-t">${esc(w.text)}</text>`);
  });
  if (rv.sel.size === 1) {
    const [x0, y0, x1, y1] = rv.words[[...rv.sel][0]].bbox, h = 7 * rvScale(rv);
    for (const [c, x, y] of [["nw", x0, y0], ["ne", x1, y0], ["sw", x0, y1], ["se", x1, y1]])
      out.push(`<rect class="handle" data-handle="${c}" x="${x - h / 2}" y="${y - h / 2}" width="${h}" height="${h}"></rect>`);
  }
  if (rv.ghost) {
    const [a, b, c, d] = rv.ghost;
    out.push(`<rect class="ghost" x="${Math.min(a, c)}" y="${Math.min(b, d)}" width="${Math.abs(c - a)}" height="${Math.abs(d - b)}"></rect>`);
  }
  svg.innerHTML = out.join("");
  const stage = $("#rv-stage");
  stage.className = `ed-stage tool-${rv.tool}`;
  stage.style.width = rv.zoom === "100" ? `${rv.pg.width}px` : "";
  $$("[data-tool]").forEach(bt => bt.classList.toggle("primary", bt.dataset.tool === rv.tool));
}

function rvScale(rv) {
  const svg = $("#rv-stage svg");
  return svg ? rv.pg.width / Math.max(1, svg.getBoundingClientRect().width) : 1;
}

function rvOrder(rv) {
  const idx = rv.words.map((_, i) => i);
  const rd = (a, b) => rv.words[a].bbox[1] - rv.words[b].bbox[1] || rv.words[a].bbox[0] - rv.words[b].bbox[0];
  if (rv.order !== "suspicious") return idx.sort(rd);
  const key = i => [lowConf(rv.words[i]) ? 0 : 1, /\d/.test(rv.words[i].text) ? 0 : 1];
  return idx.sort((a, b) => { const ka = key(a), kb = key(b); return ka[0] - kb[0] || ka[1] - kb[1] || rd(a, b); });
}

function rvSideDraw(rv) {
  const side = $("#rv-side");
  const one = rv.sel.size === 1 ? [...rv.sel][0] : -1, w = one >= 0 ? rv.words[one] : null;
  const order = rvOrder(rv);
  const nLow = rv.words.filter(lowConf).length;
  const stat = rv.pg.state && rv.pg.state.stats;
  side.innerHTML = `
    <div class="panel detail-box">
      ${w ? `<b>고른 단어</b>
        <input type="text" id="rv-txt" value="${esc(w.text)}" style="width:100%;font-size:16px">
        <div class="muted">신뢰도 ${w.edited ? "1 (사람이 고침)" : w.confidence} · 박스 ${w.bbox.map(Math.round).join(", ")}${w.added ? " · 새로 그림" : ""}</div>
        <div class="muted">Enter: 고치고 다음 단어 · 나누기(S)는 글자 칸의 커서 자리에서</div>`
      : rv.sel.size > 1 ? `<b>${rv.sel.size}개 고름</b><div class="muted">합치기(M): 한 박스로, 글자는 왼쪽부터 붙입니다 (띄어 쓸 곳은 고친 뒤 칸에서).</div>`
      : `<div class="muted">박스를 눌러 고릅니다 (Shift: 여럿). 끌어서 옮기고, 모서리로 크기를 바꿉니다. 새 박스(N)는 끌어서 그립니다.</div>`}
    </div>
    <div class="keys-help"><kbd>Tab</kbd> 다음 단어 <kbd>Shift+Tab</kbd> 앞 <kbd>N</kbd> 새 박스 <kbd>M</kbd> 합치기 <kbd>S</kbd> 나누기
      <kbd>Del</kbd> 지우기 <kbd>Ctrl+S</kbd> 저장 <kbd>Ctrl+Enter</kbd> 확인</div>
    ${stat ? `<div class="panel detail-box" style="margin-top:8px">지난 저장: 사내 OCR 글자 오류율 <b>${pct(stat.ocr_cer)}%</b> · 박스 F1 ${pct(stat.box_f1)}
      · 고침 ${stat.changed} · 더함 ${stat.added} · 뺌 ${stat.deleted} <span class="muted">(${esc(rv.pg.state.by)} ${esc(rv.pg.state.at)})</span></div>` : ""}
    <div class="bar" style="margin-top:8px"><b style="margin:0">단어 ${rv.words.length}</b>
      <span class="muted">신뢰도 낮음 ${nLow}</span>
      <select id="rv-ord"><option value="suspicious">의심 먼저 (신뢰도 낮음 → 숫자)</option><option value="reading">읽는 순서</option></select></div>
    <div class="rv-list"><table class="ed-list"><tbody>${order.map(i => {
      const x = rv.words[i];
      return `<tr class="click ${rv.sel.has(i) ? "sel" : ""}" data-row="${i}"><td>${esc(x.text)}</td>
        <td class="num">${x.added ? `<span class="tag st-added">새</span>` : x.edited ? `<span class="tag st-edited">고침</span>` : lowConf(x) ? `<span class="tag warn">${x.confidence}</span>` : x.confidence}</td></tr>`;
    }).join("")}</tbody></table></div>`;
  $("#rv-ord").value = rv.order;
  $("#rv-ord").onchange = () => { rv.order = $("#rv-ord").value; store.set("rv.order", rv.order); rvSideDraw(rv); };
  $$("[data-row]", side).forEach(tr => tr.onclick = e => rvPick(rv, +tr.dataset.row, e.shiftKey, true));
  const t = $("#rv-txt");
  if (t) {
    t.oninput = () => {
      const x = rv.words[one];
      x.text = t.value; x.edited = true; rv.dirty = true;
      const cell = $(`.rv-list tr[data-row="${one}"] td`, side);
      if (cell) cell.textContent = t.value;
      if (rv.showText) rvDraw(rv);
    };
    t.onkeydown = e => {
      if (e.key === "Enter" && !e.ctrlKey) { e.preventDefault(); rvStep(rv, 1); }
      else if (e.key === "Tab") { e.preventDefault(); rvStep(rv, e.shiftKey ? -1 : 1); }
      else if (e.key === "Escape") t.blur();
    };
  }
  const row = $(".rv-list tr.sel", side);
  if (row) scrollRowIntoView($(".rv-list", side), row);
}

function rvPick(rv, i, add = false, scroll = false) {
  if (!add) rv.sel.clear();
  if (i >= 0) { if (add && rv.sel.has(i)) rv.sel.delete(i); else rv.sel.add(i); }
  rvDraw(rv);
  rvSideDraw(rv);
  if (scroll && i >= 0) rvScrollTo(rv, i);
  if (rv.sel.size === 1 && $("#rv-txt")) { $("#rv-txt").focus(); $("#rv-txt").select(); }
}

function rvScrollTo(rv, i) {   // 그림 칸 안에서만 움직여 단어가 보이게
  const wrap = $("#rv-wrap"), svg = $("#rv-stage svg");
  if (!wrap || !svg) return;
  const k = svg.getBoundingClientRect().width / rv.pg.width, [x0, y0] = rv.words[i].bbox;
  const top = y0 * k, left = x0 * k;
  if (top < wrap.scrollTop || top > wrap.scrollTop + wrap.clientHeight - 40) wrap.scrollTop = top - wrap.clientHeight / 3;
  if (left < wrap.scrollLeft || left > wrap.scrollLeft + wrap.clientWidth - 40) wrap.scrollLeft = left - wrap.clientWidth / 3;
}

function rvStep(rv, d) {
  const order = rvOrder(rv);
  const cur = rv.sel.size === 1 ? order.indexOf([...rv.sel][0]) : -1;
  const n = order[(cur + d + order.length) % order.length];
  if (n !== undefined) rvPick(rv, n, false, true);
}

function rvChanged(rv) { rv.dirty = true; rvDraw(rv); rvSideDraw(rv); }

function rvDelete(rv) {
  if (!rv.sel.size) return;
  rv.words = rv.words.filter((_, i) => !rv.sel.has(i));
  rv.sel.clear();
  rvChanged(rv);
}

function rvMerge(rv) {
  if (rv.sel.size < 2) return toast("합칠 단어를 둘 이상 고르세요 (Shift+누르기)", true);
  const ws = [...rv.sel].map(i => rv.words[i]).sort((a, b) => a.bbox[0] - b.bbox[0]);
  const box = [Math.min(...ws.map(w => w.bbox[0])), Math.min(...ws.map(w => w.bbox[1])), Math.max(...ws.map(w => w.bbox[2])), Math.max(...ws.map(w => w.bbox[3]))];
  const merged = { text: ws.map(w => w.text).join(""), bbox: box, confidence: 1, line: ws[0].line, edited: true };
  rv.words = rv.words.filter((_, i) => !rv.sel.has(i));
  rv.words.push(merged);
  rv.sel = new Set([rv.words.length - 1]);
  rvChanged(rv);
}

function rvSplit(rv) {
  if (rv.sel.size !== 1) return toast("나눌 단어 하나를 고르세요", true);
  const i = [...rv.sel][0], w = rv.words[i], t = $("#rv-txt");
  const text = t ? t.value : w.text;
  let k = t ? t.selectionStart : Math.ceil(text.length / 2);
  if (!(k > 0 && k < text.length)) k = Math.ceil(text.length / 2);
  if (text.length < 2) return toast("한 글자는 나눌 수 없습니다", true);
  const [x0, y0, x1, y1] = w.bbox, xm = x0 + (x1 - x0) * k / text.length;
  const a = { ...w, text: text.slice(0, k).trim() || text.slice(0, k), bbox: [x0, y0, xm - 1, y1], edited: true };
  const b = { ...w, text: text.slice(k).trim() || text.slice(k), bbox: [xm + 1, y0, x1, y1], edited: true };
  rv.words.splice(i, 1, a, b);
  rv.sel = new Set([i + 1]);
  rvChanged(rv);
  toast("나눈 자리는 글자 수 비율입니다. 박스를 끌어 맞추세요");
}

function rvKey(rv, e) {
  const inInput = /^(INPUT|SELECT|TEXTAREA)$/.test(document.activeElement && document.activeElement.tagName);
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") { e.preventDefault(); rvSave(rv, false); return; }
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); rvSave(rv, true); return; }
  if (inInput) return;
  const k = e.key.toLowerCase();
  if (e.key === "Tab") { e.preventDefault(); rvStep(rv, e.shiftKey ? -1 : 1); }
  else if (e.key === "Delete" || e.key === "Backspace") { e.preventDefault(); rvDelete(rv); }
  else if (k === "n") { rv.tool = rv.tool === "draw" ? "select" : "draw"; rvDraw(rv); }
  else if (e.key === "Escape") { rv.tool = "select"; rv.sel.clear(); rvDraw(rv); rvSideDraw(rv); }
  else if (k === "m") rvMerge(rv);
  else if (k === "s") rvSplit(rv);
}

function rvBind(rv) {
  $$("[data-tool]").forEach(bt => bt.onclick = () => { rv.tool = bt.dataset.tool; rvDraw(rv); });
  $("#rv-merge").onclick = () => rvMerge(rv);
  $("#rv-split").onclick = () => rvSplit(rv);
  $("#rv-del").onclick = () => rvDelete(rv);
  $("#rv-orig").onchange = () => { rv.showOrig = $("#rv-orig").checked; rvDraw(rv); };
  $("#rv-text").onchange = () => { rv.showText = $("#rv-text").checked; store.set("rv.text", rv.showText); rvDraw(rv); };
  $("#rv-zoom").onchange = () => { rv.zoom = $("#rv-zoom").value; store.set("rv.zoom", rv.zoom); rvDraw(rv); };
  $("#rv-save").onclick = () => rvSave(rv, false);
  $("#rv-done").onclick = () => rvSave(rv, true);
  const stage = $("#rv-stage");
  const pt = e => {
    const r = stage.querySelector("svg").getBoundingClientRect();
    return { x: (e.clientX - r.left) * rv.pg.width / r.width, y: (e.clientY - r.top) * rv.pg.height / r.height, k: rv.pg.width / r.width };
  };
  const hit = p => {   // 포함하는 가장 작은 박스, 없으면 가까운 박스
    let best = -1, bs = null;
    rv.words.forEach((w, i) => {
      const [x0, y0, x1, y1] = w.bbox, d = Math.hypot(Math.max(x0 - p.x, 0, p.x - x1), Math.max(y0 - p.y, 0, p.y - y1));
      if (d > 5 * p.k) return;
      const s = [d > 0 ? 1 : 0, d > 0 ? d : (x1 - x0) * (y1 - y0)];
      if (!bs || s[0] < bs[0] || (s[0] === bs[0] && s[1] < bs[1])) { best = i; bs = s; }
    });
    return best;
  };
  let drag = null;
  if (window._rvMove) { window.removeEventListener("mousemove", window._rvMove); window.removeEventListener("mouseup", window._rvUp); }
  stage.onmousedown = e => {
    if (e.button !== 0) return;
    e.preventDefault();
    const p = pt(e);
    if (rv.tool === "draw") { drag = { mode: "draw", x0: p.x, y0: p.y }; rv.ghost = [p.x, p.y, p.x, p.y]; return; }
    const h = e.target.dataset && e.target.dataset.handle;
    if (h && rv.sel.size === 1) { drag = { mode: "resize", corner: h, last: p, i: [...rv.sel][0] }; return; }
    const i = hit(p);
    if (i < 0) { if (!e.shiftKey) rvPick(rv, -1); return; }
    if (e.shiftKey) { rvPick(rv, i, true); return; }
    if (!rv.sel.has(i) || rv.sel.size > 1) rvPick(rv, i, false, false);
    drag = { mode: "move", last: p, x0: p.x, y0: p.y, i, moved: false };
  };
  window._rvMove = e => {
    if (!drag || !$("#rv-stage")) return;
    const p = pt(e);
    if (drag.mode === "draw") { rv.ghost = [drag.x0, drag.y0, p.x, p.y]; rvDraw(rv); return; }
    const w = rv.words[drag.i];
    if (!w) return;
    const dx = p.x - drag.last.x, dy = p.y - drag.last.y;
    if (drag.mode === "move" && !drag.moved && Math.abs(p.x - drag.x0) + Math.abs(p.y - drag.y0) < 2 * p.k) return;
    drag.moved = true;
    drag.last = p;
    const b = w.bbox;
    if (drag.mode === "move") w.bbox = [b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy];
    else {
      const n = [...b];
      if (drag.corner.includes("w")) n[0] = Math.min(b[2] - 1, b[0] + dx); else n[2] = Math.max(b[0] + 1, b[2] + dx);
      if (drag.corner.includes("n")) n[1] = Math.min(b[3] - 1, b[1] + dy); else n[3] = Math.max(b[1] + 1, b[3] + dy);
      w.bbox = n;
    }
    w.edited = true;
    rv.dirty = true;
    rvDraw(rv);
  };
  window._rvUp = () => {
    if (!drag || !$("#rv-stage")) { drag = null; return; }
    if (drag.mode === "draw" && rv.ghost) {
      const [a, b, c, d] = rv.ghost;
      const box = [Math.min(a, c), Math.min(b, d), Math.max(a, c), Math.max(b, d)].map(r1);
      rv.ghost = null;
      if (box[2] - box[0] >= 3 && box[3] - box[1] >= 3) {
        const near = rv.words.reduce((best, w) => { const dy = Math.abs((w.bbox[1] + w.bbox[3]) / 2 - (box[1] + box[3]) / 2); return !best || dy < best.dy ? { w, dy } : best; }, null);
        rv.words.push({ text: "", bbox: box, confidence: 1, line: near ? near.w.line : 0, edited: true, added: true });
        rv.tool = "select";
        rv.dirty = true;
        rvPick(rv, rv.words.length - 1);
      } else rvDraw(rv);
    } else if (drag.moved) rvSideDraw(rv);
    drag = null;
  };
  window.addEventListener("mousemove", window._rvMove);
  window.addEventListener("mouseup", window._rvUp);
  stage.onmousemove = e => {
    if (drag) return;
    const tip = stage.querySelector(".tip"), i = hit(pt(e));
    if (i < 0) { tip.style.display = "none"; return; }
    const w = rv.words[i], sr = stage.getBoundingClientRect();
    tip.textContent = `${w.text || "(빈 글자)"} · ${w.edited ? "고침" : w.confidence}`;
    tip.style.display = "block";
    tip.style.left = `${Math.min(e.clientX - sr.left + 14, stage.clientWidth - tip.offsetWidth - 4)}px`;
    tip.style.top = `${e.clientY - sr.top + 16}px`;
  };
  stage.onmouseleave = () => { const t = stage.querySelector(".tip"); if (t) t.style.display = "none"; };
}

async function rvSave(rv, done) {
  const empty = rv.words.filter(w => !w.text.trim()).length;
  if (empty && !confirm(`글자가 빈 박스 ${empty}개는 저장하지 않습니다. 계속할까요?`)) return;
  try {
    const st = await api(`/api/imports/${q(rv.name)}/ocr?p=${q(rv.pid)}`, { words: rv.words, done }, "PUT");
    rv.dirty = false;
    toast(`${done ? "확인했습니다" : "저장했습니다"} · 사내 OCR 글자 오류율 ${pct(st.stats.ocr_cer)}% · 박스 F1 ${pct(st.stats.box_f1)}`);
    if (done) location.hash = rv.next ? `#/review/${q(rv.name)}/${q(rv.next)}` : `#/review/${q(rv.name)}`;
    else viewOcrPage(rv.name, rv.pid);
  } catch (e) { toast(e.message, true); }
}
