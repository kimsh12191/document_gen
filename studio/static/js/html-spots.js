// ① 서식 › 자리·템플릿 (html·코드 서식): 값이 나올 수 있는 모든 자리를 공란 그림 위에 보이고, 자리를 누르면 그 자리를 정한
// 템플릿 줄로 간다. 위치·항목명·모양은 템플릿에서 고치고 (문서마다 글꼴·행 수가 바뀌어 위치를 다시 계산하므로 끌어 옮기지 않음),
// 값 출처는 칸 목록 fields.json 에. 서버: studio/spots.py (/api/forms/{id}/spots · template · value)
"use strict";

const HS_STATUS = { base: "이 그림에 있음", other: "다른 고객·내용 많음에서만", never: "그려 본 문서에 안 나옴 (조건 칸이거나 안 쓰는 키)" };
const HS_TARGET = { field: "글자", box: "체크 보기", mark: "도장·서명" };
let hsSources = null;

async function viewHtmlSpots(d) {
  const url = `/api/forms/${encodeURIComponent(d.id)}`;
  const hs = { d, data: null, page: 0, sel: null, seed: 0, heavy: "default", values: store.get("hs.values", true), text: null, saved: null,
               dirty: false, diff: null, regions: [] };
  state.leave = unload => !hs.dirty || (unload ? false : confirm("저장하지 않은 템플릿 수정이 있습니다. 버릴까요?"));
  $("#tab").innerHTML = `
    <div class="sub">html 서식의 값 자리는 템플릿의 <span class="mono">f("키")</span> 가 정합니다. 문서마다 글꼴·행 수·쪽이 바뀌어 위치를 다시 계산하므로
      자리를 끌어 옮기지 않고 <b>템플릿</b>에서 고칩니다. 자리를 누르면 그 자리를 정한 템플릿 줄로 갑니다. 값 출처는 오른쪽에서 고칩니다.</div>
    <div class="bar"><label>고객 seed <input id="hs-seed" type="number" min="0" value="0" style="width:80px"></label>
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
          <div class="bar"><button id="hs-preview">미리보기 (저장 안 함)</button><button class="primary" id="hs-save">저장</button><button id="hs-revert">저장본으로</button>
            <span id="hs-tstatus" class="muted"></span></div>
          <div id="hs-diff"></div>
          <textarea id="hs-text" class="mono" spellcheck="false" style="width:100%;height:46vh;font-size:12px;line-height:1.45;white-space:pre;tab-size:2"></textarea>
        </div>
        <div id="hs-side"></div>
      </div>
    </div>`;
  const status = t => { const el = $("#hs-status"); if (el) el.textContent = t; };
  const tstatus = t => { const el = $("#hs-tstatus"); if (el) el.textContent = t; };
  const ta = $("#hs-text");
  ta.oninput = () => { hs.dirty = ta.value !== hs.saved; tstatus(hs.dirty ? "저장 안 됨 · 미리보기로 확인하세요" : ""); };

  const load = async (draft = null) => {
    status("모든 자리를 찾는 중 (고객 여러 명·내용 많음으로 그려 봅니다)…");
    try {
      const [data] = await Promise.all([
        api(url + "/spots", { seed: hs.seed, heavy: hs.heavy, ...(draft !== null ? { template: draft } : {}) }),
        hsSources ? null : api("/api/sources").then(s => { hsSources = s; }),
        api(url + "/regions").then(r => { hs.regions = r.regions || []; }).catch(() => { hs.regions = []; }),
      ]);
      hs.data = data;
      if (draft === null) { hs.saved = data.template; ta.value = data.template; hs.dirty = false; tstatus(""); }
      hs.diff = data.diff || null;
      $("#hs-file").textContent = data.file;
      hs.page = Math.min(hs.page, data.label.pages.length - 1);
      draw();
      const n = k => data.keys.filter(x => x.status === k).length;
      status(`자리 ${data.spots.length}개 · 키 ${data.keys.length}개 (이 그림 ${n("base")} · 다른 문서에서만 ${n("other")} · 안 나옴 ${n("never")})` +
             (draft !== null ? " · 저장 전 초안으로 그림" : ""));
    } catch (e) { status(e.message); }
  };

  const jump = line => {   // 템플릿의 그 줄을 고르고 보이게
    if (!line) return;
    const lines = ta.value.split("\n");
    const start = lines.slice(0, line - 1).reduce((a, l) => a + l.length + 1, 0);
    ta.focus({ preventScroll: true });
    ta.setSelectionRange(start, start + (lines[line - 1] || "").length);
    ta.scrollTop = Math.max(0, (line - 6) * parseFloat(getComputedStyle(ta).lineHeight));
  };

  const draw = () => {
    const data = hs.data, lab = data.label, pg = lab.pages[hs.page], scale = lab.scale || 2, w = pg.width / scale, h = pg.height / scale;
    $("#hs-pages").innerHTML = lab.pages.map((_, i) => `<button data-p="${i}" class="${hs.page === i ? "primary" : ""}">${i + 1}쪽</button>`).join("");
    const stage = $("#hs-stage");
    stage.style.width = "100%"; stage.style.maxWidth = `${w}px`;
    stage.innerHTML = `<img src="${esc(lab.image_urls[hs.page])}" draggable="false" alt="${esc(hs.d.name)}">
      <svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">${data.spots.map((s, i) => {
        if (s.page !== hs.page) return "";
        const [x, y, x1, y1] = s.rect, cls = s.target === "box" ? "t-check" : s.target === "mark" ? "st-added" : "st-auto";
        const fs = Math.max(7, Math.min(13, (y1 - y) * 0.6));
        return `<g data-i="${i}"><rect class="ed ${cls} ${hs.sel === s.pattern ? "sel" : ""}" x="${x}" y="${y}" width="${x1 - x}" height="${y1 - y}" style="cursor:pointer"></rect>
          ${hs.values && s.text && s.target === "field" ? `<text x="${x + 2}" y="${y + (y1 - y) / 2 + fs / 3}" font-size="${fs}" fill="#8a94a6" style="pointer-events:none">${esc(s.text.slice(0, 60))}</text>` : ""}
          <title>${esc(s.key)} · ${esc(s.label || "")} · ${esc(HS_TARGET[s.target] || s.target)}</title></g>`;
      }).join("")}</svg>`;
    stage.querySelector("svg").onclick = e => {
      const g = e.target.closest("[data-i]");
      if (!g) return;
      const s = data.spots[+g.dataset.i];
      select(s.pattern);
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

  const sourceSelect = (cur, code) => {
    const o = [];
    if (code) o.push(`<option value="code" ${cur === "code" || !cur ? "selected" : ""}>code — 생성 함수(generate.py) 값 그대로</option>`);
    else if (!cur) o.push(`<option value="" selected>(없음)</option>`);
    const opt = v => `<option value="${esc(v)}" ${v === cur ? "selected" : ""}>${esc(v)}</option>`;
    const prof = (hsSources?.profile || []).map(s => `<option value="${esc(s.source)}" ${s.source === cur ? "selected" : ""}>${esc(s.source)}${s.example ? ` — ${esc(String(s.example).slice(0, 24))}` : ""}</option>`);
    const rules = [...(hsSources?.rules || []), ...(hsSources?.special || []), "fixed", "choice", "empty"].filter((r, i, a) => a.indexOf(r) === i).map(r => opt(`rule:${r}`));
    return o.join("") + `<optgroup label="고객 프로필">${prof.join("")}</optgroup><optgroup label="값 종류 규칙">${rules.join("")}</optgroup>`;
  };

  const side = () => {
    const data = hs.data, k = hs.sel && data.keys.find(x => x.pattern === hs.sel);
    const code = data.kind === "code";
    const cur = k ? k.source : null;
    const row = x => `<tr data-k="${esc(x.pattern)}" class="click ${x.pattern === hs.sel ? "sel" : ""}"><td class="mono" style="font-size:11.5px">${esc(x.pattern)}</td>
      <td>${esc(x.label || "")}</td><td class="muted">${x.status === "base" ? `${x.spots || "-"}` : esc(x.seen.join(", ") || "-")}</td></tr>`;
    const group = st => {
      const rows = data.keys.filter(x => x.status === st);
      return rows.length ? `<h3 style="margin:10px 0 4px">${HS_STATUS[st]} <span class="muted">${rows.length}</span></h3>
        <table><thead><tr><th>키</th><th>항목명</th><th>${st === "base" ? "자리" : "나온 곳"}</th></tr></thead><tbody>${rows.map(row).join("")}</tbody></table>` : "";
    };
    $("#hs-info").innerHTML = k ? `<div class="box">
        <div><b class="mono">${esc(k.pattern)}</b> ${k.type ? `<span class="tag">${esc(k.type)}</span>` : ""}</div>
        <div>항목명: ${esc(k.label || "(없음)")} <span class="muted">— 템플릿의 label="…"</span></div>
        <div class="muted" style="font-size:12px">예시 값: ${k.examples.length ? k.examples.map(esc).join(" · ") : "(없음)"}</div>
        <div class="muted" style="font-size:12px">${esc(HS_STATUS[k.status])}</div>
        ${k.status === "other" ? `<div class="bar">${k.seen.slice(0, 3).map(n => `<button data-seen="${esc(n)}">${esc(n)} 로 그리기</button>`).join("")}</div>` : ""}
        <div style="margin-top:6px">정한 곳:
          ${k.template_line ? `<a href="#" id="hs-jump">템플릿 ${k.template_line}줄</a>` : `<span class="muted">템플릿 줄을 못 찾음 (매크로 안)</span>`}
          ${k.fields_line ? ` · <span class="mono">${esc(k.fields_line)}</span>` : ""}</div>
        ${k.value_from ? `<div class="muted" style="font-size:12px">값: ${esc(k.value_from.replace(/`/g, ""))}${k.key_from ? ` · 키: ${esc(k.key_from.replace(/`/g, ""))}` : ""}</div>` : ""}
        <details style="margin-top:6px" ${k.status === "never" ? "" : "open"}><summary>값 출처 바꾸기 (fields.json)</summary>
          <label class="fld">값 출처 <select id="hs-src">${sourceSelect(cur, code)}</select></label>
          <label class="fld" id="hs-fixed-l" style="display:none">고정 글자 <input id="hs-fixed" type="text"></label>
          <label class="fld" id="hs-choices-l" style="display:none">보기 (한 줄에 하나) <textarea id="hs-choices" rows="3"></textarea></label>
          <div class="bar"><button id="hs-src-save">값 출처 저장</button></div>
          <div class="muted" style="font-size:12px">저장하면 이 서식의 다음 데이터부터 바뀌고 "재검수 필요"가 됩니다.</div>
        </details>
        <div class="bar"><button id="hs-unsel">선택 해제</button></div></div>` : `<p class="muted">그림의 자리나 아래 키 목록을 누르면 그 자리를 정한 템플릿 줄로 갑니다.</p>`;
    $("#hs-side").innerHTML = group("base") + group("other") + group("never")
      + (hs.regions.length ? `<h3 style="margin:10px 0 4px">예전에 그린 고정 자리 <span class="muted">${hs.regions.length}</span></h3>
        <p class="muted" style="font-size:12px">쪽 위 고정 위치라 행 수·글꼴이 바뀌면 안 따라옵니다. html 서식은 템플릿으로 고치고, 이것은 지우는 것을 권합니다.</p>
        <table><tbody>${hs.regions.map((r, i) => `<tr><td class="mono" style="font-size:11.5px">${esc(r.key)}</td><td>${r.drop ? "빼기" : r.rect ? "위치" : "값"}</td>
          <td><button data-rdel="${i}">지우기</button></td></tr>`).join("")}</tbody></table>` : "");
    $("#hs-side").onclick = async e => {
      const tr = e.target.closest("[data-k]");
      if (tr) return select(tr.dataset.k);
      const del = e.target.closest("[data-rdel]");
      if (del && confirm("이 고정 자리를 지울까요? (칸 목록 fields.json 의 regions 에서 빠집니다)")) {
        const regions = hs.regions.filter((_, i) => i !== +del.dataset.rdel);
        try { await api(url + "/regions", { regions, seed: hs.seed, template_variant: "default" }, "PUT"); toast("지웠습니다"); state.forms = null; delete formCache[hs.d.id]; await load(); }
        catch (err) { toast(err.message, true); }
      }
    };
    if (!k) return;
    $$("#hs-info [data-seen]").forEach(b => b.onclick = () => {
      const m = /seed (\d+)/.exec(b.dataset.seen);
      hs.seed = m ? +m[1] : hs.seed; hs.heavy = b.dataset.seen.includes("내용 많음") ? "on" : "default";
      $("#hs-seed").value = hs.seed; $("#hs-heavy").value = hs.heavy;
      load(hs.dirty ? ta.value : null);
    });
    if ($("#hs-jump")) $("#hs-jump").onclick = e => { e.preventDefault(); jump(k.template_line); };
    $("#hs-unsel").onclick = () => { hs.sel = null; draw(); };
    const showExtra = () => {
      const v = $("#hs-src").value;
      $("#hs-fixed-l").style.display = v === "rule:fixed" ? "" : "none";
      $("#hs-choices-l").style.display = v === "rule:choice" ? "" : "none";
    };
    $("#hs-src").onchange = showExtra;
    showExtra();
    $("#hs-src-save").onclick = async () => {
      const source = $("#hs-src").value;
      if (!source) return toast("값 출처를 고르세요", true);
      try {
        await api(url + "/value", { pattern: k.pattern, source, text: $("#hs-fixed").value || null,
                                    choices: $("#hs-choices").value.split("\n").map(s => s.trim()).filter(Boolean) }, "PUT");
        toast("값 출처를 저장했습니다"); state.forms = null; delete formCache[hs.d.id];
        await load(hs.dirty ? ta.value : null);
      } catch (err) { toast(err.message, true); }
    };
  };

  const showDiff = () => {
    const d = hs.diff;
    $("#hs-diff").innerHTML = !d ? "" : (d.lost.length || d.added.length)
      ? `<div class="box warnbox">${d.lost.length ? `<div><b>빠지는 키 ${d.lost.length}</b>: ${d.lost.map(x => `<span class="mono">${esc(x)}</span>`).join(", ")} — 그 칸의 정답이 데이터에서 없어집니다</div>` : ""}
         ${d.added.length ? `<div><b>새로 생기는 키 ${d.added.length}</b>: ${d.added.map(x => `<span class="mono">${esc(x)}</span>`).join(", ")} — 값 출처를 정했는지 확인하세요</div>` : ""}</div>`
      : `<div class="muted">키는 저장본과 같습니다 (모양만 바뀜).</div>`;
  };

  $("#hs-go").onclick = () => { hs.seed = Math.max(0, +$("#hs-seed").value || 0); hs.heavy = $("#hs-heavy").value; load(hs.dirty ? ta.value : null); };
  $("#hs-values").onchange = e => { hs.values = e.target.checked; store.set("hs.values", hs.values); draw(); };
  $("#hs-pages").onclick = e => { if (e.target.dataset.p !== undefined) { hs.page = +e.target.dataset.p; draw(); } };
  $("#hs-preview").onclick = async () => { await load(ta.value); showDiff(); };
  $("#hs-revert").onclick = async () => { if (!hs.dirty || confirm("저장하지 않은 수정을 버릴까요?")) { hs.diff = null; showDiff(); await load(); } };
  $("#hs-save").onclick = async () => {
    if (!hs.dirty) return toast("바뀐 것이 없습니다");
    tstatus("저장 전 검사 중…");
    try {
      await load(ta.value); showDiff();
      if (hs.diff?.lost.length && !confirm(`빠지는 키가 ${hs.diff.lost.length}개 있습니다 (${hs.diff.lost.join(", ")}). 그래도 저장할까요?`)) return tstatus("저장 안 함");
      const r = await api(url + "/template", { template: ta.value }, "PUT");
      toast(`저장했습니다: ${r.file}`); state.forms = null; delete formCache[hs.d.id];
      hs.diff = null; showDiff(); await load();
    } catch (e) { tstatus(e.message); toast(e.message, true); }
  };
  await load();
}
