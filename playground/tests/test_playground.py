"""모델 써 보기 (playground/): GPU 표 읽기, 실행 명령 (평가와 같은지), 띄우기·준비·묻기·내리기 (시험용 모델 서버), 질문 문장 (벤치마크와 같은지),
보낼 그림 (자르기·상자·크기), 답 읽기, 웹 API. GPU·vLLM 없이."""
import json
import socket
import sys
import threading
import time
from pathlib import Path
from urllib.request import Request, urlopen

import pytest
from PIL import Image

from docgen.bench import prompts
from docgen.bench.ocr_tasks import PROMPTS as OCR
from playground import ask as A, gpus as G, images as IM, models as M, questions as Q
from playground.server import serve

FAKE = Path(__file__).with_name("fake_vlm.py")


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait(cond, limit=20):
    end = time.time() + limit
    while time.time() < end:
        if cond():
            return True
        time.sleep(0.2)
    return False


def test_gpu_table_free_by_memory_and_processes():
    gpu = ("0, GPU-a, NVIDIA A100-SXM4-80GB, 71234, 81920, 98\n"
           "1, GPU-b, NVIDIA A100-SXM4-80GB, 3, 81920, 0\n"
           "2, GPU-c, NVIDIA A100-SXM4-80GB, 40000, 81920, 10\n"
           "3, GPU-d, NVIDIA A100-SXM4-80GB, [N/A], 81920, [N/A]\n")
    apps = "GPU-a, 4121, 71000\n"
    rows = {g["index"]: g for g in G.parse(gpu, apps)}
    assert rows[0]["procs"] == [{"pid": 4121, "mib": 71000.0}] and not rows[0]["free"]
    assert rows[1]["free"] and rows[1]["util"] == 0
    assert not rows[2]["free"] and rows[2]["procs"] == []   # 다른 컨테이너의 프로세스는 안 보여도 메모리로 사용 중
    assert not rows[3]["free"] and rows[3]["used_mib"] is None


def _model(tmp_path, name="m"):
    d = tmp_path / name
    d.mkdir()
    (d / "config.json").write_text(json.dumps({"vision_config": {"patch_size": 16, "spatial_merge_size": 2}}))
    return d


def test_command_is_the_eval_deploy_command(tmp_path):
    d = _model(tmp_path)
    r = M.command(str(d), [3], 8123)
    want = [p.format(model=str(d), model_type=M.PIPE["model_type"], port=8123) for p in M.PIPE["eval"]["deploy_command"]]
    import shlex
    parts = shlex.split(r["command"].replace("\\\n", " "))
    env = dict(p.split("=", 1) for p in parts[:4])
    assert parts[4:] == want
    assert env["CUDA_VISIBLE_DEVICES"] == "3" and env["HF_HUB_OFFLINE"] == "1"
    assert env["IMAGE_MAX_TOKEN_NUM"] == str(M.image_tokens(d, IM.IMAGE_MAX_SIZE)[0]) and r["factor"] == 32
    two = shlex.split(M.command(str(d), [0, 1], 8124)["command"].replace("\\\n", " "))
    assert two[0] == "CUDA_VISIBLE_DEVICES=0,1" and two[-2:] == ["--vllm_tensor_parallel_size", "2"]
    v = M.command(str(d), [0], 8125, engine="vllm")["command"]
    assert "vllm serve" in v and "IMAGE_MAX_TOKEN_NUM" not in v and "--port 8125" in v.replace(" \\\n    ", " ")
    assert M.command(str(tmp_path / "none"), [0], 8126)["warnings"][0] == "폴더가 없습니다"
    with pytest.raises(ValueError, match="GPU"):
        M.command(str(d), [], 8127)


def test_lora_checkpoint_is_merged_first_into_a_new_folder(tmp_path):
    base = _model(tmp_path, "base")
    ck = tmp_path / "out" / "checkpoint-800"
    ck.mkdir(parents=True)
    (ck / "adapter_config.json").write_text("{}")
    (ck.parent / "args.json").write_text(json.dumps({"model": str(base)}))
    r = M.command(str(ck), [1], 8130)
    merged = ck.parent / "checkpoint-800-merged"
    assert r["info"]["kind"] == "adapter" and r["info"]["base"] == str(base)
    flat = r["command"].replace(" \\\n    ", " ")
    assert flat.startswith("CUDA_VISIBLE_DEVICES=1 swift export") and f"--adapters {ck}" in flat and f"--output_dir {merged}" in flat
    assert " &&\n" in r["command"] and f"--model {merged}" in flat.split("&&")[-1]
    merged.mkdir()
    (merged / "config.json").write_text("{}")
    again = M.command(str(ck), [1], 8130)["command"]
    assert "swift export" not in again and f"--model {merged}" in again.replace(" \\\n    ", " ")   # 합친 것이 있으면 바로


