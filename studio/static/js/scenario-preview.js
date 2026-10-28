// ③ 시나리오·묶음: 시나리오 안에서 같은 고객(seed·프로필 값)의 필수 서류를 펼쳐 보고 확대·쪽 넘김한다.
// scenarios.js 가 ScenarioPreviews 를 만들어 쓴다. 서버: POST /api/forms/{id}/render (extra = 고객 프로필 값, studio/app.py)
"use strict";

class ScenarioPreviews {
  constructor() {
    this.states = new WeakMap();
    this.requests = new Map();
  }

  html(s, i) {
    if (!this.states.has(s)) this.states.set(s, { open: i === 0, seed: 0, version: 0, labels: new Map() });
    const v = this.states.get(s);
    return `<details class="sc-preview" ${v.open ? "open" : ""}>
      <summary>서류 이미지로 보기 <span class="tag">필수 서류 ${s.docs.length}종</span></summary>
      <div class="sc-preview-body">
        <div class="bar">
          <label>예시 고객 seed <input type="number" class="sc-preview-seed" value="${v.seed}" min="0" max="2147483647" step="1"></label>
          <button type="button" class="sc-preview-apply">보기</button>
          <button type="button" class="sc-preview-next">다른 고객 보기</button>
          <span class="muted sc-preview-status" role="status" aria-live="polite"></span>
        </div>
        <div class="sub">고객 1명의 필수 서류 구성 예시입니다. 이미지를 누르면 확대하고 모든 쪽을 넘겨 볼 수 있습니다.
          서류 빠짐·타인 서류·변조가 적용된 결과는 ⑥ 데이터셋의 업무 묶음에서 확인합니다.</div>
        <div class="sc-preview-grid"></div>
      </div>
    </details>`;
  }

  bind(card, s) {
    const v = this.states.get(s), details = $(".sc-preview", card);
    details.addEventListener("toggle", () => {
      if (v.open === details.open) return;
      v.open = details.open;
      if (v.open) this.refresh(card, s);
      else v.version++;
    });
    const apply = () => {
      const inp = $(".sc-preview-seed", card);
      if (!inp.reportValidity()) return;
      v.seed = Number(inp.value || 0);
      card.dispatchEvent(new Event("scenario-preview-change"));
      this.refresh(card, s);
    };
    $(".sc-preview-apply", card).onclick = apply;
    $(".sc-preview-seed", card).onkeydown = e => { if (e.key === "Enter") { e.preventDefault(); apply(); } };
    $(".sc-preview-next", card).onclick = () => {
      const inp = $(".sc-preview-seed", card);
      inp.value = v.seed >= 2147483647 ? 0 : v.seed + 1;
      apply();
    };
    if (v.open) this.refresh(card, s);
  }

  async refresh(card, s) {
    const v = this.states.get(s);
    if (!v.open) return;
    const version = ++v.version, seed = v.seed;
    // Builder.bundle_profile 과 같은 설정. 편집 중인 extra 도 저장하지 않고 확인한다.
    const extra = { ...(s.extra || {}), scenario: s.id, form_bank: "하나은행" };
    const grid = $(".sc-preview-grid", card), status = $(".sc-preview-status", card);
    const active = () => card.isConnected && v.open && v.version === version;
    v.labels = new Map();
    status.textContent='역할별 서식 선택 중…';
    let resolution;
    try{resolution=await api('/api/scenarios/resolve',{scenario:{...s,docs:s.docs.map(d=>d.id)},seed});}
    catch(e){if(active()){grid.innerHTML=`<p class="err">${esc(e.message)}</p>`;status.textContent='서식 선택 오류';}return;}
    if(!active())return;
    const docs=resolution.selections.map(x=>({...x}));v.docs=docs;
    if(this.dialog?.scenario===s)this.dialog.element.close();
    grid.innerHTML = docs.map((d, i) => `<article class="sc-preview-doc">
      <button type="button" class="sc-preview-thumb" data-doc="${i}" disabled aria-label="${esc(d.name || d.id)} 확대">
        <span class="muted">이미지 대기 중…</span></button>
      <div class="sc-preview-caption"><b>${i + 1}. ${esc(d.name || d.id)}</b>
        <div><span class="mono muted">${esc(d.id)}</span> <span class="sc-preview-pages"></span></div>
      </div></article>`).join("") || `<p class="muted">필수 서류를 추가하면 이미지가 여기에 나타납니다.</p>`;
    const cards = $$(".sc-preview-doc", grid);
    let done = 0, failed = 0;
    const progress = () => { status.textContent = docs.length ? `고객 seed ${seed} · ${done}/${docs.length}종 준비${failed ? ` · 실패 ${failed}종` : ""}` : ""; };
    progress();
    // 브라우저 렌더러는 하나다. 펼친 시나리오만 순차 요청하고 화면이 바뀌면 멈춘다.
    for (const [i, d] of docs.entries()) {
      if (!active()) return;
      const tile = cards[i], thumb = $(".sc-preview-thumb", tile);
      thumb.innerHTML = `<span class="spin">이미지 만드는 중…</span>`;
      const key = JSON.stringify([d.id, seed, extra]);
      try {
        if (!this.requests.has(key)) {
          const request = api(`/api/forms/${encodeURIComponent(d.id)}/render`,
            { seed, heavy: "default", special: "default", condition: "clean", extra });
          this.requests.set(key, request);
          request.catch(() => this.requests.delete(key));
        }
        const label = await this.requests.get(key);
        if (!active()) return;
        if (!label.image_urls?.length) throw new Error("문서 이미지가 없습니다");
        v.labels.set(d.id, label);
        thumb.innerHTML = `<img src="${esc(label.image_urls[0])}" alt="${esc(d.name || d.id)} 첫 쪽"><span class="sc-preview-enlarge">확대 보기</span>`;
        thumb.disabled = false;
        thumb.onclick = () => this.show(s, d.id);
        $(".sc-preview-pages", tile).textContent = `${label.image_urls.length}쪽 · ${label.template_variant?.name || '기본 레이아웃'}`;
      } catch (e) {
        if (!active()) return;
        failed++;
        thumb.innerHTML = `<span class="err">${esc(e.message)}</span><span>다시 시도</span>`;
        thumb.disabled = false;
        thumb.onclick = () => { this.requests.delete(key); this.refresh(card, s); };
      }
      done++;
      progress();
      if (this.dialog?.scenario === s) this.dialog.ready(d.id);
    }
  }

