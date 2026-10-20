// 마지막에 읽는다: 설정을 받아 오고 첫 화면을 연다.
"use strict";

(async () => {
  try {
    state.info = await api("/api/info");
    $("#nav-foot").textContent = state.info.browser ? "" : "렌더링 브라우저가 없어 미리보기는 꺼져 있습니다 (⑨ 설정)";
  } catch { /* 설정 화면에서 다시 시도 */ }
  route();
})();
