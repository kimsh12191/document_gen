"use strict";
async function viewTemplateVariants(d) {
  const url=`/api/forms/${encodeURIComponent(d.id)}/templates`;
  let config=await api(url),configDirty=false,sourceDirty=false,current='default',label=null;
  const dirty=()=>configDirty || sourceDirty;
  state.leave=unload=>!dirty() || (unload?false:confirm('저장하지 않은 레이아웃 수정이 있습니다. 버릴까요?'));
  $('#tab').innerHTML=`<div class="sub">한 서식의 문서 종류·값 생성·항목 키를 유지하면서 배치가 다른 HTML을 여러 개 둡니다. 샘플링은 고객 seed로 재현되며, 영역 수정은 레이아웃마다 따로 저장합니다.</div>
    <div class="bar"><label>생성 방식 <select id="tv-mode"><option value="sample">가중치로 하나 샘플링</option><option value="fixed">한 레이아웃 고정</option></select></label>
    <label>고정 레이아웃 <select id="tv-fixed"></select></label><button id="tv-save">샘플링 설정 저장</button><button id="tv-add">레이아웃 변형 추가</button><span id="tv-stat"></span></div>
    <div id="tv-list"></div><div class="bar"><label>편집·미리보기 <select id="tv-current"></select></label><label>고객 seed <input type="number" id="tv-seed" min="0" value="0"></label><button id="tv-show">이 레이아웃 보기</button><button id="tv-auto">샘플링 결과 보기</button><button id="tv-region">이 레이아웃 영역 편집</button></div>
    <details><summary>HTML 원본 편집</summary><textarea id="tv-source" class="mono he-text" spellcheck="false"></textarea><button id="tv-source-save">이 변형 HTML 저장</button></details><div class="bar" id="tv-pages"></div><div class="stage" id="tv-preview"></div>`;
  const mark=()=>{configDirty=true;$('#tv-stat').textContent='설정 저장 안 됨';};
  const loadSource=async()=>{const s=await api(url+'/'+encodeURIComponent(current));$('#tv-source').value=s.template;$('#tv-source').readOnly=!s.editable;$('#tv-source-save').disabled=!s.editable;};
  const draw=()=>{
    $('#tv-mode').value=config.mode;
    const opts=config.variants.map(v=>`<option value="${esc(v.id)}">${esc(v.name)}</option>`).join('');
    $('#tv-fixed').innerHTML=opts;$('#tv-fixed').value=config.fixed;$('#tv-current').innerHTML=opts;$('#tv-current').value=current;
    $('#tv-list').innerHTML=`<table><thead><tr><th>사용</th><th>레이아웃</th><th>가중치</th></tr></thead><tbody>${config.variants.map((v,i)=>`<tr data-v="${i}"><td><input data-enabled type="checkbox" ${v.enabled!==false?'checked':''}></td><td><input data-name value="${esc(v.name)}"> <span class="mono">${esc(v.id)}</span></td><td><input data-weight type="number" min="0.01" step="0.1" value="${v.weight}"></td></tr>`).join('')}</tbody></table>`;
    $$('[data-v]').forEach(row=>{const v=config.variants[+row.dataset.v];$('[data-enabled]',row).onchange=e=>{v.enabled=e.target.checked;mark();};$('[data-name]',row).onchange=e=>{v.name=e.target.value;mark();};$('[data-weight]',row).onchange=e=>{v.weight=Number(e.target.value);mark();};});
  };
  const show=async(auto=false)=>{
    $('#tv-stat').textContent='이미지 생성 중…';
    try{label=await api(`/api/forms/${encodeURIComponent(d.id)}/render`,{seed:Number($('#tv-seed').value),extra:auto?{}:{template_variants:{[d.id]:current}}});
      $('#tv-stat').textContent=`선택: ${label.template_variant.name} (${label.template_variant.id})${dirty()?' · 저장 안 된 수정 있음':''}`;
      const paint=page=>{$('#tv-preview').innerHTML=stageHTML(label,page,-1);};
      $('#tv-pages').innerHTML=label.pages.map((_,i)=>`<button data-page="${i}">${i+1}쪽</button>`).join('');$('#tv-pages').onclick=e=>{if(e.target.dataset.page!==undefined)paint(+e.target.dataset.page);};paint(0);
    }catch(e){$('#tv-stat').textContent=e.message;}
  };
  $('#tv-mode').onchange=e=>{config.mode=e.target.value;mark();};$('#tv-fixed').onchange=e=>{config.fixed=e.target.value;mark();};
  $('#tv-save').onclick=async()=>{try{config=await api(url,config,'PUT');configDirty=false;state.forms=null;delete formCache[d.id];$('#tv-stat').textContent='샘플링 설정 저장됨'+(sourceDirty?' · HTML 저장 안 됨':'');}catch(e){toast(e.message,true);}};
  $('#tv-add').onclick=async()=>{const id=prompt('새 레이아웃 ID (영문 소문자·숫자·밑줄)');if(!id)return;const name=prompt('레이아웃 이름',id);if(name===null)return;
    try{if(configDirty)await api(url,config,'PUT');if(sourceDirty)await api(url+'/'+encodeURIComponent(current),{template:$('#tv-source').value},'PUT');config=await api(url,{id,name,base:current});current=id;configDirty=false;sourceDirty=false;draw();await loadSource();toast('같은 키를 쓰는 레이아웃을 추가했습니다. HTML 배치를 편집하세요');}catch(e){toast(e.message,true);}};
  $('#tv-current').onchange=async e=>{if(sourceDirty && !confirm('저장하지 않은 HTML 수정을 버릴까요?')){e.target.value=current;return;}sourceDirty=false;current=e.target.value;await loadSource();};
  $('#tv-source').oninput=()=>{sourceDirty=true;$('#tv-stat').textContent='HTML 저장 안 됨';};
  $('#tv-source-save').onclick=async()=>{try{await api(url+'/'+encodeURIComponent(current),{template:$('#tv-source').value},'PUT');sourceDirty=false;await show();}catch(e){toast(e.message,true);}};
  $('#tv-show').onclick=()=>show();$('#tv-auto').onclick=()=>show(true);
  $('#tv-region').onclick=()=>{if(!dirty()||confirm('저장하지 않은 수정을 버리고 영역 편집으로 갈까요?')){configDirty=false;sourceDirty=false;viewHtmlRegions(d,current);}};
  draw();await loadSource();await show();
}
