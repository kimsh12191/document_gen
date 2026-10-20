// ⑧ 작업 › 분석기: 서식 그림 → html 서식(html) / overlay 값 영역 초안(layout). 결과 검사·렌더링을 보고 승인해야 등록된다.
// 서버: studio/api_html.py, studio/analyzers.py. 설계: DESIGN.md 7절
"use strict";

addRoute(/^#\/jobs\/analyzer\/([^/]+)$/, id => viewAnalyzerJob(decodeURIComponent(id)), "jobs");

const AZ_KIND = { html: "이미지 → html 서식", layout: "값 영역 초안 (overlay)", autolabel: "실서류 먼저 채우기 (autolabel)" };

async function analyzerPanel(el) {
  const r = await api("/api/analyzer");
  const [imports, forms] = await Promise.all([api("/api/imports"), loadForms()]);
  const imgForms = forms.filter(f => f.kind === "overlay" && f.origin === "image");
  el.innerHTML = `
    <h2>분석기 작업</h2>
    <div class="sub">서식 그림을 분석기(설정의 providers)에 맡깁니다. 결과는 studio 가 검사·렌더링하고, 사람이 승인해야 서식으로 등록됩니다(등록 뒤에도 검수 전).
      외부 분석기(external)에는 실서류에서 온 그림을 보낼 수 없습니다.</div>
    ${r.providers.length ? "" : `<div class="panel warnbox">설정(studio/config.json)에 분석기가 없습니다. <span class="mono">providers</span> 예시는 studio/DESIGN.md 7.2, ⑨ 설정에서 연결 확인.</div>`}
    <div class="panel" style="margin-bottom:10px">
      <div class="bar">
        <label>작업 <select id="az-kind"><option value="html">${AZ_KIND.html}</option><option value="layout">${AZ_KIND.layout}</option></select></label>
        <label>분석기 <select id="az-prov">${r.providers.map(p => `<option value="${esc(p.name)}">${esc(p.name)} (${p.kind}${p.external ? ", 외부" : ", 내부"})</option>`).join("")}</select></label>
        <label>그림 <select id="az-src"><option value="upload">파일 올리기</option><option value="batch">가져온 묶음의 쪽</option><option value="form">가져온 이미지 서식</option></select></label>
      </div>
      <div id="az-src-box"></div>
      <div class="bar" id="az-target"></div>
      <div class="bar"><input type="text" id="az-comment" placeholder="분석기에 덧붙일 말 (선택)" style="flex:1"><button class="primary" id="az-go" ${r.providers.length ? "" : "disabled"}>맡기기</button></div>
    </div>
    ${r.jobs.length ? table(r.jobs, [["id", "작업", j => `<a href="#/jobs/analyzer/${q(j.id)}">${esc(j.id)}</a>`],
      ["kind", "종류", j => esc(AZ_KIND[j.kind] || j.kind)], ["provider", "분석기", j => `${esc(j.provider)}${j.external ? ` <span class="tag warn">외부</span>` : ""}`],
      ["target", "대상", j => esc(j.target.name || j.target.form_id || "-")],
      ["status", "상태", j => `<span class="tag ${j.status === "done" ? "ok" : j.status === "running" ? "" : "warn"}">${JOB_STATUS[j.status] || j.status || "-"}</span>`],
      ["result", "검사", j => j.result ? (j.result.ok ? `<span class="tag ok">통과</span>` : `<span class="tag warn">문제 ${j.result.errors.length}</span>`) : "-"],
      ["approved", "승인", j => j.approved ? `<span class="tag ok">${esc(j.approved.as)}</span>` : ""], ["created", "만든 때"]])
      : `<p class="muted">분석기 작업이 없습니다.</p>`}`;
  const kindSel = $("#az-kind"), srcSel = $("#az-src");
  const drawSrc = () => {
    const k = kindSel.value;
    if (k === "layout") srcSel.value = "form";
    srcSel.disabled = k === "layout";
    const s = srcSel.value;
    $("#az-src-box").innerHTML = s === "upload" ? `<div class="bar"><input type="file" id="az-file" accept=".png,.jpg,.jpeg,.pdf">
        <label><input type="checkbox" id="az-real" checked> 실서류에서 온 그림</label>
        <label><input type="checkbox" id="az-public"> 빈 서식·공개 서식 (외부 분석기에 보내도 됨)</label></div>`
      : s === "batch" ? `<div class="bar"><select id="az-batch">${imports.imports.map(b => `<option>${esc(b.name)}</option>`).join("")}</select>
        <input type="text" id="az-page" placeholder="쪽 ID (예: hf169_3000000/p1)" style="width:320px">
        <span class="muted">④ 가져오기 › 포맷 화면의 쪽 이름</span></div>`
      : `<div class="bar"><select id="az-form">${imgForms.map(f => `<option value="${esc(f.id)}">${esc(f.id)} ${esc(f.name)}</option>`).join("")}</select>
        ${imgForms.length ? "" : `<span class="muted">가져온 이미지 서식이 없습니다 (④ 가져오기 › 템플릿으로)</span>`}</div>`;
    $("#az-target").innerHTML = k === "html" ? `<label>새 서식 ID <input type="text" id="az-id" placeholder="예: tx_history_a" style="width:180px"></label>
        <label>이름 <input type="text" id="az-name" placeholder="거래내역확인서"></label>
        <label>그룹 <select id="az-group">${(state.info && state.info.groups || []).map(g => `<option>${esc(g)}</option>`).join("") || `<option>finance</option>`}</select></label>`
      : `<span class="muted">결과(값 영역)를 승인하면 그 서식의 영역 편집기에 "추가" 칸으로 들어갑니다.</span>`;
  };
  kindSel.onchange = drawSrc; srcSel.onchange = drawSrc;
  drawSrc();
  api("/api/groups").then(gs => { const g = $("#az-group"); if (g) g.innerHTML = gs.map(x => `<option value="${esc(x.id)}">${esc(x.name)}</option>`).join(""); }).catch(() => {});
  $("#az-go").onclick = async () => {
    const k = kindSel.value, s = srcSel.value;
    let source;
    try {
      if (s === "upload") {
        const f = $("#az-file").files[0];
        if (!f) return toast("그림 파일을 고르세요", true);
        const fd = new FormData(); fd.append("file", f);
        const res = await fetch("/api/analyzer/upload", { method: "POST", body: fd });
        const up = await res.json();
        if (!res.ok) throw new Error(up.detail || res.status);
        source = { upload: up.upload };
      } else if (s === "batch") source = { batch: $("#az-batch").value, pages: [$("#az-page").value.trim()] };
      else source = { form: $("#az-form").value };
      if ((r.providers.find(p => p.name === $("#az-prov").value) || {}).external &&
          !confirm("외부 분석기입니다. 빈 서식·공개 서식 그림만 보냅니다. 보낼까요?")) return;
      const target = k === "html" ? { form_id: $("#az-id").value.trim(), name: $("#az-name").value.trim(), group: $("#az-group").value } : {};
      const res = await api("/api/analyzer", { kind: k, provider: $("#az-prov").value, source, target, comment: $("#az-comment").value,
        real_data: $("#az-real") ? $("#az-real").checked : true, public: $("#az-public") ? $("#az-public").checked : false });
      toast("맡겼습니다");
      location.hash = `#/jobs/analyzer/${q(res.analyzer)}`;
    } catch (e) { toast(e.message, true); }
  };
}

async function viewAnalyzerJob(id) {
  const a = await api(`/api/analyzer/${q(id)}`);
  const run = a.run || {};
  const f = p => `/api/analyzer/${q(id)}/file?path=${q(p)}`;
  const res = a.result;
  const renders = res && res.renders ? Object.entries(res.renders) : [];
  main().innerHTML = `
    <div class="muted"><a href="#/jobs">작업</a> › 분석기</div>
    <h1>${esc(AZ_KIND[a.kind] || a.kind)} <span class="mono muted">${esc(a.id)}</span></h1>
    <div class="bar"><span class="tag">${esc(a.provider)} · ${esc(a.provider_kind)}</span>${a.external ? `<span class="tag warn">외부</span>` : `<span class="tag ok">내부</span>`}
      <span class="tag ${run.status === "done" ? "ok" : run.status === "running" ? "" : "warn"}">${JOB_STATUS[run.status] || run.status || "-"}</span>
      ${run.id ? `<a href="#/jobs/${q(run.id)}">실행 로그</a>` : ""}
      <span class="muted">그림 출처: ${esc(a.source.label || "-")}${a.source.real_data ? " (실서류)" : ""} · 대상: ${esc(a.target.name || a.target.form_id || "-")}</span>
      ${a.from_job ? `<span class="muted">· 다시 고친 작업 <a href="#/jobs/analyzer/${q(a.from_job)}">${esc(a.from_job)}</a></span>` : ""}</div>
    ${run.error ? `<p class="err">${esc(run.error)}</p>` : ""}
    <div class="rc-grid">
      <div class="panel">
        <b>보낸 그림</b>
        <div class="ds-imgs">${a.inputs.filter(n => /\.png$/.test(n)).map(n => `<div class="stage"><img src="${f("input/" + n)}" alt=""></div>`).join("")}</div>
        <details><summary>보낸 파일 ${a.sent.length}개와 지시문</summary><div class="muted mono">${a.sent.map(esc).join("<br>")}</div><pre class="ans">${esc(a.task)}</pre></details>
      </div>
      <div class="panel">
        <b>검사</b>
        ${res ? (res.ok ? `<span class="tag ok">통과</span>` : `<ul class="checks">${res.errors.map(e => `<li class="warn">⚠ ${esc(e)}</li>`).join("")}</ul>`)
          : `<span class="muted">${run.status === "running" ? "분석기가 일하는 중…" : "결과 없음"}</span>`}
        ${renders.map(([rows, info]) => `<div class="muted" style="margin-top:6px">행 ${rows === "max" ? "최대" : "최소"}: ${info.pages}쪽 · 항목 ${info.fields} · 빈 값 ${info.empty}
          ${info.checks.length ? ` · <span class="kr">경고 ${info.checks.length}</span>` : ""}</div>
          ${info.checks.length ? `<ul class="checks">${info.checks.map(c => `<li class="warn">${esc(c.text)}</li>`).join("")}</ul>` : ""}
          <div class="ds-imgs">${info.images.map(p => `<div class="stage"><img src="${f(p)}" alt=""></div>`).join("")}</div>`).join("")}
        ${a.kind === "layout" && res ? `<div class="muted">값 영역 ${res.items ?? 0}개</div>` : ""}
        ${a.kind === "autolabel" && res && res.autolabel ? `<div>채움 ${res.autolabel.done} · 건너뜀 ${res.autolabel.skipped} · 실패 ${res.autolabel.failed}
          · <a href="#/labels/${q(a.target.batch)}/format/${q(a.target.format)}">라벨 검수로</a></div>` : ""}
      </div>
    </div>
    ${Object.entries(a.output).map(([n, t]) => `<details class="panel"><summary class="mono">output/${esc(n)}</summary><pre class="ans mono">${esc(t)}</pre></details>`).join("")}
    <div class="rc-grid" style="margin-top:10px">
      <div class="panel">
        <b>승인</b>
        ${a.kind === "autolabel" ? `<div class="muted">autolabel 은 승인이 없습니다. 채운 값은 라벨 검수에서 사람이 확인해야 정답이 됩니다.</div>`
          : a.review.approved ? `<div><span class="tag ok">승인함</span> ${esc(a.review.approved.as)} · ${esc(a.review.approved.by)} ${esc(a.review.approved.at)}
            ${a.kind === "html" ? ` · <a href="#/forms/${q(a.review.approved.as)}/html">html 편집기로</a>` : ` · <a href="#/forms/${q(a.review.approved.as)}/edit">영역 편집기로</a>`}</div>`
          : a.kind === "html" && !a.target.update ? `<div class="bar"><label>서식 ID <input type="text" id="ap-id" value="${esc(a.target.form_id || "")}" style="width:180px"></label>
              <label>이름 <input type="text" id="ap-name" value="${esc(a.target.name || "")}"></label>
              <button class="primary" id="ap-go" ${res && res.ok ? "" : "disabled"}>승인하고 등록</button></div>
              <div class="muted">${a.source.real_data && !a.source.public ? "실서류 그림이라 private_forms_dir 에 만듭니다." : "docgen/templates/copies/&lt;ID&gt;/ 에 만듭니다."}</div>`
          : `<button class="primary" id="ap-go" ${res && res.ok ? "" : "disabled"}>${a.kind === "html" ? `승인하고 ${esc(a.target.form_id)} 바꾸기` : `승인하고 ${esc(a.target.form_id)} 영역 편집기에 넣기`}</button>`}
      </div>
      <div class="panel">
        <b>의견 · 다시 고쳐</b>
        ${(a.review.comments || []).map(c => `<div class="muted">${esc(c.at)} ${esc(c.by)}: ${esc(c.text)}</div>`).join("")}
        <div class="bar" style="margin-top:6px"><input type="text" id="rd-text" placeholder="고칠 점" style="flex:1"><button id="rd-go">다시 맡기기</button><button id="rd-check">다시 검사</button></div>
      </div>
    </div>`;
  if ($("#ap-go")) $("#ap-go").onclick = async () => {
    try {
      const body = $("#ap-id") ? { form_id: $("#ap-id").value.trim(), name: $("#ap-name").value.trim() } : {};
      const r = await api(`/api/analyzer/${q(id)}/approve`, body);
      toast(`승인했습니다: ${r.as}`); state.forms = null;
      location.hash = a.kind === "html" ? `#/forms/${q(r.as)}/html` : `#/forms/${q(r.as)}/edit`;
    } catch (e) { toast(e.message, true); }
  };
  $("#rd-go").onclick = async () => {
    try { const r = await api(`/api/analyzer/${q(id)}/redo`, { text: $("#rd-text").value }); location.hash = `#/jobs/analyzer/${q(r.analyzer)}`; }
    catch (e) { toast(e.message, true); }
  };
  $("#rd-check").onclick = async () => { try { await api(`/api/analyzer/${q(id)}/recheck`, {}); viewAnalyzerJob(id); } catch (e) { toast(e.message, true); } };
  if (run.status === "running") setTimeout(() => { if (location.hash === `#/jobs/analyzer/${q(id)}`) viewAnalyzerJob(id); }, 3000);
}
