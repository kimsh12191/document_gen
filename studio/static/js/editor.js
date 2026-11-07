// ① 서식 › 영역 편집 (overlay): 값 영역 그리기·옮기기·크기 바꾸기·빼기, 키·값 종류·값 출처, 배경 지우기, 수정 전후 비교.
// 고친 것은 서식 폴더의 사람 수정 파일(docgen/forms/<ID>/regions.json, 실서류에서 만든 서식은 private_forms_dir/<ID>/regions.json)에 저장한다.
// 좌표는 레이아웃과 같은 PDF pt. 서버: studio/app.py (/api/forms/{id}/layout·overrides·bg·checks), studio/editor.py
"use strict";

const ED_TOOLS = [
  ["select", "선택·옮기기", "V"], ["text", "글자 칸 그리기", "T"], ["table", "표 그리기", "B"], ["check", "체크 보기 그리기", "C"],
  ["sign", "서명·도장 자리", "S"], ["staff", "결재란 칸", "R"], ["erase", "지우기: 흰색", "E"], ["erase_auto", "지우기: 주변색", "A"],
];
const ED_STATUS = { auto: "자동", edited: "수정", added: "추가", dropped: "뺌" };
const ED_T = { text: "글자", check: "체크", date: "날짜", sign: "서명·도장", copy: "자필", staff: "결재란" };
let edKeys = null, edSources = null;

async function viewEditor(d, keep = null) {
  $("#tab").innerHTML = `<p class="spin">레이아웃을 읽는 중…</p>`;
  const [view] = await Promise.all([
    api(`/api/forms/${encodeURIComponent(d.id)}/layout`),
    edKeys ? null : Promise.all([api("/api/keys"), api("/api/dictionary/keys?scope=common").catch(() => ({ rows: [] }))])
      .then(([k, c]) => { edKeys = { ...k, common: c.rows }; }),   // 키 고르기: 공통 키(키 사전) 먼저
    edSources ? null : api("/api/sources").then(s => { edSources = s; }),
    kpLoad().catch(() => null),   // 공통 키 이름 (키 칸 표시)
  ]);
  const ed = {
    d, view, page: 0, tool: "select", sel: null, zoom: store.get("ed.zoom", 1), onlyBg: false, dirty: false, compare: null,
    ov: normOv(clone(view.overrides || {})), items: [],
  };
  ed.items = view.items.map(it => ({ ...it, base: it.status === "added" ? null : baseOf(it) }));
  for (const it of ed.items) {
    if (it.status === "added") it.ref = ed.ov.add[+it.id.split(":")[1]];
  }
  if (keep) { ed.page = keep.page; ed.tool = keep.tool; if (keep.sel && edFind(ed, keep.sel.id)) ed.sel = keep.sel; }
  // 검수 탭에서 "영역 편집에서 보기"를 눌러 왔으면 그 영역을 고른다
  if (state.editorFocus && state.editorFocus.doc === d.id) {
    const it = ed.items.find(x => x.id === state.editorFocus.id);
    if (it) { ed.sel = { id: it.id, sub: subsOf(ed, it)[0]?.name }; ed.page = it.page; }
  }
  state.editorFocus = null;
  state.leave = unload => !ed.dirty || (unload ? false : confirm("저장하지 않은 수정이 있습니다. 버리고 나갈까요?"));
  edLayout(ed);
}

function normOv(ov) {
  ov.items = ov.items || []; ov.add = ov.add || []; ov.erase = ov.erase || [];
  return ov;
}

// 서버가 준 영역은 수정이 덧씌워진 값이다. 원래 값(base)은 서버가 따로 준다.
function baseOf(it) { return it.base_raw ? clone(it.base_raw) : clone(it); }

const edEntry = (ed, it, create) => {
  let e = ed.ov.items.find(x => x.match.page === it.match.page && x.match.t === it.match.t &&
    (x.match.label || "") === (it.match.label || "") && (x.match.n || 0) === (it.match.n || 0));
  if (!e && create) { e = { match: clone(it.match) }; ed.ov.items.push(e); }
  return e;
};

// 지금 보이는 값 (자동 + 수정, 또는 추가 항목 그 자체)
function cur(ed, it) {
  if (it.status === "added") return it.ref;
  const e = edEntry(ed, it, false) || {};
  const out = { ...it.base, ...(e.set || {}) };
  for (const k of ["key", "kind", "source", "choices", "text", "note", "group"]) if (e[k] !== undefined && e[k] !== "") out[k] = e[k];
  return out;
}

function statusOf(ed, it) {
  if (it.status === "added") return "added";
  const e = edEntry(ed, it, false);
  return !e ? (it.was || "auto") : e.drop ? "dropped" : "edited";   // was: 칸 목록에 이미 합친 사람 수정
}

function tidyEntry(ed, it) {
  const e = edEntry(ed, it, false);
  if (!e) return;
  if (e.set && !Object.keys(e.set).length) delete e.set;
  for (const k of Object.keys(e)) if (k !== "match" && (e[k] === "" || e[k] === null || e[k] === undefined)) delete e[k];
  if (Object.keys(e).length === 1) ed.ov.items.splice(ed.ov.items.indexOf(e), 1);
}

function setGeom(ed, it, patch) {
  if (it.status === "added") Object.assign(it.ref, patch);
  else { const e = edEntry(ed, it, true); e.set = { ...(e.set || {}), ...patch }; tidyEntry(ed, it); }
  ed.dirty = true;
}

function setProp(ed, it, k, v) {
  const empty = v === "" || v === null || v === undefined || (Array.isArray(v) && !v.length);
  if (it.status === "added") { if (empty) delete it.ref[k]; else it.ref[k] = v; }
  else if (k === "label") { setGeom(ed, it, { label: v }); return; }
  else { const e = edEntry(ed, it, true); if (empty) delete e[k]; else e[k] = v; tidyEntry(ed, it); }
  ed.dirty = true;
}

// 영역 하나의 사각형들 [{name, box}] — 고르고 옮기고 크기를 바꾸는 단위
function subsOf(ed, it) {
  if (it.kind === "erase") return [{ name: "rect", box: it.ref.rect }];
  const c = cur(ed, it), out = [];
  if (c.t === "check") (c.options || []).forEach((o, j) => out.push({ name: `opt:${j}`, box: o.rect || o.box, small: o.box }));
  else if (c.t === "date" && c.parts) for (const p of ["y", "m", "d"]) { if (c.parts[p]) out.push({ name: `part:${p}`, box: c.parts[p] }); }
  else if (c.t === "sign") { if (c.mark) out.push({ name: "mark", box: c.mark }); if (c.name) out.push({ name: "name", box: c.name }); }
  else if (c.rect) out.push({ name: "rect", box: c.rect });
  return out;
}

