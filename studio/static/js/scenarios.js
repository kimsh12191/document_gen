// ③ 시나리오·묶음: 업무 시나리오(필수 서류) 편집, 대조 사례·심사 규칙 목록. 묶음 보기는 ⑥ 데이터셋 › 묶음 탭.
// ⑧ 작업: 데이터셋 빌드 등 백그라운드 작업의 진행과 로그.
"use strict";

async function view_scenarios() {
  const [r, forms] = await Promise.all([api("/api/scenarios"), loadForms()]);
  const names = new Map(forms.map(f => [f.id, f.name]));
  let list = clone(r.scenarios);
  let dirty = false;
  const draw = () => {
    main().innerHTML = `
      <h1>시나리오·묶음</h1>
      <div class="sub">업무마다 고객이 내는 필수 서류입니다. 은행 업무 데이터셋을 만들 때 시나리오마다 고객 묶음을 만들고, 묶음에서
        서류 구비·대조·심사 문항이 나옵니다. 저장하면 <span class="mono">docgen/scenarios.json</span>에 씁니다.
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
          <div class="sc-docs">${s.docs.map((d, j) => `<span class="tag ${d.kind || ""}">${esc(d.id)} · ${esc(d.name || names.get(d.id) || "?")}
            ${d.reviewed ? "✓" : ""}<a href="#" data-rm="${i}:${j}" title="빼기">×</a></span>`).join("")}
            <input type="text" list="sc-forms" data-addto="${i}" placeholder="서식 ID 더하기" style="width:200px"></div>
        </div>`).join("")}
      <h2>대조 사례 (${r.cases.length})</h2>
      <div class="sub">코드(<span class="mono">docgen/bench/cases.py</span>)로 둡니다. 레시피에서 사례마다 켜고 끄고 변조 비율을 정합니다.</div>
      ${table(r.cases, [["id", "ID", c => `<span class="mono">${esc(c.id)}</span>`], ["title", "사례"], ["category", "분류"], ["basis", "근거"]])}
      <h2>심사 규칙 (${r.rules.length})</h2>
      <div class="sub mono">${r.rules.map(esc).join(" · ")}</div>`;
    const mark = () => { dirty = true; $("#sc-save").disabled = false; $("#sc-dirty").textContent = "저장 안 됨"; $("#sc-dirty").className = "kr"; };
    $$(".sc-card input[data-f]").forEach(inp => inp.onchange = () => {
      const s = list[+inp.closest(".sc-card").dataset.i];
      if (inp.dataset.f === "extra") { try { s.extra = JSON.parse(inp.value || "{}"); } catch { toast("프로필 값은 JSON 이어야 합니다", true); return; } }
      else s[inp.dataset.f] = inp.value.trim();
      mark();
    });
    $$("[data-addto]").forEach(inp => inp.onchange = () => {
      const s = list[+inp.dataset.addto], id = inp.value.trim();
      if (!id) return;
      if (!names.has(id)) { toast(`모르는 서식: ${id}`, true); return; }
      if (!s.docs.some(d => d.id === id)) s.docs.push({ id, name: names.get(id), kind: id.startsWith("hf") ? "overlay" : "html" });
      mark(); draw();
    });
    main().onclick = e => {
      const rm = e.target.dataset.rm, del = e.target.dataset.del;
      if (rm) { e.preventDefault(); const [i, j] = rm.split(":").map(Number); list[i].docs.splice(j, 1); mark(); draw(); }
      if (del !== undefined) { list.splice(+del, 1); mark(); draw(); }
    };
    $("#sc-add").onclick = () => { list.push({ id: `new_${list.length + 1}`, name: "새 업무", docs: [], extra: {} }); mark(); draw(); };
    $("#sc-save").onclick = async () => {
      try {
        const res = await api("/api/scenarios", { scenarios: list.map(s => ({ id: s.id, name: s.name, docs: s.docs.map(d => d.id), extra: s.extra })) }, "PUT");
        r.scenarios = res.scenarios; list = clone(res.scenarios); dirty = false; toast("저장했습니다"); draw();
      } catch (e) { toast(e.message, true); }
    };
  };
  state.leave = unload => !dirty || (unload ? false : confirm("저장하지 않은 시나리오 수정이 있습니다. 버릴까요?"));
  draw();
}

// ⑧ 작업 -------------------------------------------------------------------
const JOB_STATUS = { running: "도는 중", done: "끝남", failed: "실패", cancelled: "취소", interrupted: "끊김" };

async function view_jobs() {
  const r = await api("/api/jobs");
  main().innerHTML = `
    <h1>작업</h1>
    <div class="sub">데이터셋 빌드처럼 오래 걸리는 일입니다. 명령줄과 같은 명령을 그대로 돌립니다 (명령은 작업을 열면 보입니다).
      분석기 작업(이미지 → html 서식)은 8단계에서 여기에 더해집니다.</div>
    ${r.jobs.length ? table(r.jobs, [["title", "작업", j => `<a href="#/jobs/${encodeURIComponent(j.id)}">${esc(j.title)}</a>`],
      ["status", "상태", j => `<span class="tag ${j.status === "done" ? "ok" : j.status === "running" ? "" : "warn"}">${JOB_STATUS[j.status] || j.status}</span>`],
      ["started", "시작"], ["ended", "끝"], ["result", "결과", j => j.result && j.result.dataset ? `<a href="#/datasets/${encodeURIComponent(j.result.dataset)}">${esc(j.result.dataset)}</a>` : esc(j.error || "")]])
      : `<p class="muted">작업이 없습니다.</p>`}`;
  if (r.jobs.some(j => j.status === "running")) setTimeout(() => { if (location.hash === "#/jobs") view_jobs(); }, 3000);
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
      ${j.status === "running" ? `<button id="jb-cancel">취소</button>` : ""}
      ${j.result && j.result.dataset ? `<a href="#/datasets/${encodeURIComponent(j.result.dataset)}">만든 데이터셋 열기</a>` : ""}</div>
    ${j.error ? `<p class="err">${esc(j.error)}</p>` : ""}
    <div class="muted">명령</div><pre class="ans mono">${esc((j.cmd || []).join(" "))}</pre>
    <div class="muted">로그 (끝부분)</div><pre class="ans mono log">${esc(j.log_tail || "")}</pre>`;
  if ($("#jb-cancel")) $("#jb-cancel").onclick = async () => { if (confirm("작업을 멈출까요?")) { await api(`/api/jobs/${encodeURIComponent(id)}/cancel`, {}); viewJob(id); } };
  const log = $("pre.log"); if (log) log.scrollTop = log.scrollHeight;
  if (j.status === "running") setTimeout(() => { if (location.hash === `#/jobs/${encodeURIComponent(id)}`) viewJob(id); }, 2000);
}
