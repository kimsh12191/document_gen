// 메뉴 첫 화면 (view_<메뉴> 가 있으면 그것, 아직 없으면 무엇이 들어올지 안내)과 ⑨ 설정. 단계 번호는 DESIGN.md 11절.
// ④ 가져오기·⑤ 검수는 import.js·review.js 가 view_import·view_review 로 그린다.
"use strict";

const PLANS = {
  scenarios: ["시나리오·묶음", "4단계", [
    "시나리오 목록·편집: 필수 서류, 쓰는 서식의 검수 상태, 적용 가능한 사례·규칙",
    "묶음 목록과 묶음 상세: 서류 전부, 고객 프로필(서류끼리 맞아야 하는 값과 위치), 이 묶음에서 나온 문항",
    "대조 문항: 변조판과 원본을 나란히, 바뀐 칸 강조 · 심사 문항: 계산식과 쓰인 값 위치 · 구비 문항",
    "직접 묶음 만들기, 고객 일관성 검사, 문제 표시"]],
  datasets: ["데이터셋", "3단계 (등록부) · 4·5단계 (만들기)", [
    "등록부: OCR·은행 업무 데이터셋을 출처와 정답 종류와 함께 한 목록으로, 명령줄로 만든 폴더도 경로만 등록",
    "새로 만들기, 문항 보기, 데이터셋 설명서, 학습 설정 내보내기"]],
  eval: ["평가", "3단계", [
    "데이터셋마다 모델 답과 점수, 답 파일 붙여 채점 (명령줄과 같은 숫자), 문항마다 정답과 답 나란히, 비교표"]],
  jobs: ["작업", "8단계", [
    "서식 이미지 → CLI 분석기 → html 서식, html 편집기, overlay 값 영역 초안, 작업 목록·검토·승인"]],
};
for (const k of [...Object.keys(PLANS), "import", "review"]) {
  addRoute(new RegExp(`^#\\/${k}$`), () => {
    if (typeof window[`view_${k}`] === "function") return window[`view_${k}`]();
    viewPlan(...PLANS[k]);
  }, k);
}

addRoute(/^#\/settings$/, () => viewSettings(), "settings");

async function viewSettings() {
  const i = state.info || (state.info = await api("/api/info"));
  const row = (k, v) => `<tr><td>${k}</td><td class="mono">${v === null || v === undefined || v === "" ? `<span class="muted">(없음)</span>` : esc(v)}</td></tr>`;
  main().innerHTML = `<h1>설정</h1>
    <div class="sub">설정 파일: <span class="mono">${esc(i.config_file || "studio/config.json 없음 — 기본값 사용 (예시: studio/config.example.json)")}</span>. 바꾼 뒤 서버를 다시 띄웁니다.</div>
    <table><tbody>
      ${row("사용자 (검수·수정 기록에 남는 이름)", i.user)}
      ${row("렌더링 브라우저", i.browser)}${row("미리보기 캐시", i.cache_dir)}
      ${row("사내 OCR", i.ocr ? `${i.ocr.callable || ""} ${i.ocr.base_url || ""}${i.ocr.path || ""}` : null)}
      ${row("데이터셋 등록부·작업 공간 (workspace_dir)", i.paths.workspace_dir)}
      ${row("가져올 이미지 폴더 (import_dir)", i.paths.import_dir)}${row("실서류 검수 결과 (real_data_dir)", i.paths.real_data_dir)}
      ${row("실서류에서 만든 서식 (private_forms_dir)", i.paths.private_forms_dir)}
    </tbody></table>
    <h2>분석기</h2>
    <div class="sub">studio/config.json 의 <span class="mono">providers</span>. 연결 확인은 openai 방식이면 모델 목록, cli 방식이면 --version 만 봅니다 (요청은 보내지 않음).</div>
    <div id="st-prov"><p class="spin">읽는 중…</p></div>`;
  const pv = (await api("/api/providers")).providers;
  $("#st-prov").innerHTML = pv.length ? table(pv, [["name", "이름"], ["kind", "방식"], ["external", "연결 대상", p => p.external ? `<span class="tag warn">외부</span>` : `<span class="tag ok">내부</span>`],
    ["where", "주소·실행 파일", p => `<span class="mono">${esc(p.kind === "cli" ? (p.cmd || "(찾지 못함)") : `${p.base_url || ""} ${p.model || ""}`)}</span>`],
    ["check", "연결 확인", p => `<button data-pc="${esc(p.name)}">확인</button> <span class="muted" data-pr="${esc(p.name)}"></span>`]])
    : `<p class="muted">분석기가 없습니다. 예시는 studio/DESIGN.md 7.2.</p>`;
  $$("[data-pc]").forEach(b => b.onclick = async () => {
    const out = $(`[data-pr="${b.dataset.pc}"]`);
    out.textContent = "확인 중…";
    try { const r = await api(`/api/providers/${encodeURIComponent(b.dataset.pc)}/check`, {}); out.innerHTML = `${r.ok ? "✔" : "✘"} ${esc(r.detail || "")}`; }
    catch (e) { out.textContent = e.message; }
  });
}
