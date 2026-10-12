"""Look at the model's OCR by eye: a small local web page in front of a running server.

    python ocr_viewer.py --endpoint http://127.0.0.1:8000/v1
    python ocr_viewer.py --endpoint http://127.0.0.1:8000/v1 --tasks data/prepared-v2/benchmark_tasks.jsonl
    python ocr_viewer.py --tasks data/prepared-v2/benchmark_tasks.jsonl --predictions runs/exp1/predictions/base.jsonl

Open http://127.0.0.1:7860 (VS Code forwards the port). Two panels:
  * Free test: any image (server path or upload) -> spotting / find text / read a dragged
    region / relation / custom prompt. The image is resized exactly like prepare does.
  * Benchmark sample: a random prepared question with its OCR reference (green) next to the
    model answer (red) and the GRPO reward. With --predictions it shows stored answers and
    needs no server.
"""
import argparse
import base64
import io
import json
import os
import random
import re
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageOps

from bank_ocr.augment import fit_scale
from bank_ocr.data import dumps, normalize_box, read_jsonl
from bank_ocr.inference import index_predictions
from bank_ocr.metrics import BOX_TASKS, answer, parse_boxes, parse_target, reward
from bank_ocr.tasks import DIRECTIONS, PROMPTS

PROMPT_BOX = re.compile(r"bbox_2d=(\[\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\])")


def png_bytes(im):
    buffer = io.BytesIO()
    im.save(buffer, "PNG")
    return buffer.getvalue()