def test_start_ready_chat_restart_stop(tmp_path):
    home = tmp_path / "home"
    ms = M.Models(home)
    port = free_port()
    e = ms.start("가짜", "/x", f"{sys.executable} {FAKE} --port {port} --wait 1", [0])
    assert e["state"] == "starting" and e["port"] == port
    assert wait(lambda: ms.refresh(ms._entry(e["id"]))["state"] == "ready")
    assert "Uvicorn running" in ms.log(e["id"]) and ms.log(e["id"]).startswith("$ ")
    r = ms.chat(e["id"], [{"role": "user", "content": [{"type": "text", "text": "REPLY: 안녕"}]}])
    assert r["text"] == "안녕"
    again = M.Models(home)   # 화면을 다시 켜도 떠 있는 것을 찾는다
    assert [x["id"] for x in again.list()] == [e["id"]] and again.list()[0]["state"] == "ready"
    pid = e["pid"]
    again.stop(e["id"])
    assert wait(lambda: not M._alive(pid))
    assert again.list()[0]["state"] == "stopped"
    again.remove(e["id"])
    assert M.Models(home).list() == []


def test_port_moved_by_swift_is_read_from_log(tmp_path):
    ms = M.Models(tmp_path)
    real = free_port()
    e = ms.start("옮김", "/x", f"{sys.executable} {FAKE} --port {real}  # --port 1", [0])   # 명령의 포트(1)와 실제 뜬 포트가 다름
    assert e["port"] == 1
    assert wait(lambda: ms.refresh(ms._entry(e["id"]))["state"] == "ready")
    assert ms._entry(e["id"])["port"] == real
    ms.stop(e["id"])


def test_exited_server_shows_exited(tmp_path):
    ms = M.Models(tmp_path)
    e = ms.start("실패", "/x", "echo boom --port 9; exit 3", [0])
    assert wait(lambda: ms.refresh(ms._entry(e["id"]))["state"] == "exited")
    assert "boom" in ms.log(e["id"])


def test_questions_are_the_benchmark_sentences(monkeypatch):
    size = [1000, 2000]
    assert Q.build({"task": "spotting"})["prompt"] == OCR["spotting"][1].format()
    assert Q.build({"task": "spotting", "lang": "en"})["prompt"] == OCR["spotting"][0].format()
    assert Q.build({"task": "bbox_ocr", "box": [100, 200, 300, 400], "size": size})["prompt"] == OCR["bbox_ocr"][1].format(box="[100, 100, 300, 200]")
    assert Q.build({"task": "grounding", "text": "성명"})["prompt"] == OCR["grounding"][1].format(text='"성명"')
    rel = Q.build({"task": "relation", "anchor_box": [0, 0, 100, 100], "direction": "below", "size": size})["prompt"]
    assert rel == OCR["relation"][1].format(direction="below", direction_ko="아래", anchor="bbox_2d=[0, 0, 100, 50] 글자")
    m = Q.build({"task": "marked_ocr", "marker": {"color": "blue", "box": [100, 100, 300, 140]}, "coords": True, "size": size})["prompt"]
    drawn = IM.norm(IM.marker_rect([100, 100, 300, 140], *size), *size)
    assert m == OCR["marked_ocr"][1].format(color="blue", color_ko="파란", coords="", coords_ko=f"(bbox_2d={json.dumps(drawn)})")
    with pytest.raises(ValueError, match="네모"):
        Q.build({"task": "bbox_ocr", "size": size})
    assert Q.build({"task": "classify"})["prompt"] == prompts.text_of(prompts.P_CLASSIFY)
    kie = Q.build({"task": "kie", "form": "loan_application", "max_keys": 3})
    assert kie["prompt"].startswith(prompts.text_of(prompts.P_KIE).split("{items}")[0]) and "applicant.name: 성명" in kie["prompt"]
    assert kie["prompt"].count("\n- ") == 3 and "앞의 3개" in kie["note"]
    marks = Q.build({"task": "marks", "form": "loan_application", "max_keys": 0})["prompt"]
    assert "(체크박스, 보기: 자가 / 전세 / 월세 / 기타)" in marks and "도장)" in marks
    # 칸 목록 fields.json 의 q (묻지 않기·항목명) 를 벤치마크처럼 따른다
    monkeypatch.setattr(Q.fieldinfo, "questions", lambda form: {"bank": {"ask": False}, "branch": {"label": "지점"}})
    k2 = Q.build({"task": "kie", "form": "loan_application", "max_keys": 2})["prompt"]
    assert "- bank:" not in k2 and "- branch: 지점" in k2


