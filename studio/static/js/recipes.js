// ⑥ 데이터셋 › 새로 만들기: 레시피(docgen/recipes/<이름>.json) 편집과 빌드 시작 (은행 서류·합성 OCR).
// 레시피 형식: studio/bank_data.py (은행 서류), docgen/ocr_set.py (OCR). 서버: studio/api_bank.py (/api/recipes, /api/builds)
"use strict";

addRoute(/^#\/recipes\/([^/]+)$/, name => viewRecipe(decodeURIComponent(name)), "datasets");

let recipeOpts = null;

async function recipesPanel() {
  const [r, opts] = await Promise.all([api("/api/recipes"), recipeOpts || api("/api/recipes/options")]);
  recipeOpts = opts;
  const tpl = Object.entries(opts.templates);
  return `
    <div class="panel" style="margin-bottom:12px">
      <b>새로 만들기</b> <span class="muted">레시피로 생성합니다. 완료하면 아래 등록 목록에 자동으로 추가됩니다. 폴더를 다시 등록할 필요가 없습니다.</span>
      ${r.recipes.length ? table(r.recipes, [
        ["name", "레시피", x => `<a href="#/recipes/${encodeURIComponent(x.name)}">${esc(x.name)}</a>`],
        ["track", "만드는 과제", x => x.track === "ocr" ? "쪽 OCR 8과제" : "문서 이해"], ["split", "용도", x => x.split === "train" ? "학습 데이터" : "평가 세트"],
        ["about", "설명"],
        ["go", "", x => `<input type="text" data-outname="${esc(x.name)}" value="${esc(x.name)}-${new Date().toISOString().slice(0, 10)}" style="width:200px" required>
          <label>프로세스 <input type="number" data-workers="${esc(x.name)}" value="4" min="1" max="32" style="width:52px" required></label>
          <button class="primary" data-build="${esc(x.name)}">만들기</button>`]]) : `<p class="muted">레시피가 없습니다. 아래 틀에서 시작하세요.</p>`}
      <div class="bar" style="margin-top:6px"><span class="muted">틀에서 새 레시피:</span>
        ${tpl.map(([k, t]) => `<button data-tpl="${esc(k)}" title="${esc(t.about)}">${esc(k)}</button>`).join("")}
        <span class="muted">(bank-* 서류 과제 · ocr-* 합성 쪽 OCR 8과제: 쪽 전체 글자 정답, 같은 과제 폴더 형식)</span></div>
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
    const output = $(`[data-outname="${name}"]`), workers = $(`[data-workers="${name}"]`);
    if (!output.reportValidity() || !workers.reportValidity()) return;
    b.disabled = true;
    try {
      const j = await api("/api/builds", { recipe: name, name: output.value.trim(), workers: +workers.value });
      datasetBuildStarted(j);
    } catch (e) { toast(e.message, true); }
    finally { if (b.isConnected) b.disabled = false; }
  });
}

async function viewRecipe(name) {
  const [r, opts] = await Promise.all([api(`/api/recipes/${encodeURIComponent(name)}`), recipeOpts || api("/api/recipes/options")]);
  recipeOpts = opts;
  if (r.track === "ocr") return viewOcrRecipe(name, r, opts);
  const conds = r.conditions || opts.conditions;
  const num = (id, v, step = 0.01) => `<input type="number" id="${id}" value="${v}" step="${step}" min="0" style="width:72px">`;
  main().innerHTML = `
    <div class="muted"><a href="#/datasets">데이터셋</a> › 레시피</div>
    <h1>${esc(name)} <span class="muted mono" style="font-size:13px">docgen/recipes/${esc(name)}.json</span></h1>
    <div class="bar"><button class="primary" id="rc-save">저장</button><button id="rc-raw">JSON 으로 보기·고치기</button>
      <button id="rc-del">지우기</button><span class="muted">평가 세트 버전 ${esc(opts.version)}</span></div>
    ${["bank-bench", "bank-train", "ocr-bench", "ocr-train"].includes(name) ? `<div class="warnbox panel" style="font-size:13px;margin:4px 0">기본 레시피입니다. 저장하면 저장소 파일 <span class="mono">docgen/recipes/${esc(name)}.json</span> 이 바뀌고, 다음에 이 레시피로 만드는 평가 세트·학습 데이터가 모두 달라집니다. 시험이나 다른 설정은 <a href="#/datasets">데이터셋</a> › <b>틀에서 새 레시피</b>로 따로 만드세요 (<span class="mono">bank-try</span> = 몇 분짜리 시험).</div>` : ""}
    <div class="muted" style="font-size:12px;margin:4px 0">서식 문항(분류·정보 추출·체크·기타 칸 정리·값 칸 OCR·표 추출·표 질의)은 늘 같이 만들어집니다. 일부 서류는 값 칸을 검은 상자로 가리고 용도·비고 같은 칸을 비워(정답 null) "없으면 null" 을 배우게 합니다 (레시피 nulls). 학습에 어떤 과제를 얼마나 쓸지는 학습 설정 task_mix 로 정합니다. 기타 칸 정리: 원본 서식의 비고·기타·사유 칸 일부에 일부러 대충 쓴 글을 넣고 DB 칸으로 정리한 것이 정답.</div>
    <div class="rc-grid">
      <div class="panel"><b>무엇을</b>
        <label class="fld">설명 <input type="text" id="rc-about" value="${esc(r.about || "")}"></label>
        <label class="fld">용도 <select id="rc-split"><option value="test">평가 세트 (test)</option><option value="train" ${r.split === "train" ? "selected" : ""}>학습 데이터 (train: 평가 세트와 seed 가 겹치지 않음, ms-swift 학습 레코드도)</option></select></label>
        <label class="fld">쓸 서식 (all · 서식 ID · 그룹, 쉼표로) <input type="text" id="rc-types" value="${esc(Array.isArray(r.types) ? r.types.join(",") : r.types || "all")}"></label>
        ${formPickButton("rc-types", "쓸 서식")}
        <label class="fld">서식마다 샘플 수 <input type="number" id="rc-perdoc" value="${r.per_doc ?? 1}" min="0"></label>
        <label class="fld">빼는 서식 (쉼표) <input type="text" id="rc-exclude" value="${esc((r.exclude || []).join(","))}"></label>
        ${formPickButton("rc-exclude", "뺄 서식")}
        <label><input type="checkbox" id="rc-reviewed" ${r.reviewed_only ? "checked" : ""}> 검수 완료 서식만 (평가 세트 권장)</label>
        <label class="fld">서류마다 값 칸 OCR 문항 수 <input type="number" id="rc-fpd" value="${r.fields_per_doc ?? 6}" min="0"></label>
        <label class="fld">kie·marks 문항 하나의 최대 항목 수 <input type="number" id="rc-maxkeys" value="${r.max_keys ?? 40}" min="1"></label>
        <label class="fld">seed 시작 (학습 데이터를 더 만들 때 앞에서 만든 서식마다 샘플 수만큼) <input type="number" id="rc-start" value="${r.start ?? 0}" min="0"></label>
      </div>
      <div class="panel"><b>촬영 조건 비율</b> <span class="muted">합 1</span>
        <div class="bar">${Object.keys(opts.conditions).map(c => `<label>${esc(COND_NAME[c] || c)} ${num(`rc-c-${c}`, conds[c] ?? 0)}</label>`).join("")}</div>
      </div>
    </div>
    <div id="rc-rawbox" style="display:none"><textarea id="rc-json" rows="24" class="mono" style="width:100%"></textarea>
      <button id="rc-rawsave">JSON 저장</button></div>`;
  bindFormPickers();
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
    return out;
  };
  const save = async body => {
    try { await api(`/api/recipes/${encodeURIComponent(name)}`, body, "PUT"); toast("저장했습니다"); viewRecipe(name); }
    catch (e) { toast(e.message, true); }
  };
  $("#rc-save").onclick = () => { try { save(collect()); } catch (e) { toast(e.message, true); } };
  $("#rc-raw").onclick = () => { $("#rc-rawbox").style.display = "block"; $("#rc-json").value = JSON.stringify(r, null, 1); };
  $("#rc-rawsave").onclick = () => { try { save(JSON.parse($("#rc-json").value)); } catch (e) { toast(e.message, true); } };
  $("#rc-del").onclick = async () => { if (confirm("레시피를 지울까요? (만든 데이터셋은 그대로)")) { await api(`/api/recipes/${encodeURIComponent(name)}`, undefined, "DELETE"); location.hash = "#/datasets"; } };
}


// 합성 OCR 레시피 (docgen/ocr_set.py) ------------------------------------------
function viewOcrRecipe(name, r, opts) {
  const conds = r.conditions || opts.conditions;
  const num = (id, v, step = 0.01) => `<input type="number" id="${id}" value="${v}" step="${step}" min="0" style="width:72px">`;
  const sel = (id, cur) => `<select id="${id}">${["default", "on", "off"].map(v => `<option value="${v}" ${v === (cur || "default") ? "selected" : ""}>${MODE_NAME[v]}</option>`).join("")}</select>`;
  main().innerHTML = `
    <div class="muted"><a href="#/datasets">데이터셋</a> › 레시피 (합성 OCR)</div>
    <h1>${esc(name)} <span class="muted mono" style="font-size:13px">docgen/recipes/${esc(name)}.json</span></h1>
    <div class="bar"><button class="primary" id="rc-save">저장</button><button id="rc-del">지우기</button>
      <span class="muted">python -m docgen.ocr_set build --recipe … → OCR 준비(docgen.bench.ocr_prepare)</span></div>
    <div class="rc-grid">
      <div class="panel"><b>무엇을</b>
        <label class="fld">설명 <input type="text" id="rc-about" value="${esc(r.about || "")}"></label>
        <label class="fld">용도 <select id="rc-split"><option value="benchmark">평가 전용 (benchmark_only)</option>
          <option value="train" ${r.split === "train" ? "selected" : ""}>학습 데이터 (benchmark_fraction 만큼 문서를 평가로 떼어 둠)</option></select></label>
        <label class="fld">서식 (all · 서식 ID · 그룹, 쉼표로) <input type="text" id="rc-types" value="${esc(Array.isArray(r.types) ? r.types.join(",") : r.types || "all")}"></label>
        ${formPickButton("rc-types", "쓸 서식")}
        <label class="fld">서식마다 고객 수 <input type="number" id="rc-perdoc" value="${r.per_doc ?? 1}" min="1"></label>
        <label class="fld">빼는 서식 (쉼표) <input type="text" id="rc-exclude" value="${esc((r.exclude || []).join(","))}"></label>
        ${formPickButton("rc-exclude", "뺄 서식")}
        <label><input type="checkbox" id="rc-reviewed" ${r.reviewed_only ? "checked" : ""}> 검수 완료 서식만</label>
        <label class="fld">정답 한 항목의 단위 <select id="rc-unit"><option value="word">단어 (줄 번호 함께)</option><option value="line" ${r.unit === "line" ? "selected" : ""}>줄</option></select></label>
        <div class="muted" style="font-size:12px">사내 OCR 이 내는 단위에 맞추세요 (DESIGN.md 12절). 견본 표시·도장 안 글자·정정 글자는 신뢰도 0.3 으로 적어 1부가 그 자리를 뺍니다.</div>
        <div class="bar"><label>내용 많음 ${sel("rc-heavy", r.heavy)}</label><label>특수 상황 ${sel("rc-special", r.special)}</label></div>
      </div>
      <div class="panel"><b>촬영 조건 비율</b> <span class="muted">합 1 (OCR 준비가 노이즈 사본을 따로 더 만듭니다)</span>
        <div class="bar">${Object.keys(opts.conditions).map(c => `<label>${esc(COND_NAME[c] || c)} ${num(`rc-c-${c}`, conds[c] ?? 0)}</label>`).join("")}</div>
        <b>합칠 manifest</b> <span class="muted">실서류 등 다른 데이터와 섞어 한 번에 prepare (한 줄에 경로 하나)</span>
        <textarea id="rc-merge" rows="3" class="mono" style="width:100%">${esc((r.merge_manifests || []).join("\n"))}</textarea>
        <b>OCR 준비 설정 덮어쓰기 (JSON)</b> <span class="muted">tasks_per_view, filters, benchmark_fraction, image_max_size …</span>
        <textarea id="rc-prepare" rows="6" class="mono" style="width:100%">${esc(JSON.stringify(r.prepare || {}, null, 1))}</textarea>
        <label class="fld">seed 시작 <input type="number" id="rc-start" value="${r.start ?? 0}" min="0"></label>
      </div>
    </div>`;
  bindFormPickers();
  $("#rc-save").onclick = async () => {
    try {
      const types = $("#rc-types").value.trim();
      const out = { about: $("#rc-about").value.trim(), track: "ocr", split: $("#rc-split").value,
        types: !types || types === "all" ? "all" : types.split(",").map(s => s.trim()).filter(Boolean),
        per_doc: +$("#rc-perdoc").value, unit: $("#rc-unit").value, heavy: $("#rc-heavy").value, special: $("#rc-special").value,
        start: +$("#rc-start").value,
        conditions: Object.fromEntries(Object.keys(opts.conditions).map(c => [c, +$(`#rc-c-${c}`).value]).filter(([, v]) => v > 0)) };
      const ex = $("#rc-exclude").value.split(",").map(s => s.trim()).filter(Boolean);
      if (ex.length) out.exclude = ex;
      if ($("#rc-reviewed").checked) out.reviewed_only = true;
      const mm = $("#rc-merge").value.split("\n").map(s => s.trim()).filter(Boolean);
      if (mm.length) out.merge_manifests = mm;
      const prep = JSON.parse($("#rc-prepare").value || "{}");
      if (Object.keys(prep).length) out.prepare = prep;
      await api(`/api/recipes/${encodeURIComponent(name)}`, out, "PUT");
      toast("저장했습니다"); viewRecipe(name);
    } catch (e) { toast(e.message, true); }
  };
  $("#rc-del").onclick = async () => { if (confirm("레시피를 지울까요?")) { await api(`/api/recipes/${encodeURIComponent(name)}`, undefined, "DELETE"); location.hash = "#/datasets"; } };
}


