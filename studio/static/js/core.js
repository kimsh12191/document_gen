// docgen studio 화면 공통: 도우미, 라우터, 그림 위 박스(겹쳐 보기·누르기). 빌드 없는 순수 JS (외부 CDN 없음).
// 메뉴마다 js/<메뉴>.js 가 addRoute 로 화면을 등록하고, main.js 가 마지막에 시작한다. 설계: studio/DESIGN.md
"use strict";

const $ = (sel, el = document) => el.querySelector(sel);
const $$ = (sel, el = document) => Array.from(el.querySelectorAll(sel));
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const main = () => $("#main");
const clone = o => JSON.parse(JSON.stringify(o));
const r1 = v => Math.round(v * 10) / 10;

async function api(path, body, method) {
  const opt = body === undefined ? { method: method || "GET" }
    : { method: method || "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  const r = await fetch(path, opt);
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(typeof data.detail === "string" ? data.detail : (JSON.stringify(data.detail) || `${r.status} ${r.statusText}`));
  return data;
}

async function apiUpload(path, file, fields = {}) {
  const fd = new FormData();
  fd.append("file", file);
  for (const [k, v] of Object.entries(fields)) fd.append(k, v);
  const r = await fetch(path, { method: "POST", body: fd });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.detail || `${r.status}`);
  return data;
}

// 화면 설정(층, 필터)은 이 브라우저에만 기억한다. 저장이 막힌 환경이면 그냥 기본값.
const store = {
  get(k, d) { try { const v = localStorage.getItem("studio." + k); return v === null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem("studio." + k, JSON.stringify(v)); } catch { /* 무시 */ } },
};

const state = {
  info: null,
  forms: null,
  layers: store.get("layers", { value: true, label: false, check: true, seal: true, sign: true }),
  filter: store.get("filter", { q: "", group: "", kind: "", review: "", korean: false }),
  sort: { key: "id", dir: 1 },
  opts: store.get("opts", { seed: 0, heavy: "default", special: "default", condition: "clean" }),
};

const LAYERS = [
  ["value", "값", "--l-value"], ["label", "키 설명", "--l-label"], ["check", "체크박스", "--l-check"],
  ["seal", "도장", "--l-seal"], ["sign", "서명", "--l-sign"],
];
const MODE_NAME = { default: "기본 확률", on: "항상", off: "끔" };
const COND_NAME = { clean: "원본", scan: "스캔", photo: "촬영", fax: "팩스", clean_jpeg: "JPEG 압축" };

function toast(msg, bad = false) {
  let t = $("#toast");
  if (!t) { t = document.createElement("div"); t.id = "toast"; document.body.appendChild(t); }
  t.textContent = msg;
  t.className = bad ? "bad on" : "on";
  clearTimeout(toast._h);
  toast._h = setTimeout(() => { t.className = ""; }, bad ? 6000 : 2500);
}

// ---------------------------------------------------------------------------
// 라우터: addRoute(정규식, 화면 함수, 메뉴 이름)
// ---------------------------------------------------------------------------
const routes = [];
const addRoute = (rx, fn, menu) => routes.push([rx, fn, menu]);
// 메뉴마다 "이 화면 도움말" 이 여는 설명서 자리 (guide/studio.md 의 절)
const HELP = { forms: "studio.md#1-서식", "new-forms": "studio.md#2-새-서식-추가", datasets: "studio.md#3-데이터셋",
  marks: "studio.md#4-돕는-메뉴", "ocr-examples": "benchmark.md", guide: "README.md" };

// 화면 단축키: 고르기 창(dialog)이 열려 있거나 입력 칸에서 누른 키는 화면에 넘기지 않는다 (Backspace 로 뒤의 칸이 빠지지 않게)
window.addEventListener("keydown", e => {
  if (!state.keyHandler || document.querySelector("dialog[open]")) return;
  if (e.target.closest && e.target.closest("input, select, textarea, [contenteditable], dialog")) return;
  state.keyHandler(e);
});

