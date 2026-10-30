// ① 서식: 목록, 상세(미리보기·예시·문항 Q/A·편집·검수·키 목록·파일), html 서식 복제.
// 탭 중 문항 Q/A 는 questions.js, 영역 편집(원본 서식)은 editor.js, 자리·템플릿(html·코드 서식)은 html-spots.js, html 편집(복제 서식의 form.json·분석기)은 htmled.js 가 그린다.
// 서버: studio/app.py (/api/forms…), studio/catalog.py, 복제는 studio/api_html.py
"use strict";

addRoute(/^#\/forms\/([^/]+)(?:\/(\w+))?$/, (id, tab) => viewForm(decodeURIComponent(id), tab || "overview"), "forms");
addRoute(/^#\/forms$/, () => viewForms(), "forms");

const REVIEW_TAG = {
  none: `<span class="tag">미검수</span>`,
  done: `<span class="tag ok">검수 완료</span>`,
  stale: `<span class="tag warn">수정 후 재검수 필요</span>`,
};
const SPLIT_NAME = { unassigned: "미배정", train: "학습·평가 모두", test_only: "평가 전용" };

async function loadForms(force = false) {
  if (!state.forms || force) state.forms = await api("/api/forms");
  return state.forms;
}

async function viewForms() {
  if (!state.forms) main().innerHTML = `<p class="spin">서식 목록을 읽는 중…</p>`;
  await loadForms();
  const f = state.filter;
  const groups = [...new Map(state.forms.map(x => [x.group, x.group_name])).entries()];
  main().innerHTML = `
    <h1>서식</h1>
    <div class="sub">생성기가 만드는 서식 ${state.forms.length}종. 줄을 누르면 상세·예시를 봅니다.</div>
    <div class="bar">
      <input type="text" id="f-q" placeholder="ID·서식명 검색" value="${esc(f.q)}" style="width:220px">
      <select id="f-group"><option value="">그룹 전체</option>${groups.map(([g, n]) =>
        `<option value="${esc(g)}" ${f.group === g ? "selected" : ""}>${esc(n)}</option>`).join("")}</select>
      <select id="f-kind">${[["", "종류 전체"], ["html", "html"], ["overlay", "overlay"]].map(([v, n]) =>
        `<option value="${v}" ${f.kind === v ? "selected" : ""}>${n}</option>`).join("")}</select>
      <select id="f-review">${[["", "검수 전체"], ["no", "미검수"], ["yes", "검수 완료"]].map(([v, n]) =>
        `<option value="${v}" ${f.review === v ? "selected" : ""}>${n}</option>`).join("")}</select>
      <label><input type="checkbox" id="f-korean" ${f.korean ? "checked" : ""}> 한글 키 있음</label>
      <label title="행 수가 서류마다 달라지는 반복 묶음 (rows[].kind) — 표 과제 table·table_read·table_find·table_qa 가 묻는다"><input type="checkbox" id="f-tables" ${f.tables ? "checked" : ""}> 표 있음</label>
      <label><input type="checkbox" id="f-scenario" ${f.scenario ? "checked" : ""}> 업무 시나리오에 쓰임</label>
      <label><input type="checkbox" id="f-issues" ${f.issues ? "checked" : ""}> 문제 표시 있음</label>
      <label><input type="checkbox" id="f-edited" ${f.edited ? "checked" : ""}> 사람 수정 있음</label>
      <span class="muted" id="f-count"></span>
      <button id="f-refresh" title="서식 폴더(docgen/forms/<ID>/, 사내 서식 폴더)를 다시 훑어 새로 넣은 서식을 등록하고, 이름·그룹을 다시 읽고, 지운 폴더는 목록에서 뺍니다. 다시 띄우지 않아도 됩니다">서식 다시 읽기</button>
    </div>
    <div id="f-refreshed">${state.showRefreshed ? refreshNote(state.refreshed) : ""}</div>
    <div id="f-table"></div>`;
  $("#f-refresh").addEventListener("click", async () => {
    const b = $("#f-refresh");
    b.disabled = true;
    b.textContent = "읽는 중…";
    try {
      state.refreshed = await api("/api/forms/refresh", {});
      Object.keys(formCache).forEach(k => delete formCache[k]);
      await loadForms(true);
      const r = state.refreshed;
      toast(`서식 다시 읽기: 새로 ${r.added.length} · 바뀜 ${r.updated.length} · 빠짐 ${r.removed.length} · 문제 ${r.problems.length}`, r.problems.length > 0);
      if (location.hash === "#/forms") {   // 기다리는 동안 다른 화면으로 갔으면 덮어쓰지 않는다
        state.showRefreshed = true;
        viewForms();
      }
    } catch (e) {
      toast(e.message, true);
      b.disabled = false;
      b.textContent = "서식 다시 읽기";
    }
  });
  state.showRefreshed = false;   // 다시 읽기 결과는 누른 직후에만 (목록을 가리지 않게)
  $("#f-refreshed").addEventListener("click", e => { if (e.target.closest("[data-close]")) $("#f-refreshed").innerHTML = ""; });
  const ids = ["#f-q", "#f-group", "#f-kind", "#f-review", "#f-korean", "#f-tables", "#f-scenario", "#f-issues", "#f-edited"];
  const update = () => {
    Object.assign(f, {
      q: $("#f-q").value.trim(), group: $("#f-group").value, kind: $("#f-kind").value, review: $("#f-review").value,
      korean: $("#f-korean").checked, tables: $("#f-tables").checked, scenario: $("#f-scenario").checked, issues: $("#f-issues").checked,
      edited: $("#f-edited").checked,
    });
    store.set("filter", f);
    drawFormTable();
  };
  ids.forEach(s => $(s).addEventListener(s === "#f-q" ? "input" : "change", update));
  drawFormTable();
}

function refreshNote(r) {
  if (!r) return "";
  const ids = (xs, name) => xs.length ? `<div><b>${name} ${xs.length}</b> ${xs.map(x =>
    `<a class="mono" href="#/forms/${encodeURIComponent(x)}">${esc(x)}</a>`).join(" ")}</div>` : "";
  const probs = r.problems.length ? `<div class="kr"><b>문제 ${r.problems.length}</b> (등록하지 않음)<ul>${r.problems.map(p =>
    `<li><span class="mono">${esc(p.id)}</span> — ${esc(p.reason)}</li>`).join("")}</ul></div>` : "";
  const none = !r.added.length && !r.updated.length && !r.removed.length && !r.problems.length;
  const cards = (r.stale_cards || []).length ? `<div><b>카드가 없거나 오래됨 ${r.stale_cards.length}</b> <span class="muted">(서식 파일·질문을 고친 뒤 FORM.md 를 안 다시 만듦 — 서식의 카드 탭 또는 <span class="mono">python -m docgen.formdir card --all --stale --workers 4</span>)</span>
    ${r.stale_cards.slice(0, 20).map(x => `<a class="mono" href="#/forms/${encodeURIComponent(x)}/card">${esc(x)}</a>`).join(" ")}${r.stale_cards.length > 20 ? " …" : ""}</div>` : "";
  return `<div class="box"><button data-close style="float:right" title="닫기">✕</button>${none ? `<span class="muted">서식 다시 읽기: 바뀐 것 없음</span>` :
    ids(r.added, "새로") + ids(r.updated, "이름·그룹 바뀜") +
    `${(r.with_script || []).length ? `<div class="kr"><b>생성 스크립트 있음 ${r.with_script.length}</b> ${r.with_script.map(esc).join(" ")} <span class="muted">(값을 만든 뒤 실행되는 코드입니다. 사람이 내용을 읽고 넣었는지 확인하세요 — 파일 탭)</span></div>` : ""}` + `${r.removed.length ? `<div><b>빠짐 ${r.removed.length}</b> <span class="mono">${r.removed.map(esc).join(" ")}</span> <span class="muted">(폴더가 없어짐. 검수 기록은 남아 있어 폴더를 되돌리면 다시 나옵니다)</span></div>` : ""}` + probs}${cards}</div>`;
}

function drawFormTable() {
  const f = state.filter, q = f.q.toLowerCase();
  let rows = state.forms.filter(x =>
    (!q || x.id.toLowerCase().includes(q) || x.name.toLowerCase().includes(q) ||
      (x.official_source && ("공식대조 HTML " + x.official_source.publisher).toLowerCase().includes(q))) &&
    (!f.group || x.group === f.group) && (!f.kind || x.kind === f.kind) &&
    (!f.review || (f.review === "yes") === !!x.reviewed) &&
    (!f.korean || x.n_korean_keys > 0) && (!f.tables || x.tables.length > 0) && (!f.scenario || x.scenarios.length > 0) &&
    (!f.issues || x.open_issues > 0) && (!f.edited || x.edited));
  const { key, dir } = state.sort;
  rows = rows.slice().sort((a, b) => {
    const va = Array.isArray(a[key]) ? a[key].length : a[key], vb = Array.isArray(b[key]) ? b[key].length : b[key];
    return (va > vb ? 1 : va < vb ? -1 : 0) * dir;
  });
  $("#f-count").textContent = `${rows.length}종`;
  const cols = [["id", "ID"], ["name", "서식명"], ["group_name", "그룹"], ["kind", "종류"], ["n_keys", "키", 1],
    ["n_korean_keys", "한글 키", 1], ["n_empty", "값 없는 칸", 1], ["n_marks", "체크·도장·서명", 1], ["tables", "표", 1],
    ["scenarios", "시나리오"], ["split", "배정"], ["open_issues", "문제", 1], ["reviewed", "검수"]];
  $("#f-table").innerHTML = `<table><thead><tr>${cols.map(([k, n, num]) =>
    `<th data-k="${k}" class="${num ? "num" : ""}">${n}${state.sort.key === k ? (dir > 0 ? " ▲" : " ▼") : ""}</th>`).join("")}
    </tr></thead><tbody>${rows.map(x => `
    <tr class="click" data-id="${esc(x.id)}">
      <td class="mono">${esc(x.id)}</td><td>${esc(x.name)}${x.official_source ? ` <span class="tag" title="공식 대조 원문 있음 · 서식·라벨 사람 검수는 별도">공식대조 HTML</span>` : ""}${x.edited ? ` <span class="tag ok" title="사람 수정 있음">수정</span>` : ""}${x.script ? ` <span class="tag warn" title="서식 폴더에 생성 스크립트 generate.py 가 있습니다 (값을 만든 뒤 실행되는 코드). 파일 탭에서 내용을 볼 수 있습니다">스크립트</span>` : ""}</td>
      <td class="nw">${esc(x.group_name)}</td>
      <td><span class="tag ${x.kind}">${x.kind}</span></td>
      <td class="num">${x.n_keys}</td>
      <td class="num ${x.n_korean_keys ? "kr" : ""}">${x.n_korean_keys || ""}</td>
      <td class="num">${x.n_empty || ""}</td><td class="num">${x.n_marks || ""}</td>
      <td class="num" title="${esc(x.tables.join(", "))}">${x.tables.length || ""}</td>
      <td>${x.scenarios.map(s => `<span class="tag">${esc(s)}</span>`).join("")}</td>
      <td class="nw">${x.split === "unassigned" ? `<span class="muted">-</span>` : esc(SPLIT_NAME[x.split] || x.split)}</td>
      <td class="num ${x.open_issues ? "kr" : ""}">${x.open_issues || ""}</td>
      <td class="nw">${x.reviewed ? `<span class="tag ok">완료</span>` : `<span class="muted">미검수</span>`}</td>
    </tr>`).join("")}</tbody></table>`;
  $("#f-table thead").addEventListener("click", e => {
    const k = e.target.closest("th")?.dataset.k;
    if (!k) return;
    state.sort = { key: k, dir: state.sort.key === k ? -state.sort.dir : 1 };
    drawFormTable();
  });
  $("#f-table tbody").addEventListener("click", e => {
    const id = e.target.closest("tr")?.dataset.id;
    if (id) location.hash = `#/forms/${encodeURIComponent(id)}`;
  });
}

// ---------------------------------------------------------------------------
// 서식 상세
// ---------------------------------------------------------------------------
const formCache = {};

async function formDetail(id, force = false) {
  if (!formCache[id] || force) formCache[id] = await api(`/api/forms/${encodeURIComponent(id)}`);
  return formCache[id];
}

// 서식 상세는 할 일 넷으로 나눈다: 무엇을 하나(개요) · 그림이 맞나(그림·검수) · 어떻게 묻고 답하나(질문·답) · 고치기.
// 아래 줄은 그 일 안의 화면. 주소는 화면 이름 그대로 (#/forms/<ID>/card 등) 라 다른 화면의 링크가 그대로 맞다.
function formTabs(d) {
  const editable = d.kind === "overlay";
  const open = d.issues.filter(x => x.status === "open").length;
  return [
    ["개요", "이 서식이 무엇을 묻는지와 상태", [["overview", "요약"], ["card", "카드 원문"], ["guide", "업무·시나리오"]]],
    ["그림·검수", "그린 그림과 정답이 맞는지 눈으로 보고 검수", [["preview", "미리보기"], ["examples", "여러 장 보기"],
      ["review", `검수${open ? ` · 문제 ${open}` : ""}`]]],
    ["질문·답", "과제마다 실제 질문·정답·채점, 칸이 누구의 무엇인지", [["questions", "실제 문항"], ["keys", `키 (${d.keys.length})`]]],
    ["고치기", "값·위치·모양·칸·질문 설정", [["edit", editable ? "영역 편집" : "자리·템플릿"],
      ...(!editable ? [["templates", "레이아웃·샘플링"]] : []),
      ...(!editable && d.origin !== "builtin" ? [["html", "html 편집"]] : []),
      ["files", "파일"]]],
  ];
}

async function viewForm(id, tab) {
  const d = await formDetail(id, tab === "review");
  const editable = d.kind === "overlay";
  const groups = formTabs(d);
  const group = groups.find(g => g[2].some(([t]) => t === tab)) || groups[0];
  if (!group[2].some(([t]) => t === tab)) tab = group[2][0][0];
  const href = t => `#/forms/${encodeURIComponent(id)}/${t}`;
  main().innerHTML = `
    <div class="muted"><a href="#/forms">서식</a> › ${esc(d.group_name)}</div>
    <h1>${esc(d.name)} <span class="mono muted">${esc(d.id)}</span></h1>
    <div>
      <span class="tag ${d.kind}">${d.kind} · ${d.origin}</span>
      ${d.official_source ? `<span class="tag">공식대조 HTML</span>` : ""}
      <span class="tag">${d.category === "internal" ? "은행 서식" : "외부 발급"}</span>
      ${REVIEW_TAG[d.review_state] || ""}
      <span class="tag">배정: ${esc(SPLIT_NAME[d.split] || d.split)}</span>
      ${d.edited ? `<span class="tag ok">사람 수정 있음</span>` : ""}
      ${d.n_korean_keys ? `<span class="tag warn">한글 키 ${d.n_korean_keys}</span>` : ""}
      ${d.scenario_names.map(s => `<span class="tag">시나리오: ${esc(s.name)}</span>`).join("")}
      ${d.kind === "html" ? `<button id="f-clone" title="템플릿을 사본으로 만들어 html 편집기에서 고칩니다 (값은 부모 생성 함수 + 칸 목록 fields.json)">복제</button>` : ""}
    </div>
    ${d.description ? `<div class="sub" style="margin-top:6px">${esc(d.description)}</div>` : ""}
    ${d.document_role ? `<div class="sub">제출 역할: <b>${esc(d.document_role.name)}</b> · 같은 역할 서식 ${d.document_role.forms.length}종
      ${d.document_role.forms.filter(x => x !== d.id).map(x => `<a href="#/forms/${encodeURIComponent(x)}">${esc(x)}</a>`).join(' · ')}</div>` : ""}
    ${d.official_source ? `<div class="sub">${esc(d.official_source.publisher)} · ${esc(d.official_source.revision || "")} · <a href="${esc(d.official_source.url)}" target="_blank" rel="noopener noreferrer">공식 원문 보기</a></div>` : ""}
    <div class="tabs">${groups.map(g =>
      `<a href="${href(g[2][0][0])}" class="${g === group ? "on" : ""}" title="${esc(g[1])}">${esc(g[0])}</a>`).join("")}</div>
    ${group[2].length > 1 ? `<div class="subtabs">${group[2].map(([t, n]) =>
      `<a href="${href(t)}" class="${t === tab ? "on" : ""}">${esc(n)}</a>`).join("")}</div>` : ""}
    <div id="tab"></div>`;
  if ($("#f-clone")) $("#f-clone").onclick = async () => {
    const nid = (prompt("새 서식 ID (영어 소문자·숫자·밑줄)", `${d.id}_copy`) || "").trim();
    if (!nid) return;
    const name = (prompt("새 서식 이름", `${d.name} (복제)`) || "").trim();
    try {
      await api(`/api/forms/${encodeURIComponent(d.id)}/clone`, { new_id: nid, name });
      state.forms = null; toast("복제했습니다. html 편집기로 갑니다");
      location.hash = `#/forms/${encodeURIComponent(nid)}/html`;
    } catch (e) { toast(e.message, true); }
  };
  if (tab === "overview") return tabOverview(d);
  if (tab === "preview") return tabPreview(d);
  if (tab === "card") return tabCard(d);
  if (tab === "guide") return tabGuide(d);
  if (tab === "examples") return tabExamples(d);
  if (tab === "questions") return tabQuestions(d);
  if (tab === "edit" && editable) return viewEditor(d);
  if (tab === "edit") return viewHtmlSpots(d);
  if (tab === "templates") return viewTemplateVariants(d);
  if (tab === "html" && typeof viewHtmlEditor === "function") return viewHtmlEditor(d);
  if (tab === "review") return tabReview(d);
  if (tab === "keys") return tabKeys(d);
  return tabFiles(d);
}

// 개요 › 요약: 상태 한 줄 + 과제마다 무엇을 묻는지 (GET /api/forms/{id}/overview, studio/catalog.py overview) ----------
async function tabOverview(d) {
  const box = $("#tab"), id = encodeURIComponent(d.id);
  const open = d.issues.filter(x => x.status === "open").length;
  const a = d.value_audit;
  box.innerHTML = `<div class="ov-status">
      <div><span class="muted">검수</span> ${REVIEW_TAG[d.review_state] || ""} <a href="#/forms/${id}/review">검수 화면</a></div>
      <div><span class="muted">문제 표시</span> ${open ? `<a class="kr" href="#/forms/${id}/review">남은 ${open}개</a>` : "없음"}</div>
      <div><span class="muted">배정</span> ${esc(SPLIT_NAME[d.split] || d.split)}</div>
      <div><span class="muted">질문 검사</span> <span id="ov-check" class="muted">…</span></div>
      <div><span class="muted">카드</span> <span id="ov-card" class="muted">…</span></div>
    </div>
    ${a ? `<details class="panel"><summary>이미지 값 점검 · ${a.checked_at} · seed ${a.seed}
      · 채운 값 ${a.filled}/${a.text_fields}${a.stale ? ' · 수정 후 다시 검사 필요' : ''}</summary>
      <p>자동 이미지 검사입니다. 사람 검수 완료와 별개입니다. 빈 값에는 미사용 행·기재 대상이 아닌 칸·출처가 없는 칸이 포함됩니다.</p>
      <p>${esc(a.coverage_note || '')}</p><p>쪽 넘침: ${a.overflow ? '있음' : '없음'} · 값 위치 누락 ${a.missing_positions?.length || 0} · 페이지 밖 ${a.offpage?.length || 0}</p>
      <div>${(a.empty || []).map(f => `<span class="tag">${esc(f.label || f.key)} · ${esc(f.key)}</span>`).join('')}</div>
      <a href="#/forms/${id}/edit">영역·값 출처 편집</a></details>` : ''}
    <h2>이 서식이 묻는 것</h2>
    <div class="sub">이 서식으로 데이터를 만들면 아래 과제마다 문항이 생깁니다. 고객 여러 명으로 그려 본 칸으로 셉니다 (카드와 같은 계산).
      행 번호가 있는 칸(<span class="mono">rows.*.kind</span>)은 표로 묶여 kie 가 아니라 표 과제가 묻습니다.
      고치는 곳 설명: <a href="#/guide/${encodeURIComponent("docgen/forms/README.md")}">서식 폴더 설명서</a></div>
    <div id="ov-tasks"><p class="spin">그려 보며 세는 중…</p></div>`;
  let o, formats;
  try { [o, formats] = await Promise.all([api(`/api/forms/${id}/overview`), loadQuestionFormats()]); }
  catch (e) { if (box.isConnected) $("#ov-tasks").innerHTML = `<p class="kr">${esc(e.message)}</p>`; return; }
  if (!box.isConnected || !$("#ov-tasks")) return;
  $("#ov-check").innerHTML = o.problems.length ? `<span class="kr">문제 ${o.problems.length} (아래)</span>` : `<span class="tag ok">통과</span>`;
  $("#ov-card").innerHTML = !o.card_exists ? `<a class="kr" href="#/forms/${id}/card">없음</a>`
    : o.card_stale ? `<a class="kr" href="#/forms/${id}/card" title="서식 파일·질문·공통 설정이 카드를 만든 뒤 바뀜">오래됨</a>` : `<a href="#/forms/${id}/card">최신</a>`;
  const name = t => formats[t]?.name || t;
  const seen = it => it.seen < it.of ? ` <span class="muted" title="그려 본 ${it.of}장 중 이 칸이 나온 장 수">${it.seen}/${it.of}장</span>` : "";
  const label = it => esc(it.q_label || it.label || (it.labels || []).filter(Boolean).join(" / ") || "-");
  const keyList = items => `<table class="ov-keys"><thead><tr><th>키</th><th>항목명 (질문에 쓰는 이름)</th><th></th></tr></thead><tbody>${items.map(it =>
    `<tr class="${it.ask === false ? "muted" : ""}"><td class="mono">${esc(it.column || it.key)}</td><td>${label(it)}${it.note ? ` <span class="muted">(${esc(it.note)})</span>` : ""}${seen(it)}</td>
      <td>${it.ask === false ? `<span class="tag">묻지 않음</span>` : ""}${(it.changed || []).length ? ` <span class="tag warn" title="fields.json 그 칸의 q">바꿈: ${esc(it.changed.join(", "))}</span>` : ""}</td></tr>`).join("")}</tbody></table>`;
  const asked = items => items.filter(it => it.ask !== false).length;
  const go = (tasks, text = "실제 문항") => `<a href="#/forms/${id}/questions" data-task="${tasks[0]}">${text}</a>`;
  const changed = t => (o.changed[t] || []).length ? ` <span class="tag warn" title="questions.json 에서 바꿈">바꿈: ${esc(o.changed[t].join(", "))}</span>` : "";
  const rows = [
    [name("classify") + changed("classify"), `무슨 서류인가 → 정답 <b>${esc(o.classify.answer)}</b>${o.classify.aliases?.length ? ` <span class="muted">(다른 이름 ${o.classify.aliases.map(esc).join(", ")})</span>` : ""}`,
      go(["classify"]), "<span class=mono>questions.json</span> 의 classify"],
    [`${name("ocr_page")} · ${name("ocr_field")}${changed("ocr_page")}`, `보이는 글자 전체 받아쓰기 · 값 칸 하나 읽기${o.ocr_off.length ? ` <span class="muted">— 뺀 칸 ${o.ocr_off.length}: ${o.ocr_off.map(esc).join(", ")}</span>` : ""}`,
      go(["ocr_page"]), "뺄 칸: <span class=mono>fields.json</span> 그 칸 <code>q.ocr</code>"],
    [name("kie") + changed("kie"), `<details><summary>칸 <b>${asked(o.kie)}</b>개의 값·위치${o.kie.length - asked(o.kie) ? ` <span class="muted">(묻지 않음 ${o.kie.length - asked(o.kie)})</span>` : ""}</summary>${keyList(o.kie)}</details>`,
      go(["kie"]), "묻는 칸·항목명: <span class=mono>fields.json</span> 그 칸 <code>q</code> · 문장·답 틀: <span class=mono>questions.json</span>"],
    ...o.tables.map(t => [`표 <span class="mono">${esc(t.group)}</span>${t.title ? ` '${esc(t.title)}'` : ""}`,
      `<details><summary>열 <b>${asked(t.columns)}</b>개, 행 수는 서류마다 다름 · ${["table", "table_read", "table_find", "table_qa"].map(name).join(" · ")}${t.seen < o.docs ? ` <span class="muted">· ${o.docs}장 중 ${t.seen}장에 행 있음</span>` : ""}</summary>${keyList(t.columns)}</details>`,
      go(["table"]), "제목·표 아님: <span class=mono>questions.json</span> 의 <code>table</code> · 열: <span class=mono>fields.json</span> <code>q</code> · 행 순서: 값 만드는 곳"]),
    ...(o.nested.length ? [["겹친 목록", `<details><summary>칸 ${o.nested.length}개 — 목록 안의 목록이라 표로도 kie 로도 묻지 않음</summary>${keyList(o.nested)}</details>`, "", "키를 <span class=mono>&lt;묶음&gt;.N.&lt;열&gt;</span> 꼴로"]] : []),
    [name("marks") + changed("marks"), o.marks.length ? `<details><summary>칸 <b>${asked(o.marks)}</b>개 (체크박스·도장·서명)</summary>${keyList(o.marks)}</details>` : `<span class="muted">없음</span>`,
      o.marks.length ? go(["marks"]) : "", "kie 와 같음"],
    [name("form_qa"), o.form_qa.length ? o.form_qa.map(r => `<span class="tag" title="${esc(r.kind || "")}">${esc(r.name)}</span>${r.asked < r.of ? ` <span class="muted">${r.asked}/${r.of}장</span>` : ""}`).join(" ")
      : `<span class="muted">없음 — 견본 <span class="mono">python -m docgen.formdir qa ${esc(d.id)} --new</span></span>`,
      o.form_qa.length ? go(["form_qa"]) : "", "<span class=mono>qa.py</span> (함수 하나 = 질문 하나)"],
    ["업무 묶음", d.scenario_names.length ? d.scenario_names.map(s => `<span class="tag">${esc(s.name)}</span>`).join(" ") + ` <span class="muted">— 구비 확인·대조·심사 문항에 쓰임</span>`
      : `<span class="muted">없음 (서류 한 건 과제에만)</span>`, d.scenario_names.length ? `<a href="#/forms/${id}/guide">업무·시나리오</a>` : "", "③ 시나리오"],
  ];
  $("#ov-tasks").innerHTML = `<table class="ov-tasks"><thead><tr><th>과제</th><th>묻는 것</th><th></th><th>고치는 곳</th></tr></thead><tbody>${rows.map(([t, w, l, f]) =>
      `<tr><td class="nw">${t}</td><td>${w}</td><td class="nw">${l}</td><td class="muted">${f}</td></tr>`).join("")}</tbody></table>
    ${o.problems.length ? `<h3 id="ov-problems" class="kr">질문 검사 문제 ${o.problems.length}</h3><ul>${o.problems.map(p => `<li>${esc(p)}</li>`).join("")}</ul>` : ""}
    ${o.notes.length ? `<details><summary class="muted">참고 ${o.notes.length}</summary><ul>${o.notes.map(p => `<li>${esc(p)}</li>`).join("")}</ul></details>` : ""}
    <div class="sub">질문 검사는 질문 설정(questions.json·칸의 q·qa.py)만 봅니다. 칸·값 출처·박스까지 보려면 <span class="mono">python -m docgen.formdir check ${esc(d.id)}</span>.</div>`;
  $("#ov-tasks").onclick = e => { const t = e.target.closest("[data-task]")?.dataset.task; if (t) state.qaTask = t; };
}

// 카드 탭: 서식 폴더의 FORM.md (docgen/formcard.py) — 항목·위치·정의한 곳·질문→답 예시·고치는 곳 ----------
async function tabCard(d) {
  const box = $("#tab");
  const draw = c => {
    if (!box.isConnected) return;
    const md = (c.markdown || "").split("\n").filter(l => !l.startsWith("<!--")).join("\n");
    box.innerHTML = `<div class="bar">
        <span class="mono muted">${esc(c.path)}</span>
        ${c.markdown == null ? `<span class="tag warn">카드 없음</span>` : c.stale ? `<span class="tag warn" title="이 서식의 파일·questions.json·공통 질문·키 사전이 카드를 만든 뒤 바뀌었습니다">오래됨</span>` : `<span class="tag ok">최신</span>`}
        <button id="cd-make">${c.markdown == null ? "카드 만들기" : "카드 다시 만들기"}</button><span id="cd-status" class="muted" role="status"></span></div>
      <div class="sub">이 서식 폴더만 보고 무엇을 어디서 뽑고, 어떻게 묻고, 답이 어떤 모양인지 알 수 있게 자동으로 만든 문서입니다. 직접 고치지 않고 아래 "고치려면" 표의 파일을 고칩니다.
        명령줄: <span class="mono">python -m docgen.formdir card ${esc(d.id)}</span></div>
      <div class="panel">${md ? guideMarkdown(md, "docgen/forms/" + d.id + "/FORM.md", []) : `<p class="muted">아직 카드가 없습니다.</p>`}</div>`;
    $("#cd-make").onclick = async () => {
      $("#cd-make").disabled = true; $("#cd-status").textContent = "그림을 그려 카드를 만드는 중…";
      try { draw(await api(`/api/forms/${encodeURIComponent(d.id)}/card`, {})); toast("카드를 다시 만들었습니다"); }
      catch (e) { toast(e.message, true); if (box.isConnected) { $("#cd-make").disabled = false; $("#cd-status").textContent = ""; } }
    };
  };
  box.innerHTML = `<p class="muted">읽는 중…</p>`;
  try { draw(await api(`/api/forms/${encodeURIComponent(d.id)}/card`)); } catch (e) { box.innerHTML = `<p class="kr">${esc(e.message)}</p>`; }
}

// 미리보기 탭 ---------------------------------------------------------------
function tabPreview(d) {
  const view = { label: null, page: 0, sel: -1, zoom: false, issueMode: false, cells: {} };
  const loadCells = async () => {   // 서식의 키 → 칸 (최종 키 · 누구의 · 무엇, 키 사전)
    await kpLoad();
    const r = await api(`/api/dictionary/cells?form=${encodeURIComponent(d.id)}&limit=3000`);
    view.cells = Object.fromEntries(r.rows.flatMap(c => c.raw.map(k => [k, c])));
  };
  const cellsReady = loadCells().catch(() => {});
  $("#tab").innerHTML = `
    <div class="bar">${optionBar(true)}
      <button class="primary" id="o-go">렌더링</button>
      <button id="o-prev" title="이전 seed">◀</button><button id="o-next" title="다음 seed">▶</button>
      <button id="o-force" title="캐시를 무시하고 다시 그림">다시 그리기</button>
      <span class="muted" id="o-stat"></span>
    </div>
    <div class="bar">${layerBar()}<button id="o-zoom">원래 크기</button>
      <button id="o-issue" title="그림에서 문제가 있는 곳을 눌러 메모를 남깁니다">문제 표시</button>
      <span class="keys-help">그림에서 박스 근처를 누르면 선택 · <kbd>↑</kbd><kbd>↓</kbd> 항목 이동 · <kbd>←</kbd><kbd>→</kbd> 쪽 · <kbd>Esc</kbd> 해제</span></div>
    <div class="viewer">
      <div><div class="pages" id="v-pages"></div><div class="stage" id="v-stage"></div></div>
      <div class="side panel" id="v-side"></div>
    </div>`;
  const issuesHere = () => (d.issues || []).filter(x => x.seed === view.label?.seed && (x.page || 0) === view.page && x.bbox &&
    (x.condition || "clean") === view.label?.condition)
    .map(x => ({ bbox: x.bbox, cls: `issue ${x.status === "done" ? "done" : ""}`, title: x.note }));
  const draw = (scroll = false) => {   // scroll: 선택한 박스가 보이게 그림을 움직임 (표·키보드로 고를 때만)
    const L = view.label;
    if (!L) return;
    $("#v-pages").innerHTML = L.pages.length > 1 ? L.pages.map((_, i) =>
      `<button data-p="${i}" class="${i === view.page ? "primary" : ""}">${i + 1}쪽</button>`).join("") : "";
    $("#v-stage").classList.toggle("zoom100", view.zoom);
    $("#v-stage").innerHTML = stageHTML(L, view.page, view.sel, issuesHere());
    drawSide();
    if (scroll) $("#v-stage rect.sel")?.scrollIntoView({ block: "nearest", inline: "nearest" });
  };
  const drawSide = () => {
    const L = view.label, f = L.fields[view.sel];
    const cell = f && view.cells[f.key];
    const detail = f ? `<div class="detail-box panel">
        <div>${cell ? kpKeyCell({ common: !!(cell.keys || []).find(k => k.raw === f.key)?.common, key: finalKey(f.key) }) : `<b class="mono">${esc(f.key)}</b>`}</div>
        ${cell && finalKey(f.key) !== f.key ? `<div class="muted" style="font-size:12px">서식의 키 <span class="mono">${esc(f.key)}</span></div>` : ""}
        ${cell ? "" : `<div>이름표: ${esc(f.label ?? "")}</div>`}<div>타입: ${esc(f.type)}</div>
        <div>값: ${esc(valueText(f))}</div>
        ${f.norm !== undefined && f.norm !== f.value ? `<div>정규화 값: <span class="mono">${esc(JSON.stringify(f.norm))}</span></div>` : ""}
        ${f.options ? `<div>보기: ${f.options.map(o => `${o.checked ? "■" : "□"} ${esc(o.text)}`).join(" ")}</div>` : ""}
        ${f.kind ? `<div>종류: ${esc(f.kind)}</div>` : ""}
        ${f.render ? `<div>풀 항목: ${esc(f.render)}</div>` : ""}
        ${f.corrected_from ? `<div>정정 전 값: ${esc(f.corrected_from)}</div>` : ""}
        <div>쪽: ${(f.page || 0) + 1} · 위치: ${f.bbox ? `<span class="mono">${f.bbox.map(Math.round).join(", ")}</span>` : "없음"}</div>
        ${cell ? `<div id="v-kp"></div>` : ""}
      </div>` : "";
    $("#v-side").innerHTML = `${detail}
      <div class="muted" style="margin-bottom:4px">항목 ${L.fields.length}개 · ${L.pages.length}쪽${L.overflow ? " · <b class=kr>쪽 넘침</b>" : ""}</div>
      <table><thead><tr><th>쪽</th><th>키</th><th>값</th></tr></thead><tbody>${L.fields.map((x, i) => `
        <tr class="click ${i === view.sel ? "sel" : ""}" data-i="${i}">
          <td>${(x.page || 0) + 1}</td><td class="mono ${/[^\x00-\x7f]/.test(finalKey(x.key)) ? "kr" : ""}">${(view.cells[x.key]?.keys || []).find(k => k.raw === x.key)?.common ? `<span class="tag ok">공통</span> ` : ""}${esc(finalKey(x.key))}</td>
          <td>${esc(valueText(x))}${x.bbox ? "" : ` <span class="muted">(위치 없음)</span>`}</td></tr>`).join("")}
      </tbody></table>`;
    scrollRowIntoView($("#v-side"), $("#v-side tr.sel"));
    if (cell) kpPanel($("#v-kp"), d.id, cell, async () => { await loadCells(); drawSide(); }, { image: false });
  };
  // 그 칸의 최종 키 (공통 키로 정했으면 공통 키). 서명 칸은 이름·서명·도장 키마다 따로
  const finalKey = raw => (view.cells[raw]?.keys || []).find(k => k.raw === raw)?.key || raw;
  const select = i => {
    view.sel = i;
    const f = view.label.fields[i];
    if (f && (f.page || 0) !== view.page) view.page = f.page || 0;
    draw(true);
  };
  const go = async (force = false) => {
    const o = readOptions(true);
    $("#o-stat").textContent = "렌더링 중…";
    try {
      const t = performance.now();
      view.label = await renderOne(d.id, o, force);
      await cellsReady;
      if (!$("#o-stat")) return;   // 렌더링하는 사이 다른 화면으로 넘어감
      view.page = Math.min(view.page, view.label.pages.length - 1);
      view.sel = -1;
      $("#o-stat").textContent = `seed ${o.seed} · ${((performance.now() - t) / 1000).toFixed(1)}초`;
      draw();
    } catch (e) {
      $("#o-stat").innerHTML = `<span class="err">${esc(e.message)}</span>`;
    }
  };
  const markIssue = async (i, p) => {
    const L = view.label, f = L.fields[i];
    const s = 18 * (p.k || 1);
    const bbox = f && f.bbox && (f.page || 0) === view.page ? f.bbox : [p.x - s, p.y - s, p.x + s, p.y + s];
    const note = prompt(`문제 메모${f ? ` (${f.key})` : ""}`, "");
    if (note === null) return;
    const o = state.opts;
    try {
      await api(`/api/forms/${encodeURIComponent(d.id)}/issues`, {
        seed: L.seed, page: view.page, bbox, key: f ? f.key : null, note, heavy: o.heavy, special: o.special, condition: L.condition,
      });
      const fresh = await formDetail(d.id, true);
      d.issues = fresh.issues;
      toast("문제를 남겼습니다 (검수 탭에서 봅니다)");
      draw();
    } catch (e) { toast(e.message, true); }
  };
  $("#o-go").onclick = () => go();
  $("#o-force").onclick = () => go(true);
  $("#o-prev").onclick = () => { $("#o-seed").value = Math.max(0, +$("#o-seed").value - 1); go(); };
  $("#o-next").onclick = () => { $("#o-seed").value = +$("#o-seed").value + 1; go(); };
  $("#o-zoom").onclick = () => { view.zoom = !view.zoom; $("#o-zoom").textContent = view.zoom ? "폭에 맞춤" : "원래 크기"; draw(); };
  $("#o-issue").onclick = () => {
    view.issueMode = !view.issueMode;
    $("#o-issue").classList.toggle("primary", view.issueMode);
    $("#o-issue").textContent = view.issueMode ? "문제 표시 중 (끄기)" : "문제 표시";
  };
  $("#v-pages").onclick = e => { const p = e.target.dataset.p; if (p !== undefined) { view.page = +p; draw(); } };
  const stage = bindStage($("#v-stage"), () => view.label, () => view.page, (i, p) => {
    if (view.issueMode) return markIssue(i, p);
    view.sel = i; draw();
  });
  $("#v-side").onclick = e => { const i = e.target.closest("tr")?.dataset.i; if (i !== undefined) select(+i); };
  $("#v-side").onmouseover = e => {   // 표에 마우스를 올리면 그림에서 그 박스를 강조
    const i = e.target.closest("tr")?.dataset.i;
    if (i !== undefined && (view.label.fields[+i].page || 0) === view.page) stage.hover(+i);
  };
  $("#v-side").onmouseleave = () => stage.hover(-1);
  state.keyHandler = e => {
    const L = view.label;
    if (!L || e.target.closest("input, select, textarea")) return;
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      const n = L.fields.length;
      select(view.sel < 0 ? (e.key === "ArrowDown" ? 0 : n - 1) : (view.sel + (e.key === "ArrowDown" ? 1 : -1) + n) % n);
    } else if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
      const p = view.page + (e.key === "ArrowRight" ? 1 : -1);
      if (p >= 0 && p < L.pages.length) { e.preventDefault(); view.page = p; view.sel = -1; draw(); }
    } else if (e.key === "Escape") {
      view.sel = -1; draw();
    }
  };
  bindLayers(draw);
  // 검수 탭에서 문제를 눌러 왔으면 그 seed·쪽으로
  const jump = state.jumpIssue && state.jumpIssue.doc === d.id ? state.jumpIssue : null;
  state.jumpIssue = null;
  if (jump) {
    $("#o-seed").value = jump.seed ?? 0;
    if (jump.heavy) $("#o-heavy").value = jump.heavy;
    if (jump.special) $("#o-special").value = jump.special;
    if (jump.condition) $("#o-cond").value = jump.condition;
    view.page = jump.page || 0;
  }
  go();
}

