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
    d = FD.create(tmp_path, conn(url), "glm", img, "", "finance", rounds=0)
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
    d = FD.create(tmp_path, conn(url), "glm", img, rounds=0)
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
    d = FD.create(tmp_path, conn(f"http://127.0.0.1:{port}/v1"), "glm", img, rounds=0)
    FD.run(d)
    keys = {k["slot"]: k for k in FD.detail(tmp_path, d.name)["keys"]}
    assert keys["v01"]["key"] == "customer.name" and keys["v06"]["key"] == "agent.name" and keys["v16"]["key"] == "sign.customer"
    assert keys["v08"]["source"] == "new" and keys["v11"]["key"] == "transfers.*.date"
    form = json.loads((d / "output" / "form.json").read_text(encoding="utf-8"))
    assert set(form["lists"]["transfers"]["fields"]) == {"date", "account", "amount"}


# ---------------------------------------------------------------------------
# 다듬기 하네스: 구획 답 · 찾아 바꾸기 · 위치 맞대기 · 회차 루프 (브라우저 없이)
# ---------------------------------------------------------------------------

def _sections_answer(template=TEMPLATE, slots=None):
    data = json.loads(HTML_ANSWER.split("</think>")[1])
    return ("<<<META>>>\n{\"name\": \"예금거래신청서\"}\n<<<TEMPLATE>>>\n```html\n" + template + "\n```\n<<<SLOTS>>>\n"
            + json.dumps(slots or data["slots"], ensure_ascii=False) + "\n<<<LISTS>>>\n" + json.dumps(data["lists"]) + "\n<<<END>>>")


def test_parse_sections_format():
    d = FD.parse_html("<think>본다</think>\n" + _sections_answer())
    assert d["name"] == "예금거래신청서" and d["template"].startswith("{% extends") and len(d["slots"]) == 5
    assert d["lists"]["rows"] == {"min": 2, "max": 5}
    with pytest.raises(ValueError, match="SLOTS"):
        FD.parse_html("<<<TEMPLATE>>>\nx\n<<<SLOTS>>>\n아님\n<<<END>>>")


def test_apply_edits_exact_whitespace_and_errors():
    tpl = "a { height: 24px; }\n<td>{{ f(\"v01\") }}</td>\n<td>x</td>\n<td>x</td>"
    one = "<<<<<<< SEARCH\na { height: 24px; }\n=======\na { height: 21px; }\n>>>>>>> REPLACE"
    assert FD.apply_edits(tpl, one).startswith("a { height: 21px; }")
    loose = "<<<<<<< SEARCH\n  <td>{{ f(\"v01\")   }}</td>\n=======\n<td class=\"c\">{{ f(\"v01\") }}</td>\n>>>>>>> REPLACE"
    assert '<td class="c">' in FD.apply_edits(tpl, loose)   # 들여쓰기·공백 수만 다르면 찾는다
    with pytest.raises(ValueError, match="여러 번"):
        FD.apply_edits(tpl, "<<<<<<< SEARCH\n<td>x</td>\n=======\n<td>y</td>\n>>>>>>> REPLACE")
    with pytest.raises(ValueError, match="찾지 못했습니다"):
        FD.apply_edits(tpl, "<<<<<<< SEARCH\nnone\n=======\ny\n>>>>>>> REPLACE")


def test_parse_refine():
    draft = FD.parse_html(_sections_answer())
    new = FD.parse_refine("<<<DIFF>>>\n- 제목이 작음\n<<<EDITS>>>\n<<<<<<< SEARCH\n{{ m.title(\"예금거래신청서\") }}\n=======\n"
                          "<h1 style=\"font-size:30px\">예금거래신청서</h1>\n>>>>>>> REPLACE\n<<<END>>>", draft)
    assert "font-size:30px" in new["template"] and new["diff"] == "- 제목이 작음" and new["name"] == "예금거래신청서"
    assert FD.parse_refine("<<<DIFF>>>\n- 없음\n<<<DONE>>>", draft) is None
    with pytest.raises(ValueError, match="템플릿에 없는"):   # 칸을 지운 수정은 칸 목록 검사에 걸린다
        FD.parse_refine("<<<EDITS>>>\n<<<<<<< SEARCH\n<th>연락처</th><td>{{ f(\"v02\", label=\"연락처\") }}</td>\n=======\n\n>>>>>>> REPLACE", draft)


