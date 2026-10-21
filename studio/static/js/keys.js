// 키 사전 (studio/DESIGN.md 16.0): 화면의 말은 업무명·문서명·키 셋. 키는 범위가 둘 — 공통 키(여러 문서에 나오고 서류끼리 대조·심사하는 값,
// 사전에서 이름을 정함)와 문서별 키(서식의 키 그대로). 문서별 키를 공통 키에 '이으면' 그 칸은 공통 키로 묻고 답한다.
// 서버: studio/api_dictionary.py (docgen/dictionary.py, docgen/dictionary/*.json), 값 종류·값 출처는 studio/api_keys.py (docgen/key_rules.json)
"use strict";

addRoute(/^#\/keys(?:\/(\w+))?$/, tab => viewKeys(tab || "keys"), "keys");

const HOW_NAME = { code: "코드", source: "프로필 값", choices: "목록", pattern: "틀" };
const BY_TAG = x => x.by === "사람" ? `<span class="tag ok">사람</span>` : "";
const STATE_TAG = { "이음": `<span class="tag ok">이음</span>`, "제안": `<span class="tag warn">제안</span>`, "끊음": `<span class="tag">끊음</span>`, "공통": `<span class="tag ok">공통</span>` };

async function viewKeys(tab) {
  const s = await api("/api/dictionary");
  const tabs = [["keys", "키", s.suggested], ["docs", "문서"], ["tasks", "업무"], ["kinds", "값 종류"]];
  main().innerHTML = `
    <h1>키 사전</h1>
    <div class="sub">프롬프트가 묻고 답하는 것은 <b>업무명 · 문서명 · 키</b>입니다. 키는 둘로 나뉩니다.
      <b>공통 키</b>는 여러 문서에 나오고 서류끼리 대조·심사하는 값(예: 고객 성명), <b>문서별 키</b>는 그 문서에 찍힌 칸 그대로입니다.
      문서별 키를 공통 키에 <b>이으면</b> 서식이 달라도 같은 키로 묻고 답합니다. 생성 결과에 반영하는 것은 평가 세트 버전을 올릴 때입니다.</div>
    <div class="sub">공통 키 ${s.common} · 문서별 키 ${s.doc_keys.toLocaleString()} (공통 키에 이음 ${s.linked.toLocaleString()} · 제안 ${s.suggested.toLocaleString()})
      · 문서 ${s.docs} · 업무 ${s.tasks}</div>
    <div class="tabs">${tabs.map(([k, n, c]) => `<a href="#/keys/${k}" class="${k === tab ? "on" : ""}">${n}${c ? ` <span class="tag warn">제안 ${c.toLocaleString()}</span>` : ""}</a>`).join("")}</div>
    <div id="kd-body"></div>`;
  if (tab === "kinds") return kindsTab(await api("/api/keyrules"));
  return ({ keys: keysTab, docs: docsTab, tasks: tasksTab })[tab](s);
}

// ---------------------------------------------------------------------------
// 키: 공통 키 · 문서별 키
// ---------------------------------------------------------------------------
async function keysTab() {
  const f = store.get("dict.keys", { scope: "common", doc: "", q: "", state: "" });
  const docs = await api("/api/dictionary/doc_types");
  const common = (await api("/api/dictionary/keys?scope=common")).rows;
  const docName = id => docs.types[id]?.name || id;
  $("#kd-body").innerHTML = `
    <div class="bar">
      <select id="kk-scope"><option value="common" ${f.scope === "common" ? "selected" : ""}>공통 키</option><option value="doc" ${f.scope === "doc" ? "selected" : ""}>문서별 키</option></select>
      <span id="kk-docbox" ${f.scope === "doc" ? "" : "hidden"}>
        <input list="kk-doclist" id="kk-doc" placeholder="문서명 (비우면 전체)" value="${esc(f.doc ? docName(f.doc) : "")}" style="width:240px">
        <datalist id="kk-doclist">${Object.entries(docs.types).map(([id, t]) => `<option value="${esc(t.name)}" data-id="${esc(id)}">`).join("")}</datalist>
        <select id="kk-state">${[["", "잇기 전체"], ["제안", "제안만"], ["이음", "이은 것"], ["끊음", "끊은 것"], ["공통", "그 자체가 공통 키"]].map(([v, n]) =>
          `<option value="${v}" ${v === f.state ? "selected" : ""}>${n}</option>`).join("")}</select></span>
      <input type="text" id="kk-q" placeholder="키·이름 검색" value="${esc(f.q)}"> <span class="muted" id="kk-n"></span>
      ${f.scope === "common" ? `<button id="kk-new">새 공통 키</button>` : ""}</div>
    <div id="kk-bulk" class="bar" ${f.scope === "doc" ? "" : 'style="display:none"'}>고른 것을
      <select id="kk-to"><option value="">(지금 제안된 공통 키)</option>${common.map(c => `<option value="${esc(c.key)}">${esc(c.name)} · ${esc(c.key)}</option>`).join("")}</select>
      <button class="primary" id="kk-link">에 잇기</button> <button id="kk-cut">끊기</button>
      <label><input type="checkbox" id="kk-all"> 보이는 것 모두</label></div>
    <div class="split"><div id="kk-list" class="scroll"></div><div id="kk-edit" class="panel">키를 고르세요.</div></div>`;
  let rows = [];
  const save = () => store.set("dict.keys", f);
  const load = async () => {
    if (f.scope === "common") {
      const r = await api(`/api/dictionary/keys?scope=common&q=${q(f.q)}`);
      rows = r.rows;
      $("#kk-n").textContent = `${r.total}개`;
      $("#kk-list").innerHTML = table(rows, [["key", "공통 키", x => `<a href="#" data-ck="${esc(x.key)}" class="mono">${esc(x.key)}</a>`],
        ["name", "이름", x => `${esc(x.name)} ${BY_TAG(x)}`], ["kind", "값 종류"], ["docs", "문서", null, true],
        ["linked", "이은 칸", x => `${x.linked}${x.suggested ? ` <span class="muted">+제안 ${x.suggested}</span>` : ""}`, true]]);
      $$("#kk-list [data-ck]").forEach(a => a.onclick = e => { e.preventDefault(); editCommon(a.dataset.ck, common); });
    } else {
      const r = await api(`/api/dictionary/keys?scope=doc&doc=${q(f.doc)}&q=${q(f.q)}&state=${q(f.state)}&limit=500`);
      rows = r.rows;
      $("#kk-n").textContent = `${r.total.toLocaleString()}개${r.total > rows.length ? ` (앞 ${rows.length})` : ""}`;
      $("#kk-list").innerHTML = table(rows, [["sel", "", (x, i) => x.state === "공통" ? "" : `<input type="checkbox" data-i="${i}">`],
        ...(f.doc ? [] : [["doc_name", "문서"]]), ["key", "문서별 키", x => `<span class="mono">${esc(x.key)}</span>`], ["label", "이름표"],
        ["to", "공통 키", x => x.to ? `${STATE_TAG[x.state] || ""} <a href="#" class="mono" data-ck="${esc(x.to)}">${esc(x.to)}</a>` : `<span class="muted">문서별</span>`]]);
      $$("#kk-list [data-ck]").forEach(a => a.onclick = e => { e.preventDefault(); editCommon(a.dataset.ck, common); });
    }
  };
  $("#kk-scope").onchange = e => { f.scope = e.target.value; save(); keysTab(); };
  $("#kk-q").onchange = e => { f.q = e.target.value; save(); load(); };
  if ($("#kk-doc")) $("#kk-doc").onchange = e => {
    const v = e.target.value.trim();
    f.doc = v ? (Object.entries(docs.types).find(([, t]) => t.name === v) || [""])[0] : "";
    save(); load();
  };
  $("#kk-state").onchange = e => { f.state = e.target.value; save(); load(); };
  $("#kk-all").onchange = e => $$("#kk-list [data-i]").forEach(el => el.checked = e.target.checked);
  const act = async state => {
    const items = $$("#kk-list [data-i]").filter(el => el.checked).map(el => ({ doc: rows[+el.dataset.i].doc, key: rows[+el.dataset.i].key }));
    if (!items.length) return toast("고른 칸이 없습니다", true);
    try { const r = await api("/api/dictionary/link", { items, to: $("#kk-to").value || null, state }); toast(`${r.changed}칸`); load(); }
    catch (e) { toast(e.message, true); }
  };
  $("#kk-link").onclick = () => act("이음");
  $("#kk-cut").onclick = () => act("끊음");
  if ($("#kk-new")) $("#kk-new").onclick = () => newCommon();
  load();
}

async function newCommon(prefill = {}) {
  const key = (prompt("새 공통 키 (영어 소문자, 앞부분.값 — 예: foreign.bank_address)", prefill.key || "") || "").trim();
  if (!key) return;
  const name = (prompt("이름 (예: 외국 상대 은행 주소)", prefill.name || "") || "").trim();
  try { await api(`/api/dictionary/key/${key.split(".").map(encodeURIComponent).join(".")}`, { name, kind: "text" }, "PUT"); toast("만들었습니다"); viewKeys("keys"); }
  catch (e) { toast(e.message, true); }
}

async function editCommon(ck, common) {
  const k = await api(`/api/dictionary/key/${ck.split(".").map(encodeURIComponent).join(".")}`);
  const rules = await api("/api/keyrules");
  const rule = (rules.keys.find(x => x.key === ck) || {}).rule || {};
  const src = await api("/api/keyrules/sources");
  const nLinked = k.docs.reduce((a, d) => a + d.keys.filter(x => x.state === "이음").length, 0);
  $("#kk-edit").innerHTML = `
    <div><b class="mono">${esc(ck)}</b> ${BY_TAG(k)} <span class="muted">문서 ${k.docs.length} · 이은 칸 ${nLinked}</span></div>
    <label>이름 <input type="text" id="ce-name" value="${esc(k.name)}" style="width:100%"></label>
    <div class="bar"><label>값 종류 <select id="ce-kind">${[...new Set([k.kind, ...rules.kinds.map(x => x.name)])].map(n =>
      `<option ${n === (rule.kind || k.kind) ? "selected" : ""}>${esc(n)}</option>`).join("")}</select></label>
      <label>가짜 값 출처 <select id="ce-src"><option value="">(값 종류로 만듦)</option>${src.sources.map(x =>
        `<option value="${esc(x.path)}" ${x.path === rule.source ? "selected" : ""}>${esc(x.path)} — ${esc(String(x.example).slice(0, 20))}</option>`).join("")}</select></label></div>
    <label>다른 이름 (외부 추출 결과의 키, 쉼표) <input type="text" id="ce-alias" value="${esc((rule.aliases || []).join(", "))}" style="width:100%"></label>
    <div class="bar"><button class="primary" id="ce-save">저장</button></div>
    <div><b>쓰는 업무</b> ${k.tasks.map(t => `<span class="tag">${esc(t.name)}</span>`).join(" ") || "없음"}</div>
    <div><b>이은 문서별 키</b></div>
    ${table(k.docs.slice(0, 120), [["name", "문서"], ["keys", "칸", d => d.keys.map(x => `${STATE_TAG[x.state]} <span class="mono">${esc(x.key)}</span> <span class="muted">${esc(x.label)}</span>`).join("<br>")]])}`;
  $("#ce-save").onclick = async () => {
    const name = $("#ce-name").value.trim(), kind = $("#ce-kind").value, source = $("#ce-src").value || null;
    try {
      await api(`/api/dictionary/key/${ck.split(".").map(encodeURIComponent).join(".")}`, { name, kind }, "PUT");
      await api(`/api/keyrules/keys/${q(ck)}`, { meaning: name, kind, source, aliases: $("#ce-alias").value.split(",").map(x => x.trim()).filter(Boolean),
        labels: rule.labels || [] }, "PUT");
      toast("저장"); editCommon(ck, common);
    } catch (e) { toast(e.message, true); }
  };
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
      <div><b>키</b> ${l.keys} — 공통 키 ${l.common} · 공통 키 제안 ${l.suggested} · 나머지는 문서별 키
        <a href="#" id="de-keys">이 문서의 키 보기</a></div>`;
    $("#de-keys").onclick = e => { e.preventDefault(); store.set("dict.keys", { ...store.get("dict.keys", {}), scope: "doc", doc: id, state: "", q: "" }); location.hash = "#/keys/keys"; };
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
