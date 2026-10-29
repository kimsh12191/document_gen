// 모델 써 보기 화면. ① GPU·모델: GPU 상태 → 고르기 → 명령 확인·고치기 → 띄우기 / 떠 있는 모델·로그·내리기
// ② 써 보기: 이미지 폴더 → 그림 고르기 → 질문 고르기·고치기 (그림에 네모 끌기) → 묻기 → 답 (상자를 그림 위에)
const $ = (s) => document.querySelector(s);
const PALETTE = ["#2563eb", "#ea580c", "#16a34a", "#9333ea", "#db2777", "#0891b2"];
const MARK = { red: "#e11919", blue: "#194beb", green: "#0fa537" };
const S = {
  gpus: [], models: [], gpuSel: new Set(), cmdEdited: false, factor: 32, nextPort: 8100,
  tasks: [], byTask: {}, items: [], cur: null, picked: [], size: null,
  shapes: { box: null, anchor: null, markers: {} }, promptEdited: false, basePrompt: "",
  turns: [], last: null, askSel: new Set(), logId: null,
};

async function api(path, body) {
  const r = await fetch(path, body === undefined ? {} : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  const j = await r.json().catch(() => ({ error: `HTTP ${r.status}` }));
  if (!r.ok) throw new Error(j.error || `HTTP ${r.status}`);
  return j;
}
function toast(msg, ok) { const t = $("#toast"); t.textContent = msg || ""; t.className = ok ? "ok" : ""; if (msg) setTimeout(() => { if (t.textContent === msg) t.textContent = ""; }, 8000); }
function esc(s) { return String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }
function debounce(fn, ms) { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; }
function colorOf(id) { const i = S.models.findIndex((m) => m.id === id); return PALETTE[(i < 0 ? 0 : i) % PALETTE.length]; }
function mmss(sec) { sec = Math.max(0, Math.round(sec)); return `${Math.floor(sec / 60)}:${String(sec % 60).padStart(2, "0")}`; }

// ---------------------------------------------------------------- 탭
document.querySelectorAll(".tab").forEach((b) => b.onclick = () => {
  document.querySelectorAll(".tab").forEach((x) => x.classList.toggle("on", x === b));
  $("#tab-models").classList.toggle("hidden", b.dataset.tab !== "models");
  $("#tab-try").classList.toggle("hidden", b.dataset.tab !== "try");
  if (b.dataset.tab === "try") renderAskModels();
});

// ---------------------------------------------------------------- ① GPU
async function loadGpus() {
  try {
    const j = await api("/api/gpus");
    S.gpus = j.gpus; $("#gpu-error").textContent = j.error || "";
  } catch (e) { $("#gpu-error").textContent = e.message; }
  renderGpus();
}
function ownersOf(index) {
  return S.models.filter((m) => m.kind === "started" && !["stopped", "exited"].includes(m.state) && (m.gpus || []).includes(index));
}
function renderGpus() {
  const tb = $("#gpus tbody");
  tb.innerHTML = S.gpus.map((g) => {
    const own = ownersOf(g.index);
    const pct = g.total_mib ? Math.round(100 * g.used_mib / g.total_mib) : 0;
    const state = own.length ? `<span class="chip" style="background:${colorOf(own[0].id)}"></span>이 화면의 모델 ${esc(own.map((m) => m.name).join(", "))}`
      : g.free ? `<span class="ok">비어 있음</span>`
      : `<span class="warn">사용 중</span> ${g.procs.length ? "pid " + g.procs.map((p) => p.pid).join(", ") : "(다른 컨테이너일 수 있음)"}`;
    return `<tr class="${g.free ? "" : "busy"}"><td><input type="checkbox" data-gpu="${g.index}" ${S.gpuSel.has(g.index) ? "checked" : ""}></td>
      <td>${g.index}</td><td>${esc(g.name)}</td>
      <td><span class="memo"><i style="width:${pct}%"></i></span>${(g.used_mib / 1024).toFixed(1)} / ${(g.total_mib / 1024).toFixed(0)} GB</td>
      <td>${g.util ?? "-"}%</td><td>${state}</td></tr>`;
  }).join("") || `<tr><td colspan="6" class="muted">GPU 를 못 읽었습니다</td></tr>`;
  tb.querySelectorAll("input[data-gpu]").forEach((c) => c.onchange = () => {
    const i = Number(c.dataset.gpu);
    c.checked ? S.gpuSel.add(i) : S.gpuSel.delete(i);
    $("#m-gpus").textContent = S.gpuSel.size ? [...S.gpuSel].sort().join(", ") : "위 표에서 고르세요";
    remake();
  });
}
$("#gpu-refresh").onclick = loadGpus;

// ---------------------------------------------------------------- ① 명령 만들기·띄우기
const remake = debounce(async (force) => {
  if (S.cmdEdited && !force) { $("#m-remake").classList.remove("hidden"); return; }
  const path = $("#m-path").value.trim();
  const warn = $("#m-warn");
  if (!path || !S.gpuSel.size) { warn.innerHTML = `<li>${!path ? "모델 경로를 적으세요" : "GPU 를 고르세요"}</li>`; return; }
  try {
    const j = await api("/api/models/command", { path, gpus: [...S.gpuSel].sort(), port: Number($("#m-port").value) || undefined,
      model_type: $("#m-type").value.trim(), engine: $("#m-engine").value });
    $("#m-cmd").value = j.command; S.factor = j.factor; S.cmdEdited = false;
    $("#m-remake").classList.add("hidden");
    const busy = [...S.gpuSel].filter((i) => { const g = S.gpus.find((x) => x.index === i); return g && !g.free; });
    const w = [...j.warnings, ...(busy.length ? [`GPU ${busy.join(", ")} 은(는) 사용 중입니다. 메모리가 모자라면 뜨다가 멈춥니다 (--vllm_gpu_memory_utilization 을 낮추거나 다른 GPU)`] : [])];
    const info = j.info.kind === "adapter" ? `LoRA 체크포인트 · 출발 모델 ${j.info.base || "?"}` : j.info.kind === "model" ? "모델 폴더" : "";
    warn.innerHTML = (info ? `<li class="muted">${esc(info)}</li>` : "") + w.map((x) => `<li>${esc(x)}</li>`).join("");
  } catch (e) { warn.innerHTML = `<li>${esc(e.message)}</li>`; }
}, 300);
["#m-path", "#m-type", "#m-port"].forEach((s) => $(s).addEventListener("input", () => remake()));
$("#m-engine").onchange = () => remake();
$("#m-cmd").addEventListener("input", () => { S.cmdEdited = true; });
$("#m-remake").onclick = () => { if (confirm("고친 명령을 버리고 입력대로 다시 만들까요?")) remake(true); };
$("#m-start").onclick = async () => {
  const command = $("#m-cmd").value.trim();
  if (!command) return toast("실행할 명령이 비었습니다");
  const busy = [...S.gpuSel].filter((i) => { const g = S.gpus.find((x) => x.index === i); return g && !g.free; });
  if (busy.length && !confirm(`GPU ${busy.join(", ")} 은(는) 사용 중입니다. 그래도 띄울까요?`)) return;
  try {
    const m = await api("/api/models/start", { name: $("#m-name").value.trim(), path: $("#m-path").value.trim(), command,
      gpus: [...S.gpuSel].sort(), factor: S.factor });
    toast(`띄우는 중: ${m.name} (포트 ${m.port})`, true);
    S.cmdEdited = false; $("#m-cmd").value = ""; $("#m-name").value = ""; $("#m-remake").classList.add("hidden");
    S.gpuSel.clear(); $("#m-gpus").textContent = "위 표에서 고르세요"; $("#m-warn").innerHTML = "";
    await loadModels(); $("#m-port").value = S.nextPort; S.logId = m.id; showLog();
  } catch (e) { toast(e.message); }
};
$("#a-attach").onclick = async () => {
  try {
    await api("/api/models/attach", { name: $("#a-name").value.trim(), endpoint: $("#a-endpoint").value.trim() });
    $("#a-name").value = ""; $("#a-endpoint").value = ""; loadModels();
  } catch (e) { toast(e.message); }
};

// ---------------------------------------------------------------- ① 떠 있는 모델
const STATE = { starting: "준비 중", ready: "준비됨", exited: "끝남 — 로그를 보세요", stopped: "내림", unreachable: "닿지 않음" };
async function loadModels() {
  try {
    const j = await api("/api/models");
    S.models = j.models; S.nextPort = j.next_port;
    if (!$("#m-port").value) $("#m-port").value = j.next_port;
    $("#m-recent").innerHTML = j.recent.map((p) => `<option value="${esc(p)}">`).join("");
  } catch (e) { toast(e.message); }
  renderModels(); renderGpus(); renderAskModels();
}
function renderModels() {
  const now = Date.now() / 1000;
  $("#models tbody").innerHTML = S.models.map((m) => {
    const st = m.state === "starting" && m.kind === "started" ? `준비 중 ${mmss(now - m.started)}` : STATE[m.state] || m.state;
    const cls = m.state === "ready" ? "ok" : ["exited", "unreachable"].includes(m.state) ? "bad" : "muted";
    const off = ["stopped", "exited"].includes(m.state);
    return `<tr><td><span class="chip" style="background:${colorOf(m.id)}"></span></td><td>${esc(m.name)}</td>
      <td class="small">${esc(m.path || m.endpoint)}</td><td>${esc((m.gpus || []).join(", "))}</td><td>${m.port ?? ""}</td>
      <td class="${cls}">${esc(st)}</td>
      <td>${m.kind === "started" ? `<button class="small" data-log="${m.id}">로그</button>` : ""}
        ${off || m.kind === "attached" ? `<button class="small" data-rm="${m.id}">${m.kind === "attached" ? "목록에서 빼기" : "지우기"}</button>`
               : `<button class="small" data-stop="${m.id}">내리기</button>`}</td></tr>`;
  }).join("") || `<tr><td colspan="7" class="muted">아직 없습니다</td></tr>`;
  document.querySelectorAll("[data-log]").forEach((b) => b.onclick = () => { S.logId = b.dataset.log; showLog(); });
  document.querySelectorAll("[data-stop]").forEach((b) => b.onclick = async () => {
    const m = S.models.find((x) => x.id === b.dataset.stop);
    if (!confirm(`${m.name} 을(를) 내릴까요? (GPU ${(m.gpus || []).join(", ")} 이 비게 됩니다)`)) return;
    try { await api(`/api/models/${m.id}/stop`, {}); loadModels(); } catch (e) { toast(e.message); }
  });
  document.querySelectorAll("[data-rm]").forEach((b) => b.onclick = async () => {
    const m = S.models.find((x) => x.id === b.dataset.rm);
    try { await api(`/api/models/${m.id}/${m.kind === "attached" ? "stop" : "remove"}`, {}); S.askSel.delete(m.id); loadModels(); } catch (e) { toast(e.message); }
  });
}
async function showLog() {
  const m = S.models.find((x) => x.id === S.logId);
  if (!m) { $("#logbox").classList.add("hidden"); return; }
  $("#logbox").classList.remove("hidden"); $("#log-name").textContent = m.name;
  try {
    const j = await api(`/api/models/${m.id}/log`);
    const pre = $("#log"); const atEnd = pre.scrollTop + pre.clientHeight >= pre.scrollHeight - 20;
    pre.textContent = j.log; if (atEnd) pre.scrollTop = pre.scrollHeight;
  } catch (e) { $("#log").textContent = e.message; }
}
$("#log-close").onclick = () => { S.logId = null; $("#logbox").classList.add("hidden"); };
setInterval(() => {
  if (!$("#tab-models").classList.contains("hidden")) { loadGpus(); if (S.logId) showLog(); }
  loadModels();
}, 5000);

// ---------------------------------------------------------------- ② 묻는 모델
function renderAskModels() {
  const ready = S.models.filter((m) => m.state === "ready");
  for (const id of [...S.askSel]) if (!ready.some((m) => m.id === id)) S.askSel.delete(id);
  if (!S.askSel.size && ready.length) S.askSel.add(ready[0].id);
  $("#ask-models").innerHTML = `<b>묻는 모델</b> ` + (ready.map((m) => `<label><input type="checkbox" data-ask="${m.id}" ${S.askSel.has(m.id) ? "checked" : ""}>
      <span class="chip" style="background:${colorOf(m.id)}"></span>${esc(m.name)}</label>`).join("")
    || `<span class="muted">준비된 모델이 없습니다. ① 에서 띄우거나 떠 있는 서버에 붙으세요.</span>`);
  document.querySelectorAll("[data-ask]").forEach((c) => c.onchange = () => { c.checked ? S.askSel.add(c.dataset.ask) : S.askSel.delete(c.dataset.ask); });
}

// ---------------------------------------------------------------- ② 이미지 폴더
async function openFolder() {
  const dir = $("#f-dir").value.trim();
  if (!dir) return;
  try {
    const j = await api(`/api/folder?dir=${encodeURIComponent(dir)}`);
    S.items = j.items; $("#f-dir").value = j.folder;
    $("#f-count").textContent = `${j.items.length}장${j.more ? " (더 있음: 하위 폴더를 여세요)" : ""}`;
    renderThumbs(); loadRecent();
  } catch (e) { toast(e.message); }
}
async function loadRecent() {
  try { const j = await api("/api/recent"); $("#f-recent").innerHTML = j.folder.map((p) => `<option value="${esc(p)}">`).join(""); } catch (e) { /* 없어도 됨 */ }
}
const keyOf = (it) => `${it.path}#${it.page}`;
function renderThumbs() {
  const f = $("#f-filter").value.trim().toLowerCase();
  const list = S.items.filter((it) => !f || it.name.toLowerCase().includes(f)).slice(0, 600);
  const picked = S.picked.map(keyOf);
  $("#thumbs").innerHTML = list.map((it) => {
    const k = keyOf(it), n = picked.indexOf(k);
    return `<div class="th ${S.cur && keyOf(S.cur) === k ? "cur" : n >= 0 ? "sel" : ""}" data-k="${esc(k)}" title="${esc(it.name)}">
      <img loading="lazy" src="/img?path=${encodeURIComponent(it.path)}&page=${it.page}&thumb=240"><span>${n >= 0 && S.picked.length > 1 ? `[${n + 1}] ` : ""}${esc(it.name)}</span></div>`;
  }).join("");
  $("#thumbs").querySelectorAll(".th").forEach((d) => d.onclick = (ev) => {
    const it = S.items.find((x) => keyOf(x) === d.dataset.k);
    if (ev.ctrlKey || ev.metaKey) {
      const i = S.picked.findIndex((x) => keyOf(x) === d.dataset.k);
      if (i >= 0) { S.picked.splice(i, 1); if (S.cur && keyOf(S.cur) === d.dataset.k) S.cur = S.picked[S.picked.length - 1] || null; }
      else { S.picked.push(it); S.cur = it; }
    } else { S.picked = [it]; S.cur = it; }
    newConversation(); showCurrent(); renderThumbs();
  });
}
$("#f-open").onclick = openFolder;
$("#f-dir").addEventListener("keydown", (e) => { if (e.key === "Enter") openFolder(); });
$("#f-filter").addEventListener("input", debounce(renderThumbs, 200));

function showCurrent() {
  S.shapes = { box: null, anchor: null, markers: {} };
  $("#picked").innerHTML = S.picked.length ? `보낼 그림 ${S.picked.length}장: ` + S.picked.map((x, i) => `${S.picked.length > 1 ? `[${i + 1}] ` : ""}${esc(x.name)}`).join(", ")
    + (S.picked.length > 1 ? ` <span class="muted">· 크게 보는 것: ${esc(S.cur?.name)}</span>` : "") : "그림을 고르세요";
  if (!S.cur) { $("#canvas").classList.add("hidden"); S.size = null; return; }
  const img = $("#big");
  img.onload = () => { S.size = [img.naturalWidth, img.naturalHeight]; drawShapes(); refreshQuestion(); };
  img.src = `/img?path=${encodeURIComponent(S.cur.path)}&page=${S.cur.page}`;
  $("#canvas").classList.remove("hidden");
}

// ---------------------------------------------------------------- ② 그림에 네모 끌기
function drawMode() {
  const t = S.byTask[$("#q-task").value] || { needs: [] };
  if (t.needs.includes("box")) return "box";
  if (t.needs.includes("anchor")) return "anchor";
  if (t.needs.includes("marker")) return "marker";
  return null;
}
const HINT = { box: "그림에서 네모를 끌어 영역을 정합니다 (다시 끌면 바뀜).", anchor: "기준 글자를 적거나, 그림에서 기준 글자에 네모를 끕니다.",
  marker: "색을 고르고 글자 둘레에 네모를 끕니다. 벤치마크와 같은 굵기·여백으로 그려 보냅니다." };
function pct(box) { const [w, h] = S.size; return `left:${100 * box[0] / w}%;top:${100 * box[1] / h}%;width:${100 * (box[2] - box[0]) / w}%;height:${100 * (box[3] - box[1]) / h}%`; }
function drawShapes() {
  if (!S.size) return;
  const out = [];
  const mode = drawMode();
  $("#draw-hint").textContent = mode ? HINT[mode] : "이 질문은 그림에 정할 것이 없습니다.";
  if (S.shapes.box && mode === "box") out.push(`<div class="shape" style="${pct(S.shapes.box)}"></div>`);
  if (S.shapes.anchor && mode === "anchor") out.push(`<div class="shape" style="${pct(S.shapes.anchor)}"><span class="lab" style="background:var(--accent)">기준</span></div>`);
  if (mode === "marker") for (const [c, b] of Object.entries(S.shapes.markers)) out.push(`<div class="shape marker" style="${pct(b)};border-color:${MARK[c]}"></div>`);
  for (const a of answerBoxesOnCurrent()) out.push(`<div class="shape ans" style="${pctN(a.box)};border-color:${a.color}"><span class="lab" style="background:${a.color}">${esc(a.label ?? "")}</span></div>`);
  $("#shapes").innerHTML = out.join("");
}
function pctN(b) { return `left:${b[0] / 10}%;top:${b[1] / 10}%;width:${(b[2] - b[0]) / 10}%;height:${(b[3] - b[1]) / 10}%`; }
(function drag() {
  const cv = $("#canvas");
  let start = null;
  const at = (ev) => { const r = $("#big").getBoundingClientRect(); const sx = S.size[0] / r.width, sy = S.size[1] / r.height;
    return [Math.min(S.size[0], Math.max(0, (ev.clientX - r.left) * sx)), Math.min(S.size[1], Math.max(0, (ev.clientY - r.top) * sy))]; };
  cv.addEventListener("mousedown", (ev) => { if (!S.size || !drawMode()) return; ev.preventDefault(); start = at(ev); });
  window.addEventListener("mousemove", (ev) => { if (!start) return; setShape(start, at(ev), false); });
  window.addEventListener("mouseup", (ev) => { if (!start) return; const s = start; start = null; setShape(s, at(ev), true); });
  function setShape(a, b, done) {
    const box = [Math.min(a[0], b[0]), Math.min(a[1], b[1]), Math.max(a[0], b[0]), Math.max(a[1], b[1])].map(Math.round);
    if (done && (box[2] - box[0] < 3 || box[3] - box[1] < 3)) { drawShapes(); return; }
    const mode = drawMode();
    if (mode === "marker") S.shapes.markers[$("#q-color").value] = box; else S.shapes[mode] = box;
    drawShapes();
    if (done) refreshQuestion();
  }
})();

// ---------------------------------------------------------------- ② 질문
async function loadForms() {
  const j = await api("/api/forms");
  S.tasks = j.tasks; S.byTask = Object.fromEntries(j.tasks.map((t) => [t.id, t]));
  const groups = [...new Set(j.tasks.map((t) => t.group))];
  $("#q-task").innerHTML = groups.map((g) => `<optgroup label="${esc(g)}">` + j.tasks.filter((t) => t.group === g)
    .map((t) => `<option value="${t.id}">${esc(t.name)} (${t.id})</option>`).join("") + "</optgroup>").join("");
  $("#forms").innerHTML = j.forms.map((f) => `<option value="${esc(f.id)}">${esc(f.name)}</option>`).join("");
  $("#q-basis").value = new Date().toISOString().slice(0, 10);
  taskChanged();
}
function taskChanged() {
  const t = S.byTask[$("#q-task").value];
  const n = t.needs;
  $("#w-lang").classList.toggle("hidden", t.group !== "OCR");
  $("#w-form").classList.toggle("hidden", !(n.includes("form") || ["classify", "ocr_page", "ocr_field"].includes(t.id)));
  $("#w-maxkeys").classList.toggle("hidden", !n.includes("form"));
  $("#w-text").classList.toggle("hidden", !n.includes("text"));
  $("#w-anchor").classList.toggle("hidden", !n.includes("anchor"));
  $("#w-marker").classList.toggle("hidden", !n.includes("marker"));
  $("#w-field").classList.toggle("hidden", !n.includes("field"));
  S.promptEdited = false; newConversation(); drawShapes(); refreshQuestion();
}
function spec() {
  const task = $("#q-task").value;
  const formIn = $("#q-form").value.trim();
  return { task, lang: $("#q-lang").value, form: formIn || null, max_keys: Number($("#q-maxkeys").value || 0), size: S.size,
    box: S.shapes.box, text: $("#q-text").value, anchor_text: $("#q-anchor").value.trim(), anchor_box: S.shapes.anchor,
    direction: $("#q-dir").value, marker: { color: $("#q-color").value, box: S.shapes.markers[$("#q-color").value] },
    coords: $("#q-coords").checked, label: $("#q-label").value, basis: $("#q-basis").value };
}
const refreshQuestion = debounce(async () => {
  const note = $("#q-note");
  try {
    const j = await api("/api/question", spec());
    note.textContent = j.note || ""; note.classList.remove("warn");
    S.basePrompt = j.prompt;
    if (!S.promptEdited) $("#q-prompt").value = j.prompt;
    $("#q-reset").classList.toggle("hidden", !S.promptEdited || $("#q-prompt").value === S.basePrompt);
  } catch (e) { note.textContent = e.message; note.classList.add("warn"); }
}, 250);
$("#q-task").onchange = taskChanged;
["#q-lang", "#q-dir", "#q-coords", "#q-basis"].forEach((s) => $(s).addEventListener("change", () => refreshQuestion()));
["#q-form", "#q-maxkeys", "#q-text", "#q-anchor", "#q-label"].forEach((s) => $(s).addEventListener("input", () => refreshQuestion()));
$("#q-color").onchange = () => { drawShapes(); refreshQuestion(); };
$("#q-prompt").addEventListener("input", () => { S.promptEdited = $("#q-prompt").value !== S.basePrompt; $("#q-reset").classList.toggle("hidden", !S.promptEdited); });
$("#q-reset").onclick = () => { $("#q-prompt").value = S.basePrompt; S.promptEdited = false; $("#q-reset").classList.add("hidden"); };

// ---------------------------------------------------------------- ② 묻기·답
function op() {
  const t = S.byTask[$("#q-task").value];
  const index = Math.max(0, S.picked.findIndex((x) => S.cur && keyOf(x) === keyOf(S.cur)));
  if (t.image === "crop") { if (!S.shapes.box) throw new Error("그림에서 자를 곳에 네모를 끄세요"); return { index, crop: S.shapes.box }; }
  if (t.image === "marker") {
    const ms = Object.entries(S.shapes.markers).map(([color, box]) => ({ color, box }));
    if (!S.shapes.markers[$("#q-color").value]) throw new Error("고른 색의 상자를 그림에서 끄세요");
    return { index, markers: ms };
  }
  return null;
}
async function ask(prompt, followup) {
  if (!S.picked.length) return toast("그림을 고르세요");
  if (!S.askSel.size) return toast("묻는 모델을 고르세요 (위쪽)");
  let o;
  try { o = op(); } catch (e) { return toast(e.message); }
  const btns = [$("#q-ask"), $("#q-send")];
  btns.forEach((b) => { b.disabled = true; });
  $("#answers").insertAdjacentHTML("afterbegin", `<p class="muted" id="waiting">묻는 중… (${[...S.askSel].map((id) => esc(S.models.find((m) => m.id === id)?.name)).join(", ")})</p>`);
  try {
    const j = await api("/api/ask", { models: [...S.askSel], images: S.picked.map((x) => ({ path: x.path, page: x.page })), task: $("#q-task").value,
      prompt, op: o, same_as_eval: $("#q-fit").checked, turns: followup ? S.turns : [] });
    const answers = Object.fromEntries(Object.entries(j.results).map(([id, r]) => [id, r.text ?? ""]));
    if (!followup) S.turns = [];
    S.turns.push({ prompt, answers });
    S.last = { results: j.results, task: followup ? "custom" : $("#q-task").value, image: S.byTask[$("#q-task").value].image };
    renderAnswers(); drawShapes();
    $("#followup").classList.remove("hidden");
  } catch (e) { toast(e.message); }
  finally { btns.forEach((b) => { b.disabled = false; }); $("#waiting")?.remove(); }
}
$("#q-ask").onclick = () => ask($("#q-prompt").value.trim(), false);
$("#q-send").onclick = () => { const v = $("#q-next").value.trim(); if (v) { ask(v, true); $("#q-next").value = ""; } };
$("#q-next").addEventListener("keydown", (e) => { if (e.key === "Enter") $("#q-send").click(); });
$("#q-new").onclick = () => { newConversation(); drawShapes(); };
function newConversation() { S.turns = []; S.last = null; $("#answers").innerHTML = ""; $("#followup").classList.add("hidden"); }

function answerBoxesOnCurrent() {
  if (!S.last || !S.cur || S.last.image === "crop") return [];
  const ci = Math.max(0, S.picked.findIndex((x) => keyOf(x) === keyOf(S.cur)));
  const page = S.last.image === "marker" ? 1 : ci + 1;
  const out = [];
  for (const [id, r] of Object.entries(S.last.results)) for (const b of r.boxes || []) if ((b.page || 1) === page) out.push({ ...b, color: colorOf(id) });
  return out;
}
function renderAnswers() {
  const hist = S.turns.slice(0, -1).map((t, i) => `<div class="turn"><b>Q${i + 1}</b> ${esc(t.prompt.slice(0, 300))}${t.prompt.length > 300 ? "…" : ""}
    ${Object.entries(t.answers).map(([id, a]) => `<br><span class="chip" style="background:${colorOf(id)}"></span>${esc(a.slice(0, 300))}`).join("")}</div>`).join("");
  const cards = Object.entries(S.last.results).map(([id, r]) => {
    const m = S.models.find((x) => x.id === id);
    const badges = [r.seconds != null ? `<span class="badge">${r.seconds}초</span>` : "",
      r.finish_reason === "length" ? `<span class="badge bad">길이 한도에서 끊김</span>` : "",
      r.format_error ? `<span class="badge bad">형식 오류 (JSON 으로 못 읽음)</span>` : "",
      r.boxes?.length ? `<span class="badge">상자 ${r.boxes.length}개</span>` : ""].join("");
    const sent = (r.sent || []).map((s, i) => `<div class="sent"><img src="/sent/${s.name}" title="보낸 그림 ${s.size.join("×")}">
      <div class="shapes">${(r.boxes || []).filter((b) => (b.page || 1) === i + 1).map((b) => `<div class="shape ans" style="${pctN(b.box)};border-color:${colorOf(id)}"></div>`).join("")}</div></div>`).join("");
    return `<div class="card"><h3><span class="chip" style="background:${colorOf(id)}"></span>${esc(m?.name || r.model || id)} ${badges}</h3>
      ${r.error ? `<pre class="light bad">${esc(r.error)}</pre>` : `<pre class="light">${esc(r.text)}</pre>`}
      ${r.json !== undefined ? `<details><summary>JSON 으로 읽은 결과</summary><pre class="light">${esc(JSON.stringify(r.json, null, 1))}</pre></details>` : ""}
      <details ${S.last.image ? "open" : ""}><summary>보낸 그림 ${(r.sent || []).length}장 (${(r.sent || []).map((s) => s.size.join("×")).join(", ")})</summary>${sent}</details></div>`;
  }).join("");
  $("#answers").innerHTML = hist + (S.turns.length > 1 ? `<div class="turn"><b>Q${S.turns.length}</b> ${esc(S.turns[S.turns.length - 1].prompt)}</div>` : "") + cards;
}

loadForms().catch((e) => toast(e.message));
loadModels(); loadGpus(); loadRecent();
