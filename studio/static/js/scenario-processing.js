// ③ 시나리오·묶음 › 처리 설정: 묶음에서 무엇을 검사·추출·비교할지(구비 검사, 대조 사례, 심사 규칙, 직접 작업) 정하고 예시 고객으로 실행한다.
// scenarios.js 가 ScenarioProcessing 을 만들어 쓰고, 저장은 시나리오와 함께 PUT /api/scenarios. 설계: DESIGN.md 9.5.1
// 서버: POST /api/scenarios/run (studio/scenario_processing.py). Q/A 창은 questions.js 의 showQuestionQA
"use strict";

class ScenarioProcessing {
  constructor(meta, previews) {
    this.meta = meta;
    this.previews = previews;
    this.states = new WeakMap();
    this.fields = new Map();
  }

  html(s, i) {
    s.processing = { doc_check: true, cross_check: true, review: true, case_ids: null, rule_ids: null, operations: [], ...(s.processing || {}) };
    if (!this.states.has(s)) this.states.set(s, { open: i === 0, version: 0, result: null });
    const p = s.processing, v = this.states.get(s);
    const checks = (key, rows) => rows.map(([id, name]) => `<label><input type="checkbox" data-pick="${key}" value="${esc(id)}"
      ${p[key] === null || p[key].includes(id) ? "checked" : ""}> ${esc(name)}</label>`).join("");
    return `<details class="sc-processing" ${v.open ? "open" : ""}>
      <summary>이 묶음에서 할 일 <span class="tag">구비 검사 · 추출 · 비교 · 심사</span></summary>
      <div class="sc-processing-body">
        <div class="bar">${[["doc_check", "서류 구비 검사"], ["cross_check", "대조 사례 생성"], ["review", "기본 심사 질의"]].map(([key, name]) =>
          `<label><input type="checkbox" data-process="${key}" ${p[key] ? "checked" : ""}> ${name}</label>`).join("")}</div>
        <div class="sc-processing-choices">
          <details><summary>대조 사례 선택 (${this.meta.cases.length}종)</summary><div class="sc-processing-checks">${checks("case_ids", this.meta.cases.map(c => [c.id, c.title]))}</div></details>
          <details><summary>심사·계산 규칙 선택 (${Object.keys(this.meta.processing_rules).length}종)</summary><div class="sc-processing-checks">${checks("rule_ids", Object.entries(this.meta.processing_rules))}</div></details>
        </div>
        <div class="muted">필요한 서류와 값이 있는 작업만 문항으로 만듭니다. 대조 사례의 변조 비율은 레시피에서 정하며, 레시피에서 끈 사례는 생성하지 않습니다.</div>
        <h3>직접 정하는 추출·비교</h3>
        <div class="bar"><button type="button" data-op-add="extract">추출 항목 추가</button><button type="button" data-op-add="compare">비교 작업 추가</button>
          <button type="button" data-op-cross title="두 개 이상의 문서에 나오는 공통 키(키 사전)마다 첫 문서와 같은지 비교">서류끼리 대조할 공통 키로 비교 작업 추가</button></div>
        <div class="sc-operations"></div>
        <div class="bar sc-processing-runbar"><button type="button" class="primary sc-process-run">예시 고객으로 실행</button>
          <span class="sc-process-status muted" role="status" aria-live="polite"></span></div>
        <div class="sub">위 이미지와 같은 고객 seed로 실행합니다. 생성된 원본의 정답으로 추출값·비교 결과·계산값을 확인하며, 근거를 누르면 문서의 해당 위치가 열립니다.
          대조 사례는 변조 문항을 만들 수 있는지 확인하고, 실제 변조 이미지는 데이터셋 생성 후 확인합니다.</div>
        <div class="sc-process-results"></div>
      </div></details>`;
  }

  invalidate(card, s) {
    const v = this.states.get(s);
    if (!v) return;
    v.version++;
    v.result = null;
    const out = $(".sc-process-results", card), status = $(".sc-process-status", card);
    if (out) out.innerHTML = "";
    if (status) status.textContent = "구성·설정이 바뀌었습니다. 다시 실행해 주세요.";
    const button = $(".sc-process-run", card);
    if (button) button.disabled = false;
  }