def test_form_fit_finds_vertical_shift(tmp_path):
    """같은 표를 20px 아래로 내린 그림: 맞대기가 '원본보다 아래' 와 가로선 대응을 낸다."""
    from PIL import ImageDraw
    from studio import form_fit as FF

    def page(shift, row):
        im = Image.new("RGB", (794, 1123), "white")
        dr = ImageDraw.Draw(im)
        for i in range(8):
            y = 200 + shift + i * row
            dr.line([(60, y), (734, y)], fill="black", width=2)
        for x in (60, 200, 734):
            dr.line([(x, 200 + shift), (x, 200 + shift + 7 * row)], fill="black", width=2)
        return im

    page(0, 22).save(tmp_path / "orig.png")
    page(20, 25).save(tmp_path / "render.png")
    r = FF.compare(tmp_path / "orig.png", tmp_path / "render.png")
    table = max(r["blocks"], key=lambda b: b["y"][1] - b["y"][0])
    assert 14 <= table["y"][0] - table["orig_y"][0] <= 26
    assert "아래" in r["feedback"] and "가로선" in r["feedback"]
    same = FF.compare(tmp_path / "orig.png", tmp_path / "orig.png")
    assert same["score"] == 100.0 and "큰 위치 차이는 없다" in same["feedback"]
    assert r["score"] < same["score"]
    FF.composite(tmp_path / "orig.png", tmp_path / "render.png", tmp_path / "c.png")
    assert Image.open(tmp_path / "c.png").size == (794 * 3 + 20, 1123)


def test_refine_keeps_best_and_stops(tmp_path, img, monkeypatch):
    """점수가 오른 수정은 남기고, 내린 수정은 되돌리고, 2회 연속 안 오르면 멈춘다."""
    d = FD.create(tmp_path, conn("http://x/v1"), "glm", img, rounds=5)
    draft = FD.parse_html(_sections_answer())
    scores = iter([60.0, 70.0, 65.0, 69.0, 99.0])

    def fake_render(d_, dr, n):
        rd = d_ / "draft" / "rounds" / str(n)
        rd.mkdir(parents=True, exist_ok=True)
        RB_write(rd / "slots.json", dr)
        (rd / "compare.png").write_bytes(b"x")
        return {"n": n, "score": next(scores), "feedback": "1. y 10~20: 시작이 원본보다 8px 아래", "pages": 1}

    from studio import real_benchmark as RB
    RB_write = RB.write
    edit = ("<<<DIFF>>>\n- 간격 {n}\n<<<EDITS>>>\n<<<<<<< SEARCH\n{{ m.title(\"예금거래신청서\") }}\n=======\n"
            "{{ m.title(\"예금거래신청서\") }}<!--{n}-->\n>>>>>>> REPLACE")
    calls = []

    def fake_chat(pc, images, turns):
        calls.append(turns[0])
        return edit.replace("{n}", str(len(calls)))

    monkeypatch.setattr(FD, "render", fake_render)
    monkeypatch.setattr(FD, "chat", fake_chat)
    best = FD.refine(d, {}, draft, 5)
    rounds = json.loads((d / "draft" / "rounds.json").read_text(encoding="utf-8"))
    assert [h["kept"] for h in rounds["rounds"]] == [True, True, False, False] and rounds["best"] == 1
    assert "<!--1-->" in best["template"] and "<!--2-->" not in best["template"]
    assert "되돌렸다" in calls[2] and "8px 아래" in calls[0] and "(1/5회차)" in calls[0]