// 예시 탭 -----------------------------------------------------------------
function tabExamples(d) {
  const start = store.get("ex.start", 0), count = store.get("ex.count", 8);
  $("#tab").innerHTML = `
    <div class="bar">
      <label>seed <input type="number" id="ex-start" value="${start}" min="0">부터</label>
      <label><input type="number" id="ex-count" value="${count}" min="1" max="48"> 장</label>
      ${optionBar(false)}
      <button class="primary" id="ex-go">만들기</button><span class="muted" id="ex-stat"></span>
    </div>
    <div class="bar">${layerBar()}</div>
    <div class="sub">같은 seed 는 늘 같은 고객·같은 값입니다. 카드를 누르면 그 seed 로 미리보기를 엽니다.</div>
    <div class="grid" id="ex-grid"></div>`;
  let labels = [];
  const drawCards = () => {
    $("#ex-grid").innerHTML = labels.map((L, k) => L && !L.error ? `
      <div class="card" data-seed="${L.seed}">
        <div class="stage">${stageHTML(L, 0, -1)}</div>
        <div class="cap"><span>seed ${L.seed}</span><span class="muted">${L.pages.length}쪽 · 항목 ${L.fields.length}${L.overflow ? " · <b class=kr>넘침</b>" : ""}</span></div>
      </div>` : `<div class="card"><div class="wait">${L && L.error ? `<span class="err">${esc(L.error)}</span>` : `seed ${k + +$("#ex-start").value}<br>만드는 중…`}</div></div>`).join("");
  };
  const go = async () => {
    const s = Math.max(0, parseInt($("#ex-start").value || "0", 10)), n = Math.min(48, Math.max(1, parseInt($("#ex-count").value || "8", 10)));
    store.set("ex.start", s); store.set("ex.count", n);
    const o = readOptions(false);
    labels = new Array(n).fill(null);
    drawCards();
    $("#ex-go").disabled = true;
    for (let k = 0; k < n; k++) {   // 렌더러가 하나라 차례로 만든다. 다 된 것부터 보인다.
      $("#ex-stat").textContent = `${k + 1}/${n}`;
      try { labels[k] = await renderOne(d.id, { ...o, seed: s + k }); } catch (e) { labels[k] = { error: e.message }; }
      drawCards();
    }
    $("#ex-stat").textContent = `${n}장`;
    $("#ex-go").disabled = false;
  };
  $("#ex-go").onclick = go;
  $("#ex-grid").onclick = e => {
    const seed = e.target.closest(".card")?.dataset.seed;
    if (seed === undefined) return;
    state.opts.seed = +seed; store.set("opts", state.opts);
    location.hash = `#/forms/${encodeURIComponent(d.id)}/preview`;
  };
  bindLayers(drawCards);
  go();
}

