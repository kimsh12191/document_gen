"use strict";

const TRACKING_TITLE = {task_group:"업무·과제 그룹",scenario:"업무 시나리오",task:"과제",label_format:"정답 구조",doc_type:"서식",source_dataset:"원본 데이터셋"};
const trackName = value => ({ocr:"OCR",doc:"문서 이해",work:"은행 업무",not_applicable:"해당 없음 (단일 서류·OCR)",unknown:"미기록",text:"텍스트",text_boxes:"글자·좌표",text_list:"문자열 목록",key_values:"키·값 추출",mark_states:"체크·도장·서명",document_sets:"서류 구비 목록",consistency_issues:"불일치 판단·근거",scalar:"계산·판단 값"}[value] || value);

async function dsTracking(d) {
  let summary;
  try { summary = await api(`/api/datasets/${encodeURIComponent(d.id)}/composition`); }
  catch(e) { $("#tab").innerHTML=`<p class="warn">구성·추적 정보를 읽지 못했습니다. 변경 전 서버라면 Studio를 재시작하세요.</p><p>${esc(e.message)}</p><a href="#/datasets/${encodeURIComponent(d.id)}/items">기존 문항 보기</a>`; return; }
  $("#tab").innerHTML = `<h2>생성 구성과 평가 추적</h2><p>업무·시나리오·정답 구조별 문항을 확인하고, 같은 구분으로 채점 결과를 봅니다. 과제가 다르면 점수를 평균내지 않습니다.</p>
    <div class="bar"><label>범위 <select id="tracking-scope"><option value="all">전체 문항 (${summary.all.n})</option><option value="evaluation">평가 문항 (${summary.evaluation.n})</option></select></label><a href="#/guide/benchmark-tracking.md">분류·보고서 안내</a></div>
    <div id="tracking-composition"></div>
    <details class="panel"><summary>생성 레시피·버전·서식 해시</summary><pre class="ans mono">${esc(JSON.stringify(summary.provenance,null,2))}</pre></details>
    <h2>구분별 평가 결과</h2><div class="bar"><label>채점 결과 <select id="tracking-score"><option value="">선택</option>${d.scores.map(s=>`<option value="${esc(s.pid)}">${esc(s.label || s.pid)} · ${esc(s.scored_at || '')}</option>`).join("")}</select></label><label>구분 <select id="tracking-dimension">${["scenario","task_group","label_format","doc_type","source_dataset"].map(key=>`<option value="${key}">${TRACKING_TITLE[key]}</option>`).join("")}<option value="field_kind">필드 타입 · 항목 단위</option></select></label><a href="#/datasets/${encodeURIComponent(d.id)}/runs">모델 답 연결·채점</a></div><div id="tracking-scores"><p class="muted">모델 답을 연결·채점한 후 결과를 선택하세요.</p></div>`;
  const draw = () => {
    const c = summary[$("#tracking-scope").value];
    $("#tracking-composition").innerHTML = `<p class="sub">${esc(c.notes)}</p><div style="overflow:auto"><table><thead><tr><th>업무·과제 그룹</th><th>시나리오</th><th>과제</th><th>정답 구조</th><th>문항 수</th></tr></thead><tbody>${c.rows.map((r,i)=>`<tr><td>${esc(trackName(r.task_group))}</td><td>${esc(trackName(r.scenario))}</td><td>${esc(r.task)}</td><td>${esc(trackName(r.label_format))}</td><td><button data-tracking-row="${i}">${r.n} · 문항 보기</button></td></tr>`).join("")}</tbody></table></div><details><summary>필드 타입별 구성 (문항 수와 별도)</summary><table><thead><tr><th>필드 타입</th><th>필드 수</th></tr></thead><tbody>${Object.entries(c.field_kind_counts).map(([kind,n])=>`<tr><td>${esc(kind)}</td><td>${n}</td></tr>`).join("") || '<tr><td colspan="2">필드 타입 기록 없음</td></tr>'}</tbody></table></details>`;
    $$("[data-tracking-row]").forEach(btn=>btn.onclick=()=>{
      const r=c.rows[+btn.dataset.trackingRow];
      store.set(`ds.${d.id}`, {task:r.task,pids:[],order:"id",evaluationOnly:$("#tracking-scope").value === "evaluation",filters:{task_group:r.task_group,scenario:r.scenario,label_format:r.label_format}});
      location.hash=`#/datasets/${encodeURIComponent(d.id)}/items`;
    });
  };
  let scores = null;
  const drawScores = () => {
    if(!scores)return;
    if(!scores.available){$("#tracking-scores").innerHTML='<p>이전 채점 결과입니다. 모델 답 탭에서 다시 채점하면 구분별 점수가 생성됩니다.</p>';return;}
    const key=$("#tracking-dimension").value;
    if(key === "field_kind") {
      const rows=[["kie","kind"],["marks","type"]].flatMap(([task,slice])=>Object.entries(scores.tasks?.[task]?.slices?.[slice] || {}).map(([kind,r])=>({task,kind,...r})));
      $("#tracking-scores").innerHTML=`<p class="sub">KIE·체크/도장/서명 문항의 필드별 값 정확도입니다. n은 항목 수이며 문항 단위 위치 F1과 다릅니다.</p><table><thead><tr><th>과제</th><th>필드 타입</th><th>항목 수</th><th>값 정확도 (%)</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(r.task)}</td><td>${esc(r.kind)}</td><td>${r.n}</td><td>${r.acc==null?'—':(100*r.acc).toFixed(1)}</td></tr>`).join('') || '<tr><td colspan="4">필드 타입별 점수가 없습니다.</td></tr>'}</tbody></table>`;
      return;
    }
    const groups=scores.breakdowns[key]||{};
    const rows=Object.entries(groups).flatMap(([name,b])=>Object.entries(b.tasks).map(([task,s])=>({name,task,...s})));
    $("#tracking-scores").innerHTML=`<p class="sub">평가 문항만 채점합니다. n은 문항 수. CER·오탐률은 낮을수록 좋습니다.</p><div style="overflow:auto"><table><thead><tr><th>${TRACKING_TITLE[key]}</th><th>과제</th><th>문항 수</th><th>주 지표</th><th>점수 (%)</th><th>예측 없음</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(trackName(r.name))}</td><td>${esc(r.task)}</td><td>${r.n}</td><td>${esc(r.main)}</td><td>${r.metrics[r.main]==null?'—':(100*r.metrics[r.main]).toFixed(1)}</td><td>${r.missing}</td></tr>`).join("")}</tbody></table></div>`;
  };
  $("#tracking-scope").onchange=draw;
  $("#tracking-score").onchange=async()=>{const pid=$("#tracking-score").value;if(!pid){scores=null;$("#tracking-scores").innerHTML='채점 결과를 선택하세요.';return;}try{scores=await api(`/api/datasets/${encodeURIComponent(d.id)}/breakdowns?pid=${encodeURIComponent(pid)}`);drawScores();}catch(e){toast(e.message,true);}};
  $("#tracking-dimension").onchange=drawScores;
  draw();
}