function moveSub(ed, it, sub, fn) {   // fn(box) → 새 box
  if (it.kind === "erase") { it.ref.rect = fn(it.ref.rect).map(r1); ed.dirty = true; return; }
  const c = cur(ed, it);
  if (sub.startsWith("opt:")) {
    const j = +sub.split(":")[1], opts = clone(c.options);
    const o = opts[j], before = o.rect || o.box, after = fn(before).map(r1);
    const dx = after[0] - before[0], dy = after[1] - before[1];
    const moved = (after[2] - after[0]) === (before[2] - before[0]) && (after[3] - after[1]) === (before[3] - before[1]);
    if (moved) o.box = o.box.map((v, i) => r1(v + (i % 2 ? dy : dx)));
    o.rect = after;
    setGeom(ed, it, { options: opts });
  } else if (sub.startsWith("part:")) {
    const p = sub.split(":")[1], parts = clone(c.parts);
    parts[p] = fn(parts[p]).map(r1);
    setGeom(ed, it, { parts });
  } else {
    setGeom(ed, it, { [sub]: fn(c[sub]).map(r1) });
  }
}

function moveWhole(ed, it, dx, dy) {
  const sh = b => [b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy];
  for (const s of subsOf(ed, it)) moveSub(ed, it, s.name, sh);
}

function edPageItems(ed) {
  const list = ed.items.filter(it => it.page === ed.page);
  const erases = ed.ov.erase.map((e, k) => ({ id: `erase:${k}`, kind: "erase", page: e.page, ref: e })).filter(x => x.page === ed.page);
  return [...list, ...erases];
}

function edFind(ed, id) {
  if (id && id.startsWith("erase:")) { const k = +id.split(":")[1]; const e = ed.ov.erase[k]; return e ? { id, kind: "erase", page: e.page, ref: e } : null; }
  return ed.items.find(x => x.id === id) || null;
}

// ---------------------------------------------------------------------------
function edLayout(ed) {
  const v = ed.view;
  $("#tab").innerHTML = `
    <div class="bar ed-bar">
      <span class="pages" id="ed-pages"></span>
      ${ED_TOOLS.map(([k, n, key]) => `<button data-tool="${k}" title="${n} (${key})">${n}</button>`).join("")}
      <span class="sep"></span>
      <label>배율 <select id="ed-zoom">${[0.6, 0.8, 1, 1.25, 1.5, 2].map(z => `<option value="${z}" ${z === ed.zoom ? "selected" : ""}>${Math.round(z * 100)}%</option>`).join("")}</select></label>
      <label><input type="checkbox" id="ed-onlybg"> 지운 배경만 보기</label>
      <span class="sep"></span>
      <button class="primary" id="ed-save">저장</button><button id="ed-reload">저장된 것으로 되돌리기</button>
      <span id="ed-dirty" class="muted"></span>
    </div>
    ${v.broken.length ? `<div class="panel warnbox">깨진 수정 ${v.broken.length}개: 레이아웃을 다시 추출해 대상 영역을 못 찾았습니다.
      ${v.broken.map(o => `<span class="tag warn">${esc(o.match.page + 1)}쪽 ${esc(ED_T[o.match.t] || o.match.t)} '${esc(o.match.label)}'</span>`).join("")}
      <button id="ed-drop-broken">깨진 수정 지우기</button></div>` : ""}
    <div class="keys-help" style="margin-bottom:6px">칸을 눌러 고르고 끌어서 옮깁니다. 모서리를 끌면 크기, <kbd>Shift</kbd>+끌기는 영역 전체 이동,
      <kbd>←↑→↓</kbd> 0.5pt (<kbd>Shift</kbd> 5pt), <kbd>Delete</kbd> 빼기, <kbd>Esc</kbd> 해제. 그리기 도구는 끌어서 새 칸을 만듭니다.</div>
    <div class="viewer ed-viewer">
      <div><div class="ed-stage" id="ed-stage"></div></div>
      <div class="side panel" id="ed-side"></div>
    </div>
    <h2>수정 전후 비교</h2>
    <div class="bar">${optionBar(true, "cmp")}<button id="ed-cmp">저장본 ↔ 지금 고친 것 렌더링</button><span class="muted" id="ed-cmp-stat"></span></div>
    <div id="ed-cmp-out"></div>`;
  $$(".ed-bar [data-tool]").forEach(b => b.onclick = () => { ed.tool = b.dataset.tool; edDraw(ed); });
  $("#ed-zoom").onchange = e => { ed.zoom = +e.target.value; store.set("ed.zoom", ed.zoom); edDraw(ed); };
  $("#ed-onlybg").onchange = e => { ed.onlyBg = e.target.checked; edDraw(ed); };
  $("#ed-save").onclick = () => edSave(ed);
  $("#ed-reload").onclick = () => { if (!ed.dirty || confirm("고친 것을 버리고 저장본으로 되돌릴까요?")) { ed.dirty = false; viewEditor(ed.d); } };
  if ($("#ed-drop-broken")) $("#ed-drop-broken").onclick = () => {
    const found = new Set(ed.items.filter(x => x.match).map(x => `${x.match.page}|${x.match.t}|${x.match.label}|${x.match.n}`));
    ed.ov.items = ed.ov.items.filter(o => found.has(`${o.match.page}|${o.match.t}|${o.match.label || ""}|${o.match.n || 0}`));
    ed.dirty = true; edSave(ed);
  };
  $("#ed-cmp").onclick = () => edCompare(ed);
  edBindStage(ed);
  state.keyHandler = e => edKey(ed, e);
  edDraw(ed);
}

