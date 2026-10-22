// ⑥ 데이터셋 (등록부·설명서·문항 보기·모델 답 붙이기·채점·업무 묶음·학습 설정) · ⑦ 평가 (비교표).
// 생성 현황 목록은 dataset-builds.js, 새로 만들기(레시피)는 recipes.js.
// 서버: studio/api_datasets.py·datasets.py (등록부·채점), studio/api_bank.py·bank_data.py·training_link.py (업무 묶음·학습)
"use strict";

addRoute(/^#\/datasets\/([^/]+)\/bundle\/(.+)$/, (id, bid) => viewBundle(decodeURIComponent(id), decodeURIComponent(bid)), "datasets");
addRoute(/^#\/datasets\/([^/]+)(?:\/(\w+))?$/, (id, tab) => viewDataset(decodeURIComponent(id), tab || "card"), "datasets");

const GROUP_NAME = { ocr: "OCR", doc: "문서 이해", work: "업무 처리" };   // 과제 묶음 (docgen.bench.evaluate.TASK_GROUP)
const TASK_GROUP = { crop_ocr: "ocr", bbox_ocr: "ocr", region_ocr: "ocr", marked_ocr: "ocr", grounding: "ocr", spotting: "ocr",
  relation: "ocr", marked_box: "ocr", ocr_field: "ocr", ocr_page: "ocr", classify: "doc", kie: "doc", marks: "doc",
  doc_check: "work", cross_check: "work", review: "work" };
const TASK_KO = {
  crop_ocr: "잘라낸 글자 읽기", bbox_ocr: "박스 안 글자", region_ocr: "영역 받아쓰기", marked_ocr: "그린 박스 글자",
  grounding: "글자 위치 찾기", spotting: "전체 글자+위치", relation: "옆 글자 찾기", marked_box: "그린 박스 위치",
  ocr_field: "값 칸 인식", ocr_page: "전체 받아쓰기", classify: "서류 분류", kie: "정보 추출", marks: "체크·도장·서명",
  doc_check: "서류 구비", cross_check: "서류 대조", review: "심사 질의",
};
const LOWER_BETTER = new Set(["cer", "false_alarm", "matched_label_cer"]);
const dsTag = d => (d.groups || []).map(g => `<span class="tag ${g === "ocr" ? "html" : g === "doc" ? "overlay" : ""}">${GROUP_NAME[g] || esc(g)}</span>`).join(" ");

async function view_datasets() {
  const [r, recipes, trainings] = await Promise.all([api("/api/datasets"), recipesPanel(), trainingsPanel()]);
  if (location.hash !== "#/datasets") return;
  main().innerHTML = `
    <h1>데이터셋</h1>
    <div class="sub">OCR·문서 이해·업무 처리 과제를 같은 형식(과제 폴더)으로, 출처와 정답 종류와 함께 한 목록으로 관리합니다.
      명령줄로 만든 폴더도 경로만 등록하면 됩니다 (studio 는 읽기만 합니다). 등록부: <span class="mono">${esc(r.workspace)}/registry.json</span></div>
    <div class="panel" style="margin-bottom:12px">
      <b>폴더 등록</b>
      <div class="bar" style="margin-top:6px">
        <input type="text" id="dr-path" placeholder="폴더 경로 (과제 폴더: docgen.bench build · OCR 준비 결과)" style="width:520px">
        <input type="text" id="dr-name" placeholder="이름 (비우면 폴더 이름)" style="width:200px">
        <select id="dr-source"><option value="">출처: 자동</option>${Object.entries(r.sources).map(([k, n]) => `<option value="${k}">${n}</option>`).join("")}</select>
        <select id="dr-gt"><option value="">정답: 자동</option>${Object.entries(r.gts).map(([k, n]) => `<option value="${k}">${n}</option>`).join("")}</select>
        <label><input type="checkbox" id="dr-real"> 실서류</label>
        <button class="primary" id="dr-go">등록</button>
      </div>
    </div>
    ${recipes}
    <div id="dataset-build-jobs"></div>
    <section id="ds-registry"><div class="bar"><h2>등록된 데이터셋</h2><span id="ds-reg-status" class="muted">${r.datasets.length}개 등록</span>
      <button type="button" id="ds-refresh">목록 새로고침</button></div><div id="ds-list">${datasetRegistryHTML(r)}</div></section>
    ${trainings}`;
  bindRecipesPanel();
  $("#dr-go").onclick = async () => {
    try {
      const d = await api("/api/datasets", { path: $("#dr-path").value.trim(), name: $("#dr-name").value.trim(),
        source: $("#dr-source").value || null, gt: $("#dr-gt").value || null, real_data: $("#dr-real").checked || null });
      location.hash = `#/datasets/${encodeURIComponent(d.id)}`;
    } catch (e) { toast(e.message, true); }
  };
  startDatasetDashboard(r);
}

async function viewDataset(id, tab) {
  const d = await api(`/api/datasets/${encodeURIComponent(id)}`);
  const tabs = [["card", "설명서"], ["tracking", "구성·추적"], ["items", "문항"], ...((d.groups || []).includes("work") ? [["bundles", "업무 묶음"]] : []),
    ["runs", `모델 답 (${d.predictions.length})`], ["train", "학습"]];
  main().innerHTML = `
    <div class="muted"><a href="#/datasets">데이터셋</a></div>
    <h1>${esc(d.name)} <span class="mono muted">${esc(d.id)}</span></h1>
    <div>${dsTag(d)} <span class="tag">${esc(d.format)}</span> <span class="tag">출처: ${esc(d.source)}</span>
      <span class="tag">정답: ${esc(d.gt)}</span> ${d.real_data ? `<span class="tag warn">실서류</span>` : ""}
      ${d.frozen ? `<span class="tag ok">고정</span>` : ""} ${d.exists ? "" : `<span class="tag warn">폴더 없음</span>`}
      <span class="sep"></span><button id="ds-freeze">${d.frozen ? "고정 풀기" : "고정"}</button>
      <button id="ds-unreg">등록 지우기</button></div>
    <div class="sub mono" style="margin-top:4px">${esc(d.path)}</div>
    <div class="tabs">${tabs.map(([t, n]) => `<a href="#/datasets/${encodeURIComponent(id)}/${t}" class="${t === tab ? "on" : ""}">${n}</a>`).join("")}</div>
    <div id="tab"></div>`;
  $("#ds-freeze").onclick = async () => { await api(`/api/datasets/${encodeURIComponent(id)}/freeze`, { frozen: !d.frozen }); viewDataset(id, tab); };
  $("#ds-unreg").onclick = async () => {
    if (!confirm("등록부에서만 지웁니다 (폴더와 파일은 그대로). 지울까요?")) return;
    await api(`/api/datasets/${encodeURIComponent(id)}`, undefined, "DELETE");
    location.hash = "#/datasets";
  };
  if (tab === "items") return dsItems(d);
  if (tab === "tracking") return dsTracking(d);
  if (tab === "runs") return dsRuns(d);
  if (tab === "bundles") return dsBundles(d);
  if (tab === "train") return dsTrain(d);
  return dsCard(d);
}

// 설명서 -------------------------------------------------------------------
function mdToHtml(md) {   // 설명서에 쓰는 만큼만 (제목, 목록, 표, 굵게, 코드)
  const inline = s => esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/`(.+?)`/g, "<code>$1</code>");
  const out = [];
  let tbl = null;
  for (const line of md.split("\n")) {
    if (line.startsWith("|")) {
      const cells = line.split("|").slice(1, -1).map(c => c.trim());
      if (cells.every(c => /^-+:?$|^:?-+$/.test(c))) continue;
      if (!tbl) { tbl = []; out.push(tbl); }
      tbl.push(cells);
      continue;
    }
    tbl = null;
    if (line.startsWith("# ")) out.push(`<h2>${inline(line.slice(2))}</h2>`);
    else if (line.startsWith("## ")) out.push(`<h3>${inline(line.slice(3))}</h3>`);
    else if (line.startsWith("- ")) out.push(`<li>${inline(line.slice(2))}</li>`);
    else if (line.trim()) out.push(`<p>${inline(line)}</p>`);
  }
  return out.map(x => Array.isArray(x) ? `<table>${x.map((r, i) => `<tr>${r.map(c => i ? `<td>${inline(c)}</td>` : `<th>${inline(c)}</th>`).join("")}</tr>`).join("")}</table>` : x).join("");
}

function dsCard(d) {
  const c = d.card || {};
  $("#tab").innerHTML = `
    <div class="viewer" style="grid-template-columns:minmax(0,1fr) 420px">
      <div class="panel card-md">${mdToHtml(d.card_md)}</div>
      <div class="panel">
        <b>사람이 쓰는 칸</b>
        <label class="fld">목적 <textarea id="cd-purpose" rows="3">${esc(c.purpose || "")}</textarea></label>
        <label class="fld">쓰면 안 되는 곳 <textarea id="cd-notfor" rows="2">${esc(c.not_for || "")}</textarea></label>
        <label class="fld">알려진 한계 <textarea id="cd-limits" rows="4">${esc(c.limits || "")}</textarea></label>
        <div class="bar"><button class="primary" id="cd-save">설명서 저장</button></div>
        <div class="muted" style="font-size:12px">파일: <span class="mono">${esc(d.card_file)}</span>. 구성·점수·쓴 학습은 자동으로 채웁니다.</div>
      </div>
    </div>`;
  $("#cd-save").onclick = async () => {
    try {
      await api(`/api/datasets/${encodeURIComponent(d.id)}/card`,
        { purpose: $("#cd-purpose").value, not_for: $("#cd-notfor").value, limits: $("#cd-limits").value }, "PUT");
      toast("저장했습니다"); viewDataset(d.id, "card");
    } catch (e) { toast(e.message, true); }
  };
}

// 문항 보기 -----------------------------------------------------------------
function parseBoxes(text) {   // 모델 답에서 [{"bbox_2d": [...], "label": ...}] 꺼내기
  if (typeof text !== "string") return [];
  let t = text.trim().replace(/^<think>\s*<\/think>\s*/, "");
  const m = t.match(/```(?:json)?\s*([\s\S]*?)```/);
  if (m) t = m[1];
  try {
    const v = JSON.parse(t);
    return Array.isArray(v) ? v.filter(x => x && Array.isArray(x.bbox_2d) && x.bbox_2d.length === 4) : [];
  } catch { return []; }
}

function itemStage(d, it, img, k) {
  const url = `/api/datasets/${encodeURIComponent(d.id)}/file?p=${encodeURIComponent(img)}`;
  const rects = [];
  for (const b of it.boxes.filter(b => b.img === k)) {
    const [x0, y0, x1, y1] = b.box;
    rects.push(`<rect class="ds-${b.cls}" x="${x0}" y="${y0}" width="${Math.max(1, x1 - x0)}" height="${Math.max(1, y1 - y0)}"><title>${esc(b.label)}</title></rect>`);
  }
  if (k === 0) it.preds.forEach((p, pi) => {
    for (const b of parseBoxes(p.output)) {
      const [x0, y0, x1, y1] = b.bbox_2d;
      rects.push(`<rect class="ds-pred p${pi % 3}" x="${x0}" y="${y0}" width="${Math.max(1, x1 - x0)}" height="${Math.max(1, y1 - y0)}"><title>${esc(p.label)}: ${esc(b.label || "")}</title></rect>`);
    }
  });
  return `<div class="stage ds-stage"><img src="${url}" alt="" loading="lazy"><svg viewBox="0 0 1000 1000" preserveAspectRatio="none">${rects.join("")}</svg></div>`;
}

const showAns = a => typeof a === "string" ? esc(a) : `<pre class="ans">${esc(JSON.stringify(a, null, 1))}</pre>`;

async function dsItems(d) {
  const st = store.get(`ds.${d.id}`, { task: Object.keys(d.tasks)[0] || "", pids: [], order: "id" });
  const tasks = Object.entries(d.tasks);
  const summary = await api(`/api/datasets/${encodeURIComponent(d.id)}/composition`).catch(() => null);
  st.filters ||= {};
  $("#tab").innerHTML = `
    ${summary ? '' : '<p class="warn">현재 서버에는 구성·추적 API가 없습니다. Studio를 재시작하면 구분별 필터를 사용할 수 있습니다.</p>'}
    <div class="bar">
      <select id="it-task"><option value="" ${st.task === "" ? "selected" : ""}>과제 전체</option>${tasks.map(([t, n]) => `<option value="${t}" ${t === st.task ? "selected" : ""}>${esc(TASK_KO[t] || t)} (${t}) · ${n}</option>`).join("")}</select>
      <input type="text" id="it-q" placeholder="문항 안 글자 검색" style="width:180px">
      <span class="muted">모델 답:</span>
      ${d.predictions.map(p => `<label><input type="checkbox" data-pid="${p.pid}" ${st.pids.includes(p.pid) ? "checked" : ""}> ${esc(p.label)}</label>`).join("") || `<span class="muted">(없음 — 모델 답 탭에서 붙입니다)</span>`}
      <label>순서 <select id="it-order"><option value="id">ID 순</option><option value="worst" ${st.order === "worst" ? "selected" : ""}>첫 답 점수 낮은 것부터</option></select></label>
      <span class="muted" id="it-stat"></span>
    </div>
    <div class="bar">${["task_group", "scenario", "label_format", "doc_type"].map(key => `<label>${TRACKING_TITLE[key]} <select data-track-filter="${key}" ${summary?'':'disabled'}><option value="">전체</option>${Object.keys(summary?.all.by[key] || {}).map(v => `<option value="${esc(v)}" ${st.filters[key] === v ? "selected" : ""}>${esc(trackName(v))}</option>`).join("")}</select></label>`).join("")}<label><input type="checkbox" id="it-evaluation-only" ${summary?'':'disabled'} ${st.evaluationOnly?'checked':''}> 평가 문항만</label><button id="it-clear-filters">필터 초기화</button></div>
    <div class="keys-help">초록 박스 = 정답, 파랑 점선 = 질문 영역, 주황·보라·청록 = 모델 답. 점수는 채점한 뒤에 보입니다 (모델 답 탭).</div>
    <div id="it-list"></div>
    <div class="bar"><button id="it-prev">◀ 이전</button><button id="it-next">다음 ▶</button></div>`;
  let offset = 0;
  const load = async () => {
    st.task = $("#it-task").value; st.order = $("#it-order").value;
    st.pids = $$("[data-pid]").filter(x => x.checked).map(x => x.dataset.pid);
    st.filters = Object.fromEntries($$("[data-track-filter]").map(x => [x.dataset.trackFilter, x.value]));
    st.evaluationOnly = $("#it-evaluation-only").checked;
    store.set(`ds.${d.id}`, st);
    $("#it-stat").textContent = "읽는 중…";
    try {
      const r = await api(`/api/datasets/${encodeURIComponent(d.id)}/items?task=${encodeURIComponent(st.task)}&offset=${offset}&limit=10` +
        `&pids=${st.pids.join(",")}&order=${st.order}&evaluation_only=${st.evaluationOnly}&q=${encodeURIComponent($("#it-q").value.trim())}&${new URLSearchParams(st.filters)}`);
      $("#it-stat").textContent = `${r.total}개 중 ${r.total ? offset + 1 : 0}–${Math.min(r.total, offset + 10)}`;
      $("#it-list").innerHTML = r.items.map(it => `
        <div class="panel ds-item">
          <div class="muted mono" style="font-size:12px">${esc(it.id)} ${Object.entries(it.meta || {}).slice(0, 6).map(([k, v]) => `<span class="tag">${esc(k)}: ${esc(v)}</span>`).join("")}</div>
          <div class="ds-row">
            <div class="ds-imgs">${it.images.slice(0, 13).map((im, k) => itemStage(d, it, im, k)).join("")}</div>
            <div class="ds-text">
              <div class="muted">질문</div><div class="prompt">${esc(it.prompt)}</div>
              <div class="muted">정답</div><div>${showAns(it.answer)}</div>
              ${it.preds.map(p => `<div class="muted">${esc(p.label)} ${p.score === null || p.score === undefined ? "" : `· 문항 점수 <b>${(p.score * 100).toFixed(0)}</b>`}</div>
                <div>${p.output === null || p.output === undefined ? `<span class="muted">(답 없음)</span>` : `<pre class="ans">${esc(p.output)}</pre>`}</div>`).join("")}
            </div>
          </div>
        </div>`).join("") || `<p class="muted">문항이 없습니다.</p>`;
      $("#it-prev").disabled = offset === 0;
      $("#it-next").disabled = offset + 10 >= r.total;
    } catch (e) { $("#it-stat").innerHTML = `<span class="err">${esc(e.message)}</span>`; }
  };
  $("#it-task").onchange = () => { offset = 0; load(); };
  $("#it-order").onchange = () => { offset = 0; load(); };
  $("#it-q").onchange = () => { offset = 0; load(); };
  $$("[data-track-filter]").forEach(x => x.onchange = () => { offset = 0; load(); });
  $("#it-evaluation-only").onchange = () => { offset = 0; load(); };
  $("#it-clear-filters").onclick = () => { $$("[data-track-filter]").forEach(x => { x.value = ""; }); $("#it-evaluation-only").checked = false; offset = 0; load(); };
  $$("[data-pid]").forEach(x => x.onchange = () => { offset = 0; load(); });
  $("#it-prev").onclick = () => { offset = Math.max(0, offset - 10); load(); };
  $("#it-next").onclick = () => { offset += 10; load(); };
  load();
}

// 모델 답 ------------------------------------------------------------------
function scoreTable(rows, tasks) {
  return `<table><thead><tr><th>모델 답</th><th>채점</th>${tasks.map(t => `<th class="num" title="${t}">${esc(TASK_KO[t] || t)}</th>`).join("")}</tr></thead>
    <tbody>${rows.map(s => `<tr><td>${esc(s.label)}${s.dataset_name ? ` <span class="muted">· ${esc(s.dataset_name)}</span>` : ""}</td>
      <td class="muted nw">${esc(s.scored_at || "")}${s.answered !== undefined ? ` · 답 ${s.answered}/${s.n}` : ""}</td>
      ${tasks.map(t => { const m = (s.main || {})[t]; return `<td class="num" title="${m ? esc(m.metric) : ""}">${m && m.value !== null && m.value !== undefined ?
        `${pct(m.value)}${LOWER_BETTER.has(m.metric) ? "<sup>↓</sup>" : ""}` : "-"}</td>`; }).join("")}</tr>`).join("")}</tbody></table>`;
}

async function dsRuns(d) {
  const reps = await api(`/api/datasets/${encodeURIComponent(d.id)}/reports`).catch(() => ({ reports: [] }));
  const tasks = Object.keys(d.tasks);
  $("#tab").innerHTML = `
    <div class="panel" style="margin-bottom:12px"><b>모델 답 붙이기</b>
      <div class="bar" style="margin-top:6px"><input type="text" id="rn-path" style="width:560px"
        placeholder="runs/<실험>/ (학습 실행 train/) · 예측 폴더 (docgen.bench run) · 답 파일 .jsonl">
        <input type="text" id="rn-label" placeholder="이름 (선택)" style="width:160px"><button class="primary" id="rn-go">붙이기</button></div>
      <div class="muted" style="font-size:12px">줄마다 {"id", "prediction"} 또는 {"id", "output"}. 붙인 폴더에는 쓰지 않습니다.</div></div>
    <h2>모델 답 ${d.predictions.length}개</h2>
    ${d.predictions.length ? table(d.predictions, [["label", "이름"], ["run", "붙인 결과"], ["path", "파일", p => `<span class="mono muted" style="font-size:12px">${esc(p.path)}</span>`],
      ["act", "", p => `<button data-score="${p.pid}">${d.scores.some(s => s.pid === p.pid) ? "다시 채점" : "채점"}</button>
        <a href="#/datasets/${encodeURIComponent(d.id)}/items" data-look="${p.pid}">문항 보기</a>`]]) : `<p class="muted">붙인 모델 답이 없습니다.</p>`}
    <h2>studio 채점 결과 <span class="muted" style="font-weight:400;font-size:13px">명령줄 채점·학습 보상과 같은 함수 (docgen.bench.evaluate)</span></h2>
    ${d.scores.length ? scoreTable(d.scores, tasks) : `<p class="muted">아직 채점하지 않았습니다.</p>`}
    ${d.gt === "pseudo" ? `<p class="muted">정답이 의사정답이라 점수는 "사내 OCR·추론과 얼마나 같은지"입니다.</p>` : ""}
    <h2>파이프라인이 낸 점수 파일</h2>
    ${reps.reports.length ? reps.reports.map(r => `<details class="panel"><summary>${esc(r.name)} <span class="muted mono">${esc(r.file)}</span></summary>
      ${table(Object.entries(r.tasks).map(([t, m]) => ({ t, m })), [["t", "과제", x => esc(TASK_KO[x.t] || x.t)],
        ["m", "지표", x => Object.entries(x.m.metrics || x.m).filter(([, v]) => typeof v === "number").slice(0, 8)
          .map(([k, v]) => `${esc(k)} ${v <= 1 ? pct(v) : v}`).join(" · ")]])}</details>`).join("") : `<p class="muted">없음</p>`}`;
  $("#rn-go").onclick = async () => {
    try {
      await api(`/api/datasets/${encodeURIComponent(d.id)}/runs`, { path: $("#rn-path").value.trim(), label: $("#rn-label").value.trim() });
      toast("붙였습니다"); viewDataset(d.id, "runs");
    } catch (e) { toast(e.message, true); }
  };
  $("#tab").onclick = async e => {
    const pid = e.target.dataset.score, look = e.target.dataset.look;
    if (look) { const st = store.get(`ds.${d.id}`, { task: tasks[0], pids: [], order: "id" }); st.pids = [look]; st.order = "worst"; store.set(`ds.${d.id}`, st); return; }
    if (!pid) return;
    e.target.disabled = true; e.target.textContent = "채점 중…";
    try { await api(`/api/datasets/${encodeURIComponent(d.id)}/score`, { pid }); toast("채점했습니다"); viewDataset(d.id, "runs"); }
    catch (err) { toast(err.message, true); e.target.disabled = false; }
  };
}

// ⑦ 평가: 여러 데이터셋의 점수를 한 표로 ------------------------------------------
async function view_eval() {
  const r = await api("/api/datasets");
  const sel = store.get("eval.ids", r.datasets.filter(d => d.n_scores).map(d => d.id));
  main().innerHTML = `
    <h1>평가</h1>
    <div class="sub">채점한 모델 답을 데이터셋끼리 나란히 봅니다: 모델끼리, 버전끼리, 합성·실서류, 의사정답·검수 정답.
      채점은 데이터셋 화면의 모델 답 탭에서 합니다.</div>
    <div class="panel" style="margin-bottom:12px">${r.datasets.length ? r.datasets.map(d => `<label style="margin-right:12px">
      <input type="checkbox" data-ds="${esc(d.id)}" ${sel.includes(d.id) ? "checked" : ""}> ${dsTag(d)} ${esc(d.name)}
      <span class="muted">(${esc(d.source)}·${esc(d.gt)}${d.real_data ? "·실서류" : ""}, 점수 ${d.n_scores})</span></label>`).join("")
      : `<span class="muted">등록된 데이터셋이 없습니다 (⑥ 데이터셋).</span>`}</div>
    <div id="ev-out"></div>`;
  const draw = async () => {
    const ids = $$("[data-ds]").filter(x => x.checked).map(x => x.dataset.ds);
    store.set("eval.ids", ids);
    if (!ids.length) { $("#ev-out").innerHTML = ""; return; }
    const c = await api(`/api/compare?ids=${ids.map(encodeURIComponent).join(",")}`);
    const out = [];
    for (const g of ["ocr", "doc", "work"]) {   // 과제 묶음마다 표 하나 (한 데이터셋이 여러 묶음에 걸칠 수 있다)
      const tasks = [...new Set(c.rows.flatMap(x => Object.keys(x.main || {})))].filter(t => (TASK_GROUP[t] || "doc") === g);
      const rows = c.rows.filter(x => tasks.some(t => (x.main || {})[t]));
      if (rows.length) out.push(`<h2>${GROUP_NAME[g]}</h2>${scoreTable(rows, tasks)}`);
    }
    $("#ev-out").innerHTML = out.join("") || `<p class="muted">고른 데이터셋에 채점 결과가 없습니다.</p>`;
  };
  $$("[data-ds]").forEach(x => x.onchange = draw);
  draw();
}


// 업무 묶음 -----------------------------------------------------------------
async function dsBundles(d) {
  const r = await api(`/api/datasets/${encodeURIComponent(d.id)}/bundles`);
  if (!r.bundles.length) {
    $("#tab").innerHTML = `<p class="muted">bundles.jsonl 이 없습니다. 묶음 기록은 2026-10-20 이후 만든 데이터셋에 들어 있습니다 (다시 만들면 생김).</p>`;
    return;
  }
  const scs = [...new Set(r.bundles.map(b => b.scenario))];
  $("#tab").innerHTML = `
    <div class="bar"><select id="bd-sc"><option value="">시나리오 전체</option>${scs.map(s => `<option>${esc(s)}</option>`).join("")}</select>
      <label><input type="checkbox" id="bd-t"> 변조 있음</label><label><input type="checkbox" id="bd-m"> 빠진 서류 있음</label>
      <label><input type="checkbox" id="bd-o"> 타인 서류</label><label><input type="checkbox" id="bd-c"> 직접 만든 묶음</label>
      <span class="muted" id="bd-n"></span></div><div id="bd-list"></div>`;
  const draw = () => {
    const sc = $("#bd-sc").value;
    const rows = r.bundles.filter(b => (!sc || b.scenario === sc) && (!$("#bd-t").checked || b.tampered) &&
      (!$("#bd-m").checked || b.missing) && (!$("#bd-o").checked || b.other) && (!$("#bd-c").checked || b.custom));
    $("#bd-n").textContent = `${rows.length}묶음`;
    $("#bd-list").innerHTML = table(rows, [
      ["bundle_id", "묶음", b => `<a href="#/datasets/${encodeURIComponent(d.id)}/bundle/${encodeURIComponent(b.bundle_id)}" class="mono">${esc(b.bundle_id)}</a>${b.custom ? ` <span class="tag">직접</span>` : ""}`],
      ["task_name", "업무"], ["customer", "고객"], ["n_docs", "서류", null, 1], ["n_pages", "쪽", null, 1], ["n_items", "문항", null, 1],
      ["missing", "빠짐", null, 1], ["other", "타인", null, 1], ["extra", "불필요", null, 1], ["tampered", "변조", null, 1],
      ["conditions", "촬영", b => b.conditions.map(c => esc(COND_NAME[c] || c)).join(" ")]]);
  };
  ["#bd-sc", "#bd-t", "#bd-m", "#bd-o", "#bd-c"].forEach(s => $(s).onchange = draw);
  draw();
}

// 그림 위 픽셀 박스: 이미지가 읽히면 원래 크기로 viewBox 를 맞춘다
function pxStage(url, boxes) {
  const id = "px" + Math.random().toString(36).slice(2, 8);
  setTimeout(() => {
    const img = document.getElementById(id);
    if (!img) return;
    const go = () => {
      const svg = img.nextElementSibling;
      svg.setAttribute("viewBox", `0 0 ${img.naturalWidth} ${img.naturalHeight}`);
      svg.innerHTML = boxes.map(b => `<rect class="${b.cls}" x="${b.bbox[0]}" y="${b.bbox[1]}" width="${Math.max(2, b.bbox[2] - b.bbox[0])}" height="${Math.max(2, b.bbox[3] - b.bbox[1])}"><title>${esc(b.title || "")}</title></rect>`).join("");
    };
    if (img.complete && img.naturalWidth) go(); else img.onload = go;
  }, 0);
  return `<div class="stage ds-stage"><img id="${id}" src="${url}" alt="" loading="lazy"><svg preserveAspectRatio="none"></svg></div>`;
}

async function viewBundle(id, bid) {
  const [d, b] = await Promise.all([api(`/api/datasets/${encodeURIComponent(id)}`), api(`/api/datasets/${encodeURIComponent(id)}/bundles/${encodeURIComponent(bid)}`)]);
  const file = p => `/api/datasets/${encodeURIComponent(id)}/file?p=${encodeURIComponent(p)}`;
  const dc = b.doc_check || {};
  const base = b.docs.filter(x => !x.why), extra = b.docs.filter(x => x.why);
  const sel = { what: null };
  const draw = () => {
    const hits = sel.what ? (b.profile.find(p => p.what === sel.what)?.where || []) : [];
    const warn = b.consistency;
    const docCard = x => {
      const boxes = [];
      for (const h of hits.filter(h => h.doc_id === x.doc_id)) if (h.bbox) boxes.push({ page: h.page || 0, bbox: h.bbox, cls: "ds-gt", title: `${h.key} = ${h.value}` });
      for (const w of warn.filter(w => w.doc_id === x.doc_id)) if (w.bbox) boxes.push({ page: w.page || 0, bbox: w.bbox, cls: "ds-warn", title: `${w.key}: ${w.value} (프로필: ${w.expected})` });
      const st = dc.missing?.includes(x.doc_id) ? `<span class="tag warn">빠짐</span>` : x.why === "other_customer" ? `<span class="tag warn">타인 서류</span>`
        : x.why === "extra" ? `<span class="tag">불필요 서류</span>` : "";
      return `<div class="panel bd-doc"><div class="bar"><b>${esc(x.name)}</b> <span class="mono muted">${esc(x.doc_id)}</span> ${st}
        <span class="tag">${esc(COND_NAME[x.condition] || x.condition)}</span> <span class="muted">${x.images.length}쪽</span></div>
        <div class="ds-imgs">${x.images.slice(0, 4).map((im, k) => pxStage(file(im), boxes.filter(bx => bx.page === k))).join("")}</div></div>`;
    };
    main().innerHTML = `
      <div class="muted"><a href="#/datasets">데이터셋</a> › <a href="#/datasets/${encodeURIComponent(id)}/bundles">${esc(d.name)}</a></div>
      <h1>${esc(b.task_name)} <span class="mono muted">${esc(b.bundle_id)}</span></h1>
      <div class="bar"><span class="tag">고객 ${esc(b.customer)}${b.source === "labels" ? " · 가져온 라벨" : ` · seed ${b.customer_seed}`}</span>
        <span class="tag">서류 ${base.length}</span><span class="tag">문항 ${(b.items || []).length}</span>
        ${dc.missing?.length ? `<span class="tag warn">빠진 서류 ${dc.missing.length}</span>` : ""}
        ${dc.not_customer?.length ? `<span class="tag warn">타인 서류 ${dc.not_customer.length}</span>` : ""}
        ${dc.not_required?.length ? `<span class="tag">불필요 서류 ${dc.not_required.length}</span>` : ""}
        ${b.plan ? `<span class="tag">직접 만든 묶음</span>` : ""}
        ${b.source === "labels" ? "" : `<button id="bd-rebuild" title="같은 seed 로 이 묶음을 새로 만들어 (서식을 고친 뒤) 전후를 비교">같은 seed 로 다시 만들기</button>`}</div>
      <div class="viewer" style="grid-template-columns:minmax(0,1fr) 420px">
        <div>${base.map(docCard).join("")}${extra.length ? `<h2>바꿔 넣은 서류</h2>${extra.map(docCard).join("")}` : ""}</div>
        <div class="side panel">
          ${b.source === "labels" ? `<b>가져온 문서의 처리 결과</b><p class="muted">입력 라벨과 문서 연결을 사용합니다.</p>` : `<b>고객 프로필</b> <span class="muted" style="font-size:12px">값을 누르면 서류에서 그 값이 있는 자리를 초록 박스로</span>`}
          ${table(b.profile, [["what", "항목", p => `<a href="#" data-what="${esc(p.what)}" class="${sel.what === p.what ? "kr" : ""}">${esc(p.what)}</a>`],
            ["value", "값"], ["where", "나온 서류", p => p.where.length ? `${p.where.length}곳` : `<span class="muted">-</span>`]])}
          <b>고객 일관성 검사</b> ${b.source === "labels" ? `<span class="muted">합성 프로필 검사 미적용</span>` : warn.length ? `<span class="tag warn">${warn.length}건</span>` : `<span class="tag ok">이상 없음</span>`}
          ${warn.length ? `<ul class="checks">${warn.map(w => `<li class="warn">${esc(w.doc)} · ${esc(w.label || w.key)}: ${esc(w.value)} (프로필 ${esc(w.expected)})</li>`).join("")}</ul>` : ""}
          ${b.source === "labels" ? "" : `<div class="muted" style="font-size:12px">고객 본인 역할 칸의 성명·주민번호·주소만 봅니다 (경고만).</div>`}
          <b>대조 문항 (변조판)</b>
          ${(b.variants || []).map(v => `<div class="bd-var"><span class="tag ${v.perturbed ? "warn" : "ok"}">${v.perturbed ? "변조" : "정상"}</span>
            <span class="mono">${esc(v.case)}</span> <span class="muted">${esc(v.category)}</span>
            ${v.changed.map(c => `<div class="muted" style="font-size:12px">${esc(c.doc_id)} ${c.kind === "swap" ? "다른 고객 서류로 바꿈" : ""}
              ${c.changes.slice(0, 4).map(x => `<div>· ${esc(x.label || x.key)}: <s>${esc(x.old)}</s> → <b>${esc(x.new)}</b></div>`).join("")}
              ${c.images.length ? `<a href="#" data-var="${esc(v.case)}|${esc(c.doc_id)}">변조판 보기</a>` : ""}</div>`).join("")}</div>`).join("") || `<p class="muted">없음</p>`}
          <div id="bd-varview"></div>
          ${b.source === "labels" ? `<b>라벨 처리 결과</b>${table(b.processing_results || [], [["id", "작업"], ["status", "상태"], ["answer", "결과", x => esc(x.answer === undefined ? "" : JSON.stringify(x.answer))], ["reason", "생략 사유"]])}` : ""}
          <b>이 묶음의 문항</b><div class="mono" style="font-size:12px">${(b.items || []).map(esc).join("<br>")}</div>
        </div>
      </div>`;
    main().onclick = e => {
      const w = e.target.dataset.what, vv = e.target.dataset.var;
      if (w) { e.preventDefault(); sel.what = sel.what === w ? null : w; draw(); }
      if (vv) {
        e.preventDefault();
        const [cs, did] = vv.split("|");
        const v = b.variants.find(x => x.case === cs), c = v.changed.find(x => x.doc_id === did);
        const boxes = c.changes.filter(x => x.bbox).map(x => ({ page: x.page || 0, bbox: x.bbox, cls: "ds-warn", title: `${x.label || x.key}: ${x.old} → ${x.new}` }));
        $("#bd-varview").innerHTML = `<div class="muted">${esc(cs)} · ${esc(did)} 변조판 (빨강 = 바뀐 칸)</div>${c.images.slice(0, 3).map((im, k) => pxStage(file(im), boxes.filter(bx => bx.page === k))).join("")}`;
      }
    };
    if ($("#bd-rebuild")) $("#bd-rebuild").onclick = async () => {
      const name = `${bid}-rebuild-${Date.now().toString(36)}`;
      try {
        await api(`/api/recipes/${encodeURIComponent(name)}`, { about: `${bid} 다시 만들기 (같은 seed)`, track: "bank", split: "test", types: [], per_doc: 0,
          scenarios: [], bundles: 0, custom_bundles: [{ scenario: b.scenario, seed: b.customer_seed, name: "", ...(b.plan ? Object.fromEntries(Object.entries(b.plan).filter(([k]) => k !== "name")) : {}) }] }, "PUT");
        const j = await api("/api/builds", { recipe: name, name, workers: 1 });
        toast("같은 seed 로 다시 만듭니다. 끝나면 새 데이터셋의 업무 묶음 탭에서 비교하세요");
        location.hash = `#/jobs/${encodeURIComponent(j.id)}`;
      } catch (err) { toast(err.message, true); }
    };
  };
  draw();
}

// 학습 -------------------------------------------------------------------
async function trainingsPanel() {
  const r = await api("/api/trainings").catch(() => ({ trainings: [] }));
  if (!r.trainings.length) return "";
  return `<h2>학습 기록</h2>${table(r.trainings, [["name", "학습"],
    ["stages", "진행", t => t.started ? t.stages.map(s => `<span class="tag ${s.done ? "ok" : ""}" title="${esc(s.id)}">${esc(s.name)}</span>`).join("") : `<span class="muted">아직 시작 안 함</span>`],
    ["command", "실행할 명령 (학습 컨테이너, 저장소 최상위에서)", t => `<span class="mono" style="font-size:12px">${esc(t.command)}</span>`],
    ["benchmark", "평가 세트", t => (t.benchmark || []).map(b => `<a href="#/datasets/${encodeURIComponent(b)}/runs">${esc(b)}</a>`).join(", ") + (t.attached ? " ✓ 결과 붙음" : "")],
    ["benchmark_units", "평가 단위", t => (t.benchmark_units || []).map(u=>`${esc(u.name)} · ${esc(u.id)} (${u.datasets.length}개)`).join('<br>')],
    ["report", "평가 보고서", t => t.finished ? `<a href="/api/trainings/${encodeURIComponent(t.name)}/report/benchmark.html" target="_blank" rel="noopener">벤치마크별 비교</a>` : '—']])}`;
}

async function dsTrain(d) {
  const all = (await api("/api/datasets")).datasets.filter(x => x.format === "docgen-tasks");
  const hasTrain = x => ["train", "mixed"].includes(x.split) || (x.counts || {}).train_items;
  const train = all.filter(hasTrain), bench = all.filter(x => x.split !== "train");
  const benchmarkEditor = benchmarkConfigEditor(bench, d.split === 'train' ? null : d.id);
  const row = (x, kind) => `<label style="display:block"><input type="checkbox" data-${kind}="${esc(x.id)}" ${x.id === d.id && (kind === "train" ? hasTrain(d) : d.split !== "train") ? "checked" : ""}>
    ${dsTag(x)} ${esc(x.name)} <span class="muted">${esc(x.id)}</span>${kind === "train" ? ` <input type="number" min="1" placeholder="문항 수 (비우면 다)" data-count="${esc(x.id)}" style="width:150px">` : ""}</label>`;
  $("#tab").innerHTML = `
    <div class="sub">학습은 하나입니다 (<span class="mono">python -m train</span>): OCR·문서 이해·업무 처리 과제 데이터셋을 함께 골라 섞습니다.
      studio 는 학습을 실행하지 않습니다. 설정 파일을 <span class="mono">train/configs/studio-&lt;이름&gt;.json</span>에 쓰고 학습 컨테이너에서 실행할 명령을 보여 줍니다.
      진행은 공유 폴더의 state.json 으로 보고, 끝나면 고른 평가 세트마다 모델 답으로 붙습니다 (guide/training.md).</div>
    <div class="panel">
      <label class="fld">학습 이름 <input type="text" id="tr-name" value="${esc(d.id)}-${new Date().toISOString().slice(0, 10)}"></label>
      <div class="fld">학습 데이터 (학습 문항이 있는 데이터셋, 문항 수를 적으면 그만큼만 무작위로) ${train.map(x => row(x, "train")).join("") || `<span class="muted">없음</span>`}</div>
      ${benchmarkEditor.html}
      <div class="bar"><button id="tr-preview">설정 미리보기</button><button class="primary" id="tr-save">설정 파일 쓰기</button></div>
      <div id="tr-out"></div>
    </div>
    ${await trainingsPanel()}`;
  benchmarkEditor.mount();
  const req = () => {
    if(!state.info?.features?.benchmark_units) throw new Error('벤치마크 평가 단위 설정을 사용하려면 Studio 서버를 재시작하세요.');
    const units=benchmarkEditor.read();
    return { train: $$("[data-train]").filter(x => x.checked).map(x => x.dataset.train),
    counts: Object.fromEntries($$("[data-count]").filter(x => x.value).map(x => [x.dataset.count, +x.value])),
    benchmark: [...new Set(units.flatMap(x=>x.datasets))], benchmark_units: units, name: $("#tr-name").value.trim() };
  };
  const show = info => {
    $("#tr-out").innerHTML = `${(info.warnings || []).map(w => `<p class="kr">⚠ ${esc(w)}</p>`).join("")}
      <div class="muted">파일 <span class="mono">train/${esc(info.file)}</span> (예시 파일과 합쳐서 씀) · ${esc(info.note || "")}</div>
      <pre class="ans mono">${esc(JSON.stringify(info.config, null, 1))}</pre>
      <div class="muted">학습 컨테이너의 저장소 최상위에서 실행</div><pre class="ans mono">${esc(info.command)}</pre>`;
  };
  $("#tr-preview").onclick = async () => { try { show(await api("/api/training/preview", req())); } catch (e) { toast(e.message, true); } };
  $("#tr-save").onclick = async () => {
    try { const rec = await api("/api/training/save", req()); toast(`썼습니다: ${rec.written}`); dsTrain(d); }
    catch (e) { toast(e.message, true); }
  };
}