def test_images_crop_marker_fit_and_listing(tmp_path):
    img = Image.new("RGB", (3000, 4000), "white")
    big = IM.fit([img], 32)[0]
    assert IM.image_tokens_for(big.size, 32) <= IM.image_tokens_for(IM.IMAGE_MAX_SIZE, 32) and big.width / big.height == pytest.approx(0.75, abs=0.01)
    assert IM.fit([img], 32, same_as_eval=False)[0].size == (3000, 4000)
    two = IM.fit([img, img], 32)
    assert sum(IM.image_tokens_for(i.size, 32) for i in two) <= IM.PER_SAMPLE
    assert IM.crop(img, [10.4, 20, 110, 70]).size == (100, 50)
    drawn = IM.draw_markers(Image.new("RGB", (400, 300), "white"), [{"box": [100, 100, 200, 140], "color": "red"}])
    r = IM.marker_rect([100, 100, 200, 140], 400, 300)
    assert drawn.getpixel((r[0], 120)) == IM.COLORS["red"][2] and drawn.getpixel((150, 120)) == (255, 255, 255)
    (tmp_path / "a").mkdir()
    Image.new("RGB", (10, 10)).save(tmp_path / "a" / "x.png")
    pages = [Image.new("RGB", (10, 10), c) for c in ("red", "blue")]
    pages[0].save(tmp_path / "scan.tif", save_all=True, append_images=pages[1:])
    (tmp_path / "note.txt").write_text("x")
    items = IM.listing(str(tmp_path))["items"]
    assert [(Path(i["path"]).name, i["page"]) for i in items] == [("x.png", 0), ("scan.tif", 0), ("scan.tif", 1)]
    assert IM.load(str(tmp_path / "scan.tif"), 1).getpixel((0, 0)) == (0, 0, 255)


def test_read_answer():
    kie = A.read_answer("kie", '```json\n[{"key": "a.name", "value": "홍길동", "bbox_2d": [1, 2, 3, 4], "page": 2}, {"key": "b", "value": null}]\n```')
    assert kie["boxes"] == [{"box": [1, 2, 3, 4], "label": "a.name: 홍길동", "page": 2}] and not kie["format_error"]
    assert A.read_answer("spotting", "글자를 찾았습니다: 없음")["format_error"]
    assert A.read_answer("ocr_page", '[{"x": 1}]') == {"boxes": [], "format_error": False}   # 글로 답하는 과제는 JSON 으로 읽지 않음
    assert A.read_answer("custom", "설명 {\"bbox_2d\": [5, 6, 7, 8], \"label\": \"x\"} 끝")["boxes"][0]["box"] == [5, 6, 7, 8]


def test_ask_crop_markers_followup_and_log(tmp_path):
    home = tmp_path / "home"
    ms = M.Models(home)
    port = free_port()
    e = ms.start("가짜", "/x", f"{sys.executable} {FAKE} --port {port}", [0])
    try:
        assert wait(lambda: ms.refresh(ms._entry(e["id"]))["state"] == "ready")
        img = tmp_path / "doc.png"
        Image.new("RGB", (3000, 4000), "white").save(img)
        asker = A.Asker(home, ms)
        pic = [{"path": str(img), "page": 0}]
        r = asker.ask({"models": [e["id"]], "images": pic, "task": "crop_ocr", "prompt": "읽어", "op": {"crop": [0, 0, 400, 100]}})["results"][e["id"]]
        s = json.loads(r["text"])
        assert s["sizes"] == [[400, 100]] and s["prompt"] == "읽어" and s["thinking"] == {"enable_thinking": False} and s["model"] == "docgen"
        r = asker.ask({"models": [e["id"]], "images": pic * 2, "task": "ocr_page", "prompt": "받아써"})["results"][e["id"]]
        sizes = json.loads(r["text"])["sizes"]
        assert len(sizes) == 2 and sizes[0][0] < 3000   # 두 장이 한 질문의 그림 몫을 나눔
        r = asker.ask({"models": [e["id"]], "images": pic, "task": "marked_box", "prompt": 'REPLY: [{"bbox_2d": [1, 2, 3, 4], "label": "x"}]',
                       "op": {"markers": [{"color": "green", "box": [100, 100, 300, 140]}]}})["results"][e["id"]]
        assert r["boxes"][0]["box"] == [1, 2, 3, 4] and len(r["sent"]) == 1
        sent = Image.open(home / "sent" / r["sent"][0]["name"])
        assert sent.size == tuple(r["sent"][0]["size"]) and sent.size[0] < 3000
        turns = [{"prompt": "첫 질문", "answers": {e["id"]: "첫 답"}}]
        r = asker.ask({"models": [e["id"]], "images": pic, "task": "kie", "prompt": "다음 질문", "turns": turns})["results"][e["id"]]
        s = json.loads(r["text"])
        assert s["roles"] == ["user", "assistant", "user"] and s["prompt"] == "다음 질문" and len(s["sizes"]) == 1
        rows = [json.loads(x) for x in (home / "log.jsonl").read_text(encoding="utf-8").splitlines()]
        assert len(rows) == 4 and rows[-1]["turn"] == 1 and rows[0]["answers"][e["id"]]["model"] == "가짜"
        with pytest.raises(ValueError, match="질문"):
            asker.ask({"models": [e["id"]], "images": pic, "prompt": " "})
    finally:
        ms.stop(e["id"])


