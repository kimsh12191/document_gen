// ④ 서류 넣기: 여러 장(+OCR·추출 결과)을 한 번에 넣고 ❶ 넣기 → ❷ 양식 정리 → ❸ 반영. 설계: studio/DESIGN.md 15절.
// ❶ 폴더 검사·묶음 만들기·OCR·묶기, ❷ 모양마다 판정(기존 서식·새 서식·건너뛰기)·쓸 길·추출 키 → 공통 키·새 서식 초안. ❸ 반영은 다음 단계.
// 서버: studio/api_intake.py, studio/intake.py·intake_judge.py (OCR·묶기는 studio/importer.py)
"use strict";

addRoute(/^#\/intake$/, () => viewIntake(), "intake");
addRoute(/^#\/intake\/([^/]+)$/, b => viewIntakeBatch(decodeURIComponent(b)), "intake");
addRoute(/^#\/intake\/([^/]+)\/draft\/([^/]+)$/, (b, f) => viewIntakeDraft(decodeURIComponent(b), decodeURIComponent(f)), "intake");

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
    ${done ? `<div class="panel"><b>❷ 양식 정리</b> <span class="muted">모양마다 기존 서식인지 새 서식인지 고르고, 쓸 길과 추출 키를 확인한 뒤 확정합니다.
      제안은 기존 서식 지문과의 비슷한 정도(0.5 이상이면 기존 서식)와 서류 수(3건 이상이면 서식으로)로 만듭니다.</span>
      <div class="bar"><button class="primary" id="ij-save">이 화면의 판정대로 확정</button> <span class="muted" id="ij-msg"></span></div>
      <div id="ij-cards" class="grid cards wide"><p class="muted">판정 읽는 중…</p></div></div>` : ""}`;
  if (done) drawJudge(b);
  if (!done && b.job) setTimeout(() => { if (location.hash === `#/intake/${q(name)}`) viewIntakeBatch(name); }, 2500);
}


async function drawJudge(b) {
  const [j, c] = await Promise.all([api(`/api/intake/${q(b.name)}/judge`), api("/api/dictionary/keys?scope=common")]);
  const commons = c.rows;
  const cards = j.formats;
  const kindOf = f => f.decision?.kind === "existing" ? `existing:${f.decision.form_id}` : (f.decision?.kind || (f.suggest.kind === "existing" ? `existing:${f.suggest.form_id}` : f.suggest.kind));
  $("#ij-cards").innerHTML = cards.map((f, i) => {
    const kind = kindOf(f), uses = f.decision?.uses || f.uses, keymap = f.decision?.keymap || {};
    return `<div class="card" data-f="${i}">
      <a href="#/import/${q(b.name)}/f/${q(f.id)}"><img loading="lazy" src="${thumb(b.name, f.sample, 240)}" alt=""></a>
      <div><b>${esc(f.name)}</b> ${f.decision ? `<span class="tag ok">확정</span>` : `<span class="tag">제안</span>`}</div>
      <div class="muted">서류 ${f.n_docs} · 쪽 ${f.n_pages} · 추출 결과 ${f.with_pred}</div>
      <div><select data-kind>${f.similar.map(x => `<option value="existing:${esc(x.form)}" ${kind === "existing:" + x.form ? "selected" : ""}>기존 서식: ${esc(x.name)} (${x.score})</option>`).join("")}
        <option value="new" ${kind === "new" ? "selected" : ""}>새 서식</option><option value="skip" ${kind === "skip" ? "selected" : ""}>건너뛰기</option></select></div>
      <div data-newbox ${kind === "new" ? "" : 'style="display:none"'}><input type="text" data-name value="${esc(f.decision?.name || f.name)}" placeholder="새 서식 이름" style="width:100%">
        <label><input type="checkbox" data-use="template" ${uses.template ? "checked" : ""}> 서식으로</label>
        <a href="#/intake/${q(b.name)}/draft/${q(f.id)}">초안 보기</a></div>
      <div><label><input type="checkbox" data-use="raw" ${uses.raw ? "checked" : ""}> 원본 데이터로</label></div>
      ${f.keys.length ? `<details><summary>추출 키 ${f.keys.length} · 공통 키에 이음 ${f.keys.filter(k => (keymap[k.key] ?? k.common)).length}</summary>
        ${f.keys.map(k => `<div class="bar small"><span class="mono" title="${esc(k.example ?? "")}">${esc(k.key)}</span>
          <select data-key="${esc(k.key)}"><option value="">(문서별 키)</option>${commons.map(x => `<option value="${esc(x.key)}" ${(keymap[k.key] ?? k.common) === x.key ? "selected" : ""}>${esc(x.name)}</option>`).join("")}</select></div>`).join("")}</details>` : ""}
    </div>`;
  }).join("");
  $$("#ij-cards [data-kind]").forEach(sel => sel.onchange = () => {
    $("[data-newbox]", sel.closest(".card")).style.display = sel.value === "new" ? "" : "none";
  });
  $("#ij-save").onclick = async () => {
    const formats = {};
    $$("#ij-cards .card").forEach(el => {
      const f = cards[+el.dataset.f], v = $("[data-kind]", el).value;
      formats[f.id] = { kind: v.startsWith("existing:") ? "existing" : v, ...(v.startsWith("existing:") ? { form_id: v.slice(9) } : {}),
        name: $("[data-name]", el).value, uses: { template: $("[data-use=template]", el).checked, raw: $("[data-use=raw]", el).checked },
        keymap: Object.fromEntries($$("[data-key]", el).map(x => [x.dataset.key, x.value || null])) };
    });
    try { const r = await api(`/api/intake/${q(b.name)}/decide`, { formats }); toast(`${r.saved}개 모양을 확정했습니다`); drawJudge(b); }
    catch (e) { toast(e.message, true); }
  };
}

async function viewIntakeDraft(name, fid) {
  main().innerHTML = `<p class="muted">초안 만드는 중…</p>`;
  const d = await api(`/api/intake/${q(name)}/draft/${q(fid)}`);
  const box = (g, cls, page) => g.page !== page ? "" : `<div class="ij-box ${cls}" title="${esc(g.key || g.label)} ${esc(g.value ?? g.note ?? "")}"
    style="left:${100 * g.rect[0] / d.images[page].width}%;top:${100 * g.rect[1] / d.images[page].height}%;width:${100 * (g.rect[2] - g.rect[0]) / d.images[page].width}%;height:${100 * (g.rect[3] - g.rect[1]) / d.images[page].height}%"></div>`;
  main().innerHTML = `
    <div class="crumb"><a href="#/intake">서류 넣기</a> › <a href="#/intake/${q(name)}">${esc(name)}</a> › 새 서식 초안</div>
    <h1>새 서식 초안 <span class="muted mono">${esc(fid)}</span></h1>
    <div class="sub">견본 서류 <span class="mono">${esc(d.sample_doc)}</span>. 파란 칸 = 추출값 위치로 만든 값 칸 ${d.regions.length}개(공통 키에 이음 ${d.keymapped}),
      주황 칸 = 추출값 밖에서 서류마다 달라지는 글자(남은 값 후보 ${d.leftover.length}개 — 개인정보가 남지 않게 함께 지웁니다).
      오른쪽은 지운 배경입니다. 서식은 ❸ 반영에서 만들고, 그 뒤 ① 서식의 영역 편집기에서 다듬습니다.</div>
    ${d.images.map((im, k) => `<div class="ij-pair"><div class="ij-stage"><img src="/api/imports/${q(name)}/page?p=${q(im.page_id)}&w=900" alt="">
      ${d.regions.map(g => box(g, "val", k)).join("")}${d.leftover.map(g => box(g, "left", k)).join("")}</div>
      <div class="ij-stage"><img src="/api/intake/${q(name)}/draft-image/${q(im.name)}?t=${Date.now()}" alt=""></div></div>`).join("")}
    <h2>값 칸</h2>
    ${table(d.regions, [["page", "쪽", g => g.page + 1, true], ["key", "추출 키", g => `<span class="mono">${esc(g.key)}</span>`], ["label", "이름표"],
      ["common", "공통 키", g => g.common ? `<span class="mono">${esc(g.common)}</span>` : `<span class="muted">문서별</span>`], ["value", "견본 값"]])}`;
}
