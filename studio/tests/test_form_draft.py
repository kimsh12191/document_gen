"""서식 초안 시험: 예시 이미지 → (가짜 openai 서버) html 칸 → 키 추천 → output/ 템플릿·form.json, 키 고치기·내려받기 (studio/form_draft.py)."""
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest
from PIL import Image

from studio import analyzers as AZ, form_draft as FD

TEMPLATE = """{% extends "_base.html.j2" %}
{% import "_macros.html.j2" as m with context %}
{% block content %}
{{ m.title("예금거래신청서") }}
<table><tr><th>성명</th><td>{{ f("v01", label="성명") }}</td><th>연락처</th><td>{{ f("v02", label="연락처") }}</td></tr></table>
{{ m.choice("v03", ["예", "아니오"], label="동의 여부") }}
{% for r in d.rows %}<p>{{ f("rows." ~ loop.index0 ~ ".v04", label="거래일") }}</p>{% endfor %}
<p>신청인 {{ f("v01", label="성명") }} {{ m.sigspot("v05", val("v01")) }}</p>
{% endblock %}"""
HTML_ANSWER = "<think>표를 본다 {}</think>" + json.dumps({
    "name": "예금거래신청서", "category": "external", "template": TEMPLATE,
    "slots": [{"id": "v01", "kind": "field", "label": "성명", "section": "신청인", "type": "text", "rule": "person"},
              {"id": "v02", "kind": "field", "label": "연락처", "section": "신청인", "type": "text", "rule": "phone"},
              {"id": "v03", "kind": "check", "label": "동의 여부", "section": "개인정보", "type": "checkbox", "choices": ["예", "아니오"]},
              {"id": "v04", "kind": "field", "label": "거래일", "section": "거래내역", "type": "date", "rule": "date_seq", "list": "rows"},
              {"id": "v05", "kind": "sign", "label": "신청인 서명", "section": "신청인", "type": "signature"}],
    "lists": {"rows": {"min": 2, "max": 5}}}, ensure_ascii=False)
KEYS_ANSWER = "```json\n" + json.dumps([
    {"slot": "v01", "key": "customer.name", "source": "existing", "label": "신청인 성명", "description": "고객 본인 성명", "type": "text", "reason": "신청인 구역"},
    {"slot": "v02", "key": "customer.phone_mobile_x", "source": "new", "label": "신청인 연락처", "description": "", "type": "text", "reason": "신청인 구역"},
    {"slot": "v03", "key": "consent.privacy", "source": "new", "label": "개인정보 동의", "description": "동의 여부", "type": "checkbox", "reason": "동의란"},
    {"slot": "v04", "key": "rows.*.date", "source": "new", "label": "거래일", "description": "거래 행의 날짜", "type": "date", "reason": "표"},
], ensure_ascii=False) + "\n```"   # v05 는 빠뜨린다


@pytest.fixture
def server():
    seen = []

    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            seen.append(body)
            text = body["messages"][0]["content"][-1]["text"]
            answer = HTML_ANSWER if "html 서식" in text.splitlines()[0] else KEYS_ANSWER
            out = json.dumps({"choices": [{"message": {"content": answer}, "finish_reason": "stop"}]}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(out)

        def log_message(self, *a):
            pass

    httpd = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_port}/v1", seen
    httpd.shutdown()


@pytest.fixture
def img(tmp_path):
    p = tmp_path / "sample.png"
    Image.new("RGB", (400, 560), "white").save(p)
    return p


def conn(url, external=False):
    return {"providers": {"glm": {"kind": "openai", "base_url": url, "model": "glm", "external": external}}}


def test_create_boundary(tmp_path, img):
    with pytest.raises(ValueError, match="외부"):
        FD.create(tmp_path, conn("http://x/v1", external=True), "glm", img, real_data=True)
    d = FD.create(tmp_path, conn("http://x/v1"), "glm", img, "예금거래신청서", "finance", "1쪽만")
    job = json.loads((d / "job.json").read_text(encoding="utf-8"))
    assert job["kind"] == "html" and job["target"]["draft"] and (d / "input" / "source.png").exists()
    task = (d / "TASK.md").read_text(encoding="utf-8")
    assert "서식 이름: 예금거래신청서" in task and "1쪽만" in task and "{types}" not in task and "date_seq" in task
    assert [j["id"] for j in FD.listing(tmp_path)] == [d.name]


