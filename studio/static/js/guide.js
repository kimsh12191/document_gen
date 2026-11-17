// guide 원문과 현재 생성 설정을 함께 읽는 사용 설명서.
"use strict";

addRoute(/^#\/guide(?:\/([^/]+))?$/, name => viewGuide(name ? decodeURIComponent(name) : "studio.md"), "guide");

// 외부 HTML을 실행하지 않고 문서의 제목·표·코드·링크를 표시한다.
function guideMarkdown(text, name, documents) {
  const inline = value => {
    const tokens = [];
    const hold = html => { tokens.push(html); return `\u0000${tokens.length - 1}\u0000`; };
    let s = esc(value).replace(/`([^`]+)`/g, (_, code) => hold(`<code>${code}</code>`));
    s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label, href) => {
      if (/^https?:\/\//.test(href)) return hold(`<a href="${href}" target="_blank" rel="noopener">${label}</a>`);
      const base = /^(docgen|docker)\//.test(name) ? `https://guide.local/${name}` : `https://guide.local/guide/${name}`;   // docgen/manual 문서는 저장소 기준 경로
      const url = new URL(href, base), path = decodeURIComponent(url.pathname);
      const target = path.startsWith("/guide/") ? path.slice(7) : path.slice(1);
      const at = url.hash ? "#" + decodeURIComponent(url.hash.slice(1)) : "";   // 문서 안 절로
      if (documents.some(d => d.id === target)) return hold(`<a href="#/guide/${encodeURIComponent(target)}${at}">${label}</a>`);
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
    if (line.trimStart().startsWith("|") && line.trimEnd().endsWith("|")) {   // 목록 안에 들여 쓴 표도
      const row = line.trim();
      if (/^\|[\s:|\-]+\|$/.test(row)) continue;
      const cells = row.slice(1, row.lastIndexOf("|")).split(/(?<!\\)\|/).map(x => inline(x.trim().replace(/\\\|/g, "|")));
      if (!table) { out.push("<div style='overflow:auto'><table>"); table = true; }
      out.push(`<tr>${cells.map(c => `<td>${c}</td>`).join("")}</tr>`);
      continue;
    }
    if (table) { out.push("</table></div>"); table = false; }
    const h = line.match(/^(#{1,6})\s+(.+)$/);
    if (/^-{3,}$/.test(line.trim())) out.push("<hr>");
    else if (h) out.push(`<h${h[1].length} id="${esc(guideSlug(h[2]))}">${inline(h[2])}</h${h[1].length}>`);
    else if (line.trim()) out.push(`<p>${inline(line)}</p>`);
  }
  if (table) out.push("</table></div>");
  return out.join("");
}

// 제목 → 링크 이름 (GitHub 과 같은 규칙: 소문자, 글자·숫자·한글·-·공백만 남기고 공백은 -)
function guideSlug(title) {
  return title.replace(/\[([^\]]*)\]\([^)]*\)/g, "$1").replace(/[`*]/g, "").trim().toLowerCase()
    .replace(/[^\w\- 가-힣]/g, "").replace(/ /g, "-");
}

async function viewGuide(name) {
  const [docName, anchor] = name.split("#");
  name = docName;
  const docs = await api("/api/guide");
  main().innerHTML = `<h1>사용 가이드</h1><div class="sub">화면 쓰는 법만 모았습니다. 처음이면 <a href="#/guide/studio.md">studio 사용법</a> (할 일별로). 학습·평가·OCR 준비는 학습 서버 쪽 문서(저장소 <span class="mono">guide/train/</span>)에 있습니다.</div>
    <div class="bar"><select id="guide-page">${docs.map(d => `<option value="${esc(d.id)}" ${d.id === name ? "selected" : ""}>${esc(d.title)}</option>`).join("")}</select>
    <a href="#/ocr-examples">OCR 이미지·질문·정답 예시</a></div><div id="guide-body"></div>`;
  $("#guide-page").onchange = e => { location.hash = `#/guide/${encodeURIComponent(e.target.value)}`; };
  const doc = await api(`/api/guide/document?name=${encodeURIComponent(name)}`);
  $("#guide-body").innerHTML = guideMarkdown(doc.markdown, name, docs);
  const at = anchor && document.getElementById(anchor);
  if (at) at.scrollIntoView();
}