function edDraw(ed) {
  const v = ed.view, pg = v.pages[ed.page];
  $("#ed-pages").innerHTML = v.pages.length > 1 ? v.pages.map((_, i) =>
    `<button data-p="${i}" class="${i === ed.page ? "primary" : ""}">${i + 1}쪽</button>`).join("") : "";
  $("#ed-pages").onclick = e => { const p = e.target.dataset.p; if (p !== undefined) { ed.page = +p; ed.sel = null; edDraw(ed); } };
  $$(".ed-bar [data-tool]").forEach(b => b.classList.toggle("primary", b.dataset.tool === ed.tool));
  $("#ed-dirty").innerHTML = ed.dirty ? `<b class="kr">저장 안 됨</b>` : "저장됨";
  const W = Math.round(pg.w * 1.6 * ed.zoom);   // 화면 폭 (pt × 1.6 × 배율)
  const rects = [];
  for (const it of edPageItems(ed)) {
    const st = it.kind === "erase" ? "erase" : statusOf(ed, it);
    if (ed.onlyBg && st !== "erase") continue;
    const t = it.kind === "erase" ? (it.ref.fill === "auto" ? "erase-auto" : "erase-white") : cur(ed, it).t;
    for (const s of subsOf(ed, it)) {
      const [x0, y0, x1, y1] = s.box;
      const sel = ed.sel && ed.sel.id === it.id;
      rects.push(`<rect data-id="${esc(it.id)}" data-sub="${s.name}" class="ed st-${st} t-${t} ${sel ? "sel" : ""} ${sel && ed.sel.sub === s.name ? "subsel" : ""}"
        x="${x0}" y="${y0}" width="${Math.max(0.5, x1 - x0)}" height="${Math.max(0.5, y1 - y0)}"></rect>`);
      if (s.small) {
        const [a, b, c, dd] = s.small;
        rects.push(`<rect class="ed-box" x="${a}" y="${b}" width="${Math.max(0.5, c - a)}" height="${Math.max(0.5, dd - b)}"></rect>`);
      }
      if (sel && ed.sel.sub === s.name) {
        const hs = 3.2 / ed.zoom;
        for (const [hx, hy, corner] of [[x0, y0, "nw"], [x1, y0, "ne"], [x0, y1, "sw"], [x1, y1, "se"]])
          rects.push(`<rect class="handle" data-handle="${corner}" x="${hx - hs}" y="${hy - hs}" width="${hs * 2}" height="${hs * 2}"></rect>`);
      }
    }
  }
  if (ed.tableDraft && ed.tableDraft.page === ed.page) {   // 표 초안: 바깥 + 열·행 나눔 미리보기
    const t = ed.tableDraft, [x0, y0, x1, y1] = t.rect;
    const nc = Math.max(1, edTableCols(t.cols).length), nr = Math.max(1, +t.rows || 1);
    rects.push(`<rect class="ghost" x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}"></rect>`);
    for (let c = 1; c < nc; c++) { const x = x0 + (x1 - x0) * c / nc; rects.push(`<rect class="ghost" x="${x}" y="${y0}" width="0.3" height="${y1 - y0}"></rect>`); }
    for (let r = 1; r < nr; r++) { const y = y0 + (y1 - y0) * r / nr; rects.push(`<rect class="ghost" x="${x0}" y="${y}" width="${x1 - x0}" height="0.3"></rect>`); }
  }
  if (ed.ghost) {
    const [x0, y0, x1, y1] = ed.ghost;
    rects.push(`<rect class="ghost" x="${Math.min(x0, x1)}" y="${Math.min(y0, y1)}" width="${Math.abs(x1 - x0)}" height="${Math.abs(y1 - y0)}"></rect>`);
  }
  const stage = $("#ed-stage");
  stage.style.width = `${W}px`;
  stage.className = `ed-stage tool-${ed.tool}${ed.onlyBg ? " onlybg" : ""}`;
  const src = `/api/forms/${encodeURIComponent(ed.d.id)}/bg/${ed.page}`;
  if (!stage.querySelector("img") || stage.querySelector("img").getAttribute("src") !== src) {
    stage.innerHTML = `<img src="${src}" alt="" draggable="false"><svg></svg><div class="tip"></div>`;
  }
  const svg = stage.querySelector("svg");
  svg.setAttribute("viewBox", `0 0 ${pg.w} ${pg.h}`);
  svg.setAttribute("preserveAspectRatio", "none");
  svg.innerHTML = rects.join("");
  if (!ed.keepSide) edSide(ed);
}

function edBindStage(ed) {
  const stage = $("#ed-stage");
  const pt = e => {
    const r = stage.querySelector("svg").getBoundingClientRect(), pg = ed.view.pages[ed.page];
    return { x: (e.clientX - r.left) * pg.w / r.width, y: (e.clientY - r.top) * pg.h / r.height, k: pg.w / r.width };
  };
  const hit = p => {   // 누른 자리: 손잡이 > 포함하는 가장 작은 칸 > 가까운 칸
    let best = null;
    for (const it of edPageItems(ed)) {
      if (ed.onlyBg && it.kind !== "erase") continue;
      for (const s of subsOf(ed, it)) {
        const [x0, y0, x1, y1] = s.box;
        const dist = Math.hypot(Math.max(x0 - p.x, 0, p.x - x1), Math.max(y0 - p.y, 0, p.y - y1));
        if (dist > 6 * p.k) continue;
        const score = [dist > 0 ? 1 : 0, dist > 0 ? dist : (x1 - x0) * (y1 - y0)];
        if (!best || score[0] < best.score[0] || (score[0] === best.score[0] && score[1] < best.score[1])) best = { it, sub: s.name, score };
      }
    }
    return best;
  };
  let drag = null;
  if (window._edMove) { window.removeEventListener("mousemove", window._edMove); window.removeEventListener("mouseup", window._edUp); }
  stage.onmousedown = e => {
    if (e.button !== 0) return;
    e.preventDefault();
    const p = pt(e);
    if (ed.tool !== "select") { drag = { mode: "draw", x0: p.x, y0: p.y }; ed.ghost = [p.x, p.y, p.x, p.y]; return; }
    const h = e.target.dataset && e.target.dataset.handle;
    if (h && ed.sel) { drag = { mode: "resize", corner: h, x0: p.x, y0: p.y, last: p }; return; }
    const b = hit(p);
    if (!b) { ed.sel = null; edDraw(ed); return; }
    ed.sel = { id: b.it.id, sub: b.sub };
    drag = { mode: e.shiftKey ? "whole" : "move", x0: p.x, y0: p.y, last: p, moved: false };
    edDraw(ed);
  };
  window._edMove = e => {
    if (!drag || !$("#ed-stage")) return;
    const p = pt(e);
    if (drag.mode === "draw") { ed.ghost = [drag.x0, drag.y0, p.x, p.y]; edDraw(ed); return; }
    const it = edFind(ed, ed.sel && ed.sel.id);
    if (!it) return;
    const dx = p.x - drag.last.x, dy = p.y - drag.last.y;
    if (Math.abs(p.x - drag.x0) + Math.abs(p.y - drag.y0) < 1.5 * p.k && !drag.moved) return;
    drag.moved = true;
    drag.last = p;
    if (it.kind !== "erase" && statusOf(ed, it) === "dropped") return;
    if (drag.mode === "whole") moveWhole(ed, it, dx, dy);
    else if (drag.mode === "move") moveSub(ed, it, ed.sel.sub, b => [b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy]);
    else if (drag.mode === "resize") moveSub(ed, it, ed.sel.sub, b => {
      const n = [...b];
      if (drag.corner.includes("w")) n[0] = Math.min(b[2] - 1, b[0] + dx); else n[2] = Math.max(b[0] + 1, b[2] + dx);
      if (drag.corner.includes("n")) n[1] = Math.min(b[3] - 1, b[1] + dy); else n[3] = Math.max(b[1] + 1, b[3] + dy);
      return n;
    });
    edDraw(ed);
  };
  window._edUp = () => {
    if (!drag || !$("#ed-stage")) { drag = null; return; }
    if (drag.mode === "draw" && ed.ghost) {
      const [a, b, c, d] = ed.ghost;
      const box = [Math.min(a, c), Math.min(b, d), Math.max(a, c), Math.max(b, d)].map(r1);
      ed.ghost = null;
      if (box[2] - box[0] >= 2 && box[3] - box[1] >= 2) edCreate(ed, box);
      else edDraw(ed);
    }
    drag = null;
  };
  window.addEventListener("mousemove", window._edMove);
  window.addEventListener("mouseup", window._edUp);
  stage.onmousemove = e => {   // 말풍선
    if (drag) return;
    const tip = stage.querySelector(".tip"), b = hit(pt(e));
    if (!tip) return;
    if (!b) { tip.style.display = "none"; return; }
    const c = b.it.kind === "erase" ? { label: b.it.ref.fill === "auto" ? "지우기(주변색)" : "지우기(흰색)" } : cur(ed, b.it);
    tip.textContent = b.it.kind === "erase" ? c.label : `${ED_T[c.t] || c.t} · ${c.label || "(이름표 없음)"}${c.key ? ` → ${c.key}` : ""}`;
    const sr = stage.getBoundingClientRect();
    tip.style.display = "block";
    tip.style.left = `${Math.min(e.clientX - sr.left + 14, stage.clientWidth - tip.offsetWidth - 4)}px`;
    tip.style.top = `${e.clientY - sr.top + 16}px`;
  };
  stage.onmouseleave = () => { const t = stage.querySelector(".tip"); if (t) t.style.display = "none"; };
}