def test_run_end_to_end(tmp_path, img, server):
    url, seen = server
    d = FD.create(tmp_path, conn(url), "glm", img, "", "finance")
    FD.run(d)
    assert len(seen) == 2 and all(m["messages"][0]["content"][0]["type"] == "image_url" for m in seen)   # 두 단계 모두 이미지를 본다
    assert "customer.name" in seen[1]["messages"][0]["content"][-1]["text"]   # 공통 키 후보를 보낸다
    info = FD.detail(tmp_path, d.name)
    keys = {k["slot"]: k for k in info["keys"]}
    assert keys["v01"]["source"] == "existing" and keys["v01"]["type"] == "text"
    assert keys["v02"]["source"] == "new" and keys["v05"]["missing"] and keys["v05"]["key"] == "todo_v05"
    tpl = (d / "output" / "template.html.j2").read_text(encoding="utf-8")
    form = json.loads((d / "output" / "form.json").read_text(encoding="utf-8"))
    assert 'f("customer.name"' in tpl and '".date"' in tpl and 'm.sigspot("todo_v05"' in tpl and "v0" not in tpl.replace("todo_v05", "")
    assert form["name"] == "예금거래신청서" and form["fields"]["consent.privacy"]["source"] == "rule:choice"
    assert form["lists"]["rows"] == {"min": 2, "max": 5, "fields": {"date": {"label": "거래일", "type": "date", "description": "거래 행의 날짜",
                                                                        "source": "rule:date_seq"}}}
    assert "customer.name" in form["fields"] and "todo_v05" not in form["fields"]   # 서명은 값 칸이 아니다


def test_save_keys_and_export(tmp_path, img, server, monkeypatch):
    url, _ = server
    d = FD.create(tmp_path, conn(url), "glm", img)
    FD.run(d)
    monkeypatch.setattr(AZ, "validate", lambda d: {"ok": True, "errors": []})   # 렌더링(브라우저)은 빼고
    rows = FD.detail(tmp_path, d.name)["keys"]
    for r in rows:
        if r["slot"] == "v05":
            r["key"] = "sign.customer"
    assert FD.save_keys(tmp_path, d.name, rows, "외주A")["ok"]
    tpl = (d / "output" / "template.html.j2").read_text(encoding="utf-8")
    assert 'm.sigspot("customer"' in tpl
    info = FD.detail(tmp_path, d.name)
    assert info["edited_by"] == "외주A" and not info["conflict"]
    ex = FD.export(tmp_path, d.name)
    assert ex["form"] == "예금거래신청서" and {"key": "sign.customer"}.items() <= next(f for f in ex["fields"] if f["kind"] == "sign").items()
    bad = [dict(r, key="customer") if r["slot"] == "v02" else r for r in rows]   # customer 와 customer.name 은 함께 못 쓴다
    with pytest.raises(ValueError, match="상위 경로"):
        FD.save_keys(tmp_path, d.name, bad, "외주A")
    with pytest.raises(ValueError, match="모든 칸"):
        FD.save_keys(tmp_path, d.name, rows[:2], "외주A")


def test_parse_html_checks():
    data = json.loads(HTML_ANSWER.split("</think>")[1])
    with pytest.raises(ValueError, match="칸 목록에 없는"):
        FD.parse_html(json.dumps({**data, "slots": data["slots"][:-1]}))
    with pytest.raises(ValueError, match="템플릿에 없는"):
        FD.parse_html(json.dumps({**data, "slots": data["slots"] + [{"id": "v09", "kind": "field", "label": "x"}]}))
    with pytest.raises(ValueError, match="문법"):
        FD.parse_html(json.dumps({**data, "template": data["template"] + "{% if %}"}))
    ok = FD.parse_html(json.dumps({**data, "template": data["template"].split("{% block content %}")[1].replace("{% endblock %}", "")}))
    assert ok["template"].startswith('{% extends "_base.html.j2" %}')   # 머리를 빠뜨려도 붙인다


def test_dev_vlm_mock_runs_whole_flow(tmp_path, img):
    """시험용 더미 모델 서버(studio.dev_vlm --mock)로 처음부터 끝까지: 공통 키는 기존, 나머지는 새 키."""
    import socket
    from studio import dev_vlm

    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    threading.Thread(target=dev_vlm.serve, args=("127.0.0.1", port, "mock", "", 0), daemon=True).start()
    import time
    for _ in range(50):
        try:
            socket.create_connection(("127.0.0.1", port), timeout=0.2).close()
            break
        except OSError:
            time.sleep(0.1)
    d = FD.create(tmp_path, conn(f"http://127.0.0.1:{port}/v1"), "glm", img)
    FD.run(d)
    keys = {k["slot"]: k for k in FD.detail(tmp_path, d.name)["keys"]}
    assert keys["v01"]["key"] == "customer.name" and keys["v06"]["key"] == "agent.name" and keys["v16"]["key"] == "sign.customer"
    assert keys["v08"]["source"] == "new" and keys["v11"]["key"] == "transfers.*.date"
    form = json.loads((d / "output" / "form.json").read_text(encoding="utf-8"))
    assert set(form["lists"]["transfers"]["fields"]) == {"date", "account", "amount"}
