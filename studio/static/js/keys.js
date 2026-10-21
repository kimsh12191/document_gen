// 키 사전: 당사자 → 서류 속 역할 → 속성 계층(필드 키·표시 요소), 문서 분류, 업무, 합치기 후보, 키 규칙(값 종류·값 출처·동의어), 값 종류.
// 설계: studio/DESIGN.md 15.7·16절. 계층 파일은 docgen/dictionary/*.json (서버 studio/api_dictionary.py, docgen/dictionary.py),
// 키 규칙은 docgen/key_rules.json (studio/api_keys.py, docgen/keyrules.py), 자동 키 목록은 docgen/keys.json.
"use strict";

addRoute(/^#\/keys(?:\/(\w+))?$/, tab => viewKeys(tab || "fields"), "keys");

const HOW_NAME = { code: "코드", source: "프로필 값", choices: "목록", pattern: "틀" };
const BY_TAG = x => x.by === "사람" ? `<span class="tag ok">사람</span>` : x.sure === false ? `<span class="tag warn">확인</span>` : "";

async function viewKeys(tab) {
  const s = await api("/api/dictionary");
  const tabs = [["fields", "필드 키", s.unsure], ["marks", "표시 요소"], ["docs", "문서 분류"], ["tasks", "업무"],
    ["merges", "합치기 후보", s.proposed], ["keys", "키 규칙"], ["kinds", "값 종류"]];
  main().innerHTML = `
    <h1>키 사전</h1>
    <div class="sub">서식·추출 결과·시나리오가 같은 이름을 쓰게 맞춥니다. 필드 키와 표시 요소는 <b>당사자 → 서류 속 역할 → 속성</b>으로 나뉘고,
      같은 사람·같은 값이면 서식이 달라도 같은 <b>당사자 키</b>(예: 고객 본인.이름)가 됩니다. 합치기는 결정만 하고, 생성 결과에 반영하는 것은
      평가 세트 버전을 올릴 때입니다 (DESIGN 16.2).</div>
    <div class="sub">역할 ${s.stats.roles ?? "-"} · 속성 ${s.stats.attributes ?? "-"} · 문서 종류 ${s.stats.doc_types ?? "-"} · 업무 ${s.stats.tasks ?? "-"}
      · 확인할 역할 ${s.unsure} · 합치기 후보 ${s.proposed}</div>
    <div class="tabs">${tabs.map(([k, n, c]) => `<a href="#/keys/${k}" class="${k === tab ? "on" : ""}">${n}${c ? ` <span class="tag warn">${c}</span>` : ""}</a>`).join("")}</div>
    <div id="kd-body"></div>`;
  if (tab === "keys" || tab === "kinds") {
    const d = await api("/api/keyrules");
    return (tab === "keys" ? keysTab : kindsTab)(d);
  }
  return ({ fields: fieldsTab, marks: marksTab, docs: docsTab, tasks: tasksTab, merges: mergesTab })[tab](s);
}

// ---------------------------------------------------------------------------
// 필드 키: 당사자 나무 → 역할 → 키
// ---------------------------------------------------------------------------
function fieldsTab(s) {
  const f = store.get("dict.fields", { open: "customer", unsure: false });
  $("#kd-body").innerHTML = `
    <div class="bar"><label><input type="checkbox" id="fd-unsure" ${f.unsure ? "checked" : ""}> 확인할 역할만</label>
      <span class="muted">역할을 누르면 그 역할의 키와 당사자 키가 보입니다. 당사자를 바꾸면 '사람'이 정한 것으로 남습니다.</span></div>
    <div class="split"><div id="fd-tree" class="scroll tree"></div><div id="fd-edit" class="panel">왼쪽에서 역할을 고르세요.</div></div>`;
  const draw = () => {
    $("#fd-tree").innerHTML = `<div class="node"><a href="#" id="fd-single"><b>▸ 역할 없는 키</b></a>
      <span class="muted">bank · date · 취급점 · 금액 처럼 속성만 있는 키 (주로 overlay 서식의 항목명 키)</span></div>` + s.parties.map(p => {
      const roles = p.roles.filter(r => !f.unsure || (r.sure === false && r.by !== "사람"));
      if (f.unsure && !roles.length) return "";
      const open = f.open === p.id || f.unsure;
      return `<div class="node"><a href="#" data-party="${esc(p.id)}"><b>${open ? "▾" : "▸"} ${esc(p.name)}</b></a>
        <span class="muted">역할 ${p.roles.length} · 키 ${p.keys} · 서식 ${p.forms}</span> <span class="muted small">${esc(p.desc || "")}</span>
        ${open ? `<div class="kids">${roles.map(r => `<div><a href="#" data-role="${esc(r.role)}" class="mono">${esc(r.role)}</a>
          <span class="muted">키 ${r.keys} · 서식 ${r.forms}</span> ${BY_TAG(r)}${r.by_task ? ` <span class="tag">업무별</span>` : ""}</div>`).join("")}</div>` : ""}</div>`;
    }).join("");
    $$("#fd-tree [data-party]").forEach(a => a.onclick = e => { e.preventDefault(); f.open = f.open === a.dataset.party ? "" : a.dataset.party; store.set("dict.fields", f); draw(); });
    $$("#fd-tree [data-role]").forEach(a => a.onclick = e => { e.preventDefault(); editRole(s, a.dataset.role); });
    $("#fd-single").onclick = e => { e.preventDefault(); editSingle(s, "unassigned"); };
  };
  $("#fd-unsure").onchange = e => { f.unsure = e.target.checked; store.set("dict.fields", f); draw(); };
  draw();
}

async function editSingle(s, show, qv = "") {
  const r = await api(`/api/dictionary/single?show=${show}&q=${q(qv)}`);
  const opts = cur => s.parties.map(p => `<option value="${p.id}" ${p.id === cur ? "selected" : ""}>${esc(p.name)}</option>`).join("");
  $("#fd-edit").innerHTML = `
    <div><b>역할 없는 키</b> <span class="muted">미정 ${r.counts.unassigned} · 추정 ${r.counts.unsure} · 전체 ${r.counts.all}</span></div>
    <div class="bar"><select id="sg-show">${[["unassigned", "미정"], ["unsure", "추정한 것"], ["all", "전체"]].map(([k, n]) =>
      `<option value="${k}" ${k === show ? "selected" : ""}>${n}</option>`).join("")}</select>
      <input type="text" id="sg-q" placeholder="속성·항목명" value="${esc(qv)}"> <span class="muted">${r.total}개 (서식 많은 순 ${r.rows.length})</span></div>
    <div class="bar">고른 것을 <select id="sg-all">${opts("")}</select> <button id="sg-apply">로 바꾸기</button>
      <button class="primary" id="sg-save">저장</button> <span class="muted">저장하면 '사람'이 정한 것으로 남습니다.</span></div>
    ${table(r.rows, [["sel", "", (x, i) => `<input type="checkbox" data-sg="${i}">`], ["attribute", "속성", x => `<span class="mono">${esc(x.attribute)}</span>`],
      ["label", "항목명"], ["forms", "서식", null, true], ["state", "", x => x.state === "사람" ? `<span class="tag ok">사람</span>` : x.state === "추정" ? `<span class="tag warn">추정</span>` : ""],
      ["party", "당사자", (x, i) => `<select data-sp="${i}">${opts(x.party)}</select>`]])}`;
  const changed = new Set();
  $$("[data-sp]").forEach(el => el.onchange = () => changed.add(+el.dataset.sp));
  $("#sg-show").onchange = e => editSingle(s, e.target.value, $("#sg-q").value);
  $("#sg-q").onchange = e => editSingle(s, $("#sg-show").value, e.target.value);
  $("#sg-apply").onclick = () => $$("[data-sg]").filter(el => el.checked).forEach(el => {
    const i = +el.dataset.sg; $(`[data-sp="${i}"]`).value = $("#sg-all").value; changed.add(i);
  });
  $("#sg-save").onclick = async () => {
    const parties = Object.fromEntries([...changed].map(i => [r.rows[i].attribute, $(`[data-sp="${i}"]`).value]));
    if (!Object.keys(parties).length) return toast("바꾼 것이 없습니다", true);
    try { const res = await api("/api/dictionary/single", { parties }, "PUT"); toast(`${res.changed}개 저장`); editSingle(s, show, qv); }
    catch (e) { toast(e.message, true); }
  };
}

async function editRole(s, role) {
  const r = await api(`/api/dictionary/role/${q(role)}`);
  const parties = s.parties.map(p => [p.id, p.name]);
  const sel = (id, cur, empty) => `<select ${id}>${empty ? `<option value="">${empty}</option>` : ""}${parties.map(([k, n]) =>
    `<option value="${k}" ${k === cur ? "selected" : ""}>${esc(n)}</option>`).join("")}</select>`;
  $("#fd-edit").innerHTML = `
    <div><b class="mono">${esc(role)}</b> ${BY_TAG(r)} <span class="muted">키 ${r.keys.length} · 서식 ${r.forms}</span></div>
    <div class="bar"><label>당사자 ${sel('id="rl-party"', r.party)}</label> <label>이름 <input type="text" id="rl-name" value="${esc(r.name || "")}" placeholder="예: 신청인"></label></div>
    <details ${r.by_task ? "open" : ""}><summary>업무마다 다르게 (예: 주택담보대출에서 buyer = 고객 본인)</summary>
      ${Object.entries(s.tasks).map(([t, n]) => `<div class="bar"><span style="width:160px">${esc(n)}</span>${sel(`data-task="${esc(t)}"`, (r.by_task || {})[t], "(기본)")}</div>`).join("")}</details>
    <div class="bar"><button class="primary" id="rl-save">저장</button></div>
    ${table(r.keys.slice(0, 200), [["key", "키", k => `<span class="mono">${esc(k.key)}</span>${k.canonical !== k.key ? `<div class="muted">→ ${esc(k.canonical)}</div>` : ""}`],
      ["labels", "항목명", k => esc(k.labels.join(" · "))], ["party_key", "당사자 키", k => `<a href="#" class="mono" data-pk="${esc(k.party_key)}">${esc(k.party_key)}</a>`],
      ["forms", "서식", null, true], ["doc_types", "문서 종류", null, true]])}
    <div id="rl-pk"></div>`;
  $$("#fd-edit [data-pk]").forEach(a => a.onclick = e => { e.preventDefault(); showPartyKey(a.dataset.pk, $("#rl-pk")); });
  $("#rl-save").onclick = async () => {
    const by_task = Object.fromEntries($$("[data-task]").map(el => [el.dataset.task, el.value]).filter(([, v]) => v));
    try { await api(`/api/dictionary/role/${q(role)}`, { party: $("#rl-party").value, name: $("#rl-name").value, by_task }, "PUT"); toast("저장"); viewKeys("fields"); }
    catch (e) { toast(e.message, true); }
  };
}

async function showPartyKey(pk, box) {
  const l = await api(`/api/dictionary/links/party_key/${pk.split(".").map(encodeURIComponent).join(".")}`);
  box.innerHTML = `<div class="panel"><b class="mono">${esc(pk)}</b> — 문서 종류 ${l.doc_types.length} · 업무 ${l.tasks.length}
    <div>${l.tasks.map(t => `<span class="tag">${esc(t.name)}</span>`).join(" ")}</div>
    <div class="muted">${esc(l.doc_types.slice(0, 30).map(d => d.name).join(" · "))}${l.doc_types.length > 30 ? " …" : ""}</div></div>`;
}

// ---------------------------------------------------------------------------
// 표시 요소: 도장·서명(당사자별) + 체크 보기 목록
// ---------------------------------------------------------------------------
async function marksTab(s) {
  const d = await api("/api/dictionary/marks");
  const pname = Object.fromEntries(s.parties.map(p => [p.id, p.name]));
  $("#kd-body").innerHTML = `
    <div class="sub">도장·서명 키는 역할 이름이 달라도 당사자로 모입니다 (seal.applicant · seal.holder → seal.고객 본인). 역할의 당사자는 '필드 키' 탭에서 바꿉니다.</div>
    <div class="bar">${Object.entries(d.by_party).map(([p, n]) => `<span class="tag">${esc(pname[p] || p)} ${n}</span>`).join(" ")}</div>
    ${table(d.marks, [["key", "키", m => `<span class="mono">${esc(m.key)}</span>`], ["type", "종류", m => m.type === "seal" ? "도장" : "서명"],
      ["party", "당사자", m => esc(pname[m.party] || m.party)], ["party_key", "당사자 키", m => `<span class="mono">${esc(m.party_key)}</span>`],
      ["labels", "항목명", m => esc(m.labels.join(" · "))], ["forms", "서식", null, true]])}
    <h2>체크 보기 목록 <span class="muted">${d.n_options}개 속성 (서식 많은 순 ${d.options.length})</span></h2>
    <input type="text" id="op-q" placeholder="속성·보기 검색"><div id="op-list"></div>`;
  const draw = () => {
    const ql = $("#op-q").value.trim();
    $("#op-list").innerHTML = table(d.options.filter(o => !ql || o.attribute.includes(ql) || o.options.some(x => x.includes(ql))).slice(0, 150), [
      ["attribute", "속성", o => `<span class="mono">${esc(o.attribute)}</span>`], ["options", "보기", o => esc(o.options.slice(0, 12).join(" · "))],
      ["forms", "서식", null, true]]);
  };
  $("#op-q").oninput = draw;
  draw();
}

// ---------------------------------------------------------------------------
// 문서 분류: 대분류 → 문서 종류 → 실제 서식
// ---------------------------------------------------------------------------
async function docsTab() {
  const d = await api("/api/dictionary/doc_types");
  const f = store.get("dict.docs", { q: "", group: "" });
  $("#kd-body").innerHTML = `
    <div class="bar"><input type="text" id="dc-q" placeholder="문서 종류·다른 이름 검색" value="${esc(f.q)}">
      <select id="dc-g"><option value="">대분류 전체</option>${Object.entries(d.groups).map(([k, n]) => `<option value="${k}" ${k === f.group ? "selected" : ""}>${esc(n)}</option>`).join("")}</select>
      <span class="muted" id="dc-n"></span></div>
    <div class="split"><div id="dc-list" class="scroll"></div><div id="dc-edit" class="panel">문서 종류를 고르세요. 이름은 분류 문항의 정답, 다른 이름은 채점·서류 넣기에서 같은 것으로 봅니다.</div></div>`;
  const draw = () => {
    const ql = f.q.toLowerCase();
    const rows = Object.entries(d.types).filter(([id, t]) => (!f.group || t.group === f.group)
      && (!ql || id.includes(ql) || t.name.toLowerCase().includes(ql) || t.aliases.some(a => a.toLowerCase().includes(ql))));
    $("#dc-n").textContent = `${rows.length}종`;
    $("#dc-list").innerHTML = table(rows.slice(0, 300), [["id", "문서 종류", ([id, t]) => `<a href="#" data-doc="${esc(id)}">${esc(t.name)}</a> ${BY_TAG(t)}<div class="muted mono">${esc(id)}</div>`],
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
    <label>이름 (분류 정답) <input type="text" id="de-name" value="${esc(t.name)}" style="width:100%"></label>
    <label>대분류 <select id="de-g">${Object.entries(d.groups).map(([k, n]) => `<option value="${k}" ${k === t.group ? "selected" : ""}>${esc(n)}</option>`).join("")}</select></label>
    <label>다른 이름 (한 줄에 하나 — 영문 이름, 줄임말) <textarea id="de-al" rows="5" style="width:100%">${esc(t.aliases.join("\n"))}</textarea></label>
    <div>실제 서식: ${t.forms.map(f => `<a href="#/forms/${q(f)}" class="mono">${esc(f)}</a>`).join(" · ")}</div>
    <div class="bar"><button class="primary" id="de-save">저장</button></div>
    <div id="de-links" class="muted">연결 읽는 중…</div>`;
  api(`/api/dictionary/links/doc_type/${q(id)}`).then(l => {
    $("#de-links").innerHTML = `<div><b>쓰는 업무</b> ${l.tasks.map(t => `<span class="tag">${esc(t.name)}</span>`).join(" ") || "없음"}</div>
      <div><b>당사자 키</b> ${l.party_keys.length} (키 ${l.keys}) — 다른 문서 종류에도 나오는 순</div>
      <div>${l.party_keys.slice(0, 40).map(x => `<a href="#" class="mono" data-pk="${esc(x.party_key)}">${esc(x.party_key)}</a><span class="muted">(${x.doc_types})</span>`).join(" · ")}</div>
      <div id="de-pk"></div>`;
    $$("#de-links [data-pk]").forEach(a => a.onclick = e => { e.preventDefault(); showPartyKey(a.dataset.pk, $("#de-pk")); });
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
async function tasksTab() {
  const d = await api("/api/dictionary/tasks");
  const byGroup = {};
  for (const [id, t] of Object.entries(d.tasks)) (byGroup[t.group] = byGroup[t.group] || []).push([id, t]);
  $("#kd-body").innerHTML = `
    <div class="split"><div class="scroll tree">${Object.entries(d.groups).map(([g, n]) => `<div class="node"><b>${esc(n)}</b>
      <div class="kids">${(byGroup[g] || []).map(([id, t]) => `<div><a href="#" data-task="${esc(id)}">${esc(t.name)}</a> <span class="muted mono">${esc(id)}</span> ${BY_TAG(t)}</div>`).join("")}</div></div>`).join("")}</div>
      <div id="tk-edit" class="panel">업무를 고르세요. 다른 이름은 서류 넣기의 업무 폴더 이름을 알아볼 때, 역할 → 당사자는 이 업무 서류에서만 쓰는 당사자입니다.</div></div>`;
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
    <div><b>이 업무의 역할 → 당사자</b></div>
    <div id="te-roles">${[...roleRows, ["", "customer"]].map(([r, p]) => `<div class="bar te-row"><input type="text" value="${esc(r)}" placeholder="역할 (예: buyer)" class="mono"> → ${psel(p)}</div>`).join("")}</div>
    <div class="bar"><button class="primary" id="te-save">저장</button></div>
    <div id="te-links" class="muted">연결 읽는 중…</div>`;
  api(`/api/dictionary/links/task/${q(id)}`).then(l => {
    $("#te-links").innerHTML = `<div><b>필수 문서 종류</b> ${l.doc_types.map(d => `<span class="tag">${esc(d.name)}</span>`).join(" ")}</div>
      <div><b>서류끼리 겹치는 당사자 키 (대조 후보) ${l.shared.length}</b> — 같은 값이어야 하는 칸</div>
      ${table(l.shared.slice(0, 60), [["party_key", "당사자 키", x => `<span class="mono">${esc(x.party_key)}</span>`],
        ["names", "나오는 문서 종류", x => esc(x.names.join(" · "))], ["n", "수", x => x.doc_types.length, true]])}`;
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
// 합치기 후보
// ---------------------------------------------------------------------------
async function mergesTab() {
  const f = store.get("dict.merges", { dict: "", status: "proposed", q: "" });
  const DICT = { field: "필드 키", attribute: "속성", role: "역할", doc_type: "문서 종류", task: "업무" };
  const STATUS = { proposed: "후보", accepted: "합침", rejected: "안 합침" };
  $("#kd-body").innerHTML = `
    <div class="sub">합치면 왼쪽 이름은 오른쪽의 다른 이름이 됩니다(지우지 않음). 결정은 사전 풀이·시나리오·서류 넣기에 바로 쓰이고,
      생성 라벨의 키 이름 바꾸기(적용)는 평가 세트 버전을 올릴 때 합니다.</div>
    <div class="bar"><select id="mg-d"><option value="">사전 전체</option>${Object.entries(DICT).map(([k, n]) => `<option value="${k}" ${k === f.dict ? "selected" : ""}>${n}</option>`).join("")}</select>
      <select id="mg-s">${["", ...Object.keys(STATUS)].map(k => `<option value="${k}" ${k === f.status ? "selected" : ""}>${k ? STATUS[k] : "상태 전체"}</option>`).join("")}</select>
      <input type="text" id="mg-q" placeholder="이름·이유 검색" value="${esc(f.q)}"> <span class="muted" id="mg-n"></span></div>
    <div class="bar"><label><input type="checkbox" id="mg-all"> 보이는 것 모두</label>
      <button id="mg-acc" class="primary">합치기</button> <button id="mg-rej">안 합치기</button> <button id="mg-reset">후보로 되돌리기</button></div>
    <div id="mg-list"></div>`;
  let rows = [];
  const load = async () => {
    const r = await api(`/api/dictionary/merges?dict=${q(f.dict)}&status=${q(f.status)}&q=${q(f.q)}`);
    rows = r.items;
    $("#mg-n").textContent = `${r.total}건 · 후보 이유: ${Object.entries(r.counts.by_reason).map(([k, v]) => `${k} ${v}`).join(", ")}`;
    $("#mg-list").innerHTML = table(rows, [["sel", "", (m, i) => `<input type="checkbox" data-i="${i}">`],
      ["dict", "사전", m => DICT[m.dict] || m.dict], ["from", "이 이름을", m => `<span class="mono">${esc(m.from)}</span>`],
      ["into", "이 이름으로", m => `<span class="mono">${esc(m.into)}</span>`], ["reason", "이유", m => esc(m.reason) + (m.note ? `<div class="muted">${esc(m.note)}</div>` : "")],
      ["status", "상태", m => `<span class="tag ${m.status === "accepted" ? "ok" : ""}">${STATUS[m.status]}</span>${m.applied ? " 적용됨" : ""}`]]);
  };
  const act = async status => {
    const pick = $$("#mg-list [data-i]").filter(el => el.checked).map(el => rows[+el.dataset.i]);
    if (!pick.length) return toast("고른 후보가 없습니다", true);
    try { const r = await api("/api/dictionary/merges", { items: pick, status }); toast(`${r.changed}건`); load(); } catch (e) { toast(e.message, true); }
  };
  $("#mg-all").onchange = e => $$("#mg-list [data-i]").forEach(el => el.checked = e.target.checked);
  $("#mg-acc").onclick = () => act("accepted");
  $("#mg-rej").onclick = () => act("rejected");
  $("#mg-reset").onclick = () => act("proposed");
  for (const [id, k] of [["mg-d", "dict"], ["mg-s", "status"], ["mg-q", "q"]])
    $("#" + id).onchange = $("#" + id).oninput = e => { f[k] = e.target.value; store.set("dict.merges", f); load(); };
  load();
}

// ---------------------------------------------------------------------------
// 키 규칙 (docgen/key_rules.json): 표준 키의 값 종류·값 출처·동의어·overlay 항목명
// ---------------------------------------------------------------------------
function keysTab(d) {
  const f = store.get("keys.filter", { q: "", kind: "", only: "" });
  const kinds = d.kinds.map(k => k.name);
  $("#kd-body").innerHTML = `
    <div class="bar"><input type="text" id="kf-q" placeholder="키·항목명 검색" value="${esc(f.q)}">
      <select id="kf-kind"><option value="">값 종류 전체</option>${kinds.map(k => `<option ${k === f.kind ? "selected" : ""}>${esc(k)}</option>`).join("")}</select>
      <select id="kf-only">${[["", "모든 키"], ["rule", "사람이 정한 키만"], ["nosrc", "값 출처·종류 없는 사전 키"], ["sugg", "켜지 않은 항목명 제안 있음"]]
        .map(([v, n]) => `<option value="${v}" ${v === f.only ? "selected" : ""}>${n}</option>`).join("")}</select>
      <span class="muted" id="kf-n"></span> <button id="kf-new">새 표준 키</button></div>
    <div class="split"><div id="kf-list" class="scroll"></div><div id="kf-edit" class="panel">왼쪽에서 키를 고르세요.</div></div>`;
  const draw = () => {
    const q = f.q.toLowerCase();
    const rows = d.keys.filter(k => (!q || k.key.toLowerCase().includes(q) || k.labels.some(l => l.toLowerCase().includes(q))
        || (k.rule?.aliases || []).some(a => a.toLowerCase().includes(q)))
      && (!f.kind || k.rule?.kind === f.kind)
      && (f.only !== "rule" || k.rule || k.label_rules)
      && (f.only !== "nosrc" || (k.rule && !k.rule.kind && !k.rule.source))
      && (f.only !== "sugg" || (k.rule?.label_suggestions || []).length)).slice(0, 400);
    $("#kf-n").textContent = `${rows.length}${rows.length === 400 ? "+" : ""}개`;
    $("#kf-list").innerHTML = table(rows, [
      ["key", "키", k => `<a href="#" data-key="${esc(k.key)}" class="mono">${esc(k.key)}</a>`],
      ["labels", "항목명 예", k => esc(k.labels.slice(0, 3).join(" · "))],
      ["kind", "값 종류", k => k.rule?.kind ? `<span class="tag">${esc(k.rule.kind)}</span>` : (k.rule?.source ? `<span class="tag">출처</span>` : "")],
      ["forms", "서식", null, true],
      ["rule", "", k => (k.rule?.label_suggestions || []).length ? `<span class="tag warn" title="항목명 제안">제안</span>` : ""]]);
    $$("#kf-list [data-key]").forEach(a => a.onclick = e => { e.preventDefault(); editKey(d, d.keys.find(k => k.key === a.dataset.key)); });
  };
  for (const [id, k] of [["kf-q", "q"], ["kf-kind", "kind"], ["kf-only", "only"]])
    $("#" + id).oninput = e => { f[k] = e.target.value; store.set("keys.filter", f); draw(); };
  $("#kf-new").onclick = () => {
    const key = (prompt("새 표준 키 (영어 소문자, 역할.속성 — 예: foreign.bank_address)") || "").trim();
    if (key) editKey(d, { key, labels: [], forms: 0, rule: { meaning: "", aliases: [], labels: [] } });
  };
  draw();
}

async function editKey(d, k) {
  const r = k.rule || { meaning: "", aliases: [], labels: [] };
  const src = await api("/api/keyrules/sources");
  const box = $("#kf-edit");
  box.innerHTML = `
    <div><b class="mono">${esc(k.key)}</b> <span class="muted">서식 ${k.forms} · ${esc(k.type || "")}</span></div>
    ${k.labels.length ? `<div class="muted">항목명 예: ${esc(k.labels.join(" · "))}</div>` : ""}
    ${(k.label_rules || []).length ? `<div class="muted">항목명 규칙(코드에서 옮긴 것): <span class="mono">${esc(k.label_rules.join("  "))}</span></div>` : ""}
    <label>뜻 <input type="text" id="ke-meaning" value="${esc(r.meaning || "")}" style="width:100%"></label>
    <div class="bar"><label>값 종류 <select id="ke-kind"><option value="">(없음)</option>${d.kinds.map(x =>
      `<option value="${esc(x.name)}" ${x.name === r.kind ? "selected" : ""}>${esc(x.name)} — ${esc(x.meaning)}</option>`).join("")}</select></label></div>
    <div class="bar"><label>값 출처 <select id="ke-src"><option value="">(값 종류로 만듦)</option>${src.sources.map(s =>
      `<option value="${esc(s.path)}" ${s.path === r.source ? "selected" : ""}>${esc(s.path)} — ${esc(String(s.example).slice(0, 24))}</option>`).join("")}</select></label></div>
    <div id="ke-ex" class="muted"></div>
    <label>동의어 (외부 추출 키 이름, 쉼표) <input type="text" id="ke-alias" value="${esc((r.aliases || []).join(", "))}" style="width:100%"></label>
    <label>항목명 (overlay 서식, 쉼표) <input type="text" id="ke-labels" value="${esc((r.labels || []).join(", "))}" style="width:100%"></label>
    ${(r.label_suggestions || []).length ? `<div class="warnbox panel">항목명 제안: ${esc(r.label_suggestions.join(", "))}
      <button id="ke-sugg">항목명에 넣기</button><div class="muted">항목명을 켜면 그 항목명이 있는 overlay 서식의 생성 값이 바뀝니다 (평가 세트 버전을 올릴 때).</div></div>` : ""}
    <div class="bar"><button class="primary" id="ke-save">저장</button>${k.rule ? `<button id="ke-del">사전에서 빼기</button>` : ""}
      <span id="ke-msg" class="muted"></span></div>`;
  const split = s => s.split(",").map(x => x.trim()).filter(Boolean);
  const showEx = async () => {
    const kind = $("#ke-kind").value, source = $("#ke-src").value;
    if (!kind && !source) { $("#ke-ex").textContent = ""; return; }
    const ex = await api("/api/keyrules/examples", source ? { definition: { how: "source", source }, n: 6 } : { kind, n: 6 });
    $("#ke-ex").textContent = "예시 값: " + ex.examples.map(v => v ?? "(빈 칸)").join(" · ");
  };
  $("#ke-kind").onchange = showEx;
  $("#ke-src").onchange = showEx;
  showEx();
  if ($("#ke-sugg")) $("#ke-sugg").onclick = () => {
    $("#ke-labels").value = [...new Set([...split($("#ke-labels").value), ...r.label_suggestions])].join(", ");
  };
  $("#ke-save").onclick = async () => {
    try {
      const res = await api(`/api/keyrules/keys/${q(k.key)}`, { meaning: $("#ke-meaning").value, kind: $("#ke-kind").value || null,
        source: $("#ke-src").value || null, aliases: split($("#ke-alias").value), labels: split($("#ke-labels").value) }, "PUT");
      toast(res.affected.length ? `저장 — 항목명이 바뀌어 overlay 서식 ${res.affected.length}종의 생성 값이 바뀝니다 (${res.affected.slice(0, 5).join(", ")}…)` : "저장");
      viewKeys("keys");
    } catch (e) { toast(e.message, true); }
  };
  if ($("#ke-del")) $("#ke-del").onclick = async () => {
    if (!confirm(`${k.key} 를 사전에서 뺄까요? (자동 키 목록에는 남습니다)`)) return;
    try { await api(`/api/keyrules/keys/${q(k.key)}`, undefined, "DELETE"); viewKeys("keys"); } catch (e) { toast(e.message, true); }
  };
}

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