async function route() {
  state.keyHandler = null;   // 화면마다 자기 단축키를 다시 건다
  state.leave = null;
  const h = location.hash || "#/forms";
  for (const [rx, fn, menu] of routes) {
    const m = h.match(rx);
    if (m) {
      $$("#nav a").forEach(a => a.classList.toggle("on", a.dataset.menu === menu));
      if ($("#nav-help")) $("#nav-help").href = "#/guide/" + (HELP[menu] || "studio.md");
      try { await fn(...m.slice(1)); } catch (e) { main().innerHTML = `<p class="err">${esc(e.message)}</p>`; console.error(e); }
      return;
    }
  }
  location.hash = "#/forms";
}
window.addEventListener("hashchange", e => {
  if (state.leave && !state.leave()) {   // 떠나지 않기로 하면 주소를 되돌린다
    history.replaceState(null, "", new URL(e.oldURL).hash);
    return;
  }
  route();
});
window.addEventListener("beforeunload", e => { if (state.leave && !state.leave(true)) { e.preventDefault(); e.returnValue = ""; } });

// ---------------------------------------------------------------------------
// 렌더링 옵션 막대 (seed·내용 많음·특수 상황·촬영 조건)
// ---------------------------------------------------------------------------
function optionBar(withSeed, prefix = "o") {
  const o = state.opts, info = state.info || { modes: ["default", "on", "off"], conditions: Object.keys(COND_NAME) };
  const sel = (id, list, cur, names) => `<select id="${id}">${list.map(v =>
    `<option value="${v}" ${v === cur ? "selected" : ""}>${names[v] || v}</option>`).join("")}</select>`;
  return `
    ${withSeed ? `<label>seed <input type="number" id="${prefix}-seed" value="${o.seed}" min="0"></label>` : ""}
    <label>내용 많음 ${sel(`${prefix}-heavy`, info.modes, o.heavy, MODE_NAME)}</label>
    <label>특수 상황 ${sel(`${prefix}-special`, info.modes, o.special, MODE_NAME)}</label>
    <label>촬영 조건 ${sel(`${prefix}-cond`, info.conditions, o.condition, COND_NAME)}</label>`;
}

function readOptions(withSeed, prefix = "o") {
  const o = state.opts;
  if (withSeed) o.seed = Math.max(0, parseInt($(`#${prefix}-seed`).value || "0", 10));
  o.heavy = $(`#${prefix}-heavy`).value; o.special = $(`#${prefix}-special`).value; o.condition = $(`#${prefix}-cond`).value;
  store.set("opts", o);
  return o;
}

function layerBar() {
  return `<div class="layers">${LAYERS.map(([k, n, c]) =>
    `<label><input type="checkbox" data-layer="${k}" ${state.layers[k] ? "checked" : ""}>
     <span class="sw" style="background:var(${c})"></span>${n}</label>`).join("")}
    <label title="그림의 칸마다 정답 키(태그 이름)를 글자로 겹쳐 보입니다"><input type="checkbox" data-layer="keyname" ${state.layers.keyname ? "checked" : ""}> 키 이름</label></div>`;
}

function bindLayers(redraw) {
  $$("[data-layer]").forEach(cb => cb.addEventListener("change", () => {
    state.layers[cb.dataset.layer] = cb.checked;
    store.set("layers", state.layers);
    redraw();
  }));
}

async function renderOne(id, o, force = false, draft = undefined) {
  return api(`/api/forms/${encodeURIComponent(id)}/render`,
    { seed: o.seed, heavy: o.heavy, special: o.special, condition: o.condition, force, ...(draft !== undefined ? { draft } : {}) });
}

// ---------------------------------------------------------------------------
// 라벨 박스 겹쳐 보기와 누르기
// ---------------------------------------------------------------------------

