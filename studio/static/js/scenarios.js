// ③ 시나리오·묶음: 서류 이미지·구성, 시나리오별 처리 설정과 예시 실행. 생성된 묶음은 ⑥ 데이터셋에서 본다.
// 서류 펼쳐 보기는 scenario-preview.js, 처리 설정은 scenario-processing.js. 서버: GET/PUT /api/scenarios (studio/api_bank.py, bank_data.py)
// ⑧ 작업: 데이터셋 빌드 등 백그라운드 작업의 진행과 로그 (/api/jobs, studio/jobs.py). 분석기 작업 화면은 analyzer.js.
"use strict";

async function view_scenarios() {
  const [r, forms] = await Promise.all([api("/api/scenarios"), loadForms()]);
  const names = new Map(forms.map(f => [f.id, f.name]));
  const byId = new Map(forms.map(f => [f.id, f]));
  const roles = new Map((r.document_roles || []).flatMap(role => role.forms.map(id => [id, role])));
  const roleOf = id => roles.get(id) || { id, name: names.get(id) || id, forms: [id] };
  let list = clone(r.scenarios);
  let dirty = false;
  const previews = new ScenarioPreviews();
  const processing = new ScenarioProcessing(r, previews);
  const draw = () => {
    main().innerHTML = `
      <h1>시나리오·묶음</h1>
      <div class="sub">업무마다 고객이 내는 필수 서류입니다. 은행 업무 데이터셋을 만들 때 시나리오마다 고객 묶음을 만들고, 묶음에서
        서류 구비·대조·심사 문항이 나옵니다. 저장하면 <span class="mono">docgen/scenarios.json</span>에 씁니다.
        서류 이미지를 펼치면 같은 고객으로 구성한 필수 서류를 보고, 눌러서 확대할 수 있습니다.
        <b>이미 있던 시나리오의 순서는 바꾸지 않습니다</b> (순서가 고객 seed 를 정함). 만든 묶음은 ⑥ 데이터셋 › 묶음 탭에서 봅니다.</div>
      <div class="bar"><button class="primary" id="sc-save" ${dirty ? "" : "disabled"}>저장</button><button id="sc-add">새 시나리오</button>
        <span id="sc-dirty" class="${dirty ? "kr" : "muted"}">${dirty ? "저장 안 됨" : ""}</span></div>
      <datalist id="sc-forms">${forms.map(f => `<option value="${esc(f.id)}">${esc(f.name)}</option>`).join("")}</datalist>
      ${list.map((s, i) => `
        <div class="panel sc-card" data-i="${i}">
          <div class="bar"><input type="text" data-f="id" value="${esc(s.id)}" ${r.scenarios.some(x => x.id === s.id) ? "readonly" : ""} style="width:200px" class="mono">
            <input type="text" data-f="name" value="${esc(s.name)}" style="width:220px">
            <span class="muted">프로필 값</span><input type="text" data-f="extra" value="${esc(JSON.stringify(s.extra || {}))}" class="mono" style="width:220px"
              title='서류 생성 함수가 참고하는 값. 예: {"loan_kind": "jeonse"}'>
            <span class="muted">만든 묶음 ${s.bundles || 0}</span>
            ${r.scenarios.some(x => x.id === s.id) ? "" : `<button data-del="${i}">지우기</button>`}</div>
          <div class="sub">제출 역할 하나당 문서 한 개를 넣습니다. 고정 서식을 쓰거나, 선택한 후보 중 하나를 고객 seed로 샘플링합니다.
            각 HTML 안의 레이아웃도 별도로 샘플링됩니다. 후보별 추출·비교 항목은 아래 처리 설정에서 연결하세요.</div>
          <div class="sc-docs">${s.docs.map((d, j) => { const role = roleOf(d.id), sample=s.sampling?.[d.id], on=sample?.mode==='sample'; return `<div class="panel">
            <b>${esc(role.name)}</b> <a href="#" data-rm="${i}:${j}" title="빼기">×</a>
            <label><input type="checkbox" data-sampling="${i}:${j}" ${on?'checked':''}> 후보 중 하나 샘플링</label>
            <span class="muted">${on?'항목 설정의 기준 서식':'고정 서식'}</span>
            <select data-variant="${i}:${j}" aria-label="${esc(role.name)} 서식 선택">${role.forms.map(id =>
              `<option value="${esc(id)}" ${id === d.id ? "selected" : ""}>${esc(names.get(id) || id)} · ${esc(byId.get(id)?.kind || "")} · ${esc(id)}</option>`).join("")}</select>
            <a href="#/forms/${encodeURIComponent(d.id)}" target="_blank">서식·값 확인</a>${role.note ? `<div class="muted">${esc(role.note)}</div>` : ""}
            ${on?`<div class="sub">고객마다 아래 후보에서 하나만 선택합니다. 가중치가 같으면 같은 비율로 뽑습니다.</div>${role.forms.map(id=>`<div class="bar"><label><input type="checkbox" data-candidate="${i}:${j}" value="${esc(id)}" ${sample.forms.includes(id)?'checked':''}>${esc(names.get(id) || id)} · ${esc(id)}</label><label>가중치 <input type="number" data-weight="${i}:${j}" data-form="${esc(id)}" value="${sample.weights?.[id] || 1}" min="0.01" step="0.1" required style="width:80px" ${sample.forms.includes(id)?'':'disabled'}></label></div>`).join('')}`:''}
            </div>`; }).join("")}
            <input type="text" list="sc-forms" data-addto="${i}" placeholder="서식 ID 더하기" style="width:200px"></div>
          ${previews.html(s, i)}
          ${processing.html(s, i)}
        </div>`).join("")}
      <h2>대조 사례 (${r.cases.length})</h2>
      <div class="sub">코드(<span class="mono">docgen/bench/cases.py</span>)로 둡니다. 레시피에서 사례마다 켜고 끄고 변조 비율을 정합니다.</div>
      ${table(r.cases, [["id", "ID", c => `<span class="mono">${esc(c.id)}</span>`], ["title", "사례"], ["category", "분류"], ["basis", "근거"]])}
      <h2>심사·계산 규칙 (${Object.keys(r.processing_rules).length})</h2>
      <div class="sub">${Object.values(r.processing_rules).map(esc).join(" · ")}</div>`;
    const mark = () => { dirty = true; $("#sc-save").disabled = false; $("#sc-dirty").textContent = "저장 안 됨"; $("#sc-dirty").className = "kr"; };
    $$(".sc-card input[data-f]").forEach(inp => inp.onchange = () => {
      const s = list[+inp.closest(".sc-card").dataset.i];
      if (inp.dataset.f === "extra") {
        try {
          const extra = JSON.parse(inp.value || "{}");
          if (!extra || Array.isArray(extra) || typeof extra !== "object") throw new Error();
          s.extra = extra;
          inp.setCustomValidity("");
        } catch { inp.setCustomValidity("프로필 값은 JSON 객체여야 합니다"); inp.reportValidity(); return; }
      }
      else s[inp.dataset.f] = inp.value.trim();
      mark();
      processing.invalidate(inp.closest(".sc-card"), s);
      if (inp.dataset.f === "extra" || inp.dataset.f === "id") previews.refresh(inp.closest(".sc-card"), s);
    });
    $$("[data-addto]").forEach(inp => inp.onchange = () => {
      const s = list[+inp.dataset.addto], id = inp.value.trim();
      if (!id) return;
      if (!names.has(id)) { toast(`모르는 서식: ${id}`, true); return; }
      if (s.docs.some(d => roleOf(d.id).id === roleOf(id).id)) { toast("같은 제출 역할이 있습니다. 해당 역할의 서식 선택에서 바꾸세요", true); return; }
      s.docs.push({ id, name: names.get(id), kind: byId.get(id).kind });
      processing.invalidate(inp.closest(".sc-card"), s);
      mark(); draw();
    });
    $$('[data-variant]').forEach(inp => inp.onchange = () => {
      const [i,j] = inp.dataset.variant.split(':').map(Number), s = list[i], old = s.docs[j].id, id = inp.value;
      s.docs[j] = {id, name:names.get(id), kind:byId.get(id).kind};
      if(s.sampling?.[old]){s.sampling[id]=s.sampling[old];delete s.sampling[old];}
      for (const op of s.processing?.operations || []) for (const side of ['left','right']) {
        if (op[side]?.doc === old) { op[side] = {doc:id, key:'__select_field__'}; op.enabled = false; }
      }
      processing.invalidate(inp.closest('.sc-card'), s); mark(); draw();
    });
    $$('[data-sampling]').forEach(inp=>inp.onchange=()=>{
      const [i,j]=inp.dataset.sampling.split(':').map(Number),s=list[i],id=s.docs[j].id;
      s.sampling ||= {};
      if(inp.checked)s.sampling[id]={mode:'sample',forms:[...roleOf(id).forms],weights:{}};else delete s.sampling[id];
      processing.invalidate(inp.closest('.sc-card'),s);mark();draw();
    });
    $$('[data-candidate]').forEach(inp=>inp.onchange=()=>{
      const [i,j]=inp.dataset.candidate.split(':').map(Number),s=list[i],conf=s.sampling[s.docs[j].id];
      conf.forms=inp.checked?[...conf.forms,inp.value]:conf.forms.filter(id=>id!==inp.value);
      if(!inp.checked)delete conf.weights[inp.value];
      processing.invalidate(inp.closest('.sc-card'),s);mark();draw();
    });
    $$('[data-weight]').forEach(inp=>inp.onchange=()=>{
      if(!inp.reportValidity())return;
      const [i,j]=inp.dataset.weight.split(':').map(Number),s=list[i];s.sampling[s.docs[j].id].weights[inp.dataset.form]=Number(inp.value);
      processing.invalidate(inp.closest('.sc-card'),s);previews.refresh(inp.closest('.sc-card'),s);mark();
    });
    main().onclick = e => {
      const rm = e.target.dataset.rm, del = e.target.dataset.del;
      if (rm) { e.preventDefault(); const [i, j] = rm.split(":").map(Number),s=list[i],id=s.docs[j].id; processing.invalidate(e.target.closest(".sc-card"), s); s.docs.splice(j, 1);if(s.sampling)delete s.sampling[id];s.processing.operations=s.processing.operations.filter(op=>![op.left?.doc,op.right?.doc].includes(id)); mark(); draw(); }
      if (del !== undefined) { list.splice(+del, 1); mark(); draw(); }
    };
    $("#sc-add").onclick = () => { list.push({ id: `new_${list.length + 1}`, name: "새 업무", docs: [], extra: {} }); mark(); draw(); };
    $("#sc-save").onclick = async () => {
      if ($$(".sc-card input[data-f], .sc-operations [required], .sc-docs [required]").some(inp => !inp.reportValidity())) return;
      try {
        const res = await api("/api/scenarios", { scenarios: list.map(s => ({ id: s.id, name: s.name, docs: s.docs.map(d => d.id), extra: s.extra, processing: s.processing,sampling:s.sampling })) }, "PUT");
        r.scenarios = res.scenarios; list = clone(res.scenarios); dirty = false; toast("저장했습니다"); draw();
      } catch (e) { toast(e.message, true); }
    };
    $$(".sc-card").forEach((card, i) => { processing.bind(card, list[i], mark); previews.bind(card, list[i]); });
  };
  state.leave = unload => !dirty || (unload ? false : confirm("저장하지 않은 시나리오 수정이 있습니다. 버릴까요?"));
  draw();
}

