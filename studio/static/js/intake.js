// ④ 서류 넣기: 여러 장(+OCR·추출 결과)을 한 번에 넣고 ❶ 넣기 → ❷ 양식 정리 → ❸ 반영. 설계: studio/DESIGN.md 15절.
// 지금은 ❶(폴더 검사·묶음 만들기·OCR·묶기)과 ❷의 양식 요약까지. 양식마다 결정은 가져오기 화면(import.js)의 포맷 화면을 쓴다.
// 서버: studio/api_intake.py, studio/intake.py (OCR·묶기는 studio/importer.py)
"use strict";

addRoute(/^#\/intake$/, () => viewIntake(), "intake");
addRoute(/^#\/intake\/([^/]+)$/, b => viewIntakeBatch(decodeURIComponent(b)), "intake");

const INTAKE_STEPS = ["❶ 넣기", "❷ 양식 정리", "❸ 반영"];
const intakeSteps = cur => `<div class="bar steps">${INTAKE_STEPS.map((s, i) =>
  `<span class="tag ${i === cur ? "ok" : i < cur ? "" : "muted"}">${s}</span>`).join(" ─ ")}</div>`;

function intakeSummary(s) {
  const n = v => (v ?? 0).toLocaleString();
  return `업무 ${n(s.scenarios)} · 건 ${n(s.cases)} · 서류 ${n(s.documents)} · 쪽 ${n(s.pages)}
    · OCR ${s.pages ? Math.round(100 * s.with_ocr / s.pages) : 0}% · 추출 결과 ${s.documents ? Math.round(100 * s.with_pred / s.documents) : 0}%
    · 구분 <b>${esc(s.structure)}</b>${s.pdf ? ` · PDF ${n(s.pdf)}` : ""}${s.cases_csv ? " · cases.csv" : ""}`;
}

async function viewIntake() {
  const r = await api("/api/intake");
  main().innerHTML = `
    <h1>서류 넣기</h1>
    <div class="sub">서류 이미지(또는 PDF) 여러 장을 한 번에 넣습니다. OCR·추출 결과가 있으면 같이 넣으세요. 같은 양식끼리 묶어
      기존 서식과 맞춰 보고, 새 서식·원본 데이터·시나리오 변경안을 만듭니다. 원본 폴더는 읽기만 합니다.</div>
    ${intakeSteps(0)}
    <div class="panel">
      <b>❶ 넣기</b>
      <details><summary class="muted">넣는 폴더 모양</summary><pre class="mono">&lt;폴더&gt;/
  images/&lt;업무&gt;/&lt;건&gt;/&lt;서류&gt;/p1.png …   (PDF 면 &lt;서류&gt;.pdf, 단계는 빠져도 됨 — images/*.png 도 됨)
  ocr/&lt;같은 경로&gt;/p1.json              (선택) 사내 OCR 응답 그대로
  pred/&lt;업무&gt;/&lt;건&gt;/&lt;서류&gt;.json          (선택) 추출 결과 {"items": [{key, value, bbox_2d, page}]}
  cases.csv                             (선택) path,case,scenario
  meta.json                             (선택) real_data · mapping · model</pre>
        <div class="muted">시험 폴더: <span class="mono">python -m studio.intake_testset &lt;out&gt;</span> → <span class="mono">&lt;out&gt;/structured</span> 또는 <span class="mono">&lt;out&gt;/flat</span></div></details>
      <div class="bar"><input type="text" id="in-path" placeholder="폴더 경로" style="flex:1" value="${esc(store.get("intake.path", ""))}">
        <button id="in-check">검사</button></div>
      <div id="in-res"></div>
    </div>
    ${r.ocr_set ? "" : `<div class="muted">사내 OCR 설정이 없어 OCR 파일이 없는 쪽이 있으면 OCR 단계에서 멈춥니다.</div>`}
    <h2>넣은 묶음</h2>
    ${r.batches.length ? table(r.batches, [
      ["name", "묶음", b => `<a href="#/intake/${q(b.name)}">${esc(b.name)}</a><div class="muted mono">${esc(b.path)}</div>`],
      ["summary", "내용", b => intakeSummary(b.summary)],
      ["n_formats", "양식", null, true], ["stage", "단계", b => esc(STAGE_NAME[b.stage] || b.stage)], ["created", "만든 때"]])
      : `<p class="muted">아직 없습니다.</p>`}`;
  $("#in-check").onclick = async () => {
    const path = $("#in-path").value.trim();
    store.set("intake.path", path);
    $("#in-res").innerHTML = `<p class="muted">검사 중…</p>`;
    let c;
    try { c = await api("/api/intake/check", { path }); } catch (e) { $("#in-res").innerHTML = `<p class="err">${esc(e.message)}</p>`; return; }
    const base = (c.root || path).split(/[\\/]/).filter(Boolean).slice(-2).join("-");
    $("#in-res").innerHTML = `
      <p>${c.ok ? "✓" : "✗"} ${c.summary ? intakeSummary(c.summary) : ""}</p>
      ${c.errors.map(e => `<div class="err">✗ ${esc(e)}</div>`).join("")}
      ${c.warnings.map(w => `<div class="warn">⚠ ${esc(w)}</div>`).join("")}
      ${c.examples?.length ? `<details><summary class="muted">서류 예 ${c.examples.length}</summary>${table(c.examples, [
        ["id", "서류", d => `<span class="mono">${esc(d.id)}</span>`], ["scenario", "업무"], ["case", "건"], ["pages", "쪽", null, true],
        ["pred", "추출 결과", d => d.pred ? "있음" : "-"]])}</details>` : ""}
      ${c.ok ? `<div class="bar">묶음 이름 <input type="text" id="in-name" value="${esc(base)}"> <button class="primary" id="in-go">묶기 시작</button></div>` : ""}`;
    if (c.ok) $("#in-go").onclick = async () => {
      try {
        const b = await api("/api/intake", { name: $("#in-name").value.trim(), path });
        location.hash = `#/intake/${q(b.name)}`;
      } catch (e) { toast(e.message, true); }
    };
  };
}

async function viewIntakeBatch(name) {
  const b = await api(`/api/intake/${q(name)}`);
  const done = b.stage === "grouped";
  main().innerHTML = `
    <div class="crumb"><a href="#/intake">서류 넣기</a> › ${esc(b.name)}</div>
    <h1>${esc(b.name)}</h1>
    ${intakeSteps(done ? 1 : 0)}
    <div class="panel"><b>❶ 넣기</b> <span class="mono muted">${esc(b.path)}</span>
      <p>${intakeSummary(b.summary)}</p>
      ${b.warnings.map(w => `<div class="warn">⚠ ${esc(w)}</div>`).join("")}
      <p>OCR ${b.n_ocr}/${b.n_pages} · ${esc(STAGE_NAME[b.stage] || b.stage)}
        ${b.job ? ` · <a href="#/jobs/${q(b.job.id)}">${esc(b.job.title)}</a> ${b.job.progress ? `${b.job.progress[0]}/${b.job.progress[1]}` : "진행 중…"}` : ""}</p>
    </div>
    ${done ? `<div class="panel"><b>❷ 양식 정리</b> 양식 ${b.formats.length}개 · 많은 순
      <span class="muted">— 양식마다 결정(기존 서식과 같음·새 서식·건너뛰기)은 지금은 <a href="#/import/${q(b.name)}">포맷 화면</a>에서 합니다.</span>
      <div class="grid cards">${b.formats.map(f => `
        <div class="card"><a href="#/import/${q(b.name)}/f/${q(f.id)}"><img loading="lazy" src="${thumb(b.name, f.sample, 240)}" alt=""></a>
          <div><b>${esc(f.name)}</b></div>
          <div class="muted">서류 ${f.n_docs} · 쪽 ${f.n_pages} · 추출 결과 ${f.with_pred}</div>
          <div class="muted">업무 ${Object.entries(f.scenarios).map(([k, v]) => `${esc(k)} ${v}`).join(" · ")}</div>
          ${f.similar.length ? `<div class="muted">가까운 서식 ${esc(f.similar[0].form)} (${f.similar[0].score})</div>` : ""}
          <div>${decisionTag(f.decision)}</div></div>`).join("")}</div></div>` : ""}`;
  if (!done && b.job) setTimeout(() => { if (location.hash === `#/intake/${q(name)}`) viewIntakeBatch(name); }, 2500);
}
