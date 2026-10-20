// ⑤ 검수 › 라벨 검수: 결과 폴더(또는 autolabel)의 추론 결과를 문서마다 고쳐 실서류 정답을 만든다.
// 포맷 → 키 대응 → 문서(의심 먼저) → 값·위치 고치기·확인 → 표준 라벨 v1 폴더 → ④ 라벨 있는 데이터로 데이터셋.
// 서버: studio/api_review.py, studio/label_review.py
"use strict";

addRoute(/^#\/labels\/([^/]+)$/, b => viewLabels(decodeURIComponent(b)), "review");
addRoute(/^#\/labels\/([^/]+)\/keymap\/([^/]+)$/, (b, f) => viewKeymap(decodeURIComponent(b), decodeURIComponent(f)), "review");
addRoute(/^#\/labels\/([^/]+)\/format\/([^/]+)$/, (b, f) => viewLabelDocs(decodeURIComponent(b), decodeURIComponent(f)), "review");
addRoute(/^#\/labels\/([^/]+)\/key\/([^/]+)\/(.+)$/, (b, f, k) => viewKeyView(decodeURIComponent(b), decodeURIComponent(f), decodeURIComponent(k)), "review");
addRoute(/^#\/labels\/([^/]+)\/doc\/([^/]+)\/(.+)$/, (b, f, d) => viewLabelDoc(decodeURIComponent(b), decodeURIComponent(f), decodeURIComponent(d)), "review");
addRoute(/^#\/labels\/([^/]+)\/bundles$/, b => viewLabelBundles(decodeURIComponent(b)), "review");

const LB_STATE = { auto: ["자동", ""], edited: ["수정", "st-edited"], confirmed: ["확인", "ok"], added: ["추가", "st-added"], deleted: ["삭제", "st-dropped"] };
const lbHead = (b, extra = "") => `<div class="muted"><a href="#/review">검수</a> › <a href="#/labels/${q(b)}">라벨 검수 · ${esc(b)}</a>${extra}</div>`;

async function viewLabels(name) {
  const [o, sc, pv] = await Promise.all([api(`/api/labels/${q(name)}`), api(`/api/labels/${q(name)}/score`).catch(() => null),
    api("/api/providers").catch(() => ({ providers: [] }))]);
  const intProv = pv.providers.filter(p => p.kind === "openai" && !p.external);
  const tk = sc && sc.tasks ? Object.entries(sc.tasks) : [];
  main().innerHTML = lbHead(name) + `
    <h1>라벨 검수 · ${esc(name)} ${o.real_data ? `<span class="tag warn">실서류</span>` : ""}</h1>
    <div class="sub">포맷마다 서식을 정하고(④ 포맷 › 기존 서식과 같음 / 템플릿으로) 키를 맞춘 뒤 문서마다 값·위치를 고쳐 확인합니다.
      확인한 문서는 표준 라벨 v1 폴더 <span class="mono">${esc(o.root)}</span>에 쌓이고, 그 폴더가 그대로 ④ 라벨 있는 데이터의 입력입니다.
      ${o.model ? `원래 추론 모델: <b>${esc(o.model)}</b>.` : ""}</div>
    ${o.real_root_set ? "" : `<div class="panel warnbox">설정에 <span class="mono">real_data_dir</span> 이 없어 검수 결과를 작업 공간에 둡니다.</div>`}
    ${table(o.formats, [["name", "포맷", f => `${esc(f.name)} <span class="muted">${esc(f.id)}</span>`],
      ["doc_type", "서식", f => f.doc_type ? `<a href="#/forms/${q(f.doc_type)}">${esc(f.doc_type)}</a>` : `<a href="#/import/${q(name)}/f/${q(f.id)}"><span class="tag warn">정하기</span></a>`],
      ["documents", "문서", null, true], ["with_pred", "추론 있음", null, true], ["done", "확인", f => `${f.done}/${f.documents}`, true],
      ["n_unmapped", "키 대응", f => f.n_unmapped ? `<a href="#/labels/${q(name)}/keymap/${q(f.id)}"><span class="tag warn">맞출 키 ${f.n_unmapped}</span></a>`
        : `<a href="#/labels/${q(name)}/keymap/${q(f.id)}">보기</a>`],
      ["go", "", f => `<a href="#/labels/${q(name)}/format/${q(f.id)}"><button>문서 검수</button></a>
        ${f.doc_type && intProv.length ? `<button data-al="${esc(f.id)}" title="내부 모델로 값·위치를 먼저 채웁니다 (추론 결과가 없는 문서만)">모델로 먼저 채우기</button>` : ""}`]])}
    ${intProv.length ? `<div class="bar" style="margin-top:6px"><label>autolabel 분석기 <select id="lb-prov">${intProv.map(p => `<option>${esc(p.name)}</option>`).join("")}</select></label>
      <span class="muted">내부(external: false) openai 방식만. 실서류를 보내므로 외부 분석기는 고를 수 없습니다.</span></div>` : ""}
    <div class="rc-grid" style="margin-top:12px">
      <div class="panel"><b>검수 전 점수</b>
        <div class="muted">확인한 문서에서 원래 추론(키 대응 뒤)을 검수 결과에 대어 평가 세트와 같은 채점기로 낸 점수 = 그 모델의 실서류 점수입니다.</div>
        ${tk.length ? table(tk.map(([t, m]) => ({ t, ...m })), [["t", "과제"], ["n", "문서", null, true],
          ["f1", "값", x => pct(x.metrics.f1 ?? x.metrics.acc), true], ["loc", "위치", x => pct(x.metrics.loc_f1), true],
          ["vl", "값+위치 (주 점수)", x => `<b>${pct(x.metrics.vl_f1)}</b>`, true]]) : `<div class="muted">확인한 문서가 없거나 추론 결과가 없습니다.</div>`}
      </div>
      <div class="panel"><b>다음</b>
        <div class="bar"><a href="#/labels/${q(name)}/bundles"><button>업무 묶음 정하기</button></a>
          <button class="primary" id="lb-ds" ${o.exported ? "" : "disabled"}>데이터셋으로 (확인한 문서 ${o.exported}건)</button></div>
        <div class="muted">데이터셋으로: ④ 가져오기의 "라벨 있는 데이터"에 이 폴더를 넣어 검사 → 과제 선택 → 생성·등록합니다.</div>
      </div>
    </div>`;
  $("#lb-ds").onclick = () => { store.set("li.path", o.root); location.hash = "#/import"; };
  $$("[data-al]").forEach(bt => bt.onclick = async () => {
    try {
      const res = await api(`/api/labels/${q(name)}/autolabel/${q(bt.dataset.al)}`, { provider: $("#lb-prov").value });
      toast("모델로 채우는 중입니다 (⑧ 작업)"); location.hash = `#/jobs/analyzer/${q(res.analyzer)}`;
    } catch (e) { toast(e.message, true); }
  });
}

async function viewKeymap(name, fid) {
  const k = await api(`/api/labels/${q(name)}/keymap/${q(fid)}`);
  const opts = cur => `<option value="">(버림)</option>` + k.standard.map(s => `<option value="${esc(s.key)}" ${s.key === cur ? "selected" : ""}>${esc(s.key)} · ${esc(s.label || "")}</option>`).join("")
    + `<option value="__keep" ${cur && !k.standard.some(s => s.key === cur) ? "selected" : ""}>그대로 (표준 키 아님)</option>`;
  main().innerHTML = lbHead(name, ` › 키 대응`) + `
    <h1>키 대응 <span class="muted">${esc(fid)} → ${esc(k.doc_type || "서식 미정")}</span></h1>
    <div class="sub">모델이 낸 키를 이 포맷의 서식(${esc(k.doc_type || "-")}) 표준 키로 맞춥니다. 포맷 안 모든 문서에 한 번에 적용됩니다.
      ${k.doc_type ? "" : "서식을 먼저 정하면 표준 키 목록이 나옵니다."}</div>
    ${table(k.model_keys, [["key", "모델 키", m => `<span class="mono">${esc(m.key)}</span>`], ["label", "항목명"], ["n", "문서", null, true],
      ["example", "예", m => esc(String(m.example ?? "").slice(0, 40))],
      ["to", "표준 키", m => `<select data-mk="${esc(m.key)}">${opts(m.mapped === null || m.mapped === undefined ? (k.standard.some(s => s.key === m.key) ? m.key : "__keep") : m.mapped)}</select>`]])}
    <div class="bar" style="margin-top:8px"><button class="primary" id="km-save">저장</button><a href="#/labels/${q(name)}/format/${q(fid)}">문서 검수로</a></div>`;
  $("#km-save").onclick = async () => {
    const mapping = {};
    $$("[data-mk]").forEach(s => { mapping[s.dataset.mk] = s.value === "__keep" ? s.dataset.mk : s.value; });
    try { await api(`/api/labels/${q(name)}/keymap/${q(fid)}`, { mapping }, "PUT"); toast("저장했습니다 (검수하지 않은 문서에 적용)"); }
    catch (e) { toast(e.message, true); }
  };
}

async function viewLabelDocs(name, fid) {
  const [r, km] = await Promise.all([api(`/api/labels/${q(name)}/formats/${q(fid)}`), api(`/api/labels/${q(name)}/keymap/${q(fid)}`)]);
  const keys = [...new Set([...km.standard.map(s => s.key), ...km.model_keys.map(m => m.mapped || m.key)])].filter(Boolean);
  main().innerHTML = lbHead(name, ` › ${esc(fid)}`) + `
    <h1>문서 검수 <span class="muted">${esc(fid)} · ${esc(km.doc_type || "서식 미정")}</span></h1>
    <div class="sub">의심 먼저: 같은 포맷 문서 절반 이상에 있는 키가 빠진 문서, 위치가 없는 값, OCR 글자에 없는 값이 많은 문서부터.</div>
    <div class="bar"><label>같은 자리 모아 보기 <select id="kv-key">${keys.map(k => `<option>${esc(k)}</option>`).join("")}</select></label><button id="kv-go">보기</button></div>
    ${table(r.docs, [["doc", "문서", d => `<a href="#/labels/${q(name)}/doc/${q(fid)}/${q(d.doc)}">${esc(d.doc)}</a>`],
      ["status", "상태", d => d.status === "done" ? `<span class="tag ok">확인</span>` : d.status ? `<span class="tag">고치는 중</span>` : `<span class="muted">안 봄</span>`],
      ["missing", "빠진 키", d => d.missing.length ? `<span class="kr">${esc(d.missing.join(", "))}</span>` : ""],
      ["no_box", "위치 없음", d => esc(d.no_box.join(", "))], ["not_in_ocr", "OCR 에 없는 값", d => esc(d.not_in_ocr.join(", "))]])}`;
  $("#kv-go").onclick = () => { location.hash = `#/labels/${q(name)}/key/${q(fid)}/${q($("#kv-key").value)}`; };
}

async function viewKeyView(name, fid, key) {
  const r = await api(`/api/labels/${q(name)}/keyview/${q(fid)}?key=${q(key)}`);
  main().innerHTML = lbHead(name, ` › <a href="#/labels/${q(name)}/format/${q(fid)}">${esc(fid)}</a> › 같은 자리`) + `
    <h1>같은 자리 모아 보기 <span class="mono muted">${esc(key)}</span></h1>
    <div class="sub">포맷 안 모든 문서의 같은 키를 한 화면에. 값을 고치고 저장하면 그 문서는 "고치는 중"으로 저장됩니다 (확인은 문서 화면에서).</div>
    ${table(r.rows, [["doc", "문서", x => `<a href="#/labels/${q(name)}/doc/${q(fid)}/${q(x.doc)}">${esc(x.doc)}</a>`],
      ["crop", "그 자리", x => x.field && x.field.bbox && x.page_id ? `<img class="lb-crop" src="/api/labels/${q(name)}/crop?p=${q(x.page_id)}&box=${x.field.bbox.map(Math.round).join(",")}" alt="">` : `<span class="muted">위치 없음</span>`],
      ["value", "값", x => x.field ? `<input type="text" data-kv="${esc(x.doc)}" value="${esc(x.field.value ?? "")}" style="width:100%">` : `<span class="muted">없음</span>`],
      ["state", "상태", x => x.field ? `<span class="tag ${(LB_STATE[x.field.state] || [])[1] || ""}">${(LB_STATE[x.field.state] || [x.field.state])[0]}</span>` : ""]])}
    <div class="bar" style="margin-top:8px"><button class="primary" id="kv-save">바꾼 값 저장</button></div>`;
  const before = Object.fromEntries($$("[data-kv]").map(i => [i.dataset.kv, i.value]));
  $("#kv-save").onclick = async () => {
    let n = 0;
    for (const inp of $$("[data-kv]")) {
      if (inp.value === before[inp.dataset.kv]) continue;
      const d = await api(`/api/labels/${q(name)}/doc?d=${q(inp.dataset.kv)}`);
      for (const f of d.fields) if (f.key === key && f.state !== "deleted") { f.value = inp.value; f.state = "edited"; }
      await api(`/api/labels/${q(name)}/doc?d=${q(inp.dataset.kv)}`, { fields: d.fields, done: false }, "PUT");
      n += 1;
    }
    toast(`${n}건 저장했습니다`);
    viewKeyView(name, fid, key);
  };
}

async function viewLabelDoc(name, fid, doc) {
  const [d, list] = await Promise.all([api(`/api/labels/${q(name)}/doc?d=${q(doc)}`), api(`/api/labels/${q(name)}/formats/${q(fid)}`)]);
  const order = list.docs.map(x => x.doc);
  const next = order.slice(order.indexOf(doc) + 1).find(x => (list.docs.find(y => y.doc === x) || {}).status !== "done");
  const lb = { name, fid, doc, d, fields: d.fields.map(f => ({ ...f })), sel: -1, page: 0, draw: false, dirty: false, next };
  main().innerHTML = lbHead(name, ` › <a href="#/labels/${q(name)}/format/${q(fid)}">${esc(fid)}</a>`) + `
    <h1>${esc(doc)} ${d.status === "done" ? `<span class="tag ok">확인</span>` : ""} <span class="muted">${esc(d.doc_type || "서식 미정")}</span></h1>
    <div class="bar">
      <span id="lb-pages"></span>
      <button id="lb-add">항목 추가</button><button id="lb-draw" title="고른 항목의 위치를 그림에서 끌어 그립니다 (B)">위치 그리기</button>
      <button id="lb-del" title="Delete">삭제</button>
      <span style="flex:1"></span>
      ${!d.has_pred ? `<span class="muted">추론 결과 없음: 빈 라벨에서 시작</span>` : ""}
      <button id="lb-save" title="Ctrl+S">저장</button><button class="primary" id="lb-done" title="Ctrl+Enter: 확인하고 다음 문서로">확인 (검수 끝)</button>
    </div>
    <div class="viewer ed-viewer">
      <div id="lb-wrap"><div class="ed-stage" id="lb-stage"><img id="lb-img" alt=""><svg preserveAspectRatio="none"></svg></div></div>
      <div class="side" id="lb-side"></div>
    </div>`;
  lbBind(lb);
  lbPage(lb, 0);
  state.keyHandler = e => {
    const typing = /^(INPUT|SELECT|TEXTAREA)$/.test(document.activeElement && document.activeElement.tagName);
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") { e.preventDefault(); lbSave(lb, false); }
    else if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); lbSave(lb, true); }
    else if (!typing && e.key === "Delete") lbDelete(lb);
    else if (!typing && e.key.toLowerCase() === "b") { lb.draw = !lb.draw; lbDraw(lb); }
  };
  state.leave = unload => !lb.dirty || (unload ? false : confirm("저장하지 않은 라벨 수정이 있습니다. 버릴까요?"));
}

function lbPage(lb, k) {
  lb.page = k;
  const pg = lb.d.pages[k];
  $("#lb-img").src = `/api/imports/${q(lb.name)}/page?p=${q(pg.id)}`;
  $("#lb-stage svg").setAttribute("viewBox", `0 0 ${pg.width} ${pg.height}`);
  $("#lb-pages").innerHTML = lb.d.pages.length > 1 ? lb.d.pages.map((_, i) => `<button data-lp="${i}" class="${i === k ? "primary" : ""}">${i + 1}쪽</button>`).join("") : "";
  $$("[data-lp]").forEach(b => b.onclick = () => lbPage(lb, +b.dataset.lp));
  lbDraw(lb);
}

function lbDraw(lb) {
  const svg = $("#lb-stage svg");
  if (!svg) return;
  svg.innerHTML = lb.fields.map((f, i) => f.bbox && f.page === lb.page && f.state !== "deleted" ? (() => {
    const [x0, y0, x1, y1] = f.bbox;
    return `<rect data-i="${i}" class="rv-w ${f.state === "edited" ? "edited" : f.state === "added" ? "added" : f.state === "confirmed" ? "" : "low"} ${i === lb.sel ? "sel" : ""}"
      x="${x0}" y="${y0}" width="${Math.max(1, x1 - x0)}" height="${Math.max(1, y1 - y0)}"><title>${esc(f.key)} = ${esc(f.value ?? "")}</title></rect>`;
  })() : "").join("") + (lb.ghost ? `<rect class="ghost" x="${Math.min(lb.ghost[0], lb.ghost[2])}" y="${Math.min(lb.ghost[1], lb.ghost[3])}"
      width="${Math.abs(lb.ghost[2] - lb.ghost[0])}" height="${Math.abs(lb.ghost[3] - lb.ghost[1])}"></rect>` : "");
  $("#lb-stage").className = `ed-stage ${lb.draw ? "" : "tool-select"}`;
  $("#lb-draw").classList.toggle("primary", lb.draw);
  lbSide(lb);
}

function lbSide(lb) {
  const std = lb.d.standard;
  const keyOpts = cur => `<datalist id="lb-keys">${std.map(s => `<option value="${esc(s.key)}">${esc(s.label || "")}</option>`).join("")}</datalist>`;
  $("#lb-side").innerHTML = `${keyOpts()}
    <div class="muted" style="margin-bottom:4px">주황: 자동(추론 그대로) · 초록: 수정 · 보라: 추가 · 파랑 테두리: 고른 항목. 확인을 누르면 손대지 않은 칸도 "확인"이 됩니다.</div>
    <table class="ed-list"><thead><tr><th>키</th><th>값</th><th>쪽</th><th></th></tr></thead><tbody>
    ${lb.fields.map((f, i) => f.state === "deleted" ? "" : `<tr class="click ${i === lb.sel ? "sel" : ""}" data-row="${i}">
      <td><input type="text" list="lb-keys" data-k="${i}" value="${esc(f.key)}" style="width:150px" class="mono"></td>
      <td>${f.type === "seal" || f.type === "signature" ? `<label><input type="checkbox" data-pres="${i}" ${f.value || f.present ? "checked" : ""}> 있음</label>`
        : `<input type="text" data-v="${i}" value="${esc(f.value ?? "")}" style="width:100%">`}</td>
      <td class="num">${f.bbox ? f.page + 1 : `<span class="kr">-</span>`}</td>
      <td><span class="tag ${(LB_STATE[f.state] || [])[1] || ""}">${(LB_STATE[f.state] || [f.state])[0]}</span></td></tr>`).join("")}
    </tbody></table>
    ${(() => { const have = new Set(lb.fields.filter(f => f.state !== "deleted").map(f => f.key));
      const miss = std.filter(s => !have.has(s.key));
      return miss.length ? `<details style="margin-top:6px"><summary class="muted">서식에 있는데 없는 키 ${miss.length}</summary>${miss.map(s =>
        `<button data-addk="${esc(s.key)}" style="margin:2px">${esc(s.key)} ${esc(s.label || "")}</button>`).join("")}</details>` : ""; })()}`;
  const mark = (i, patch) => {
    const f = lb.fields[i];
    Object.assign(f, patch);
    if (f.state === "auto" || f.state === "confirmed") f.state = "edited";
    lb.dirty = true;
  };
  $$("[data-row]").forEach(tr => tr.onclick = e => { if (e.target.tagName !== "INPUT") { lb.sel = +tr.dataset.row; const f = lb.fields[lb.sel]; if (f.bbox && f.page !== lb.page) lbPage(lb, f.page); else lbDraw(lb); } });
  $$("[data-v]").forEach(inp => { inp.onfocus = () => { lb.sel = +inp.dataset.v; lbDrawOnly(lb); }; inp.oninput = () => mark(+inp.dataset.v, { value: inp.value }); });
  $$("[data-k]").forEach(inp => inp.onchange = () => { mark(+inp.dataset.k, { key: inp.value.trim() }); lbDraw(lb); });
  $$("[data-pres]").forEach(cb => cb.onchange = () => mark(+cb.dataset.pres, { value: cb.checked, present: cb.checked }));
  $$("[data-addk]").forEach(b => b.onclick = () => lbAdd(lb, b.dataset.addk));
}

function lbDrawOnly(lb) {   // 표는 두고 그림의 고른 칸만 다시
  $$("#lb-stage svg rect[data-i]").forEach(r => r.classList.toggle("sel", +r.dataset.i === lb.sel));
  $$("#lb-side tr[data-row]").forEach(tr => tr.classList.toggle("sel", +tr.dataset.row === lb.sel));
}

function lbAdd(lb, key = "") {
  const s = lb.d.standard.find(x => x.key === key);
  lb.fields.push({ key, label: s ? s.label : "", type: s ? s.type : "text", value: "", page: lb.page, bbox: null, state: "added" });
  lb.sel = lb.fields.length - 1;
  lb.draw = true;   // 바로 위치를 그리게
  lb.dirty = true;
  lbDraw(lb);
  toast("그림에서 끌어 위치를 그리고, 표에 값을 적으세요");
}

function lbDelete(lb) {
  if (lb.sel < 0) return;
  const f = lb.fields[lb.sel];
  if (f.state === "added" && !f.original) lb.fields.splice(lb.sel, 1); else f.state = "deleted";
  lb.sel = -1; lb.dirty = true;
  lbDraw(lb);
}

function lbBind(lb) {
  $("#lb-add").onclick = () => lbAdd(lb);
  $("#lb-draw").onclick = () => { lb.draw = !lb.draw; lbDraw(lb); };
  $("#lb-del").onclick = () => lbDelete(lb);
  $("#lb-save").onclick = () => lbSave(lb, false);
  $("#lb-done").onclick = () => lbSave(lb, true);
  const stage = $("#lb-stage");
  const pt = e => {
    const r = stage.querySelector("svg").getBoundingClientRect(), pg = lb.d.pages[lb.page];
    return { x: (e.clientX - r.left) * pg.width / r.width, y: (e.clientY - r.top) * pg.height / r.height };
  };
  let drag = null;
  stage.onmousedown = e => {
    if (e.button !== 0) return;
    const p = pt(e);
    if (lb.draw) {
      if (lb.sel < 0) { toast("표에서 항목을 먼저 고르세요", true); return; }
      e.preventDefault();
      drag = { x0: p.x, y0: p.y };
      lb.ghost = [p.x, p.y, p.x, p.y];
      return;
    }
    const t = e.target.dataset && e.target.dataset.i;
    if (t !== undefined) { lb.sel = +t; lbDrawOnly(lb); const inp = $(`[data-v="${t}"]`); if (inp) { inp.focus(); inp.select(); } }
  };
  stage.onmousemove = e => { if (!drag) return; const p = pt(e); lb.ghost = [drag.x0, drag.y0, p.x, p.y]; lbDraw(lb); };
  stage.onmouseup = () => {
    if (!drag) return;
    const [a, b, c, d] = lb.ghost;
    drag = null; lb.ghost = null;
    if (Math.abs(c - a) > 3 && Math.abs(d - b) > 3) {
      const f = lb.fields[lb.sel];
      f.bbox = [Math.min(a, c), Math.min(b, d), Math.max(a, c), Math.max(b, d)].map(r1);
      f.page = lb.page;
      if (f.state === "auto" || f.state === "confirmed") f.state = "edited";
      lb.dirty = true; lb.draw = false;
    }
    lbDraw(lb);
  };
}

async function lbSave(lb, done) {
  try {
    const r = await api(`/api/labels/${q(lb.name)}/doc?d=${q(lb.doc)}`, { fields: lb.fields, done }, "PUT");
    lb.dirty = false;
    toast(done ? `확인했습니다 (항목 ${r.fields})` : "저장했습니다");
    if (done) location.hash = lb.next ? `#/labels/${q(lb.name)}/doc/${q(lb.fid)}/${q(lb.next)}` : `#/labels/${q(lb.name)}/format/${q(lb.fid)}`;
    else viewLabelDoc(lb.name, lb.fid, lb.doc);
  } catch (e) { toast(e.message, true); }
}

async function viewLabelBundles(name) {
  const r = await api(`/api/labels/${q(name)}/bundles`);
  let rows = r.bundles.map(b => ({ bundle_id: b.bundle_id, scenario: b.scenario || "", customer: b.customer || "",
    documents: b.source_documents || b.documents || [], not_customer: b.not_customer ?? null }));
  const draw = () => {
    main().innerHTML = lbHead(name, " › 업무 묶음") + `
      <h1>업무 묶음 · ${esc(name)}</h1>
      <div class="sub">한 고객이 한 업무로 낸 서류를 묶고 시나리오를 고릅니다. 구비·대조·심사 정답은 규칙 코드가 검수한 값으로 계산합니다(④ 라벨 있는 데이터로 만들 때).
        표준 라벨 v1 규칙: 한 묶음에 서식마다 문서 한 건. 타인 명의 서류는 "타인"에 체크 (확인 안 했으면 비워 둠 → 구비 문항 생략).</div>
      ${r.suggest.length ? `<div class="panel" style="margin-bottom:8px"><b>묶음 후보</b> <span class="muted">검수한 주민번호·사업자번호가 같은 문서</span>
        ${r.suggest.map((s, i) => `<div><button data-sg="${i}">묶음으로</button> ${s.documents.map(esc).join(", ")}</div>`).join("")}</div>` : ""}
      ${rows.map((b, i) => `<div class="panel sc-card">
        <div class="bar"><label>묶음 ID <input type="text" data-bid="${i}" value="${esc(b.bundle_id)}" style="width:160px"></label>
          <label>업무 <select data-bsc="${i}"><option value="">고르기</option>${r.scenarios.map(s => `<option value="${esc(s.id)}" ${s.id === b.scenario ? "selected" : ""}>${esc(s.name)}</option>`).join("")}</select></label>
          <label>고객 <input type="text" data-bcu="${i}" value="${esc(b.customer)}" style="width:120px"></label>
          <label><input type="checkbox" data-bnc="${i}" ${b.not_customer !== null ? "checked" : ""}> 명의 확인함</label>
          <button data-bdel="${i}">묶음 빼기</button></div>
        <div class="rc-scs">${r.documents.map(d => `<label><input type="checkbox" data-bd="${i}" value="${esc(d.doc)}" ${b.documents.includes(d.doc) ? "checked" : ""}>
          ${esc(d.doc)} ${d.status === "done" ? "" : `<span class="muted">(미확인)</span>`}
          ${b.not_customer !== null ? `<input type="checkbox" data-bnot="${i}" value="${esc(d.doc)}" ${(b.not_customer || []).includes(d.doc) ? "checked" : ""} title="타인 명의"> 타인` : ""}</label>`).join("")}</div>
      </div>`).join("")}
      <div class="bar"><button id="bn-add">묶음 더하기</button><button class="primary" id="bn-save">저장</button></div>`;
    const read = () => rows.forEach((b, i) => {
      b.bundle_id = $(`[data-bid="${i}"]`).value.trim(); b.scenario = $(`[data-bsc="${i}"]`).value; b.customer = $(`[data-bcu="${i}"]`).value.trim();
      b.documents = $$(`[data-bd="${i}"]`).filter(c => c.checked).map(c => c.value);
      b.not_customer = $(`[data-bnc="${i}"]`).checked ? $$(`[data-bnot="${i}"]`).filter(c => c.checked).map(c => c.value) : null;
    });
    $$("[data-bnc]").forEach(c => c.onchange = () => { read(); draw(); });
    $$("[data-bdel]").forEach(bt => bt.onclick = () => { read(); rows.splice(+bt.dataset.bdel, 1); draw(); });
    $$("[data-sg]").forEach(bt => bt.onclick = () => { read(); rows.push({ bundle_id: `b${rows.length + 1}`, scenario: "", customer: "", documents: r.suggest[+bt.dataset.sg].documents, not_customer: null }); draw(); });
    $("#bn-add").onclick = () => { read(); rows.push({ bundle_id: `b${rows.length + 1}`, scenario: "", customer: "", documents: [], not_customer: null }); draw(); };
    $("#bn-save").onclick = async () => {
      read();
      try {
        const res = await api(`/api/labels/${q(name)}/bundles`, { bundles: rows.map(b => ({ ...b, not_customer: b.not_customer })) }, "PUT");
        toast(`묶음 ${res.saved}개를 저장했습니다`);
      } catch (e) { toast(e.message, true); }
    };
  };
  draw();
}
