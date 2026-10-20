// ⑥ 데이터셋 (등록부·설명서·문항 보기·모델 답 붙이기·채점) · ⑦ 평가 (비교표). 서버: studio/datasets.py
"use strict";

addRoute(/^#\/datasets\/([^/]+)(?:\/(\w+))?$/, (id, tab) => viewDataset(decodeURIComponent(id), tab || "card"), "datasets");

const TRACK_NAME = { ocr: "OCR", bank: "은행 업무" };
const TASK_KO = {
  crop_ocr: "잘라낸 글자 읽기", bbox_ocr: "박스 안 글자", region_ocr: "영역 받아쓰기", marked_ocr: "그린 박스 글자",
  grounding: "글자 위치 찾기", spotting: "전체 글자+위치", relation: "옆 글자 찾기", marked_box: "그린 박스 위치",
  ocr_field: "값 칸 인식", ocr_page: "전체 받아쓰기", classify: "서류 분류", kie: "정보 추출", marks: "체크·도장·서명",
  doc_check: "서류 구비", cross_check: "서류 대조", review: "심사 질의",
};
const LOWER_BETTER = new Set(["cer"]);
const dsTag = d => `<span class="tag ${d.track === "ocr" ? "html" : "overlay"}">${TRACK_NAME[d.track]}</span>`;

async function view_datasets() {
  const r = await api("/api/datasets");
  main().innerHTML = `
    <h1>데이터셋</h1>
    <div class="sub">OCR·은행 업무 데이터셋을 출처와 정답 종류와 함께 한 목록으로 관리합니다. 1부·2부 파이프라인이 명령줄로 만든 폴더도
      경로만 등록하면 됩니다 (studio 는 읽기만 합니다). 등록부: <span class="mono">${esc(r.workspace)}/registry.json</span></div>
    <div class="panel" style="margin-bottom:12px">
      <b>폴더 등록</b>
      <div class="bar" style="margin-top:6px">
        <input type="text" id="dr-path" placeholder="폴더 경로 (1부 prepare 결과 · docgen.bench 결과 · 2부 prepare 결과)" style="width:520px">
        <input type="text" id="dr-name" placeholder="이름 (비우면 폴더 이름)" style="width:200px">
        <select id="dr-source"><option value="">출처: 자동</option>${Object.entries(r.sources).map(([k, n]) => `<option value="${k}">${n}</option>`).join("")}</select>
        <select id="dr-gt"><option value="">정답: 자동</option>${Object.entries(r.gts).map(([k, n]) => `<option value="${k}">${n}</option>`).join("")}</select>
        <label><input type="checkbox" id="dr-real"> 실서류</label>
        <button class="primary" id="dr-go">등록</button>
      </div>
      <div class="muted" style="font-size:12px">새 데이터셋 만들기(합성 레시피·이미지 묶음·결과 폴더)는 4·5단계에서 이 화면에 생깁니다.</div>
    </div>
    ${r.datasets.length ? table(r.datasets, [
      ["name", "이름", d => `<a href="#/datasets/${encodeURIComponent(d.id)}">${esc(d.name)}</a> <span class="mono muted">${esc(d.id)}</span>`],
      ["track", "벤치마크", d => dsTag(d)],
      ["source", "출처", d => esc(r.sources[d.source] || d.source)],
      ["gt", "정답", d => esc((r.gts[d.gt] || d.gt).split(" (")[0])],
      ["real", "", d => d.real_data ? `<span class="tag warn">실서류</span>` : ""],
      ["version", "버전", d => esc(d.version || "-")],
      ["counts", "문항", d => esc(Object.entries(d.counts || {}).filter(([k]) => !/train|val|pages|documents/.test(k) || k === "benchmark_tasks")
        .reduce((a, [, v]) => a + (+v || 0), 0) || "-")],
      ["runs", "모델 답", d => d.n_runs || ""], ["scores", "점수", d => d.n_scores || ""],
      ["frozen", "고정", d => d.frozen ? `<span class="tag ok">고정</span>` : ""],
      ["exists", "", d => d.exists ? "" : `<span class="tag warn">폴더 없음</span>`],
    ]) : `<p class="muted">등록된 데이터셋이 없습니다.</p>`}`;
  $("#dr-go").onclick = async () => {
    try {
      const d = await api("/api/datasets", { path: $("#dr-path").value.trim(), name: $("#dr-name").value.trim(),
        source: $("#dr-source").value || null, gt: $("#dr-gt").value || null, real_data: $("#dr-real").checked || null });
      location.hash = `#/datasets/${encodeURIComponent(d.id)}`;
    } catch (e) { toast(e.message, true); }
  };
}

async function viewDataset(id, tab) {
  const d = await api(`/api/datasets/${encodeURIComponent(id)}`);
  const tabs = [["card", "설명서"], ["items", "문항"], ["runs", `모델 답 (${d.predictions.length})`]];
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
  if (tab === "runs") return dsRuns(d);
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

function dsItems(d) {
  const st = store.get(`ds.${d.id}`, { task: Object.keys(d.tasks)[0] || "", pids: [], order: "id" });
  const tasks = Object.entries(d.tasks);
  $("#tab").innerHTML = `
    <div class="bar">
      <select id="it-task">${tasks.map(([t, n]) => `<option value="${t}" ${t === st.task ? "selected" : ""}>${esc(TASK_KO[t] || t)} (${t}) · ${n}</option>`).join("")}</select>
      <input type="text" id="it-q" placeholder="문항 안 글자 검색" style="width:180px">
      <span class="muted">모델 답:</span>
      ${d.predictions.map(p => `<label><input type="checkbox" data-pid="${p.pid}" ${st.pids.includes(p.pid) ? "checked" : ""}> ${esc(p.label)}</label>`).join("") || `<span class="muted">(없음 — 모델 답 탭에서 붙입니다)</span>`}
      <label>순서 <select id="it-order"><option value="id">ID 순</option><option value="worst" ${st.order === "worst" ? "selected" : ""}>첫 답 점수 낮은 것부터</option></select></label>
      <span class="muted" id="it-stat"></span>
    </div>
    <div class="keys-help">초록 박스 = 정답, 파랑 점선 = 질문 영역, 주황·보라·청록 = 모델 답. 점수는 채점한 뒤에 보입니다 (모델 답 탭).</div>
    <div id="it-list"></div>
    <div class="bar"><button id="it-prev">◀ 이전</button><button id="it-next">다음 ▶</button></div>`;
  let offset = 0;
  const load = async () => {
    st.task = $("#it-task").value; st.order = $("#it-order").value;
    st.pids = $$("[data-pid]").filter(x => x.checked).map(x => x.dataset.pid);
    store.set(`ds.${d.id}`, st);
    $("#it-stat").textContent = "읽는 중…";
    try {
      const r = await api(`/api/datasets/${encodeURIComponent(d.id)}/items?task=${encodeURIComponent(st.task)}&offset=${offset}&limit=10` +
        `&pids=${st.pids.join(",")}&order=${st.order}&q=${encodeURIComponent($("#it-q").value.trim())}`);
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
        placeholder="runs/<실험>/ (1부·2부 파이프라인) · 예측 폴더 (docgen.bench run) · 답 파일 .jsonl">
        <input type="text" id="rn-label" placeholder="이름 (선택)" style="width:160px"><button class="primary" id="rn-go">붙이기</button></div>
      <div class="muted" style="font-size:12px">줄마다 {"id", "prediction"} 또는 {"id", "output"}. 붙인 폴더에는 쓰지 않습니다.</div></div>
    <h2>모델 답 ${d.predictions.length}개</h2>
    ${d.predictions.length ? table(d.predictions, [["label", "이름"], ["run", "붙인 결과"], ["path", "파일", p => `<span class="mono muted" style="font-size:12px">${esc(p.path)}</span>`],
      ["act", "", p => `<button data-score="${p.pid}">${d.scores.some(s => s.pid === p.pid) ? "다시 채점" : "채점"}</button>
        <a href="#/datasets/${encodeURIComponent(d.id)}/items" data-look="${p.pid}">문항 보기</a>`]]) : `<p class="muted">붙인 모델 답이 없습니다.</p>`}
    <h2>studio 채점 결과 <span class="muted" style="font-weight:400;font-size:13px">명령줄 채점과 같은 함수 (1부 bank_ocr.metrics · docgen.bench.evaluate)</span></h2>
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
    for (const track of ["ocr", "bank"]) {
      const rows = c.rows.filter(x => x.track === track);
      if (!rows.length) continue;
      const tasks = [...new Set(rows.flatMap(x => Object.keys(x.main || {})))];
      out.push(`<h2>${TRACK_NAME[track]}</h2>${scoreTable(rows, tasks)}`);
    }
    $("#ev-out").innerHTML = out.join("") || `<p class="muted">고른 데이터셋에 채점 결과가 없습니다.</p>`;
  };
  $$("[data-ds]").forEach(x => x.onchange = draw);
  draw();
}
