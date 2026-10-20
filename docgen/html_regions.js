// 페이지 나눔 후 적용. 글자·날인·서명·체크 위치와 라벨을 함께 옮긴다.
() => {
  const config = document.getElementById('docgen-html-regions');
  if (!config) return;
  const {regions, mark_art = {}} = JSON.parse(config.textContent);
  const pages = [...document.querySelectorAll('.page')], nodes = new Map();
  const ident = (target,key,option=0) => JSON.stringify([target,key,option]);
  const register = (target,key,option,el,attr) => {
    const id=ident(target,key,option);
    if(!nodes.has(id)) nodes.set(id,[]);
    const occurrence=nodes.get(id).length;
    el.__regionOccurrences ||= {};
    el.__regionOccurrences[id]=occurrence;
    if(target==='field') el.dataset.regionOccurrence=occurrence;
    nodes.get(id).push({el,attr});
  };
  for(const el of document.querySelectorAll('[data-field]')) register('field',el.dataset.field,0,el,'data-field');
  for(const el of document.querySelectorAll('[data-mark], [data-mark2]')) {
    for(const attr of ['data-mark','data-mark2']) if(el.hasAttribute(attr)) register('mark',el.getAttribute(attr),0,el,attr);
  }
  for(const el of document.querySelectorAll('[data-box]')) {
    const [key,opt]=el.dataset.box.split('#');register('box',key,Number(opt || 0),el,'data-box');
  }
  const detach = (el,attr,containerOnly=false) => {
    if(containerOnly) {el.removeAttribute(attr); return;}
    const placeholder=el.cloneNode(true);
    for(const p of [placeholder,...placeholder.querySelectorAll('*')]) for(const a of ['data-field','data-mark','data-mark2','data-box','data-opt']) p.removeAttribute(a);
    placeholder.style.visibility='hidden';el.replaceWith(placeholder);
  };
  for(const r of regions) {
    const target=r.target || 'field', option=r.option || 0, id=ident(target,r.key,option), occurrence=r.occurrence || 0;
    const found=nodes.get(id)?.[occurrence];let el=found?.el, attr=found?.attr;
    let pageIndex=r.page, rect=r.rect;
    if(el && !rect) {
      pageIndex=pages.indexOf(el.closest('.page'));
      if(pageIndex>=0) {const a=el.getBoundingClientRect(),b=pages[pageIndex].getBoundingClientRect();rect=[a.left-b.left,a.top-b.top,a.right-b.left,a.bottom-b.top];}
    }
    const isMarkContainer=target==='mark' && el && !el.matches('.seal,.scribble,.seal-missing,.html-region-art');
    if(r.drop) {if(el) detach(el,attr,isMarkContainer);continue;}
    if(!rect) continue;
    const page=pages[pageIndex];
    if(!page) throw new Error('값 영역 '+r.key+': '+(pageIndex+1)+'쪽이 없습니다');
    const [x0,y0,x1,y1]=rect;
    if(x1>page.clientWidth+1 || y1>page.clientHeight+1) throw new Error('값 영역 '+r.key+': 페이지 밖 좌표입니다');
    if(target==='mark') {
      if(el) detach(el,attr,isMarkContainer);
      el=document.createElement('span');el.className='html-region-art';el.setAttribute('data-mark',r.key);
      el.innerHTML=mark_art[r.key] || '';
      Object.assign(el.style,{display:'flex',width:'100%',height:'100%',alignItems:'center',justifyContent:'center'});
      for(const svg of el.querySelectorAll('svg')) {
        if(!svg.hasAttribute('viewBox')) svg.setAttribute('viewBox','0 0 '+(parseFloat(svg.getAttribute('width')) || 100)+' '+(parseFloat(svg.getAttribute('height')) || 40));
        Object.assign(svg.style,{width:'100%',height:'100%',maxWidth:'100%',maxHeight:'100%'});
      }
    } else {
      if(!el) continue;
      detach(el,attr);
    }
    el.__regionOccurrences ||= {};el.__regionOccurrences[id]=occurrence;
    if(target==='field') el.dataset.regionOccurrence=occurrence;
    page.style.position='relative';
    const holder=document.createElement('div');holder.className='html-value-region';
    Object.assign(holder.style,{position:'absolute',left:x0+'px',top:y0+'px',width:(x1-x0)+'px',height:(y1-y0)+'px',
      display:'flex',alignItems:'center',overflow:'hidden',zIndex:'30',lineHeight:'1.15'});
    if(target==='field') {
      Object.assign(holder.style,{color:'#152b57',fontSize:(r.font_size || 12)+'px'});
      Object.assign(el.style,{position:'static',display:'inline-block',transform:'none',font:'inherit',color:'inherit'});
    } else if(target==='box') Object.assign(el.style,{position:'relative',left:'0',top:'0',width:'100%',height:'100%',transform:'none'});
    holder.append(el);page.append(holder);
    if(target==='field' && el.scrollWidth>x1-x0) holder.style.fontSize=Math.max(4,(r.font_size || 12)*(x1-x0)/el.scrollWidth)+'px';
  }
}
