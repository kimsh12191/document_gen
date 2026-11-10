// ⑥ 데이터셋 › 구성: 과제·정답 구조별 문항 수, 생성 레시피·버전. 서버: GET /api/datasets/{id}/composition
"use strict";

const TRACKING_TITLE = {task_group:"과제 그룹",task:"과제",label_format:"정답 구조",doc_type:"서식",source_dataset:"원본 데이터셋"};
const trackName = value => ({ocr:"OCR",doc:"문서 이해",not_applicable:"해당 없음 (단일 서류·OCR)",unknown:"미기록",text:"텍스트",text_boxes:"글자·좌표",text_list:"문자열 목록",key_values:"키·값 추출",mark_states:"체크·도장·서명",scalar:"계산·판단 값"}[value] || value);

async function dsTracking(d) {
  let summary;
  try { summary = await api(`/api/datasets/${encodeURIComponent(d.id)}/composition`); }
  catch(e) { $("#tab").innerHTML=`<p class="warn">구성 정보를 읽지 못했습니다.</p><p>${esc(e.message)}</p><a href="#/datasets/${encodeURIComponent(d.id)}/items">기존 문항 보기</a>`; return; }
  $("#tab").innerHTML = `<h2>생성 구성</h2><p>과제·정답 구조별 문항 수입니다. 같은 구분의 점수는 학습 서버 결과 보고서에서 봅니다 (guide/results.md).</p>
    <div class="bar"><label>범위 <select id="tracking-scope"><option value="all">전체 문항 (${summary.all.n})</option><option value="evaluation">평가 문항 (${summary.evaluation.n})</option></select></label><a href="#/guide/results.md">결과 보고서 안내</a></div>
    <div id="tracking-composition"></div>
    <details class="panel"><summary>생성 레시피·버전·서식 해시</summary><pre class="ans mono">${esc(JSON.stringify(summary.provenance,null,2))}</pre></details>`;
  const draw = () => {
    const c = summary[$("#tracking-scope").value];
    $("#tracking-composition").innerHTML = `<p class="sub">${esc(c.notes)}</p><div style="overflow:auto"><table><thead><tr><th>과제 그룹</th><th>과제</th><th>정답 구조</th><th>문항 수</th></tr></thead><tbody>${c.rows.map((r,i)=>`<tr><td>${esc(trackName(r.task_group))}</td><td>${esc(r.task)}</td><td>${esc(trackName(r.label_format))}</td><td><button data-tracking-row="${i}">${r.n} · 문항 보기</button></td></tr>`).join("")}</tbody></table></div><details><summary>필드 타입별 구성 (문항 수와 별도)</summary><table><thead><tr><th>필드 타입</th><th>필드 수</th></tr></thead><tbody>${Object.entries(c.field_kind_counts).map(([kind,n])=>`<tr><td>${esc(kind)}</td><td>${n}</td></tr>`).join("") || '<tr><td colspan="2">필드 타입 기록 없음</td></tr>'}</tbody></table></details>`;
    $$("[data-tracking-row]").forEach(btn=>btn.onclick=()=>{
      const r=c.rows[+btn.dataset.trackingRow];
      store.set(`ds.${d.id}`, {task:r.task,evaluationOnly:$("#tracking-scope").value === "evaluation",filters:{task_group:r.task_group,label_format:r.label_format}});
      location.hash=`#/datasets/${encodeURIComponent(d.id)}/items`;
    });
  };
  $("#tracking-scope").onchange=draw;
  draw();
}
