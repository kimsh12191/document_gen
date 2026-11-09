// ① 서식 › 자리·템플릿 (html·코드 서식): 값이 나올 수 있는 모든 자리를 공란 그림 위에 보이고, 자리를 누르면 그 자리를 정한
// 템플릿 줄로 간다. 위치·항목명·모양은 템플릿에서 고치고 (문서마다 글꼴·행 수가 바뀌어 위치를 다시 계산하므로 끌어 옮기지 않음),
// 생성 방법은 칸 목록 fields.json 에. 빈칸을 누르면 근처 인쇄 글자가 있는 템플릿 줄로, [자리 넣기] 는 커서 자리에 f() 줄과 생성 방법을.
// 템플릿·생성 방법 고친 것은 모아 두었다가 [저장] 한 번에. 레이아웃 변형이 있으면 골라서 그 템플릿을.
// 서버: studio/spots.py (/api/forms/{id}/spots · template)
"use strict";

const HS_STATUS = { base: "이 그림에 있음", other: "다른 고객·내용 많음에서만", never: "그려 본 문서에 안 나옴 (조건 칸이거나 안 쓰는 키)" };
const HS_TARGET = { field: "글자", box: "체크 보기", mark: "도장·서명" };
const HS_KINDS = { field: "글자", choice: "체크 보기", seal: "도장", sigspot: "서명·도장 자리" };
const HS_KEY_RX = /^[a-z][a-z0-9_]*(\.[a-z0-9_]+)*$/;
let hsSources = null, hsCommon = null;

