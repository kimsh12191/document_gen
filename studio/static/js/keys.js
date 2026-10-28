// 키 사전 (studio/DESIGN.md 16.0): 칸마다 키는 하나 — 공통 키(여러 서류에 나오고 서류끼리 대조하는 값) 또는 문서별 키(그 서식에만 있는 칸).
// 칸의 누구의 · 무엇을 정하면 그 둘이 공통 키일 때 공통 키가 된다. 고르기 패널은 keypick.js (서식 미리보기·영역 편집과 같이 쓴다).
// 서버: studio/api_dictionary.py (docgen/dictionary.py, docgen/dictionary/*.json), 값 종류·값 출처는 studio/api_keys.py (docgen/key_rules.json)
"use strict";

addRoute(/^#\/keys(?:\/(\w+))?$/, tab => viewKeys(tab || "common"), "keys");

const HOW_NAME = { code: "코드", source: "프로필 값", choices: "목록", pattern: "틀" };
const BY_TAG = x => x.by === "사람" ? `<span class="tag ok">사람</span>` : "";

async function viewKeys(tab) {
  if (tab === "keys") tab = "common";   // 예전 주소
  const [s] = await Promise.all([api("/api/dictionary"), kpLoad(true)]);
  const tabs = [["common", "공통 키"], ["cells", "서식의 키"], ["todo", "정리할 것", s.todo], ["docs", "문서"], ["tasks", "업무"], ["kinds", "값 종류"]];
  main().innerHTML = `
    <h1>키 사전</h1>
    <div class="sub">서식의 칸마다 키가 하나 있습니다. 키는 두 가지입니다.
      <b>공통 키</b>는 여러 서류에 나오고 서류끼리 대조하는 값(예: 고객 성명), <b>문서별 키</b>는 그 서식에만 있는 칸입니다.
      칸이 <b>누구의 · 무엇</b>인지 정하면, 그 둘이 공통 키일 때 그 칸은 공통 키가 됩니다. 생성 결과에 반영하는 것은 평가 세트 버전을 올릴 때입니다.</div>
    <div class="sub">공통 키 ${s.common} · 서식 ${s.forms} · 칸 ${s.cells.toLocaleString()} (공통 ${s.common_cells.toLocaleString()} · 문서별 ${s.doc_cells.toLocaleString()})
      ${s.todo ? ` · <a href="#/keys/todo">정리할 것 ${s.todo.toLocaleString()}</a>` : ""}</div>
    <div class="tabs">${tabs.map(([k, n, c]) => `<a href="#/keys/${k}" class="${k === tab ? "on" : ""}">${n}${c ? ` <span class="tag warn">${c.toLocaleString()}</span>` : ""}</a>`).join("")}</div>
    <div id="kd-body"></div>`;
  if (tab === "kinds") return kindsTab(await api("/api/keyrules"));
  return ({ common: commonTab, cells: () => cellsView($("#kd-body"), {}), todo: todoTab, docs: docsTab, tasks: tasksTab })[tab](s);
}

// ---------------------------------------------------------------------------
// 공통 키: 누구의 × 무엇
// ---------------------------------------------------------------------------
async function commonTab() {
  const t = await api("/api/dictionary/common");
  const byWho = {};
  for (const r of t.rows) (byWho[r.who] = byWho[r.who] || []).push(r);
  $("#kd-body").innerHTML = `
    <div class="bar"><button id="cm-new">새 공통 키</button>
      <span class="muted">누구의(줄) · 무엇(칸). 숫자는 그 키를 쓰는 서식 수입니다. 누르면 그 키인 칸을 봅니다.</span></div>
    <div class="split"><div class="scroll">${kpVocab.who.filter(w => byWho[w.id]).map(w => `<div class="who-row">
        <div class="who-name"><b>${esc(w.name)}</b><div class="muted" style="font-size:12px">${esc(w.desc)}</div></div>
        <div class="who-keys">${byWho[w.id].map(r => `<a href="#" data-ck="${esc(r.key)}" class="chip ${r.forms ? "" : "muted"}" title="${esc(r.name)} · ${esc(r.key)}">${esc(r.what_name || r.what)}
          <span class="muted">${r.forms}</span></a>`).join("")}</div></div>`).join("")}</div>
      <div id="cm-edit" class="panel">공통 키를 고르세요.</div></div>`;
  $$("#kd-body [data-ck]").forEach(a => a.onclick = e => { e.preventDefault(); editCommon(a.dataset.ck); });
  $("#cm-new").onclick = () => newCommon();
}

function newCommon() {
  $("#cm-edit").innerHTML = `<div><b>새 공통 키</b></div>
    <div class="muted">여러 서류에 나오고 서류끼리 같은 값이어야 하는 것만 공통 키로 만듭니다.</div>
    <div class="bar"><label>누구의 <select id="nc-who">${kpVocab.who.map(w => `<option value="${w.id}">${esc(w.name)}</option>`).join("")}</select></label>
      <label>무엇 <input id="nc-what" list="nc-whats" placeholder="예: bank_address" class="mono"></label>
      <datalist id="nc-whats">${kpVocab.what.filter(w => !KP_MARK.includes(w.id)).slice(0, 3000).map(w => `<option value="${esc(w.id)}">${esc(w.name)}</option>`).join("")}</datalist></div>
    <label>이름 <input id="nc-name" placeholder="(비우면 누구의 + 무엇 이름)" style="width:100%"></label>
    <div class="bar"><button class="primary" id="nc-save">만들기</button></div>`;
  $("#nc-save").onclick = async () => {
    try {
      const r = await api("/api/dictionary/common", { who: $("#nc-who").value, what: $("#nc-what").value.trim(), name: $("#nc-name").value.trim() });
      toast(`만들었습니다: ${r.name}`); await kpLoad(true); await commonTab(); editCommon(r.key);
    } catch (e) { toast(e.message, true); }
  };
}

async function editCommon(ck) {
  const [k, rules, src] = await Promise.all([api(`/api/dictionary/key/${ck.split(".").map(encodeURIComponent).join(".")}`),
    api("/api/keyrules"), api("/api/keyrules/sources")]);
  const rule = (rules.keys.find(x => x.key === ck) || {}).rule || {};
  $("#cm-edit").innerHTML = `
    <div><b>${esc(k.name)}</b> ${BY_TAG(k)} <span class="mono muted">${esc(ck)}</span></div>
    <div class="muted">누구의 <b>${esc(k.who_name)}</b> · 무엇 <b>${esc(k.what_name)}</b> · 서식 ${k.forms} · 칸 ${k.cells.length}</div>
    <label>이름 <input type="text" id="ce-name" value="${esc(k.name)}" style="width:100%"></label>
    <div class="bar"><label>값 종류 <select id="ce-kind">${[...new Set([k.kind, ...rules.kinds.map(x => x.name)])].map(n =>
      `<option ${n === (rule.kind || k.kind) ? "selected" : ""}>${esc(n)}</option>`).join("")}</select></label>
      <label>가짜 값 출처 <select id="ce-src"><option value="">(값 종류로 만듦)</option>${src.sources.map(x =>
        `<option value="${esc(x.path)}" ${x.path === rule.source ? "selected" : ""}>${esc(x.path)} — ${esc(String(x.example).slice(0, 20))}</option>`).join("")}</select></label></div>
    <label>다른 이름 (외부 추출 결과의 키, 쉼표) <input type="text" id="ce-alias" value="${esc((rule.aliases || []).join(", "))}" style="width:100%"></label>
    <div class="bar"><button class="primary" id="ce-save">저장</button></div>
    <div><b>쓰는 업무</b> ${k.tasks.map(t => `<span class="tag">${esc(t.name)}</span>`).join(" ") || "없음"}</div>
    <div><b>이 키인 칸</b></div>
    ${table(k.cells.slice(0, 300), [["form_name", "서식", x => `<a href="#/forms/${q(x.form)}/keys">${esc(x.form_name)}</a>`],
      ["label", "이름표"], ["raw", "서식의 키", x => `<span class="mono muted">${esc(x.raw[0])}</span>`], ["by", "정함", x => esc(KP_BY[x.by] || "")]])}`;
  $("#ce-save").onclick = async () => {
    const name = $("#ce-name").value.trim(), kind = $("#ce-kind").value, source = $("#ce-src").value || null;
    try {
      await api(`/api/dictionary/key/${ck.split(".").map(encodeURIComponent).join(".")}`, { name, kind }, "PUT");
      await api(`/api/keyrules/keys/${q(ck)}`, { meaning: name, kind, source, aliases: $("#ce-alias").value.split(",").map(x => x.trim()).filter(Boolean),
        labels: rule.labels || [] }, "PUT");
      toast("저장"); await kpLoad(true); editCommon(ck);
    } catch (e) { toast(e.message, true); }
  };
}

// ---------------------------------------------------------------------------
// 서식의 키: 칸마다 이름표 · 누구의 · 무엇 · 키. 서식 화면의 '키' 탭도 이것 (opts.form 고정)
// ---------------------------------------------------------------------------
async function cellsView(el, opts) {
  await kpLoad();
  const fixed = opts.form;
  const f = fixed ? { form: fixed, q: "", scope: "", who: "" } : store.get("dict.cells", { form: "", q: "", scope: "", who: "" });
  const ids = fixed ? null : await api("/api/form-ids").catch(() => null);
  const forms = ids ? (ids.forms || ids) : [];
  const fname = id => (forms.find(x => (x.id || x) === id) || {}).name || id;
  el.innerHTML = `
    <div class="bar">
      ${fixed ? "" : `<input list="cv-forms" id="cv-form" placeholder="서식 (비우면 전체)" value="${esc(f.form ? fname(f.form) : "")}" style="width:260px">
        <datalist id="cv-forms">${forms.map(x => `<option value="${esc(x.name || x)}" data-id="${esc(x.id || x)}">`).join("")}</datalist>`}
      <input type="text" id="cv-q" placeholder="이름표·키 검색" value="${esc(f.q)}">
      <select id="cv-scope">${[["", "공통·문서별"], ["common", "공통 키만"], ["doc", "문서별 키만"]].map(([v, n]) => `<option value="${v}" ${v === f.scope ? "selected" : ""}>${n}</option>`).join("")}</select>
      <select id="cv-who"><option value="">누구의 전체</option><option value="-" ${f.who === "-" ? "selected" : ""}>(모름)</option>${kpVocab.who.map(w =>
        `<option value="${w.id}" ${w.id === f.who ? "selected" : ""}>${esc(w.name)}</option>`).join("")}</select>
      <span class="muted" id="cv-n"></span></div>
    <div class="bar" id="cv-bulk">고른 칸을 누구의 <select id="cv-bwho"><option value="">(모름)</option>${kpVocab.who.map(w => `<option value="${w.id}">${esc(w.name)}</option>`).join("")}</select>
      <button id="cv-bset">로 정하기</button> <label><input type="checkbox" id="cv-all"> 보이는 것 모두</label>
      <span class="muted">무엇은 칸마다 정한 것(없으면 키로 추정한 것)을 그대로 씁니다.</span></div>
    <div class="split"><div id="cv-list" class="scroll"></div><div id="cv-edit" class="panel">칸을 고르세요.</div></div>`;
  let rows = [];
  const save = () => { if (!fixed) store.set("dict.cells", f); };
  const load = async () => {
    if (!$("#cv-list")) return;
    if (!fixed && !f.form && !f.q && !f.who && !f.scope) { $("#cv-list").innerHTML = `<p class="muted">서식을 고르거나 검색하세요.</p>`; $("#cv-n").textContent = ""; return; }
    const r = await api(`/api/dictionary/cells?form=${q(f.form)}&q=${q(f.q)}&scope=${q(f.scope)}&who=${q(f.who)}&limit=800`);
    if (!$("#cv-list")) return;   // 읽는 사이 다른 화면으로 넘어감
    rows = r.rows;
    $("#cv-n").textContent = `${r.total.toLocaleString()}칸${r.total > rows.length ? ` (앞 ${rows.length})` : ""}`;
    $("#cv-list").innerHTML = table(rows, [["sel", "", (x, i) => `<input type="checkbox" data-i="${i}">`],
      ...(f.form ? [] : [["form_name", "서식", x => `<a href="#/forms/${q(x.form)}/keys">${esc(x.form_name)}</a>`]]),
      ["label", "이름표", (x, i) => `<a href="#" data-c="${i}">${esc(x.label || "(없음)")}</a>`],
      ["who", "누구의 · 무엇", x => kpWhoCell(x)], ["key", "키", x => kpKeyCell(x)],
      ["by", "정함", x => x.by === "사람" ? `<span class="tag ok">사람</span>` : x.by === "자동" ? `<span class="muted">자동</span>` : ""]],
      (x, i) => `data-row="${i}"`);
    $$("#cv-list [data-c]").forEach(a => a.onclick = e => { e.preventDefault(); pick(+a.dataset.c); });
  };
  const pick = i => kpPanel($("#cv-edit"), rows[i].form, rows[i], async () => { await load(); const j = rows.findIndex(x => x.form === rows[i]?.form && x.id === rows[i]?.id); if (j >= 0) pick(j); });
  if (!fixed) $("#cv-form").onchange = e => {
    const v = e.target.value.trim();
    f.form = v ? ((forms.find(x => (x.name || x) === v) || {}).id || v) : "";
    save(); load();
  };
  $("#cv-q").onchange = e => { f.q = e.target.value.trim(); save(); load(); };
  $("#cv-scope").onchange = e => { f.scope = e.target.value; save(); load(); };
  $("#cv-who").onchange = e => { f.who = e.target.value; save(); load(); };
  $("#cv-all").onchange = e => $$("#cv-list [data-i]").forEach(x => x.checked = e.target.checked);
  $("#cv-bset").onclick = async () => {
    const pickd = $$("#cv-list [data-i]").filter(x => x.checked).map(x => rows[+x.dataset.i]);
    if (!pickd.length) return toast("고른 칸이 없습니다", true);
    const who = $("#cv-bwho").value || null;
    try {
      for (const [what, grp] of Object.entries(groupBy(pickd, x => x.what || ""))) {
        await api("/api/dictionary/cells", { items: grp.map(x => ({ form: x.form, keys: x.raw })), who, what: what || null }, "PUT");
      }
      toast(`${pickd.length}칸`); load();
    } catch (e) { toast(e.message, true); }
  };
  load();
}

const groupBy = (xs, fn) => xs.reduce((m, x) => ((m[fn(x)] = m[fn(x)] || []).push(x), m), {});

// ---------------------------------------------------------------------------
// 정리할 것: 공통 키 후보 · 누구 것인지 모르는 서명 칸 · 누구의만 정하면 되는 칸 · 깨진 이름표
// ---------------------------------------------------------------------------
async function todoTab() {
  const t = await api("/api/dictionary/todo");
  const g = Object.fromEntries(t.groups.map(x => [x.id, x]));
  const whoSel = (id, cur = "") => `<select id="${id}"><option value="">(누구의)</option>${kpVocab.who.map(w => `<option value="${w.id}" ${w.id === cur ? "selected" : ""}>${esc(w.name)}</option>`).join("")}</select>`;
  const cellLink = (x, i, grp) => `<a href="#" data-g="${grp}" data-i="${i}">${esc(x.label || "(없음)")}</a>`;
  const sect = (x, body) => `<details class="panel todo" ${x.n ? "open" : ""}><summary><b>${esc(x.title)}</b> <span class="tag ${x.n ? "warn" : "ok"}">${x.n.toLocaleString()}</span></summary>
    <div class="muted">${esc(x.desc)}</div>${x.n ? body : `<p class="muted">없습니다.</p>`}</details>`;
  $("#kd-body").innerHTML = `<div class="split"><div class="scroll">
    ${sect(g.candidate, `<div class="bar"><button class="primary" id="td-cand-all">모두 제안대로</button></div>
      ${table(g.candidate.rows.slice(0, 300), [["form_name", "서식"], ["label", "이름표", (x, i) => cellLink(x, i, "candidate")],
        ["raw", "서식의 키", x => `<span class="mono muted">${esc(x.raw[0])}</span>`],
        ["suggest", "제안", x => kpKeyCell({ common: true, key: x.suggest.key })],
        ["ok", "", (x, i) => `<button data-cand="${i}">제안대로</button>`]])}`)}
    ${sect(g.who, g.who.groups.slice(0, 80).map((x, j) => `<div class="todo-grp">
      <div class="bar"><b>${esc(x.label)}</b> <span class="muted">무엇: ${esc(x.what_name)} · ${x.rows.length}칸 · 서식 ${x.forms}</span>
        ${whoSel(`td-who-${j}`)} <button data-who="${j}">고른 칸 정하기</button></div>
      <details><summary class="muted">칸 보기</summary>${table(x.rows, [["c", "", (r, i) => `<input type="checkbox" data-wg="${j}" data-wi="${i}" checked>`],
        ["form_name", "서식"], ["label", "이름표", (r, i) => `<a href="#" data-wg2="${j}" data-wi2="${i}">${esc(r.label)}</a>`],
        ["raw", "서식의 키", r => `<span class="mono muted">${esc(r.raw[0])}</span>`]])}</details></div>`).join(""))}
    ${sect(g.mark, table(g.mark.rows, [["form_name", "서식", x => `<a href="#/forms/${q(x.form)}/preview">${esc(x.form_name)}</a>`],
      ["label", "이름표", (x, i) => cellLink(x, i, "mark")], ["raw", "서식의 키", x => `<span class="mono muted">${esc(x.raw.join(" · "))}</span>`]]))}
    ${sect(g.broken, table(g.broken.rows.slice(0, 300), [["form_name", "서식", x => `<a href="#/forms/${q(x.form)}/edit">${esc(x.form_name)}</a>`],
      ["label", "이름표", x => `<span class="kr">${esc(x.label || "(없음)")}</span>`], ["raw", "서식의 키", x => `<span class="mono muted">${esc(x.raw[0])}</span>`]]))}
    </div><div id="td-edit" class="panel">칸을 누르면 여기서 누구의 · 무엇을 정합니다.</div></div>`;
  const reload = () => viewKeys("todo");
  const put = async (items, who, what) => api("/api/dictionary/cells", { items: items.map(x => ({ form: x.form, keys: x.raw })), who, what }, "PUT");
  $$("#kd-body [data-g]").forEach(a => a.onclick = e => {
    e.preventDefault();
    const x = g[a.dataset.g].rows[+a.dataset.i];
    kpPanel($("#td-edit"), x.form, x.suggest ? { ...x, who: x.suggest.who, what: x.suggest.what } : x, reload);
  });
  $$("#kd-body [data-wg2]").forEach(a => a.onclick = e => {
    e.preventDefault();
    const x = g.who.groups[+a.dataset.wg2].rows[+a.dataset.wi2];
    kpPanel($("#td-edit"), x.form, { ...x, what: x.suggest.what }, reload);
  });
  $$("#kd-body [data-cand]").forEach(b => b.onclick = async () => {
    const x = g.candidate.rows[+b.dataset.cand];
    try { await put([x], x.suggest.who, x.suggest.what); toast("저장"); reload(); } catch (e) { toast(e.message, true); }
  });
  if ($("#td-cand-all")) $("#td-cand-all").onclick = async () => {
    if (!confirm(`공통 키 후보 ${g.candidate.rows.length}칸을 모두 제안대로 정할까요?`)) return;
    try {
      for (const grp of Object.values(groupBy(g.candidate.rows, x => `${x.suggest.who}|${x.suggest.what}`))) await put(grp, grp[0].suggest.who, grp[0].suggest.what);
      toast("저장"); reload();
    } catch (e) { toast(e.message, true); }
  };
  $$("#kd-body [data-who]").forEach(b => b.onclick = async () => {
    const j = +b.dataset.who, x = g.who.groups[j], who = $(`#td-who-${j}`).value;
    if (!who) return toast("누구의를 고르세요", true);
    const items = $$(`#kd-body [data-wg="${j}"]`).filter(c => c.checked).map(c => x.rows[+c.dataset.wi]);
    if (!items.length) return toast("고른 칸이 없습니다", true);
    try { await put(items, who, x.what); toast(`${items.length}칸`); reload(); } catch (e) { toast(e.message, true); }
  });
}

// ---------------------------------------------------------------------------
// 문서: 대분류 → 문서명 → 서식
// ---------------------------------------------------------------------------
async function docsTab() {
  const d = await api("/api/dictionary/doc_types");
  const f = store.get("dict.docs", { q: "", group: "" });
  $("#kd-body").innerHTML = `
    <div class="bar"><input type="text" id="dc-q" placeholder="문서명·다른 이름 검색" value="${esc(f.q)}">
      <select id="dc-g"><option value="">대분류 전체</option>${Object.entries(d.groups).map(([k, n]) => `<option value="${k}" ${k === f.group ? "selected" : ""}>${esc(n)}</option>`).join("")}</select>
      <span class="muted" id="dc-n"></span></div>
    <div class="split"><div id="dc-list" class="scroll"></div><div id="dc-edit" class="panel">문서를 고르세요. 문서명은 분류 문항의 정답이고, 다른 이름(영문 이름·줄임말)도 채점·서류 넣기에서 같은 문서로 봅니다.</div></div>`;
  const draw = () => {
    const ql = f.q.toLowerCase();
    const rows = Object.entries(d.types).filter(([id, t]) => (!f.group || t.group === f.group)
      && (!ql || id.includes(ql) || t.name.toLowerCase().includes(ql) || t.aliases.some(a => a.toLowerCase().includes(ql))));
    $("#dc-n").textContent = `${rows.length}종`;
    $("#dc-list").innerHTML = table(rows.slice(0, 300), [["id", "문서명", ([id, t]) => `<a href="#" data-doc="${esc(id)}">${esc(t.name)}</a> ${BY_TAG(t)}<div class="muted mono">${esc(id)}</div>`],
      ["group", "대분류", ([, t]) => esc(d.groups[t.group] || t.group)], ["forms", "서식", ([, t]) => t.forms.length, true],
      ["aliases", "다른 이름", ([, t]) => `<span class="muted">${esc(t.aliases.slice(0, 2).join(" · "))}</span>`]]);
    $$("#dc-list [data-doc]").forEach(a => a.onclick = e => { e.preventDefault(); editDoc(d, a.dataset.doc); });
  };
  $("#dc-q").oninput = e => { f.q = e.target.value; store.set("dict.docs", f); draw(); };
  $("#dc-g").onchange = e => { f.group = e.target.value; store.set("dict.docs", f); draw(); };
  draw();
}

function editDoc(d, id) {
  const t = d.types[id];
  $("#dc-edit").innerHTML = `
    <div class="mono">${esc(id)}</div>
    <label>문서명 (분류 정답) <input type="text" id="de-name" value="${esc(t.name)}" style="width:100%"></label>
    <label>대분류 <select id="de-g">${Object.entries(d.groups).map(([k, n]) => `<option value="${k}" ${k === t.group ? "selected" : ""}>${esc(n)}</option>`).join("")}</select></label>
    <label>다른 이름 (한 줄에 하나 — 영문 이름, 줄임말) <textarea id="de-al" rows="5" style="width:100%">${esc(t.aliases.join("\n"))}</textarea></label>
    <div>실제 서식: ${t.forms.map(f => `<a href="#/forms/${q(f)}" class="mono">${esc(f)}</a>`).join(" · ")}</div>
    <div class="bar"><button class="primary" id="de-save">저장</button></div>
    <div id="de-links" class="muted">연결 읽는 중…</div>`;
  api(`/api/dictionary/links/doc_type/${q(id)}`).then(l => {
    $("#de-links").innerHTML = `<div><b>쓰는 업무</b> ${l.tasks.map(t => `<span class="tag">${esc(t.name)}</span>`).join(" ") || "없음"}</div>
      <div><b>칸</b> ${l.keys} — 공통 키 ${l.common} · 나머지는 문서별 키
        ${t.forms.map(f => `<a href="#/forms/${q(f)}/keys">${esc(f)} 칸 보기</a>`).join(" · ")}</div>`;
  }).catch(() => { $("#de-links").textContent = ""; });
  $("#de-save").onclick = async () => {
    try {
      await api(`/api/dictionary/doc_type/${q(id)}`, { name: $("#de-name").value, group: $("#de-g").value,
        aliases: $("#de-al").value.split("\n").map(x => x.trim()).filter(Boolean) }, "PUT");
      toast("저장"); viewKeys("docs");
    } catch (e) { toast(e.message, true); }
  };
}

// ---------------------------------------------------------------------------
// 업무: 대분류 → 업무 (다른 이름, 이 업무의 역할 → 당사자)
// ---------------------------------------------------------------------------
// ---------------------------------------------------------------------------
// 업무: 대분류 → 업무명 (다른 이름, 필요한 문서, 대조할 공통 키)
// ---------------------------------------------------------------------------
async function tasksTab() {
  const d = await api("/api/dictionary/tasks");
  const byGroup = {};
  for (const [id, t] of Object.entries(d.tasks)) (byGroup[t.group] = byGroup[t.group] || []).push([id, t]);
  $("#kd-body").innerHTML = `
    <div class="split"><div class="scroll tree">${Object.entries(d.groups).map(([g, n]) => `<div class="node"><b>${esc(n)}</b>
      <div class="kids">${(byGroup[g] || []).map(([id, t]) => `<div><a href="#" data-task="${esc(id)}">${esc(t.name)}</a> <span class="muted mono">${esc(id)}</span> ${BY_TAG(t)}</div>`).join("")}</div></div>`).join("")}</div>
      <div id="tk-edit" class="panel">업무를 고르세요. 다른 이름은 서류 넣기에서 업무 폴더 이름을 알아볼 때 씁니다.</div></div>`;
  $$("[data-task]").forEach(a => a.onclick = e => { e.preventDefault(); editTask(d, a.dataset.task); });
}

function editTask(d, id) {
  const t = d.tasks[id];
  const roleRows = Object.entries(t.roles || {});
  const psel = cur => `<select>${Object.entries(d.parties).map(([k, n]) => `<option value="${k}" ${k === cur ? "selected" : ""}>${esc(n)}</option>`).join("")}</select>`;
  $("#tk-edit").innerHTML = `
    <div class="mono">${esc(id)}</div>
    <label>이름 <input type="text" id="te-name" value="${esc(t.name)}" style="width:100%"></label>
    <label>대분류 <select id="te-g">${Object.entries(d.groups).map(([k, n]) => `<option value="${k}" ${k === t.group ? "selected" : ""}>${esc(n)}</option>`).join("")}</select></label>
    <label>다른 이름 (쉼표) <input type="text" id="te-al" value="${esc(t.aliases.join(", "))}" style="width:100%"></label>
    <details><summary>이 업무에서만 뜻이 바뀌는 이름 (예: buyer = 고객)</summary>
    <div id="te-roles">${[...roleRows, ["", "customer"]].map(([r, p]) => `<div class="bar te-row"><input type="text" value="${esc(r)}" placeholder="키 앞부분 (예: buyer)" class="mono"> → ${psel(p)}</div>`).join("")}</div></details>
    <div class="bar"><button class="primary" id="te-save">저장</button></div>
    <div id="te-links" class="muted">연결 읽는 중…</div>`;
  api(`/api/dictionary/links/task/${q(id)}`).then(l => {
    $("#te-links").innerHTML = `<div><b>필요한 문서</b> ${l.doc_types.map(d => `<span class="tag">${esc(d.name)}</span>`).join(" ")}</div>
      <div><b>서류끼리 대조할 공통 키 ${l.shared.length}</b> — 이 업무의 둘 이상의 문서에 나와 같은 값이어야 하는 키</div>
      ${table(l.shared.slice(0, 60), [["key", "공통 키", x => `<span class="mono">${esc(x.key)}</span> ${esc(x.name)}`],
        ["names", "나오는 문서", x => esc(x.names.join(" · "))], ["n", "수", x => x.doc_types.length, true]])}`;
  }).catch(() => { $("#te-links").textContent = ""; });
  $("#te-save").onclick = async () => {
    const roles = Object.fromEntries($$(".te-row").map(el => [$("input", el).value.trim(), $("select", el).value]).filter(([r]) => r));
    try {
      await api(`/api/dictionary/task/${q(id)}`, { name: $("#te-name").value, group: $("#te-g").value,
        aliases: $("#te-al").value.split(",").map(x => x.trim()).filter(Boolean), roles }, "PUT");
      toast("저장"); viewKeys("tasks");
    } catch (e) { toast(e.message, true); }
  };
}

// ---------------------------------------------------------------------------
// 값 종류 (docgen/key_rules.json): 코드 종류(설명만)와 데이터 종류(프로필 값·목록·틀)
// ---------------------------------------------------------------------------
function kindsTab(d) {
  $("#kd-body").innerHTML = `
    <div class="bar"><button id="kn-new">새 값 종류</button>
      <span class="muted">코드 종류는 계산·형식이 있는 것이라 화면에서 고치지 않습니다. 데이터 종류는 프로필 값·목록·틀(# 숫자, A 대문자, a 소문자, {가|나} 고르기)로 만듭니다.</span></div>
    <div class="split"><div class="scroll">${table(d.kinds, [
      ["name", "종류", k => `<a href="#" data-kind="${esc(k.name)}" class="mono">${esc(k.name)}</a>`], ["meaning", "뜻"],
      ["how", "방식", k => `<span class="tag ${k.how === "code" ? "" : "ok"}">${HOW_NAME[k.how] || k.how}</span>`],
      ["keys", "쓰는 키", k => esc(k.keys.slice(0, 3).join(", ")) + (k.keys.length > 3 ? ` 외 ${k.keys.length - 3}` : "")]])}</div>
      <div id="kn-edit" class="panel">왼쪽에서 종류를 고르세요.</div></div>`;
  $$("[data-kind]").forEach(a => a.onclick = e => { e.preventDefault(); editKind(d.kinds.find(k => k.name === a.dataset.kind)); });
  $("#kn-new").onclick = () => {
    const name = (prompt("새 값 종류 이름 (영어 소문자·숫자·밑줄 — 예: bl_no)") || "").trim();
    if (name) editKind({ name, meaning: "", how: "pattern", pattern: "", keys: [], isNew: true });
  };
}

async function editKind(k) {
  const box = $("#kn-edit");
  const code = k.how === "code";
  const choicesText = c => Object.entries(c || {}).map(([v, w]) => w === 1 ? v : `${v}:${w}`).join("\n");
  box.innerHTML = `
    <div><b class="mono">${esc(k.name)}</b> <span class="tag">${HOW_NAME[k.how] || k.how}</span></div>
    ${code ? `<p>${esc(k.meaning)}</p><p class="muted">코드(docgen/realform.py Values.by_kind)로 만드는 종류입니다.</p>` : `
    <label>뜻 <input type="text" id="kn-meaning" value="${esc(k.meaning || "")}" style="width:100%"></label>
    <div class="bar"><label>방식 <select id="kn-how">${["pattern", "choices", "source"].map(h =>
      `<option value="${h}" ${h === k.how ? "selected" : ""}>${HOW_NAME[h]}</option>`).join("")}</select></label></div>
    <div id="kn-def"></div>`}
    <div id="kn-ex" class="muted"></div>
    ${code ? "" : `<div class="bar"><button class="primary" id="kn-save">저장</button>${k.isNew ? "" : `<button id="kn-del">지우기</button>`}</div>`}
    ${k.keys.length ? `<div class="muted">쓰는 키: ${esc(k.keys.join(", "))}</div>` : ""}`;
  const src = code ? null : await api("/api/keyrules/sources");
  const def = () => {
    const how = $("#kn-how").value;
    if (how === "pattern") return { how, pattern: $("#kn-pattern").value };
    if (how === "source") return { how, source: $("#kn-source").value };
    const choices = {};
    for (const line of $("#kn-choices").value.split("\n").map(s => s.trim()).filter(Boolean)) {
      const m = line.match(/^(.*?)(?::(\d+(?:\.\d+)?))?$/);
      choices[m[1].trim()] = m[2] ? Number(m[2]) : 1;
    }
    return { how, choices };
  };
  const showEx = async () => {
    try {
      const ex = await api("/api/keyrules/examples", code ? { kind: k.name } : { definition: def() });
      $("#kn-ex").textContent = "예시 값: " + ex.examples.map(v => v ?? "(빈 칸)").join(" · ");
    } catch (e) { $("#kn-ex").textContent = e.message; }
  };
  const drawDef = () => {
    const how = $("#kn-how").value;
    $("#kn-def").innerHTML = how === "pattern" ? `<label>틀 <input type="text" id="kn-pattern" class="mono" value="${esc(k.pattern || "")}" style="width:100%"></label>`
      : how === "source" ? `<label>프로필 값 <select id="kn-source">${src.sources.map(s => `<option value="${esc(s.path)}" ${s.path === k.source ? "selected" : ""}>${esc(s.path)} — ${esc(String(s.example).slice(0, 24))}</option>`).join("")}</select></label>`
      : `<label>목록 (한 줄에 하나, 가중치는 값:3) <textarea id="kn-choices" rows="8" style="width:100%">${esc(choicesText(k.choices))}</textarea></label>`;
    $$("#kn-def input, #kn-def select, #kn-def textarea").forEach(el => el.oninput = showEx);
    showEx();
  };
  if (code) { showEx(); return; }
  $("#kn-how").onchange = drawDef;
  drawDef();
  $("#kn-save").onclick = async () => {
    try { await api(`/api/keyrules/kinds/${q(k.name)}`, { meaning: $("#kn-meaning").value, ...def() }, "PUT"); toast("저장"); viewKeys("kinds"); }
    catch (e) { toast(e.message, true); }
  };
  if ($("#kn-del")) $("#kn-del").onclick = async () => {
    try { await api(`/api/keyrules/kinds/${q(k.name)}`, undefined, "DELETE"); viewKeys("kinds"); } catch (e) { toast(e.message, true); }
  };
}
