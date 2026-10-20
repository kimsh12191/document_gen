// ⑥ 안에서 생성 진행과 자동 등록을 확인한다. 목록만 갱신해 입력 중인 이름·설정은 유지한다.
"use strict";

let datasetBuildDashboard = null;

function datasetRegistryHTML(r, added = new Set()) {
  if (!r.datasets.length) return `<p class="muted">등록된 데이터셋이 없습니다. 위에서 새로 만들면 완료 후 여기에 자동으로 등록됩니다.</p>`;
  return table(r.datasets, [
    ["name", "이름", d => `<a href="#/datasets/${encodeURIComponent(d.id)}">${esc(d.name)}</a> <span class="mono muted">${esc(d.id)}</span>
      ${added.has(d.id) ? `<span class="tag ok">새로 등록됨</span>` : ""}`],
    ["track", "벤치마크", d => dsTag(d)], ["source", "출처", d => esc(r.sources[d.source] || d.source)],
    ["gt", "정답", d => esc((r.gts[d.gt] || d.gt).split(" (")[0])],
    ["real", "", d => d.real_data ? `<span class="tag warn">실서류</span>` : ""],
    ["version", "버전", d => esc(d.version || "-")],
    ["counts", "문항", d => esc(Object.entries(d.counts || {}).filter(([k]) => !/train|val|pages|documents/.test(k) || k === "benchmark_tasks")
      .reduce((a, [, v]) => a + (+v || 0), 0) || "-")],
    ["runs", "모델 답", d => d.n_runs || ""], ["scores", "점수", d => d.n_scores || ""],
    ["frozen", "고정", d => d.frozen ? `<span class="tag ok">고정</span>` : ""],
    ["exists", "", d => d.exists ? "" : `<span class="tag warn">폴더 없음</span>`],
  ], d => added.has(d.id) ? `class="ds-new"` : "");
}

function datasetBuildsHTML(jobs) {
  const pending = j => ["running", "interrupted"].includes(j.status);
  const shown = [...jobs.filter(pending), ...jobs.filter(j => !pending(j)).slice(0, 5)];
  const status = j => j.stage === "registering" ? "등록 중" : j.stage === "registration_failed" ? "등록 실패"
    : ({ running: "생성 중", done: j.result?.dataset ? "자동 등록 완료" : "완료 · 등록 확인 필요", failed: "생성 실패", cancelled: "취소", interrupted: "연결 끊김 · 완료 결과 확인 중" }[j.status] || j.status);
  return `<div class="panel ds-build-panel"><h2>데이터셋 생성 현황</h2>
    <div class="sub">완료하면 아래 등록 목록에 자동으로 추가됩니다. 상세 로그는 작업 이름을 눌러 확인합니다.</div>
    ${shown.length ? table(shown, [
      ["title", "작업", j => `<a href="#/jobs/${encodeURIComponent(j.id)}">${esc(j.title)}</a>`],
      ["status", "상태", j => `<span class="tag ${j.status === "done" ? "ok" : j.status === "running" ? "" : "warn"}">${status(j)}</span>
        ${j.recovered ? `<div class="muted">완성된 결과 자동 복구</div>` : ""}`],
      ["progress", "진행", j => j.status === "running" && j.progress ? `${j.progress[0]} / ${j.progress[1]}` : ""],
      ["result", "결과", j => j.result?.dataset ? `<a href="#/datasets/${encodeURIComponent(j.result.dataset)}">등록된 데이터셋 열기</a>`
        : j.error ? `<span class="err">${esc(j.error)}</span>` : j.status === "interrupted" ? `<span class="muted">완료 파일이 확인되면 자동 등록합니다. 미완성 작업은 작업 화면에서 확인하세요.</span>` : ""],
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
        $("#ds-reg-status").textContent = `${r.datasets.length}개 등록`;
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

function datasetBuildStarted(job) {
  toast("생성을 시작했습니다. 완료하면 아래 목록에 자동 등록됩니다");
  if (datasetBuildDashboard?.active()) datasetBuildDashboard.refresh();
  else location.hash = "#/datasets";
}
