// 문항 Q/A: 실제 생성기의 prompt·answer·eval 계약과 고객별 문항을 함께 보여 준다 (DESIGN.md 9.3.1).
// ① 서식 › 문항 Q/A 탭(tabQuestions, forms.js 가 부름).
// 서버: GET /api/question-formats, POST /api/forms/{id}/questions (studio/app.py, studio/questions.py)
"use strict";

let questionFormatsPromise = null;
const loadQuestionFormats = () => questionFormatsPromise || (questionFormatsPromise = api("/api/question-formats").catch(e => { questionFormatsPromise = null; throw e; }));
const qaJSON = value => JSON.stringify(value, null, 2);

function questionContractHTML(c) {
  return `<p class="sub">${esc(c.notes)}</p>
    <details class="qa-contract"><summary>모든 서식 공통 질문 문장 (데이터의 <code>prompt</code>)</summary><pre class="ans mono">${esc(c.prompt_template)}</pre></details>
    <details class="qa-contract"><summary>정답의 꼴 (JSON Schema) · 예시</summary>
      <pre class="ans mono">${esc(qaJSON(c.answer_schema))}</pre><div class="muted">형식 설명용 예시</div><pre class="ans mono">${esc(qaJSON(c.example))}</pre></details>`;
}

// 정답 안의 위치 (kie·marks 칸, 표 행 row_boxes, 표 찾기): [{bbox (0~1000), page (1부터), title}]
function answerBoxes(answer) {
  const out = [];
  const walk = (x, title) => {
    if (Array.isArray(x)) return x.forEach((y, i) => walk(y, title));
    if (!x || typeof x !== "object") return;
    if (Array.isArray(x.bbox_2d) && x.bbox_2d.length === 4)
      out.push({ bbox: x.bbox_2d, page: x.page || 1, title: x.key ?? (x.columns ? `표 (${x.columns.join(", ")})` : title ?? "") });
    if (Array.isArray(x.row_boxes)) x.row_boxes.forEach((b, i) => walk(b, `${i + 1}행`));
    for (const [k, v] of Object.entries(x)) if (k !== "row_boxes" && typeof v === "object") walk(v, title);
  };
  walk(answer);
  return out;
}

// 입력 그림을 그대로 보이고 정답 위치를 겹친다 (누르면 원본 크기로 새 창)
function questionImagesHTML(item) {
  const boxes = answerBoxes(item.answer);
  return `<div class="qa-images">${item.image_urls.map((url, i) => {
    const mine = boxes.filter(b => b.page === i + 1);
    return `<a class="qa-page" href="${esc(url)}" target="_blank" rel="noopener" title="${item.image_urls.length > 1 ? `${i + 1}쪽 · ` : ""}원본 크기로 보기">
      <img src="${esc(url)}" alt="문항 입력 이미지 ${i + 1}" loading="lazy">
      ${mine.length ? `<svg viewBox="0 0 1000 1000" preserveAspectRatio="none">${mine.map(b => {
        const [x0, y0, x1, y1] = b.bbox;
        return `<rect x="${x0}" y="${y0}" width="${Math.max(2, x1 - x0)}" height="${Math.max(2, y1 - y0)}"><title>${esc(b.title)}</title></rect>`;
      }).join("")}</svg>` : ""}
      ${item.image_urls.length > 1 ? `<span class="qa-pno">${i + 1}쪽</span>` : ""}</a>`;
  }).join("")}</div>
  ${boxes.length ? `<div class="muted" style="font-size:12px">빨간 상자 = 정답 위치 ${boxes.length}개 (마우스를 올리면 키·행)</div>` : ""}`;
}

function questionItemsHTML(items) {
  return items.map(item => {
    const record = Object.fromEntries(["id", "task", "images", "prompt", "answer", "eval", "meta"].filter(k => k in item).map(k => [k, item[k]]));
    return `<article class="panel qa-item">
      <div class="bar"><span class="tag">${esc(item.task)}</span><span class="mono">${esc(item.id)}</span></div>
      ${questionImagesHTML(item)}
      <div class="qa-columns"><div><b>question → prompt</b><pre class="ans mono qa-prompt">${esc(item.prompt)}</pre></div>
        <div><b>answer (데이터 정답)</b><pre class="ans mono">${esc(qaJSON(item.answer))}</pre>
          <b>모델이 출력할 답 예시</b><pre class="ans mono">${esc(item.model_answer)}</pre></div></div>
      <details><summary>채점 조건 eval</summary><pre class="ans mono">${esc(qaJSON(item.eval || {}))}</pre></details>
      <details><summary>문항 레코드 JSON</summary><pre class="ans mono">${esc(qaJSON(record))}</pre></details>
    </article>`;
  }).join("");
}