// 검수 탭: 자동 검사(경고만), 검수 완료 버튼, 학습/평가 배정, 메모, 문제 표시 목록 --------------------
async function tabReview(d) {
  const issues = d.issues || [];
  $("#tab").innerHTML = `
    <div class="viewer" style="grid-template-columns:minmax(0,1fr) 380px">
      <div>
        <h2>자동 검사 <span class="muted" style="font-weight:400;font-size:13px">경고만 보여 주고 검수를 막지 않습니다</span></h2>
        <div id="rv-checks" class="panel"><span class="spin">검사 중… (seed 0 으로 한 번 렌더링합니다)</span></div>
        <h2>문제 표시 (${issues.length})</h2>
        <div class="sub">미리보기에서 <b>문제 표시</b>를 켜고 그림을 눌러 남깁니다. 줄을 누르면 그 seed·쪽을 엽니다.</div>
        <div id="rv-issues"></div>
      </div>
      <div class="panel">
        <h2 style="margin-top:0">검수</h2>
        <div style="margin-bottom:8px">${REVIEW_TAG[d.review_state]}
          ${d.reviewed ? `<div class="muted">${esc(d.reviewed.by)} · ${esc(d.reviewed.at)}</div>` : ""}</div>
        <div class="bar">
          <button class="primary" id="rv-done">${d.review_state === "done" ? "다시 검수 완료" : "검수 완료"}</button>
          ${d.reviewed ? `<button id="rv-undo">검수 취소</button>` : ""}
        </div>
        <h2>배정</h2>
        <select id="rv-split">${Object.entries(SPLIT_NAME).map(([k, n]) =>
          `<option value="${k}" ${d.split === k ? "selected" : ""}>${n}</option>`).join("")}</select>
        <div class="muted" style="font-size:12px;margin-top:4px">평가 전용: 학습 데이터(<span class="mono">--split train</span>)를 만들 때 이 서식을 뺍니다.</div>
        <h2>메모</h2>
        <textarea id="rv-note" rows="4" style="width:100%">${esc(d.note || "")}</textarea>
        <div class="bar"><button id="rv-save">배정·메모 저장</button></div>
      </div>
    </div>`;
  const drawIssues = list => {
    $("#rv-issues").innerHTML = list.length ? table(list, [
      ["id", "ID"], ["status", "상태", x => x.status === "open" ? `<span class="tag warn">열림</span>` : `<span class="tag ok">끝남</span>`],
      ["seed", "seed"], ["page", "쪽", x => (x.page || 0) + 1], ["key", "키", x => `<span class="mono">${esc(x.key || "")}</span>`],
      ["note", "메모"], ["at", "남긴 때"],
      ["act", "", x => `<button data-done="${x.id}">${x.status === "open" ? "끝남으로" : "다시 열기"}</button> <button data-del="${x.id}">지우기</button>`],
    ], x => `class="click" data-open="${x.id}"`) : `<p class="muted">문제 표시가 없습니다.</p>`;
  };
  drawIssues(issues);
  $("#rv-issues").onclick = async e => {
    const done = e.target.dataset.done, del = e.target.dataset.del;
    try {
      if (done) {
        const it = issues.find(x => x.id === done);
        await api(`/api/forms/${encodeURIComponent(d.id)}/issues/${done}`, { status: it.status === "open" ? "done" : "open" }, "PATCH");
      } else if (del) {
        if (!confirm("이 문제 표시를 지울까요?")) return;
        await api(`/api/forms/${encodeURIComponent(d.id)}/issues/${del}`, { delete: true }, "PATCH");
      } else {
        const id = e.target.closest("tr")?.dataset.open;
        const it = issues.find(x => x.id === id);
        if (!it) return;
        state.jumpIssue = { doc: d.id, ...it };
        location.hash = `#/forms/${encodeURIComponent(d.id)}/preview`;
        return;
      }
      state.forms = null;
      viewForm(d.id, "review");
    } catch (err) { toast(err.message, true); }
  };
  const setReview = async done => {
    try {
      await api(`/api/forms/${encodeURIComponent(d.id)}/review`, { done });
      state.forms = null;
      toast(done ? "검수 완료로 표시했습니다" : "검수를 취소했습니다");
      viewForm(d.id, "review");
    } catch (e) { toast(e.message, true); }
  };
  $("#rv-done").onclick = () => setReview(true);
  if ($("#rv-undo")) $("#rv-undo").onclick = () => setReview(false);
  $("#rv-save").onclick = async () => {
    try {
      await api(`/api/forms/${encodeURIComponent(d.id)}/meta`, { split: $("#rv-split").value, note: $("#rv-note").value });
      state.forms = null;
      toast("저장했습니다");
      viewForm(d.id, "review");
    } catch (e) { toast(e.message, true); }
  };
  try {
    const r = await api(`/api/forms/${encodeURIComponent(d.id)}/checks`);
    const icon = { warn: "⚠", info: "ℹ" };
    $("#rv-checks").innerHTML = r.checks.length ? `<ul class="checks">${r.checks.map(c =>
      `<li class="${c.level}">${icon[c.level] || ""} ${esc(c.text)}${c.id && d.kind === "overlay" ?
        ` <a href="#/forms/${encodeURIComponent(d.id)}/edit" data-goto="${esc(c.id)}">영역 편집에서 보기</a>` : ""}</li>`).join("")}</ul>`
      : `<p class="muted">경고가 없습니다.${r.rendered ? "" : " (브라우저가 없어 한글 키 검사는 건너뜀)"}</p>`;
    $("#rv-checks").onclick = e => { const g = e.target.dataset.goto; if (g) state.editorFocus = { doc: d.id, id: g }; };
  } catch (e) { $("#rv-checks").innerHTML = `<span class="err">${esc(e.message)}</span>`; }
}

