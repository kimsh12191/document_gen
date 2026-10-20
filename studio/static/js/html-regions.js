// HTML의 값 영역 편집. 원본 템플릿은 유지하고 별도 영역 수정 파일을 저장한다.
"use strict";

async function viewHtmlRegions(d, variant = 'default') {
  $('#tab').innerHTML = '<p class="spin">값이 들어간 이미지와 영역을 읽는 중…</p>';
  const url = `/api/forms/${encodeURIComponent(d.id)}`;
  const [config, sources, variants] = await Promise.all([api(url + '/regions?variant='+encodeURIComponent(variant)), api('/api/sources'), api(url+'/templates')]);
  let label, page = 0, selected = -1, dirty = false, drawing = false, rows = [], seed = 0;
  state.leave = unload => !dirty || (unload ? false : confirm('저장하지 않은 영역 수정이 있습니다. 버릴까요?'));
  $('#tab').innerHTML = `<div class="sub">값 칸을 눌러 선택하고 끌어서 옮깁니다. 오른쪽 아래 모서리를 끌면 크기가 바뀝니다.
    좌표는 페이지 기준이며 같은 키가 여러 번 나오면 출력 순서로 구분합니다. 값 출처를 바꾸면 같은 키의 모든 출력에 적용합니다.
    도장·서명과 체크 보기의 영역도 선택·이동할 수 있습니다.</div>
    <div class="bar"><label>레이아웃 <select id="hr-variant">${variants.variants.map(v=>`<option value="${esc(v.id)}" ${variant===v.id?'selected':''}>${esc(v.name)}</option>`).join('')}</select></label><label>고객 seed <input id="hr-seed" type="number" min="0" max="2147483647" value="0" style="width:100px"></label>
    <button id="hr-preview">변경 미리보기</button><select id="hr-type"><option value="field">글자 칸</option><option value="seal">도장</option><option value="signature">서명</option></select><button id="hr-draw">새 영역 그리기</button>
    <button class="primary" id="hr-save">저장</button><button id="hr-reset">저장본 다시 읽기</button><span id="hr-status" class="muted"></span></div>
    <div class="bar" id="hr-pages"></div><div class="viewer ed-viewer"><div><div id="hr-stage" class="ed-stage"></div></div><div class="side panel" id="hr-side"></div></div>`;
  const mark = () => { dirty = true; $('#hr-status').textContent = '저장 안 됨 · 변경 미리보기로 값을 확인하세요'; };
  const same = (x,row) => x.key===row.key && (x.occurrence || 0)===row.occurrence && (x.target || 'field')===(row.target || 'field') && (x.option || 0)===(row.option || 0);
  const edit = row => {
    let r = config.regions.find(x => same(x,row));
    if (!r) { r = {key:row.key, occurrence:row.occurrence, target:row.target || 'field', ...(row.target==='box'?{option:row.option}:{} )}; config.regions.push(r); }
    return r;
  };
  const patch = row => config.regions.find(x => same(x,row)) || {};
  const geom = row => { const r = patch(row); return {page:r.page ?? row.page, rect:r.rect || row.rect}; };
  const draw = () => {
    if (!label) return;
    const pg = label.pages[page], scale = label.scale || 2, w = pg.width / scale, h = pg.height / scale;
    $('#hr-pages').innerHTML = label.pages.map((_,i) => `<button data-p="${i}" class="${page === i ? 'primary' : ''}">${i+1}쪽</button>`).join('');
    const stage = $('#hr-stage'); stage.style.width = `${w}px`;stage.className=`ed-stage ${drawing?'tool-text':'tool-select'}`;
    stage.innerHTML = `<img src="${esc(label.image_urls[page])}" draggable="false" alt="${esc(d.name)}"><svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">${rows.map((row,i) => {
      const g = geom(row); if (!g.rect || g.page !== page || patch(row).drop) return '';
      const [x,y,x1,y1] = g.rect;
      return `<g data-i="${i}"><rect class="ed st-auto ${selected===i?'sel subsel':''} ${row.target==='mark'?'hr-mark':''}" x="${x}" y="${y}" width="${x1-x}" height="${y1-y}"></rect>
      ${selected===i?`<rect class="handle" data-resize="1" x="${x1-5}" y="${y1-5}" width="7" height="7"></rect>`:''}<title>${esc(row.key)} · ${esc(row.text || '빈 값')}</title></g>`;
    }).join('')}</svg><div class="tip"></div>`;
    const row = rows[selected], r = row && patch(row), g = row && geom(row);
    $('#hr-side').innerHTML = `${row ? `<b>${esc(row.label || row.key)}</b><div class="mono">${esc(row.key)} · ${row.occurrence+1}번째</div>
      <div>현재 값: ${esc(row.text || '(빈 값)')}</div>
      <div>${row.target==='mark' ? row.type==='signature'?'서명':'도장' : row.target==='box'?'체크 보기 '+(row.option+1):'글자 값'}</div>
      ${row.target==='mark'?`<label><input id="hr-present" type="checkbox" ${r.present ?? row.present ? 'checked':''}> 날인·서명 있음</label>
        <label>도장 모양 <select id="hr-shape"><option value="circle" ${r.shape!=='square'?'selected':''}>원형</option><option value="square" ${r.shape==='square'?'selected':''}>사각형</option></select></label>`:''}
      <label>항목명 <input id="hr-label" value="${esc(r.label || row.label || '')}"></label>
      <label>값 출처 <input id="hr-source" list="hr-sources" value="${esc(r.source || '')}" placeholder="기존 생성 규칙 유지"></label>
      <datalist id="hr-sources">${(sources.profile || []).map(x=>`<option value="${esc(x.source)}">${esc(x.example)}</option>`).join('')}
        ${['rule:fixed','rule:empty','rule:date','rule:amount','rule:phone','rule:account'].map(x=>`<option value="${x}">`).join('')}</datalist>
      <label>고정 값 (rule:fixed) <input id="hr-text" value="${esc(r.text || '')}"></label>
      <label>글자 크기 <input id="hr-font" type="number" min="4" max="96" value="${r.font_size || 12}"></label>
      <label>쪽 <input id="hr-page" type="number" min="1" max="${label.pages.length}" value="${g.page+1}"></label>
      <div>${['왼쪽','위','오른쪽','아래'].map((s,j)=>`<label>${s} <input data-coord="${j}" type="number" min="0" step="0.5" value="${g.rect?.[j] ?? 0}"></label>`).join('')}</div>
      <div class="bar"><button id="hr-revert">이 영역 수정 취소</button><button id="hr-drop">이 출력 빼기</button></div>` : '<p>그림의 칸 또는 아래 항목을 고르세요. 새 영역은 그리기 버튼을 누르고 그림 위에서 끕니다.</p>'}
      <table><thead><tr><th>쪽</th><th>항목·값</th></tr></thead><tbody>${rows.map((x,i)=>`<tr data-row="${i}" class="click ${i===selected?'sel':''}"><td>${geom(x).page+1}</td><td>${esc(x.label || x.key)}<br>${esc(x.text || '(빈 값)')}${patch(x).drop?' · 제외':''}</td></tr>`).join('')}</tbody></table>`;
    if (row) {
      if(row.target==='box') for(const id of ['hr-source','hr-text','hr-font']) $('#'+id).disabled=true;
      if(row.target==='mark') {
        $('#hr-present').onchange=e=>{edit(row).present=e.target.checked;mark();};
        $('#hr-shape').onchange=e=>{edit(row).shape=e.target.value;mark();};
      }
      for (const [id, prop] of [['hr-label','label'],['hr-source','source'],['hr-text','text'],['hr-font','font_size']]) {
        $('#'+id).onchange = e => {
          const r = edit(row); r[prop] = prop === 'font_size' ? Number(e.target.value) : e.target.value;
          if (prop === 'source' || prop === 'text') for (const other of config.regions.filter(x=>x.key===row.key)) other[prop]=r[prop];
          mark();
        };
      }
      $('#hr-page').onchange = e => { const r=edit(row); r.page=Number(e.target.value)-1; r.rect=[...(g.rect || [0,0,120,20])]; page=r.page; mark(); draw(); };
      $$('[data-coord]').forEach(inp=>inp.onchange=()=>{const r=edit(row); r.page=g.page; r.rect=[...(g.rect || [0,0,120,20])]; r.rect[+inp.dataset.coord]=Number(inp.value); mark(); draw();});
      $('#hr-revert').onclick = () => { const idx=config.regions.indexOf(patch(row)); if(idx>=0) config.regions.splice(idx,1); mark(); draw(); };
      $('#hr-drop').onclick = () => { edit(row).drop=true; mark(); draw(); };
    }
    bindStage(stage, w, h);
  };
  const bindStage = (stage,w,h) => {
    const svg=stage.querySelector('svg');
    const point=e=>{const b=svg.getBoundingClientRect();return [Math.max(0,Math.min(w,(e.clientX-b.left)*w/b.width)),Math.max(0,Math.min(h,(e.clientY-b.top)*h/b.height))];};
    svg.onpointerdown = e => {
      const hit=e.target.closest('[data-i]'), start=point(e), resizing=e.target.hasAttribute('data-resize');
      if (!drawing && !hit) return;
      e.preventDefault();
      const index=hit?Number(hit.dataset.i):-1, before=index>=0?[...geom(rows[index]).rect]:null;
      if(index>=0) selected=index;
      svg.setPointerCapture(e.pointerId);
      let last=start;
      svg.onpointermove = ev => {
        last=point(ev);
        if(drawing) return;
        const dx=last[0]-start[0],dy=last[1]-start[1], r=edit(rows[index]);
        r.page=page;
        r.rect=resizing?[before[0],before[1],Math.max(before[0]+3,last[0]),Math.max(before[1]+3,last[1])]:
          [Math.max(0,Math.min(w-(before[2]-before[0]),before[0]+dx)),Math.max(0,Math.min(h-(before[3]-before[1]),before[1]+dy))];
        if(!resizing) r.rect.push(r.rect[0]+before[2]-before[0],r.rect[1]+before[3]-before[1]);
        r.rect=r.rect.map(x=>Math.round(x*10)/10);
        const rect=svg.querySelector(`[data-i="${index}"] rect`); const b=r.rect;
        rect.setAttribute('x',b[0]);rect.setAttribute('y',b[1]);rect.setAttribute('width',b[2]-b[0]);rect.setAttribute('height',b[3]-b[1]);
        mark();
      };
      svg.onpointerup = ev => {
        last=point(ev); svg.onpointermove=null; svg.onpointerup=null;
        if(drawing) {
          const rect=[Math.min(start[0],last[0]),Math.min(start[1],last[1]),Math.max(start[0],last[0]),Math.max(start[1],last[1])];
          if(rect[2]-rect[0]>3 && rect[3]-rect[1]>3) {
            if(selected>=0 && !geom(rows[selected]).rect) {
              const r=edit(rows[selected]);r.rect=rect;r.page=page;mark();
            } else {
            const type=$('#hr-type').value, target=type==='field'?'field':'mark', prefix=type==='field'?'added.field':type==='seal'?'seal.added':'sign.added';
            let n=1;while(rows.some(x=>x.key===`${prefix}${n}`))n++;
            const row={key:`${prefix}${n}`,target,occurrence:0,page,rect,label:type==='field'?'성명':type==='seal'?'도장':'서명',text:'',type,present:true}; rows.push(row);selected=rows.length-1;
            config.regions.push({key:row.key,target,occurrence:0,page,rect,label:row.label,source:'profile.person.name',font_size:12,...(target==='mark'?{mark_type:type,present:true}:{})});
            // text는 값 출처에 쓰는 설정에만 남긴다.
            delete config.regions.at(-1).text;
            mark();
            }
          }
          drawing=false;$('#hr-draw').classList.remove('primary');
        }
        draw();
      };
    };
  };
  const go = async () => {
    if(!$('#hr-seed').reportValidity())return;
    seed=Number($('#hr-seed').value); $('#hr-status').textContent='이미지와 실제 값을 확인하는 중…';
    try {
      label=await api(url+'/render',{seed,condition:'clean',draft:{html_regions:config},extra:{template_variants:{[d.id]:variant}}});
      const fields=new Map((label.editable_fields || []).map(f=>[f.key,f]));
      const isText=f=>!['checkbox','checkbox_multi','seal','signature'].includes(f.type);
      rows=(label.anchors || []).filter(a=>a.target!=='field' || isText(a)).map(a=>({...a,present:fields.get(a.key)?.present,text:a.target==='mark'?(fields.get(a.key)?.present?'있음':'없음'):a.text,rect:a.bbox.map(v=>v/(label.scale||2))}));
      for(const f of (label.editable_fields || []).filter(f=>!['checkbox','checkbox_multi'].includes(f.type))) if(!rows.some(a=>a.key===f.key)) rows.push({...f,target:['seal','signature'].includes(f.type)?'mark':'field',occurrence:0,page:0,rect:null,text:f.value || ''});
      page=Math.min(page,label.pages.length-1);selected=-1;draw();
      $('#hr-status').textContent=`빈 값 ${rows.filter(x=>!x.text.trim()).length} / 출력 ${rows.length}개${dirty?' · 저장 안 됨':''}`;
    }catch(e){$('#hr-status').textContent=e.message;}
  };
  $('#hr-preview').onclick=go;
  $('#hr-variant').onchange=e=>{if(!dirty||confirm('저장하지 않은 수정을 버리고 레이아웃을 바꿀까요?')){dirty=false;viewHtmlRegions(d,e.target.value);}else e.target.value=variant;};
  $('#hr-draw').onclick=()=>{drawing=!drawing;$('#hr-draw').classList.toggle('primary',drawing);};
  $('#hr-pages').onclick=e=>{if(e.target.dataset.p!==undefined){page=Number(e.target.dataset.p);draw();}};
  $('#hr-side').onclick=e=>{const i=e.target.closest('[data-row]')?.dataset.row;if(i!==undefined){selected=+i;page=geom(rows[selected]).page;draw();}};
  $('#hr-reset').onclick=()=>{if(!dirty||confirm('저장하지 않은 수정을 버릴까요?')){dirty=false;viewHtmlRegions(d,variant);}};
  $('#hr-save').onclick=async()=>{
    try{await api(url+'/regions',{...config,seed,template_variant:variant},'PUT');dirty=false;state.forms=null;delete formCache[d.id];await go();toast('영역과 값 출처를 저장했습니다');}
    catch(e){toast(e.message,true);}
  };
  await go();
}
