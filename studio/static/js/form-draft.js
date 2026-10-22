// 서식 초안 (외주 작업): 예시 서식 이미지 → VLM 이 같은 모양의 html 서식 → 키 사전을 참고해 칸마다 추출 키·항목명·설명 추천.
// 작업자는 키를 고쳐 저장(다시 그려 검사)하고, 검사를 통과하면 서식으로 등록하거나 키 목록을 내려받는다.
// 서버: studio/api_form_draft.py, studio/form_draft.py. 모델 연결은 실문서 벤치마크의 'OCR·모델 연결' 설정을 같이 쓴다.
"use strict";

addRoute(/^#\/form-draft$/, () => viewFormDrafts(), "form-draft");
addRoute(/^#\/form-draft\/([^/]+)$/, id => viewFormDraft(decodeURIComponent(id)), "form-draft");

const FD_KIND = { field: "글자", check: "체크", seal: "도장", sign: "서명" };
let fdCatalog = null;
async function fdLoadCatalog() {
  if (!fdCatalog) {
    const r = await api("/api/form-draft/catalog");
    fdCatalog = { rows: r.keys, by: Object.fromEntries(r.keys.map(k => [k.key, k])) };
  }
  return fdCatalog;
}
const fdStatus = s => `<span class="tag ${s === "done" ? "ok" : s === "running" ? "" : "warn"}">${JOB_STATUS[s] || s || "-"}</span>`;

async function viewFormDrafts() {
  const [r, groups] = await Promise.all([api("/api/form-draft"), api("/api/groups").catch(() => [])]);
  const pv = r.providers;
  main().innerHTML = `<h1>서식 초안</h1>
    <div class="sub">예시 서식 이미지를 올리면 VLM 이 이미지와 같은 모양의 html 서식을 만들고, 키 사전(공통 키·문서별 키와 항목 설명)을 참고해 칸마다
      추출 키·항목명·설명을 추천합니다. 추천을 고쳐 저장하면 다시 그려 검사하고, 검사를 통과하면 서식으로 등록합니다.</div>
    ${pv.length ? "" : `<div class="panel warnbox">모델 연결이 없습니다. <a href="#/real-bench/connections">OCR·모델 연결</a>에서 vLLM 주소(…/v1)와 모델 이름을 등록하세요.</div>`}
    <form class="panel" id="fd-new" style="margin-bottom:10px">
      <div class="bar">
        <label>예시 이미지 <input type="file" id="fd-file" accept=".png,.jpg,.jpeg,.tif,.tiff,.bmp,.webp,.pdf" required></label>
        <label>모델 <select id="fd-prov">${pv.map(p => `<option value="${esc(p.name)}">${esc(p.name)} · ${esc(p.model || "")}${p.external ? " (외부)" : ""}</option>`).join("")}</select></label>
      </div>
      <div class="bar">
        <label>서식 이름 <input type="text" id="fd-name" placeholder="예: 예금거래신청서 (비우면 모델이 제목을 읽음)" style="width:300px"></label>
        <label>그룹 <select id="fd-group">${groups.map(g => `<option value="${esc(g.id)}">${esc(g.name)}</option>`).join("") || `<option>finance</option>`}</select></label>
        <label title="그려서 원본과 견주며 고치는 횟수. 2회 연속 나아지지 않으면 일찍 멈춥니다">다듬기 <input type="number" id="fd-rounds" min="0" max="8" value="3" style="width:56px">회</label>
        <label title="개인 값이 들어 있는 실서류면 내부 연결로만 보내고, 등록할 때 private_forms_dir 에 둡니다"><input type="checkbox" id="fd-real" checked> 실서류 (개인 값 포함)</label>
      </div>
      <div class="bar"><input type="text" id="fd-comment" placeholder="모델에 덧붙일 말 (선택, 예: 2쪽짜리 서식의 1쪽입니다)" style="flex:1">
        <button class="primary" id="fd-go" ${pv.length ? "" : "disabled"}>만들기</button></div>
      <div class="muted">PDF 는 첫 쪽만 씁니다. 뒤에서 모델을 여러 번 부릅니다: 초안 1번, 다듬기마다 1번 (그려서 원본과 견준 그림·위치 차이를 보내 고치게 함), 키 추천 1번.
        큰 모델은 몇 분 걸립니다 (연결의 최대 응답 길이·시간 제한을 넉넉히: 16000 토큰 · 900초 정도).</div>
    </form>
    ${r.drafts.length ? table(r.drafts, [["id", "초안", d => `<a href="#/form-draft/${q(d.id)}">${esc(d.name || d.id)}</a> <span class="muted mono" style="font-size:11px">${esc(d.id)}</span>`],
      ["provider", "모델", d => esc(d.provider)], ["by", "올린 사람", d => esc(d.by || "")],
      ["status", "상태", d => fdStatus(d.status)], ["slots", "칸", d => d.slots || "-", true],
      ["edited", "키", d => d.edited ? `<span class="tag ok">작업자 수정</span>` : d.slots ? `<span class="tag">모델 추천</span>` : ""],
      ["result", "검사", d => d.result ? (d.result.ok ? `<span class="tag ok">통과</span>` : `<span class="tag warn">문제 ${d.result.errors.length}</span>`) : "-"],
      ["approved", "등록", d => d.approved ? `<a href="#/forms/${q(d.approved.as)}/html">${esc(d.approved.as)}</a>` : ""], ["created", "만든 때"]])
      : `<p class="muted">초안이 없습니다.</p>`}`;
  $("#fd-new").onsubmit = async e => {
    e.preventDefault();
    const file = $("#fd-file").files[0];
    if (!file) return toast("이미지를 고르세요", true);
    const p = pv.find(x => x.name === $("#fd-prov").value) || {};
    if (p.external && $("#fd-real").checked) return toast("실서류는 외부 연결로 보낼 수 없습니다", true);
    $("#fd-go").disabled = true;
    try {
      const res = await apiUpload("/api/form-draft", file, { provider: p.name, name: $("#fd-name").value.trim(), group: $("#fd-group").value,
        comment: $("#fd-comment").value, real_data: $("#fd-real").checked, rounds: $("#fd-rounds").value || 3 });
      location.hash = `#/form-draft/${q(res.id)}`;
    } catch (err) { toast(err.message, true); $("#fd-go").disabled = false; }
  };
}

async function viewFormDraft(id) {
  const [a, cat] = await Promise.all([api(`/api/form-draft/${q(id)}`), fdLoadCatalog()]);
  const run = a.run || {};
  const file = p => `/api/analyzer/${q(id)}/file?path=${q(p)}`;
  const res = a.result, draft = a.draft;
  const renders = res && res.renders ? Object.entries(res.renders) : [];
  const running = run.status === "running";
  const keys = a.keys.map(k => ({ ...k }));
  main().innerHTML = `
    <div class="muted"><a href="#/form-draft">서식 초안</a></div>
    <div class="bar"><h1>${esc(a.target.name || (draft && draft.name) || "서식 초안")} <span class="mono muted" style="font-size:13px">${esc(a.id)}</span></h1>
      <span style="flex:1"></span>${fdStatus(run.status)}<span class="tag">${esc(a.provider)}</span>
      ${run.id ? `<a href="#/jobs/${q(run.id)}">실행 로그</a>` : ""}<a href="#/jobs/analyzer/${q(a.id)}">분석기 작업으로</a></div>
    ${running ? `<div class="panel"><p class="spin">${run.stage === "finalizing" ? "만든 서식을 그려 검사하는 중…"
      : esc((run.log_tail || "").trim().split("\n").filter(Boolean).slice(-1)[0] || "모델이 일하는 중…")}</p></div>` : ""}
    ${run.status === "failed" || run.status === "interrupted" ? `<div class="panel warnbox"><b>실패</b><pre class="ans">${esc(run.error || (run.log_tail || "").slice(-1500))}</pre></div>` : ""}
    ${a.conflict ? `<div class="panel warnbox">추천 키끼리 부딪혀 칸 ID 그대로 그렸습니다: ${esc(a.conflict)}. 아래에서 키를 고쳐 저장하세요.</div>` : ""}
    <div class="rc-grid">
      <div class="panel"><b>예시 이미지</b><div class="stage"><img src="${file("input/source.png")}" alt="" style="max-width:100%"></div></div>
      <div class="panel"><b>만든 서식 ${res ? (res.ok ? `<span class="tag ok">검사 통과</span>` : `<span class="tag warn">문제 ${res.errors.length}</span>`) : ""}</b>
        ${res && !res.ok ? `<ul class="checks">${res.errors.map(e => `<li class="warn">⚠ ${esc(e)}</li>`).join("")}</ul>` : ""}
        ${renders.length ? `<div class="bar">${renders.map(([rows], i) => `<label><input type="radio" name="fd-rows" value="${i}" ${i === 0 ? "checked" : ""}> 행 ${rows === "max" ? "최대" : "최소"}</label>`).join("")}</div>` : ""}
        ${renders.map(([rows, info], i) => `<div data-fd-render="${i}" ${i ? "hidden" : ""}>
          <div class="muted">${info.pages}쪽 · 항목 ${info.fields} · 빈 값 ${info.empty}${info.checks.length ? ` · <span class="kr">경고 ${info.checks.length}</span>` : ""}</div>
          ${info.checks.length ? `<ul class="checks">${info.checks.map(c => `<li class="warn">${esc(c.text)}</li>`).join("")}</ul>` : ""}
          ${info.images.map(p => `<div class="stage"><img src="${file(p)}" alt="" style="max-width:100%"></div>`).join("")}</div>`).join("")}
        ${!renders.length && !running ? `<p class="muted">그린 결과가 없습니다.</p>` : ""}
      </div>
    </div>
    ${a.rounds.length ? `<div class="panel" style="margin-top:10px"><div class="bar"><b>다듬기</b>
        <span class="muted">점수는 원본과 선·글자가 겹치는 정도 (0~100). 가장 좋은 회차가 기본으로 쓰입니다.</span></div>
      <div style="overflow-x:auto"><table><thead><tr><th>회차</th><th>점수</th><th>결과</th><th>무엇을 고쳤나</th><th>비교 그림</th><th></th></tr></thead><tbody>
      ${a.rounds.map(h => `<tr><td class="mono">${h.n === 0 ? "초안" : h.n}</td>
        <td class="num">${h.score ?? "-"}${h.pages > 1 ? ` <span class="tag warn">${h.pages}쪽</span>` : ""}</td>
        <td>${h.n === a.using_round ? `<span class="tag ok">사용 중</span>` : ""}${h.n === a.best_round ? ` <span class="tag">최고</span>` : ""}
          ${h.n && !h.kept ? `<span class="tag warn">${h.score == null ? "멈춤" : "되돌림"}</span>` : ""}</td>
        <td class="muted" style="font-size:12px;white-space:pre-wrap;max-width:420px">${esc(h.note || "")}</td>
        <td>${h.has_image ? `<a href="${file(`draft/rounds/${h.n}/compare.png`)}" target="_blank" rel="noopener"><img src="${file(`draft/rounds/${h.n}/compare.png`)}" alt="" style="width:210px;border:1px solid var(--line, #ccc)"></a>` : ""}</td>
        <td>${h.has_image && h.n !== a.using_round && !running ? `<button data-fd-round="${h.n}">이 회차로</button>` : ""}</td></tr>`).join("")}
      </tbody></table></div></div>` : ""}
    ${draft ? `<div class="panel" style="margin-top:10px">
      <div class="bar"><b>추출 키</b><span class="muted">칸 ${draft.slots.length}개 · ${a.edited_by && a.edited_by !== "model" ? `${esc(a.edited_by)} 수정 ${esc(a.edited_at || "")}` : "모델 추천"}</span>
        <span style="flex:1"></span><button id="fd-reset" ${a.suggested.length ? "" : "disabled"}>모델 추천으로 되돌리기</button>
        <a href="/api/form-draft/${q(id)}/export" download="${esc(id)}_keys.json"><button type="button">키 목록 내려받기</button></a>
        <button class="primary" id="fd-save">저장하고 다시 그리기</button></div>
      <div class="muted">키는 '누구의 무엇'입니다. 기존 키(공통·문서별)와 뜻이 정확히 맞으면 그대로 쓰고, 아니면 같은 규칙으로 새 키를 짓습니다.
        반복 표 칸은 <span class="mono">목록.*.속성</span>, 도장·서명은 <span class="mono">seal.당사자</span> · <span class="mono">sign.당사자</span>.</div>
      <datalist id="fd-keys">${cat.rows.map(k => `<option value="${esc(k.key)}">${esc(k.meaning)}</option>`).join("")}</datalist>
      <div style="overflow-x:auto"><table class="fd-keys"><thead><tr><th>칸</th><th>문서 항목명 · 구역</th><th>종류</th><th>키</th><th>구분</th><th>항목명 (누구의 무엇)</th><th>항목 설명</th><th>타입</th><th>추천 이유</th></tr></thead>
        <tbody id="fd-rows"></tbody></table></div>
    </div>
    <details class="panel"><summary>만든 html 템플릿</summary><pre class="ans mono">${esc(a.output["template.html.j2"] || "")}</pre></details>
    <details class="panel"><summary>모델 답 원문</summary>${Object.entries(a.answers).map(([n, t]) => `<b>${n === "html" ? "1단계 html" : "2단계 키"}</b><pre class="ans mono">${esc(t)}</pre>`).join("")}</details>
    <div class="rc-grid" style="margin-top:10px">
      <div class="panel"><b>서식으로 등록</b>
        ${a.review.approved ? `<div><span class="tag ok">등록함</span> <a href="#/forms/${q(a.review.approved.as)}/html">${esc(a.review.approved.as)}</a> · ${esc(a.review.approved.by)} ${esc(a.review.approved.at)}</div>`
          : `<div class="bar"><label>서식 ID <input type="text" id="fd-id" placeholder="영어 소문자·숫자·밑줄" style="width:200px"></label>
            <label>이름 <input type="text" id="fd-rname" value="${esc(a.target.name || draft.name || "")}"></label>
            <button class="primary" id="fd-register" ${res && res.ok ? "" : "disabled"}>등록</button></div>
            <div class="muted">${a.source.real_data ? "실서류 이미지라 private_forms_dir 에 만듭니다." : "docgen/templates/copies/&lt;ID&gt;/ 에 만듭니다."} 등록 뒤 ① 서식의 html 편집기에서 모양을 더 고칠 수 있습니다.</div>`}
      </div>
    </div>` : ""}
    ${running ? "" : `<div class="panel" style="margin-top:10px"><b>다시 만들기</b>
      <div class="muted">같은 이미지로 처음부터 다시 맡깁니다 (새 초안).</div>
      <div class="bar"><input type="text" id="fd-again" placeholder="고칠 점 (예: 표의 열 너비를 이미지처럼, 하단 동의 문구 빠짐)" style="flex:1"><button id="fd-rerun">다시 만들기</button></div>
    </div>`}`;
  $$('[name="fd-rows"]').forEach(r => r.onchange = () => $$("[data-fd-render]").forEach(el => el.hidden = el.dataset.fdRender !== r.value));
  if (running) setTimeout(() => { if (location.hash === `#/form-draft/${q(id)}`) viewFormDraft(id); }, 3000);
  $$("[data-fd-round]").forEach(b => b.onclick = async () => {
    b.disabled = true;
    try { const r = await api(`/api/form-draft/${q(id)}/use-round`, { n: +b.dataset.fdRound }); toast(r.ok ? "그 회차로 바꿨습니다 · 검사 통과" : "그 회차로 바꿨습니다 · 검사에 문제", !r.ok); viewFormDraft(id); }
    catch (e) { toast(e.message, true); b.disabled = false; }
  });
  if ($("#fd-rerun")) $("#fd-rerun").onclick = async () => {
    try { const r = await api(`/api/form-draft/${q(id)}/rerun`, { comment: $("#fd-again").value }); location.hash = `#/form-draft/${q(r.id)}`; }
    catch (e) { toast(e.message, true); }
  };
  if (!draft) return;

  const slots = Object.fromEntries(draft.slots.map(s => [s.id, s]));
  const kindTag = k => {
    const known = cat.by[k.key];
    return known ? `<span class="tag ok" title="${esc(known.meaning)}">기존 ${known.scope === "common" ? "공통" : "문서별"}</span>` : `<span class="tag warn">새 키</span>`;
  };
  const drawRows = () => {
    $("#fd-rows").innerHTML = keys.map((k, i) => {
      const s = slots[k.slot] || {};
      return `<tr data-i="${i}">
        <td class="mono">${esc(k.slot)}</td>
        <td><b>${esc(s.label)}</b>${s.section ? `<div class="muted">${esc(s.section)}</div>` : ""}${s.list ? `<div class="muted mono">반복: ${esc(s.list)}</div>` : ""}</td>
        <td>${FD_KIND[s.kind] || esc(s.kind)}${s.choices ? `<div class="muted">${s.choices.map(esc).join(" / ")}</div>` : ""}</td>
        <td><input type="text" class="mono" data-f="key" list="fd-keys" value="${esc(k.key)}" style="width:210px">${k.missing ? `<div class="kr">모델이 빠뜨림</div>` : ""}</td>
        <td data-kind>${kindTag(k)}</td>
        <td><input type="text" data-f="label" value="${esc(k.label)}" style="width:150px"></td>
        <td><input type="text" data-f="description" value="${esc(k.description)}" style="width:240px"></td>
        <td><select data-f="type">${["text", "amount", "number", "date", "checkbox", "seal", "signature"].map(t => `<option ${t === k.type ? "selected" : ""}>${t}</option>`).join("")}</select></td>
        <td class="muted" style="font-size:12px;min-width:200px;max-width:320px">${esc(k.reason || "")}</td></tr>`;
    }).join("");
    $$("#fd-rows input, #fd-rows select").forEach(el => el.oninput = el.onchange = () => {
      const tr = el.closest("tr"), k = keys[+tr.dataset.i];
      k[el.dataset.f] = el.value.trim();
      if (el.dataset.f === "key") {
        const known = cat.by[k.key];
        if (known) {   // 기존 키를 고르면 사전의 뜻·타입으로 빈 칸을 채운다
          if (!k.description) { k.description = known.meaning; $('[data-f="description"]', tr).value = known.meaning; }
          if (known.type) { k.type = known.type; $('[data-f="type"]', tr).value = known.type; }
        }
        $("[data-kind]", tr).innerHTML = kindTag(k);
      }
    });
  };
  drawRows();
  $("#fd-reset").onclick = () => { keys.splice(0, keys.length, ...a.suggested.map(k => ({ ...k }))); drawRows(); toast("모델 추천으로 되돌렸습니다 (저장 전)"); };
  $("#fd-save").onclick = async () => {
    $("#fd-save").disabled = true;
    try {
      const r = await api(`/api/form-draft/${q(id)}/keys`, { keys }, "PUT");
      toast(r.ok ? "저장했습니다 · 검사 통과" : `저장했습니다 · 문제 ${r.errors.length}`, !r.ok);
      viewFormDraft(id);
    } catch (e) { toast(e.message, true); $("#fd-save").disabled = false; }
  };
  if ($("#fd-register")) $("#fd-register").onclick = async () => {
    try {
      const r = await api(`/api/form-draft/${q(id)}/register`, { form_id: $("#fd-id").value.trim(), name: $("#fd-rname").value.trim() });
      toast(`등록했습니다: ${r.as}`); state.forms = null; viewFormDraft(id);
    } catch (e) { toast(e.message, true); }
  };
}
