"use strict";

function benchmarkConfigEditor(datasets, selected) {
  let nextId = 1;
  const create = chosen => ({id:`benchmark_${nextId++}`,name:chosen?.name || "새 벤치마크",group:chosen ? `${chosen.real_data ? 'real' : 'synthetic'}_${chosen.groups?.every(x=>x==='ocr')?'ocr':'bank'}` : "ungrouped",datasets:chosen?[chosen.id]:[]});
  let units = [create(datasets.find(x=>x.id===selected))];
  const read = () => $$("[data-benchmark-unit]").map(panel=>({
    id:$("[data-unit-id]",panel).value.trim(),name:$("[data-unit-name]",panel).value.trim(),group:$("[data-unit-group]",panel).value.trim(),
    datasets:$$('[data-unit-dataset]:checked',panel).map(x=>x.value)
  }));
  const draw = () => {
    $("#benchmark-units").innerHTML=units.map((u,i)=>`<section class="panel" data-benchmark-unit="${i}" style="margin:8px 0">
      <div class="bar"><label>ID <input data-unit-id value="${esc(u.id)}" pattern="[A-Za-z0-9][A-Za-z0-9_.-]*"></label><label>표시 이름 <input data-unit-name value="${esc(u.name)}"></label><label>보고서 분류 group <input data-unit-group value="${esc(u.group)}" list="benchmark-group-names"></label><button type="button" data-unit-remove="${i}">평가 단위 삭제</button></div>
      <p class="sub">아래에서 선택한 데이터셋들을 합쳐 이 ID의 과제별 점수를 계산합니다.</p>
      ${datasets.map(d=>`<label style="display:block"><input type="checkbox" data-unit-dataset value="${esc(d.id)}" ${u.datasets.includes(d.id)?'checked':''}>${esc(d.name)} · ${esc(d.id)} ${dsTag(d)} <span class="tag">${d.real_data?'실데이터':'합성/기타'}</span> <span class="muted">정답: ${esc({exact:'생성 정답',pseudo:'의사정답',reviewed:'사람 검수'}[d.gt]||d.gt||'미기록')}</span></label>`).join('') || '<p>선택할 평가 데이터셋이 없습니다.</p>'}
      </section>`).join('');
    $$('[data-unit-remove]').forEach(btn=>btn.onclick=()=>{units=read();units.splice(+btn.dataset.unitRemove,1);draw();});
  };
  return {html:`<div class="fld"><b>벤치마크 평가 단위</b><p class="sub">하나의 ID·이름에 데이터셋 여러 개를 선택할 수 있습니다. 같은 group은 보고서에서 모아 보여주며 점수는 합치지 않습니다.</p><datalist id="benchmark-group-names">${['real_ocr','synthetic_ocr','real_bank','synthetic_bank','ungrouped'].map(x=>`<option value="${x}">`).join('')}</datalist><div id="benchmark-units"></div><button type="button" id="benchmark-add">평가 단위 추가</button></div>`,
    mount(){draw();$("#benchmark-add").onclick=()=>{units=read();units.push(create());draw();};},read};
}
