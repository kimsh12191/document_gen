// ⑥ 데이터셋 › 생성 현황·등록된 데이터셋 목록: 생성 진행과 자동 등록을 확인한다. 목록만 갱신해 입력 중인 이름·설정은 유지한다.
// 돌고 있는 작업이 있으면 2초마다 다시 읽는다. 서버: GET /api/datasets·/api/builds (studio/api_datasets.py, api_bank.py, build_registration.py)
// datasets.js 의 view_datasets 가 startDatasetDashboard 를, 만들기 버튼(recipes.js)이 datasetBuildStarted 를 부른다.
"use strict";

let datasetBuildDashboard = null;

function datasetRegistryHTML(r, added = new Set()) {
  if (!r.datasets.length) return `<p class="muted">등록된 데이터셋이 없습니다. 위에서 새로 만들면 완료 후 여기에 자동으로 등록됩니다.</p>`;
  return table(r.datasets, [
    ["name", "이름", d => `<a href="#/datasets/${encodeURIComponent(d.id)}">${esc(d.name)}</a> <span class="mono muted">${esc(d.id)}</span>
      ${added.has(d.id) ? `<span class="tag ok">새로 등록됨</span>` : ""}`],
    ["groups", "과제", d => dsTag(d)], ["source", "출처", d => esc(r.sources[d.source] || d.source)],
    ["gt", "정답", d => esc((r.gts[d.gt] || d.gt).split(" (")[0])],
    ["real", "", d => d.real_data ? `<span class="tag warn">실서류</span>` : ""],
    ["version", "버전", d => esc(d.version || "-")],
    ["counts", "문항", d => esc(Object.entries(d.counts || {}).filter(([k]) => !/train|val|pages|documents/.test(k) || k === "benchmark_tasks")
      .reduce((a, [, v]) => a + (+v || 0), 0) || "-")],
    ["frozen", "고정", d => d.frozen ? `<span class="tag ok">고정</span>` : ""],
    ["exists", "", d => (d.exists ? "" : `<span class="tag warn">폴더 없음</span> `)
      + `<button type="button" class="link ds-unreg" data-id="${esc(d.id)}" data-frozen="${d.frozen ? 1 : ""}" data-exists="${d.exists ? 1 : ""}">등록 해제</button>`],
  ], d => added.has(d.id) ? `class="ds-new"` : "");
}

function datasetBuildsHTML(jobs) {
  const pending = j => ["running", "interrupted"].includes(j.status);
  const shown = [...jobs.filter(pending), ...jobs.filter(j => !pending(j)).slice(0, 5)];
  const status = j => j.stage === "registering" ? "등록 중" : j.stage === "registration_failed" ? "등록 실패"
    : ({ running: "생성 중", done: j.result?.dataset ? "자동 등록 완료" : "완료 · 등록 확인 필요", failed: "생성 실패", cancelled: "취소", interrupted: "studio 재시작 · 생성은 계속 (확인 중)" }[j.status] || j.status);
  const removable = j => ["failed", "cancelled"].includes(j.status) || (j.status === "done" && !j.result?.dataset);
  return `<div class="panel ds-build-panel"><div class="bar"><h2>데이터셋 생성 현황</h2>
      <button type="button" id="ds-jobs-cleanup" title="실패·취소·멈춘 작업, 만든 데이터셋이 등록 해제됐거나 폴더가 없어진 작업의 기록을 지웁니다 (데이터셋 폴더는 그대로)">끝난 기록 정리</button></div>
    <div class="sub">완료하면 아래 등록 목록에 자동으로 추가됩니다. 상세 로그는 작업 이름을 눌러 확인합니다.</div>
    ${shown.length ? table(shown, [
      ["title", "작업", j => `<a href="#/jobs/${encodeURIComponent(j.id)}">${esc(j.title)}</a>`],
      ["status", "상태", j => `<span class="tag ${j.status === "done" ? "ok" : j.status === "running" ? "" : "warn"}">${status(j)}</span>
        ${j.recovered ? `<div class="muted">완성된 결과 자동 복구</div>` : ""}`],
      ["progress", "진행", j => j.status === "running" && j.progress ? `${j.progress[0]} / ${j.progress[1]}` : ""],
      ["result", "결과", j => j.result?.dataset ? `<a href="#/datasets/${encodeURIComponent(j.result.dataset)}">등록된 데이터셋 열기</a>`
        : j.error ? `<span class="err">${esc(j.error)}</span>` : j.status === "interrupted" ? `<span class="muted">studio 가 다시 떴지만 생성은 따로 계속 돕니다. 30초마다 확인해 끝나면 자동 등록하고, 멈췄으면 실패로 바꿉니다.</span>` : ""],
      ["forget", "", j => removable(j) ? `<button type="button" class="link ds-forget" data-id="${esc(j.id)}">기록 지우기</button>` : ""],
    ]) : `<p class="muted">생성 작업이 없습니다.</p>`}</div>`;
}

