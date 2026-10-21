// 칸의 키 고르기: 누구의 · 무엇. 키 사전 · 서식 미리보기 · 영역 편집이 같이 쓴다 (studio/DESIGN.md 16.0).
// 칸마다 키는 하나 — 누구의 · 무엇이 공통 키이면 공통 키, 아니면 문서별 키(서식의 키 그대로).
// 서버: studio/api_dictionary.py (/api/dictionary/vocab · cells · common), 풀이는 docgen/dictionary.py
"use strict";

let kpVocab = null;
async function kpLoad(force = false) {
  if (!kpVocab || force) kpVocab = await api("/api/dictionary/vocab");
  return kpVocab;
}
const KP_MARK = ["seal", "sign"];
const kpWhoName = id => kpVocab?.who.find(w => w.id === id)?.name || "";
const kpWhatName = id => ({ seal: "도장", sign: "서명" })[id] || kpVocab?.what.find(w => w.id === id)?.name || id || "";
const kpKeyFor = (who, what) => KP_MARK.includes(what) ? `${what}.${who}` : `${who}.${what}`;
const kpCommon = (who, what) => who && what ? kpVocab.common.find(c => c.key === kpKeyFor(who, what)) || null : null;
const kpRaw = cell => cell.raw || (cell.keys || []).map(k => k.raw || k);
const KP_BY = { "사람": "사람이 정함", "자동": "자동으로 정함", "없음": "안 정함" };

// 표 한 칸에 쓰는 짧은 키 표시: [공통] 고객 성명 / [문서별] signer2.name
function kpKeyCell(c) {
  if (c.common) {
    const k = kpVocab?.common.find(x => x.key === c.key);
    return `<span class="tag ok">공통</span> ${esc(k?.name || c.key)} <span class="muted mono" style="font-size:11px">${esc(c.key)}</span>`;
  }
  return `<span class="tag">문서별</span> <span class="mono">${esc(c.key)}</span>`;
}

function kpWhoCell(c) {
  if (!c.who) return `<span class="muted">—</span>`;
  return `${esc(kpWhoName(c.who))}${c.what ? ` · ${esc(kpWhatName(c.what))}` : ""}`;
}

// 누구의 · 무엇을 고르면 키가 어떻게 되는지 (저장 전에 보여 준다)
function kpResult(cell, who, what) {
  const raw = kpRaw(cell);
  const isSign = cell.t === "sign" || cell.t === "staff";
  const main = isSign && !raw.some(k => k.endsWith(".name")) ? null : what;
  const ck = kpCommon(who, main || (isSign ? "seal" : what));
  if (ck) {
    const extra = isSign ? KP_MARK.map(m => kpCommon(who, m)).filter(Boolean).filter(x => x.key !== ck.key) : [];
    return `<div><span class="tag ok">공통 키</span> <b>${esc(ck.name)}</b> <span class="mono muted">${esc(ck.key)}</span>
      ${extra.map(x => ` · ${esc(x.name)}`).join("")}</div>
      <div class="muted">묶음 안 다른 서류의 같은 키와 같은 값이 들어가고, 서류끼리 대조하는 문제에 쓰입니다.</div>`;
  }
  const doc = `<span class="tag">문서별 키</span> <span class="mono">${esc(raw[0] || "")}</span>`;
  if (who === "bank") return `<div>${doc}</div><div class="muted">은행·직원 칸: 고객 값을 넣지 않습니다.</div>`;
  if (who && what && !KP_MARK.includes(what)) {
    return `<div>${doc}</div><div class="muted">'${esc(kpWhoName(who))} · ${esc(kpWhatName(what))}'는 아직 공통 키가 아닙니다.
      서류끼리 대조할 값이면 <a href="#" id="kp-make">공통 키로 만들기</a></div>`;
  }
  return `<div>${doc}</div><div class="muted">이 서식에서만 묻고 답합니다.</div>`;
}

