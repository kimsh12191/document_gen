// ④ 가져오기: 문서 이미지 묶음 → 사내 OCR → 포맷·양식 묶기 → 포맷마다 결정(템플릿으로·기존 서식과 같음·건너뛰기) → OCR 벤치마크로.
// 결과 폴더에서(저장된 OCR·추론 결과)와 생성 데이터로 시험도 같은 묶음이 된다. 라벨 있는 데이터 칸은 labeled-import.js.
// 설계: studio/DESIGN.md 8절. 서버: studio/api_import.py, studio/importer.py, studio/formats.py, 결과 폴더 검사는 studio/api_review.py·results.py
"use strict";

addRoute(/^#\/import\/([^/]+)\/f\/([^/]+)$/, (b, f) => viewFormat(decodeURIComponent(b), decodeURIComponent(f)), "import");
addRoute(/^#\/import\/([^/]+)$/, b => viewBatch(decodeURIComponent(b)), "import");

const STAGE_NAME = { listed: "쪽 목록", generating: "생성 중", ocr_done: "OCR 끝", grouped: "묶음 끝" };
const DECISION_NAME = { template: "템플릿으로", existing: "기존 서식과 같음", skip: "건너뛰기" };
const thumb = (b, p, w = 360) => `/api/imports/${encodeURIComponent(b)}/page?p=${encodeURIComponent(p)}&w=${w}`;
const q = s => encodeURIComponent(s);

function decisionTag(d) {
  if (!d) return `<span class="tag">미결정</span>`;
  const extra = d.kind === "template" && d.form_id ? ` <a href="#/forms/${q(d.form_id)}/edit">${esc(d.form_id)}</a>`
    : d.kind === "existing" && d.form_id ? ` ${esc(d.form_id)}` : "";
  return `<span class="tag ${d.kind === "skip" ? "" : "ok"}">${DECISION_NAME[d.kind] || d.kind}</span>${extra}`;
}

function realWarn(r) {
  return r.real_root_set ? "" : `<div class="panel warnbox">설정에 <span class="mono">real_data_dir</span> 이 없어 OCR 검수본을 작업 공간
    (<span class="mono">${esc(r.real_root)}</span>)에 둡니다. 실서류를 다룰 때는 저장소 밖 폴더를 정하세요 (⑨ 설정).</div>`;
}

async function view_import() {
  const r = await api("/api/imports");
  main().innerHTML = `
    <h1>가져오기</h1>
    <div class="sub">문서 이미지(또는 PDF) 묶음을 사내 OCR 로 읽고, 같은 포맷끼리 묶습니다. 포맷마다 템플릿으로 만들지, 기존 서식과 같은지,
      건너뛸지 정하고, 묶음(또는 고른 포맷)을 그대로 OCR 벤치마크로 만들 수 있습니다. 원본 폴더는 읽기만 합니다.</div>
    <details class="panel">
      <summary><b>라벨 있는 데이터 준비 · 생성기 공통 규격 v1</b></summary>
      <p>문서마다 <span class="mono">labels/&lt;id&gt;.json</span>을 만들고 생성 데이터와 같은
        <span class="mono">images · pages · fields</span>를 채웁니다.
        원본 라벨의 <b>page는 0부터, bbox는 이미지 픽셀 좌표</b>입니다.
        키는 해당 서식의 키를 그대로 쓰고, 값은 문서 표시 문자열 또는 빈 칸의 <span class="mono">null</span>로 적습니다.</p>
      <div class="bar">
        <a href="/static/label-format/v1/example.zip" download>이미지·라벨 예제 ZIP</a>
        <a href="/static/label-format/v1/document.example.json" download>문서 라벨 예제 JSON</a>
        <a href="/static/label-format/v1/document.schema.json" download>문서 JSON Schema</a>
        <a href="/static/label-format/v1/ocr.example.json" download>OCR 예제 JSON</a>
        <a href="/static/label-format/v1/ocr.schema.json" download>OCR JSON Schema</a>
        <a href="/static/label-format/v1/meta.schema.json" download>패키지 JSON Schema</a>
        <a href="/static/label-format/v1/bundle.schema.json" download>묶음 JSON Schema</a>
      </div>
      <p class="muted">예제 ZIP을 풀어 아래 '라벨 있는 데이터'에 경로를 입력하세요. OCR 예제는 값 칸·항목명만 포함합니다.
        쪽 전체 OCR 정답은 별도로 준비합니다. 모델 답의 1부터 시작하는 page·0~1000 bbox_2d와 구분하세요.</p>
    </details>
    ${labeledImportHTML()}
    ${realWarn(r)}
    ${r.ocr_set ? "" : `<div class="panel warnbox">사내 OCR 설정(<span class="mono">ocr.callable · revision</span>)이 없습니다. 폴더 묶음은 OCR 단계에서 멈춥니다.
      사내 OCR 없이 흐름을 보려면 아래 "생성 데이터로 시험"을 쓰세요.</div>`}
    ${r.imports.length ? table(r.imports, [
      ["name", "묶음", b => `<a href="#/import/${q(b.name)}">${esc(b.name)}</a>`],
      ["source", "출처", b => `${esc({ folder: "폴더", upload: "올린 파일", docgen: "생성 데이터(시험)", results: "결과 폴더" }[b.source.kind] || b.source.kind)}
        <div class="muted mono">${esc(b.source.path || "")}</div>`],
      ["real_data", "실서류", b => b.real_data ? `<span class="tag warn">실서류</span>` : `<span class="tag">아님</span>`],
      ["n_pages", "쪽", b => `${b.n_ocr}/${b.n_pages}`, true], ["n_formats", "포맷", null, true],
      ["stage", "단계", b => esc(STAGE_NAME[b.stage] || b.stage)],
      ["review", "OCR 검수", b => b.review.done ? `${b.review.done}쪽 확인` : `<span class="muted">-</span>`],
      ["created", "만든 때"]]) : `<p class="muted">묶음이 없습니다.</p>`}
    <h2>새 묶음</h2>
    <div class="rc-grid">
      <div class="panel">
        <b>서버 폴더에서</b>
        <label class="fld">묶음 이름 <input type="text" id="im-name" placeholder="예: 2026-10 급여명세서"></label>
        <label class="fld">폴더 경로 ${r.import_dir ? `(<span class="mono">${esc(r.import_dir)}</span> 아래)` : ""}
          <input type="text" id="im-path" value="${esc(r.import_dir || "")}"></label>
        <label class="fld"><input type="checkbox" id="im-real" checked> 실서류 (검수본·만든 서식이 저장소 밖에만 저장됩니다)</label>
        <label class="fld"><input type="checkbox" id="im-public"> 공개 서식 (빈 서식·견본이라 저장소에 서식으로 넣어도 됨)</label>
        <button class="primary" id="im-go">만들고 OCR·묶기</button>
        <div class="muted" style="margin-top:6px">폴더 안의 이미지 한 장 = 문서 하나, PDF 하나 = 문서 하나(쪽마다 그림).</div>
        <b style="margin-top:14px">결과 폴더에서 (저장된 OCR·추론 결과)</b>
        <div class="muted">이미 OCR·모델 추론을 돌려 저장해 둔 폴더 (<span class="mono">meta.json · images/ · ocr/ · pred/</span>, studio/RESULTS_FORMAT.md).
          저장된 OCR 로 묶고, 추론 결과는 ⑤ 라벨 검수의 출발점이 됩니다. 폴더에는 쓰지 않습니다.</div>
        <label class="fld">묶음 이름 <input type="text" id="rs-name"></label>
        <label class="fld">결과 폴더 경로 <input type="text" id="rs-path"></label>
        <div class="bar"><button id="rs-check">검사</button><button class="primary" id="rs-go" disabled>만들고 묶기</button></div>
        <div id="rs-report"></div>
      </div>
      <div class="panel">
        <b>파일 올리기</b>
        <label class="fld">묶음 이름 <input type="text" id="up-name"></label>
        <input type="file" id="up-files" multiple accept=".png,.jpg,.jpeg,.tif,.tiff,.bmp,.webp,.pdf">
        <label class="fld"><input type="checkbox" id="up-real" checked> 실서류</label>
        <button id="up-go">올리고 OCR·묶기</button>
        <b>생성 데이터로 시험</b>
        <div class="muted">사내 OCR 없이 흐름 전체를 봅니다. 생성기의 서류를 만들어 정답 글자를 OCR 결과처럼 씁니다. 쪽마다 진짜 서식을 알아 묶기 정확도가 나옵니다.</div>
        <label class="fld">서식 ID (쉼표) <input type="text" id="dg-types" value="employment_certificate,career_certificate,hf169,income_certificate"></label>
        <label class="fld">서식당 서류 수 <input type="number" id="dg-per" value="3" min="1" max="20"></label>
        <label class="fld">묶음 이름 <input type="text" id="dg-name" value="시험-생성"></label>
        <button id="dg-go">생성 데이터로 묶음</button>
      </div>
    </div>`;
  bindLabeledImport();
  const started = res => { toast(`작업을 시작했습니다: ${res.name}`); location.hash = `#/import/${q(res.name)}`; };
  $("#rs-check").onclick = async () => {
    try {
      const c = await api("/api/results/check", { path: $("#rs-path").value.trim() });
      $("#rs-report").innerHTML = `<div class="${c.ok ? "" : "err"}">${c.ok ? "✔ 검사 통과" : "✘ 문제가 있습니다"}
        ${c.summary ? ` · 문서 ${c.summary.documents} · 쪽 ${c.summary.pages} · 추론 ${c.summary.with_pred} · 묶음 ${c.summary.bundles}` : ""}</div>
        <ul class="checks">${c.errors.map(e => `<li class="warn">✘ ${esc(e)}</li>`).join("")}${c.warnings.map(w => `<li>⚠ ${esc(w)}</li>`).join("")}</ul>`;
      $("#rs-go").disabled = !c.ok;
      if (c.ok && !$("#rs-name").value && c.meta) $("#rs-name").value = c.meta.name || "";
    } catch (e) { toast(e.message, true); }
  };
  $("#rs-go").onclick = async () => {
    try { started(await api("/api/imports", { name: $("#rs-name").value.trim(), kind: "results", path: $("#rs-path").value.trim() })); }
    catch (e) { toast(e.message, true); }
  };
  $("#im-go").onclick = async () => {
    try {
      started(await api("/api/imports", { name: $("#im-name").value.trim(), kind: "folder", path: $("#im-path").value.trim(),
        real_data: $("#im-real").checked, public: $("#im-public").checked }));
    } catch (e) { toast(e.message, true); }
  };
  $("#up-go").onclick = async () => {
    const files = $("#up-files").files;
    if (!files.length || !$("#up-name").value.trim()) return toast("이름과 파일을 고르세요", true);
    const fd = new FormData();
    fd.append("name", $("#up-name").value.trim());
    fd.append("real_data", $("#up-real").checked);
    for (const f of files) fd.append("files", f);
    try {
      const res = await fetch("/api/imports/upload", { method: "POST", body: fd });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || res.status);
      started(data);
    } catch (e) { toast(e.message, true); }
  };
  $("#dg-go").onclick = async () => {
    try {
      started(await api("/api/imports", { name: $("#dg-name").value.trim(), kind: "docgen", real_data: false, public: true,
        recipe: { types: $("#dg-types").value.split(",").map(s => s.trim()).filter(Boolean), per_doc: +$("#dg-per").value || 1 } }));
    } catch (e) { toast(e.message, true); }
  };
}

async function batchJob(name) {   // 이 묶음의 마지막 작업 (OCR·묶기 도는 중이면 진행 막대)
  const jobs = (await api("/api/jobs")).jobs.filter(j => j.info && j.info.batch === name);
  return jobs[0] || null;
}

async function viewBatch(name) {
  const [b, job] = await Promise.all([api(`/api/imports/${q(name)}`), batchJob(name)]);
  const running = job && job.status === "running";
  const head = `<div class="muted"><a href="#/import">가져오기</a></div>
    <h1>${esc(b.name)} ${b.real_data ? `<span class="tag warn">실서류</span>` : ""} ${b.public ? `<span class="tag">공개 서식</span>` : ""}</h1>
    <div class="sub">쪽 ${b.pages.length} · OCR ${b.pages.filter(p => p.has_ocr).length} · 포맷 ${b.formats.length} · ${esc(STAGE_NAME[b.stage] || b.stage)}
      ${b.grouped ? ` (묶은 때 ${esc(b.grouped)})` : ""} · OCR <span class="mono">${esc((b.ocr && b.ocr.revision) || "-")}</span></div>`;
  const jobBar = job ? `<div class="bar"><a href="#/jobs/${q(job.id)}">${esc(job.title)}</a>
    <span class="tag ${job.status === "done" ? "ok" : job.status === "running" ? "" : "warn"}">${JOB_STATUS[job.status] || job.status}</span>
    ${job.progress ? `<div class="progress"><div style="width:${(100 * job.progress[0] / job.progress[1]).toFixed(1)}%"></div></div>
      <span class="muted">${job.progress[0]} / ${job.progress[1]}</span>` : ""}
    ${job.error ? `<span class="err">${esc(job.error)}</span>` : ""}</div>` : "";
  if (running || !b.formats.length) {
    main().innerHTML = head + jobBar + (running ? `<p class="spin">OCR·묶기가 도는 중입니다…</p>` : `<p class="muted">아직 묶지 않았습니다.</p>
      <button id="bt-regroup">묶기</button>`);
    if ($("#bt-regroup")) $("#bt-regroup").onclick = async () => { try { await api(`/api/imports/${q(name)}/regroup`, {}); viewBatch(name); } catch (e) { toast(e.message, true); } };
    if (running) setTimeout(() => { if (location.hash === `#/import/${q(name)}`) viewBatch(name); }, 2500);
    return;
  }
  const acc = b.accuracy ? `<div class="panel" style="margin-bottom:10px">생성 데이터 묶기 정확도: 순도 <b>${pct(b.accuracy.purity)}%</b>
    (포맷 ${b.accuracy.formats}개 / 진짜 서식 ${b.accuracy.true_forms}종). 겉모습이 같은 서식(예: 재직·경력증명서)은 한 포맷으로 묶이고 변형으로 갈립니다.</div>` : "";
  const rv = b.review.done ? ` · OCR 검수 ${b.review.done}쪽 확인 (사내 OCR 글자 오류율 ${pct(b.review.ocr_cer)}%, 박스 F1 ${pct(b.review.box_f1)})` : "";
  main().innerHTML = head + jobBar + acc + `
    <div class="bar">
      <button id="bt-regroup">다시 묶기</button>
      <button id="bt-prints" title="기존 서식을 한 번씩 그려 지문을 만들어 둡니다. 포맷마다 가까운 기존 서식이 나옵니다">기존 서식 지문 ${b.has_prints ? "다시 " : ""}만들기</button>
      <a href="#/review/${q(b.name)}">OCR 검수로</a><span class="muted">${rv}</span>
      <span style="flex:1"></span>
      <button class="primary" id="bt-ocrset">OCR 벤치마크로…</button>
    </div>
    <div id="bt-ocrset-box"></div>
    <div class="grid fm-grid">${b.formats.map(f => {
      const first = Object.values(f.docs || { x: f.pages })[0][0];
      const nv = Object.keys(f.variants || {}).length;
      return `<div class="card" data-f="${esc(f.id)}">
        <div class="stage"><img src="${thumb(b.name, first)}" alt="" loading="lazy"></div>
        <div class="cap"><b>${esc(f.name)}</b><span class="muted">${esc(f.id)}</span></div>
        <div class="cap"><span>문서 ${Object.keys(f.docs || {}).length || f.pages.length} · 쪽 ${f.pages.length}${nv > 1 ? ` · 변형 ${nv}` : ""}</span>${decisionTag(f.decision)}</div>
        ${f.similar && f.similar.length ? `<div class="cap muted">가까운 서식: ${esc(f.similar[0].form)} ${esc(f.similar[0].name)} (${f.similar[0].score})</div>` : ""}
      </div>`;
    }).join("")}</div>`;
  $$(".fm-grid .card").forEach(c => c.onclick = () => { location.hash = `#/import/${q(name)}/f/${q(c.dataset.f)}`; });
  $("#bt-regroup").onclick = async () => { try { await api(`/api/imports/${q(name)}/regroup`, {}); toast("다시 묶었습니다"); viewBatch(name); } catch (e) { toast(e.message, true); } };
  $("#bt-prints").onclick = async () => {
    try { const j = await api("/api/form-prints", {}); toast("기존 서식 지문을 만드는 중입니다 (⑧ 작업). 끝나면 다시 묶기를 누르세요"); location.hash = `#/jobs/${q(j.id)}`; }
    catch (e) { toast(e.message, true); }
  };
  $("#bt-ocrset").onclick = () => ocrSetBox(b);
}

function ocrSetBox(b) {
  const box = $("#bt-ocrset-box");
  if (box.innerHTML) { box.innerHTML = ""; return; }
  box.innerHTML = `<div class="panel" style="margin-bottom:12px">
    <b>OCR 벤치마크로</b> <span class="muted">OCR 준비(docgen.bench.ocr_prepare)로 쪽 OCR 8과제를 만들고 ⑥ 데이터셋에 등록합니다.</span>
    <div class="rc-scs" style="margin:8px 0">${b.formats.filter(f => !f.decision || f.decision.kind !== "skip").map(f =>
      `<label><input type="checkbox" data-of="${esc(f.id)}" checked> ${esc(f.name)} <span class="muted">(${f.pages.length}쪽)</span></label>`).join("")}</div>
    <div class="bar">
      <label>정답 <select id="os-gt"><option value="pseudo">사내 OCR 그대로 (일치도)</option>
        <option value="reviewed" ${b.review.done ? "selected" : ""}>OCR 검수본 (확인한 쪽만: ${b.review.done || 0}쪽)</option></select></label>
      <label>용도 <select id="os-split"><option value="benchmark">평가 전용</option><option value="train">학습 (+일부 평가로)</option></select></label>
      <label>이름 <input type="text" id="os-name" value="${esc(b.name)}-ocr"></label>
      <button class="primary" id="os-go">만들기</button>
    </div>
    <div class="muted">사내 OCR 그대로는 "사내 OCR 과 얼마나 같게 읽나"이고, 검수본은 "실제로 맞게 읽나"입니다. 데이터셋 설명서에 함께 적힙니다.</div></div>`;
  $("#os-go").onclick = async () => {
    try {
      const res = await api(`/api/imports/${q(b.name)}/ocr-set`, { formats: $$("[data-of]").filter(c => c.checked).map(c => c.dataset.of),
        gt: $("#os-gt").value, split: $("#os-split").value, name: $("#os-name").value.trim() });
      toast(`${res.pages}쪽으로 만드는 중입니다`);
      location.hash = `#/jobs/${q(res.job)}`;
    } catch (e) { toast(e.message, true); }
  };
}

async function viewFormat(name, fid) {
  const b = await api(`/api/imports/${q(name)}`);
  const f = b.formats.find(x => x.id === fid);
  if (!f) throw new Error(`포맷이 없습니다: ${fid}`);
  const pages = Object.fromEntries(b.pages.map(p => [p.id, p]));
  const others = b.formats.filter(x => x.id !== fid);
  const docs = f.docs || Object.fromEntries(f.pages.map(p => [p, [p]]));
  const variantOf = {};
  for (const [k, ids] of Object.entries(f.variants || {})) for (const i of ids) variantOf[i] = k;
  const sample = Object.keys(docs)[0];
  const suggestId = "img_" + (f.name.normalize("NFC").replace(/[^a-z0-9]+/gi, "_").toLowerCase().replace(/^_|_$/g, "") || fid).slice(0, 30);
  main().innerHTML = `
    <div class="muted"><a href="#/import">가져오기</a> › <a href="#/import/${q(name)}">${esc(name)}</a></div>
    <h1>${esc(f.name)} <span class="muted">${esc(f.id)}</span> ${decisionTag(f.decision)}</h1>
    <div class="sub">문서 ${Object.keys(docs).length} · 쪽 ${f.pages.length}. 쪽을 골라 "따로 떼기"로 새 포맷을 만들 수 있습니다 (다시 묶어도 유지).</div>
    <div class="rc-grid">
      <div class="panel">
        <b>이름</b>
        <div class="bar"><input type="text" id="ff-name" value="${esc(f.name)}" style="flex:1"><button id="ff-rename">바꾸기</button></div>
        <b>결정</b>
        <div class="bar">
          <button id="ff-skip">건너뛰기</button>
          <select id="ff-exist"><option value="">기존 서식과 같음…</option>${(f.similar || []).map(s =>
            `<option value="${esc(s.form)}">${esc(s.form)} ${esc(s.name)} (${s.score})</option>`).join("")}
            <option value="?">직접 입력</option></select>
          ${f.decision ? `<button id="ff-undo">결정 지우기</button>` : ""}
        </div>
        ${f.similar && f.similar.length ? "" : `<div class="muted">가까운 기존 서식을 보려면 묶음 화면에서 "기존 서식 지문 만들기" 후 다시 묶기.</div>`}
        <b>합치기</b>
        <div class="bar"><select id="ff-merge"><option value="">이 포맷을 다른 포맷에 합치기…</option>${others.map(o =>
          `<option value="${esc(o.id)}">${esc(o.name)} (${o.pages.length}쪽)</option>`).join("")}</select></div>
      </div>
      <div class="panel">
        <b>템플릿으로 (overlay 이미지 서식)</b>
        <div class="muted">견본 문서 하나의 쪽 그림을 배경으로 서식을 만들고, 값 영역은 ① 서식 › 영역 편집에서 그립니다.
          ${b.real_data && !b.public ? "실서류 묶음이라 <b>private_forms_dir</b> 에만 만듭니다 (값을 지우기 전 그림에 개인정보가 있습니다)." : ""}</div>
        <label class="fld">견본 문서 <select id="ff-sample">${Object.entries(docs).map(([d, ids]) =>
          `<option value="${esc(d)}">${esc(d)} (${ids.length}쪽${variantOf[ids[0]] !== undefined ? `, 변형 ${variantOf[ids[0]]}` : ""})</option>`).join("")}</select></label>
        <label class="fld">서식 ID <input type="text" id="ff-id" value="${esc(suggestId.length > 6 ? suggestId : `img_${fid}`)}"></label>
        <label class="fld">서식 이름 <input type="text" id="ff-fname" value="${esc(f.name)}"></label>
        <label class="fld"><input type="checkbox" id="ff-drafts" ${Object.keys(docs).length > 1 ? "checked" : "disabled"}>
          값 자리·지우기 초안 (같은 포맷의 다른 문서와 견줘 바뀌는 글자 = 값${Object.keys(docs).length > 1 ? "" : ", 문서가 둘 이상일 때"})</label>
        <button class="primary" id="ff-tpl" ${f.decision && f.decision.kind === "template" ? "disabled" : ""}>템플릿 만들기</button>
      </div>
    </div>
    ${Object.entries(f.variants || {}).map(([k, ids]) => `
      <h2>변형 ${k} <span class="muted">${ids.length}쪽</span>
        ${Object.keys(f.variants).length > 1 ? `<button data-split-var="${esc(k)}">이 변형을 따로 떼기</button>` : ""}</h2>
      <div class="grid fm-pages">${ids.map(p => `<div class="card" data-p="${esc(p)}">
        <div class="stage"><img src="${thumb(name, p, 300)}" alt="" loading="lazy"></div>
        <div class="cap"><label><input type="checkbox" data-pick="${esc(p)}" onclick="event.stopPropagation()"> ${esc(p)}</label></div>
        <div class="cap"><span class="muted">${pages[p] ? `단어 ${pages[p].n_words ?? "-"}` : ""}${pages[p] && pages[p].truth ? ` · 진짜 ${esc(pages[p].truth)}` : ""}</span>
          ${pages[p] && pages[p].review ? `<span class="tag ${pages[p].review === "done" ? "ok" : ""}">${pages[p].review === "done" ? "검수 확인" : "검수 중"}</span>` : ""}</div>
      </div>`).join("")}</div>`).join("")}
    <div class="bar" style="margin-top:10px"><button id="ff-split">고른 쪽 따로 떼기</button><span class="muted">고른 쪽: <span id="ff-n">0</span></span></div>`;
  const reload = () => viewFormat(name, fid);
  const post = async (path, body, msg) => {
    try { const r = await api(`/api/imports/${q(name)}${path}`, body); toast(msg); return r; } catch (e) { toast(e.message, true); return null; }
  };
  const decide = async d => { if (await post(`/formats/${q(fid)}`, { decision: d }, "정했습니다")) reload(); };
  $("#ff-rename").onclick = async () => { if (await post(`/formats/${q(fid)}`, { name: $("#ff-name").value.trim() }, "이름을 바꿨습니다")) reload(); };
  $("#ff-skip").onclick = () => decide({ kind: "skip" });
  if ($("#ff-undo")) $("#ff-undo").onclick = () => decide({});
  $("#ff-exist").onchange = () => {
    let v = $("#ff-exist").value;
    if (v === "?") v = (prompt("같은 기존 서식 ID") || "").trim();
    if (v) decide({ kind: "existing", form_id: v });
  };
  $("#ff-merge").onchange = async () => {
    const dst = $("#ff-merge").value;
    if (dst && confirm("이 포맷의 쪽을 모두 그 포맷으로 옮길까요?") && await post("/merge", { src: fid, dst }, "합쳤습니다")) location.hash = `#/import/${q(name)}`;
  };
  const picked = () => $$("[data-pick]").filter(c => c.checked).map(c => c.dataset.pick);
  $$("[data-pick]").forEach(c => c.onchange = () => { $("#ff-n").textContent = picked().length; });
  const split = async ids => {
    if (!ids.length) return toast("쪽을 고르세요", true);
    const nm = prompt("새 포맷 이름 (비우면 자동)", "") ?? null;
    if (nm === null) return;
    if (await post("/split", { pages: ids, name: nm.trim() }, "따로 뗐습니다")) location.hash = `#/import/${q(name)}`;
  };
  $("#ff-split").onclick = () => split(picked());
  $$("[data-split-var]").forEach(bt => bt.onclick = () => split(f.variants[bt.dataset.splitVar]));
  $$(".fm-pages .card").forEach(c => c.onclick = () => { location.hash = `#/review/${q(name)}/${q(c.dataset.p)}`; });
  $("#ff-tpl").onclick = async () => {
    const ids = docs[$("#ff-sample").value];
    const r = await post("/template", { format: fid, pages: ids, form_id: $("#ff-id").value.trim(), name: $("#ff-fname").value.trim(),
      drafts: $("#ff-drafts").checked }, "서식을 만들었습니다. 영역 편집기로 갑니다");
    if (r) {
      if (r.drafts) toast(`값 자리 초안 ${r.drafts}개와 지우기를 넣었습니다. 영역 편집기에서 항목명·키를 확인하세요`);
      state.forms = null;
      location.hash = `#/forms/${q(r.form_id)}/edit`;
    }
  };
  if (sample && $("#ff-sample")) $("#ff-sample").value = sample;
}
