// docgen studio 화면. 빌드 없는 순수 JS (내부망에서 외부 CDN 없이 돈다). 설계: studio/DESIGN.md
"use strict";

const $ = (sel, el = document) => el.querySelector(sel);
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const main = () => $("#main");

async function api(path, body) {
  const r = await fetch(path, body === undefined ? {} :
    { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.detail || `${r.status} ${r.statusText}`);
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
  filter: store.get("filter", { q: "", group: "", kind: "", review: "", korean: false, scenario: false }),
  sort: { key: "id", dir: 1 },
  opts: store.get("opts", { seed: 0, heavy: "default", special: "default", condition: "clean" }),
};

const LAYERS = [
  ["value", "값", "--l-value"], ["label", "항목명", "--l-label"], ["check", "체크박스", "--l-check"],
  ["seal", "도장", "--l-seal"], ["sign", "서명", "--l-sign"],
];
const MODE_NAME = { default: "기본 확률", on: "항상", off: "끔" };
const COND_NAME = { clean: "원본", scan: "스캔", photo: "촬영", fax: "팩스", clean_jpeg: "JPEG 압축" };

// ---------------------------------------------------------------------------
// 라우터
// ---------------------------------------------------------------------------
const routes = [
  [/^#\/forms\/([^/]+)(?:\/(\w+))?$/, (id, tab) => viewForm(decodeURIComponent(id), tab || "preview"), "forms"],
  [/^#\/forms$/, () => viewForms(), "forms"],
  [/^#\/marks$/, () => viewPlan("marks"), "marks"],
  [/^#\/scenarios$/, () => viewPlan("scenarios"), "scenarios"],
  [/^#\/import$/, () => viewPlan("import"), "import"],
  [/^#\/review$/, () => viewPlan("review"), "review"],
  [/^#\/datasets$/, () => viewPlan("datasets"), "datasets"],
  [/^#\/eval$/, () => viewPlan("eval"), "eval"],
  [/^#\/jobs$/, () => viewPlan("jobs"), "jobs"],
  [/^#\/settings$/, () => viewSettings(), "settings"],
];

window.addEventListener("keydown", e => state.keyHandler && state.keyHandler(e));

async function route() {
  state.keyHandler = null;   // 화면마다 자기 단축키를 다시 건다
  const h = location.hash || "#/forms";
  for (const [rx, fn, menu] of routes) {
    const m = h.match(rx);
    if (m) {
      document.querySelectorAll("#nav a").forEach(a => a.classList.toggle("on", a.dataset.menu === menu));
      try { await fn(...m.slice(1)); } catch (e) { main().innerHTML = `<p class="err">${esc(e.message)}</p>`; }
      return;
    }
  }
  location.hash = "#/forms";
}
window.addEventListener("hashchange", route);

// ---------------------------------------------------------------------------
// ① 서식 목록
// ---------------------------------------------------------------------------
async function viewForms() {
  if (!state.forms) {
    main().innerHTML = `<p class="spin">서식 목록을 읽는 중…</p>`;
    state.forms = await api("/api/forms");
  }
  const f = state.filter;
  const groups = [...new Map(state.forms.map(x => [x.group, x.group_name])).entries()];
  main().innerHTML = `
    <h1>서식</h1>
    <div class="sub">생성기가 만드는 서식 ${state.forms.length}종. 줄을 누르면 상세·예시를 봅니다.</div>
    <div class="bar">
      <input type="text" id="f-q" placeholder="ID·서식명 검색" value="${esc(f.q)}" style="width:220px">
      <select id="f-group"><option value="">그룹 전체</option>${groups.map(([g, n]) =>
        `<option value="${esc(g)}" ${f.group === g ? "selected" : ""}>${esc(n)}</option>`).join("")}</select>
      <select id="f-kind">${[["", "종류 전체"], ["html", "html"], ["overlay", "overlay"]].map(([v, n]) =>
        `<option value="${v}" ${f.kind === v ? "selected" : ""}>${n}</option>`).join("")}</select>
      <select id="f-review">${[["", "검수 전체"], ["no", "미검수"], ["yes", "검수 완료"]].map(([v, n]) =>
        `<option value="${v}" ${f.review === v ? "selected" : ""}>${n}</option>`).join("")}</select>
      <label><input type="checkbox" id="f-korean" ${f.korean ? "checked" : ""}> 한글 키 있음</label>
      <label><input type="checkbox" id="f-scenario" ${f.scenario ? "checked" : ""}> 업무 시나리오에 쓰임</label>
      <span class="muted" id="f-count"></span>
    </div>
    <div id="f-table"></div>`;
  const update = () => {
    Object.assign(f, {
      q: $("#f-q").value.trim(), group: $("#f-group").value, kind: $("#f-kind").value, review: $("#f-review").value,
      korean: $("#f-korean").checked, scenario: $("#f-scenario").checked,
    });
    store.set("filter", f);
    drawFormTable();
  };
  ["#f-q", "#f-group", "#f-kind", "#f-review", "#f-korean", "#f-scenario"].forEach(s =>
    $(s).addEventListener(s === "#f-q" ? "input" : "change", update));
  drawFormTable();
}

function drawFormTable() {
  const f = state.filter, q = f.q.toLowerCase();
  let rows = state.forms.filter(x =>
    (!q || x.id.toLowerCase().includes(q) || x.name.toLowerCase().includes(q)) &&
    (!f.group || x.group === f.group) && (!f.kind || x.kind === f.kind) &&
    (!f.review || (f.review === "yes") === !!x.reviewed) &&
    (!f.korean || x.n_korean_keys > 0) && (!f.scenario || x.scenarios.length > 0));
  const { key, dir } = state.sort;
  rows = rows.slice().sort((a, b) => {
    const va = Array.isArray(a[key]) ? a[key].length : a[key], vb = Array.isArray(b[key]) ? b[key].length : b[key];
    return (va > vb ? 1 : va < vb ? -1 : 0) * dir;
  });
  $("#f-count").textContent = `${rows.length}종`;
  const cols = [["id", "ID"], ["name", "서식명"], ["group_name", "그룹"], ["kind", "종류"], ["n_keys", "키", 1],
    ["n_korean_keys", "한글 키", 1], ["n_empty", "값 없는 칸", 1], ["n_marks", "체크·도장·서명", 1],
    ["scenarios", "시나리오"], ["reviewed", "검수"]];
  $("#f-table").innerHTML = `<table><thead><tr>${cols.map(([k, n, num]) =>
    `<th data-k="${k}" class="${num ? "num" : ""}">${n}${state.sort.key === k ? (dir > 0 ? " ▲" : " ▼") : ""}</th>`).join("")}
    </tr></thead><tbody>${rows.map(x => `
    <tr class="click" data-id="${esc(x.id)}">
      <td class="mono">${esc(x.id)}</td><td>${esc(x.name)}</td><td class="nw">${esc(x.group_name)}</td>
      <td><span class="tag ${x.kind}">${x.kind}</span></td>
      <td class="num">${x.n_keys}</td>
      <td class="num ${x.n_korean_keys ? "kr" : ""}">${x.n_korean_keys || ""}</td>
      <td class="num">${x.n_empty || ""}</td><td class="num">${x.n_marks || ""}</td>
      <td>${x.scenarios.map(s => `<span class="tag">${esc(s)}</span>`).join("")}</td>
      <td class="nw">${x.reviewed ? `<span class="tag ok">완료</span>` : `<span class="muted">미검수</span>`}</td>
    </tr>`).join("")}</tbody></table>`;
  $("#f-table thead").addEventListener("click", e => {
    const k = e.target.closest("th")?.dataset.k;
    if (!k) return;
    state.sort = { key: k, dir: state.sort.key === k ? -state.sort.dir : 1 };
    drawFormTable();
  });
  $("#f-table tbody").addEventListener("click", e => {
    const id = e.target.closest("tr")?.dataset.id;
    if (id) location.hash = `#/forms/${encodeURIComponent(id)}`;
  });
}

// ---------------------------------------------------------------------------
// ① 서식 상세
// ---------------------------------------------------------------------------
const formCache = {};

async function viewForm(id, tab) {
  const d = formCache[id] || (formCache[id] = await api(`/api/forms/${encodeURIComponent(id)}`));
  const tabs = [["preview", "미리보기"], ["examples", "예시"], ["keys", `키 목록 (${d.keys.length})`], ["files", "파일"]];
  main().innerHTML = `
    <div class="muted"><a href="#/forms">서식</a> › ${esc(d.group_name)}</div>
    <h1>${esc(d.name)} <span class="mono muted">${esc(d.id)}</span></h1>
    <div>
      <span class="tag ${d.kind}">${d.kind} · ${d.origin}</span>
      <span class="tag">${d.category === "internal" ? "은행 서식" : "외부 발급"}</span>
      ${d.reviewed ? `<span class="tag ok">검수 완료</span>` : `<span class="tag">미검수</span>`}
      <span class="tag">배정: ${esc(d.split)}</span>
      ${d.n_korean_keys ? `<span class="tag warn">한글 키 ${d.n_korean_keys}</span>` : ""}
      ${d.scenario_names.map(s => `<span class="tag">시나리오: ${esc(s.name)}</span>`).join("")}
    </div>
    ${d.description ? `<div class="sub" style="margin-top:6px">${esc(d.description)}</div>` : ""}
    <div class="tabs">${tabs.map(([t, n]) =>
      `<a href="#/forms/${encodeURIComponent(id)}/${t}" class="${t === tab ? "on" : ""}">${n}</a>`).join("")}</div>
    <div id="tab"></div>`;
  if (tab === "preview") return tabPreview(d);
  if (tab === "examples") return tabExamples(d);
  if (tab === "keys") return tabKeys(d);
  return tabFiles(d);
}

function optionBar(withSeed) {
  const o = state.opts, info = state.info || { modes: ["default", "on", "off"], conditions: Object.keys(COND_NAME) };
  const sel = (id, list, cur, names) => `<select id="${id}">${list.map(v =>
    `<option value="${v}" ${v === cur ? "selected" : ""}>${names[v] || v}</option>`).join("")}</select>`;
  return `
    ${withSeed ? `<label>seed <input type="number" id="o-seed" value="${o.seed}" min="0"></label>` : ""}
    <label>내용 많음 ${sel("o-heavy", info.modes, o.heavy, MODE_NAME)}</label>
    <label>특수 상황 ${sel("o-special", info.modes, o.special, MODE_NAME)}</label>
    <label>촬영 조건 ${sel("o-cond", info.conditions, o.condition, COND_NAME)}</label>`;
}

function readOptions(withSeed) {
  const o = state.opts;
  if (withSeed) o.seed = Math.max(0, parseInt($("#o-seed").value || "0", 10));
  o.heavy = $("#o-heavy").value; o.special = $("#o-special").value; o.condition = $("#o-cond").value;
  store.set("opts", o);
  return o;
}

function layerBar() {
  return `<div class="layers">${LAYERS.map(([k, n, c]) =>
    `<label><input type="checkbox" data-layer="${k}" ${state.layers[k] ? "checked" : ""}>
     <span class="sw" style="background:var(${c})"></span>${n}</label>`).join("")}</div>`;
}

function bindLayers(redraw) {
  document.querySelectorAll("[data-layer]").forEach(cb => cb.addEventListener("change", () => {
    state.layers[cb.dataset.layer] = cb.checked;
    store.set("layers", state.layers);
    redraw();
  }));
}

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

function stageHTML(label, page, sel) {
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

// 그림 위 마우스: 잡힐 박스를 미리 강조하고 말풍선으로 키·값을 보여 준다. 누르면 onPick(항목 번호 또는 -1).
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
    return { i: hitTest(L, getPage(), x, y, 14 * kx), px: e.clientX - stageEl.getBoundingClientRect().left, py: e.clientY - stageEl.getBoundingClientRect().top };
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
  stageEl.addEventListener("click", e => { const p = locate(e); if (p) onPick(p.i); });
  return { hover: i => { hov = -2; setHover(i); } };
}

function valueText(f) {
  if (f.type === "seal" || f.type === "signature") return f.present ? "있음" : "없음";
  if (Array.isArray(f.value)) return f.value.join(", ");
  return f.value === null || f.value === undefined ? "(빈 칸)" : f.value;
}

async function renderOne(id, o, force = false) {
  return api(`/api/forms/${encodeURIComponent(id)}/render`,
    { seed: o.seed, heavy: o.heavy, special: o.special, condition: o.condition, force });
}

// 미리보기 탭 ---------------------------------------------------------------
function tabPreview(d) {
  const view = { label: null, page: 0, sel: -1, zoom: false };
  $("#tab").innerHTML = `
    <div class="bar">${optionBar(true)}
      <button class="primary" id="o-go">렌더링</button>
      <button id="o-prev" title="이전 seed">◀</button><button id="o-next" title="다음 seed">▶</button>
      <button id="o-force" title="캐시를 무시하고 다시 그림">다시 그리기</button>
      <span class="muted" id="o-stat"></span>
    </div>
    <div class="bar">${layerBar()}<button id="o-zoom">원래 크기</button>
      <span class="keys-help">그림에서 박스 근처를 누르면 선택 · <kbd>↑</kbd><kbd>↓</kbd> 항목 이동 · <kbd>←</kbd><kbd>→</kbd> 쪽 · <kbd>Esc</kbd> 해제</span></div>
    <div class="viewer">
      <div><div class="pages" id="v-pages"></div><div class="stage" id="v-stage"></div></div>
      <div class="side panel" id="v-side"></div>
    </div>`;
  const draw = (scroll = false) => {   // scroll: 선택한 박스가 보이게 그림을 움직임 (표·키보드로 고를 때만)
    const L = view.label;
    if (!L) return;
    $("#v-pages").innerHTML = L.pages.length > 1 ? L.pages.map((_, i) =>
      `<button data-p="${i}" class="${i === view.page ? "primary" : ""}">${i + 1}쪽</button>`).join("") : "";
    $("#v-stage").classList.toggle("zoom100", view.zoom);
    $("#v-stage").innerHTML = stageHTML(L, view.page, view.sel);
    drawSide();
    if (scroll) $("#v-stage rect.sel")?.scrollIntoView({ block: "nearest", inline: "nearest" });
  };
  const drawSide = () => {
    const L = view.label, f = L.fields[view.sel];
    const detail = f ? `<div class="detail-box panel">
        <div><b class="mono">${esc(f.key)}</b></div>
        <div>항목명: ${esc(f.label ?? "")}</div><div>타입: ${esc(f.type)}</div>
        <div>값: ${esc(valueText(f))}</div>
        ${f.norm !== undefined && f.norm !== f.value ? `<div>정규화 값: <span class="mono">${esc(JSON.stringify(f.norm))}</span></div>` : ""}
        ${f.options ? `<div>보기: ${f.options.map(o => `${o.checked ? "■" : "□"} ${esc(o.text)}`).join(" ")}</div>` : ""}
        ${f.kind ? `<div>종류: ${esc(f.kind)}</div>` : ""}
        ${f.corrected_from ? `<div>정정 전 값: ${esc(f.corrected_from)}</div>` : ""}
        <div>쪽: ${(f.page || 0) + 1} · 위치: ${f.bbox ? `<span class="mono">${f.bbox.map(Math.round).join(", ")}</span>` : "없음"}</div>
      </div>` : "";
    $("#v-side").innerHTML = `${detail}
      <div class="muted" style="margin-bottom:4px">항목 ${L.fields.length}개 · ${L.pages.length}쪽${L.overflow ? " · <b class=kr>쪽 넘침</b>" : ""}</div>
      <table><thead><tr><th>쪽</th><th>키</th><th>값</th></tr></thead><tbody>${L.fields.map((x, i) => `
        <tr class="click ${i === view.sel ? "sel" : ""}" data-i="${i}">
          <td>${(x.page || 0) + 1}</td><td class="mono ${/[^\x00-\x7f]/.test(x.key) ? "kr" : ""}">${esc(x.key)}</td>
          <td>${esc(valueText(x))}${x.bbox ? "" : ` <span class="muted">(위치 없음)</span>`}</td></tr>`).join("")}
      </tbody></table>`;
    // 선택한 줄이 보이게 표 안에서만 스크롤한다 (scrollIntoView 는 본문까지 움직여 그림 위치가 바뀐다)
    const side = $("#v-side"), row = side.querySelector("tr.sel");
    if (row) {
      const rr = row.getBoundingClientRect(), sr = side.getBoundingClientRect();
      if (rr.top < sr.top || rr.bottom > sr.bottom) side.scrollTop += rr.top - sr.top - sr.height / 3;
    }
  };
  const select = i => {
    view.sel = i;
    const f = view.label.fields[i];
    if (f && (f.page || 0) !== view.page) view.page = f.page || 0;
    draw(true);
  };
  const go = async (force = false) => {
    const o = readOptions(true);
    $("#o-stat").textContent = "렌더링 중…";
    try {
      const t = performance.now();
      view.label = await renderOne(d.id, o, force);
      view.page = Math.min(view.page, view.label.pages.length - 1);
      view.sel = -1;
      $("#o-stat").textContent = `seed ${o.seed} · ${((performance.now() - t) / 1000).toFixed(1)}초`;
      draw();
    } catch (e) {
      $("#o-stat").innerHTML = `<span class="err">${esc(e.message)}</span>`;
    }
  };
  $("#o-go").onclick = () => go();
  $("#o-force").onclick = () => go(true);
  $("#o-prev").onclick = () => { $("#o-seed").value = Math.max(0, +$("#o-seed").value - 1); go(); };
  $("#o-next").onclick = () => { $("#o-seed").value = +$("#o-seed").value + 1; go(); };
  $("#o-zoom").onclick = () => { view.zoom = !view.zoom; $("#o-zoom").textContent = view.zoom ? "폭에 맞춤" : "원래 크기"; draw(); };
  $("#v-pages").onclick = e => { const p = e.target.dataset.p; if (p !== undefined) { view.page = +p; draw(); } };
  const stage = bindStage($("#v-stage"), () => view.label, () => view.page, i => { view.sel = i; draw(); });
  $("#v-side").onclick = e => { const i = e.target.closest("tr")?.dataset.i; if (i !== undefined) select(+i); };
  $("#v-side").onmouseover = e => {   // 표에 마우스를 올리면 그림에서 그 박스를 강조
    const i = e.target.closest("tr")?.dataset.i;
    if (i !== undefined && (view.label.fields[+i].page || 0) === view.page) stage.hover(+i);
  };
  $("#v-side").onmouseleave = () => stage.hover(-1);
  state.keyHandler = e => {
    const L = view.label;
    if (!L || e.target.closest("input, select, textarea")) return;
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      const n = L.fields.length;
      select(view.sel < 0 ? (e.key === "ArrowDown" ? 0 : n - 1) : (view.sel + (e.key === "ArrowDown" ? 1 : -1) + n) % n);
    } else if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
      const p = view.page + (e.key === "ArrowRight" ? 1 : -1);
      if (p >= 0 && p < L.pages.length) { e.preventDefault(); view.page = p; view.sel = -1; draw(); }
    } else if (e.key === "Escape") {
      view.sel = -1; draw();
    }
  };
  bindLayers(draw);
  go();
}

// 예시 탭 -----------------------------------------------------------------
function tabExamples(d) {
  const start = store.get("ex.start", 0), count = store.get("ex.count", 8);
  $("#tab").innerHTML = `
    <div class="bar">
      <label>seed <input type="number" id="ex-start" value="${start}" min="0">부터</label>
      <label><input type="number" id="ex-count" value="${count}" min="1" max="48"> 장</label>
      ${optionBar(false)}
      <button class="primary" id="ex-go">만들기</button><span class="muted" id="ex-stat"></span>
    </div>
    <div class="bar">${layerBar()}</div>
    <div class="sub">같은 seed 는 늘 같은 고객·같은 값입니다. 카드를 누르면 그 seed 로 미리보기를 엽니다.</div>
    <div class="grid" id="ex-grid"></div>`;
  let labels = [];
  const drawCards = () => {
    $("#ex-grid").innerHTML = labels.map((L, k) => L && !L.error ? `
      <div class="card" data-seed="${L.seed}">
        <div class="stage">${stageHTML(L, 0, -1)}</div>
        <div class="cap"><span>seed ${L.seed}</span><span class="muted">${L.pages.length}쪽 · 항목 ${L.fields.length}${L.overflow ? " · <b class=kr>넘침</b>" : ""}</span></div>
      </div>` : `<div class="card"><div class="wait">${L && L.error ? `<span class="err">${esc(L.error)}</span>` : `seed ${k + +$("#ex-start").value}<br>만드는 중…`}</div></div>`).join("");
  };
  const go = async () => {
    const s = Math.max(0, parseInt($("#ex-start").value || "0", 10)), n = Math.min(48, Math.max(1, parseInt($("#ex-count").value || "8", 10)));
    store.set("ex.start", s); store.set("ex.count", n);
    const o = readOptions(false);
    labels = new Array(n).fill(null);
    drawCards();
    $("#ex-go").disabled = true;
    for (let k = 0; k < n; k++) {   // 렌더러가 하나라 차례로 만든다. 다 된 것부터 보인다.
      $("#ex-stat").textContent = `${k + 1}/${n}`;
      try { labels[k] = await renderOne(d.id, { ...o, seed: s + k }); } catch (e) { labels[k] = { error: e.message }; }
      drawCards();
    }
    $("#ex-stat").textContent = `${n}장`;
    $("#ex-go").disabled = false;
  };
  $("#ex-go").onclick = go;
  $("#ex-grid").onclick = e => {
    const seed = e.target.closest(".card")?.dataset.seed;
    if (seed === undefined) return;
    state.opts.seed = +seed; store.set("opts", state.opts);
    location.hash = `#/forms/${encodeURIComponent(d.id)}/preview`;
  };
  bindLayers(drawCards);
  go();
}

// 키 목록 탭 ---------------------------------------------------------------
function tabKeys(d) {
  $("#tab").innerHTML = `
    <div class="sub">서식마다 고객 30명으로 렌더링해 모은 키입니다 (<span class="mono">guide/fields/fields.json</span>).
      채움률은 30번 중 그 키가 나온 비율, 예시가 비어 있으면 값이 한 번도 안 채워진 칸입니다.
      <span class="kr">주황색</span>은 한글 키(영어 표준 키로 바꿀 대상)입니다.</div>
    <div class="bar"><input type="text" id="k-q" placeholder="키·항목명 검색" style="width:240px"></div>
    <div id="k-table"></div>`;
  const draw = () => {
    const q = $("#k-q").value.trim().toLowerCase();
    const rows = d.keys.filter(k => !q || k.key.toLowerCase().includes(q) || (k.label || "").toLowerCase().includes(q));
    $("#k-table").innerHTML = rows.length ? `<table><thead><tr><th>키</th><th>항목명</th><th>타입</th><th class="num">채움률</th><th>예시</th></tr></thead>
      <tbody>${rows.map(k => `<tr><td class="mono ${/[^\x00-\x7f]/.test(k.key) ? "kr" : ""}">${esc(k.key)}</td>
        <td>${esc(k.label ?? "")}</td><td>${esc(k.type)}</td><td class="num">${Math.round((k.fill_rate ?? 0) * 100)}%</td>
        <td>${k.example ? esc(k.example) : `<span class="muted">(값 없음)</span>`}</td></tr>`).join("")}</tbody></table>`
      : `<p class="muted">키 목록이 없습니다. <span class="mono">python scripts/build_schema.py</span>로 만듭니다.</p>`;
  };
  $("#k-q").oninput = draw;
  draw();
}

function tabFiles(d) {
  $("#tab").innerHTML = `
    <div class="sub">이 서식의 결과를 정하는 파일입니다 (저장소 기준 경로). 편집은 2단계(overlay 영역 편집·배경 지우기)와 6단계(html 복제)에서 UI로 합니다.</div>
    <table><thead><tr><th>역할</th><th>경로</th></tr></thead><tbody>${d.files.map(f =>
      `<tr><td>${esc(f.role)}</td><td class="mono">${esc(f.path)}</td></tr>`).join("")}</tbody></table>`;
}

// ---------------------------------------------------------------------------
// ②~⑧ 아직 구현 전인 메뉴: 무엇이 들어올지 보여 준다 (단계 번호는 DESIGN.md 11절)
// ---------------------------------------------------------------------------
const PLANS = {
  marks: ["표시 요소", "2단계", [
    "풀: 체크 표시·서명(투명 배경 이미지), 도장 틀(모양·테두리·글꼴·글자 배치·인주 색·번짐), 손글씨·인쇄체 글꼴",
    "지금 코드가 그리는 모양(V·■·○ 체크, 낙서 서명, 원형·사각 도장)을 기본 항목으로 등록",
    "이미지 올리기, 가중치·켜기 (도장 틀은 파일로 정함)",
    "샘플 서식에 바로 적용해 보기. 생성 라벨에 어떤 항목을 썼는지 기록",
    "확률(어느 칸에 무엇이 나올지)은 docgen/marks.json, 모양은 풀 — 둘을 나눈다"]],
  scenarios: ["시나리오·묶음", "4단계", [
    "시나리오 목록·편집: 필수 서류, 쓰는 서식의 검수 상태, 적용 가능한 사례·규칙",
    "묶음 목록과 묶음 상세: 서류 전부, 고객 프로필(서류끼리 맞아야 하는 값과 위치), 이 묶음에서 나온 문항",
    "대조 문항: 변조판과 원본을 나란히, 바뀐 칸 강조 · 심사 문항: 계산식과 쓰인 값 위치 · 구비 문항",
    "직접 묶음 만들기, 고객 일관성 검사, 문제 표시"]],
  import: ["가져오기", "7단계 (이미지 묶음) · 9단계 (결과 폴더)", [
    "두 방식: ① 이미지 묶음 → 사내 OCR → 묶기 ② 이미 만든 OCR·추론 결과 폴더 경로(studio/RESULTS_FORMAT.md) → 저장된 OCR로 묶기",
    "문서 이미지 뭉치(스캔·사진·PDF) 폴더 지정 또는 끌어다 놓기",
    "사내 OCR은 1부 준비 단계(training/bank_ocr)와 같은 코드·같은 캐시로 읽기. 이 PC처럼 OCR이 없으면 생성 데이터로 시험",
    "같은 포맷·양식끼리 묶기(masking_ui 지문 방식), 포맷마다 견본·문서 수·가까운 기존 서식",
    "포맷·양식마다 \"템플릿으로\" / \"기존 서식과 같음\" / \"건너뛰기\" 결정, 묶음 전체 또는 고른 포맷을 \"OCR 벤치마크로\"",
    "템플릿으로: 견본 고르기 → 배경 값 지우기(흰색·주변색, 지울 후보) → 값 영역 지정 → overlay 서식"]],
  review: ["검수", "7단계 (OCR 검수) · 9단계 (라벨·묶음 검수, 내부망)", [
    "OCR 검수: 쪽마다 사내 OCR 글자·박스를 고치고 확인 → 사내 OCR 형식 그대로 저장, 1부 scan --ocr-dir 로 바로 읽힘 → OCR 검수 정답",
    "라벨 검수: 결과 폴더의 추론 결과를 포맷 단위로 검수(키 대응, 값·박스 고치기, 같은 자리 모아 보기, 의심 먼저 보기), 검수 전후 점수",
    "묶음 검수: 실서류를 고객·업무 묶음으로 묶고 시나리오 지정 → 구비·대조·심사 정답은 규칙 코드가 계산, 사람은 확인",
    "실서류 검수 결과는 real_data_dir 에만 쓰고, 저장소에 넣거나 외부 분석기로 보내지 않음"]],
  datasets: ["데이터셋", "3단계 (등록부) · 4·5단계 (만들기)", [
    "등록부: OCR·은행 업무 데이터셋을 출처(합성 / 이미지 묶음 / 결과 폴더)와 정답 종류(정확 / 의사정답 / 검수 정답)와 함께 한 목록으로",
    "1부·2부 파이프라인이 명령줄로 만든 폴더도 경로만 등록 (형식 자동 인식, 읽기만)",
    "새로 만들기: OCR = 1부 bank_ocr prepare 형식(8과제), 은행 업무 = docgen.bench build + 2부 bank_task prepare",
    "레시피(과제, 서식, 시나리오, 수, 촬영 조건, 묶음 구성 규칙), 빌드 진행, 버전 기록·고정",
    "과제별 문항 보기: 이미지·질문·정답 박스(bbox_2d 0~1000)",
    "데이터셋 설명서(구성·정답 종류·한계·쓴 학습), 학습 설정 내보내기(1부 run_pipeline / 2부 run_bank_pipeline, studio/TRAINING.md)"]],
  eval: ["평가", "3단계", [
    "데이터셋마다 모델 답(predictions/*.jsonl)과 점수(reports/*.json) 목록, 답 파일 붙여 채점",
    "채점은 bank_ocr.metrics · bank_task.score 를 그대로 불러 명령줄과 같은 숫자",
    "문항마다 정답과 여러 모델 답을 나란히, 박스 겹쳐 보기, 틀린 것부터",
    "비교표: 모델끼리, 버전끼리, 합성·실서류, 사내 OCR 기준·검수 정답 기준",
    "학습 결과 폴더(runs/<실험>/)를 붙이면 어떤 데이터로 학습한 모델인지 함께 표시. 추론은 학습 파이프라인이 한다"]],
  jobs: ["작업", "8단계", [
    "서식 이미지 → CLI 분석기(Claude·Codex 등) → html 서식. 표 행 수·여러 쪽이 바뀌는 서류용",
    "html 편집기: 템플릿과 항목 표를 고치며 원본을 겹쳐 미리보기, 행 수 최소·최대로 쪽 나뉨 확인",
    "overlay 서식의 값 영역 초안 (vLLM 등 OpenAI 호환 API 또는 CLI)",
    "작업 목록과 진행 로그, 원본과 결과를 나란히 검토, \"다시 고쳐\" 의견, 승인 → 서식 등록"]],
};

function viewPlan(key) {
  const [title, stage, items] = PLANS[key];
  main().innerHTML = `<div class="plan"><h1>${title}</h1><div class="sub">${stage}에서 구현합니다. 설계: <span class="mono">studio/DESIGN.md</span></div>
    <div class="panel"><ul>${items.map(i => `<li>${esc(i)}</li>`).join("")}</ul></div></div>`;
}

// ⑨ 설정 -------------------------------------------------------------------
async function viewSettings() {
  const i = state.info || (state.info = await api("/api/info"));
  const row = (k, v) => `<tr><td>${k}</td><td class="mono">${v === null || v === undefined || v === "" ? `<span class="muted">(없음)</span>` : esc(v)}</td></tr>`;
  main().innerHTML = `<h1>설정</h1>
    <div class="sub">설정 파일: <span class="mono">${esc(i.config_file || "studio/config.json 없음 — 기본값 사용 (예시: studio/config.example.json)")}</span>. 바꾼 뒤 서버를 다시 띄웁니다.</div>
    <table><tbody>
      ${row("렌더링 브라우저", i.browser)}${row("미리보기 캐시", i.cache_dir)}
      ${row("사내 OCR", i.ocr ? `${i.ocr.callable || ""} ${i.ocr.base_url || ""}${i.ocr.path || ""}` : null)}
      ${row("데이터셋 등록부·작업 공간 (workspace_dir)", i.paths.workspace_dir)}
      ${row("가져올 이미지 폴더 (import_dir)", i.paths.import_dir)}${row("실서류 검수 결과 (real_data_dir)", i.paths.real_data_dir)}
      ${row("실서류에서 만든 서식 (private_forms_dir)", i.paths.private_forms_dir)}
      ${row("분석기", i.providers.join(", "))}
    </tbody></table>`;
}

// ---------------------------------------------------------------------------
(async () => {
  try {
    state.info = await api("/api/info");
    $("#nav-foot").textContent = state.info.browser ? "" : "렌더링 브라우저를 찾지 못했습니다 (⑨ 설정)";
  } catch { /* 설정 화면에서 다시 시도 */ }
  route();
})();