// 서식 고르기 창: 레시피의 "쓸 서식"(types)·"빼는 서식"(exclude) 칸을 목록에서 체크해 채운다 --------------------
// 칸에 저장되는 형식은 그대로 (쉼표로 이은 서식 ID). 서식 ID 가 아닌 값(all·그룹 이름)은 고른 뒤에도 남긴다.
const csvIds = v => v.split(",").map(s => s.trim()).filter(Boolean);

function formPickButton(inputId, what, note = "") {
  return `<div class="bar"><button type="button" data-pick="${inputId}" data-what="${esc(what)}" data-note="${esc(note)}">서식 고르기</button>
    <span class="muted" data-pick-n="${inputId}"></span></div>`;
}

function bindFormPickers() {
  $$("[data-pick]").forEach(b => {
    const input = $(`#${b.dataset.pick}`), n = $(`[data-pick-n="${b.dataset.pick}"]`);
    const count = () => {
      const ids = csvIds(input.value).filter(x => x !== "all");
      n.textContent = ids.length ? `${ids.length}개` : "";
    };
    input.addEventListener("input", count);
    count();
    b.onclick = async () => {
      const picked = await pickForms(csvIds(input.value), b.dataset.what, b.dataset.note);
      if (picked === null) return;
      input.value = picked.length ? picked.join(",") : (b.dataset.pick === "rc-types" ? "all" : "");
      count();
    };
  });
}

