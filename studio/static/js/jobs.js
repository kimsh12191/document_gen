// 작업: 데이터셋 빌드처럼 오래 걸리는 일의 목록·진행·로그. 서버: /api/jobs (studio/jobs.py)
"use strict";

addRoute(/^#\/jobs$/, () => view_jobs(), "jobs");
const JOB_STATUS = { running: "도는 중", done: "끝남", failed: "실패", cancelled: "취소", interrupted: "끊김" };

async function view_jobs() {
  main().innerHTML = `
    <h1>작업</h1>
    <div class="sub">데이터셋 빌드처럼 오래 걸리는 일입니다. 명령줄과 같은 명령을 그대로 돌립니다 (명령은 작업을 열면 보입니다).
</div>
    <div id="jb-list"></div>`;
  drawJobList();
}

async function drawJobList() {   // 도는 작업이 있으면 목록만 3초마다 다시
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
