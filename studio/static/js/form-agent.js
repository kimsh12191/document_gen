// 이미지로 서식 만들기: 사내 모델이 ReLab 으로 스킬 form-from-image 를 따라 서식 초안을 만든다.
// 서버: /api/form-agent (studio/api_form_agent.py) → 명령 python -m formagent go|continue (formagent/README.md)
"use strict";

addRoute(/^#\/form-agent$/, () => viewFormAgent(), "form-agent");
addRoute(/^#\/form-agent\/([^/]+)(?:\/(progress|result|files))?$/, (id, tab) => viewFormAgentOne(decodeURIComponent(id), tab || "progress"), "form-agent");

const FA_STATUS = { ready: "준비", installing: "ReLab 설치 중", running: "도는 중", waiting: "질문 대기", done: "끝남",
  stopped: "멈춤", failed: "실패", interrupted: "끊김" };
const FA_LIVE = new Set(["installing", "running"]);
const FA_EXIT = { 0: "완료", 1: "미완료 (ReLab 판정: 검사 미통과나 남은 일)", 2: "시작 못 함", 3: "모델이 질문함" };
const faTag = s => `<span class="tag ${s === "done" ? "ok" : FA_LIVE.has(s) || s === "ready" ? "" : "warn"}">${esc(FA_STATUS[s] || s)}</span>`;
const faBase = id => `#/form-agent/${encodeURIComponent(id)}`;

async function viewFormAgent() {
  main().innerHTML = `
    <h1>이미지로 서식 만들기</h1>
    <div class="sub">서식 그림을 올리면 사내 모델이 스킬 <span class="mono">.claude/skills/form-from-image/SKILL.md</span> 를 따라
      <b>뽑을 키·항목 설명(fields.md)</b> → <span class="mono">template.html.j2 · form.json</span> (칸끼리 관계가 있으면 <span class="mono">generate.py</span>) 를 만들고,
      원본과 렌더를 나란히 놓고 고칩니다. 실제로 도는 것은 명령줄과 같은 <span class="mono">python -m formagent</span> 이고, 결과는 <span class="mono">out/form_drafts/&lt;ID&gt;/</span> 에 남습니다.
      만든 초안은 사람이 보고 등록합니다 (스킬 7단계).</div>
    <div id="fa-env" class="bar fa-env"></div>
    <details class="panel fa-new" id="fa-new-box" open><summary><b>새로 만들기</b></summary>
      <div class="fa-form">
        <label class="fld">서식 그림 <span class="muted">(쪽 순서대로, 최대 3장 · png·jpg)</span>
          <input type="file" id="fa-files" multiple accept=".png,.jpg,.jpeg,.webp"></label>
        <div id="fa-thumbs" class="fa-thumbs"></div>
        <label class="fld">서식 ID <span class="muted">(영어 소문자·숫자·밑줄, 예: loan_application)</span>
          <input type="text" id="fa-id" class="mono" size="30" placeholder="loan_application"> <span id="fa-id-msg" class="muted"></span></label>
        <label class="fld">원본 종류 <select id="fa-kind"></select></label>
        <label class="fld">추가 요청 <span class="muted">(선택)</span><textarea id="fa-note" rows="2" placeholder="예: 현금 행은 입금 계좌를 비워 둔다"></textarea></label>
        <div class="bar"><button class="primary" id="fa-start" disabled>시작</button>
          <span class="muted" id="fa-start-msg">ReLab 이 없으면 시작할 때 자동으로 설치합니다.</span></div>
      </div>
    </details>
    <h2>만든 것</h2>
    <div id="fa-list"></div>`;
  const ov = await drawFaOverview();
  $("#fa-kind").innerHTML = Object.entries(ov.kinds).map(([k, n]) => `<option value="${k}">${esc(n.split(" (")[0])}</option>`).join("");
  let idOk = false;
  const ready = () => {
    const files = $("#fa-files").files;
    const busy = !!state.faBusy;
    $("#fa-start").disabled = !(idOk && files.length >= 1 && files.length <= ov.max_pages) || busy;
    $("#fa-start-msg").textContent = busy ? "다른 서식을 만드는 중입니다 (한 번에 한 건)."
      : files.length > ov.max_pages ? `그림은 ${ov.max_pages}장까지` : "ReLab 이 없으면 시작할 때 자동으로 설치합니다.";
  };
  $("#fa-files").onchange = () => {
    $("#fa-thumbs").innerHTML = Array.from($("#fa-files").files).map((f, i) =>
      `<figure><img src="${URL.createObjectURL(f)}" alt=""><figcaption>${i + 1}쪽 · ${esc(f.name)}</figcaption></figure>`).join("");
    ready();
  };
  let timer = null;
  $("#fa-id").oninput = () => {
    clearTimeout(timer);
    idOk = false; ready();
    const v = $("#fa-id").value.trim();
    if (!v) { $("#fa-id-msg").textContent = ""; return; }
    timer = setTimeout(async () => {
      const r = await api(`/api/form-agent/check-id?id=${encodeURIComponent(v)}`);
      idOk = r.ok;
      $("#fa-id-msg").innerHTML = r.ok ? `<span class="tag ok">쓸 수 있음</span>` : `<span class="tag warn">${esc(r.reason)}</span>`;
      ready();
    }, 300);
  };
  $("#fa-start").onclick = async () => {
    const fd = new FormData();
    Array.from($("#fa-files").files).forEach(f => fd.append("images", f));
    fd.append("id", $("#fa-id").value.trim());
    fd.append("kind", $("#fa-kind").value);
    fd.append("note", $("#fa-note").value);
    $("#fa-start").disabled = true;
    $("#fa-start-msg").textContent = "초안 폴더를 만들고 시작하는 중…";
    const r = await fetch("/api/form-agent", { method: "POST", body: fd });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) { toast(data.detail || `${r.status}`, true); ready(); return; }
    location.hash = faBase(data.id);
  };
}

async function drawFaOverview() {
  const ov = await api("/api/form-agent");
  state.faBusy = ov.busy;
  const rl = ov.relab, s = ov.settings;
  const env = $("#fa-env");
  if (env) env.innerHTML = `
    <span>ReLab ${rl.installed ? `<span class="tag ok">설치됨 ${esc(rl.version)}</span> <span class="mono muted">${esc(rl.path)}</span>`
      : `<span class="tag warn">없음</span> <span class="muted">시작하면 저장소의 묶음으로 <span class="mono">${esc(rl.install_to)}</span> 에 설치</span>`}</span>
    <span>모델 ${s.model ? `<span class="mono">${esc(s.provider || "")} · ${esc(s.model)}</span> <span class="mono muted">${esc(s.endpoint || "")}</span>`
      : `<span class="muted">ReLab 설정(~/.relab/config.json)을 따름 — studio 설정 <span class="mono">form_agent</span> 로 정할 수 있음</span>`}</span>
    ${ov.busy ? `<span class="tag">도는 작업: ${esc(ov.busy.title)}</span>` : ""}`;
  const box = $("#fa-list");
  if (box) box.innerHTML = ov.items.length ? `<div class="fa-cards">${ov.items.map(it => `
      <a class="card fa-card" href="${faBase(it.id)}">
        <div class="fa-thumb"><img src="${esc(it.thumb)}" alt="" loading="lazy"></div>
        <div class="cap"><b class="mono">${esc(it.id)}</b> ${faTag(it.status)}<br>
          <span>${esc(it.name || "")}</span><br>
          <span class="muted">${esc((ov.kinds[it.kind] || "").split(" (")[0])} · ${it.rounds}회차</span>
          ${it.passed === true ? `<span class="tag ok">검사 통과</span>` : it.passed === false ? `<span class="tag warn">문제 ${it.problems}</span>` : ""}
          ${it.warnings ? `<span class="tag warn">경고 ${it.warnings}</span>` : ""}
          ${it.outside ? `<span class="tag warn">초안 밖 변경 ${it.outside}</span>` : ""}
          ${it.registered ? `<span class="tag ok">등록됨</span>` : ""}
          <br><span class="muted">${esc(it.created || "")}</span></div></a>`).join("")}</div>`
    : `<p class="muted">아직 없습니다.</p>`;
  clearTimeout(state.faListTimer);
  if (ov.items.some(it => FA_LIVE.has(it.status)) || ov.busy)
    state.faListTimer = setTimeout(() => { if (location.hash === "#/form-agent") drawFaOverview(); }, 3000);
  return ov;
}

// --------------------------------------------------------------------- 하나

// 도는 중 새로 고침: 타이머는 하나. 상태·회차·검사가 바뀌면 지금 주소의 탭을 스크롤 그대로 다시 그리고,
// 아니면 도는 회차의 로그 글자만 바꾼다 (탭이 저절로 바뀌거나 펼친 것·스크롤이 풀리지 않게)
const faTab = () => (location.hash.match(/\/(progress|result|files)$/) || [null, "progress"])[1];
const faSig = d => { const r = d.rounds[d.rounds.length - 1] || {};
  return [d.status, d.rounds.length, r.ended, r.check ? JSON.stringify(r.check) : "", d.registered ? 1 : 0].join("|"); };

function faPoll(id) {
  clearTimeout(state.faTimer);
  state.faTimer = setTimeout(async () => {
    if (!location.hash.startsWith(faBase(id))) return;
    let d;
    try { d = await api(`/api/form-agent/${encodeURIComponent(id)}`); } catch { faPoll(id); return; }
    if (!location.hash.startsWith(faBase(id))) return;
    if (faSig(d) !== state.faSig) {
      const y = main().scrollTop, typed = $("#fa-msg") ? $("#fa-msg").value : "";
      const opened = $$(".fa-round").filter(r => $("details", r) && $("details", r).open).map(r => r.dataset.n);
      await viewFormAgentOne(id, faTab(), d);
      if (typed && $("#fa-msg")) $("#fa-msg").value = typed;
      for (const n of opened) { const det = $(`.fa-round[data-n="${n}"] details`); if (det) det.open = true; }
      main().scrollTop = y;
      return;
    }
    if (faTab() === "progress") await faRefreshLogs(d);
    if (FA_LIVE.has(d.status)) faPoll(id);
  }, 4000);
}

async function faRefreshLogs(d) {
  for (const pre of $$("pre.fa-log")) {
    const r = d.rounds.find(x => String(x.n) === pre.dataset.n);
    if (r && r.ended != null && pre.dataset.done) continue;          // 끝난 회차는 한 번 읽으면 됨
    const t = await fetch(`/api/form-agent/${encodeURIComponent(d.id)}/log/${pre.dataset.n}`).then(x => x.ok ? x.text() : "").catch(() => "");
    if (!t || t === pre.textContent) continue;
    const atEnd = pre.scrollTop + pre.clientHeight >= pre.scrollHeight - 20;
    pre.textContent = t;
    if (atEnd) pre.scrollTop = pre.scrollHeight;
    if (r && r.ended != null) pre.dataset.done = "1";
  }
}

async function viewFormAgentOne(id, tab, given) {
  clearTimeout(state.faTimer);
  const d = given || await api(`/api/form-agent/${encodeURIComponent(id)}`);
  state.faSig = faSig(d);
  const live = FA_LIVE.has(d.status);
  const tabs = [["progress", "진행"], ["result", "결과"], ["files", "파일"]];
  main().innerHTML = `
    <div class="muted"><a href="#/form-agent">이미지로 서식 만들기</a></div>
    <h1><span class="mono">${esc(d.id)}</span> ${esc(d.name || "")} ${faTag(d.status)}</h1>
    <div class="bar">
      <span class="muted">${esc((d.kind && { blank: "빈 서식", sample: "견본", real: "실서류" }[d.kind]) || "")} · ${d.rounds.length}회차 · ${esc(d.created || "")}${d.ended ? ` → ${esc(d.ended)}` : ""}</span>
      ${d.relab ? `<span class="muted mono">ReLab ${esc(d.relab_version || "")}</span>` : ""}
      ${d.registered ? `<span class="tag ok">등록됨 · ${d.registered.to === "private" ? "비공개" : "공개"}</span>
        <a href="#/forms/${encodeURIComponent(d.id)}">서식 화면 열기 (미리보기·검수)</a>` : ""}
      ${live ? `<button id="fa-stop">멈추기</button>` : ""}
    </div>
    ${d.note ? `<div class="sub">추가 요청: ${esc(d.note)}</div>` : ""}
    ${d.error && d.status !== "done" ? `<p class="err">${esc(d.error)}</p>` : ""}
    ${d.status === "waiting" ? `<div class="panel fa-q"><b>모델이 묻습니다</b><pre class="ans mono">${esc(d.question || "")}</pre>
      <div class="muted">아래 <b>이어서 지시</b>에 답을 적어 보내면 다음 회차가 이어집니다.</div></div>` : ""}
    ${d.outside_changes.length ? `<div class="panel fa-warn"><b>초안 폴더 밖에서 바뀐 파일 ${d.outside_changes.length}개</b> — 모델이 손댄 것인지 확인하세요
      <pre class="mono">${esc(d.outside_changes.join("\n"))}</pre></div>` : ""}
    <div class="tabs">${tabs.map(([t, n]) => `<a href="${faBase(id)}/${t}" class="${t === tab ? "on" : ""}">${n}</a>`).join("")}</div>
    <div id="fa-tab"></div>
    <div class="panel fa-cont">
      <b>이어서 지시</b> <span class="muted">— 고칠 점이나 모델의 질문에 대한 답. 다음 회차 요청에 넣어 이어서 고칩니다.</span>
      <textarea id="fa-msg" rows="2" placeholder="예: 계좌번호 칸을 세 칸(□전체 · 계좌1 · 계좌2)으로 나눠 줘"></textarea>
      <div class="bar"><button class="primary" id="fa-cont" ${live ? "disabled" : ""}>이어서</button>
        <span class="muted">${live ? "도는 중에는 보낼 수 없습니다" : ""}</span></div>
    </div>`;
  if ($("#fa-stop")) $("#fa-stop").onclick = async () => {
    if (!confirm("멈출까요? 지금 회차의 ReLab 을 끝내고 그때까지 만든 초안은 남겨 둡니다.")) return;
    await api(`/api/form-agent/${encodeURIComponent(id)}/stop`, {});
    toast("멈춤 표시를 남겼습니다");
    setTimeout(() => { if (location.hash.startsWith(faBase(id))) viewFormAgentOne(id, faTab()); }, 1500);
  };
  $("#fa-cont").onclick = async () => {
    const message = $("#fa-msg").value.trim();
    if (!message) { toast("지시를 적어 주세요", true); return; }
    try { await api(`/api/form-agent/${encodeURIComponent(id)}/continue`, { message }); }
    catch (e) { toast(e.message, true); return; }
    location.hash = `${faBase(id)}/progress`;
    viewFormAgentOne(id, "progress");
  };
  if (tab === "progress") await faProgress(d);
  else if (tab === "result") faResult(d);
  else faFiles(d);
  if (live) faPoll(id);
}

async function faProgress(d) {
  const box = $("#fa-tab");
  const jobLog = await fetch(`/api/form-agent/${encodeURIComponent(d.id)}/job-log`).then(r => r.text()).catch(() => "");
  const rounds = d.rounds.slice().reverse();
  box.innerHTML = `
    <div class="fa-steps">${faSteps(d)}</div>
    ${rounds.map(r => `
      <div class="panel fa-round" data-n="${r.n}">
        <div class="bar"><b>${r.n}회차</b>${r.kind ? ` <span class="muted">${esc(FA_KIND[r.kind] || r.kind)}</span>` : ""}
          ${r.ended == null ? `<span class="tag">도는 중</span>`
            : `<span class="tag ${r.exit === 0 ? "ok" : "warn"}">ReLab: ${esc(r.exit === null ? "멈춤·시간 넘음" : FA_EXIT[r.exit] || `종료 코드 ${r.exit}`)}</span>`}
          ${r.check ? (r.check.passed ? `<span class="tag ok">검사 통과</span>` : `<span class="tag warn">검사 문제 ${r.check.problems.length}</span>`) : ""}
          ${r.check && r.check.warnings.length ? `<span class="tag warn">경고 ${r.check.warnings.length}</span>` : ""}
          <span class="muted">${esc(r.started || "")}${r.seconds !== undefined && r.seconds !== null ? ` · ${r.seconds}초` : ""}</span></div>
        <details><summary class="muted">이 회차 요청 문장 (모델에게 보낸 것)</summary><pre class="ans mono">${esc(r.request || "")}</pre></details>
        <div class="muted">모델이 한 일 (ReLab 출력 · <b>●</b> 모델의 말, <b>⎿</b> 한 일)</div>
        <pre class="ans mono log fa-log" data-n="${r.n}">불러오는 중…</pre>
        ${r.check && (r.check.problems.length || r.check.warnings.length) ? `<div class="fa-issues">
          ${r.check.problems.map(p => `<div class="err">문제: ${esc(p)}</div>`).join("")}
          ${r.check.warnings.map(w => `<div class="fa-w">경고: ${esc(w)}</div>`).join("")}</div>` : ""}
      </div>`).join("")}
    <details ${d.rounds.length ? "" : "open"}><summary class="muted">진행기 출력 (ReLab 설치·회차 시작/끝)</summary><pre class="ans mono log">${esc(jobLog)}</pre></details>`;
  for (const pre of $$("pre.fa-log", box)) {
    const t = await fetch(`/api/form-agent/${encodeURIComponent(d.id)}/log/${pre.dataset.n}`).then(r => r.ok ? r.text() : "").catch(() => "");
    pre.textContent = t || "(아직 출력 없음)";
    pre.scrollTop = pre.scrollHeight;
    const r = d.rounds.find(x => String(x.n) === pre.dataset.n);
    if (r && r.ended != null) pre.dataset.done = "1";
  }
}

const FA_KIND = { read: "글자 옮기기 (source_text.md)", build: "만들기 (칸 표 → 템플릿 → 검사)", fix: "비교 그림 보고 고치기" };

function faSteps(d) {
  // 화면 위 줄: ReLab 준비 → 글자 옮기기 → 만들기 → 비교·고치기 회차 → 끝 (지금 자리 강조)
  const s = d.status, kinds = d.rounds.map(r => r.kind || "build"), last = kinds[kinds.length - 1];
  const at = k => kinds.includes(k) ? (last === k && FA_LIVE.has(s) ? "now" : "done") : "";
  const steps = [["ReLab 준비", s === "installing" ? "now" : (kinds.length || d.relab) ? "done" : ""],
    ["글자 옮기기", at("read")], ["칸 표 → 템플릿 → 검사", at("build")], ["비교 그림 보고 고치기", at("fix")],
    [s === "waiting" ? "질문 대기" : s === "stopped" ? "멈춤" : s === "failed" ? "실패" : "끝 · 사람이 확인", ["done", "waiting", "stopped", "failed", "interrupted"].includes(s) ? "now" : ""]];
  return steps.map(([t, c], i) => `<span class="fa-step ${c}">${i + 1}. ${esc(t)}</span>`).join(`<span class="muted">→</span>`);
}

function faResult(d) {
  const box = $("#fa-tab");
  box.innerHTML = `<div id="fa-reg-box"></div><div id="fa-res"></div>`;
  faRegister(d);
  faResultBody(d, $("#fa-res"));
}

// 등록: 초안 → docgen/forms/<ID> (공개) 또는 비공개 서식 폴더. 서버가 검사 통과·ID 비어 있음을 다시 확인한다 (스킬 register.py)
function faRegister(d) {
  const box = $("#fa-reg-box");
  if (d.registered) {
    const r = d.registered;
    box.innerHTML = `<div class="panel fa-reg"><b>등록됨</b> <span class="tag ok">${r.to === "private" ? "비공개" : "공개"}</span>
      <span class="mono">${esc(r.path)}</span> <span class="muted">${esc(r.at)}</span>
      ${r.card_ok ? "" : `<span class="tag warn">카드 만들기 실패</span>`} ${r.check_ok ? `<span class="tag ok">formdir check 통과</span>` : `<span class="tag warn">formdir check 문제</span>`}
      <div class="bar"><a href="#/forms/${encodeURIComponent(d.id)}">서식 화면 열기</a>
        <span class="muted">→ 생성 사례 › 미리보기/검수 에서 원본과 비교해 <b>검수 완료</b>. 등록은 검수가 아닙니다.</span></div></div>`;
    return;
  }
  if (FA_LIVE.has(d.status) || d.status === "ready") { box.innerHTML = ""; return; }
  const real = d.kind === "real", hasGen = "generate.py" in d.files;
  const passed = d.final ? d.final.passed : null;
  box.innerHTML = `<div class="panel fa-reg"><b>등록</b> <span class="muted">— 초안을 서식 폴더로 옮겨 서식 목록에 올립니다. 그다음 서식 › 미리보기/검수.</span>
    ${passed === false ? `<div class="err">마지막 검사를 통과하지 못해 등록할 수 없습니다. 이어서 지시로 고치세요.</div>` : ""}
    <div class="fa-reg-to">
      <label><input type="radio" name="fa-to" value="public" ${real ? "disabled" : "checked"}> 공개 <span class="mono">docgen/forms/${esc(d.id)}/</span>
        ${real ? `<span class="muted">(실서류는 공개 폴더에 넣지 않음)</span>` : `<span class="muted">(빈 서식·공개 견본)</span>`}</label>
      <label><input type="radio" name="fa-to" value="private" ${d.private_dir ? (real ? "checked" : "") : "disabled"}> 비공개
        <span class="mono">${esc(d.private_dir || "(studio 설정 private_forms_dir 이 없음)")}/${esc(d.id)}/</span> <span class="muted">(실서류에서 만든 것)</span></label>
    </div>
    <div class="fa-reg-check">
      <label><input type="checkbox" class="fa-ok"> <b>파일</b> 탭의 fields.md 키·항목 설명을 확인했다 (데이터셋을 만든 뒤에는 키를 못 바꿈)</label>
      <label><input type="checkbox" class="fa-ok"> 원본·렌더 나란히 그림에서 같은 서류로 보인다</label>
      ${hasGen ? `<label><input type="checkbox" class="fa-ok"> generate.py 를 읽었다 (미리보기·생성 때 실행되는 코드)</label>` : ""}
    </div>
    <div class="bar"><button class="primary" id="fa-reg" disabled>등록</button><span class="muted" id="fa-reg-msg"></span></div>
    <div id="fa-reg-out"></div></div>`;
  const ready = () => {
    const to = $("input[name=fa-to]:checked", box);
    $("#fa-reg").disabled = !to || passed === false || $$(".fa-ok", box).some(c => !c.checked);
  };
  $$("input", box).forEach(i => i.onchange = ready);
  ready();
  $("#fa-reg").onclick = async () => {
    const to = $("input[name=fa-to]:checked", box).value;
    if (!confirm(`${to === "private" ? "비공개" : "공개"} 서식 폴더에 ${d.id} 를 등록할까요? (이미 있으면 덮어쓰지 않고 멈춥니다)`)) return;
    $("#fa-reg").disabled = true;
    $("#fa-reg-msg").textContent = "검사하고 옮기는 중… (수십 초)";
    try {
      const r = await api(`/api/form-agent/${encodeURIComponent(d.id)}/register`, { to });
      toast(`등록했습니다: ${r.path}`);
      $("#fa-reg-out").innerHTML = `<pre class="ans mono">${esc(r.formdir_check.out)}</pre>`;
      setTimeout(() => viewFormAgentOne(d.id, "result"), 800);
    } catch (e) {
      $("#fa-reg-msg").textContent = "";
      $("#fa-reg-out").innerHTML = `<p class="err">${esc(e.message)}</p>`;
      ready();
    }
  };
}

function faResultBody(d, box) {
  const withImg = d.rounds.filter(r => r.images && r.images.side.length);
  const fin = d.final;
  const pick = withImg.length ? withImg[withImg.length - 1].n : null;
  box.innerHTML = `
    ${fin ? `<div class="panel"><b>마지막 검사</b> (진행기가 직접 다시 돌린 것) ${fin.passed ? `<span class="tag ok">통과</span>` : `<span class="tag warn">통과 못 함</span>`}
      ${Object.entries(fin.renders || {}).map(([k, v]) => `<span class="tag">${esc(k)}: ${v.pages ?? "?"}쪽 · 값 ${v.fields ?? "?"} · 빈 ${v.empty ?? "?"}${v.overflow ? " · 넘침" : ""}</span>`).join("")}
      ${(fin.problems || []).map(p => `<div class="err">문제: ${esc(p)}</div>`).join("")}
      ${(fin.warnings || []).map(w => `<div class="fa-w">경고: ${esc(w)}</div>`).join("")}</div>` : `<p class="muted">아직 마지막 검사가 없습니다 (끝나면 생깁니다).</p>`}
    <div class="bar">원본 · 렌더 나란히 <select id="fa-round">${withImg.map(r => `<option value="${r.n}" ${r.n === pick ? "selected" : ""}>${r.n}회차 뒤</option>`).join("")}
      ${d.final_images && d.final_images.side.length ? `<option value="final" selected>마지막 검사</option>` : ""}</select>
      <span class="muted">왼쪽 원본 · 오른쪽 렌더(--rows min). 같은 서류로 보이는지, 빠진 항목·넘치는 값이 없는지</span></div>
    <div id="fa-imgs"></div>
    <div class="grid fa-md">
      <div><h2>보고 (report.md)</h2><pre class="ans">${esc(d.files["report.md"] || "아직 없음")}</pre></div>
      <div><h2>비교 기록 (review.md)</h2><pre class="ans">${esc(d.files["review.md"] || "아직 없음")}</pre></div>
    </div>
    <div class="muted">원본: ${d.sources.map((u, i) => `<a href="${esc(u)}" target="_blank">${i + 1}쪽</a>`).join(" · ")}</div>`;
  const draw = () => {
    const v = $("#fa-round").value;
    const im = v === "final" ? d.final_images : (d.rounds.find(r => String(r.n) === v) || {}).images;
    $("#fa-imgs").innerHTML = im ? `${im.side.map(u => `<a href="${esc(u)}" target="_blank"><img class="fa-side" src="${esc(u)}" alt=""></a>`).join("")}
      ${im.renders ? `<div class="muted">렌더 모음 (min · max · seed 1 · seed 2 첫 쪽) — 서류마다 값·행 수가 바뀌는지</div>
        <a href="${esc(im.renders)}" target="_blank"><img class="fa-renders" src="${esc(im.renders)}" alt=""></a>` : ""}` : `<p class="muted">그림이 없습니다.</p>`;
  };
  if ($("#fa-round").options.length) draw(); else $("#fa-imgs").innerHTML = `<p class="muted">아직 그림이 없습니다 (만들기 회차가 끝나면 생깁니다).</p>`;
  $("#fa-round").onchange = draw;
}

function faFiles(d) {
  const box = $("#fa-tab");
  const names = Object.keys(d.files);
  const cur = store.get("fa.file", "fields.md");
  const sel = names.includes(cur) ? cur : names[0];
  box.innerHTML = names.length ? `
    <div class="subtabs">${names.map(n => `<a href="javascript:void 0" data-f="${esc(n)}" class="${n === sel ? "on" : ""}">${esc(n)}</a>`).join("")}</div>
    <div id="fa-file"></div>` : `<p class="muted">아직 모델이 쓴 파일이 없습니다.</p>`;
  const show = n => {
    store.set("fa.file", n);
    $$(".subtabs a", box).forEach(a => a.classList.toggle("on", a.dataset.f === n));
    const text = d.files[n] || "";
    const head = n === "generate.py" ? `<div class="panel fa-warn"><b>실행되는 코드입니다.</b> 미리보기·생성 때 돌아갑니다. 등록 전에 읽어 주세요 (docgen.formkit 과 표준 라이브러리만, 칸 목록의 키만 고쳐야 함).</div>`
      : n === "source_text.md" ? `<div class="muted">1회차에 모델이 그림에서 옮겨 적은 인쇄 글자 — 원본과 대 보면 모델이 그림을 제대로 읽었는지 바로 보입니다. 템플릿 글자는 이것을 기준으로 검사합니다.</div>`
      : n === "fields.md" ? `<div class="muted">뽑을 키와 항목 설명 — 사람이 가장 먼저 검토할 곳입니다 (데이터셋을 만든 뒤에는 키를 바꾸지 않음). 확신 "낮음"·"판단이 안 선 것"을 보세요.</div>` : "";
    $("#fa-file").innerHTML = head + (n.endsWith(".md") ? faMarkdown(text) : `<pre class="ans mono">${esc(text)}</pre>`);
  };
  if (names.length) { show(sel); $$(".subtabs a", box).forEach(a => a.onclick = () => show(a.dataset.f)); }
}

// 아주 작은 마크다운: 제목·표·목록·코드 블록 (fields.md · review.md · report.md 를 표로 보이게)
function faMarkdown(text) {
  const out = []; const lines = text.split("\n"); let i = 0;
  const cells = l => l.trim().replace(/^\||\|$/g, "").split("|").map(c => c.trim());
  const inline = s => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>");
  while (i < lines.length) {
    const l = lines[i];
    if (l.startsWith("```")) { const buf = []; i++; while (i < lines.length && !lines[i].startsWith("```")) buf.push(lines[i++]); i++;
      out.push(`<pre class="ans mono">${esc(buf.join("\n"))}</pre>`); continue; }
    if (/^#{1,4} /.test(l)) { const h = l.match(/^#+/)[0].length; out.push(`<h${h + 1}>${inline(l.replace(/^#+ /, ""))}</h${h + 1}>`); i++; continue; }
    if (l.trim().startsWith("|") && i + 1 < lines.length && /^\s*\|?\s*-{3}/.test(lines[i + 1])) {
      const head = cells(l); i += 2; const rows = [];
      while (i < lines.length && lines[i].trim().startsWith("|")) rows.push(cells(lines[i++]));
      out.push(`<table class="fa-md-table"><thead><tr>${head.map(c => `<th>${inline(c)}</th>`).join("")}</tr></thead><tbody>${rows.map(r =>
        `<tr class="${r.some(c => /낮음|중간/.test(c)) ? "fa-low" : ""}">${r.map(c => `<td>${inline(c)}</td>`).join("")}</tr>`).join("")}</tbody></table>`);
      continue;
    }
    if (/^\s*[-*] /.test(l)) { const items = []; while (i < lines.length && /^\s*[-*] /.test(lines[i])) items.push(lines[i++].replace(/^\s*[-*] /, ""));
      out.push(`<ul>${items.map(t => `<li>${inline(t)}</li>`).join("")}</ul>`); continue; }
    if (l.trim()) out.push(`<p>${inline(l)}</p>`);
    i++;
  }
  return `<div class="fa-mdview">${out.join("")}</div>`;
}