  bind(card, s, mark) {
    const v = this.states.get(s), p = s.processing, details = $(".sc-processing", card);
    details.ontoggle = () => { v.open = details.open; };
    const changed = () => { mark(); this.invalidate(card, s); };
    card.addEventListener("scenario-preview-change", () => this.invalidate(card, s));
    $$("[data-process]", card).forEach(cb => cb.onchange = () => { p[cb.dataset.process] = cb.checked; changed(); });
    $$("[data-pick]", card).forEach(cb => cb.onchange = () => {
      p[cb.dataset.pick] = $$(`[data-pick="${cb.dataset.pick}"]`, card).filter(x => x.checked).map(x => x.value);
      changed();
    });
    $("[data-op-cross]", card).onclick = async () => {
      const lists = await Promise.all(s.docs.map(d => this.commonKeys(d.id)));
      const where = new Map();
      // 도장·서명과 주소는 뺀다: 주소는 서류마다 적는 방식이 달라(", JAPAN" 등) 글자 그대로 같은지 묻는 비교가 의미 없다
      lists.forEach((keys, i) => keys.filter(c => !/^(seal|sign)\./.test(c.key) && !/address$/.test(c.key)).forEach(c => {
        if (!where.has(c.key)) where.set(c.key, { name: c.name, docs: [] });
        where.get(c.key).docs.push(s.docs[i].id);
      }));
      let added = 0;
      for (const [key, w] of where) {
        for (const other of w.docs.slice(1)) {
          const first = w.docs[0];
          if (p.operations.some(op => op.kind === "compare" && op.left.common === key && op.right?.common === key && op.left.doc === first && op.right.doc === other)) continue;
          let n = p.operations.length + 1;
          while (p.operations.some(op => op.id === `cross_${n}`)) n++;
          p.operations.push({ id: `cross_${n}`, kind: "compare", name: `${w.name}: ${s.docs.find(d => d.id === first)?.name || first} ↔ ${s.docs.find(d => d.id === other)?.name || other}`,
            enabled: true, operator: "equal", left: { doc: first, common: key }, right: { doc: other, common: key } });
          added++;
        }
      }
      toast(added ? `비교 작업 ${added}개를 더했습니다` : "더할 공통 키가 없습니다 (두 개 이상의 문서에 나오는 공통 키)");
      if (added) { changed(); this.drawOperations(card, s, changed); }
    };
    $$("[data-op-add]", card).forEach(btn => btn.onclick = () => {
      if (!s.docs.length) { toast("먼저 필수 서류를 추가하세요", true); return; }
      let n = 1;
      while (p.operations.some(op => op.id === `step_${n}`)) n++;
      const kind = btn.dataset.opAdd;
      p.operations.push({ id: `step_${n}`, kind, name: kind === "extract" ? "항목 추출" : "항목 비교", enabled: true,
        left: { doc: s.docs[0].id, key: "" }, ...(kind === "compare" ? { right: { doc: s.docs[0].id, key: "" }, operator: "equal" } : {}) });
      changed(); this.drawOperations(card, s, changed);
    });
    this.drawOperations(card, s, changed);
    $(".sc-process-run", card).onclick = async () => {
      if ($$(".sc-operations [required]", card).some(inp => !inp.reportValidity())) return;
      const version = ++v.version, seed = this.previews.states.get(s).seed;
      const button = $(".sc-process-run", card), status = $(".sc-process-status", card);
      button.disabled = true;
      status.className = "sc-process-status muted";
      status.textContent = `고객 seed ${seed} · 서류 준비와 처리 결과 계산 중…`;
      try {
        const result = await api("/api/scenarios/run", { scenario: { ...s, docs: s.docs.map(d => d.id) }, seed });
        if (!card.isConnected || v.version !== version) return;
        v.result = result;
        const pv = this.previews.states.get(s);
        pv.docs=result.selections || s.docs;
        for (const [did, label] of Object.entries(result.labels)) pv.labels.set(did, label);
        status.textContent = `${result.customer} · seed ${seed} · 실행 완료`;
        this.drawResults(card, s);
        this.drawOperations(card, s, changed); // 실제 고객에서 새로 발견된 항목도 선택 후보에 반영
      } catch (e) {
        if (card.isConnected && v.version === version) { status.textContent = e.message; status.classList.add("err"); }
      } finally { if (card.isConnected && v.version === version) button.disabled = false; }
    };
    if (v.result) this.drawResults(card, s);
  }

  commonKeys(doc) {   // 그 서식에 있는 공통 키 (키 사전). 공통 키로 정한 작업은 같은 문서의 다른 서식으로 바꿔도 그대로 돈다
    this.common ||= new Map();
    if (!this.common.has(doc)) this.common.set(doc, api(`/api/dictionary/common_for/${encodeURIComponent(doc)}`).then(d => d.keys).catch(() => []));
    return this.common.get(doc);
  }

