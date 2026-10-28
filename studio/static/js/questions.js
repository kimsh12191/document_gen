// 문항 Q/A: 실제 생성기의 prompt·answer·eval 계약과 고객별 문항을 함께 보여 준다 (DESIGN.md 9.3.1).
// ① 서식 › 문항 Q/A 탭(tabQuestions, forms.js 가 부름)과 ③ 처리 설정의 Q/A 창(showQuestionQA, scenario-processing.js).
// 서버: GET /api/question-formats, POST /api/forms/{id}/questions (studio/app.py, studio/questions.py)
"use strict";

let questionFormatsPromise = null;
let questionDialog = null;
const loadQuestionFormats = () => questionFormatsPromise || (questionFormatsPromise = api("/api/question-formats").catch(e => { questionFormatsPromise = null; throw e; }));
const qaJSON = value => JSON.stringify(value, null, 2);

function questionContractHTML(c) {
  return `<p class="sub">${esc(c.notes)}</p>
    <details class="qa-contract"><summary>공통 question 템플릿 (데이터의 prompt)</summary><pre class="ans mono">${esc(c.prompt_template)}</pre></details>
    <details class="qa-contract"><summary>answer JSON Schema · 형식 예시</summary>
      <pre class="ans mono">${esc(qaJSON(c.answer_schema))}</pre><div class="muted">형식 설명용 예시</div><pre class="ans mono">${esc(qaJSON(c.example))}</pre></details>`;
}

function questionItemsHTML(items) {
  return items.map(item => {
    const record = Object.fromEntries(["id", "task", "images", "prompt", "answer", "eval", "meta"].filter(k => k in item).map(k => [k, item[k]]));
    return `<article class="panel qa-item">
      <div class="bar"><span class="tag">${esc(item.task)}</span><span class="mono">${esc(item.id)}</span></div>
      <details><summary>입력 이미지 ${item.image_urls.length}장</summary><div class="qa-images">${item.image_urls.map((url, i) =>
        `<a href="${esc(url)}" target="_blank" rel="noopener"><img src="${esc(url)}" alt="문항 입력 이미지 ${i + 1}" loading="lazy"></a>`).join("")}</div></details>
      <div class="qa-columns"><div><b>question → prompt</b><pre class="ans mono qa-prompt">${esc(item.prompt)}</pre></div>
        <div><b>answer (데이터 정답)</b><pre class="ans mono">${esc(qaJSON(item.answer))}</pre>
          <b>모델이 출력할 답 예시</b><pre class="ans mono">${esc(item.model_answer)}</pre></div></div>
      <details><summary>채점 조건 eval</summary><pre class="ans mono">${esc(qaJSON(item.eval || {}))}</pre></details>
      <details><summary>문항 레코드 JSON</summary><pre class="ans mono">${esc(qaJSON(record))}</pre></details>
    </article>`;
  }).join("");
}

async function showQuestionQA(task, items = [], title = "", note = "") {
  const formats = await loadQuestionFormats();
  if (questionDialog) questionDialog.close();
  const dialog = document.createElement("dialog");
  questionDialog = dialog;
  dialog.className = "qa-dialog";
  const tasks = [...new Set([task, ...items.map(x => x.task)])];
  dialog.innerHTML = `<div class="bar"><h2>${esc(title || formats[task].name)} · Q/A 포맷·예시</h2><button type="button" class="qa-close">닫기 ×</button></div>
    ${note ? `<p class="qa-notice">${esc(note)}</p>` : ""}
    ${tasks.map(t => `<h3>${esc(formats[t].name)} <span class="mono muted">${esc(t)}</span></h3>${questionContractHTML(formats[t])}`).join("")}
    ${items.length ? questionItemsHTML(items) : `<p class="muted">현재 고객의 실행 가능한 문항 예시가 없습니다. 위에서 공통 질문과 정답 형식을 확인하세요.</p>`}`;
  $(".qa-close", dialog).onclick = () => dialog.close();
  dialog.addEventListener("close", () => { if (questionDialog === dialog) questionDialog = null; dialog.remove(); });
  document.body.appendChild(dialog);
  dialog.showModal();
  $(".qa-close", dialog).focus();
}

async function tabQuestions(d) {
  const formats = await loadQuestionFormats();
  if (!$("#tab") || location.hash !== `#/forms/${encodeURIComponent(d.id)}/questions`) return;
  const tasks = ["classify", "ocr_field", "ocr_page", "kie", "marks"];
  let items = null, request = 0;
  $("#tab").innerHTML = `<div class="sub">각 과제가 모델에 묻는 question은 실제 데이터의 <code>prompt</code>입니다.
      공통 형식과 선택한 고객의 문항을 함께 확인합니다.</div>
    <div class="bar">${optionBar(true, "qa")}
      <label>값 칸 OCR 문항 수 <input type="number" id="qa-fpd" value="6" min="0" max="50"></label>
      <label>최대 추출·표시 항목 수 <input type="number" id="qa-max" value="40" min="1" max="500"></label>
      <button type="button" class="primary" id="qa-build">실제 문항 예시 만들기</button><span id="qa-status" class="muted" role="status"></span></div>
    <div class="bar"><label>과제 <select id="qa-task">${tasks.map(t => `<option value="${t}" ${t === "kie" ? "selected" : ""}>${esc(formats[t].name)} · ${t}</option>`).join("")}</select></label></div>
    <div id="qa-contract-box"></div><div id="qa-examples"></div>`;
  const draw = () => {
    const task = $("#qa-task").value;
    $("#qa-contract-box").innerHTML = questionContractHTML(formats[task]);
    const selected = items?.filter(item => item.task === task);
    $("#qa-examples").innerHTML = selected ? (questionItemsHTML(selected) || `<p class="muted">이 고객의 서식·생성 옵션에서는 해당 과제 문항이 없습니다. 필요한 값·위치·표시 항목이 있는지 확인하세요.</p>`)
      : `<p class="muted">위 버튼을 누르면 실제 생성기가 만드는 질문 전문과 정답·채점 조건이 나타납니다.</p>`;
  };
  $("#qa-task").onchange = draw;
  $$("input, select", $("#tab")).filter(el => el.id !== "qa-task").forEach(el => el.addEventListener("change", () => {
    request++; items = null; $("#qa-status").textContent = "생성 조건이 바뀌었습니다. 문항 예시를 다시 만들어 주세요.";
    $("#qa-build").disabled = false; draw();
  }));
  $("#qa-build").onclick = async () => {
    if ($$("input", $("#tab")).some(inp => !inp.reportValidity())) return;
    const token = ++request, box = $("#tab"), button = $("#qa-build"), status = $("#qa-status");
    button.disabled = true; status.textContent = "문항 생성 중…";
    try {
      const o = readOptions(true, "qa");
      const result = await api(`/api/forms/${encodeURIComponent(d.id)}/questions`, { ...o, fields_per_doc: +$("#qa-fpd").value, max_keys: +$("#qa-max").value });
      if (!box.isConnected || request !== token) return;
      items = result.items; status.textContent = `seed ${result.seed} · 문항 ${items.length}개`; draw();
    } catch (e) { if (box.isConnected && request === token) status.textContent = e.message; }
    finally { if (box.isConnected && request === token) button.disabled = false; }
  };
  draw();
}