// 라벨 항목 하나 → 그릴 상자들 [{layer, bbox, cls}]
function boxesOf(f) {
  const out = [];
  if (f.type === "checkbox" || f.type === "checkbox_multi") {
    for (const o of f.options || []) if (o.box_bbox) out.push({ layer: "check", bbox: o.box_bbox, cls: o.checked ? "checked" : "" });
    if (!(f.options || []).some(o => o.box_bbox) && f.bbox) out.push({ layer: "check", bbox: f.bbox, cls: "" });
  } else if (f.type === "seal" || f.type === "signature") {
    if (f.bbox) out.push({ layer: f.type === "seal" ? "seal" : "sign", bbox: f.bbox, cls: f.present ? "" : "absent" });
  } else {
    if (f.bbox) out.push({ layer: "value", bbox: f.bbox, cls: "" });
  }
  if (f.label_bbox) out.push({ layer: "label", bbox: f.label_bbox, cls: "" });
  return out;
}

// extra: [{bbox, cls, title}] 라벨 밖 상자 (문제 표시 등)
function stageHTML(label, page, sel, extra = []) {
  const pg = label.pages[page], url = label.image_urls[page];
  const rects = [];
  label.fields.forEach((f, i) => {
    if ((f.page || 0) !== page) return;
    for (const b of boxesOf(f)) {
      if (!state.layers[b.layer]) continue;
      const [x0, y0, x1, y1] = b.bbox;
      rects.push(`<rect data-i="${i}" class="l-${b.layer} ${b.cls} ${i === sel ? "sel" : ""}" x="${x0}" y="${y0}"
        width="${Math.max(1, x1 - x0)}" height="${Math.max(1, y1 - y0)}"></rect>`);
    }
  });
  if (state.layers.keyname) {   // 칸마다 키 이름 (박스 왼쪽 위)
    const fs = Math.max(8, pg.width * 0.0105);
    label.fields.forEach((f, i) => {
      if ((f.page || 0) !== page) return;
      const b = boxesOf(f).find(x => x.layer !== "label" && state.layers[x.layer]);
      if (b) rects.push(`<text class="keyname ${i === sel ? "sel" : ""}" x="${b.bbox[0]}" y="${Math.max(fs, b.bbox[1] - fs * 0.25)}" font-size="${fs}">${esc(f.key)}</text>`);
    });
  }
  for (const x of extra) {
    const [x0, y0, x1, y1] = x.bbox;
    rects.push(`<rect class="${x.cls || ""}" x="${x0}" y="${y0}" width="${Math.max(1, x1 - x0)}" height="${Math.max(1, y1 - y0)}"><title>${esc(x.title || "")}</title></rect>`);
  }
  return `<img src="${url}" alt=""><svg viewBox="0 0 ${pg.width} ${pg.height}" preserveAspectRatio="none">${rects.join("")}</svg><div class="tip"></div>`;
}

// 누른 자리의 항목 찾기: 자리를 포함하는 박스 중 가장 작은 것(겹친 큰 칸보다 안쪽 체크박스·도장이 먼저),
// 포함하는 박스가 없으면 tol 안에서 가장 가까운 것. 크기·거리가 같으면 실제로 찍힌 것(결재란의 도장/서명 자리가
// 같은 칸에 겹쳐 있음)을 먼저. 켜 둔 층의 박스만 본다.
function hitTest(label, page, x, y, tol) {
  let best = null;
  const better = (a, b) => { for (let k = 0; k < a.length; k++) if (a[k] !== b[k]) return a[k] < b[k]; return false; };
  label.fields.forEach((f, i) => {
    if ((f.page || 0) !== page) return;
    for (const b of boxesOf(f)) {
      if (!state.layers[b.layer]) continue;
      const [x0, y0, x1, y1] = b.bbox;
      const d = Math.hypot(Math.max(x0 - x, 0, x - x1), Math.max(y0 - y, 0, y - y1));
      if (d > tol) continue;
      const s = [d > 0 ? 1 : 0, d > 0 ? d : (x1 - x0) * (y1 - y0), b.cls === "absent" ? 1 : 0];
      if (!best || better(s, best.s)) best = { i, s };
    }
  });
  return best ? best.i : -1;
}