  async keyOptions(doc, selected, s, common) {
    const ck = (await this.commonKeys(doc)).filter(c => !/^(seal|sign)\./.test(c.key));
    const commonOpts = ck.length ? `<optgroup label="공통 키 (서식이 바뀌어도 그대로)">${ck.map(c =>
      `<option value="common:${esc(c.key)}" ${c.key === common ? "selected" : ""}>${esc(c.name)} · ${esc(c.key)}</option>`).join("")}</optgroup>` : "";
    if (!this.fields.has(doc)) this.fields.set(doc, api(`/api/forms/${encodeURIComponent(doc)}`).then(d => d.keys).catch(e => { this.fields.delete(doc); throw e; }));
    const fields = new Map((await this.fields.get(doc)).filter(f => !["checkbox", "checkbox_multi", "seal", "signature"].includes(f.type)).map(f => [f.key, f]));
    const rendered = this.previews.states.get(s).labels.get(doc);
    for (const f of rendered?.fields || []) if (!f.group && !["checkbox", "checkbox_multi", "seal", "signature"].includes(f.type)) fields.set(f.key, f);
    if (selected && !fields.has(selected)) fields.set(selected, { key: selected, label: "현재 고객의 후보에 없는 항목" });
    return `<option value="">항목을 고르세요</option>` + commonOpts + `<optgroup label="이 서식의 키">` + [...fields.values()].map(f =>
      `<option value="${esc(f.key)}" ${f.key === selected && !common ? "selected" : ""}>${esc(f.label || f.key)} · ${esc(f.key)}</option>`).join("") + `</optgroup>`;
  }

  drawOperations(card, s, changed) {
    const box = $(".sc-operations", card), p = s.processing;
    const candidateName=id=>state.forms?.find(f=>f.id===id)?.name || id;
    const mappings=(op,side)=>{
      const conf=s.sampling?.[op[side].doc], forms=conf?.mode==='sample'&&!op[side].common?conf.forms.filter(id=>id!==op[side].doc):[];
      return forms.length?`<details><summary>후보 서식별 항목 연결 · ${forms.length}종</summary><div class="muted">다른 서식은 키가 다를 수 있습니다. 연결하지 않은 후보가 선택되면 이 작업을 건너뜁니다.</div>${forms.map(id=>`<label>${esc(candidateName(id))} · ${esc(id)}<select data-ref-map="${side}" data-candidate="${esc(id)}"><option value="">연결 안 함</option></select></label>`).join('')}</details>`:'';
    };
    const ref = (op, side) => `<div class="sc-operation-ref">
      <select data-ref-doc="${side}" aria-label="${side === "left" ? "기준" : "비교"} 문서" required><option value="">문서 선택</option>${s.docs.map(d =>
        `<option value="${esc(d.id)}" ${d.id === op[side].doc ? "selected" : ""}>${esc(d.name || d.id)}</option>`).join("")}</select>
      <select data-ref-key="${side}" aria-label="${side === "left" ? "기준" : "비교"} 항목" required><option value="">항목 불러오는 중…</option></select>${mappings(op,side)}</div>`;
    box.innerHTML = p.operations.map((op, i) => `<div class="sc-operation" data-op="${i}">
      <div class="bar"><label><input type="checkbox" data-op-enabled ${op.enabled === false ? "" : "checked"}> ${op.kind === "extract" ? "추출" : "비교"}</label>
        <input type="text" data-op-name value="${esc(op.name || "")}" aria-label="작업 이름"><button type="button" data-op-delete>작업 삭제</button></div>
      <div class="sc-operation-fields">${ref(op, "left")}${op.kind === "compare" ? `<select data-op-operator aria-label="비교 조건">${Object.entries(this.meta.compare_operators).map(([key, name]) =>
        `<option value="${key}" ${op.operator === key ? "selected" : ""}>${esc(name)}</option>`).join("")}</select>${ref(op, "right")}` : `<span class="muted">값과 근거 위치 추출</span>`}</div>
      </div>`).join("") || `<p class="muted">문서와 항목을 골라 필요한 값 추출이나 문서 간 비교를 추가하세요.</p>`;
    $$(".sc-operation", box).forEach(row => {
      const op = p.operations[+row.dataset.op];
      const fill = async side => {
        const key = $(`[data-ref-key="${side}"]`, row), did = op[side].doc;
        try {
          const options = await this.keyOptions(did, op[side].key, s, op[side].common);
          if (key.isConnected && op[side].doc === did) key.innerHTML = options;
        } catch (e) { if (key.isConnected) { key.innerHTML = `<option value="">항목을 불러오지 못했습니다</option>`; toast(e.message, true); } }
      };
      $$("[data-ref-doc]", row).forEach(sel => sel.onchange = () => { const side = sel.dataset.refDoc; op[side] = { doc: sel.value, key: "" }; changed(); this.drawOperations(card,s,changed); });
      $$("[data-ref-key]", row).forEach(sel => { sel.onchange = () => {
        const side = sel.dataset.refKey, doc = op[side].doc;
        op[side] = sel.value.startsWith("common:") ? { doc, common: sel.value.slice(7) } : { doc, key: sel.value };
        changed(); this.drawOperations(card, s, changed);
      }; fill(sel.dataset.refKey); });
      $$('[data-ref-map]',row).forEach(async sel=>{
        const side=sel.dataset.refMap,id=sel.dataset.candidate;
        try{const options=await this.keyOptions(id,op[side].keys?.[id],s);if(sel.isConnected)sel.innerHTML=options;}
        catch(e){if(sel.isConnected)sel.innerHTML='<option value="">항목 읽기 실패</option>';}
        sel.onchange=()=>{op[side].keys ||= {};if(sel.value)op[side].keys[id]=sel.value;else delete op[side].keys[id];changed();};
      });
      $("[data-op-enabled]", row).onchange = e => { op.enabled = e.target.checked; changed(); };
      $("[data-op-name]", row).onchange = e => { op.name = e.target.value.trim(); changed(); };
      const oper = $("[data-op-operator]", row);
      if (oper) oper.onchange = () => { op.operator = oper.value; changed(); };
      $("[data-op-delete]", row).onclick = () => { p.operations.splice(+row.dataset.op, 1); changed(); this.drawOperations(card, s, changed); };
    });
  }