def test_web_api_and_static(tmp_path):
    httpd = serve(tmp_path, "127.0.0.1", 0)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{httpd.server_address[1]}"
    try:
        def get(p):
            with urlopen(base + p) as r:
                return r.read()

        def post(p, body):
            req = Request(base + p, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            with urlopen(req) as r:
                return json.load(r)

        assert b"<title>" in get("/") and b"api(" in get("/app.js")
        forms = json.loads(get("/api/forms"))
        assert {t["id"] for t in forms["tasks"]} >= {"kie", "spotting", "marked_ocr", "custom"} and len(forms["forms"]) > 400
        assert post("/api/question", {"task": "classify"})["prompt"]
        from urllib.error import HTTPError
        with pytest.raises(HTTPError) as err:
            get("/../server.py")
        assert err.value.code == 404
        with pytest.raises(HTTPError) as err:
            post("/api/question", {"task": "grounding"})
        assert err.value.code == 400 and "찾을 글자" in json.load(err.value)["error"]
        Image.new("RGB", (50, 40)).save(tmp_path / "p.png")
        listing = json.loads(get("/api/folder?dir=" + str(tmp_path)))
        assert [Path(i["path"]).name for i in listing["items"]] == ["p.png"]
        assert json.loads(get("/api/recent"))["folder"] == [str(tmp_path.resolve())]
        assert get(f"/img?path={tmp_path / 'p.png'}&page=0")[:4] == b"\x89PNG"
        assert get(f"/img?path={tmp_path / 'p.png'}&page=0&thumb=20")[:2] == b"\xff\xd8"
        models = json.loads(get("/api/models"))
        assert models["models"] == [] and models["next_port"] >= M.PORT_BASE
    finally:
        httpd.shutdown()


def test_merged_folder_missing_weights_warns_and_fills_a_copy(tmp_path):
    """합친 모델에 출발 모델의 가중치(MTP mtp.*)가 빠졌으면 알려 주고, [채운 사본 만들기] 는 <경로>-filled 새 폴더."""
    from train.tests.test_fill_weights import read_st, write_st
    from train import fill_weights as FW

    base, merged = _model(tmp_path, "base"), _model(tmp_path, "merged")
    write_st(base / "model.safetensors", {"model.a": b"AAAA", "mtp.fc": b"FCFC"})
    write_st(merged / "model.safetensors", {"model.a": b"aaaa"})
    (merged / "args.json").write_text(json.dumps({"model": str(base)}))   # swift export 가 남기는 출발 모델 경로
    info = M.inspect(str(merged))
    assert info["missing"] == {"mtp": 1} and info["fillable"]
    assert any("mtp 1개" in w and "채운 사본" in w for w in M.command(str(merged), [0], 8140)["warnings"])
    r = M.fill_copy(str(merged))
    out = tmp_path / "merged-filled"
    assert r["written"] == str(out) and read_st(out / FW.FILLED) == {"mtp.fc": b"FCFC"}
    assert sorted(p.name for p in merged.iterdir()) == ["args.json", "config.json", "model.safetensors"]   # 원본 그대로
    assert M.inspect(str(out)) == {"path": str(out), "kind": "model", "filled": True}
    assert not M.command(str(out), [0], 8141)["warnings"]
    with pytest.raises(ValueError, match="이미 있습니다"):
        M.fill_copy(str(merged))


def test_adapter_command_fills_after_merging(tmp_path):
    base = _model(tmp_path, "base")
    ck = tmp_path / "out" / "checkpoint-9"
    ck.mkdir(parents=True)
    (ck / "adapter_config.json").write_text("{}")
    (ck.parent / "args.json").write_text(json.dumps({"model": str(base)}))
    text = M.command(str(ck), [2], 8150)["command"]
    flat = text.replace(" \\\n    ", " ")
    assert f"-m train.fill_weights {base} {ck.parent / 'checkpoint-9-merged'} --in-place || echo" in flat
    assert flat.index("swift export") < flat.index("train.fill_weights") < flat.index("swift deploy")
    import subprocess
    assert subprocess.run(["bash", "-n", "-c", text]).returncode == 0
