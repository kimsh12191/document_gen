"""묻기: 고른 그림(들)을 질문에 맞게 만들어 (자르기·상자 그리기·평가와 같은 크기로) 모델마다 보내고, 답을 읽는다.
보낸 그림은 <home>/sent/, 묻고 받은 것은 <home>/log.jsonl."""
from __future__ import annotations

import base64
import hashlib
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import images as IM
from .questions import BY_ID

FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.S)


def _json(text: str):
    """답에서 JSON 을 읽는다: 그대로 → ``` 안 → 처음 [ 또는 { 부터 마지막 ] 또는 } 까지. 못 읽으면 None."""
    cands = [text.strip()] + FENCE.findall(text)
    spans = [(text.find(o), text.rfind(c)) for o, c in (("[", "]"), ("{", "}"))]
    cands += [text[i:j + 1] for i, j in sorted(spans) if 0 <= i < j]   # 바깥쪽(먼저 열린 것)부터
    for c in cands:
        try:
            return json.loads(c)
        except ValueError:
            continue
    return None


def _boxes(obj) -> list[dict]:
    """답 속 bbox_2d 를 모두: [{box: 0~1000, label, page(1부터)}]."""
    out = []

    def walk(x):
        if isinstance(x, dict):
            b = x.get("bbox_2d")
            if isinstance(b, list) and len(b) == 4 and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in b):
                label = x.get("label", x.get("value", x.get("key")))
                key = x.get("key")
                out.append({"box": b, "label": f"{key}: {label}" if key and "value" in x else label,
                            "page": x.get("page") if isinstance(x.get("page"), int) else 1})
            for v in x.values():
                if isinstance(v, (dict, list)):
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(obj)
    return out


def read_answer(task: str, text: str) -> dict:
    """{"json"?, "boxes", "format_error"}: JSON 으로 답하는 과제인데 못 읽으면 형식 오류."""
    kind = BY_ID.get(task, {}).get("answer", "auto")
    obj = _json(text) if kind != "text" else None
    out = {"boxes": _boxes(obj) if obj is not None else [], "format_error": kind in ("boxes", "entries", "json", "table") and obj is None}
    if obj is not None:
        out["json"] = obj
    return out


class Asker:
    def __init__(self, home: Path, models):
        self.home, self.models = Path(home), models
        self.sent = self.home / "sent"
        self.sent.mkdir(parents=True, exist_ok=True)
        self.logfile = self.home / "log.jsonl"

    def _save(self, img) -> tuple[str, list[int], str]:
        data = IM.png(img)
        name = hashlib.sha1(data).hexdigest()[:20] + ".png"
        p = self.sent / name
        if not p.exists():
            p.write_bytes(data)
        return name, [img.width, img.height], base64.b64encode(data).decode("ascii")

    def prepare(self, spec: dict):
        """고른 그림 → 보낼 그림 (자르기·상자 그리기는 op.index 번째 그림에)."""
        picked = spec.get("images") or []
        if not picked:
            raise ValueError("그림을 고르세요")
        if len(picked) > 16:
            raise ValueError("그림은 16장까지 (모델 서버 limit_mm_per_prompt)")
        imgs = [IM.load(x["path"], int(x.get("page") or 0)) for x in picked]
        op = spec.get("op") or {}
        i = int(op.get("index") or 0)
        if op.get("crop"):
            imgs[i] = IM.crop(imgs[i], op["crop"])
        if op.get("markers"):
            imgs[i] = IM.draw_markers(imgs[i], op["markers"])
        if op and BY_ID.get(spec.get("task"), {}).get("image") in ("crop", "marker"):
            imgs = [imgs[i]]   # 자른 것·상자를 그린 것 한 장만 (벤치마크와 같음)
        return imgs

    def ask(self, spec: dict) -> dict:
        """spec: models[ids], images[{path, page}], task, prompt, op?, same_as_eval?, turns?[{prompt, answers{id: 답}}]
        → {"results": {id: {text, seconds, finish_reason, json?, boxes, format_error, sent:[{name, size}]} 또는 {error}}}"""
        prompt = (spec.get("prompt") or "").strip()
        if not prompt:
            raise ValueError("질문이 비었습니다")
        mids = spec.get("models") or []
        if not mids:
            raise ValueError("물을 모델을 고르세요")
        base = self.prepare(spec)
        turns = spec.get("turns") or []
        task = spec.get("task") or "custom"

        def one(mid):
            e = self.models._entry(mid)
            imgs = IM.fit(base, int(e.get("factor") or 32), spec.get("same_as_eval", True))
            sent = [self._save(im) for im in imgs]
            content = [{"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}} for _, _, b64 in sent]
            first = turns[0]["prompt"] if turns else prompt
            messages = [{"role": "user", "content": content + [{"type": "text", "text": first}]}]   # 그림 먼저 (평가와 같음)
            for k, t in enumerate(turns):
                messages.append({"role": "assistant", "content": (t.get("answers") or {}).get(mid, "")})
                messages.append({"role": "user", "content": turns[k + 1]["prompt"] if k + 1 < len(turns) else prompt})
            try:
                r = self.models.chat(mid, messages)
            except Exception as exc:   # 서버 오류는 모델마다 따로 보여 준다
                return mid, {"error": f"{type(exc).__name__}: {exc}", "sent": [{"name": n, "size": s} for n, s, _ in sent]}
            return mid, {**r, **read_answer(task if not turns else "custom", r["text"]),
                         "sent": [{"name": n, "size": s} for n, s, _ in sent], "model": e.get("name")}

        with ThreadPoolExecutor(max_workers=len(mids)) as ex:
            results = dict(ex.map(one, mids))
        self._log(spec, prompt, results)
        return {"results": results}

    def _log(self, spec, prompt, results):
        row = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "task": spec.get("task"), "prompt": prompt,
               "turn": len(spec.get("turns") or []), "images": spec.get("images"), "op": spec.get("op"),
               "same_as_eval": spec.get("same_as_eval", True),
               "answers": {mid: {"model": r.get("model"), "path": (self._path(mid)), "text": r.get("text"), "error": r.get("error"),
                                 "seconds": r.get("seconds"), "sent": [s["name"] for s in r.get("sent", [])]}
                           for mid, r in results.items()}}
        with self.logfile.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    def _path(self, mid):
        try:
            e = self.models._entry(mid)
        except KeyError:
            return None
        return e.get("path") or e.get("endpoint")
