// guide 원문과 현재 생성 설정을 함께 읽는 사용 설명서.
"use strict";

addRoute(/^#\/guide(?:\/([^/]+))?$/, name => viewGuide(name ? decodeURIComponent(name) : "README.md"), "guide");

// 외부 HTML을 실행하지 않고 문서의 제목·표·코드·링크를 표시한다.
function guideMarkdown(text, name, documents) {
  const inline = value => {
    const tokens = [];
    const hold = html => { tokens.push(html); return `\u0000${tokens.length - 1}\u0000`; };
    let s = esc(value).replace(/`([^`]+)`/g, (_, code) => hold(`<code>${code}</code>`));
    s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label, href) => {
      if (/^https?:\/\//.test(href)) return hold(`<a href="${href}" target="_blank" rel="noopener">${label}</a>`);
      const target = new URL(href, `https://guide.local/guide/${name}`).pathname.replace(/^\/guide\//, "");
      if (documents.some(d => d.id === target)) return hold(`<a href="#/guide/${encodeURIComponent(target)}">${label}</a>`);
      if (target === "catalog.json") return hold(`<a href="/api/guide/catalog" target="_blank" rel="noopener">${label} (현재 JSON)</a>`);
      return `${label} <span class="muted">(${href})</span>`;
    });
    return s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>").replace(/\u0000(\d+)\u0000/g, (_, i) => tokens[+i]);
  };
  const lines = text.split(/\r?\n/), out = [];
  let code = null, table = false;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith("```")) {
      if (code !== null) { out.push(`<pre class="ans mono">${esc(code.join("\n"))}</pre>`); code = null; }
      else code = [];
      continue;
    }
    if (code !== null) { code.push(line); continue; }
    if (line.startsWith("|") && line.trimEnd().endsWith("|")) {
      if (/^\|[\s:|\-]+\|$/.test(line)) continue;
      const cells = line.slice(1, line.lastIndexOf("|")).split(/(?<!\\)\|/).map(x => inline(x.trim().replace(/\\\|/g, "|")));
      if (!table) { out.push("<div style='overflow:auto'><table>"); table = true; }
      out.push(`<tr>${cells.map(c => `<td>${c}</td>`).join("")}</tr>`);
      continue;
    }
    if (table) { out.push("</table></div>"); table = false; }
    const h = line.match(/^(#{1,6})\s+(.+)$/);
    if (h) out.push(`<h${h[1].length}>${inline(h[2])}</h${h[1].length}>`);
    else if (line.trim()) out.push(`<p>${inline(line)}</p>`);
  }
  if (table) out.push("</table></div>");
  return out.join("");
}

async function viewGuide(name) {
  const docs = await api("/api/guide");
  main().innerHTML = `<h1>사용 가이드</h1><div class="sub">생성 범위 → 서류·추출 항목 → 생성 요청 → 결과 사용 순서로 확인하세요. 문서와 Studio가 같은 카탈로그를 사용합니다.</div>
    <div class="bar"><select id="guide-page">${docs.map(d => `<option value="${esc(d.id)}" ${d.id === name ? "selected" : ""}>${esc(d.title)}</option>`).join("")}</select>
    <a href="#/guide/catalog.md">서류·추출 카탈로그</a><a href="#/ocr-examples">OCR 이미지·질문·정답 예시</a><a href="/api/guide/catalog" target="_blank" rel="noopener">현재 카탈로그 JSON</a></div><div id="guide-body"></div>`;
  $("#guide-page").onchange = e => { location.hash = `#/guide/${encodeURIComponent(e.target.value)}`; };
  if (name === "catalog.md") {
    const data = await api("/api/guide/catalog");
    $("#guide-body").innerHTML = `<p>${esc(data.notes)} 현재 ${data.forms.length}종.</p><input id="guide-search" placeholder="서류명·ID·필드·업무 검색" style="width:360px;max-width:100%"><div id="guide-results"></div>`;
    const draw = () => {
      const q = $("#guide-search").value.trim().toLowerCase();
      const forms = data.forms.filter(f => JSON.stringify(f).toLowerCase().includes(q));
      $("#guide-results").innerHTML = `<p>${forms.length}종</p>` + forms.map(f => `<details class="panel"><summary>${esc(f.name)} · ${esc(f.id)} · ${f.fields.length}항목</summary>${guideFormHTML(f)}</details>`).join("");
    };
    $("#guide-search").oninput = draw;
    draw();
  } else {
    const doc = await api(`/api/guide/document?name=${encodeURIComponent(name)}`);
    $("#guide-body").innerHTML = guideMarkdown(doc.markdown, name, docs);
  }
}