function edCreate(ed, box) {
  const page = ed.page;
  if (ed.tool === "table") {   // 표: 끈 영역을 열 × 행 칸으로 나눌 초안 (오른쪽에서 열 이름·행 수를 정하고 만든다)
    const t = ed.tableDraft || {};
    ed.tableDraft = { page, rect: box, cols: t.cols || "", rows: t.rows || 5, group: t.group || "" };
    ed.sel = null; ed.tool = "select";
    edDraw(ed);
    setTimeout(() => $("#ed-tb-cols")?.focus(), 0);
    return;
  }
  if (ed.tool === "erase" || ed.tool === "erase_auto") {
    ed.ov.erase.push({ page, rect: box, fill: ed.tool === "erase_auto" ? "auto" : "white" });
    ed.sel = { id: `erase:${ed.ov.erase.length - 1}`, sub: "rect" };
    ed.dirty = true; edDraw(ed); return;
  }
  // 체크 도구: 추가한 체크 영역을 고른 상태면 그 영역에 보기를 하나 더한다
  if (ed.tool === "check" && ed.sel) {
    const it = edFind(ed, ed.sel.id);
    if (it && it.status === "added" && it.ref.t === "check" && it.page === page) {
      const h = Math.min(box[3] - box[1], 10);
      it.ref.options.push({ text: `보기${it.ref.options.length + 1}`, box: [box[0], box[1], r1(box[0] + h), r1(box[1] + h)], rect: box });
      ed.sel = { id: it.id, sub: `opt:${it.ref.options.length - 1}` };
      ed.dirty = true; edDraw(ed); return;
    }
  }
  const a = { t: ed.tool, page, label: "" };
  if (ed.tool === "check") {
    const h = Math.min(box[3] - box[1], 10);
    a.options = [{ text: "보기1", box: [box[0], box[1], r1(box[0] + h), r1(box[1] + h)], rect: box }];
  } else if (ed.tool === "sign") a.mark = box;
  else { a.rect = box; if (ed.tool === "staff") a.label = "결재"; }
  ed.ov.add.push(a);
  const it = { id: `add:${ed.ov.add.length - 1}:${Date.now()}`, status: "added", page, ref: a, auto: { key: null, kind: null } };
  ed.items.push(it);
  ed.sel = { id: it.id, sub: subsOf(ed, it)[0].name };
  ed.tool = ed.tool === "check" ? "check" : "select";
  ed.dirty = true; edDraw(ed);
  setTimeout(() => $("#ed-label")?.focus(), 0);
}

function edDelete(ed) {
  const it = ed.sel && edFind(ed, ed.sel.id);
  if (!it) return;
  if (it.kind === "erase") ed.ov.erase.splice(ed.ov.erase.indexOf(it.ref), 1);
  else if (it.status === "added") {
    if (it.ref.t === "check" && ed.sel.sub && ed.sel.sub.startsWith("opt:") && it.ref.options.length > 1) {
      it.ref.options.splice(+ed.sel.sub.split(":")[1], 1);
      ed.sel.sub = "opt:0"; ed.dirty = true; edDraw(ed); return;
    }
    ed.ov.add.splice(ed.ov.add.indexOf(it.ref), 1);
    ed.items.splice(ed.items.indexOf(it), 1);
  } else {
    const e = edEntry(ed, it, true);
    e.drop = true;
  }
  ed.sel = null; ed.dirty = true; edDraw(ed);
}

function edKey(ed, e) {
  if (e.target.closest("input, select, textarea")) return;
  const tool = ED_TOOLS.find(t => t[2] === e.key.toUpperCase());
  if (tool && !e.ctrlKey && !e.metaKey) { ed.tool = tool[0]; edDraw(ed); return; }
  if (e.key === "Escape") { ed.sel = null; ed.tool = "select"; ed.tableDraft = null; edDraw(ed); return; }
  if ((e.key === "Delete" || e.key === "Backspace") && ed.sel) { e.preventDefault(); edDelete(ed); return; }
  if (e.key === "s" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); edSave(ed); return; }
  const dir = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] }[e.key];
  if (dir && ed.sel) {
    e.preventDefault();
    const it = edFind(ed, ed.sel.id), s = e.shiftKey ? 5 : 0.5;
    if (!it) return;
    moveSub(ed, it, ed.sel.sub, b => [b[0] + dir[0] * s, b[1] + dir[1] * s, b[2] + dir[0] * s, b[3] + dir[1] * s]);
    edDraw(ed);
  }
}

// ---------------------------------------------------------------------------
// 오른쪽: 고른 영역의 정보와 이 쪽의 영역 목록
// ---------------------------------------------------------------------------
function keyCandidates(label) {
  if (!edKeys || !label) return [];
  const n = label.replace(/[\s()·:*]/g, "");
  return edKeys.keys.filter(k => k.labels.some(l => l.replace(/[\s()·:*]/g, "") === n)).sort((a, b) => b.forms - a.forms).slice(0, 8);
}