async function tabQuestions(d) {
  const formats = await loadQuestionFormats();
  if (!$("#tab") || location.hash !== `#/forms/${encodeURIComponent(d.id)}/questions`) return;
  const tasks = ["classify", "ocr_field", "ocr_page", "kie", "marks", "freetext", "form_qa", "table", "table_read", "table_find", "table_qa"];
  let items = null, request = 0;
  const first = tasks.includes(state.qaTask) ? state.qaTask : "kie";   // 개요에서 과제를 눌러 왔으면 그 과제
  state.qaTask = null;
  const qf = d.questions;
  $("#tab").innerHTML = `<div class="sub">과제마다 모델이 실제로 받는 질문과 정답입니다. 가짜 고객(seed)·촬영 조건을 고르고 <b>실제 문항 예시 만들기</b>를 누릅니다 (한 번 그려서 만듦).</div>
    <details class="qa-contract"><summary>이 서식의 질문·답 바꾼 것 <span class="mono">${esc(qf ? qf.path : "questions.json 없음 — 모두 기본")}${d.qa ? " · qa.py" : ""}</span></summary>
      <div class="sub">질문 문장·질문 항목 줄 틀(item)·답 항목 틀(answer)은 공통 <span class="mono">docgen/forms/_common/questions.json</span>, 항목명은 칸의 항목명이 기본입니다.
        이 서식에서 다르게 할 것: 질문 문장 <code>prompt</code>·답 항목 틀 <code>answer</code>(JSON 틀 <code>{"key": "{key}", "value": "{value}"}</code> 또는 줄글 <code>"{label}: {value}"</code>)·분류 정답은 서식 폴더의 <span class="mono">questions.json</span>,
        이 서식만의 질문(form_qa)은 서식 폴더의 <span class="mono">qa.py</span> (함수 하나 = 질문 하나, 견본 <span class="mono">python -m docgen.formdir qa ${esc(d.id)} --new</span>),
        칸마다(묻지 않기 <code>ask: false</code>, 키 설명 <code>label</code>, 설명 <code>note</code>, OCR 빼기 <code>ocr: false</code>)는 칸 목록 <span class="mono">fields.json</span> 그 칸의 <code>"q"</code>.
        과제마다 묻는 칸은 <a href="#/forms/${encodeURIComponent(d.id)}/overview">개요</a>, 합친 전체와 고칠 줄은 <a href="#/forms/${encodeURIComponent(d.id)}/card">카드 원문</a>. 고친 뒤 아래에서 문항을 다시 만들어 확인합니다.
        검사: <span class="mono">python -m docgen.formdir check ${esc(d.id)}</span> · 설명: <a href="#/guide/${encodeURIComponent("docgen/forms/README.md")}">서식 폴더 설명서</a></div>
      ${qf ? `<pre class="ans mono" style="max-height:420px;overflow:auto">${esc(qf.source)}</pre>` : ""}
      ${d.qa ? `<div class="sub mono">${esc(d.qa.path)}</div><pre class="ans mono" style="max-height:420px;overflow:auto">${esc(d.qa.source)}</pre>` : ""}</details>
    <div class="bar">${optionBar(true, "qa")}
      <label>값 칸 OCR 문항 수 <input type="number" id="qa-fpd" value="6" min="0" max="50"></label>
      <label>최대 추출·표시 항목 수 <input type="number" id="qa-max" value="40" min="1" max="500"></label>
      <button type="button" class="primary" id="qa-build">실제 문항 예시 만들기</button><span id="qa-status" class="muted" role="status"></span></div>
    <div class="bar"><label>과제 <select id="qa-task">${tasks.map(t => `<option value="${t}" ${t === first ? "selected" : ""}>${esc(formats[t].name)} · ${t}</option>`).join("")}</select></label></div>
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