// 키 탭: 칸마다 이름표 · 누구의 · 무엇 · 키 (키 사전 keys.js 의 cellsView)
function tabKeys(d) {
  $("#tab").innerHTML = `<div class="sub">칸마다 키가 하나 있습니다. 칸이 <b>누구의 · 무엇</b>인지 정하면, 그 둘이 공통 키일 때 공통 키로 묻고 답합니다.
    나머지는 문서별 키(서식의 키 그대로)입니다. 미리보기에서 칸을 눌러도 같은 것을 정합니다.</div><div id="k-cells"></div>`;
  return cellsView($("#k-cells"), { form: d.id });
}

// 예전 키 목록 (30번 렌더링해 모은 키·채움률) -----------------------------------
function tabKeysSampled(d) {
  $("#tab").innerHTML = `
    <div class="sub">서식마다 고객 30명으로 렌더링해 모은 키입니다 (<span class="mono">guide/fields/fields.json</span>).
      채움률은 30번 중 그 키가 나온 비율, 예시가 비어 있으면 값이 한 번도 안 채워진 칸입니다.
      <span class="kr">주황색</span>은 한글 키(영어 표준 키로 바꿀 대상)입니다.</div>
    <div class="bar"><input type="text" id="k-q" placeholder="키·항목명 검색" style="width:240px"></div>
    <div id="k-table"></div>`;
  const draw = () => {
    const q = $("#k-q").value.trim().toLowerCase();
    const rows = d.keys.filter(k => !q || k.key.toLowerCase().includes(q) || (k.label || "").toLowerCase().includes(q));
    $("#k-table").innerHTML = rows.length ? `<table><thead><tr><th>키</th><th>항목명</th><th>타입</th><th class="num">채움률</th><th>예시</th></tr></thead>
      <tbody>${rows.map(k => `<tr><td class="mono ${/[^\x00-\x7f]/.test(k.key) ? "kr" : ""}">${esc(k.key)}</td>
        <td>${esc(k.label ?? "")}</td><td>${esc(k.type)}</td><td class="num">${Math.round((k.fill_rate ?? 0) * 100)}%</td>
        <td>${k.example ? esc(k.example) : `<span class="muted">(값 없음)</span>`}</td></tr>`).join("")}</tbody></table>`
      : `<p class="muted">키 목록이 없습니다. <span class="mono">python docgen/scripts/build_schema.py</span>로 만듭니다.</p>`;
  };
  $("#k-q").oninput = draw;
  draw();
}

function tabFiles(d) {
  $("#tab").innerHTML = `
    <div class="sub">이 서식의 결과를 정하는 파일입니다 (저장소 기준 경로). 영역 편집기·html 편집기에서 고친 것도 이 파일들에 저장됩니다.</div>
    <table><thead><tr><th>역할</th><th>경로</th></tr></thead><tbody>${d.files.map(f =>
      `<tr><td>${esc(f.role)}</td><td class="mono">${esc(f.path)}</td></tr>`).join("")}</tbody></table>
    ${d.script ? `<h3>생성 스크립트 <span class="mono muted">${esc(d.script.path)}</span></h3>
      <div class="sub">칸 목록이 값을 채운 뒤 <span class="mono">adjust(d, p, rng)</span> 가 값을 다듬습니다 (칸끼리 순서·합계·조건·표기).
      그림을 그릴 때마다 실행되는 코드이니 내용을 읽고 확인하세요. 고치는 것은 파일로 (고치면 재검수 필요로 바뀝니다).</div>
      <pre class="mono" style="max-height:480px;overflow:auto">${esc(d.script.source)}</pre>` : ""}`;
}