// 생성 방법 (값 출처 source) 고르기: 이름은 사람이 읽는 말, 값은 fields.json 의 source 그대로 (docgen/sources.py)
const ED_SPECIAL = { choice: "보기 중 하나 (아래에 보기 목록)", fixed: "늘 같은 글자 (아래에 글자)", free_text: "짧은 자유 문장 (가끔 빈 칸)",
  empty: "늘 빈 칸", date_seq: "행마다 늘어나는 날짜 (표의 날짜 열)" };
function sourceOptions(curSrc, autoText = "") {
  const sel = v => v === curSrc ? "selected" : "";
  const o = [`<option value="" ${sel("")}>자동 — 항목명으로 정함${autoText ? ` (${esc(autoText)})` : ""}</option>`];
  const names = edSources?.rule_names || {};
  const rules = (edSources?.rules || []).map(r => `<option value="rule:${r}" ${sel(`rule:${r}`)}>${esc(names[r] || r)}</option>`);
  const sp = (edSources?.special || []).map(r => `<option value="rule:${r}" ${sel(`rule:${r}`)}>${esc(ED_SPECIAL[r] || r)}</option>`);
  const prof = (edSources?.profile || []).map(s => `<option value="${esc(s.source)}" ${sel(s.source)}>${esc(s.source.replace(/^profile\./, ""))}${s.example ? ` — 예: ${esc(String(s.example).slice(0, 24))}` : ""}</option>`);
  return o.join("") + `<optgroup label="종류에 맞는 그럴듯한 값 (문서마다 새로)">${rules.join("")}</optgroup>`
    + `<optgroup label="특별">${sp.join("")}</optgroup>`
    + `<optgroup label="고객 정보 (같은 고객의 다른 서류와 같은 값)">${prof.join("")}</optgroup>`;
}