function guideFormHTML(f) {
  return `<p>${esc(f.description)}</p><div class="bar"><a href="#/forms/${encodeURIComponent(f.id)}/questions">실제 문항 Q/A</a><a href="#/forms/${encodeURIComponent(f.id)}">서식 미리보기·편집</a><a href="#/guide/studio.md">생성 방법</a></div>
    <p class="sub">필드 목록은 스키마 수집 결과입니다. 현재 값·문항은 문항 Q/A에서 확인하세요. 원본 키와 공통 문항 키를 함께 표시합니다.</p>
    ${!f.schema_available ? '<p>필드 목록 미수집 · 스키마 갱신 필요</p>' : `<div style="overflow:auto"><table><thead><tr><th>원본 키</th><th>문항 키</th><th>항목명</th><th>타입</th><th>값 예시</th></tr></thead><tbody>${f.fields.map(x => `<tr>${[x.key,x.question_key,x.label,x.type,typeof x.example === 'object' ? JSON.stringify(x.example) : x.example].map(v => `<td>${esc(v)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`}
    <h3>연결된 업무 · 추출/비교 시나리오</h3>${f.scenarios.length ? f.scenarios.map(s => `<details><summary>${esc(s.name)} · ${esc(s.id)}</summary><p>문서 역할: ${s.roles.map(esc).join(", ")}</p><p>${[["doc_check","구비 확인"],["cross_check","서류 대조"],["review","심사 질의"]].map(([k,n]) => `${n}: ${s.processing[k] ? "켜짐" : "꺼짐"}`).join(" · ")}</p><p>명시적 추출·비교 작업 ${s.operations.length}개. 작업이 없더라도 켜진 기본 과제는 유효한 서류·규칙에 따라 생성됩니다.</p>${guideOperationsHTML(s.operations)}<details><summary>전체 처리 설정 JSON</summary><pre class="ans mono">${esc(JSON.stringify(s.processing, null, 2))}</pre></details><a href="#/scenarios">시나리오의 서류·후보·처리 설정 확인</a></details>`).join("") : '<p>연결된 업무 없음 · 단일 서류 과제로 사용 가능</p>'}`;
}

function guideOperationsHTML(ops) {
  const ref = r => r ? `${r.doc} → ${r.common || r.key || ""}` : "";
  const operators = {equal:"같다",not_equal:"다르다",lte:"이하",gte:"이상",lt:"미만",gt:"초과"};
  return ops.length ? `<table><thead><tr><th>작업</th><th>종류</th><th>추출/비교할 항목</th><th>상태</th></tr></thead><tbody>${ops.map(op => `<tr><td>${esc(op.name || op.id)}</td><td>${op.kind === "extract" ? "추출" : "비교"}</td><td>${esc(ref(op.left))}${op.kind === "compare" ? ` / ${esc(operators[op.operator] || op.operator)} / ${esc(ref(op.right))}` : ""}</td><td>${op.enabled === false ? "꺼짐" : "켜짐"}</td></tr>`).join("")}</tbody></table>` : "";
}

async function tabGuide(d) {
  const form = await api(`/api/guide/forms/${encodeURIComponent(d.id)}`);
  $("#tab").innerHTML = guideFormHTML(form);
}
