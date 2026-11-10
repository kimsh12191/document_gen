"""qlabel 라벨 → ms-swift·과제 폴더 변환 (docgen.bench.qlabel)."""
import json

from PIL import Image

from docgen.bench.evaluate import SCORERS
from docgen.bench.prompts import P_KIE
from docgen.bench.qlabel import convert, main


def _fixture(tmp_path, size=(1658, 2346)):
    (tmp_path / "imgs" / "images").mkdir(parents=True)
    Image.new("RGB", size, "white").save(tmp_path / "imgs" / "images" / "a_1_3.png")
    W, H = 1658, 2346
    labels = [["/{img_dir}/images/a_1_3.png", {
        "BANK_ISSUE_CODE": [{"text": "KOEXKRSE", "bbox_2d": [[W, H], [303.19, 1785.14], [410.61, 1785.14],
                                                              [410.61, 1807.0], [303.19, 1807.0]]}],
        "APPLICANT_NAME": [{"text": "HENGLI PETROCHEMICAL", "bbox_2d": [[W, H], [141.9, 492.1], [656.2, 492.1],
                                                                         [656.2, 520.0], [141.9, 520.0]]},
                           {"text": "INTERNATIONAL PTE. LTD.", "bbox_2d": [[W, H], [141.9, 530.0], [600.0, 530.0],
                                                                            [600.0, 560.0], [141.9, 560.0]]}],
        "REMARK": [{"text": "", "bbox_2d": [[W, H], [1, 1], [2, 1], [2, 2], [1, 2]]}]}],
              ["/{img_dir}/images/missing.png", {"X": []}]]
    f = tmp_path / "qlabel.json"
    f.write_text(json.dumps(labels), encoding="utf-8")
    return f


def test_converts_tags_present_per_image_with_boxes(tmp_path):
    f = _fixture(tmp_path)
    rep = convert([f], str(tmp_path / "imgs"), tmp_path / "out")
    assert rep["images"] == 1 and rep["skipped"][0]["reason"] == "그림 파일 없음"
    row = json.loads((tmp_path / "out" / "train.jsonl").read_text().splitlines()[0])
    user, asst = row["messages"]
    assert user["content"].startswith("<image>") and row["images"][0].endswith("a_1_3.png")
    assert user["content"][len("<image>"):] == P_KIE.format(
        items="- BANK_ISSUE_CODE: -\n- APPLICANT_NAME: -\n- REMARK: -")
    ans = json.loads(asst["content"])
    assert ans[0] == {"key": "BANK_ISSUE_CODE", "value": "KOEXKRSE", "bbox_2d": [183, 761, 248, 770], "page": 1}
    assert ans[1]["value"] == "HENGLI PETROCHEMICAL INTERNATIONAL PTE. LTD."    # 칸 둘 → 이은 값·감싸는 박스
    assert ans[1]["bbox_2d"] == [86, 210, 396, 239]
    assert ans[2] == {"key": "REMARK", "value": None}
    # 과제 폴더: 정답을 그대로 내면 만점
    it = json.loads((tmp_path / "out" / "tasks" / "kie.jsonl").read_text().splitlines()[0])
    meta = json.loads((tmp_path / "out" / "meta.json").read_text())
    assert meta["format"] == "docgen-tasks/1" and it["answer"] == ans
    assert SCORERS["kie"](it, asst["content"])["metrics"]["f1"] == 1.0


def test_options_pixel_each_maxkeys_and_test_split(tmp_path):
    f = _fixture(tmp_path, size=(829, 1173))   # 그림이 라벨 크기의 절반 → 꼭짓점도 절반
    out = tmp_path / "o"
    assert main([str(f), "--img-dir", str(tmp_path / "imgs"), "--out", str(out), "--coord", "pixel",
                 "--multi", "each", "--max-keys", "2", "--split", "test"]) == 0
    items = [json.loads(x) for x in (out / "tasks" / "kie.jsonl").read_text().splitlines()]
    assert len(items) == 2 and not (out / "train.jsonl").exists()
    assert all(i["meta"]["split"] == "benchmark" for i in items)
    assert items[0]["answer"][0]["bbox_2d"] == [152, 893, 205, 904]
    assert [e["value"] for e in items[0]["answer"][1:]] == ["HENGLI PETROCHEMICAL", "INTERNATIONAL PTE. LTD."]
    assert json.loads((out / "REPORT.json").read_text())["notes"]