function edSide(ed) {
  const it = ed.sel && edFind(ed, ed.sel.id);
  let html = "";
  if (it && it.kind === "erase") {
    html = `<div class="detail-box panel"><b>배경 지우기</b> · ${it.ref.page + 1}쪽
      <div class="bar"><label><input type="radio" name="ef" value="white" ${it.ref.fill !== "auto" ? "checked" : ""}> 흰색</label>
      <label><input type="radio" name="ef" value="auto" ${it.ref.fill === "auto" ? "checked" : ""}> 주변색</label></div>
      <div class="mono">${it.ref.rect.join(", ")}</div>
      <div class="bar"><button id="ed-del">지우기 영역 빼기</button><button id="ed-to-text">이 자리를 값 영역으로</button></div>
      <div class="muted" style="font-size:12px">값을 지운 자리는 대개 값이 들어갈 자리입니다. "값 영역으로"를 누르면 같은 자리에 글자 칸을 만듭니다.</div></div>`;
  } else if (it) {
    const c = cur(ed, it), st = statusOf(ed, it), cands = keyCandidates(c.label);
    const auto = it.auto || {}, added = it.status === "added" || ed.view.origin === "drawn";   // 그려서 만든 서식은 저장한 칸도 그린 칸처럼
    html = `<div class="detail-box panel">
      <div><b>${esc(ED_T[c.t] || c.t)}</b> <span class="tag st-${st}">${ED_STATUS[st]}</span> <span class="muted mono" style="font-size:11px">${esc(it.id)}</span></div>
      ${st === "dropped" ? `<p class="muted">이 영역은 뺐습니다. 생성기가 값을 쓰지 않습니다.</p><button id="ed-undrop">되살리기</button>` : `
      ${c.t === "staff" ? `<div class="fld muted">결재란은 은행·직원 칸입니다 (문서별 키).</div>` : `
      <div class="fld">${it.cell && !ed.dirty ? `<div>키 ${kpKeyCell(it.cell)}</div><div id="ed-kp"></div>`
        : `<div class="muted">${it.cell ? "저장하면" : "저장한 뒤"} 이 칸의 키(누구의 · 무엇)를 정합니다.</div>`}</div>`}
      ${added ? `<label class="fld"><b>항목명</b> <span class="muted" style="font-size:12px">그림에 인쇄된 이름 그대로 — 질문(무엇을 읽을지)과 자동 키에 쓰입니다</span>
        <input type="text" id="ed-label" value="${esc(c.label || "")}" placeholder="예: 성명, 지급총액"></label>`
        : `<div class="muted" style="font-size:12px">서식에 인쇄된 글자: ${esc(c.label || "(없음)")}</div>`}
      <details class="fld"><summary class="muted">${added ? "자세히 — 키를 직접 적기" : "자세히 — 인쇄된 글자를 잘못 읽었을 때만 고칩니다"}</summary>
      ${added ? "" : `<label class="fld">인쇄된 글자 <input type="text" id="ed-label" value="${esc(c.label || "")}"></label>`}
      ${c.t === "staff" ? "</details>" : `
      <label class="fld">서식의 키 <input type="text" id="ed-key" list="ed-keylist" value="${esc(c.key || "")}" placeholder="${esc(auto.key || "(자동: 인쇄된 글자로)")}"></label>
      <datalist id="ed-keylist">${(edKeys?.common || []).map(k => `<option value="${esc(k.key)}">공통 키 · ${esc(k.name)}</option>`).join("")}${(edKeys?.keys || []).filter(k => !(edKeys?.common || []).some(c => c.key === k.key)).slice(0, 4000).map(k => `<option value="${esc(k.key)}">${esc(k.labels[0] || "")}</option>`).join("")}</datalist>
      ${cands.length ? `<div class="cands">사전 후보: ${cands.map(k => `<a href="#" data-key="${esc(k.key)}" class="mono">${esc(k.key)}</a> <span class="muted">(${k.forms})</span>`).join(" · ")}</div>` : ""}
      ${auto.key ? `<div class="muted" style="font-size:12px">자동 키: <span class="mono">${esc(auto.key)}</span></div>` : ""}</details>
      ${c.t === "text" ? `<div class="fld" style="margin-top:8px"><b>값 만들기</b> <span class="muted" style="font-size:12px">문서를 만들 때마다 이 칸에 넣을 값${added && c.row ? " — 같은 열의 모든 행에 같이 적용" : ""}</span></div>
      <label class="fld">생성 방법 <select id="ed-source">${sourceOptions(c.source || "", auto.kind ? (edSources?.rule_names || {})[auto.kind] || auto.kind : "")}</select></label>
      <label class="fld">값 종류 <span class="muted" style="font-size:12px">(자동 생성과 채점 비교에 씀)</span> <select id="ed-kind"><option value="">(자동: ${esc(auto.kind || "text")})</option>${ed.view.kinds.map(k =>
        `<option value="${k}" ${c.kind === k ? "selected" : ""}>${k}</option>`).join("")}</select></label>
      ${c.source === "rule:choice" ? `<label class="fld">보기 (한 줄에 하나) <textarea id="ed-choices" rows="3">${esc((c.choices || []).join("\n"))}</textarea></label>` : ""}
      ${c.source === "rule:fixed" ? `<label class="fld">고정 글자 <input type="text" id="ed-fixed" value="${esc(c.text || "")}"></label>` : ""}
      ${added && c.t === "text" ? `<label class="fld"><input type="checkbox" id="ed-row" ${c.row ? "checked" : ""}> 표의 반복 행 칸 <span class="muted" style="font-size:12px">(행마다 같은 항목을 적는 표 — 표 질문으로 묻습니다)</span></label>` : ""}
      ${c.row ? `<label class="fld">표 묶음 <input type="text" id="ed-group" value="${esc(c.group || "")}" placeholder="(없음: 목록)"></label>
        <div class="muted" style="font-size:12px">표 반복 행입니다. 같은 표의 칸은 같은 묶음, 다른 표는 다른 묶음 (키 <span class="mono">&lt;묶음&gt;_목록.&lt;행&gt;.&lt;항목명&gt;</span>).
          키에 <span class="mono">{i}</span>를 쓰면 행 번호가 들어갑니다 (예: products.{i}.name)</div>
        ${c.rect ? `<div class="bar" style="flex-wrap:wrap">아래로 <input type="number" id="ed-rown" value="4" min="1" max="50" style="width:4em"> 행,
          행 간격 <input type="number" id="ed-rowh" value="${r1(c.rect[3] - c.rect[1])}" min="1" step="0.5" style="width:5em"> pt <button id="ed-rowdup">이 행 복제</button>
          <button id="ed-colfit" title="같은 표 묶음·같은 항목명(같은 열)의 모든 행 칸을 이 칸과 같은 가로 위치·폭으로">이 열 폭을 모든 행에</button></div>
          <div class="muted" style="font-size:12px">첫 행의 칸을 모두 그리고(각 칸: 항목명 + 표의 반복 행 + 같은 표 묶음) 누릅니다. 이 칸과 같은 높이에 있는 같은 묶음의 칸을 함께 복제합니다.
            표 행이 둘 이상이어야 표가 됩니다 (한 행뿐이면 보통 칸).</div>` : ""}` : ""}` : ""}
      ${c.t === "copy" ? `<label class="fld">따라 쓸 문구 <input type="text" id="ed-copytext" value="${esc(c.text || "")}"></label>` : ""}
      ${c.t === "check" ? `<div class="fld">보기 ${(c.options || []).map((o, j) => `<div class="optrow"><input type="text" data-opt="${j}" value="${esc(o.text || "")}"
        ${ed.sel.sub === `opt:${j}` ? `class="cur"` : ""}></div>`).join("")}
        <div class="muted" style="font-size:12px">${it.status === "added" ? "체크 도구로 끌면 보기를 더합니다. 보기를 고르고 Delete 로 뺍니다." : ""}</div></div>` : ""}`}
      <label class="fld">메모 <input type="text" id="ed-note" value="${esc(c.note || "")}"></label>
      <div class="mono muted" style="font-size:11px">${subsOf(ed, it).map(s => `${s.name}: ${s.box.map(r1).join(", ")}`).join("<br>")}</div>
      <div class="bar"><button id="ed-del">${it.status === "added" ? "지우기" : "빼기"}</button>
        ${st === "edited" && edEntry(ed, it, false) ? `<button id="ed-revert">이번 수정 되돌리기</button>` : ""}</div>`}
    </div>`;
  }
  if (ed.tableDraft) html = edTableForm(ed) + html;
  const list = edPageItems(ed).filter(x => x.kind !== "erase");
  const nEdited = ed.items.filter(x => statusOf(ed, x) !== "auto").length;
  html += `<div class="muted" style="margin:6px 0 4px">이 쪽 영역 ${list.length}개 · 지우기 ${ed.ov.erase.filter(e => e.page === ed.page).length}개 · 전체 수정 ${nEdited}개</div>
    <table class="ed-list"><thead><tr><th>상태</th><th>종류</th><th>키</th></tr></thead><tbody>${list.map(x => {
      const c = cur(ed, x), st = statusOf(ed, x);
      return `<tr class="click ${ed.sel && ed.sel.id === x.id ? "sel" : ""}" data-id="${esc(x.id)}"><td><span class="tag st-${st}">${ED_STATUS[st]}</span></td>
        <td class="nw">${esc(ED_T[c.t] || c.t)}</td>
        <td>${x.cell ? kpKeyCell(x.cell) : `<span class="mono muted">${esc(c.key || x.auto?.key || "")}</span>`}
          <div class="muted" style="font-size:11px">${esc(c.label || "")}</div></td></tr>`;
    }).join("")}</tbody></table>`;
  $("#ed-side").innerHTML = html;
  scrollRowIntoView($("#ed-side"), $("#ed-side tr.sel"));
  $("#ed-side .ed-list").onclick = e => {
    const id = e.target.closest("tr")?.dataset.id;
    const x = id && edFind(ed, id);
    if (x) { ed.sel = { id, sub: subsOf(ed, x)[0]?.name }; edDraw(ed); }
  };
  if (ed.tableDraft) edTableBind(ed);
  if (!it) return;
  const redraw = () => edDraw(ed);
  const on = (sel, ev, fn) => { const el = $(sel); if (el) el.addEventListener(ev, fn); };
  on("#ed-del", "click", () => edDelete(ed));
  on("#ed-undrop", "click", () => { const e = edEntry(ed, it, false); if (e) { delete e.drop; tidyEntry(ed, it); ed.dirty = true; redraw(); } });
  on("#ed-revert", "click", () => { const e = edEntry(ed, it, false); if (e) { ed.ov.items.splice(ed.ov.items.indexOf(e), 1); ed.dirty = true; redraw(); } });
  if (it.kind === "erase") {
    $$("input[name=ef]").forEach(r => r.onchange = () => { it.ref.fill = r.value; ed.dirty = true; redraw(); });
    on("#ed-to-text", "click", () => {
      ed.ov.add.push({ t: "text", page: it.ref.page, rect: [...it.ref.rect], label: "" });
      const x = { id: `add:${ed.ov.add.length - 1}:${Date.now()}`, status: "added", page: it.ref.page, ref: ed.ov.add[ed.ov.add.length - 1], auto: {} };
      ed.items.push(x); ed.sel = { id: x.id, sub: "rect" }; ed.dirty = true; redraw();
    });
    return;
  }
  if ($("#ed-kp")) kpPanel($("#ed-kp"), ed.d.id, it.cell, () => viewEditor(ed.d, { page: ed.page, tool: ed.tool, sel: ed.sel }), { label: false, image: false });
  on("#ed-label", "change", e => { setProp(ed, it, "label", e.target.value.trim()); redraw(); });
  on("#ed-key", "change", e => { setProp(ed, it, "key", e.target.value.trim()); redraw(); });
  const setCol = (k, v) => { for (const x of colPeers(ed, it)) setProp(ed, x, k, v); };   // 표 칸이면 같은 열 전체
  on("#ed-kind", "change", e => { setCol("kind", e.target.value); redraw(); });
  on("#ed-group", "change", e => { setProp(ed, it, "group", e.target.value.trim()); redraw(); });
  on("#ed-row", "change", e => {
    if (it.status === "added") setProp(ed, it, "row", e.target.checked ? true : null);
    else setGeom(ed, it, { row: e.target.checked });
    redraw();
  });
  on("#ed-rowdup", "click", () => edDupRows(ed, it, +$("#ed-rown").value, +$("#ed-rowh").value));
  on("#ed-colfit", "click", () => edFitColumn(ed, it));
  on("#ed-source", "change", e => { setCol("source", e.target.value); redraw(); });
  on("#ed-choices", "change", e => { setCol("choices", e.target.value.split("\n").map(s => s.trim()).filter(Boolean)); redraw(); });
  on("#ed-fixed", "change", e => { setCol("text", e.target.value); redraw(); });
  on("#ed-copytext", "change", e => { setProp(ed, it, "text", e.target.value); redraw(); });
  on("#ed-note", "change", e => { setProp(ed, it, "note", e.target.value.trim()); redraw(); });
  $$("#ed-side [data-key]").forEach(a => a.onclick = e => { e.preventDefault(); setProp(ed, it, "key", a.dataset.key); redraw(); });
  $$("#ed-side [data-opt]").forEach(inp => inp.onchange = () => {
    const c = cur(ed, it), opts = clone(c.options);
    opts[+inp.dataset.opt].text = inp.value;
    setGeom(ed, it, { options: opts });
    redraw();
  });
}