  show(s, docId, key = null) {
    if (this.dialog) this.dialog.element.close();
    const v = this.states.get(s), dialog = document.createElement("dialog");
    dialog.className = "sc-preview-dialog";
    const docs=v.docs || s.docs;
    let selected = Math.max(0,docs.findIndex(d => d.id === docId)), zoom = false;
    let page = v.labels.get(docId)?.fields.find(f => f.key === key)?.page || 0;
    const draw = () => {
      const d = docs[selected], label = v.labels.get(d.id);
      const n = label?.image_urls.length || 0;
      const field = key && label?.fields.find(f => f.key === key);
      dialog.innerHTML = `<div class="sc-preview-dialog-head">
        <div><div class="muted">${esc(s.name)} · 같은 고객 seed ${v.seed} · 서류 ${selected + 1}/${docs.length}</div>
          <h2>${esc(d.name || d.id)}</h2></div><button type="button" class="sc-close" aria-label="미리보기 닫기">닫기 ×</button></div>
        <div class="bar">
          <button type="button" class="sc-prev-doc" ${selected === 0 ? "disabled" : ""}>이전 서류</button>
          <button type="button" class="sc-next-doc" ${selected === docs.length - 1 ? "disabled" : ""}>다음 서류</button>
          <span class="sep"></span>
          <button type="button" class="sc-prev-page" ${page <= 0 ? "disabled" : ""}>이전 쪽</button>
          <span>${n ? `${page + 1} / ${n}쪽` : "준비 중"}</span>
          <button type="button" class="sc-next-page" ${page + 1 >= n ? "disabled" : ""}>다음 쪽</button>
          <button type="button" class="sc-zoom">${zoom ? "화면에 맞추기" : "원본 크기"}</button>
          <a href="#/forms/${encodeURIComponent(d.id)}/preview" class="sc-form-link">서식 상세·편집</a>
        </div>
        ${field ? `<div class="sc-evidence-note">근거 항목: ${esc(field.label || key)} · <b>${esc(field.value)}</b> <span class="mono">${esc(key)}</span></div>` : ""}
        <div class="sc-preview-paper ${zoom ? "sc-preview-original" : ""}">
          ${n ? `<div class="stage">${stageHTML({ ...label, fields: [] }, page, -1,
            field?.bbox && (field.page || 0) === page ? [{ bbox: field.bbox, cls: "sc-evidence", title: key }] : [])
            .replace('alt=""', `alt="${esc(d.name || d.id)} ${page + 1}쪽"`)}</div>`
            : `<p class="muted">이미지를 준비하고 있습니다. 실패한 문서는 목록에서 다시 시도해 주세요.</p>`}</div>`;
      $(".sc-close", dialog).onclick = () => dialog.close();
      $(".sc-form-link", dialog).onclick = () => dialog.close();
      $(".sc-prev-doc", dialog).onclick = () => { selected--; page = 0; key = null; draw(); };
      $(".sc-next-doc", dialog).onclick = () => { selected++; page = 0; key = null; draw(); };
      $(".sc-prev-page", dialog).onclick = () => { page--; draw(); };
      $(".sc-next-page", dialog).onclick = () => { page++; draw(); };
      $(".sc-zoom", dialog).onclick = () => { zoom = !zoom; draw(); };
    };
    this.dialog = { scenario: s, element: dialog, ready: id => { if (docs[selected].id === id) draw(); } };
    dialog.addEventListener("close", () => { if (this.dialog?.element === dialog) this.dialog = null; dialog.remove(); });
    dialog.addEventListener("click", e => { if (e.target === dialog) {
      const r = dialog.getBoundingClientRect();
      if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close();
    } });
    document.body.appendChild(dialog);
    draw();
    dialog.showModal();
    $(".sc-close", dialog).focus();
  }
}