  drawResults(card, s) {
    const result = this.states.get(s).result;
    if (!result) return;
    const statuses = { ready: "확인 가능", skipped: "적용 불가", disabled: "끔", error: "오류" };
    const kinds = { extract: "추출", compare: "비교", rule: "심사·계산", case: "대조 사례", doc_check: "구비 검사" };
    const out = $(".sc-process-results", card);
    out.innerHTML = table(result.rows, [["kind", "처리", (row, i) => `${kinds[row.kind]}<div><button type="button" data-qa="${i}">Q/A 포맷·예시</button></div>`], ["name", "작업·기준", row => `<b>${esc(row.name)}</b>
      ${row.question ? `<div class="sc-result-question muted">${esc(row.question)}</div>` : ""}`],
      ["answer", "결과", row => `<span class="tag ${row.status === "ready" ? "ok" : row.status === "disabled" ? "" : "warn"}">${statuses[row.status]}</span>
        <div>${esc(row.reason || (typeof row.answer === "object" ? JSON.stringify(row.answer) : row.answer))}</div>
        ${(row.changes || []).slice(0, 3).map(c => `<div class="sc-result-question muted">변조 예: ${esc(c.key)} · ${esc(c.old)} → ${esc(c.new)}</div>`).join("")}`],
      ["sources", "근거", (row, i) => row.sources.map((ref, j) => `<button type="button" class="sc-evidence-link" data-source="${i}:${j}">${esc(ref.name)}${ref.key ? ` · ${esc(ref.label || ref.key)}` : ""}
        ${ref.key ? `<span class="muted">${esc(ref.value)}</span>` : ""}</button>`).join("")]]);
    $$("[data-source]", out).forEach(btn => btn.onclick = () => {
      const [i, j] = btn.dataset.source.split(":").map(Number), ref = result.rows[i].sources[j];
      this.previews.show(s, ref.doc, ref.key);
    });
    $$("[data-qa]", out).forEach(btn => btn.onclick = () => {
      const row = result.rows[+btn.dataset.qa], task = { extract: "kie", compare: "review", case: "cross_check", rule: "review", doc_check: "doc_check" }[row.kind];
      showQuestionQA(task, row.qa || [], row.name, "현재 고객의 원본 정답을 사용하는 Q/A 예시입니다. 변조·빠짐·타인 서류가 적용된 최종 문항은 데이터셋 생성 후 ⑥에서 확인합니다.").catch(e => toast(e.message, true));
    });
  }
}