// 그림 위 마우스: 잡힐 박스를 미리 강조하고 말풍선으로 키·값을 보여 준다. 누르면 onPick(항목 번호 또는 -1, 그림 좌표).
// 그림을 다시 그려도(innerHTML) 바깥 상자에 붙인 이벤트는 그대로 남는다.
function bindStage(stageEl, getLabel, getPage, onPick) {
  stageEl.classList.add("pick");
  let hov = -1;
  const locate = e => {
    const svg = stageEl.querySelector("svg"), L = getLabel();
    if (!svg || !L) return null;
    const r = svg.getBoundingClientRect(), pg = L.pages[getPage()];
    const kx = pg.width / r.width, ky = pg.height / r.height;
    const x = (e.clientX - r.left) * kx, y = (e.clientY - r.top) * ky;
    return { i: hitTest(L, getPage(), x, y, 14 * kx), x, y, k: kx,
             px: e.clientX - stageEl.getBoundingClientRect().left, py: e.clientY - stageEl.getBoundingClientRect().top };
  };
  const setHover = (i, pos) => {
    if (i !== hov) {
      stageEl.querySelectorAll("rect.hover").forEach(r => r.classList.remove("hover"));
      if (i >= 0) stageEl.querySelectorAll(`rect[data-i="${i}"]`).forEach(r => r.classList.add("hover"));
      hov = i;
    }
    stageEl.classList.toggle("over", i >= 0);
    const tip = stageEl.querySelector(".tip");
    if (!tip) return;
    if (i < 0 || !pos) { tip.style.display = "none"; return; }
    const f = getLabel().fields[i];
    tip.textContent = `${f.key} = ${valueText(f)}`;
    tip.style.display = "block";
    tip.style.left = `${Math.min(pos.px + 14, stageEl.clientWidth - tip.offsetWidth - 4)}px`;
    tip.style.top = `${pos.py + 16}px`;
  };
  stageEl.addEventListener("mousemove", e => { const p = locate(e); if (p) setHover(p.i, p); });
  stageEl.addEventListener("mouseleave", () => setHover(-1));
  stageEl.addEventListener("click", e => { const p = locate(e); if (p) onPick(p.i, p); });
  return { hover: i => { hov = -2; setHover(i); } };
}

function valueText(f) {
  if (f.type === "seal" || f.type === "signature") return f.present ? "있음" : "없음";
  if (Array.isArray(f.value)) return f.value.join(", ");
  return f.value === null || f.value === undefined ? "(빈 칸)" : f.value;
}

// 표 안에서만 스크롤해 줄이 보이게 (scrollIntoView 는 본문까지 움직여 그림 위치가 바뀐다)
function scrollRowIntoView(box, row) {
  if (!box || !row) return;
  const rr = row.getBoundingClientRect(), sr = box.getBoundingClientRect();
  if (rr.top < sr.top || rr.bottom > sr.bottom) box.scrollTop += rr.top - sr.top - sr.height / 3;
}

// 간단한 표 (rows: 객체 목록, cols: [[키, 제목, 셀 함수?, 숫자?]])
function table(rows, cols, rowAttr = () => "") {
  return `<table><thead><tr>${cols.map(c => `<th class="${c[3] ? "num" : ""}">${c[1]}</th>`).join("")}</tr></thead><tbody>${rows.map((r, i) =>
    `<tr ${rowAttr(r, i)}>${cols.map(c => `<td class="${c[3] ? "num" : ""}">${c[2] ? c[2](r, i) : esc(r[c[0]] ?? "")}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
}
