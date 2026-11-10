// ⑥ 데이터셋 (등록부·설명서·구성·문항 보기·업무 묶음). 평가·채점·학습은 학습 서버의 python -m train (guide/eval.md).
// 생성 현황 목록은 dataset-builds.js, 새로 만들기(레시피)는 recipes.js.
// 서버: studio/api_datasets.py·datasets.py (등록부), studio/api_bank.py·bank_data.py (레시피·빌드·업무 묶음)
"use strict";

addRoute(/^#\/datasets$/, () => view_datasets(), "datasets");
addRoute(/^#\/datasets\/([^/]+)\/bundle\/(.+)$/, (id, bid) => viewBundle(decodeURIComponent(id), decodeURIComponent(bid)), "datasets");
addRoute(/^#\/datasets\/([^/]+)(?:\/(\w+))?$/, (id, tab) => viewDataset(decodeURIComponent(id), tab || "card"), "datasets");

const GROUP_NAME = { ocr: "OCR", doc: "문서 이해", work: "업무 처리" };   // 과제 묶음 (docgen.bench.evaluate.TASK_GROUP)
const TASK_GROUP = { crop_ocr: "ocr", bbox_ocr: "ocr", region_ocr: "ocr", marked_ocr: "ocr", grounding: "ocr", spotting: "ocr",
  relation: "ocr", marked_box: "ocr", ocr_field: "ocr", ocr_page: "ocr", classify: "doc", kie: "doc", marks: "doc", freetext: "doc", form_qa: "doc",
  table: "doc", table_read: "doc", table_find: "doc", table_qa: "doc",
  doc_check: "work", cross_check: "work", review: "work" };
const TASK_KO = {
  crop_ocr: "잘라낸 글자 읽기", bbox_ocr: "박스 안 글자", region_ocr: "영역 받아쓰기", marked_ocr: "그린 박스 글자",
  grounding: "글자 위치 찾기", spotting: "전체 글자+위치", relation: "옆 글자 찾기", marked_box: "그린 박스 위치",
  ocr_field: "값 칸 인식", ocr_page: "전체 받아쓰기", classify: "서류 분류", kie: "정보 추출", marks: "체크·도장·서명", freetext: "기타 칸 정리", form_qa: "서식 전용 질문",
  table: "표 추출", table_read: "표 그대로 옮기기", table_find: "표 찾기", table_qa: "표 질의",
  doc_check: "서류 구비", cross_check: "서류 대조", review: "심사 질의",
};
// 이름만으로 헷갈리는 과제의 설명 (과제 이름에 마우스를 올리면 보임)
const TASK_HINT = { freetext: "기타·비고·사유 칸의 자유 기재를 DB 칸(용도·금액·날짜…)으로 정리. 정보 추출(kie)은 적힌 그대로, 이건 정리한 값",
  form_qa: "서식마다 사람이 정한 질문 (서식 폴더 qa.py)",
  table: "표(행 수가 서류마다 다른 반복 목록)의 모든 행을 정해 준 열로. 행 수는 모델이 정함",
  table_read: "표를 머리글까지 그대로 옮기기 (열을 정해 주지 않음)", table_find: "서류의 표를 모두 찾기 (머리글·위치·행 수)",
  table_qa: "표를 보고 행 수·찾기·합계 등을 묻기" };
const dsTag = d => (d.groups || []).map(g => `<span class="tag ${g === "ocr" ? "html" : g === "doc" ? "overlay" : ""}">${GROUP_NAME[g] || esc(g)}</span>`).join(" ");

async function view_datasets() {
  const [r, recipes] = await Promise.all([api("/api/datasets"), recipesPanel()]);
  if (location.hash !== "#/datasets") return;
  main().innerHTML = `
    <h1>데이터셋</h1>
    <div class="sub">레시피로 평가 세트·학습 데이터를 만들고(<b>새로 만들기</b>), 끝나면 아래 목록에서 문항을 봅니다. 학습·평가는 학습 서버에서 (<a href="#/guide/training.md">training.md</a>).
      <a href="#/guide/studio.md">studio 사용법 3절</a> · 등록부 <span class="mono">${esc(r.workspace)}/registry.json</span></div>
    ${recipes}
    <div id="dataset-build-jobs"></div>
    <section id="ds-registry"><div class="bar"><h2>등록된 데이터셋</h2><span id="ds-reg-status" class="muted">${r.datasets.length}개 등록</span>
      <button type="button" id="ds-refresh">목록 새로고침</button></div><div id="ds-list">${datasetRegistryHTML(r)}</div></section>
    <details class="panel" style="margin:12px 0">
      <summary><b>폴더 등록</b> <span class="muted">— studio 밖(명령줄)에서 만든 데이터셋 폴더를 목록에 넣을 때만</span></summary>
      <div class="bar" style="margin-top:6px">
        <input type="text" id="dr-path" placeholder="폴더 경로 (과제 폴더: docgen.bench build · OCR 준비 결과)" style="width:520px">
        <input type="text" id="dr-name" placeholder="이름 (비우면 폴더 이름)" style="width:200px">
        <select id="dr-source"><option value="">출처: 자동</option>${Object.entries(r.sources).map(([k, n]) => `<option value="${k}">${n}</option>`).join("")}</select>
        <select id="dr-gt"><option value="">정답: 자동</option>${Object.entries(r.gts).map(([k, n]) => `<option value="${k}">${n}</option>`).join("")}</select>
        <label><input type="checkbox" id="dr-real"> 실서류</label>
        <button class="primary" id="dr-go">등록</button>
      </div>
    </details>`;
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
  const tabs = [["card", "설명서"], ["tracking", "구성"], ["items", "문항"], ...((d.groups || []).includes("work") ? [["bundles", "업무 묶음"]] : []),
  ];
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
  if (tab === "bundles") return dsBundles(d);
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
function itemStage(d, it, img, k) {
  const url = `/api/datasets/${encodeURIComponent(d.id)}/file?p=${encodeURIComponent(img)}`;
  const rects = [];
  for (const b of it.boxes.filter(b => b.img === k)) {
    const [x0, y0, x1, y1] = b.box;
    rects.push(`<rect class="ds-${b.cls}" x="${x0}" y="${y0}" width="${Math.max(1, x1 - x0)}" height="${Math.max(1, y1 - y0)}"><title>${esc(b.label)}</title></rect>`);
  }
  return `<div class="stage ds-stage"><img src="${url}" alt="" loading="lazy"><svg viewBox="0 0 1000 1000" preserveAspectRatio="none">${rects.join("")}</svg></div>`;
}

const showAns = a => typeof a === "string" ? esc(a) : `<pre class="ans">${esc(JSON.stringify(a, null, 1))}</pre>`;

async function dsItems(d) {
  const st = store.get(`ds.${d.id}`, { task: Object.keys(d.tasks)[0] || "" });
  const tasks = Object.entries(d.tasks);
  const summary = await api(`/api/datasets/${encodeURIComponent(d.id)}/composition`).catch(() => null);
  st.filters ||= {};
  $("#tab").innerHTML = `
    ${summary ? '' : '<p class="warn">현재 서버에는 구성·추적 API가 없습니다. Studio를 재시작하면 구분별 필터를 사용할 수 있습니다.</p>'}
    <div class="bar">
      <select id="it-task"><option value="" ${st.task === "" ? "selected" : ""}>과제 전체</option>${tasks.map(([t, n]) => `<option value="${t}" title="${esc(TASK_HINT[t] || "")}" ${t === st.task ? "selected" : ""}>${esc(TASK_KO[t] || t)} (${t}) · ${n}</option>`).join("")}</select>
      <input type="text" id="it-q" placeholder="문항 안 글자 검색" style="width:180px">
      <span class="muted" id="it-stat"></span>
    </div>
    <div class="bar">${["task_group", "scenario", "label_format", "doc_type"].map(key => `<label>${TRACKING_TITLE[key]} <select data-track-filter="${key}" ${summary?'':'disabled'}><option value="">전체</option>${Object.keys(summary?.all.by[key] || {}).map(v => `<option value="${esc(v)}" ${st.filters[key] === v ? "selected" : ""}>${esc(trackName(v))}</option>`).join("")}</select></label>`).join("")}<label><input type="checkbox" id="it-evaluation-only" ${summary?'':'disabled'} ${st.evaluationOnly?'checked':''}> 평가 문항만</label><button id="it-clear-filters">필터 초기화</button></div>
    <div class="keys-help">초록 박스 = 정답, 파랑 점선 = 질문 영역. 모델 답과 점수는 학습 서버 결과의 answers.html 에서 봅니다 (guide/results.md).</div>
    <div id="it-list"></div>
    <div class="bar"><button id="it-prev">◀ 이전</button><button id="it-next">다음 ▶</button></div>`;
  let offset = 0;
  const load = async () => {
    st.task = $("#it-task").value;
    st.filters = Object.fromEntries($$("[data-track-filter]").map(x => [x.dataset.trackFilter, x.value]));
    st.evaluationOnly = $("#it-evaluation-only").checked;
    store.set(`ds.${d.id}`, st);
    $("#it-stat").textContent = "읽는 중…";
    try {
      const r = await api(`/api/datasets/${encodeURIComponent(d.id)}/items?task=${encodeURIComponent(st.task)}&offset=${offset}&limit=10` +
        `&evaluation_only=${st.evaluationOnly}&q=${encodeURIComponent($("#it-q").value.trim())}&${new URLSearchParams(st.filters)}`);
      $("#it-stat").textContent = `${r.total}개 중 ${r.total ? offset + 1 : 0}–${Math.min(r.total, offset + 10)}`;
      $("#it-list").innerHTML = r.items.map(it => `
        <div class="panel ds-item">
          <div class="muted mono" style="font-size:12px">${esc(it.id)} ${Object.entries(it.meta || {}).slice(0, 6).map(([k, v]) => `<span class="tag">${esc(k)}: ${esc(v)}</span>`).join("")}</div>
          <div class="ds-row">
            <div class="ds-imgs">${it.images.slice(0, 13).map((im, k) => itemStage(d, it, im, k)).join("")}</div>
            <div class="ds-text">
              <div class="muted">질문</div><div class="prompt">${esc(it.prompt)}</div>
              <div class="muted">정답</div><div>${showAns(it.answer)}</div>
            </div>
          </div>
        </div>`).join("") || `<p class="muted">문항이 없습니다.</p>`;
      $("#it-prev").disabled = offset === 0;
      $("#it-next").disabled = offset + 10 >= r.total;
    } catch (e) { $("#it-stat").innerHTML = `<span class="err">${esc(e.message)}</span>`; }
  };
  $("#it-task").onchange = () => { offset = 0; load(); };
  $("#it-q").onchange = () => { offset = 0; load(); };
  $$("[data-track-filter]").forEach(x => x.onchange = () => { offset = 0; load(); });
  $("#it-evaluation-only").onchange = () => { offset = 0; load(); };
  $("#it-clear-filters").onclick = () => { $$("[data-track-filter]").forEach(x => { x.value = ""; }); $("#it-evaluation-only").checked = false; offset = 0; load(); };
  $("#it-prev").onclick = () => { offset = Math.max(0, offset - 10); load(); };
  $("#it-next").onclick = () => { offset += 10; load(); };
  load();
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