// 표 그리기 (도구 B): 끈 영역 = 표의 값 행들 (머리글 줄 빼고). 열 항목명·행 수·표 묶음을 정하면 열 × 행 글자 칸을 한 번에 만든다
const edTableCols = text => (text || "").split("\n").map(x => x.trim()).filter(Boolean);

function edTableForm(ed) {
  const t = ed.tableDraft;
  return `<div class="detail-box panel"><b>표 만들기</b> · ${t.page + 1}쪽
    <div class="muted" style="font-size:12px">끈 영역 = 표에서 값이 적히는 행들 (머리글 줄은 빼고). 열은 같은 폭으로 나눕니다.
      만든 뒤 첫 행 칸의 폭을 고치고 <b>이 열 폭을 모든 행에</b>로 맞춥니다. 영역을 다시 끌면 초안을 바꿉니다.</div>
    <label class="fld">열 항목명 <span class="muted" style="font-size:12px">(한 줄에 하나, 왼쪽부터 — 그림의 머리글 그대로)</span>
      <textarea id="ed-tb-cols" rows="4" placeholder="거래일&#10;적요&#10;금액">${esc(t.cols)}</textarea></label>
    <label class="fld">행 수 <input type="number" id="ed-tb-rows" min="2" max="60" value="${t.rows}" style="width:5em"></label>
    <label class="fld">표 묶음 이름 <input type="text" id="ed-tb-group" value="${esc(t.group)}" placeholder="예: 거래 (서식 안의 표마다 다르게)"></label>
    <div class="bar"><button class="primary" id="ed-tb-make">표 칸 만들기</button><button id="ed-tb-cancel">취소</button></div></div>`;
}

function edTableBind(ed) {
  const t = ed.tableDraft;
  const read = () => { t.cols = $("#ed-tb-cols").value; t.rows = +$("#ed-tb-rows").value; t.group = $("#ed-tb-group").value.trim(); };
  const preview = () => { read(); ed.keepSide = true; try { edDraw(ed); } finally { ed.keepSide = false; } };   // 나눔 미리보기 (입력 칸은 그대로)
  $("#ed-tb-cols").oninput = $("#ed-tb-rows").oninput = preview;
  $("#ed-tb-group").oninput = read;
  $("#ed-tb-cancel").onclick = () => { ed.tableDraft = null; edDraw(ed); };
  $("#ed-tb-make").onclick = () => { read(); edMakeTable(ed); };
}

function edMakeTable(ed) {
  const t = ed.tableDraft, cols = edTableCols(t.cols), n = t.rows;
  if (!cols.length) { toast("열 항목명을 한 줄에 하나씩 적으세요", true); return; }
  if (new Set(cols).size !== cols.length) { toast("열 항목명이 겹칩니다 (같은 이름 = 같은 열)", true); return; }
  if (!(n >= 2 && n <= 60)) { toast("행 수는 2~60 (한 행뿐이면 표가 아니라 보통 칸)", true); return; }
  const used = new Set(ed.items.filter(x => x.kind !== "erase" && cur(ed, x).row).map(x => cur(ed, x).group || ""));
  let group = t.group;
  if (!group) { let k = 1; while (used.has(`표${k}`)) k++; group = `표${k}`; }
  else if (used.has(group) && !confirm(`표 묶음 '${group}' 이 이미 있습니다. 같은 표에 더할까요? (다른 표면 취소하고 이름을 바꾸세요)`)) return;
  const [x0, y0, x1, y1] = t.rect, w = (x1 - x0) / cols.length, h = (y1 - y0) / n, pad = Math.min(1, h * 0.1);
  let first = null;
  for (let r = 0; r < n; r++) cols.forEach((label, c) => {
    const a = { t: "text", page: t.page, label, row: true, group,
      rect: [r1(x0 + c * w + pad), r1(y0 + r * h + pad), r1(x0 + (c + 1) * w - pad), r1(y0 + (r + 1) * h - pad)] };
    ed.ov.add.push(a);
    const x = { id: `add:${ed.ov.add.length - 1}:${Date.now()}:${r}:${c}`, status: "added", page: t.page, ref: a, auto: { key: null, kind: null } };
    ed.items.push(x);
    first = first || x;
  });
  ed.tableDraft = null;
  ed.sel = { id: first.id, sub: "rect" };
  ed.dirty = true;
  toast(`표 '${group}': ${cols.length}열 × ${n}행 = ${cols.length * n}칸. 열 폭이 그림과 다르면 첫 행 칸을 고치고 [이 열 폭을 모든 행에]. 저장해야 남습니다`);
  edDraw(ed);
}

// 이 칸과 같은 열의 추가한 표 칸들 (자신 포함). 표 칸이 아니면 자신만
function colPeers(ed, it) {
  const c = cur(ed, it);
  if (it.kind === "erase" || c.t !== "text" || !c.row) return [it];
  return ed.items.filter(x => {
    if (x === it) return true;
    if (x.kind === "erase" || x.page !== it.page || statusOf(ed, x) === "dropped") return false;
    const y = cur(ed, x);
    return y.t === "text" && y.row && (y.group || "") === (c.group || "") && y.label === c.label;
  });
}

