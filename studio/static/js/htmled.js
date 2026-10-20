// ① 서식 › html 편집: 화면에서 만든 html 서식(복제·분석기)의 템플릿과 form.json 을 고치고 바로 렌더링해 본다.
// 원본 그림 겹쳐 보기, 행 수 최소·최대, 저장 전 검사, 분석기에 다시 고쳐. 서버: studio/api_html.py, 생성기: docgen/htmlform.py
"use strict";

async function viewHtmlEditor(d) {
  const src = await api(`/api/forms/${q(d.id)}/html`);
  const prov = (await api("/api/providers")).providers;
  const he = {
    d, src, tab: "template", template: src.template, formText: JSON.stringify(src.form, null, 1), label: null, page: 0,
    rows: store.get("he.rows", "auto"), seed: 0, overlay: false, opacity: 0.45, dirty: false,
  };
  $("#tab").innerHTML = `
    <div class="bar">
      <button data-he="template" class="primary">템플릿</button><button data-he="form">form.json</button>
      <span class="sep"></span>
      <label>seed <input type="number" id="he-seed" value="0" min="0"></label>
      <label>행 수 <select id="he-rows"><option value="auto">서식대로</option><option value="min">최소</option><option value="max">최대</option></select></label>
      <button class="primary" id="he-run" title="Ctrl+Enter">미리보기</button>
      ${src.has_source ? `<label><input type="checkbox" id="he-ov"> 원본 겹쳐 보기</label>
        <input type="range" id="he-op" min="0.1" max="0.9" step="0.05" value="0.45" style="width:90px">` : ""}
      <span style="flex:1"></span>
      <span class="muted" id="he-state">저장됨</span>
      <button id="he-save" title="Ctrl+S">저장</button>
    </div>
    <div class="he-grid">
      <div>
        <textarea id="he-text" class="mono he-text" spellcheck="false"></textarea>
        <div class="muted he-help">값은 <span class="mono">{{ f("키", label="항목명") }}</span>, 반복 행은
          <span class="mono">{% for r in d.rows %} … f("rows." ~ loop.index0 ~ ".date") {% endfor %}</span>. 값 출처·반복 행 수는 form.json.
          미리보기의 박스를 누르면 템플릿에서 그 키를 찾습니다.</div>
        <div class="panel" style="margin-top:8px">
          <b>분석기에 다시 고쳐</b>
          ${src.has_source ? `<div class="bar" style="margin:6px 0">
            <select id="he-prov">${prov.map(p => `<option value="${esc(p.name)}">${esc(p.name)} (${p.kind}${p.external ? ", 외부" : ""})</option>`).join("")}</select>
            <input type="text" id="he-comment" placeholder="고칠 점 (예: 표 열 너비를 원본처럼, 합계 행 추가)" style="flex:1">
            <button id="he-redo" ${prov.length ? "" : "disabled"}>맡기기</button></div>
            <div class="muted">지금 편집 중인 템플릿·form.json 과 원본 그림, 의견을 함께 보냅니다. 결과는 ⑧ 작업에서 보고 승인하면 이 서식이 바뀝니다.
              ${prov.length ? "" : "설정에 분석기(providers)가 없습니다."}</div>`
            : `<div class="muted">원본 그림이 없는 서식(코드 서식을 복제한 것)은 분석기에 맡기지 않습니다.</div>`}
        </div>
      </div>
      <div>
        <div class="pages" id="he-pages"></div>
        <div class="stage he-stage" id="he-stage"><p class="muted" style="padding:20px">미리보기를 누르세요</p></div>
        <div class="panel" id="he-checks" style="margin-top:8px"></div>
      </div>
    </div>`;
  $("#he-rows").value = he.rows;
  const ta = $("#he-text");
  const showTab = () => {
    ta.value = he.tab === "template" ? he.template : he.formText;
    $$("[data-he]").forEach(b => b.classList.toggle("primary", b.dataset.he === he.tab));
  };
  ta.oninput = () => {
    if (he.tab === "template") he.template = ta.value; else he.formText = ta.value;
    he.dirty = true; $("#he-state").textContent = "고침 (저장 안 함)";
  };
  ta.onkeydown = e => {   // Tab 은 들여쓰기
    if (e.key === "Tab") { e.preventDefault(); const s = ta.selectionStart; ta.setRangeText("  ", s, ta.selectionEnd, "end"); ta.oninput(); }
  };
  $$("[data-he]").forEach(b => b.onclick = () => { he.tab = b.dataset.he; showTab(); });
  $("#he-rows").onchange = () => { he.rows = $("#he-rows").value; store.set("he.rows", he.rows); heRender(he); };
  $("#he-seed").onchange = () => { he.seed = Math.max(0, +$("#he-seed").value || 0); heRender(he); };
  $("#he-run").onclick = () => heRender(he);
  $("#he-save").onclick = () => heSave(he);
  if ($("#he-ov")) {
    $("#he-ov").onchange = () => { he.overlay = $("#he-ov").checked; heDraw(he); };
    $("#he-op").oninput = () => { he.opacity = +$("#he-op").value; heDraw(he); };
  }
  if ($("#he-redo")) $("#he-redo").onclick = () => heRedo(he);
  state.keyHandler = e => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") { e.preventDefault(); heSave(he); }
    else if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); heRender(he); }
  };
  state.leave = unload => !he.dirty || (unload ? false : confirm("저장하지 않은 html 서식 수정이 있습니다. 버릴까요?"));
  showTab();
  heRender(he);
}