async function pickForms(current, what, note = "") {
  const forms = await api("/api/forms");
  const known = new Set(forms.map(f => f.id));
  const keep = current.filter(x => !known.has(x) && x !== "all");   // 그룹 이름 등 서식 ID 가 아닌 값
  const sel = new Set(current.filter(x => known.has(x)));
  const groups = [...new Map(forms.map(f => [f.group, f.group_name])).entries()].sort((a, b) => a[1].localeCompare(b[1]));
  const dialog = document.createElement("dialog");
  dialog.className = "qa-dialog";
  dialog.innerHTML = `<div class="bar"><h2>${esc(what)} 고르기</h2><button type="button" class="fp-close">닫기 ×</button></div>
    <div class="bar">
      <input type="search" id="fp-q" placeholder="ID·서식명 검색" style="width:220px">
      <select id="fp-group"><option value="">그룹 전체</option>${groups.map(([g, n]) => `<option value="${esc(g)}">${esc(n)}</option>`).join("")}</select>
      <label><input type="checkbox" id="fp-only"> 고른 것만 보기</label>
    </div>
    <div class="bar"><button type="button" id="fp-all">보이는 것 모두 고르기</button><button type="button" id="fp-none">보이는 것 모두 빼기</button>
      <span class="muted" id="fp-count"></span></div>
    ${keep.length ? `<p class="muted">목록에 없는 값은 그대로 둡니다: <span class="mono">${esc(keep.join(", "))}</span></p>` : ""}
    <div id="fp-list" style="max-height:56vh;overflow:auto"></div>
    ${note ? `<p class="muted" style="font-size:12px">${esc(note)}</p>` : ""}
    <div class="bar"><button type="button" class="primary" id="fp-ok">적용</button><button type="button" class="fp-close">취소</button></div>`;
  document.body.appendChild(dialog);
  let rows = [];
  const draw = () => {
    const q = $("#fp-q", dialog).value.trim().toLowerCase(), g = $("#fp-group", dialog).value;
    const only = $("#fp-only", dialog).checked;
    rows = forms.filter(f => (!q || f.id.toLowerCase().includes(q) || f.name.toLowerCase().includes(q)) && (!g || f.group === g) &&
      (!only || sel.has(f.id)));
    $("#fp-count", dialog).textContent = `보이는 서식 ${rows.length}종 · 고른 서식 ${sel.size}종`;
    $("#fp-list", dialog).innerHTML = `<table><thead><tr><th></th><th>ID</th><th>서식명</th><th>그룹</th></tr></thead><tbody>${rows.map(f => `
      <tr><td><input type="checkbox" data-fp="${esc(f.id)}" ${sel.has(f.id) ? "checked" : ""}></td>
        <td class="mono">${esc(f.id)}</td><td>${esc(f.name)}</td><td class="nw">${esc(f.group_name)}</td></tr>`).join("")}</tbody></table>`;
  };
  ["#fp-q", "#fp-group", "#fp-only"].forEach(id => $(id, dialog).addEventListener("input", draw));
  $("#fp-list", dialog).addEventListener("change", e => {
    const id = e.target.dataset.fp;
    if (!id) return;
    e.target.checked ? sel.add(id) : sel.delete(id);
    $("#fp-count", dialog).textContent = `보이는 서식 ${rows.length}종 · 고른 서식 ${sel.size}종`;
  });
  $("#fp-all", dialog).onclick = () => { rows.forEach(f => sel.add(f.id)); draw(); };
  $("#fp-none", dialog).onclick = () => { rows.forEach(f => sel.delete(f.id)); draw(); };
  draw();
  return new Promise(resolve => {
    let result = null;
    $$(".fp-close", dialog).forEach(b => b.onclick = () => dialog.close());
    $("#fp-ok", dialog).onclick = () => {
      result = [...keep, ...forms.map(f => f.id).filter(id => sel.has(id))];
      dialog.close();
    };
    dialog.addEventListener("close", () => { dialog.remove(); resolve(result); });
    dialog.showModal();
    $("#fp-q", dialog).focus();
  });
}
