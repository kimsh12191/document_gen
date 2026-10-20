// ② 표시 요소: 확률 설정(docgen/marks.json)과 모양 풀(docgen/assets/marks/). 생성기 규칙은 docgen/marks.py
"use strict";

addRoute(/^#\/marks$/, () => viewMarks(), "marks");

const MARK_SETTINGS = [
  ["hand", null, "손글씨 비율", "overlay 서식에서 서류 전체를 손글씨로 쓸 확률 (나머지는 전산 인쇄체)"],
  ["staff", "processed", "결재란: 처리된 서류", "은행이 접수·처리를 마쳐 결재란에 도장·서명이 있는 서류 비율"],
  ["staff", "filled", "결재란: 칸마다 찍힘", "처리된 서류에서 결재란 칸마다 찍혀 있을 확률"],
  ["staff_spot", "square_below", "결재란: 사각 도장", "결재란 도장 중 사각 도장 비율"],
  ["staff_spot", "seal_below", "결재란: 도장(나머지 서명)", "결재란에서 도장 비율 (나머지는 서명)"],
  ["sign_spot", "seal_below", "(서명 또는 인): 도장", "'(서명 또는 인)' 자리에 도장이 찍힐 확률"],
  ["sign_spot", "sign_below", "(서명 또는 인): 도장+서명", "도장 또는 서명이 있을 확률 (나머지는 빈칸)"],
  ["seal_spot", "seal_below", "인감·날인 칸: 도장", "'인감', '서명/날인' 칸에 도장이 찍힐 확률"],
  ["seal_spot", "sign_below", "인감·날인 칸: 도장+서명", "도장 또는 서명이 있을 확률 (나머지는 빈칸)"],
];

async function viewMarks() {
  const m = await api("/api/marks");
  const get = (o, k, kk) => kk ? o[k][kk] : o[k];
  main().innerHTML = `
    <h1>표시 요소</h1>
    <div class="sub">손글씨·체크·도장·서명이 <b>어느 칸에 얼마나</b> 나올지(확률)와 <b>어떻게 생겼는지</b>(풀)를 정합니다.
      기본값은 지금 생성기와 같아서, 바꾸지 않으면 생성 결과도 그대로입니다. 바꾸면 그다음 렌더링부터 모든 서식에 반영됩니다.</div>
    <h2>확률 <span class="muted" style="font-weight:400;font-size:13px">(서식마다 다르게 하려면 영역 편집기의 수정 파일 marks 항목)</span></h2>
    <div class="panel"><table class="mk-set"><thead><tr><th>항목</th><th>값</th><th class="muted">기본</th><th>뜻</th></tr></thead><tbody>
      ${MARK_SETTINGS.map(([k, kk, n, desc]) => `<tr><td class="nw">${n}</td>
        <td><input type="number" step="0.01" min="0" max="1" data-k="${k}" data-kk="${kk || ""}" value="${get(m.settings, k, kk)}"></td>
        <td class="muted num">${get(m.defaults, k, kk)}</td><td class="muted">${desc}</td></tr>`).join("")}
    </tbody></table>
    <div class="bar"><button class="primary" id="mk-save">확률 저장</button><button id="mk-reset">기본값으로</button></div></div>
    <h2>풀</h2>
    <div class="sub">항목마다 가중치(뽑힐 비율)와 켜기를 정합니다. 체크·서명은 투명 배경 PNG(또는 SVG)를 올립니다.
      <b>실서류에서 잘라 온 서명·도장은 여기 올리지 마세요</b> (저장소에 들어갑니다).</div>
    <div id="mk-pools"></div>
    <h2>미리보기</h2>
    <div class="bar"><label>서식 <input type="text" id="mk-form" value="${esc(store.get("mk.form", "hf169"))}" style="width:180px"></label>
      <label>seed <input type="number" id="mk-seed" value="${store.get("mk.seed", 0)}" min="0"></label>
      <button id="mk-preview">렌더링</button><span class="muted" id="mk-stat"></span></div>
    <div id="mk-out"></div>`;
  $("#mk-save").onclick = async () => {
    const out = JSON.parse(JSON.stringify(m.settings));
    for (const inp of $$(".mk-set input")) {
      const v = parseFloat(inp.value);
      if (inp.dataset.kk) out[inp.dataset.k][inp.dataset.kk] = v; else out[inp.dataset.k] = v;
    }
    try { await api("/api/marks/settings", out, "PUT"); toast("저장했습니다"); viewMarks(); } catch (e) { toast(e.message, true); }
  };
  $("#mk-reset").onclick = async () => {
    if (!confirm("확률을 모두 기본값으로 되돌릴까요?")) return;
    try { await api("/api/marks/settings", m.defaults, "PUT"); viewMarks(); } catch (e) { toast(e.message, true); }
  };
  drawPools(m);
  $("#mk-preview").onclick = async () => {
    const id = $("#mk-form").value.trim(), seed = +$("#mk-seed").value || 0;
    store.set("mk.form", id); store.set("mk.seed", seed);
    $("#mk-stat").textContent = "렌더링 중…";
    try {
      const L = await renderOne(id, { ...state.opts, seed }, true);
      const marks = L.fields.filter(f => ["seal", "signature", "checkbox", "checkbox_multi"].includes(f.type));
      $("#mk-out").innerHTML = `<div class="viewer"><div class="stage">${stageHTML(L, 0, -1)}</div>
        <div class="side panel">${table(marks, [["key", "키", f => `<span class="mono">${esc(f.key)}</span>`], ["v", "값", f => esc(valueText(f))],
          ["render", "풀 항목", f => esc(f.render || "")]])}</div></div>`;
      $("#mk-stat").textContent = `${L.pages.length}쪽 · 1쪽만 표시`;
    } catch (e) { $("#mk-stat").innerHTML = `<span class="err">${esc(e.message)}</span>`; }
  };
}

function drawPools(m) {
  // 손글씨 글꼴 미리보기: 생성기와 같은 글꼴 파일(docgen/fonts/<id>.woff2)을 이 화면에도 건다
  let st = $("#mk-fontfaces");
  if (!st) { st = document.createElement("style"); st.id = "mk-fontfaces"; document.head.appendChild(st); }
  st.textContent = m.pools.hand_fonts.map(f => `@font-face{font-family:'${f.id}';src:url('/fonts/${f.id}.woff2') format('woff2')}`).join("");
  const glyph = (name, it) => {
    if (it.url) return `<img src="${esc(it.url)}" alt="">`;
    if (name === "check") return `<span class="glyph">${esc(it.id === "O" ? "○" : it.id)}</span>`;
    if (name === "hand_fonts") return `<span class="glyph" style="font-family:'${esc(it.id)}'">홍길동 123</span>`;
    if (name === "print_fonts") return `<span class="glyph" style="font-family:${esc(it.id)}">홍길동 123</span>`;
    if (name === "seal") {
      const st = [it.shape === "square" ? "border-radius:4px" : it.shape === "oval" ? "border-radius:50%;width:60px" : "",
        it.border ? `border-width:${it.border}px` : "", it.double ? "border-style:double;border-width:4px" : "",
        it.font ? `font-family:${it.font}` : "", it.ink ? `color:${it.ink};border-color:${it.ink}` : ""].filter(Boolean).join(";");
      return `<span class="seal-demo" style="${esc(st)}">홍길<br>동인</span>`;
    }
    return `<span class="glyph muted">(코드가 그림)</span>`;
  };
  $("#mk-pools").innerHTML = Object.entries(m.pools).map(([name, items]) => `
    <div class="panel pool" data-pool="${name}">
      <div class="bar"><b>${esc(m.names[name])}</b> <span class="muted">${items.filter(x => x.enabled !== false && x.weight > 0).length}/${items.length} 켜짐</span>
        <span class="sep"></span>
        ${m.image_pools.includes(name) ? `<input type="file" accept=".png,.svg" data-up="${name}"> <button data-upgo="${name}">올리기</button>` : ""}
        ${name === "seal" ? `<select data-shape>${m.seal_shapes.map(s => `<option>${s}</option>`).join("")}</select>
          <label>테두리 <input type="number" data-border value="2" min="1" max="6" style="width:50px"></label>
          <label><input type="checkbox" data-double> 겹선</label>
          <label>인주 <input type="text" data-ink value="#c00" style="width:70px"></label>
          <label>글꼴 <input type="text" data-font placeholder="'Nanum Myeongjo'" style="width:140px"></label>
          <button data-addseal>틀 추가</button>` : ""}
        ${name === "hand_fonts" || name === "print_fonts" ? `<input type="text" data-fontid placeholder="${name === "hand_fonts" ? "docgen/fonts/ 의 파일 이름 (예: NanumPen)" : "글꼴 이름 (예: 'Malgun Gothic')"}" style="width:220px">
          ${name === "hand_fonts" ? `<label>크기 비율 <input type="number" data-fontscale value="1.0" step="0.05" style="width:60px"></label>` : ""}
          <button data-addfont>글꼴 추가</button>` : ""}
        <button class="primary" data-savepool="${name}">이 풀 저장</button>
      </div>
      <div class="pool-grid">${items.map(it => `
        <div class="pool-item ${it.enabled === false || it.weight === 0 ? "off" : ""}" data-id="${esc(it.id)}">
          <div class="pv">${glyph(name, it)}</div>
          <div class="nm">${esc(it.name || it.id)}${it.builtin ? ` <span class="tag">기본</span>` : ""}</div>
          <div class="bar"><label>가중치 <input type="number" min="0" max="100" value="${it.weight ?? 1}" data-w style="width:56px"></label>
            <label><input type="checkbox" data-en ${it.enabled === false ? "" : "checked"}> 켜기</label>
            ${it.builtin ? "" : `<button data-del="${esc(it.id)}">지우기</button>`}</div>
        </div>`).join("")}</div>
    </div>`).join("");
  $("#mk-pools").onclick = async e => {
    const box = e.target.closest(".pool"), name = box?.dataset.pool;
    if (!name) return;
    try {
      if (e.target.dataset.savepool) {
        const items = $$(".pool-item", box).map(el => ({ id: el.dataset.id, weight: parseInt($("[data-w]", el).value || "0", 10),
          enabled: $("[data-en]", el).checked }));
        await api(`/api/marks/pools/${name}`, items, "PUT");
        toast("저장했습니다"); viewMarks();
      } else if (e.target.dataset.upgo) {
        const f = $(`[data-up="${name}"]`, box).files[0];
        if (!f) { toast("파일을 고르세요", true); return; }
        await apiUpload(`/api/marks/pools/${name}/upload`, f, { label: f.name });
        toast("올렸습니다"); viewMarks();
      } else if (e.target.dataset.del) {
        if (!confirm("이 항목을 지울까요?")) return;
        await api(`/api/marks/pools/${name}/${encodeURIComponent(e.target.dataset.del)}`, undefined, "DELETE");
        viewMarks();
      } else if (e.target.dataset.addfont !== undefined) {
        const fid = $("[data-fontid]", box).value.trim();
        if (!fid) return;
        await api(`/api/marks/pools/${name}/font`, { id: fid, scale: +($("[data-fontscale]", box)?.value || 1) });
        toast("글꼴을 더했습니다"); viewMarks();
      } else if (e.target.dataset.addseal !== undefined) {
        await api("/api/marks/seal-template", { shape: $("[data-shape]", box).value, border: +$("[data-border]", box).value,
          double: $("[data-double]", box).checked, ink: $("[data-ink]", box).value.trim(), font: $("[data-font]", box).value.trim() });
        toast("도장 틀을 더했습니다"); viewMarks();
      }
    } catch (err) { toast(err.message, true); }
  };
}