// ⑧ 작업 -------------------------------------------------------------------
const JOB_STATUS = { running: "도는 중", done: "끝남", failed: "실패", cancelled: "취소", interrupted: "끊김" };

async function view_jobs() {
  main().innerHTML = `
    <h1>작업</h1>
    <div class="sub">데이터셋 빌드처럼 오래 걸리는 일입니다. 명령줄과 같은 명령을 그대로 돌립니다 (명령은 작업을 열면 보입니다).
      아래 분석기 작업은 서식 그림을 분석기에 맡겨 html 서식이나 값 영역 초안을 받는 일입니다.</div>
    <div id="jb-list"></div><div id="az-panel"></div>`;
  if (typeof analyzerPanel === "function") analyzerPanel($("#az-panel")).catch(e => { $("#az-panel").innerHTML = `<p class="err">${esc(e.message)}</p>`; });
  drawJobList();
}

async function drawJobList() {   // 도는 작업이 있으면 목록만 3초마다 다시 (분석기 입력 칸은 그대로)
  const box = $("#jb-list");
  if (!box) return;
  const r = await api("/api/jobs");
  box.innerHTML = `
    ${r.jobs.length ? table(r.jobs, [["title", "작업", j => `<a href="#/jobs/${encodeURIComponent(j.id)}">${esc(j.title)}</a>`],
      ["status", "상태", j => `<span class="tag ${j.status === "done" ? "ok" : j.status === "running" ? "" : "warn"}">${JOB_STATUS[j.status] || j.status}</span>`],
      ["started", "시작"], ["ended", "끝"], ["result", "결과", j => j.result && j.result.dataset ? `<a href="#/datasets/${encodeURIComponent(j.result.dataset)}">${esc(j.result.dataset)}</a>` : esc(j.error || "")]])
      : `<p class="muted">작업이 없습니다.</p>`}`;
  if (r.jobs.some(j => j.status === "running")) setTimeout(() => { if (location.hash === "#/jobs") drawJobList(); }, 3000);
}

