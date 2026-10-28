"""시험용 모델 서버: studio 가 vLLM 에 보내는 것과 같은 openai 방식 요청(/v1/chat/completions)을 받는다.
내부망 vLLM 없이 서식 초안·키 추천 흐름을 따라 해 볼 때 쓴다.

  python -m studio.dev_vlm --mock                    더미: 이미지를 보지 않고 늘 같은 예시 서식(예금거래신청서)을 돌려준다.
                                                     키 추천은 받은 칸 목록과 기존 키 목록으로 간단히 맞춘다. 외부 연결 없음.
  python -m studio.dev_vlm --claude [--model claude-sonnet-5-5]
                                                     Claude 에 그대로 넘긴다 (Anthropic SDK, ANTHROPIC_API_KEY 또는 `ant auth login`).
                                                     이미지가 사외로 나가므로 빈 서식·공개 서식으로만 시험한다.

studio 연결: 서버 주소 http://127.0.0.1:8790/v1, 모델 이름 mock (또는 claude-sonnet-5-5).
  더미는 실문서 벤치마크 › OCR·모델 연결 화면에 등록해도 되고, Claude 는 사외 연결이므로 studio/config.json 의 providers 에
  "external": true 로 둔다 (그러면 studio 가 실서류 이미지를 보내지 않는다). 예시는 studio/README.md 의 서식 초안 절.
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ---------------------------------------------------------------------------
# 더미 (--mock)
# ---------------------------------------------------------------------------

MOCK_TEMPLATE = """{% extends "_base.html.j2" %}
{% import "_macros.html.j2" as m with context %}
{% block style %}
table.form th { background: #f3f3f3; width: 16%; }
table.form td { height: 30px; }
.sec { margin-top: 14px; font-weight: 700; }
.agree { margin-top: 10px; font-size: calc(var(--fs) - 1px); }
.sign-line { margin-top: 18px; text-align: right; line-height: 2.2; }
table.bank { width: 46%; margin-left: auto; margin-top: 14px; }
{% endblock %}
{% block content %}
{{ m.title("예금거래신청서") }}
<div class="sec">1. 신청인</div>
<table class="form">
  <tr><th>성 명</th><td>{{ f("v01", label="성명") }}</td><th>생년월일</th><td>{{ f("v02", label="생년월일") }}</td></tr>
  <tr><th>휴대폰</th><td>{{ f("v03", label="휴대폰") }}</td><th>이메일</th><td>{{ f("v04", label="이메일") }}</td></tr>
  <tr><th>주 소</th><td colspan="3">{{ f("v05", label="주소") }}</td></tr>
</table>
<div class="sec">2. 대리인 (대리인이 신청하는 경우)</div>
<table class="form">
  <tr><th>성 명</th><td>{{ f("v06", label="성명") }}</td><th>본인과의 관계</th><td>{{ f("v07", label="본인과의 관계") }}</td></tr>
</table>
<div class="sec">3. 신청 내용</div>
<table class="form">
  <tr><th>상 품 명</th><td>{{ f("v08", label="상품명") }}</td><th>신청 금액</th><td>{{ f("v09", label="신청 금액") }}</td></tr>
  <tr><th>계좌번호</th><td colspan="3">{{ f("v10", label="계좌번호") }}</td></tr>
</table>
<div class="sec">4. 자동이체 등록</div>
{{ m.grid(["이체일", "받는 계좌", "금액"], "transfers", ["v11", "v12", "v13"], num_cols=[2], widths=["20%", "50%", "30%"]) }}
<div class="agree">개인(신용)정보 수집·이용에 동의하십니까? {{ m.choice("v14", ["동의함", "동의하지 않음"], label="개인정보 동의") }}</div>
<div class="sign-line">
  신청일 {{ f("v15", label="신청일") }}<br>
  신청인 {{ val("v01") }} {{ m.sigspot("v16", val("v01")) }}<br>
  대리인 {{ val("v06") }} {{ m.sigspot("v17", val("v06")) }}
</div>
<table class="form bank"><tr><th>담당자</th><td>{{ f("v18", label="담당자") }}</td><th>책임자</th><td>{{ m.seal("책임자", key="v19", kind="직인") }}</td></tr></table>
{% endblock %}"""

MOCK_SLOTS = [
    ("v01", "field", "성명", "1. 신청인", "text", "person"), ("v02", "field", "생년월일", "1. 신청인", "date", "date"),
    ("v03", "field", "휴대폰", "1. 신청인", "text", "phone"), ("v04", "field", "이메일", "1. 신청인", "text", "email"),
    ("v05", "field", "주소", "1. 신청인", "text", "address"), ("v06", "field", "성명", "2. 대리인", "text", "person"),
    ("v07", "field", "본인과의 관계", "2. 대리인", "text", "note"), ("v08", "field", "상품명", "3. 신청 내용", "text", "product"),
    ("v09", "field", "신청 금액", "3. 신청 내용", "amount", "amount"), ("v10", "field", "계좌번호", "3. 신청 내용", "text", "account"),
    ("v11", "field", "이체일", "4. 자동이체 등록", "date", "date_seq"), ("v12", "field", "받는 계좌", "4. 자동이체 등록", "text", "account"),
    ("v13", "field", "금액", "4. 자동이체 등록", "amount", "amount"), ("v14", "check", "개인정보 동의", "개인(신용)정보 동의", "checkbox", None),
    ("v15", "field", "신청일", "신청인 서명란", "date", "date"), ("v16", "sign", "신청인 서명", "신청인 서명란", "signature", None),
    ("v17", "sign", "대리인 서명", "대리인 서명란", "signature", None), ("v18", "field", "담당자", "은행 확인란", "text", "person"),
    ("v19", "seal", "책임자 도장", "은행 확인란", "seal", None)]


def mock_html() -> str:
    slots = []
    for sid, kind, label, section, typ, rule in MOCK_SLOTS:
        s = {"id": sid, "kind": kind, "label": label, "section": section, "type": typ}
        if rule:
            s["rule"] = rule
        if kind == "check":
            s["choices"] = ["동의함", "동의하지 않음"]
        if sid in ("v11", "v12", "v13"):
            s["list"] = "transfers"
        slots.append(s)
    return json.dumps({"name": "예금거래신청서", "category": "external", "template": MOCK_TEMPLATE, "slots": slots,
                       "lists": {"transfers": {"min": 1, "max": 6}}}, ensure_ascii=False)


# 구역 → 당사자 (키 사전 parties 의 이름), 기존 키에 없을 때 쓸 새 키 (더미 서식의 칸)
PARTY = [("대리인", "agent", "대리인"), ("보증", "related", "보증인·공동"), ("은행", "bank", "은행"), ("신청인", "customer", "고객"),
         ("고객", "customer", "고객"), ("본인", "customer", "고객"), ("예금주", "customer", "고객")]
SYNONYM = {"휴대폰": "휴대전화", "본인과의 관계": "관계", "성 명": "성명"}
NEW = {"상품명": ("deal.product", "신청 상품명"), "신청 금액": ("deal.amount", "신청 금액"), "계좌번호": ("deal.account", "신청 계좌번호"),
       "이체일": ("transfers.*.date", "자동이체 이체일"), "받는 계좌": ("transfers.*.account", "자동이체 받는 계좌"),
       "금액": ("transfers.*.amount", "자동이체 금액"), "개인정보 동의": ("consent.privacy", "개인(신용)정보 수집·이용 동의 여부"),
       "신청일": ("document.date", "신청서 작성일"), "담당자": ("bank.staff", "은행 담당 직원 성명"), "책임자 도장": ("seal.bank", "은행 책임자 도장")}


def _grams(s: str) -> set[str]:
    s = re.sub(r"\s+", "", s)
    return {s[i:i + 2] for i in range(len(s) - 1)} or {s}


def mock_keys(prompt: str) -> str:
    """칸 목록·기존 키 목록을 프롬프트에서 읽어 구역(당사자)과 항목명으로 맞춘다. 맞는 것이 없으면 새 키."""
    slots = json.loads(re.search(r"칸 목록: (\[.*?\])\n", prompt).group(1))
    catalog = json.loads(re.search(r"기존 키 목록: (\[.*\])", prompt, re.S).group(1))
    out, used = [], set()
    for s in slots:
        who = next(((en, ko) for word, en, ko in PARTY if word in s.get("section", "") + s["label"]), ("customer", "고객"))
        label = SYNONYM.get(s["label"], s["label"])
        if s["kind"] in ("sign", "seal"):
            key = f"{'sign' if s['kind'] == 'sign' else 'seal'}.{who[0]}"
            hit = next((r for r in catalog if r["key"] == key), None)
        else:
            pool = [r for r in catalog if r.get("scope") == "common" and r["key"].startswith(who[0] + ".")]
            scored = sorted(((len(_grams(label) & _grams(r["meaning"].replace(who[1], ""))), r) for r in pool), key=lambda x: -x[0])
            hit = scored[0][1] if scored and scored[0][0] else None
            key = hit["key"] if hit else None
        if hit and key not in used:
            out.append({"slot": s["id"], "key": key, "source": "existing", "label": hit["meaning"], "description": f"{hit['meaning']} ({s['section']})",
                        "type": hit.get("type") or s.get("type"), "reason": f"'{s['section']}' 구역의 '{s['label']}' → 기존 키 뜻 '{hit['meaning']}'"})
        else:
            key, desc = NEW.get(s["label"], (f"{who[0]}.field_{s['id']}", f"{who[1]} {s['label']}"))
            out.append({"slot": s["id"], "key": key, "source": "new", "label": desc,
                        "description": desc, "type": s.get("type"), "reason": "기존 키 중 뜻이 맞는 것이 없어 새 키 (더미 규칙)"})
        used.add(out[-1]["key"])
    return json.dumps(out, ensure_ascii=False)


def mock_answer(body: dict, delay: float) -> str:
    text = "\n".join(p.get("text", "") for p in body["messages"][-1]["content"] if isinstance(p, dict) and p.get("type") == "text") \
        if isinstance(body["messages"][-1]["content"], list) else body["messages"][-1]["content"]
    time.sleep(delay)   # 화면에서 '도는 중'을 볼 수 있게
    if "칸 목록:" in text and "기존 키 목록:" in text:
        return mock_keys(text)
    if "더 비슷하게 고치기" in text:   # 다듬기: 더미는 그림을 보지 않으므로 고칠 것이 없다고 답한다
        return "<<<DIFF>>>\n- (더미 모델) 그림을 보지 않아 고칠 것을 찾지 못함\n<<<DONE>>>"
    if "html 서식" in text:
        return "<think>예시 이미지의 표와 칸을 살펴본다.</think>\n" + mock_html()
    return "[]"


# ---------------------------------------------------------------------------
# Claude (--claude)
# ---------------------------------------------------------------------------

def claude_answer(client, model: str, body: dict) -> tuple[str, str]:
    """openai 방식 요청 → Claude Messages. 이미지(data URL)와 글자를 순서대로 옮긴다. (답, finish_reason)"""
    content = []
    for part in body["messages"][-1]["content"]:
        if part.get("type") == "image_url":
            head, data = part["image_url"]["url"].split(",", 1)
            content.append({"type": "image", "source": {"type": "base64", "media_type": head[5:].split(";")[0], "data": data}})
        elif part.get("type") == "text":
            content.append({"type": "text", "text": part["text"]})
    with client.beta.messages.stream(model=model, max_tokens=max(16000, int(body.get("max_tokens") or 0)),
                                     messages=[{"role": "user", "content": content}],
                                     betas=["server-side-fallback-2026-07-01"], fallbacks="default") as stream:
        msg = stream.get_final_message()
    if msg.stop_reason == "refusal":
        raise RuntimeError(f"Claude 가 거절했습니다: {getattr(msg.stop_details, 'category', None)}")
    text = "".join(b.text for b in msg.content if b.type == "text")
    return text, "length" if msg.stop_reason == "max_tokens" else "stop"


# ---------------------------------------------------------------------------
# 서버
# ---------------------------------------------------------------------------

def serve(host: str, port: int, mode: str, model: str, delay: float) -> None:
    client = None
    if mode == "claude":
        import anthropic

        client = anthropic.Anthropic()
    name = model if mode == "claude" else "mock"

    class H(BaseHTTPRequestHandler):
        def _send(self, code: int, obj: dict) -> None:
            data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path.rstrip("/").endswith("/models"):
                return self._send(200, {"object": "list", "data": [{"id": name, "object": "model"}]})
            self._send(404, {"error": "not found"})

        def do_POST(self):
            if not self.path.rstrip("/").endswith("/chat/completions"):
                return self._send(404, {"error": "not found"})
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
            try:
                if client:
                    text, finish = claude_answer(client, model, body)
                else:
                    text, finish = mock_answer(body, delay), "stop"
            except Exception as e:  # noqa: BLE001  studio 작업 로그에 이유가 보이게
                return self._send(500, {"error": {"message": f"{type(e).__name__}: {e}"}})
            self._send(200, {"id": "dev-" + base64.b32encode(time.time_ns().to_bytes(8, "big")).decode().lower().rstrip("="),
                             "object": "chat.completion", "model": name,
                             "choices": [{"index": 0, "message": {"role": "assistant", "content": text}, "finish_reason": finish}]})

        def log_message(self, fmt, *args):
            print(f"[dev_vlm] {self.address_string()} {fmt % args}", flush=True)

    print(f"시험용 모델 서버 ({mode}): http://{host}:{port}/v1 · 모델 이름 {name}", flush=True)
    ThreadingHTTPServer((host, port), H).serve_forever()


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="studio.dev_vlm", description="서식 초안 시험용 openai 방식 모델 서버 (더미 또는 Claude)")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--mock", action="store_const", dest="mode", const="mock", help="외부 연결 없는 더미")
    mode.add_argument("--claude", action="store_const", dest="mode", const="claude", help="Claude 에 넘김 (Anthropic SDK)")
    ap.add_argument("--model", default="claude-sonnet-5-5")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8790)
    ap.add_argument("--delay", type=float, default=3.0, help="더미 답을 늦추는 초 (진행 화면 보기)")
    a = ap.parse_args(argv)
    serve(a.host, a.port, a.mode, a.model, a.delay)


if __name__ == "__main__":
    main()
