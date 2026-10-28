// 새 서식 추가 안내 (한 화면 요약). 자세한 절차는 guide/new-forms.md, 결과물 형식은 docgen/manual/NEW_FORM_SPEC.md.
// 지시문·옮기기 명령은 guide/new-forms.md 의 코드 블록을 그대로 읽어 보여 준다 (문서와 화면이 어긋나지 않게).
"use strict";

addRoute(/^#\/new-forms$/, () => viewNewForms(), "new-forms");

// 마크다운에서 제목(heading 으로 시작하는 줄) 다음 첫 코드 블록
function mdBlock(md, heading) {
  const lines = md.split(/\r?\n/);
  let i = lines.findIndex(l => l.startsWith("#") && l.includes(heading));
  if (i < 0) return "";
  while (++i < lines.length && !lines[i].startsWith("```"));
  const out = [];
  while (++i < lines.length && !lines[i].startsWith("```")) out.push(lines[i]);
  return out.join("\n");
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    toast("복사했습니다");
  } catch {
    toast("복사하지 못했습니다. 상자 안 글자를 직접 선택해 복사하세요", true);
  }
}

async function viewNewForms() {
  const doc = await api(`/api/guide/document?name=${encodeURIComponent("new-forms.md")}`);
  const md = doc.markdown;
  const prompt = mdBlock(md, "지시문"), install = mdBlock(md, "studio 에 넣기");
  const spec = `#/guide/${encodeURIComponent("docgen/manual/NEW_FORM_SPEC.md")}`;
  const step = (n, title, body) => `<div class="box" style="margin:8px 0"><h3 style="margin:0 0 6px">${n}. ${title}</h3>${body}</div>`;
  const code = (id, text) => `<div class="bar"><button data-copy="${id}">복사</button></div><pre class="ans mono" id="${id}" style="max-height:320px;overflow:auto">${esc(text)}</pre>`;
  main().innerHTML = `
    <h1>새 서식 추가</h1>
    <div class="sub">서식 그림 한 장 → <b>대형 모델</b>이 html 서식과 키를 만들고 → 사람이 검사해 넣고 → studio 에서 손보고 검수합니다.
      자세한 설명은 <a href="#/guide/new-forms.md">새 서식 추가 가이드</a>, 결과물 형식은 <a href="${spec}">NEW_FORM_SPEC</a>.</div>
    <div class="box kr" style="margin:8px 0">외부 모델(클로드 등)에는 <b>빈 서식·공개 서식 그림만</b> 보냅니다. 값이 적힌 실서류 견본은 사내 모델로만 (AGENTS.md 규칙 10).</div>

    ${step(1, "모델에게 맡기기", `
      <p>넘길 것: 서식 그림, <a href="${spec}">NEW_FORM_SPEC.md</a>(통째로), 키 사전 <span class="mono">docgen/dictionary/common.json</span>·<span class="mono">docgen/keys.json</span>.
        아래 지시문의 <span class="mono">&lt;…&gt;</span> 만 바꿔 붙여 넣습니다.</p>
      <p>모델이 만드는 것:</p>
      <pre class="ans mono">&lt;이름&gt;/
  template.html.j2   모양 + 값 자리 — 값은 모두 f("키", label="원본 항목명")
  form.json          서식 이름·그룹 + 칸 목록 (키마다 항목명·타입·값 출처, 반복 표 행 수)
  generate.py        (선택) 칸끼리 관계 맞추기: 시작일 ≤ 종료일, 합계, 잔액, 조건부 칸
  source.png         (선택) 원본 그림</pre>
      ${prompt ? code("nf-prompt", prompt) : `<p class="muted">지시문을 문서에서 찾지 못했습니다 — 가이드 3절을 보세요.</p>`}`)}

    ${step(2, "검사", `
      <p>행 최소·최대로 그려 봅니다. 마지막 줄 JSON 에서 <span class="mono">overflow: false</span>, <span class="mono">checks: []</span>, 쪽 수가 원본과 같은지,
        그림이 원본과 비슷한지 봅니다. <b>generate.py 가 있으면 사람이 읽습니다</b> (그림마다 실행되는 코드).</p>
      ${code("nf-check", "python -m docgen.preview --dir work/<이름> --rows min --out work/check_min\npython -m docgen.preview --dir work/<이름> --rows max --out work/check_max")}`)}

    ${step(3, "studio 에 넣기", `
      <p>초안 폴더를 서식 폴더(<span class="mono">docgen/forms/&lt;ID&gt;/</span>, 실서류에서 만든 것은 사내 서식 폴더)로 옮기고 <b>서식 다시 읽기</b>를 누릅니다.
        저장소 루트에서:</p>
      ${install ? code("nf-install", install) : `<p class="muted">명령을 문서에서 찾지 못했습니다 — 가이드 5절을 보세요.</p>`}
      <div class="bar"><button class="primary" id="nf-refresh">서식 다시 읽기</button></div>
      <div id="nf-refreshed">${refreshNote(state.refreshed)}</div>`)}

    ${step(4, "손보고 검수", `
      <table><tbody>
        <tr><td>값 출처, 단독 칸 추가·위치</td><td>① 서식 › <b>영역 편집</b></td></tr>
        <tr><td>체크·도장·서명, 반복 표 안의 칸, 표 구조·문구</td><td>① 서식 › <b>html 편집</b> (템플릿)</td></tr>
        <tr><td>칸끼리 관계</td><td>서식 폴더의 <span class="mono">generate.py</span> (파일 탭에서 내용 확인)</td></tr>
        <tr><td>원본과 나란히 보고 확인</td><td>① 서식 › <b>검수</b> › 검수 완료</td></tr>
      </tbody></table>
      <p class="muted">html 서식은 검수 전이어도 레시피의 "all"·그룹 선택에 들어갑니다. 검수한 것만 쓰려면 레시피의 <b>검수 완료 서식만</b>을 켭니다.</p>`)}`;
  $("#nf-refreshed").addEventListener("click", e => { if (e.target.closest("[data-close]")) $("#nf-refreshed").innerHTML = ""; });
  main().querySelectorAll("[data-copy]").forEach(b => { b.onclick = () => copyText($(`#${b.dataset.copy}`).textContent); });
  $("#nf-refresh").onclick = async () => {
    const b = $("#nf-refresh");
    b.disabled = true;
    try {
      state.refreshed = await api("/api/forms/refresh", {});
      state.forms = null;
      const r = state.refreshed;
      $("#nf-refreshed").innerHTML = refreshNote(r);
      toast(`서식 다시 읽기: 새로 ${r.added.length} · 바뀜 ${r.updated.length} · 빠짐 ${r.removed.length} · 문제 ${r.problems.length}`, r.problems.length > 0);
    } catch (e) {
      toast(e.message, true);
    } finally {
      b.disabled = false;
    }
  };
}
