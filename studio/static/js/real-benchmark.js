// 실문서 벤치마크: 작업 목록 → 포맷·항목 → 추론·검수 → 확정. 기존 박스 편집기를 공유한다.
"use strict";

addRoute(/^#\/real-bench$/, () => rbList(), "real-bench");
addRoute(/^#\/real-bench\/connections(?:\?from=([^&]+))?$/, from => rbConnections(from ? decodeURIComponent(from) : ""), "real-bench");
addRoute(/^#\/real-bench\/([^/]+)\/doc\/([^/]+)\/(.+)$/, (n, f, d) => rbReview(decodeURIComponent(n), decodeURIComponent(f), decodeURIComponent(d)), "real-bench");
addRoute(/^#\/real-bench\/([^/]+)$/, n => rbWork(decodeURIComponent(n)), "real-bench");

const RB_TYPES = { text: "글자", amount: "금액", number: "숫자", date: "날짜", checkbox: "체크 선택", seal: "도장 유무", signature: "서명 유무" };
const rbUrl = n => `/api/real-bench/${q(n)}`;
const rbHash = n => `#/real-bench/${q(n)}`;
const rbHead = n => `<div class="muted rb-breadcrumb"><a href="#/real-bench">실문서 벤치마크</a>${n ? ` › <a href="${rbHash(n)}">${esc(n)}</a>` : ""}</div>`;
const rbImage = (n, p, w = 320) => `/api/imports/${q(n)}/page?p=${q(p)}&w=${w}`;

async function rbAction(button, fn) {
  button.disabled = true;
  try { await fn(); } catch (e) { toast(e.message, true); }
  finally { if (button.isConnected) button.disabled = false; }
}

async function rbList() {
  const r = await api("/api/real-bench");
  const ready = !!r.connections.ocr.revision;
  main().innerHTML = `<div class="bar"><h1>실문서 벤치마크</h1><span style="flex:1"></span><a href="#/real-bench/connections"><button>OCR·모델 연결</button></a></div>
    <p class="sub">내 문서를 포맷별로 묶고, 원하는 항목을 모델로 추출한 뒤 검수하여 평가 세트로 만듭니다.</p>
    ${!ready ? `<div class="panel warnbox">먼저 <a href="#/real-bench/connections">OCR·모델 연결</a>에서 OCR 서버와 버전을 등록하세요. 기존 Studio 설정이 있으면 그대로 사용합니다.</div>` : ""}
    <details class="panel rb-create" ${r.works.length ? "" : "open"}><summary>새 작업 만들기</summary>
      <form id="rb-create"><label>작업 이름 <input id="rb-name" required placeholder="대출서류 1차"></label>
      <label>가져올 위치 <select id="rb-source"><option value="upload">파일 업로드</option><option value="folder">서버 폴더</option></select></label>
      <label id="rb-files-row">이미지·PDF <input id="rb-files" type="file" multiple accept="image/*,.pdf"></label>
      <label id="rb-path-row" hidden>서버 폴더 경로 <input id="rb-path" placeholder="/data/documents"></label>
      <p class="muted">PDF 한 파일은 문서 하나입니다. 개별 이미지는 포맷 확인 단계에서 여러 쪽 문서로 묶을 수 있습니다.</p>
      <button class="primary" id="rb-create-btn" ${ready ? "" : "disabled"}>등록하고 포맷 묶기</button></form>
    </details>
    ${r.works.length ? table(r.works, [["name", "작업", w => `<a href="${rbHash(w.name)}">${esc(w.name)}</a>`], ["n_documents", "문서 수", null, true],
      ["status", "진행", w => w.snapshots.length ? `<span class="tag ok">확정 ${w.snapshots.length}개 버전</span> · 검수 ${w.done}/${w.n_documents}` : `검수 ${w.done}/${w.n_documents} · 추론 ${w.with_pred}`],
      ["created", "등록일"], ["go", "", w => `<a href="${rbHash(w.name)}"><button>작업 열기</button></a>`]]) : `<div class="panel muted">등록한 작업이 없습니다. 이미지·PDF로 첫 벤치마크를 만들어 보세요.</div>`}`;
  $("#rb-source").onchange = e => { $("#rb-path-row").hidden = e.target.value !== "folder"; $("#rb-files-row").hidden = e.target.value === "folder"; };
  $("#rb-create").onsubmit = e => {
    e.preventDefault();
    rbAction($("#rb-create-btn"), async () => {
      let res;
      if ($("#rb-source").value === "folder") res = await api("/api/real-bench", { name: $("#rb-name").value, path: $("#rb-path").value });
      else {
        const fd = new FormData(); fd.append("name", $("#rb-name").value);
        for (const f of $("#rb-files").files) fd.append("files", f);
        const response = await fetch("/api/real-bench/upload", { method: "POST", body: fd });
        res = await response.json(); if (!response.ok) throw new Error(res.detail || "업로드 실패");
      }
      location.hash = rbHash(res.name);
    });
  };
}

async function rbConnections(from = "") {
  const c = await api("/api/real-bench/connections");
  const providerNames = Object.keys(c.providers);
  main().innerHTML = rbHead() + `<h1>OCR·모델 연결</h1><p class="sub">한 번 등록한 연결을 모든 실문서 작업에서 사용합니다. 기존 Studio 설정도 자동으로 불러옵니다.</p>
    <form id="rb-connections"><div class="rb-connection-grid">
      <section class="panel rb-form"><h2>OCR</h2><p class="muted">글자와 좌표를 읽어 같은 포맷끼리 묶습니다.</p>
        <label>서버 주소 <input id="rb-ocr-url" placeholder="http://ocr-server:30107" value="${esc(c.ocr.base_url || "")}"></label>
        <label>OCR 버전 <input id="rb-ocr-version" placeholder="ocr-v1" value="${esc(c.ocr.revision || "")}"></label>
        <details><summary>상세 설정</summary><label>어댑터 <input id="rb-ocr-adapter" value="${esc(c.ocr.callable || "studio.internal_ocr_adapter:ocr_from_file")}"></label>
          <label>응답 매핑 (비워 두면 사내 OCR 형식) <textarea id="rb-ocr-mapping" rows="6">${esc(c.ocr.mapping ? JSON.stringify(c.ocr.mapping, null, 2) : "")}</textarea></label></details>
        <button type="button" id="rb-check-ocr">저장한 OCR 연결 확인</button><div id="rb-ocr-status" role="status"></div>
      </section>
      <section class="panel rb-form"><h2>VLM</h2><p class="muted">별도 서버의 vLLM에 이미지를 보내 항목을 추출합니다.</p>
        <label>등록 모델 <select id="rb-provider"><option value="">새 연결</option>${providerNames.map(n => `<option value="${esc(n)}">${esc(n)}</option>`).join("")}</select></label>
        <label>연결 이름 <input id="rb-provider-name" placeholder="bank-sft-v1"></label>
        <label>서버 주소 <input id="rb-vlm-url" placeholder="http://model-server:8000/v1"></label>
        <label>서버의 모델 이름 <input id="rb-vlm-model" placeholder="bank-sft-v1"></label>
        <details><summary>상세 설정</summary>
          <label>인증 키 환경변수 이름 (선택) <input id="rb-vlm-auth" placeholder="VLLM_API_KEY"></label>
          <label>최대 응답 길이 <input id="rb-vlm-tokens" type="number" min="256" max="65536" value="8192"></label>
          <label>타임아웃 (초) <input id="rb-vlm-timeout" type="number" min="5" max="1800" value="300"></label>
        </details><button type="button" id="rb-check-vlm">저장한 모델 연결 확인</button><div id="rb-vlm-status" role="status"></div>
      </section></div><div class="bar"><button class="primary" id="rb-save-connections">연결 저장</button><a href="${from ? rbHash(from) : "#/real-bench"}">작업으로 돌아가기</a><span id="rb-connection-saved" role="status"></span></div></form>`;
  const fill = name => {
    const p = c.providers[name] || {};
    $("#rb-provider-name").value = name;
    $("#rb-vlm-url").value = p.base_url || ""; $("#rb-vlm-model").value = p.model || "";
    $("#rb-vlm-auth").value = p.api_key_env || ""; $("#rb-vlm-tokens").value = p.max_tokens || 8192; $("#rb-vlm-timeout").value = p.timeout || 300;
  };
  if (providerNames.length) { $("#rb-provider").value = providerNames[0]; fill(providerNames[0]); }
  $("#rb-provider").onchange = e => fill(e.target.value);
  $("#rb-connections").onsubmit = e => {
    e.preventDefault(); rbAction($("#rb-save-connections"), async () => {
      const providers = { ...c.providers }, name = $("#rb-provider-name").value.trim();
      if (name) providers[name] = { base_url: $("#rb-vlm-url").value.trim(), model: $("#rb-vlm-model").value.trim(), api_key_env: $("#rb-vlm-auth").value.trim(),
        max_tokens: +$("#rb-vlm-tokens").value, timeout: +$("#rb-vlm-timeout").value };
      const ocr = { ...c.ocr, base_url: $("#rb-ocr-url").value.trim(), revision: $("#rb-ocr-version").value.trim(), callable: $("#rb-ocr-adapter").value.trim() };
      ocr.mapping = $("#rb-ocr-mapping").value.trim() ? JSON.parse($("#rb-ocr-mapping").value) : null;
      const result = await api("/api/real-bench/connections", { ocr, providers }, "PUT");
      c.providers = result.providers; c.ocr = result.ocr;
      $("#rb-provider").innerHTML = `<option value="">새 연결</option>` + Object.keys(c.providers).map(n => `<option value="${esc(n)}">${esc(n)}</option>`).join("");
      $("#rb-provider").value = name;
      $("#rb-connection-saved").textContent = "저장했습니다"; toast("연결을 저장했습니다");
    });
  };
  for (const kind of ["ocr", "vlm"]) $(`#rb-check-${kind}`).onclick = e => rbAction(e.currentTarget, async () => {
    const res = await api("/api/real-bench/connections/check", { kind, provider: $("#rb-provider-name").value });
    $(`#rb-${kind}-status`).textContent = `${res.ok && res.model_listed !== false ? "연결 확인" : "연결 확인 필요"}: ${res.detail || ""}${res.model_listed === false ? " (등록한 모델 이름이 서버 목록에 없습니다)" : ""}`;
  });
}

function rbSteps(w) {
  const stage = w.snapshots.length ? 4 : w.done ? 3 : w.with_pred ? 3 : w.formats.some(f => f.schema) ? 2 : w.formats.length ? 2 : 1;
  return `<div class="rb-steps">${["이미지 등록", "포맷·추출 항목", "추론·검수", "벤치마크 확정"].map((s, i) => `<a href="#rb-step-${i + 1}" data-rb-anchor="rb-step-${i + 1}" class="${i + 1 <= stage ? "reached" : ""}"><span>${i + 1}</span>${s}</a>`).join("")}</div>`;
}

function rbJobPanel(jobs) {
  return jobs.slice(0, 5).map(j => `<div class="rb-job"><b>${esc(j.title)}</b> <span class="tag ${j.status === "done" ? "ok" : "warn"}">${esc(({ running: "실행 중", done: "완료", failed: "실패", interrupted: "중단됨", cancelled: "취소됨" })[j.status] || j.status)}</span>
    ${j.progress ? `${j.progress[0]} / ${j.progress[1]}` : ""}
    ${j.result && j.result.failed ? `<span class="kr">실패 ${j.result.failed}건 — 추론 시작으로 다시 실행할 수 있습니다.</span>` : ""}
    ${j.result && Object.keys(j.result.failures || {}).length ? `<details><summary>실패한 문서</summary><pre>${esc(Object.entries(j.result.failures).map(([d, v]) => `${d}: ${v.error}`).join("\n"))}</pre></details>` : ""}
    ${j.log_tail || j.error ? `<details><summary>실행 로그</summary><pre>${esc(j.error || "")}${esc(j.log_tail || "")}</pre></details>` : ""}</div>`).join("");
}

async function rbWork(name) {
  const [w, c] = await Promise.all([api(rbUrl(name)), api("/api/real-bench/connections")]);
  const running = w.jobs.some(j => j.status === "running"), hasSchemas = w.formats.some(f => f.schema);
  const h = rbHash(name), url = rbUrl(name), providers = Object.keys(c.providers);
  main().innerHTML = rbHead(name) + `<div class="bar"><h1>${esc(name)}</h1><span style="flex:1"></span><a href="#/real-bench/connections?from=${q(name)}"><button>연결 설정</button></a><button id="rb-reload">새로고침</button></div>
    ${rbSteps(w)}
    <section class="panel" id="rb-step-1"><div class="bar"><b>이미지 ${w.pages.length}쪽 · 문서 ${w.n_documents}건 · 포맷 ${w.formats.length}개</b>
      <button id="rb-ocr-retry" ${running || hasSchemas ? "disabled" : ""}>OCR·포맷 묶기 재시도</button></div>
      <div id="rb-jobs">${rbJobPanel(w.jobs)}</div><div id="rb-update" role="status"></div>
    </section>
    <section id="rb-step-2"><h2>포맷·추출 항목</h2><p class="muted">같은 질문을 적용할 문서를 확인하고, 포맷마다 찾을 항목을 입력하세요. 추출 항목을 저장하기 전에 그룹을 합치거나 나눠 주세요.</p>
      ${w.formats.length ? `<div class="panel bar"><label>포맷 <select id="rb-merge-src">${w.formats.map(f => `<option value="${esc(f.id)}">${esc(f.name)}</option>`).join("")}</select></label>
        <span>→</span><label>합칠 포맷 <select id="rb-merge-dst">${w.formats.map(f => `<option value="${esc(f.id)}">${esc(f.name)}</option>`).join("")}</select></label>
        <button id="rb-merge" ${running || hasSchemas ? "disabled" : ""}>합치기</button>
        <label>새 그룹 이름 <input id="rb-split-name" value="새 포맷" size="12"></label><button id="rb-split" ${running || hasSchemas ? "disabled" : ""}>선택 문서로 그룹 분리</button>
        <button id="rb-join" ${running || hasSchemas ? "disabled" : ""}>선택 이미지를 한 문서로</button></div>` : `<div class="panel muted">OCR과 포맷 묶기가 끝나면 그룹이 나타납니다. 실패하면 연결 설정과 실행 로그를 확인하고 재시도하세요.</div>`}
      <div class="rb-formats">${w.formats.map((f, index) => `<details class="panel rb-format" ${index === 0 ? "open" : ""} data-fid="${esc(f.id)}">
        <summary><b>${esc(f.schema ? f.schema.name : f.name)}</b> · ${f.documents.length}문서 · 추론 ${f.with_pred} · 검수 ${f.done}${f.schema ? '<span class="tag ok">항목 설정됨</span>' : '<span class="tag warn">추출 항목 필요</span>'}</summary>
        <div class="rb-format-body"><div><div class="rb-thumbs">${f.documents.map(d => `<label class="rb-thumb"><input type="checkbox" data-rb-doc="${esc(d.doc)}" ${hasSchemas || running ? "disabled" : ""}>
          <img src="${rbImage(name, d.pages[0])}" loading="lazy" alt="${esc(d.doc)}"><span>${esc(d.doc)}${d.pages.length > 1 ? ` (${d.pages.length}쪽)` : ""}</span></label>`).join("")}</div></div>
        <div class="rb-schema"><label>포맷 이름 / 분류 정답 <input data-rb-title value="${esc(f.schema ? f.schema.name : f.name)}" ${f.with_pred ? "disabled" : ""}></label>
          <div class="muted">키는 결과의 항목 이름, 설명은 문서에서 찾을 내용입니다. 예: applicant_name / 신청인 성명</div>
          <div class="rb-key-assist"><div class="bar">
            <label>제안 모델 <select data-rb-key-model ${running || f.with_pred ? "disabled" : ""}>${providers.map(n => `<option value="${esc(n)}">${esc(n)}</option>`).join("")}</select></label>
            <button data-rb-suggest ${running || f.with_pred || !providers.length ? "disabled" : ""}>VLM으로 항목·키 제안</button></div>
            <details><summary>대표 문서 선택</summary><select data-rb-key-sample>${f.documents.map(d => `<option value="${esc(d.doc)}">${esc(d.doc)} (${d.pages.length}쪽)</option>`).join("")}</select></details>
            <p class="muted">찾을 내용만 입력해도 기존 키를 연결합니다. 비워 두면 대표 문서에서 항목을 찾습니다. 기존 키의 의미·역할을 함께 보내며, 맞는 키가 없으면 새 키를 제안합니다.</p>
            <div data-rb-key-status role="status"></div><div data-rb-key-results></div>
          </div>
          <table><thead><tr><th>키</th><th>찾을 내용</th><th>타입</th><th></th></tr></thead><tbody data-rb-fields></tbody></table>
          <div class="bar"><button data-rb-add ${f.with_pred || running ? "disabled" : ""}>항목 추가</button><button class="primary" data-rb-save ${f.with_pred || running ? "disabled" : ""}>추출 항목 저장</button></div>
          <div data-rb-schema-status role="status"></div><details><summary>추출 질문 미리보기</summary><pre data-rb-prompt>${esc(f.prompt || "항목을 입력하면 구성을 미리 볼 수 있습니다. 저장하면 실제 질문이 표시됩니다.")}</pre></details>
        </div></div>
      </details>`).join("")}</div>
    </section>
    <section class="panel" id="rb-step-3"><h2>추론·검수</h2><div class="bar"><label>추출 모델 <select id="rb-model">${providers.map(n => `<option value="${esc(n)}">${esc(n)} · ${esc(c.providers[n].model)}</option>`).join("")}</select></label>
      <label>대상 포맷 <select id="rb-infer-format"><option value="">항목을 설정한 모든 포맷</option>${w.formats.filter(f => f.schema).map(f => `<option value="${esc(f.id)}">${esc(f.schema.name)}</option>`).join("")}</select></label>
      <button class="primary" id="rb-infer" ${running || !providers.length || !hasSchemas ? "disabled" : ""}>추출 시작 / 실패 재시도</button></div>
      ${!providers.length ? `<p class="muted"><a href="#/real-bench/connections">VLM 연결을 등록하세요.</a></p>` : ""}
      <p class="muted">문서별로 이미지를 보내 값과 위치를 추출합니다. 성공한 결과와 사용자 수정은 보존하고, 실패·미실행 문서만 다시 실행합니다.</p>
      ${table(w.formats.flatMap(f => f.documents.map(d => ({ ...d, fid: f.id, format: f.schema ? f.schema.name : f.name, ready: !!f.schema }))), [
        ["doc", "문서"], ["format", "포맷"], ["model", "추론 모델", d => esc(d.model || "미실행")],
        ["status", "검수", d => d.status === "done" ? '<span class="tag ok">완료</span>' : d.status ? "수정 중" : "미검수"],
        ["go", "", d => d.ready && !running ? `<a href="${h}/doc/${q(d.fid)}/${q(d.doc)}"><button>${d.status === "done" ? "검수 보기" : "검수하기"}</button></a>` : '<span class="muted">항목 저장·실행 완료 후 검수</span>']])}
    </section>
    <section class="panel" id="rb-step-4"><h2>벤치마크 확정</h2><p class="muted">검수 완료 ${w.done}/${w.n_documents}건만 포함합니다. 이미지·추론 원본·질문·검수 정답을 복사해서 고정하며, 이후 수정은 새 버전으로 확정합니다.</p>
      <form id="rb-finalize" class="bar"><label>이름 <input id="rb-dataset-name" required value="${esc(name)}"></label><label>버전 <input id="rb-version" required value="v${w.snapshots.length + 1}" size="8"></label>
        <label><input type="checkbox" id="rb-classify">포맷 이름으로 문서 분류도 평가</label><button class="primary" id="rb-finalize-btn" ${running || !w.done ? "disabled" : ""}>검수 문서로 확정</button></form>
      ${w.snapshots.length ? table(w.snapshots, [["name", "이름"], ["version", "버전"], ["documents", "문서", null, true], ["at", "확정일"],
        ["go", "", s => `<a href="#/datasets/${q(s.dataset)}">데이터셋 보기</a> · <a href="#/eval">평가 보기</a>`]]) : ""}
    </section>`;
  $("#rb-reload").onclick = () => { if (!state.leave || state.leave()) { state.leave = null; rbWork(name); } };
  $$("[data-rb-anchor]").forEach(a => a.onclick = e => { e.preventDefault(); document.getElementById(a.dataset.rbAnchor).scrollIntoView({ behavior: "smooth", block: "start" }); });
  let dirty = false;
  state.leave = unload => !dirty || (unload ? false : confirm("저장하지 않은 추출 항목이 있습니다. 이동할까요?"));
  const clearAndReload = async () => { dirty = false; state.leave = null; await rbWork(name); };
  const action = (id, fn) => { const b = $(id); if (b) b.onclick = e => rbAction(e.currentTarget, fn); };
  action("#rb-ocr-retry", async () => { await api(`${url}/ocr`, {}); await clearAndReload(); });
  action("#rb-merge", async () => { await api(`${url}/grouping`, { action: "merge", src: $("#rb-merge-src").value, dst: $("#rb-merge-dst").value }); await clearAndReload(); });
  for (const [id, kind] of [["#rb-split", "split"], ["#rb-join", "document"]]) action(id, async () => {
    const documents = $$('[data-rb-doc]:checked').map(e => e.dataset.rbDoc);
    await api(`${url}/grouping`, { action: kind, documents, title: $("#rb-split-name").value }); await clearAndReload();
  });
  for (const panel of $$("[data-fid]")) {
    const f = w.formats.find(f => f.id === panel.dataset.fid), locked = f.with_pred > 0 || running;
    let fields = clone(f.schema ? f.schema.fields : [{ key: "", label: "", type: "text" }]);
    const render = () => {
      $("[data-rb-fields]", panel).innerHTML = fields.map((f, i) => `<tr><td><input data-key="${i}" value="${esc(f.key)}" placeholder="applicant_name" ${locked ? "disabled" : ""}></td>
        <td><input data-label="${i}" value="${esc(f.label)}" placeholder="신청인 성명" ${locked ? "disabled" : ""}></td>
        <td><select data-type="${i}" ${locked ? "disabled" : ""}>${Object.entries(RB_TYPES).map(([k, n]) => `<option value="${k}" ${f.type === k ? "selected" : ""}>${n}</option>`).join("")}</select></td>
        <td><button data-remove="${i}" ${locked ? "disabled" : ""}>삭제</button></td></tr>`).join("");
      for (const [attr, prop] of [["key", "key"], ["label", "label"], ["type", "type"]]) $$(`[data-${attr}]`, panel).forEach(e => e.oninput = () => {
        fields[+e.dataset[attr]][prop] = e.value; dirty = true; $("[data-rb-prompt]", panel).textContent = rbPromptPreview(fields);
      });
      $$("[data-remove]", panel).forEach(b => b.onclick = () => { fields.splice(+b.dataset.remove, 1); dirty = true; render(); });
    };
    render();
    const suggestionArea = $("[data-rb-key-results]", panel), suggestionStatus = $("[data-rb-key-status]", panel);
    const showSuggestions = result => {
      const suggestions = result.suggestions || [];
      suggestionStatus.textContent = `제안 ${suggestions.length}개 · ${result.model || ""} · 기존 키 후보 ${result.candidate_count}/${result.catalog_total}개. 선택 후 반영하고 추출 항목을 저장하세요.`;
      suggestionArea.innerHTML = `<div class="rb-key-table"><table><thead><tr><th>반영</th><th>문서 표시명</th><th>키·의미</th><th>구분</th><th>제안 이유</th></tr></thead><tbody>${suggestions.map((s, i) => `<tr>
        <td><input type="checkbox" data-rb-key-pick="${i}" aria-label="${esc(s.document_label)} 키 제안 선택" ${s.source === "existing" ? "checked" : ""} ${locked ? "disabled" : ""}></td>
        <td>${esc(s.document_label)}<div class="muted">${esc(s.label)}</div></td><td><code>${esc(s.key)}</code><div class="muted">${esc(s.meaning)} · ${esc(RB_TYPES[s.type])}</div></td>
        <td><span class="tag ${s.source === "existing" ? "ok" : "warn"}">${s.source === "existing" ? "기존 키" : "새 키 제안"}</span></td><td>${esc(s.reason)}</td></tr>`).join("")}</tbody></table></div>
        <button data-rb-apply-keys ${locked ? "disabled" : ""}>선택 제안을 항목에 반영</button><div class="muted">새 키는 자동 선택하지 않습니다. 반영해도 공통 키 사전에는 자동 등록되지 않습니다.</div>`;
      $("[data-rb-apply-keys]", panel).onclick = () => {
        const selected = $$('[data-rb-key-pick]:checked', panel).map(e => suggestions[+e.dataset.rbKeyPick]);
        if (!selected.length) { toast("반영할 제안을 선택하세요", true); return; }
        // 사용자 작성 항목은 보존한다. 키만 비어 있던 행은 해당 설명의 제안으로 채운다.
        const next = clone(fields);
        for (const s of selected) {
          const target = Number.isInteger(s.request_index) ? s.request_index : -1;
          const at = target >= 0 && target < next.length && (!next[target].label.trim() || next[target].label === (s.requested_label || s.document_label)) ? target
            : next.findIndex(f => f.key === s.key || (!f.key.trim() && f.label === (s.requested_label || s.document_label)));
          const item = { key: s.key, label: s.label, type: s.type };
          if (at >= 0) next[at] = item; else next.push(item);
        }
        const clean = next.filter(f => f.key.trim() || f.label.trim());
        if (new Set(clean.filter(f => f.key.trim()).map(f => f.key)).size !== clean.filter(f => f.key.trim()).length) {
          toast("같은 키가 중복됩니다. 제안 선택이나 기존 항목을 확인하세요", true); return;
        }
        fields = clean; dirty = true; render();
        $("[data-rb-prompt]", panel).textContent = rbPromptPreview(fields);
        toast(`${selected.length}개 제안을 반영했습니다. 확인 후 추출 항목을 저장하세요`);
      };
    };
    const loadSuggestions = async job => {
      if (!panel.isConnected) return;
      try {
        const result = await api(`${url}/key-suggestions/${q(job)}`);
        if (!panel.isConnected) return;
        if (result.status === "running") {
          suggestionStatus.textContent = "대표 문서와 키 개념·후보 목록을 VLM으로 보내 제안받고 있습니다…";
          $("[data-rb-suggest]", panel).disabled = true;
          setTimeout(() => loadSuggestions(job), 2000);
        } else if (result.status === "done") {
          $("[data-rb-suggest]", panel).disabled = locked || !providers.length;
          showSuggestions(result);
        } else {
          $("[data-rb-suggest]", panel).disabled = locked || !providers.length;
          suggestionStatus.textContent = `키 제안 실패: ${result.error || result.status}. 다시 실행할 수 있습니다.`;
        }
      } catch (e) {
        if (panel.isConnected) { suggestionStatus.textContent = e.message; $("[data-rb-suggest]", panel).disabled = locked || !providers.length; }
      }
    };
    if (f.key_suggestion_job) loadSuggestions(f.key_suggestion_job);
    $("[data-rb-suggest]", panel).onclick = async e => {
      const button = e.currentTarget; button.disabled = true;
      try {
        const result = await api(`${url}/schemas/${q(f.id)}/suggest-keys`, { provider: $("[data-rb-key-model]", panel).value, fields,
          document: $("[data-rb-key-sample]", panel).value });
        await loadSuggestions(result.job);
      } catch (e) { button.disabled = false; toast(e.message, true); }
    };
    $("[data-rb-title]", panel).oninput = () => { dirty = true; };
    $("[data-rb-add]", panel).onclick = () => { fields.push({ key: "", label: "", type: "text" }); dirty = true; render(); };
    $("[data-rb-save]", panel).onclick = e => rbAction(e.currentTarget, async () => {
      await api(`${url}/schemas/${q(f.id)}`, { name: $("[data-rb-title]", panel).value, fields }, "PUT");
      // 다른 포맷의 작성 중 항목은 그대로 둔다. 저장 상태만 갱신한다.
      f.schema = { name: $("[data-rb-title]", panel).value, fields: clone(fields) };
      $("[data-rb-schema-status]", panel).textContent = "저장했습니다. 다른 포맷도 저장한 뒤 새로고침하면 추론할 수 있습니다.";
      dirty = $$("[data-fid]").some(p => {
        const saved = w.formats.find(g => g.id === p.dataset.fid).schema;
        if (!saved) return $$('[data-key], [data-label]', p).some(e => e.value.trim());
        return $("[data-rb-title]", p).value !== saved.name || JSON.stringify($$('[data-key]', p).map((e, i) => ({ key: e.value, label: $$('[data-label]', p)[i].value, type: $$('[data-type]', p)[i].value }))) !== JSON.stringify(saved.fields);
      });
      if (!dirty) { state.leave = null; await rbWork(name); } else toast("저장했습니다. 다른 포맷의 작성 내용은 유지됩니다");
    });
  }
  action("#rb-infer", async () => {
    if (dirty) throw new Error("작성 중인 추출 항목을 먼저 저장하세요");
    const fid = $("#rb-infer-format").value;
    await api(`${url}/infer`, { provider: $("#rb-model").value, formats: fid ? [fid] : w.formats.filter(f => f.schema).map(f => f.id) });
    await clearAndReload();
  });
  $("#rb-finalize").onsubmit = e => { e.preventDefault(); rbAction($("#rb-finalize-btn"), async () => {
    if (dirty) throw new Error("작성 중인 추출 항목을 먼저 저장하세요");
    await api(`${url}/finalize`, { name: $("#rb-dataset-name").value, version: $("#rb-version").value, classify: $("#rb-classify").checked });
    toast("벤치마크를 확정했습니다"); await clearAndReload();
  }); };
  if (running) {
    const marker = $("#rb-jobs");
    const poll = async () => {
      if (!marker.isConnected) return;
      try {
        const latest = await api(url); if (!marker.isConnected) return;
        marker.innerHTML = rbJobPanel(latest.jobs);
        if (latest.jobs.some(j => j.status === "running")) setTimeout(poll, 2500);
        else if (!dirty) await clearAndReload();
        else { $("#rb-update").innerHTML = '<button id="rb-show-result" class="primary">작업 종료 · 결과 반영하기</button>'; $("#rb-show-result").onclick = () => { if (confirm("저장하지 않은 항목을 버리고 결과를 불러올까요?")) clearAndReload(); }; }
      } catch (e) { if (marker.isConnected) { $("#rb-update").textContent = e.message + " · 새로고침으로 다시 확인하세요"; } }
    };
    setTimeout(poll, 2000);
  }
}

function rbPromptPreview(fields) {
  return "각 항목의 값과 위치를 추출하세요. 위치는 0~1000 좌표와 1부터 시작하는 쪽 번호입니다.\n" + fields.map(f => `- ${f.key}: ${f.label} (${RB_TYPES[f.type] || f.type})`).join("\n")
    + '\n응답: [{"key":"…", "value":"…", "bbox_2d":[x0,y0,x1,y1], "page":1}]\n빈칸·찾지 못한 값은 null, 도장·서명은 true/false로 답하세요.';
}

async function rbReview(name, fid, doc) {
  const w = await api(rbUrl(name)), f = w.formats.find(f => f.id === fid);
  if (!f) throw new Error("포맷이 없습니다");
  if (w.jobs.some(j => j.status === "running")) { location.hash = rbHash(name); return; }
  const context = {
    header: rbHead(name) + `<div class="bar"><a href="${rbHash(name)}"><button>작업으로 돌아가기</button></a><b>${esc(f.schema ? f.schema.name : f.name)} · 검수 ${f.done}/${f.documents.length}</b><span class="muted">값이 있는 항목은 위치도 확인하세요. 빈칸은 값을 비워 둡니다.</span></div>`,
    load: async () => [await api(`${rbUrl(name)}/doc?doc=${q(doc)}`), { docs: f.documents }],
    saveUrl: `${rbUrl(name)}/doc?doc=${q(doc)}`, backHash: rbHash(name), docHash: d => `${rbHash(name)}/doc/${q(fid)}/${q(d)}`,
  };
  await viewLabelDoc(name, fid, doc, context);
}
