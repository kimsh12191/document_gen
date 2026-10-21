// 키 사전: 표준 키의 뜻·값 종류·값 출처·동의어(추출 키)·항목명, 값 종류(코드·데이터), 이름 두 벌. 설계: studio/DESIGN.md 15.7
// 사람이 정하는 부분은 docgen/key_rules.json, 자동으로 모은 키 목록은 docgen/keys.json. 서버: studio/api_keys.py, docgen/keyrules.py
"use strict";

addRoute(/^#\/keys(?:\/(\w+))?$/, tab => viewKeys(tab || "keys"), "keys");

const KEY_TABS = [["keys", "키"], ["kinds", "값 종류"], ["dups", "이름 두 벌"]];
const HOW_NAME = { code: "코드", source: "프로필 값", choices: "목록", pattern: "틀" };

async function viewKeys(tab) {
  const d = await api("/api/keyrules");
  main().innerHTML = `
    <h1>키 사전</h1>
    <div class="sub">서식·추출 결과의 키를 표준 키로 맞추고, 키마다 어떤 값을 넣을지(값 종류·값 출처) 정합니다. 저장하면 다음 렌더링·빌드부터 반영됩니다.
      서류 넣기에서 모르는 추출 키는 동의어로 이 사전에 이어집니다.</div>
    <div class="sub">키 ${d.counts.keys.toLocaleString()} · 사람이 정한 키 ${d.counts.rules} · 이름 두 벌 ${d.duplicates.length} (미결 ${d.counts.dup_open})</div>
    <div class="tabs">${KEY_TABS.map(([k, n]) => `<a href="#/keys/${k}" class="${k === tab ? "on" : ""}">${n}</a>`).join("")}</div>
    <div id="kd-body"></div>`;
  ({ keys: keysTab, kinds: kindsTab, dups: dupsTab })[tab](d);
}

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

function dupsTab(d) {
  $("#kd-body").innerHTML = `<div class="sub">같은 뜻인데 이름이 두 벌인 키입니다. 결정만 적어 두고, 실제 이름 바꾸기는 생성 결과가 바뀌므로 평가 세트 버전을 올릴 때 합니다 (DESIGN.md 5.3).</div>
    ${table(d.duplicates, [
      ["keys", "키", x => x.keys.map(k => `<div class="mono">${esc(k)}</div>`).join("")], ["meaning", "뜻"], ["where", "어디서", x => `<div class="muted">${esc(x.where)}</div>`],
      ["proposal", "제안"],
      ["decision", "결정", (x, i) => `<input type="text" data-dup="${i}" value="${esc(x.decision || "")}" placeholder="미결" style="width:220px">`]])}
    <div class="bar"><button class="primary" id="dp-save">결정 저장</button></div>`;
  $("#dp-save").onclick = async () => {
    try {
      for (const el of $$("[data-dup]")) {
        const x = d.duplicates[+el.dataset.dup];
        if ((x.decision || "") !== el.value.trim()) await api("/api/keyrules/duplicates", { keys: x.keys, decision: el.value.trim() || null }, "PUT");
      }
      toast("저장"); viewKeys("dups");
    } catch (e) { toast(e.message, true); }
  };
}