// 같은 표 묶음·같은 항목명(= 같은 열)의 표 칸을 이 칸의 가로 위치·폭으로
function edFitColumn(ed, it) {
  const r = cur(ed, it).rect;
  let n = 0;
  for (const x of colPeers(ed, it)) {
    if (x === it) continue;
    const y = cur(ed, x).rect;
    setGeom(ed, x, { rect: [r[0], y[1], r[2], y[3]] });
    n++;
  }
  toast(n ? `'${cur(ed, it).label}' 열 ${n}칸을 맞췄습니다` : "같은 열(같은 묶음·항목명)의 다른 칸이 없습니다", !n);
  edDraw(ed);
}

// 표 행 복제: 고른 칸과 같은 높이·같은 쪽·같은 표 묶음의 표 칸들을 n 행 아래로 (행 간격 gap pt). 복제한 칸은 새로 더한 칸
function edDupRows(ed, it, n, gap) {
  if (!(n >= 1 && n <= 50) || !(gap > 0)) { toast("행 수(1~50)와 행 간격을 확인하세요", true); return; }
  const c = cur(ed, it), grp = c.group || "", y0 = c.rect[1], y1 = c.rect[3];
  const mid = r => (r[1] + r[3]) / 2;
  const row = ed.items.filter(x => {
    if (x.kind === "erase" || x.page !== it.page || statusOf(ed, x) === "dropped") return false;
    const y = cur(ed, x);
    return y.t === "text" && y.row && y.rect && (y.group || "") === grp && mid(y.rect) >= y0 && mid(y.rect) <= y1;
  });
  if (row.some(x => !cur(ed, x).label)) { toast("이 행에 항목명이 없는 칸이 있습니다. 항목명을 먼저 적으세요 (같은 항목명끼리 한 열)", true); return; }
  const H = ed.view.pages[it.page].h, KEEP = ["t", "page", "label", "row", "group", "key", "kind", "source", "choices", "text", "note"];
  const taken = ed.items.filter(x => x.kind !== "erase" && x.page === it.page && statusOf(ed, x) !== "dropped" && cur(ed, x).rect).map(x => cur(ed, x).rect);
  const over = (a, b) => Math.max(0, Math.min(a[2], b[2]) - Math.max(a[0], b[0])) * Math.max(0, Math.min(a[3], b[3]) - Math.max(a[1], b[1]))
    > 0.5 * Math.min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]));
  const first = row.map(x => { const r = cur(ed, x).rect; return [r[0], r[1] + gap, r[2], r[3] + gap]; });
  if (first.some(r => taken.some(t => over(r, t)))) { toast("바로 아래 자리에 이미 칸이 있습니다. 표의 마지막 행에서 복제하세요", true); return; }
  let made = 0, cut = 0;
  for (let k = 1; k <= n; k++) for (const x of row) {
    const y = cur(ed, x), r = y.rect, rect = [r[0], r1(r[1] + k * gap), r[2], r1(r[3] + k * gap)];
    if (rect[3] > H) { cut++; continue; }
    const a = { rect };
    for (const key of KEEP) if (y[key] !== undefined && y[key] !== "") a[key] = clone(y[key]);
    ed.ov.add.push(a);
    ed.items.push({ id: `add:${ed.ov.add.length - 1}:${Date.now()}:${made}`, status: "added", page: it.page, ref: a, auto: { key: null, kind: null } });
    made++;
  }
  ed.dirty = true;
  toast(`${row.length}열 × ${n}행 → ${made}칸을 더했습니다${cut ? ` (쪽을 넘는 ${cut}칸은 뺌)` : ""}. 저장해야 남습니다`);
  edDraw(ed);
}

// ---------------------------------------------------------------------------
function edPayload(ed) {
  const ov = clone(ed.ov);
  ov.add = ov.add.map(a => { const b = { ...a }; for (const k of Object.keys(b)) if (b[k] === "" || b[k] === null) delete b[k]; return b; });
  return ov;
}

async function edSave(ed) {
  try {
    await api(`/api/forms/${encodeURIComponent(ed.d.id)}/overrides`, { overrides: edPayload(ed) }, "PUT");
    ed.dirty = false;
    toast("저장했습니다. 생성기가 다음 렌더링부터 이 수정을 씁니다");
    state.forms = null;
    delete formCache[ed.d.id];
    const sel = ed.sel && !ed.sel.id.startsWith("add:") && !ed.sel.id.startsWith("erase:") ? ed.sel : null;
    await viewEditor(ed.d, { page: ed.page, tool: ed.tool, sel });
  } catch (e) { toast(e.message, true); }
}

async function edCompare(ed) {
  const o = readOptions(true, "cmp");
  $("#ed-cmp-stat").textContent = "렌더링 중…";
  try {
    const [a, b] = await Promise.all([renderOne(ed.d.id, o), renderOne(ed.d.id, o, false, edPayload(ed))]);
    const fa = new Map(a.fields.map(f => [f.key, f])), fb = new Map(b.fields.map(f => [f.key, f]));
    const diff = [];
    for (const k of new Set([...fa.keys(), ...fb.keys()])) {
      const x = fa.get(k), y = fb.get(k);
      const vx = x ? valueText(x) : "(없음)", vy = y ? valueText(y) : "(없음)";
      const moved = x && y && JSON.stringify((x.bbox || []).map(Math.round)) !== JSON.stringify((y.bbox || []).map(Math.round));
      if (vx !== vy || moved || !x || !y) diff.push({ key: k, before: vx, after: vy, moved: moved ? "위치 바뀜" : "" });
    }
    const page = Math.min(ed.page, a.pages.length - 1, b.pages.length - 1);
    $("#ed-cmp-out").innerHTML = `
      <div class="cmp2"><div><div class="muted">저장본 (seed ${o.seed}, ${page + 1}쪽)</div><div class="stage">${stageHTML(a, page, -1)}</div></div>
        <div><div class="muted">지금 고친 것</div><div class="stage">${stageHTML(b, page, -1)}</div></div></div>
      <h2>바뀐 키·값 ${diff.length}개</h2>
      ${diff.length ? table(diff, [["key", "키", r => `<span class="mono">${esc(r.key)}</span>`], ["before", "저장본"], ["after", "고친 것"], ["moved", ""]])
        : `<p class="muted">값과 위치가 같습니다 (배경 지우기는 그림에서 확인).</p>`}`;
    $("#ed-cmp-stat").textContent = `${a.elapsed}초 · ${b.elapsed}초`;
  } catch (e) { $("#ed-cmp-stat").innerHTML = `<span class="err">${esc(e.message)}</span>`; }
}