function startDatasetDashboard(initial) {
  if (datasetBuildDashboard) datasetBuildDashboard.stop();
  const root = $("#ds-registry"), known = new Set(initial.datasets.map(d => d.id)), added = new Set();
  let stopped = false, timer = null, inflight = null, queued = false;
  const active = () => !stopped && root.isConnected && location.hash === "#/datasets";
  const refresh = () => {
    if (!active()) return Promise.resolve();
    if (inflight) { queued = true; return inflight; }
    clearTimeout(timer);
    $("#ds-refresh").disabled = true;
    inflight = (async () => {
      let poll = false;
      try {
        const [r, builds] = await Promise.all([api("/api/datasets"), api("/api/builds")]);
        if (!active()) return;
        const newRows = r.datasets.filter(d => !known.has(d.id));
        for (const d of r.datasets) { if (!known.has(d.id)) added.add(d.id); known.add(d.id); }
        $("#ds-list").innerHTML = datasetRegistryHTML(r, added);
        $("#dataset-build-jobs").innerHTML = datasetBuildsHTML(builds.jobs);
        const missing = r.datasets.filter(d => !d.exists).length;
        $("#ds-reg-status").innerHTML = `${r.datasets.length}개 등록` + (missing
          ? ` · <button type="button" class="link" id="ds-prune">폴더 없는 ${missing}개 등록 해제</button>` : "");
        bindDatasetCleanup();
        if (newRows.length) toast(`데이터셋 ${newRows.length}개가 자동 등록되었습니다`);
        poll = builds.jobs.some(j => ["running", "interrupted"].includes(j.status));
      } catch (e) {
        if (active()) { $("#ds-reg-status").textContent = `목록 갱신 실패: ${e.message} · 다시 확인 중`; poll = true; }
      } finally {
        inflight = null;
        if (active()) {
          $("#ds-refresh").disabled = false;
          if (queued || poll) { timer = setTimeout(refresh, queued ? 0 : 2000); queued = false; }
        }
      }
    })();
    return inflight;
  };
  datasetBuildDashboard = { active, refresh, stop: () => { stopped = true; clearTimeout(timer); } };
  $("#ds-refresh").onclick = refresh;
  refresh();
}

// 목록 정리: 데이터셋 등록 해제(폴더는 그대로)·작업 기록 지우기. 지운 뒤 목록을 다시 읽는다.
function bindDatasetCleanup() {
  const again = () => datasetBuildDashboard?.refresh();
  const run = async (fn, done) => { try { const r = await fn(); toast(done(r)); again(); } catch (e) { toast(e.message, true); } };
  for (const b of document.querySelectorAll(".ds-unreg")) b.onclick = () => {
    const warn = b.dataset.frozen ? "\n고정한 평가 세트입니다. 이 세트로 낸 점수와 비교가 끊깁니다." : "";
    const keep = b.dataset.exists ? "폴더(데이터)는 지우지 않고 목록에서만 뺍니다. 필요하면 폴더 등록으로 다시 넣을 수 있습니다." : "폴더는 이미 없습니다.";
    if (confirm(`${b.dataset.id} 를 등록 해제할까요?\n${keep}${warn}`))
      run(() => api(`/api/datasets/${encodeURIComponent(b.dataset.id)}`, undefined, "DELETE"), () => `등록 해제: ${b.dataset.id}`);
  };
  for (const b of document.querySelectorAll(".ds-forget")) b.onclick = () =>
    run(() => api(`/api/jobs/${encodeURIComponent(b.dataset.id)}`, undefined, "DELETE"), () => "작업 기록을 지웠습니다");
  const prune = $("#ds-prune");
  if (prune) prune.onclick = () => confirm("폴더가 없어진 데이터셋을 모두 목록에서 뺄까요?")
    && run(() => api("/api/datasets/prune-missing", {}), r => `${r.removed.length}개 등록 해제`);
  const clean = $("#ds-jobs-cleanup");
  if (clean) clean.onclick = () => confirm("끝난 생성 기록(실패·취소·멈춘 작업, 데이터셋이 없어진 작업)을 지울까요? 데이터셋 폴더는 그대로입니다.")
    && run(() => api("/api/builds/cleanup", {}), r => `기록 ${r.removed.length}개를 지웠습니다`);
}

function datasetBuildStarted(job) {
  toast("생성을 시작했습니다. 완료하면 아래 목록에 자동 등록됩니다");
  if (datasetBuildDashboard?.active()) datasetBuildDashboard.refresh();
  else location.hash = "#/datasets";
}