addRoute(/^#\/jobs\/([^/]+)$/, id => viewJob(decodeURIComponent(id)), "jobs");

async function viewJob(id) {
  const j = await api(`/api/jobs/${encodeURIComponent(id)}`);
  const pg = j.progress ? `<div class="progress"><div style="width:${(100 * j.progress[0] / j.progress[1]).toFixed(1)}%"></div></div>
    <span class="muted">${j.progress[0]} / ${j.progress[1]}</span>` : "";
  main().innerHTML = `
    <div class="muted"><a href="#/jobs">작업</a></div>
    <h1>${esc(j.title)}</h1>
    <div class="bar"><span class="tag ${j.status === "done" ? "ok" : j.status === "running" ? "" : "warn"}">${JOB_STATUS[j.status] || j.status}</span>
      <span class="muted">${esc(j.started)}${j.ended ? ` → ${esc(j.ended)}` : ""}</span> ${pg}
      ${j.status === "running" && j.stage !== "registering" ? `<button id="jb-cancel">취소</button>` : ""}
      ${j.result && j.result.dataset ? `<a href="#/datasets/${encodeURIComponent(j.result.dataset)}">만든 데이터셋 열기</a>` : ""}</div>
    ${j.error ? `<p class="err">${esc(j.error)}</p>` : ""}
    <div class="muted">명령</div><pre class="ans mono">${esc((j.cmd || []).join(" "))}</pre>
    <div class="muted">로그 (끝부분)</div><pre class="ans mono log">${esc(j.log_tail || "")}</pre>`;
  if ($("#jb-cancel")) $("#jb-cancel").onclick = async () => { if (confirm("작업을 멈출까요?")) { await api(`/api/jobs/${encodeURIComponent(id)}/cancel`, {}); viewJob(id); } };
  const log = $("pre.log"); if (log) log.scrollTop = log.scrollHeight;
  if (j.status === "running") setTimeout(() => { if (location.hash === `#/jobs/${encodeURIComponent(id)}`) viewJob(id); }, 2000);
}