function heForm(he) {
  try { return JSON.parse(he.formText); } catch (e) { throw new Error(`form.json 이 JSON 이 아닙니다: ${e.message}`); }
}

async function heRender(he) {
  let form;
  try { form = heForm(he); } catch (e) { return toast(e.message, true); }
  $("#he-stage").innerHTML = `<p class="spin" style="padding:20px">렌더링 중…</p>`;
  try {
    he.label = await api(`/api/forms/${q(he.d.id)}/html/render`, { template: he.template, form, seed: he.seed, rows: he.rows });
    if (!$("#he-stage")) return;   // 그사이 다른 화면으로 갔으면 그만
    he.page = Math.min(he.page, he.label.images.length - 1);
    heDraw(he);
  } catch (e) {
    if (!$("#he-stage")) return;
    $("#he-stage").innerHTML = `<p class="err" style="padding:12px">${esc(e.message)}</p>`;
    $("#he-checks").innerHTML = "";
  }
}

function heDraw(he) {
  const L = he.label;
  if (!L || !$("#he-stage")) return;
  $("#he-pages").innerHTML = L.images.length > 1 ? L.images.map((_, i) =>
    `<button data-pg="${i}" class="${i === he.page ? "primary" : ""}">${i + 1}쪽</button>`).join("") + `<span class="muted"> ${L.images.length}쪽</span>` : "";
  $$("[data-pg]").forEach(b => b.onclick = () => { he.page = +b.dataset.pg; heDraw(he); });
  const stage = $("#he-stage");
  stage.innerHTML = stageHTML(L, he.page, -1) + (he.overlay && he.page === 0
    ? `<img class="he-src" src="/api/forms/${q(he.d.id)}/source-image" style="opacity:${he.opacity}" alt="">` : "");
  if (!stage.dataset.bound) {
    stage.dataset.bound = "1";
    bindStage(stage, () => he.label, () => he.page, i => { if (i >= 0) heFind(he, he.label.fields[i].key); });
  }
  const checks = L.checks || [];
  const empty = L.fields.filter(f => f.type !== "seal" && f.type !== "signature" && (f.value === null || f.value === "")).length;
  $("#he-checks").innerHTML = `<b>검사</b> <span class="muted">${L.images.length}쪽 · 항목 ${L.fields.length} · 빈 값 ${empty} · 행 수 ${esc(L.rows || "auto")}${L.overflow ? " · <span class='err'>쪽 넘침</span>" : ""}</span>
    ${checks.length ? `<ul class="checks">${checks.map(c => `<li class="warn">⚠ ${esc(c.text)}</li>`).join("")}</ul>` : `<div class="muted">경고 없음</div>`}`;
}

function heFind(he, key) {   // 미리보기에서 누른 키를 템플릿에서 찾는다 (반복 행은 rows.3.date → rows. ~ … .date)
  if (he.tab !== "template") { he.tab = "template"; $("#he-text").value = he.template; $$("[data-he]").forEach(b => b.classList.toggle("primary", b.dataset.he === "template")); }
  const ta = $("#he-text");
  const m = key.match(/^(.*?)\.\d+\.(.+)$/);
  const needles = m ? [`"${m[1]}." ~`, `.${m[2]}"`] : [`"${key}"`];
  let at = -1;
  for (const n of needles) { at = ta.value.indexOf(n); if (at >= 0) break; }
  if (at < 0) return toast(`템플릿에서 ${key} 를 찾지 못했습니다 (부모 서식 쪽에서 나온 값일 수 있습니다)`);
  ta.focus();
  ta.setSelectionRange(at, at + needles[0].length);
  const line = ta.value.slice(0, at).split("\n").length;
  ta.scrollTop = Math.max(0, (line - 5) * parseFloat(getComputedStyle(ta).lineHeight || "16"));
}

async function heSave(he) {
  let form;
  try { form = heForm(he); } catch (e) { return toast(e.message, true); }
  try {
    await api(`/api/forms/${q(he.d.id)}/html`, { template: he.template, form }, "PUT");
    he.dirty = false; $("#he-state").textContent = "저장됨";
    toast("저장했습니다. 이 서식은 검수 전 상태입니다 (① 서식 › 검수)");
    state.forms = null;
  } catch (e) { toast(e.message, true); }
}

async function heRedo(he) {
  let form;
  try { form = heForm(he); } catch (e) { return toast(e.message, true); }
  const p = $("#he-prov").value;
  try {
    const r = await api(`/api/forms/${q(he.d.id)}/html/redo`, { provider: p, comment: $("#he-comment").value, template: he.template, form });
    toast("분석기에 맡겼습니다 (⑧ 작업)");
    location.hash = `#/jobs/analyzer/${q(r.analyzer)}`;
  } catch (e) { toast(e.message, true); }
}