async function viewHtmlSpots(d) {
  const url = `/api/forms/${encodeURIComponent(d.id)}`;
  const hs = { d, data: null, page: 0, sel: null, seed: 0, heavy: "default", variant: "default", values: store.get("hs.values", true),
               saved: null, pending: new Map(), diff: null, regions: [], near: null, caret: null };
  const dirtyText = () => $("#hs-text") && $("#hs-text").value !== hs.saved;
  const dirty = () => dirtyText() || hs.pending.size > 0;
  state.leave = unload => !dirty() || (unload ? false : confirm("저장하지 않은 템플릿·생성 방법 수정이 있습니다. 버릴까요?"));
  $("#tab").innerHTML = `
    <div class="sub">html 서식의 값 자리는 템플릿의 <span class="mono">f("키")</span> 가 정합니다. 문서마다 글꼴·행 수·쪽이 바뀌어 위치를 다시 계산하므로
      자리를 끌어 옮기지 않고 <b>템플릿</b>에서 고칩니다. 상자를 누르면 그 자리를 정한 줄로, <b>빈칸</b>을 누르면 근처 인쇄 글자가 있는 줄로 갑니다.
      거기서 <b>[자리 넣기]</b>. 고친 것은 모아 두었다가 <b>[저장]</b> 한 번에 저장합니다.</div>
    <div class="bar"><label id="hs-lay-l" style="display:none">레이아웃 <select id="hs-lay"></select></label>
      <label>고객 seed <input id="hs-seed" type="number" min="0" value="0" style="width:80px"></label>
      <label>내용 <select id="hs-heavy"><option value="default">보통</option><option value="on">많음 (반복 행·여러 쪽)</option></select></label>
      <label><input type="checkbox" id="hs-values" ${hs.values ? "checked" : ""}> 값 예시 보기</label>
      <button id="hs-go">다시 그리기</button><span id="hs-status" class="muted"></span></div>
    <div class="bar" id="hs-pages"></div>
    <div class="viewer ed-viewer" style="grid-template-columns:minmax(0,1fr) minmax(0,1fr)">
      <div><div id="hs-stage" class="ed-stage tool-select"></div></div>
      <div class="side">
        <div id="hs-info"></div>
        <div class="panel" style="margin:8px 0">
          <div class="bar"><b>템플릿</b> <span class="mono muted" id="hs-file" style="font-size:11.5px"></span></div>
          <div class="bar"><button id="hs-ins-open">자리 넣기</button><button id="hs-preview">미리보기 (저장 안 함)</button>
            <button class="primary" id="hs-save">저장</button><button id="hs-revert">저장본으로</button></div>
          <div id="hs-tstatus" class="muted" style="font-size:12px"></div>
          <div id="hs-ins"></div>
          <div id="hs-diff"></div>
          <textarea id="hs-text" class="mono" spellcheck="false" style="width:100%;height:46vh;font-size:12px;line-height:1.45;white-space:pre;tab-size:2"></textarea>
        </div>
        <div id="hs-side"></div>
      </div>
    </div>`;
  const status = t => { const el = $("#hs-status"); if (el) el.textContent = t; };
  const ta = $("#hs-text");
  const tstatus = () => {
    const el = $("#hs-tstatus");
    if (!el) return;
    const parts = [dirtyText() ? "템플릿 고침" : "", hs.pending.size ? `생성 방법 ${hs.pending.size}개 (${[...hs.pending.keys()].join(", ")})` : ""].filter(Boolean);
    el.textContent = parts.length ? `저장 안 됨: ${parts.join(" · ")} — 미리보기로 확인하고 [저장]` : "";
  };
  ta.oninput = tstatus;
  const keepCaret = () => { hs.caret = ta.selectionEnd; };
  ta.onkeyup = keepCaret; ta.onmouseup = keepCaret; ta.onblur = keepCaret;

  // 그리기: fresh 면 저장본으로 (편집기 글도 저장본으로), 아니면 지금 초안(템플릿·생성 방법)으로
  const load = async (fresh = false) => {
    status("모든 자리를 찾는 중 (고객 여러 명·내용 많음·다른 레이아웃으로 그려 봅니다)…");
    const body = { seed: hs.seed, heavy: hs.heavy, variant: hs.variant };
    if (!fresh && dirtyText()) body.template = ta.value;
    if (hs.pending.size) body.values = [...hs.pending.values()];
    try {
      const [data] = await Promise.all([
        api(url + "/spots", body),
        hsSources ? null : api("/api/sources").then(s => { hsSources = s; }),
        hsCommon ? null : api("/api/dictionary/keys?scope=common").then(r => { hsCommon = r.rows || []; }).catch(() => { hsCommon = []; }),
        api(url + "/regions").then(r => { hs.regions = r.regions || []; }).catch(() => { hs.regions = []; }),
      ]);
      hs.data = data;
      if (fresh) { hs.saved = data.template; ta.value = data.template; }
      hs.diff = data.diff || null;
      $("#hs-file").textContent = data.file;
      $("#hs-lay-l").style.display = data.layouts.length > 1 ? "" : "none";
      $("#hs-lay").innerHTML = data.layouts.map(l => `<option value="${esc(l.id)}" ${l.id === hs.variant ? "selected" : ""}>${esc(l.name)}${l.id === "default" ? " (기본)" : ""}${l.enabled ? "" : " · 꺼짐"}</option>`).join("");
      hs.page = Math.min(hs.page, data.label.pages.length - 1);
      draw(); showDiff(); tstatus();
      const n = k => data.keys.filter(x => x.status === k).length;
      status(`자리 ${data.spots.length}개 · 키 ${data.keys.length}개 (이 그림 ${n("base")} · 다른 문서에서만 ${n("other")} · 안 나옴 ${n("never")})` +
             (dirty() ? " · 저장 전 초안으로 그림" : ""));
    } catch (e) { status(e.message); }
  };

  const lineStart = line => ta.value.split("\n").slice(0, line - 1).reduce((a, l) => a + l.length + 1, 0);
  const jump = (line, collapse = false) => {   // 템플릿의 그 줄을 고르고 (collapse 면 줄 끝에 커서) 보이게
    if (!line) return;
    const start = lineStart(line), end = start + (ta.value.split("\n")[line - 1] || "").length;
    ta.focus({ preventScroll: true });
    ta.setSelectionRange(collapse ? end : start, end);
    hs.caret = end;
    ta.scrollTop = Math.max(0, (line - 6) * parseFloat(getComputedStyle(ta).lineHeight));
  };

  // 빈칸을 누르면: 같은 줄 왼쪽(없으면 위)에서 가장 가까운 인쇄 글자 덩어리 → 그 글자가 있는 템플릿 줄
  const norm = s => s.replace(/\{\{.*?\}\}|\{%.*?%\}|\{#.*?#\}/g, "").replace(/<[^>]*>/g, "").replace(/&nbsp;|&#160;/g, "").replace(/\s+/g, "");
  const nearText = (x, y) => {
    const mark = new Set((hs.data.label.texts || []).filter(t => /견본|SAMPLE|합성/.test(t.text)).map(t => `${t.page}:${t.blk}`));   // 견본 표시
    const ts = (hs.data.label.texts || []).filter(t => t.page === hs.page && !mark.has(`${t.page}:${t.blk}`));
    const row = ts.filter(t => y >= t.rect[1] - 4 && y <= t.rect[3] + 4 && t.rect[2] <= x + 4).sort((a, b) => (x - a.rect[2]) - (x - b.rect[2]));
    const above = ts.filter(t => t.rect[3] <= y + 4).sort((a, b) =>
      Math.hypot(x - (a.rect[0] + a.rect[2]) / 2, y - a.rect[3]) - Math.hypot(x - (b.rect[0] + b.rect[2]) / 2, y - b.rect[3]));
    const pick = row[0] || above[0];
    if (!pick) return null;
    const blk = ts.filter(t => t.blk === pick.blk && t.blk !== null && t.blk !== undefined);
    return { word: pick.text, phrase: (blk.length ? blk : [pick]).map(t => t.text).join(""), top: pick.rect[1], left: pick.rect[0] };
  };
  const linesWith = (s, top = null, left = null) => {   // 그 글자가 있는 줄. 위치를 적은 줄(top:…px)이면 누른 글자와 가까운 순
    const want = norm(s);
    if (!want) return [];
    const raw = ta.value.split("\n");
    const hits = raw.map((l, i) => [i + 1, l]).filter(([, l]) => norm(l).includes(want));
    const px = (l, k) => { const m = new RegExp(`${k}\\s*:\\s*(-?[\\d.]+)px`).exec(l); return m ? +m[1] : null; };
    if (top !== null) hits.sort((a, b) => {
      const da = px(a[1], "top") === null ? 1e9 : Math.abs(px(a[1], "top") - top) + Math.abs((px(a[1], "left") ?? left) - left) / 4;
      const db = px(b[1], "top") === null ? 1e9 : Math.abs(px(b[1], "top") - top) + Math.abs((px(b[1], "left") ?? left) - left) / 4;
      return da - db || a[0] - b[0];
    });
    return hits.map(([n]) => n);
  };
  // 좌표로 자리를 적는 서식 (공식 대조 html: <div class="entry" style="left:…px;top:…px">) 은 누른 곳에 자리를 만든다
  const absolute = () => /class="entry"/.test(ta.value);
  const sectionEnd = page => {   // page 번째 쪽 <section> 의 끝 (</section> 앞) 글자 위치
    let at = -1;
    for (let i = 0; i <= page; i++) { at = ta.value.indexOf("</section>", at + 1); if (at < 0) return null; }
    return at;
  };
  const clickBlank = (x, y) => {
    const t = nearText(x, y);
    hs.sel = null;
    if (absolute()) {
      const at = sectionEnd(hs.page);
      hs.near = { page: hs.page, x, y, label: t ? t.phrase : null, lines: [], abs: at !== null ? { at, x, y } : null };
      if (at !== null) { hs.caret = at; jump(ta.value.slice(0, at).split("\n").length, true); hs.caret = at; }
      draw(); return;
    }
    if (!t) { hs.near = { page: hs.page, x, y, label: null, lines: [] }; draw(); return; }
    let lines = linesWith(t.phrase, t.top, t.left), label = t.phrase;
    if (!lines.length) { lines = linesWith(t.word, t.top, t.left); label = t.word; }
    hs.near = { page: hs.page, x, y, label, lines };
    draw();
    if (lines.length) jump(lines[0], true);
  };

  const draw = () => {
    const data = hs.data, lab = data.label, pg = lab.pages[hs.page], scale = lab.scale || 2, w = pg.width / scale, h = pg.height / scale;
    $("#hs-pages").innerHTML = lab.pages.map((_, i) => `<button data-p="${i}" class="${hs.page === i ? "primary" : ""}">${i + 1}쪽</button>`).join("");
    const stage = $("#hs-stage");
    stage.style.width = "100%"; stage.style.maxWidth = `${w}px`;
    const nr = hs.near && hs.near.page === hs.page ? hs.near : null;
    stage.innerHTML = `<img src="${esc(lab.image_urls[hs.page])}" draggable="false" alt="${esc(hs.d.name)}">
      <svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" style="cursor:crosshair">${data.spots.map((s, i) => {
        if (s.page !== hs.page) return "";
        const [x, y, x1, y1] = s.rect, cls = s.target === "box" ? "t-check" : s.target === "mark" ? "st-added" : "st-auto";
        const fs = Math.max(7, Math.min(13, (y1 - y) * 0.6));
        const missing = (data.keys.find(k => k.pattern === s.pattern) || {}).missing_in || [];
        return `<g data-i="${i}"><rect class="ed ${cls} ${hs.sel === s.pattern ? "sel" : ""}" x="${x}" y="${y}" width="${x1 - x}" height="${y1 - y}"
            style="cursor:pointer${missing.length ? ";stroke-dasharray:4 2" : ""}"></rect>
          ${hs.values && s.text && s.target === "field" ? `<text x="${x + 2}" y="${y + (y1 - y) / 2 + fs / 3}" font-size="${fs}" fill="#8a94a6" style="pointer-events:none">${esc(s.text.slice(0, 60))}</text>` : ""}
          <title>${esc(s.key)} · ${esc(s.label || "")} · ${esc(HS_TARGET[s.target] || s.target)}${missing.length ? ` · 없는 레이아웃: ${esc(missing.join(", "))}` : ""}</title></g>`;
      }).join("")}
      ${nr ? `<circle cx="${nr.x}" cy="${nr.y}" r="6" fill="none" stroke="#d97706" stroke-width="2" vector-effect="non-scaling-stroke"></circle>` : ""}</svg>`;
    const svg = stage.querySelector("svg");
    svg.onclick = e => {
      const g = e.target.closest("[data-i]");
      if (g) { hs.near = null; return select(data.spots[+g.dataset.i].pattern); }
      const b = svg.getBoundingClientRect();
      clickBlank((e.clientX - b.left) * w / b.width, (e.clientY - b.top) * h / b.height);
    };
    side();
  };

  const select = pat => {
    hs.sel = pat;
    const k = hs.data.keys.find(x => x.pattern === pat);
    const first = hs.data.spots.find(s => s.pattern === pat);
    if (first && first.page !== hs.page) hs.page = first.page;
    draw();
    if (k) jump(k.template_line);
  };

  const sourceSelect = (cur, code, id = "hs-src") => {
    const o = [];
    if (code) o.push(`<option value="code" ${cur === "code" || !cur ? "selected" : ""}>code — 생성 함수(generate.py) 값 그대로</option>`);
    else if (!cur) o.push(`<option value="" selected>(고르세요)</option>`);
    const opt = v => `<option value="${esc(v)}" ${v === cur ? "selected" : ""}>${esc(v)}</option>`;
    const prof = (hsSources?.profile || []).map(s => `<option value="${esc(s.source)}" ${s.source === cur ? "selected" : ""}>${esc(s.source)}${s.example ? ` — ${esc(String(s.example).slice(0, 24))}` : ""}</option>`);
    const rules = [...(hsSources?.rules || []), ...(hsSources?.special || []), "fixed", "choice", "empty"].filter((r, i, a) => a.indexOf(r) === i).map(r => opt(`rule:${r}`));
    return `<select id="${id}">${o.join("")}<optgroup label="고객 프로필">${prof.join("")}</optgroup><optgroup label="값 종류 규칙">${rules.join("")}</optgroup></select>`;
  };
  const extraFields = pre => `<label class="fld" id="${pre}-fixed-l" style="display:none">고정 글자 <input id="${pre}-fixed" type="text"></label>
    <label class="fld" id="${pre}-choices-l" style="display:none">보기 (한 줄에 하나) <textarea id="${pre}-choices" rows="3"></textarea></label>`;
  const bindExtra = (sel, pre) => {
    const show = () => {
      $(`#${pre}-fixed-l`).style.display = $(sel).value === "rule:fixed" ? "" : "none";
      $(`#${pre}-choices-l`).style.display = $(sel).value === "rule:choice" ? "" : "none";
    };
    $(sel).onchange = show; show();
  };
  const valueOf = (pattern, sel, pre) => ({ pattern, source: $(sel).value, text: $(`#${pre}-fixed`).value || null,
                                            choices: $(`#${pre}-choices`).value.split("\n").map(s => s.trim()).filter(Boolean) });

  const side = () => {
    const data = hs.data, k = hs.sel && data.keys.find(x => x.pattern === hs.sel);
    const code = data.kind === "code";
    const row = x => `<tr data-k="${esc(x.pattern)}" class="click ${x.pattern === hs.sel ? "sel" : ""}"><td class="mono" style="font-size:11.5px">${esc(x.pattern)}${hs.pending.has(x.pattern) ? " ✎" : ""}</td>
      <td>${esc(x.label || "")}${x.missing_in.length ? ` <span class="tag warn" title="이 키가 없는 레이아웃">${esc(x.missing_in.join(", "))}에 없음</span>` : ""}</td>
      <td class="muted">${x.status === "base" ? `${x.spots || "-"}` : esc(x.seen.join(", ") || "-")}</td></tr>`;
    const group = st => {
      const rows = data.keys.filter(x => x.status === st);
      return rows.length ? `<h3 style="margin:10px 0 4px">${HS_STATUS[st]} <span class="muted">${rows.length}</span></h3>
        <table><thead><tr><th>키</th><th>항목명</th><th>${st === "base" ? "자리" : "나온 곳"}</th></tr></thead><tbody>${rows.map(row).join("")}</tbody></table>` : "";
    };
    const nr = hs.near;
    $("#hs-info").innerHTML = k ? `<div class="box">
        <div><b class="mono">${esc(k.pattern)}</b> ${k.type ? `<span class="tag">${esc(k.type)}</span>` : ""}
          ${k.missing_in.length ? `<span class="tag warn">${esc(k.missing_in.join(", "))} 레이아웃에 없음</span>` : ""}</div>
        <div>항목명: ${esc(k.label || "(없음)")} <span class="muted">— 템플릿의 label="…"</span></div>
        <div class="muted" style="font-size:12px">예시 값: ${k.examples.length ? k.examples.map(esc).join(" · ") : "(없음)"}</div>
        <div class="muted" style="font-size:12px">${esc(HS_STATUS[k.status])}</div>
        ${k.status === "other" ? `<div class="bar">${k.seen.slice(0, 3).map(n => `<button data-seen="${esc(n)}">${esc(n)} 로 그리기</button>`).join("")}</div>` : ""}
        <div style="margin-top:6px">정한 곳:
          ${k.template_line ? `<a href="#" id="hs-jump">템플릿 ${k.template_line}줄</a>` : `<span class="muted">템플릿 줄을 못 찾음 (매크로 안)</span>`}
          ${k.fields_line ? ` · <span class="mono">${esc(k.fields_line)}</span>` : ""}</div>
        ${k.value_from ? `<div class="muted" style="font-size:12px">값: ${esc(k.value_from.replace(/`/g, ""))}${k.key_from ? ` · 키: ${esc(k.key_from.replace(/`/g, ""))}` : ""}</div>` : ""}
        <details style="margin-top:6px" ${k.status === "never" ? "" : "open"}><summary>생성 방법 바꾸기 (fields.json)${hs.pending.has(k.pattern) ? " · 저장 안 됨" : ""}</summary>
          <label class="fld">생성 방법 ${sourceSelect(hs.pending.get(k.pattern)?.source || k.source, code)}</label>
          ${extraFields("hs")}
          <div class="bar"><button id="hs-src-set">바꾸고 미리보기</button>${hs.pending.has(k.pattern) ? `<button id="hs-src-undo">바꾼 것 취소</button>` : ""}</div>
        </details>
        <div class="bar"><button id="hs-unsel">선택 해제</button></div></div>`
      : nr && nr.abs ? `<div class="box"><div>누른 곳 근처 글자: <b>${esc(nr.label || "(없음)")}</b></div>
          <div>이 서식은 자리를 좌표로 적습니다. <b>누른 곳</b>(${Math.round(nr.x)}, ${Math.round(nr.y)} px, ${hs.page + 1}쪽)에 자리를 만듭니다.</div>
          <div class="bar"><button id="hs-ins-here">여기에 자리 넣기</button></div></div>`
      : nr ? `<div class="box"><div>누른 곳 근처 글자: <b>${esc(nr.label || "(없음)")}</b></div>
          ${nr.lines.length ? `<div>템플릿 ${nr.lines.map((n, i) => `<a href="#" data-line="${n}">${n}줄</a>${i === 0 ? " (커서를 이 줄 끝에 둠)" : ""}`).join(" · ")}</div>
            <div class="bar"><button id="hs-ins-here">여기에 자리 넣기</button></div>`
          : `<div class="muted">그 글자가 있는 템플릿 줄을 못 찾았습니다 (매크로가 만든 글자일 수 있음). 템플릿에서 직접 찾으세요 (편집기 안에서 Ctrl+F).</div>`}</div>`
      : `<p class="muted">상자를 누르면 그 자리를 정한 템플릿 줄로, 빈칸을 누르면 근처 인쇄 글자가 있는 줄로 갑니다.</p>`;
    $("#hs-side").innerHTML = group("base") + group("other") + group("never")
      + (hs.regions.length ? `<h3 style="margin:10px 0 4px">예전에 그린 고정 자리 <span class="muted">${hs.regions.length}</span></h3>
        <p class="muted" style="font-size:12px">쪽 위 고정 위치라 행 수·글꼴이 바뀌면 안 따라옵니다. html 서식은 템플릿으로 고치고, 이것은 지우는 것을 권합니다.</p>
        <table><tbody>${hs.regions.map((r, i) => `<tr><td class="mono" style="font-size:11.5px">${esc(r.key)}</td><td>${r.drop ? "빼기" : r.rect ? "위치" : "값"}</td>
          <td><button data-rdel="${i}">지우기</button></td></tr>`).join("")}</tbody></table>` : "");
    $("#hs-side").onclick = async e => {
      const tr = e.target.closest("[data-k]");
      if (tr) { hs.near = null; return select(tr.dataset.k); }
      const del = e.target.closest("[data-rdel]");
      if (del && confirm("이 고정 자리를 지울까요? (칸 목록 fields.json 의 regions 에서 빠집니다)")) {
        const regions = hs.regions.filter((_, i) => i !== +del.dataset.rdel);
        try { await api(url + "/regions", { regions, seed: hs.seed, template_variant: "default" }, "PUT"); toast("지웠습니다"); state.forms = null; delete formCache[hs.d.id]; await load(); }
        catch (err) { toast(err.message, true); }
      }
    };
    $$("#hs-info [data-line]").forEach(a => a.onclick = e => { e.preventDefault(); jump(+a.dataset.line, true); });
    if ($("#hs-ins-here")) $("#hs-ins-here").onclick = () => openInsert(nr.label || "");
    if (!k) return;
    $$("#hs-info [data-seen]").forEach(b => b.onclick = () => {
      const m = /seed (\d+)/.exec(b.dataset.seen);
      hs.seed = m ? +m[1] : hs.seed; hs.heavy = b.dataset.seen.includes("내용 많음") ? "on" : "default";
      $("#hs-seed").value = hs.seed; $("#hs-heavy").value = hs.heavy;
      load();
    });
    if ($("#hs-jump")) $("#hs-jump").onclick = e => { e.preventDefault(); jump(k.template_line); };
    $("#hs-unsel").onclick = () => { hs.sel = null; draw(); };
    bindExtra("#hs-src", "hs");
    const p = hs.pending.get(k.pattern);
    if (p) { $("#hs-fixed").value = p.text || ""; $("#hs-choices").value = (p.choices || []).join("\n"); }
    $("#hs-src-set").onclick = () => {
      const v = valueOf(k.pattern, "#hs-src", "hs");
      if (!v.source) return toast("생성 방법을 고르세요", true);
      hs.pending.set(k.pattern, v); load();
    };
    if ($("#hs-src-undo")) $("#hs-src-undo").onclick = () => { hs.pending.delete(k.pattern); load(); };
  };

  // [자리 넣기]: 커서 자리에 종류에 맞는 줄 + (글자·체크 보기) 생성 방법을 모아 둠 → 미리보기
  const openInsert = (label = "") => {
    const code = hs.data.kind === "code";
    const names = hs.data.keys.map(k => k.pattern).filter(p => /(^|\.)name$/.test(p));
    $("#hs-ins").innerHTML = `<div class="box" style="margin:6px 0">
      <div class="bar"><label>종류 <select id="hi-kind">${Object.entries(HS_KINDS).map(([v, n]) => `<option value="${v}">${n}</option>`).join("")}</select></label>
        <label>키 <input id="hi-key" list="hi-keys" placeholder="예: applicant.phone" style="width:200px"></label>
        <label>항목명 <input id="hi-label" value="${esc(label)}" placeholder="원본에 인쇄된 글자" style="width:150px"></label></div>
      <datalist id="hi-keys">${(hsCommon || []).slice(0, 400).map(r => `<option value="${esc(r.key)}">${esc(r.name || "")}</option>`).join("")}</datalist>
      <div id="hi-more"></div>
      <div class="bar"><button class="primary" id="hi-go">넣기 (커서 자리)</button><button id="hi-close">닫기</button>
        <span class="muted" style="font-size:12px">키는 영어 소문자·숫자·밑줄을 점으로 이은 "누구의.무엇". 도장·서명은 자리 이름만 (seal.·sign. 이 붙음)</span></div></div>`;
    const more = () => {
      const kind = $("#hi-kind").value;
      $("#hi-more").innerHTML = kind === "field" ? `<label class="fld">생성 방법 ${sourceSelect(code ? "code" : "", code, "hi-src")}</label>${extraFields("hi")}`
        : kind === "choice" ? `<label class="fld">보기 (한 줄에 하나, 고객마다 하나가 체크됨) <textarea id="hi-opts" rows="3"></textarea></label>`
        : kind === "sigspot" ? `<label class="fld">서명·도장 할 사람의 이름 키 <input id="hi-name" list="hi-names" value="${esc(names[0] || "")}"></label>
            <datalist id="hi-names">${names.map(n => `<option value="${esc(n)}">`).join("")}</datalist>`
        : `<div class="muted" style="font-size:12px">도장 글자는 항목명으로 찍습니다 (예: 회사직인 → "회사직인").</div>`;
      if (kind === "field") bindExtra("#hi-src", "hi");
    };
    $("#hi-kind").onchange = more; more();
    $("#hi-close").onclick = () => { $("#hs-ins").innerHTML = ""; };
    $("#hi-go").onclick = () => {
      const kind = $("#hi-kind").value, key = $("#hi-key").value.trim(), lab = $("#hi-label").value.trim();
      const q = s => s.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
      if (!HS_KEY_RX.test(key)) return toast("키는 영어 소문자로 시작, 소문자·숫자·밑줄을 점으로 이은 꼴 (예: applicant.phone)", true);
      if (!lab) return toast("항목명을 적으세요 (원본에 인쇄된 글자)", true);
      const full = kind === "seal" ? `seal.${key}` : kind === "sigspot" ? `sign.${key}` : key;
      const have = hs.data.keys.map(k => k.pattern);
      const clash = have.find(p => p.startsWith(full + ".") || full.startsWith(p + "."));
      if (clash) return toast(`키 '${full}' 와 '${clash}' 를 함께 쓸 수 없습니다 (한 키가 다른 키의 앞부분)`, true);
      if (have.includes(full) && !confirm(`'${full}' 는 이미 있는 키입니다. 같은 값을 한 번 더 찍습니다. 넣을까요?`)) return;
      let snippet, value = null;
      if (kind === "field") {
        snippet = `{{ f("${q(key)}", label="${q(lab)}") }}`;
        const v = valueOf(key, "#hi-src", "hi");
        if (!v.source) return toast("생성 방법을 고르세요", true);
        if (!(code && v.source === "code")) value = v;
        else if (!have.includes(key)) return toast("코드 서식의 새 키는 생성 함수가 값을 만들지 않으니 생성 방법을 고르세요 (고객 프로필·규칙)", true);
      } else if (kind === "choice") {
        const opts = $("#hi-opts").value.split("\n").map(s => s.trim()).filter(Boolean);
        if (opts.length < 2) return toast("보기를 두 개 이상 적으세요", true);
        snippet = `{{ m.choice("${q(key)}", [${opts.map(o => `"${q(o)}"`).join(", ")}], label="${q(lab)}") }}`;
        value = { pattern: key, source: "rule:choice", choices: opts };
      } else if (kind === "seal") {
        snippet = `{{ m.seal("${q(lab)}", key="${q(key)}", label="${q(lab)}") }}`;
      } else {
        const name = $("#hi-name").value.trim();
        if (!name) return toast("이름 키를 적으세요", true);
        snippet = `{{ m.sigspot("${q(key)}", val("${q(name)}"), label="${q(lab)}") }}`;
      }
      const abs = hs.near && hs.near.abs;
      if (abs && kind !== "sigspot") snippet = `<div class="entry" style="left:${(abs.x - 3).toFixed(1)}px;top:${(abs.y - 10).toFixed(1)}px;width:160px;height:20px;font-size:12px">${snippet}</div>\n`;
      const at = abs ? abs.at : (hs.caret ?? ta.selectionEnd);
      ta.setRangeText(snippet, at, at, "end");
      hs.caret = at + snippet.length;
      if (value) hs.pending.set(value.pattern, value);
      $("#hs-ins").innerHTML = "";
      hs.sel = full; hs.near = null;
      toast(`넣었습니다: ${snippet}`);
      load();
    };
  };

  const showDiff = () => {
    const d = hs.diff;
    $("#hs-diff").innerHTML = !d ? "" : (d.lost.length || d.added.length)
      ? `<div class="box warnbox">${d.lost.length ? `<div><b>빠지는 키 ${d.lost.length}</b>: ${d.lost.map(x => `<span class="mono">${esc(x)}</span>`).join(", ")} — 그 칸의 정답이 데이터에서 없어집니다</div>` : ""}
         ${d.added.length ? `<div><b>새로 생기는 키 ${d.added.length}</b>: ${d.added.map(x => `<span class="mono">${esc(x)}</span>`).join(", ")} — 생성 방법을 정했는지 확인하세요</div>` : ""}</div>`
      : `<div class="muted">키는 저장본과 같습니다.</div>`;
  };

  $("#hs-go").onclick = () => { hs.seed = Math.max(0, +$("#hs-seed").value || 0); hs.heavy = $("#hs-heavy").value; load(); };
  $("#hs-lay").onchange = e => {
    if (dirtyText() && !confirm("이 레이아웃의 템플릿 수정을 버리고 다른 레이아웃으로 갈까요? (생성 방법 바꾼 것은 그대로)")) { e.target.value = hs.variant; return; }
    hs.variant = e.target.value; hs.sel = null; hs.near = null; hs.page = 0; load(true);
  };
  $("#hs-values").onchange = e => { hs.values = e.target.checked; store.set("hs.values", hs.values); draw(); };
  $("#hs-pages").onclick = e => { if (e.target.dataset.p !== undefined) { hs.page = +e.target.dataset.p; hs.near = null; draw(); } };
  $("#hs-ins-open").onclick = () => openInsert(hs.near?.label || "");
  $("#hs-preview").onclick = () => load();
  $("#hs-revert").onclick = async () => { if (!dirty() || confirm("저장하지 않은 수정(템플릿·생성 방법)을 버릴까요?")) { hs.pending.clear(); hs.diff = null; await load(true); } };
  $("#hs-save").onclick = async () => {
    if (!dirty()) return toast("바뀐 것이 없습니다");
    $("#hs-tstatus").textContent = "저장 전 검사 중…";
    try {
      await load();
      if (hs.diff?.lost.length && !confirm(`빠지는 키가 ${hs.diff.lost.length}개 있습니다 (${hs.diff.lost.join(", ")}). 그래도 저장할까요?`)) return tstatus();
      const r = await api(url + "/template", { template: dirtyText() ? ta.value : null, variant: hs.variant,
                                                values: hs.pending.size ? [...hs.pending.values()] : null }, "PUT");
      toast(`저장했습니다: ${r.file}${r.values ? ` · 생성 방법 ${r.values}개` : ""}`); state.forms = null; delete formCache[hs.d.id];
      hs.pending.clear(); hs.diff = null; await load(true);
    } catch (e) { $("#hs-tstatus").textContent = e.message; toast(e.message, true); }
  };
  await load(true);
}