// 고르기 패널을 el 에 그린다. 저장하면 onSaved() (화면이 다시 읽는다)
async function kpPanel(el, form, cell, onSaved, opts = {}) {
  await kpLoad();
  const isSign = cell.t === "sign" || cell.t === "staff";
  const whats = kpVocab.what.filter(w => w.common > 0 && !KP_MARK.includes(w.id));
  if (cell.what && !KP_MARK.includes(cell.what) && !whats.some(w => w.id === cell.what)) whats.unshift(kpVocab.what.find(w => w.id === cell.what) || { id: cell.what, name: cell.what });
  const signWhat = cell.what === "ceo" ? "ceo" : "name";
  el.innerHTML = `<div class="kp">
    ${opts.image === false ? "" : `<div class="kp-img"><a href="#/forms/${encodeURIComponent(form)}/preview" title="미리보기로">
      <img src="/api/forms/${encodeURIComponent(form)}/cell-image?keys=${encodeURIComponent(kpRaw(cell).join(","))}" alt=""
        onerror="this.closest('.kp-img').innerHTML='<span class=muted>그림에 이 칸의 위치가 없습니다</span>'"></a>
      <div class="muted" style="font-size:12px">${esc(cell.form_name || form)} · seed 0 미리보기, 빨간 테두리가 이 칸</div></div>`}
    ${opts.label === false ? "" : `<div class="kp-label"><span class="muted">이름표</span> <b>${esc(cell.label || "(없음)")}</b></div>`}
    <div class="bar">
      <label>누구의 <select id="kp-who"><option value="">(모름)</option>${kpVocab.who.map(w =>
        `<option value="${w.id}" ${w.id === cell.who ? "selected" : ""} title="${esc(w.desc)}">${esc(w.name)}</option>`).join("")}</select></label>
      ${isSign ? `<label>이름 칸 <select id="kp-what"><option value="name" ${signWhat === "name" ? "selected" : ""}>성명·상호</option>
          <option value="ceo" ${signWhat === "ceo" ? "selected" : ""}>대표자</option></select></label>
          <span class="muted">서명·도장은 같은 사람으로</span>`
      : `<label>무엇 <select id="kp-what"><option value="">(모름)</option>${whats.map(w =>
        `<option value="${esc(w.id)}" ${w.id === cell.what ? "selected" : ""}>${esc(w.name)}</option>`).join("")}</select></label>`}
    </div>
    <div id="kp-res" class="kp-res"></div>
    <div class="bar"><button class="primary" id="kp-save">저장</button>
      ${cell.by && cell.by !== "없음" ? `<button id="kp-reset" title="정한 것을 지우고 서식의 키 그대로">처음 상태로</button>` : ""}
      <span class="muted">${KP_BY[cell.by] || ""}</span></div>
    <details class="muted"><summary>서식의 키</summary><span class="mono">${kpRaw(cell).map(esc).join(" · ")}</span></details>
  </div>`;
  const who = () => $("#kp-who", el).value, what = () => $("#kp-what", el).value;
  const show = () => {
    $("#kp-res", el).innerHTML = kpResult(cell, who(), what());
    const mk = $("#kp-make", el);
    if (mk) mk.onclick = async e => {
      e.preventDefault();
      try { await api("/api/dictionary/common", { who: who(), what: what() }); await kpLoad(true); toast("공통 키를 만들었습니다"); show(); }
      catch (err) { toast(err.message, true); }
    };
  };
  $("#kp-who", el).onchange = show;
  $("#kp-what", el).onchange = show;
  show();
  const put = async body => {
    try { await api("/api/dictionary/cells", { items: [{ form, keys: kpRaw(cell) }], ...body }, "PUT"); toast("저장"); onSaved && onSaved(); }
    catch (err) { toast(err.message, true); }
  };
  $("#kp-save", el).onclick = () => put({ who: who() || null, what: what() || null });
  if ($("#kp-reset", el)) $("#kp-reset", el).onclick = () => put({ clear: true });
}
