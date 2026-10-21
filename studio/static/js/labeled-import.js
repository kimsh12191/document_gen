// ④ 가져오기 › 라벨 있는 데이터: 생성기 공통 라벨(v1) 폴더를 검사하고 정답·문서 연결 확인 후 데이터셋을 만든다 → ⑥ 자동 등록.
// import.js 가 labeledImportHTML·bindLabeledImport 로 ④ 화면에 넣는다. 서버: studio/api_labels.py, studio/labeled_data.py. 규격: studio/LABEL_FORMAT.md
"use strict";

function labeledImportHTML() {
  return `<section class="panel" id="li-panel">
    <h2>라벨 있는 데이터</h2>
    <p class="sub">예제 ZIP을 풀거나 같은 형식으로 준비한 폴더의 경로를 입력하세요.
      <span class="mono">meta.json · images/ · labels/</span>를 검사한 뒤 기존 정답으로 문항을 만듭니다. OCR 서버를 호출하지 않습니다.</p>
    <div class="bar"><input id="li-path" aria-label="라벨 데이터 폴더 경로" placeholder="예제 ZIP을 푼 폴더 또는 준비한 데이터 폴더" style="flex:1;min-width:260px">
      <button class="primary" id="li-check">폴더 검사</button></div>
    <div id="li-report"></div>
  </section>`;
}

function bindLabeledImport() {
  const pre = store.get("li.path", "");   // ⑤ 라벨 검수의 "데이터셋으로" 가 넘긴 폴더
  if (pre && $("#li-path")) { $("#li-path").value = pre; store.set("li.path", ""); setTimeout(() => $("#li-check") && $("#li-check").click(), 0); }
  const root = $("#li-panel"), input = $("#li-path"), report = $("#li-report"), checkButton = $("#li-check");
  input.oninput = () => { report.innerHTML = ""; };
  checkButton.onclick = async () => {
    if (!input.value.trim()) return toast("라벨 데이터 폴더 경로를 입력하세요", true);
    checkButton.disabled = true; input.disabled = true;
    report.innerHTML = `<p class="spin">이미지·라벨·좌표를 검사하고 있습니다…</p>`;
    try {
      const r = await api("/api/labeled-imports/check", {path: input.value.trim()});
      if (!root.isConnected) return;
      const issues = (rows, name) => rows.length ? `<details ${name === "오류" ? "open" : ""}><summary>${name} ${rows.length}건${rows.length === 200 ? " (최대 200건 표시)" : ""}</summary>${table(rows, [["file", "파일"], ["path", "항목"], ["message", "내용"]])}</details>` : "";
      if (!r.ok) { report.innerHTML = issues(r.errors, "오류") + issues(r.warnings, "확인 사항"); return; }
      const s = r.summary;
      report.innerHTML = `<div class="bar"><span class="tag ok">검사 통과</span>
        <span>문서 ${s.documents}건 · ${s.pages}쪽 · 항목 ${s.fields}개 · 업무 묶음 ${s.bundles}건</span></div>
        <p>출처: ${r.meta.real_data ? "실서류" : "합성/공개 데이터"} · 정답: ${esc({exact:"생성 정답", reviewed:"사람 확인 정답", pseudo:"미검수 후보"}[r.meta.gt])}</p>
        ${issues(r.warnings, "확인 사항")}
        <details><summary>이미지·정답 미리보기</summary><div class="bar">
          <select id="li-doc" aria-label="미리볼 문서">${r.documents.map((d, i) => `<option value="${i}">${esc(d.label.id)} · ${esc(d.label.doc_name)}</option>`).join("")}</select>
          <select id="li-page" aria-label="미리볼 쪽"></select></div><div id="li-preview"></div></details>
        <div class="bar" style="margin-top:12px">
          <label>데이터셋 이름 <input id="li-name" value="${esc(r.meta.name)}"></label>
          <label>용도 <select id="li-split"><option value="test">평가</option><option value="train">학습</option></select></label>
        </div>
        <div class="bar" id="li-tasks"><span class="muted">과제 (한 데이터셋에 함께):</span>${[["classify","문서 분류"],["kie","항목 추출"],["marks","체크·도장·서명"],["ocr_field","값 칸 OCR"],["doc_check","서류 구비"],["review","직접 비교·심사"]].map(([id, name]) =>
          `<label><input type="checkbox" data-li-task="${id}" checked>${name}</label>`).join("")}
          <label title="${s.full_ocr ? "쪽 전체 OCR 정답으로 OCR 8과제" : "모든 쪽의 OCR 정답과 ocr_scope:full_page 가 필요합니다"}"><input type="checkbox" data-li-task="ocr" ${s.full_ocr ? "" : "disabled"}>쪽 OCR 8과제${s.full_ocr ? "" : " (쪽 전체 정답 필요)"}</label></div>
        <p class="sub">업무 묶음은 bundles.jsonl과 저장된 ③ 처리 설정을 사용합니다. 값이나 근거가 없는 작업은 사유를 남기고 생략합니다.
          구비 검사는 명의를 확인한 not_customer 목록(타인 서류가 없으면 [])이 필요합니다. 합성 변조 사례는 적용하지 않습니다.</p>
        <label><input type="checkbox" id="li-confirm">라벨 정답 종류와 문서·쪽·고객별 묶음 연결을 확인했습니다.</label>
        <div class="bar"><button class="primary" id="li-build" disabled>데이터셋 만들고 등록</button><span id="li-status" class="muted"></span></div>`;
      const show = () => {
        const d = r.documents[+$("#li-doc").value].label, p = +$("#li-page").value;
        const label = {...d, image_urls: d.images.map((_, i) => `/api/labeled-imports/${r.token}/image?doc=${encodeURIComponent(d.id)}&page=${i}`)};
        $("#li-preview").innerHTML = `<div class="viewer" style="grid-template-columns:minmax(0,1fr) 400px"><div class="stage">${stageHTML(label, p, -1)}</div>
          <div>${table(d.fields.filter(f => f.page === undefined || f.page === p), [["key","키"],["label","항목"],["value","정답", f => `<span class="mono">${esc(JSON.stringify(f.value))}</span>`]])}</div></div>`;
      };
      const doc = () => { const d = r.documents[+$("#li-doc").value].label; $("#li-page").innerHTML = d.images.map((_, i) => `<option value="${i}">${i + 1}쪽</option>`).join(""); show(); };
      $("#li-doc").onchange = doc; $("#li-page").onchange = show; doc();
      $("#li-confirm").onchange = () => { $("#li-build").disabled = !$("#li-confirm").checked; };
      $("#li-build").onclick = async () => {
        const button = $("#li-build"); button.disabled = true; $("#li-confirm").disabled = true;
        try {
          const result = await api(`/api/labeled-imports/${r.token}/build`, {name: $("#li-name").value.trim(),
            split: $("#li-split").value, tasks: $$("[data-li-task]:checked").map(x => x.dataset.liTask), confirmed: true});
          if (!root.isConnected) return;
          toast("생성을 시작했습니다. 완료 후 ⑥ 목록에 자동 등록됩니다");
          location.hash = "#/datasets";
        } catch (e) {
          if (root.isConnected) { $("#li-status").textContent = e.message; button.disabled = false; $("#li-confirm").disabled = false; }
        }
      };
    } catch (e) { if (root.isConnected) report.textContent = e.message; }
    finally { checkButton.disabled = false; input.disabled = false; }
  };
}
