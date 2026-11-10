// 새 서식 추가: 서식 그림을 올려 그림 위에 칸을 그리는 overlay 서식(img_*)을 만든다 (studio/drawn.py → 영역 편집).
// 자세한 절차는 guide/new-forms.md. 이미 있는 html 서식은 코드로 고친다 (docgen/forms/README.md).
"use strict";

addRoute(/^#\/new-forms$/, () => viewNewForms(), "new-forms");

async function viewNewForms() {
  main().innerHTML = `
    <h1>새 서식 추가</h1>
    <div class="sub">서식 그림을 올리면 그 그림을 배경으로 하는 서식 <span class="mono">img_*</span> 를 만들고 바로 <b>영역 편집</b>으로 갑니다.
      영역 편집에서 칸을 그리고(표는 <b>표 그리기</b>로 열 × 행을 한 번에) 칸마다 <b>키</b> · <b>키 설명</b> · <b>생성 방법</b>을 정하면
      분류·내용 추출(kie)·체크·표·OCR 문항이 생깁니다. 자세한 설명은 <a href="#/guide/new-forms.md">새 서식 추가 가이드</a>.</div>
    <div class="box" style="margin:8px 0" id="nf-draw">
      <div class="bar" style="flex-wrap:wrap;gap:8px">
        <label>그림 (PNG·JPG·PDF, 여러 쪽이면 쪽 순서대로) <input type="file" id="nf-files" multiple accept=".png,.jpg,.jpeg,.tif,.tiff,.bmp,.webp,.pdf"></label>
        <label>서식 ID <input type="text" id="nf-id" placeholder="img_payslip_a" size="22" class="mono"></label>
        <label>서식 이름 <input type="text" id="nf-name" placeholder="급여명세서" size="22"></label>
        <label title="값이 적힌 실제 서류에서 가져온 그림이면 켭니다. 사내 서식 폴더(private_forms_dir)에만 만듭니다"><input type="checkbox" id="nf-real" checked> 실서류 견본 (값이 적힌 서류)</label>
        <button class="primary" id="nf-create">만들고 영역 편집으로</button>
      </div>
      <div class="muted" style="font-size:12px">서식 이름 = 문서 분류의 정답입니다. 실서류 견본이면 남아 있는 값을 영역 편집의 <b>지우기</b>로 덮어야 합니다 (안 지우면 그 값이 생성 그림마다 복제됨).
        배경 글자(그림 속 인쇄 글자)는 영역 편집에서 <b>사내 OCR 로 읽기</b>를 해야 <b>합성 OCR 세트</b>(쪽 전체 받아쓰기 정답)에 들어갑니다.
        칸끼리 관계(합계·날짜 순서)는 서식 폴더 <span class="mono">generate.py</span> (<a href="#/guide/generators.md">generators.md</a>).</div>
      <div id="nf-draw-out"></div>
    </div>`;
  $("#nf-create").onclick = () => createDrawn();
}

// A. 그림 위에 그려서: 그림 → 빈 overlay 서식 img_* (studio/drawn.py) → 영역 편집
async function createDrawn() {
  const files = [...$("#nf-files").files], id = $("#nf-id").value.trim(), name = $("#nf-name").value.trim();
  if (!files.length) return toast("서식 그림을 고르세요", true);
  if (!/^img_[a-z0-9_]{2,40}$/.test(id)) return toast("서식 ID 는 img_ 로 시작하는 영어 소문자·숫자·밑줄 (예: img_payslip_a)", true);
  if (!name) return toast("서식 이름을 적으세요 (문서 분류의 정답)", true);
  const fd = new FormData();
  files.forEach(f => fd.append("files", f));
  fd.append("form_id", id);
  fd.append("name", name);
  fd.append("real_data", $("#nf-real").checked ? "true" : "false");
  const b = $("#nf-create"), out = $("#nf-draw-out");
  b.disabled = true;
  out.innerHTML = `<p class="spin">서식을 만드는 중… (${files.length}개 파일)</p>`;
  try {
    const r = await fetch("/api/forms/new-image", { method: "POST", body: fd });
    const data = await r.json().catch(() => ({}));
    if (r.status === 404 || r.status === 405)   // 화면(js)만 새것이고 서버는 예전 코드
      throw new Error(`서버에 이 기능이 없습니다 (${r.status}). git pull 뒤 studio 서버를 다시 띄우세요 (도커면 컨테이너 재시작)`);
    if (!r.ok) throw new Error(typeof data.detail === "string" ? data.detail : `${r.status} ${r.statusText}`);
    out.innerHTML = `<p>만들었습니다: <a href="#/forms/${encodeURIComponent(data.form_id)}/edit">${esc(data.form_id)} 영역 편집</a></p>`;
    state.forms = null;
    toast(`만들었습니다: ${data.form_id} (${data.pages}쪽${data.private ? ", 사내 서식 폴더" : ""})`);
    location.hash = `#/forms/${encodeURIComponent(data.form_id)}/edit`;
  } catch (e) {
    out.innerHTML = `<p class="err">만들지 못했습니다: ${esc(e.message)}</p>`;
    out.scrollIntoView({ block: "center" });
    toast(e.message, true);
  } finally {
    b.disabled = false;
  }
}