def data_url(im, quality=90):
    buffer = io.BytesIO()
    im.convert("RGB").save(buffer, "JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def to_pixels(box, width, height, x0=0, y0=0):
    """0..1000 bbox_2d on a (tile) image of width x height -> pixels on the full image."""
    return [x0 + box[0] * width / 1000, y0 + box[1] * height / 1000, x0 + box[2] * width / 1000, y0 + box[3] * height / 1000]


class Viewer:
    def __init__(self, a):
        self.endpoint = a.endpoint.rstrip("/") if a.endpoint else None
        self.model, self.max_tokens, self.timeout = a.model, a.max_tokens, a.timeout
        self.max_size = a.max_size
        self.rows = read_jsonl(a.tasks) if a.tasks else []
        self.predictions = index_predictions(a.predictions) if a.predictions else {}
        if self.predictions:
            self.rows = [r for r in self.rows if r["id"] in self.predictions]
            if not self.rows:
                raise SystemExit("No task IDs of --tasks appear in --predictions")
        self._scores = {}

    # -- model -------------------------------------------------------------------------
    def chat(self, image_png, prompt):
        if not self.endpoint:
            raise ValueError("Start the viewer with --endpoint to ask the model")
        content = [{"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(image_png).decode("ascii")}},
                   {"type": "text", "text": prompt}]
        payload = {"model": self.model, "messages": [{"role": "user", "content": content}], "temperature": 0,
                   "max_tokens": self.max_tokens, "stream": False, "chat_template_kwargs": {"enable_thinking": False}}
        headers = {"Content-Type": "application/json"}
        if os.getenv("INTERNAL_MODEL_API_KEY"):
            headers["Authorization"] = "Bearer " + os.environ["INTERNAL_MODEL_API_KEY"]
        req = Request(self.endpoint + "/chat/completions", data=dumps(payload).encode(), headers=headers)
        with urlopen(req, timeout=self.timeout) as response:
            choice = json.load(response)["choices"][0]
        return choice["message"].get("content") or "", choice.get("finish_reason")

    # -- free test ---------------------------------------------------------------------
    def load(self, req):
        if req.get("path"):
            im = Image.open(Path(req["path"]).expanduser())
        elif req.get("upload"):
            im = Image.open(io.BytesIO(base64.b64decode(req["upload"].split(",", 1)[1])))
        else:
            raise ValueError("Give an image path on the server or upload a file")
        im = ImageOps.exif_transpose(im).convert("RGB")
        scale = fit_scale(*im.size, self.max_size)
        if scale != 1:
            im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
        return im

    def run(self, req):
        im = self.load(req)
        lang = 1 if req.get("lang") == "ko" else 0
        mode = req.get("mode", "spotting")
        jobs = []  # (tile box in pixels, prompt)
        full = [0, 0, im.width, im.height]
        if mode == "spotting":
            rows, cols = (int(v) for v in req.get("grid", "1x1").split("x"))
            for r in range(rows):
                for c in range(cols):
                    jobs.append(([round(c * im.width / cols), round(r * im.height / rows),
                                  round((c + 1) * im.width / cols), round((r + 1) * im.height / rows)],
                                 PROMPTS["spotting"][lang].format()))
        elif mode == "find":
            jobs.append((full, PROMPTS["grounding"][lang].format(text=dumps(req["text"]))))
        elif mode == "read_box":
            box = normalize_box(req["box"], im.width, im.height)
            jobs.append((full, PROMPTS["region_ocr"][lang].format(box=dumps(box))))
        elif mode == "relation":
            direction = DIRECTIONS[req["direction"]]
            anchor = dumps(req["text"])
            jobs.append((full, PROMPTS["relation"][lang].format(direction=direction[0], direction_ko=direction[1], anchor=anchor)))
        elif mode == "custom":
            jobs.append((full, req["prompt"]))
        else:
            raise ValueError(f"Unknown mode {mode}")

        def ask(job):
            tile, prompt = job
            crop = im.crop(tuple(tile)) if tile != full else im
            text, finish = self.chat(png_bytes(crop), prompt)
            boxes = parse_boxes(text)
            w, h = tile[2] - tile[0], tile[3] - tile[1]
            drawn = [{"px": to_pixels(b["bbox_2d"], w, h, tile[0], tile[1]), "label": b["label"]} for b in boxes or []]
            return {"tile": tile, "prompt": prompt, "raw": text, "finish_reason": finish,
                    "parsed": boxes is not None, "boxes": drawn}

        with ThreadPoolExecutor(max_workers=8) as pool:
            parts = list(pool.map(ask, jobs))
        result = {"image": data_url(im), "width": im.width, "height": im.height, "parts": parts,
                  "pred": [b for p in parts for b in p["boxes"]], "gold": [], "query": []}
        if mode == "read_box":
            result["query"] = [req["box"]]
        return result

    # -- benchmark sample --------------------------------------------------------------
    def score(self, row):
        if row["id"] not in self._scores:
            self._scores[row["id"]] = reward(self.predictions[row["id"]], row["task"], row["target"])
        return self._scores[row["id"]]

    def info(self):
        return {"endpoint": self.endpoint, "stored_predictions": bool(self.predictions),
                "tasks": sorted({r["task"] for r in self.rows}), "views": sorted({r.get("view", "") for r in self.rows}),
                "rows": len(self.rows)}

    def sample(self, req):
        if not self.rows:
            raise ValueError("Start the viewer with --tasks (prepared *_tasks.jsonl) for benchmark samples")
        rows = [r for r in self.rows if (not req.get("task") or r["task"] == req["task"])
                and (not req.get("view") or r.get("view") == req["view"])]
        if req.get("id"):
            rows = [r for r in self.rows if r["id"] == req["id"].strip()]
        if self.predictions and req.get("max_reward") not in (None, ""):
            rows = [r for r in rows if self.score(r) <= float(req["max_reward"])]
        if not rows:
            raise ValueError("No question matches these filters")
        row = random.choice(rows)
        with Image.open(row["images"][0]) as im:
            im = im.convert("RGB")
        prompt = row["messages"][0]["content"].replace("<image>", "").strip()
        if self.predictions:
            raw, finish = self.predictions[row["id"]], "stored"
        else:
            raw, finish = self.chat(Path(row["images"][0]).read_bytes(), prompt)
        target = parse_target(row["target"])
        result = {"image": data_url(im), "width": im.width, "height": im.height, "id": row["id"], "task": row["task"],
                  "view": row.get("view"), "view_ops": row.get("view_ops"), "prompt": prompt, "raw": raw,
                  "finish_reason": finish, "reward": round(reward(raw, row["task"], row["target"]), 3),
                  "gold": [], "pred": [], "query": [], "gold_text": None, "pred_text": None}
        if row["task"] in BOX_TASKS:
            result["gold"] = [{"px": to_pixels(b["bbox_2d"], im.width, im.height), "label": b["label"]} for b in target["boxes"]]
            boxes = parse_boxes(raw)
            result["parsed"] = boxes is not None
            result["pred"] = [{"px": to_pixels(b["bbox_2d"], im.width, im.height), "label": b["label"]} for b in boxes or []]
        else:
            result["gold_text"], result["pred_text"] = target["text"], answer(raw)
        # Boxes named in the question (bbox_ocr / region_ocr / relation anchor / marked_ocr coordinates).
        result["query"] = [to_pixels(json.loads(m), im.width, im.height) for m in PROMPT_BOX.findall(prompt)]
        return result


PAGE = r"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OCR Viewer</title>
<style>
:root{--bg:#f6f7f9;--panel:#fff;--ink:#1d2330;--muted:#677084;--line:#dfe3ea;--gold:#12a150;--pred:#e5383b;--query:#2563eb;--accent:#2563eb}
@media (prefers-color-scheme:dark){:root{--bg:#14171c;--panel:#1d2128;--ink:#e6e9ef;--muted:#9aa3b2;--line:#2e3440}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,"Malgun Gothic",sans-serif}
header{padding:12px 16px;border-bottom:1px solid var(--line);display:flex;gap:16px;align-items:baseline;flex-wrap:wrap}
header h1{font-size:16px;margin:0}header span{color:var(--muted);font-size:12px}
main{display:grid;grid-template-columns:340px 1fr;gap:12px;padding:12px 16px}
@media (max-width:900px){main{grid-template-columns:1fr}}
section{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px}
h2{font-size:13px;margin:0 0 8px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
label{display:block;margin:8px 0 3px;color:var(--muted);font-size:12px}
input,select,textarea{width:100%;padding:6px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--ink);font:inherit}
textarea{min-height:70px}
button{margin-top:10px;padding:7px 12px;border:0;border-radius:6px;background:var(--accent);color:#fff;font:inherit;cursor:pointer}
button:disabled{opacity:.5}.row{display:flex;gap:8px}.row>*{flex:1}
.hint{color:var(--muted);font-size:12px;margin-top:6px}
#stage{position:relative;overflow:auto;max-height:78vh;border:1px solid var(--line);border-radius:6px;background:var(--bg)}
canvas{display:block;cursor:crosshair}
.legend{display:flex;gap:14px;font-size:12px;margin:6px 0;flex-wrap:wrap}.legend b{display:inline-block;width:12px;height:12px;border-radius:2px;vertical-align:-2px;margin-right:4px}
pre{white-space:pre-wrap;word-break:break-all;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:8px;max-height:260px;overflow:auto;font-size:12px}
table{border-collapse:collapse;width:100%;font-size:12px}td,th{border-bottom:1px solid var(--line);padding:3px 6px;text-align:left}
tr:hover{background:rgba(37,99,235,.12)}.err{color:var(--pred)}.kv{font-size:12px;color:var(--muted)}
</style></head><body>
<header><h1>OCR Viewer</h1><span id="status"></span></header>
<main>
<div>
<section>
<h2>자유 테스트</h2>
<label>이미지 경로 (서버)</label><input id="path" placeholder="/share/.../sample.jpg">
<label>또는 업로드</label><input id="file" type="file" accept="image/*">
<label>질문</label>
<select id="mode">
<option value="spotting">전체 글자 + 위치 (spotting)</option>
<option value="find">글자 찾기 (grounding)</option>
<option value="read_box">드래그한 영역 읽기 (region_ocr)</option>
<option value="relation">기준 글자 옆 찾기 (relation)</option>
<option value="custom">직접 입력</option>
</select>
<div id="opt-grid"><label>타일 분할 (spotting 답이 길면 잘리므로 페이지는 나눠서)</label>
<select id="grid"><option>1x1</option><option>2x1</option><option>2x2</option><option selected>3x2</option><option>3x3</option><option>4x3</option></select></div>
<div id="opt-text" hidden><label>글자</label><input id="text"></div>
<div id="opt-dir" hidden><label>방향</label><select id="direction"><option value="right">오른쪽</option><option value="left">왼쪽</option><option value="below">아래</option><option value="above">위</option></select></div>
<div id="opt-box" hidden class="hint">이미지를 한 번 불러온 뒤(spotting 등으로 실행) 그림 위에서 드래그해 영역을 고르세요. <span id="boxinfo"></span></div>
<div id="opt-prompt" hidden><label>프롬프트</label><textarea id="prompt"></textarea></div>
<div class="row"><div><label>언어</label><select id="lang"><option value="ko">한국어</option><option value="en">English</option></select></div></div>
<button id="run">실행</button>
</section>
<section style="margin-top:12px" id="bench">
<h2>벤치마크 문제</h2>
<div class="row"><div><label>과제</label><select id="task"><option value="">전체</option></select></div>
<div><label>화면</label><select id="view"><option value="">전체</option></select></div></div>
<div id="opt-maxr"><label>보상 이하만 (예: 0.5, 저장된 답일 때)</label><input id="maxr" placeholder="비우면 전체"></div>
<label>문제 ID (선택)</label><input id="qid">
<button id="sample">무작위 문제</button>
</section>
</div>
<section>
<div class="legend"><span><b style="background:var(--gold)"></b>정답(OCR 기준)</span><span><b style="background:var(--pred)"></b>모델 답</span><span><b style="background:var(--query)"></b>질문 영역</span>
<label style="display:inline;margin:0"><input type="checkbox" id="showlabels" checked style="width:auto"> 글자 표시</label>
<label style="display:inline;margin:0">확대 <input type="range" id="zoom" min="0.2" max="1.5" step="0.05" value="0.5" style="width:120px;vertical-align:middle"></label></div>
<div id="meta" class="kv"></div>
<div id="stage"><canvas id="cv"></canvas></div>
<div id="texts"></div>
<h2 style="margin-top:12px">결과</h2><div id="table"></div>
<h2 style="margin-top:12px">모델 원문</h2><pre id="raw"></pre>
</section>
</main>
<script>
const $=id=>document.getElementById(id);let last=null,img=new Image(),drag=null,picked=null,hover=-1;
const css=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();
function setStatus(t,err){$('status').textContent=t;$('status').className=err?'err':''}
async function post(url,body){const r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const j=await r.json();if(!r.ok)throw new Error(j.error||r.statusText);return j}
function modeUI(){const m=$('mode').value;$('opt-grid').hidden=m!=='spotting';$('opt-text').hidden=!(m==='find'||m==='relation');$('opt-dir').hidden=m!=='relation';$('opt-box').hidden=m!=='read_box';$('opt-prompt').hidden=m!=='custom'}
$('mode').onchange=modeUI;
function readFile(){return new Promise(res=>{const f=$('file').files[0];if(!f)return res(null);const r=new FileReader();r.onload=()=>res(r.result);r.readAsDataURL(f)})}
function draw(){const cv=$('cv'),z=+$('zoom').value;if(!last)return;cv.width=last.width*z;cv.height=last.height*z;const c=cv.getContext('2d');c.drawImage(img,0,0,cv.width,cv.height);
 const box=(b,col,w,i)=>{c.lineWidth=(i===hover?w+2:w);c.strokeStyle=col;c.strokeRect(b[0]*z,b[1]*z,(b[2]-b[0])*z,(b[3]-b[1])*z)};
 const label=(b,t,col,below)=>{if(!$('showlabels').checked||!t)return;const fs=Math.max(10,Math.min(18,(b[3]-b[1])*z*.8));c.font=fs+'px "Malgun Gothic",sans-serif';const w=c.measureText(t).width+4;const y=below?b[3]*z:b[1]*z-fs-2;c.fillStyle=col;c.globalAlpha=.85;c.fillRect(b[0]*z,y,w,fs+2);c.globalAlpha=1;c.fillStyle='#fff';c.fillText(t,b[0]*z+2,y+fs-1)};
 (last.query||[]).forEach(b=>box(b,css('--query'),2));
 (last.gold||[]).forEach((b,i)=>{box(b.px,css('--gold'),2);label(b.px,b.label,css('--gold'),true)});
 (last.pred||[]).forEach((b,i)=>{box(b.px,css('--pred'),2,i);label(b.px,b.label,css('--pred'),false)});
 (last.parts||[]).length>1&&last.parts.forEach(p=>{c.setLineDash([6,4]);box(p.tile,'#999',1);c.setLineDash([])});
 if(picked)box(picked,css('--query'),2)}
function esc(s){return String(s??'').replace(/[&<>]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m]))}
function show(j){last=j;img=new Image();img.onload=draw;img.src=j.image;
 let meta=[];if(j.id)meta.push('ID '+j.id,'과제 '+j.task,'화면 '+j.view+(j.view_ops&&j.view_ops.length?' ('+j.view_ops.join(', ')+')':''),'보상 '+j.reward);
 const cut=(j.parts||[]).filter(p=>p.finish_reason==='length').length+(j.finish_reason==='length'?1:0);
 if(cut)meta.push('⚠ 답이 길이 제한에서 잘림 '+cut+'건: 타일을 더 잘게');
 if(j.parsed===false||(j.parts||[]).some(p=>p.parsed===false&&p.prompt.includes('bbox_2d": [x1')))meta.push('⚠ JSON 형식 아님');
 $('meta').innerHTML=esc(meta.join(' · '))+(j.prompt?'<div>질문: '+esc(j.prompt)+'</div>':'');
 $('texts').innerHTML=j.gold_text!=null?'<table><tr><th>정답(OCR)</th><td>'+esc(j.gold_text).replace(/\n/g,'<br>')+'</td></tr><tr><th>모델</th><td>'+esc(j.pred_text).replace(/\n/g,'<br>')+'</td></tr></table>':'';
 const rows=(j.pred||[]).map((b,i)=>'<tr data-i="'+i+'"><td>'+(i+1)+'</td><td>'+esc(b.label)+'</td><td>'+b.px.map(v=>Math.round(v)).join(', ')+'</td></tr>').join('');
 $('table').innerHTML=(j.pred||[]).length?'<table><tr><th>#</th><th>모델 글자</th><th>픽셀 박스</th></tr>'+rows+'</table>':'<div class="kv">박스 없음</div>';
 $('table').querySelectorAll('tr[data-i]').forEach(tr=>{tr.onmouseenter=()=>{hover=+tr.dataset.i;draw()};tr.onmouseleave=()=>{hover=-1;draw()}});
 $('raw').textContent=j.raw!=null?j.raw:(j.parts||[]).map(p=>(j.parts.length>1?'# tile '+p.tile.join(',')+'\n':'')+p.raw).join('\n\n')}
$('run').onclick=async()=>{const m=$('mode').value;if(m==='read_box'&&!picked){setStatus('먼저 그림 위에서 영역을 드래그하세요',1);return}
 const body={mode:m,lang:$('lang').value,path:$('path').value.trim(),grid:$('grid').value,text:$('text').value,direction:$('direction').value,prompt:$('prompt').value,box:picked};
 if(!body.path)body.upload=await readFile();$('run').disabled=true;setStatus('모델 실행 중...');const t=performance.now();
 try{const j=await post('/api/run',body);if(m!=='read_box')picked=null;show(j);setStatus('완료 '+((performance.now()-t)/1000).toFixed(1)+'s')}catch(e){setStatus(e.message,1)}finally{$('run').disabled=false}};
$('sample').onclick=async()=>{$('sample').disabled=true;setStatus('불러오는 중...');picked=null;
 try{show(await post('/api/sample',{task:$('task').value,view:$('view').value,max_reward:$('maxr').value,id:$('qid').value}));setStatus('')}catch(e){setStatus(e.message,1)}finally{$('sample').disabled=false}};
$('zoom').oninput=draw;$('showlabels').onchange=draw;
const cv=$('cv');const pos=e=>{const r=cv.getBoundingClientRect(),z=+$('zoom').value;return[(e.clientX-r.left)/z,(e.clientY-r.top)/z]};
cv.onmousedown=e=>{if($('mode').value!=='read_box'||!last||last.id)return;drag=pos(e)};
cv.onmousemove=e=>{if(!drag)return;const p=pos(e);picked=[Math.min(drag[0],p[0]),Math.min(drag[1],p[1]),Math.max(drag[0],p[0]),Math.max(drag[1],p[1])];draw()};
cv.onmouseup=()=>{if(!drag)return;drag=null;if(picked)$('boxinfo').textContent='선택: '+picked.map(Math.round).join(', ')};
fetch('/api/info').then(r=>r.json()).then(i=>{setStatus((i.endpoint?'서버 '+i.endpoint:'서버 없음')+(i.rows?' · 벤치마크 '+i.rows+'문항'+(i.stored_predictions?' (저장된 답)':''):''));
 i.tasks.forEach(t=>$('task').add(new Option(t,t)));i.views.forEach(v=>v&&$('view').add(new Option(v,v)));
 if(!i.rows)$('bench').hidden=true;if(!i.stored_predictions)$('opt-maxr').hidden=true;if(!i.endpoint)$('run').disabled=true});
modeUI();
</script></body></html>
"""


def handler(viewer):
    class Handler(BaseHTTPRequestHandler):
        def reply(self, code, body, kind="application/json; charset=utf-8"):
            data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                self.reply(200, PAGE.encode(), "text/html; charset=utf-8")
            elif self.path == "/api/info":
                self.reply(200, viewer.info())
            else:
                self.reply(404, {"error": "not found"})

        def do_POST(self):
            try:
                req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
                if self.path == "/api/run":
                    self.reply(200, viewer.run(req))
                elif self.path == "/api/sample":
                    self.reply(200, viewer.sample(req))
                else:
                    self.reply(404, {"error": "not found"})
            except Exception as exc:  # Shown in the page; the server keeps running.
                self.reply(400, {"error": f"{type(exc).__name__}: {exc}"})

        def log_message(self, fmt, *args):
            pass

    return Handler


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--endpoint", help="OpenAI-compatible server, e.g. http://127.0.0.1:8000/v1")
    p.add_argument("--model", default="bank-ocr", help="served_model_name of the server")
    p.add_argument("--tasks", help="Prepared *_tasks.jsonl for benchmark samples")
    p.add_argument("--predictions", help="Stored predictions for --tasks (no server needed)")
    p.add_argument("--max-size", type=int, nargs=2, default=[2300, 1600], metavar=("LONG", "SHORT"),
                   help="Same image_max_size as prepare (default 2300 1600)")
    p.add_argument("--max-tokens", type=int, default=2048)
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=7860)
    a = p.parse_args()
    if not a.endpoint and not a.predictions:
        p.error("Give --endpoint (ask the model) and/or --tasks with --predictions (stored answers)")
    if a.predictions and not a.tasks:
        p.error("--predictions needs --tasks")
    viewer = Viewer(a)
    server = ThreadingHTTPServer((a.host, a.port), handler(viewer))
    print(f"OCR viewer on http://{a.host}:{a.port}  (Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
