// 아직 만들지 않은 메뉴(무엇이 들어올지 안내)와 ⑨ 설정. 단계 번호는 DESIGN.md 11절.
"use strict";

const PLANS = {
  scenarios: ["시나리오·묶음", "4단계", [
    "시나리오 목록·편집: 필수 서류, 쓰는 서식의 검수 상태, 적용 가능한 사례·규칙",
    "묶음 목록과 묶음 상세: 서류 전부, 고객 프로필(서류끼리 맞아야 하는 값과 위치), 이 묶음에서 나온 문항",
    "대조 문항: 변조판과 원본을 나란히, 바뀐 칸 강조 · 심사 문항: 계산식과 쓰인 값 위치 · 구비 문항",
    "직접 묶음 만들기, 고객 일관성 검사, 문제 표시"]],
  import: ["가져오기", "7단계 (이미지 묶음) · 9단계 (결과 폴더)", [
    "두 방식: ① 이미지 묶음 → 사내 OCR → 묶기 ② 이미 만든 OCR·추론 결과 폴더 경로(studio/RESULTS_FORMAT.md) → 저장된 OCR로 묶기",
    "포맷·양식마다 \"템플릿으로\" / \"기존 서식과 같음\" / \"건너뛰기\" 결정, 묶음 전체 또는 고른 포맷을 \"OCR 벤치마크로\""]],
  review: ["검수", "7단계 (OCR 검수) · 9단계 (라벨·묶음 검수, 내부망)", [
    "OCR 검수: 쪽마다 사내 OCR 글자·박스를 고치고 확인 → 사내 OCR 형식 그대로 저장 → OCR 검수 정답",
    "라벨 검수: 결과 폴더의 추론 결과를 포맷 단위로 검수, 검수 전후 점수",
    "묶음 검수: 실서류를 고객·업무 묶음으로 묶고 시나리오 지정 → 구비·대조·심사 정답은 규칙 코드가 계산, 사람은 확인"]],
  datasets: ["데이터셋", "3단계 (등록부) · 4·5단계 (만들기)", [
    "등록부: OCR·은행 업무 데이터셋을 출처와 정답 종류와 함께 한 목록으로, 명령줄로 만든 폴더도 경로만 등록",
    "새로 만들기, 문항 보기, 데이터셋 설명서, 학습 설정 내보내기"]],
  eval: ["평가", "3단계", [
    "데이터셋마다 모델 답과 점수, 답 파일 붙여 채점 (명령줄과 같은 숫자), 문항마다 정답과 답 나란히, 비교표"]],
  jobs: ["작업", "8단계", [
    "서식 이미지 → CLI 분석기 → html 서식, html 편집기, overlay 값 영역 초안, 작업 목록·검토·승인"]],
};
for (const k of Object.keys(PLANS)) {
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
      ${row("분석기", (i.providers || []).join(", "))}
    </tbody></table>`;
}
