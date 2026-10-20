// ⑥ 데이터셋 › 새로 만들기: 레시피(datasets/recipes/<이름>.json) 편집과 빌드 시작. 레시피 형식: studio/bank_data.py
"use strict";

addRoute(/^#\/recipes\/([^/]+)$/, name => viewRecipe(decodeURIComponent(name)), "datasets");

let recipeOpts = null;

async function recipesPanel() {
  const [r, opts] = await Promise.all([api("/api/recipes"), recipeOpts || api("/api/recipes/options")]);
  recipeOpts = opts;
  const tpl = Object.entries(opts.templates);
  return `
    <div class="panel" style="margin-bottom:12px">
      <b>새로 만들기</b> <span class="muted">레시피로 데이터셋을 만듭니다. 명령줄 <span class="mono">python -m docgen.bench build --recipe …</span>과 같은 결과입니다.</span>
      ${r.recipes.length ? table(r.recipes, [
        ["name", "레시피", x => `<a href="#/recipes/${encodeURIComponent(x.name)}">${esc(x.name)}</a>`],
        ["track", "벤치마크", x => esc(TRACK_NAME[x.track || "bank"])], ["split", "용도", x => x.split === "train" ? "학습 데이터" : "평가 세트"],
        ["about", "설명"],
        ["go", "", x => `<input type="text" data-outname="${esc(x.name)}" value="${esc(x.name)}-${new Date().toISOString().slice(0, 10)}" style="width:200px">
          <label>프로세스 <input type="number" data-workers="${esc(x.name)}" value="4" min="1" max="32" style="width:52px"></label>
          <button class="primary" data-build="${esc(x.name)}">만들기</button>`]]) : `<p class="muted">레시피가 없습니다. 아래 틀에서 시작하세요.</p>`}
      <div class="bar" style="margin-top:6px"><span class="muted">틀에서 새 레시피:</span>
        ${tpl.map(([k, t]) => `<button data-tpl="${esc(k)}" title="${esc(t.about)}">${esc(k)}</button>`).join("")}
        <span class="muted">· OCR 레시피는 5단계</span></div>
    </div>`;
}

function bindRecipesPanel() {
  $$("[data-tpl]").forEach(b => b.onclick = async () => {
    const name = prompt("새 레시피 이름 (영어·숫자·-)", b.dataset.tpl);
    if (!name) return;
    try { await api(`/api/recipes/${encodeURIComponent(name)}`, recipeOpts.templates[b.dataset.tpl], "PUT"); location.hash = `#/recipes/${encodeURIComponent(name)}`; }
    catch (e) { toast(e.message, true); }
  });
  $$("[data-build]").forEach(b => b.onclick = async () => {
    const name = b.dataset.build;
    try {
      const j = await api("/api/builds", { recipe: name, name: $(`[data-outname="${name}"]`).value.trim(), workers: +$(`[data-workers="${name}"]`).value || 1 });
      location.hash = `#/jobs/${encodeURIComponent(j.id)}`;
    } catch (e) { toast(e.message, true); }
  });
}

async function viewRecipe(name) {
  const [r, opts] = await Promise.all([api(`/api/recipes/${encodeURIComponent(name)}`), recipeOpts || api("/api/recipes/options")]);
  recipeOpts = opts;
  const b = { ...opts.bundle_defaults, ...(r.bundle || {}) };
  const conds = r.conditions || opts.conditions;
  const scs = r.scenarios === "all" || !r.scenarios ? opts.scenarios.map(s => s.id) : r.scenarios;
  const bundlesN = typeof r.bundles === "object" ? r.bundles : { default: r.bundles ?? 4 };
  const num = (id, v, step = 0.01) => `<input type="number" id="${id}" value="${v}" step="${step}" min="0" style="width:72px">`;
  main().innerHTML = `
    <div class="muted"><a href="#/datasets">데이터셋</a> › 레시피</div>
    <h1>${esc(name)} <span class="muted mono" style="font-size:13px">datasets/recipes/${esc(name)}.json</span></h1>
    <div class="bar"><button class="primary" id="rc-save">저장</button><button id="rc-raw">JSON 으로 보기·고치기</button>
      <button id="rc-del">지우기</button><span class="muted">평가 세트 버전 ${esc(opts.version)}</span></div>
    <div class="rc-grid">
      <div class="panel"><b>무엇을</b>
        <label class="fld">설명 <input type="text" id="rc-about" value="${esc(r.about || "")}"></label>
        <label class="fld">용도 <select id="rc-split"><option value="test">평가 세트 (test)</option><option value="train" ${r.split === "train" ? "selected" : ""}>학습 데이터 (train: 평가 세트와 seed 가 겹치지 않음, ms-swift 학습 레코드도)</option></select></label>
        <label class="fld">단일 서류 과제에 쓸 서식 (all · 서식 ID · 그룹, 쉼표로) <input type="text" id="rc-types" value="${esc(Array.isArray(r.types) ? r.types.join(",") : r.types || "all")}"></label>
        <label class="fld">서식마다 샘플 수 <input type="number" id="rc-perdoc" value="${r.per_doc ?? 1}" min="0"></label>
        <label class="fld">빼는 서식 (쉼표) <input type="text" id="rc-exclude" value="${esc((r.exclude || []).join(","))}"></label>
        <label><input type="checkbox" id="rc-reviewed" ${r.reviewed_only ? "checked" : ""}> 검수 완료 서식만 (평가 세트 권장)</label>
        <label class="fld">서류마다 값 칸 OCR 문항 수 <input type="number" id="rc-fpd" value="${r.fields_per_doc ?? 6}" min="0"></label>
        <label class="fld">kie·marks 문항 하나의 최대 항목 수 <input type="number" id="rc-maxkeys" value="${r.max_keys ?? 40}" min="1"></label>
        <label class="fld">seed 시작 (학습 데이터를 더 만들 때 앞의 묶음 수만큼) <input type="number" id="rc-start" value="${r.start ?? 0}" min="0"></label>
      </div>
      <div class="panel"><b>촬영 조건 비율</b> <span class="muted">합 1</span>
        <div class="bar">${Object.keys(opts.conditions).map(c => `<label>${esc(COND_NAME[c] || c)} ${num(`rc-c-${c}`, conds[c] ?? 0)}</label>`).join("")}</div>
        <b>업무 묶음 규칙</b>
        <div class="bar"><label>빠진 서류 0건 ${num("rc-m0", b.missing[0])}</label><label>1건 ${num("rc-m1", b.missing[1])}</label><label>2건 ${num("rc-m2", b.missing[2])}</label></div>
        <div class="bar"><label>타인 서류 ${num("rc-other", b.other_customer)}</label><label>불필요 서류 ${num("rc-extra", b.extra_doc)}</label>
          <label>대조 변조 ${num("rc-tamper", b.tamper)}</label></div>
        <b>시나리오와 고객 묶음 수</b> <label class="muted">기본 ${num("rc-bdefault", bundlesN.default ?? 4, 1)}</label>
        <div class="rc-scs">${opts.scenarios.map(s => `<label><input type="checkbox" data-sc="${esc(s.id)}" ${scs.includes(s.id) ? "checked" : ""}> ${esc(s.name)}
          <input type="number" data-scn="${esc(s.id)}" value="${bundlesN[s.id] ?? ""}" placeholder="기본" min="0" style="width:60px"></label>`).join("")}</div>
      </div>
      <div class="panel"><b>대조 사례</b> <span class="muted">켜기·변조 비율 (비우면 위의 대조 변조)</span>
        ${table(opts.cases, [["id", "사례", c => `<label title="${esc(c.basis)}"><input type="checkbox" data-case="${esc(c.id)}" ${(r.cases || {})[c.id]?.enabled === false ? "" : "checked"}> ${esc(c.title)}</label>`],
          ["category", "분류"], ["t", "변조", c => c.category === "format" ? `<span class="muted">늘 정상</span>` :
            `<input type="number" data-ctamper="${esc(c.id)}" value="${(r.cases || {})[c.id]?.tamper ?? ""}" step="0.05" min="0" max="1" style="width:64px" placeholder="기본">`]])}
      </div>
      <div class="panel"><b>직접 만든 묶음</b> <span class="muted">시나리오·고객 seed 와 뺄 서류·타인 서류·불필요 서류·사례·변조를 정해 특정 상황의 묶음을 만듭니다 (JSON 목록)</span>
        <textarea id="rc-custom" rows="8" class="mono" style="width:100%">${esc(JSON.stringify(r.custom_bundles || [], null, 1))}</textarea>
        <div class="muted" style="font-size:12px">예: [{"scenario": "jeonse_loan", "seed": 2002000, "name": "owner_mismatch", "missing": [], "other": [], "extra": [],
          "cases": ["lease_owner"], "tamper": {"lease_owner": true}}] · name 을 "" 로 두면 같은 seed 의 보통 묶음을 그대로 다시 만듭니다.</div>
      </div>
    </div>
    <div id="rc-rawbox" style="display:none"><textarea id="rc-json" rows="24" class="mono" style="width:100%"></textarea>
      <button id="rc-rawsave">JSON 저장</button></div>`;
  const collect = () => {
    const out = { about: $("#rc-about").value.trim(), track: "bank", split: $("#rc-split").value };
    const types = $("#rc-types").value.trim();
    out.types = !types || types === "all" ? "all" : types.split(",").map(s => s.trim()).filter(Boolean);
    out.per_doc = +$("#rc-perdoc").value; out.fields_per_doc = +$("#rc-fpd").value; out.max_keys = +$("#rc-maxkeys").value;
    out.start = +$("#rc-start").value;
    const ex = $("#rc-exclude").value.split(",").map(s => s.trim()).filter(Boolean);
    if (ex.length) out.exclude = ex;
    if ($("#rc-reviewed").checked) out.reviewed_only = true;
    out.conditions = Object.fromEntries(Object.keys(opts.conditions).map(c => [c, +$(`#rc-c-${c}`).value]).filter(([, v]) => v > 0));
    out.bundle = { missing: [+$("#rc-m0").value, +$("#rc-m1").value, +$("#rc-m2").value], other_customer: +$("#rc-other").value,
      extra_doc: +$("#rc-extra").value, tamper: +$("#rc-tamper").value };
    const sel = $$("[data-sc]").filter(x => x.checked).map(x => x.dataset.sc);
    out.scenarios = sel.length === opts.scenarios.length ? "all" : sel;
    const bn = { default: +$("#rc-bdefault").value };
    $$("[data-scn]").forEach(x => { if (x.value !== "") bn[x.dataset.scn] = +x.value; });
    out.bundles = Object.keys(bn).length === 1 ? bn.default : bn;
    const cases = {};
    for (const c of opts.cases) {
      const en = $(`[data-case="${c.id}"]`).checked, t = $(`[data-ctamper="${c.id}"]`)?.value;
      if (!en) cases[c.id] = { enabled: false };
      else if (t !== undefined && t !== "") cases[c.id] = { tamper: +t };
    }
    if (Object.keys(cases).length) out.cases = cases;
    const custom = JSON.parse($("#rc-custom").value || "[]");
    if (custom.length) out.custom_bundles = custom;
    return out;
  };
  const save = async body => {
    try { await api(`/api/recipes/${encodeURIComponent(name)}`, body, "PUT"); toast("저장했습니다"); viewRecipe(name); }
    catch (e) { toast(e.message, true); }
  };
  $("#rc-save").onclick = () => { try { save(collect()); } catch (e) { toast(`직접 만든 묶음 JSON: ${e.message}`, true); } };
  $("#rc-raw").onclick = () => { $("#rc-rawbox").style.display = "block"; $("#rc-json").value = JSON.stringify(r, null, 1); };
  $("#rc-rawsave").onclick = () => { try { save(JSON.parse($("#rc-json").value)); } catch (e) { toast(e.message, true); } };
  $("#rc-del").onclick = async () => { if (confirm("레시피를 지울까요? (만든 데이터셋은 그대로)")) { await api(`/api/recipes/${encodeURIComponent(name)}`, undefined, "DELETE"); location.hash = "#/datasets"; } };
}
