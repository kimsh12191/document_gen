// 설정 화면 (설정 요약). 서버: /api/info
"use strict";

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
      ${row("실서류에서 만든 서식 (private_forms_dir)", i.paths.private_forms_dir)}
    </tbody></table>`;
}
