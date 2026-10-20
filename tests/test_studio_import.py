"""7단계 시험: 가져오기(묶기·템플릿·값 자리 초안), OCR 검수 저장·통계, 검수본으로 1부 OCR 세트. 사내 OCR·브라우저 없이
(쪽 그림은 흰 종이, OCR 결과는 사내 OCR 형식 JSON 을 직접 만든다)."""
import json

import pytest
from PIL import Image

from studio import formats as F
from studio import importer as IM
from studio import ocr_review as OR
from docgen import ocr_export as X

W, H = 1000, 1400
FORMS = {   # 서식마다 (제목, [(항목명, x, y)]) — 값은 항목명 오른쪽 x+200
    "pay": ("급여명세서", [("성명", 100, 300), ("지급총액", 100, 400), ("공제총액", 100, 500), ("실수령액", 100, 600)]),
    "tax": ("납세증명서", [("납세자", 100, 250), ("주민등록번호", 100, 350), ("발급번호", 100, 450), ("세무서장", 450, 1200)]),
}
VALUES = [["김하나", "3,100,000원", "210,000원", "2,890,000원"], ["이두리", "4,200,000원", "380,000원", "3,820,000원"],
          ["박세찬", "2,750,000원", "190,000원", "2,560,000원"]]


def words_of(form, k, dx=0.0, dy=0.0, s=1.0):
    title, labels = FORMS[form]
    out = [(title, 380, 120, 620, 170)]
    for (lab, x, y), val in zip(labels, VALUES[k]):
        out.append((lab, x, y, x + 25 * len(lab), y + 30))
        out.append((val + str(k) if form == "tax" else val, x + 200, y, x + 200 + 22 * len(val), y + 30))
    return [{"text": t, "bbox": [x0 * s + dx, y0 * s + dy, x1 * s + dx, y1 * s + dy]} for t, x0, y0, x1, y1 in out]


def ocr_json(words, name):
    items = [X.item(w["text"], w["bbox"], 0.99 if i % 7 else 0.6, i) for i, w in enumerate(words)]
    return X.page_document(items, name)


@pytest.fixture
def batch(tmp_path, monkeypatch):
    """서식 둘 × 문서 셋 (급여명세서 하나는 스캔처럼 밀리고 커진 쪽)."""
    ws = tmp_path / "ws"
    b = ws / "imports" / "t"
    (b / "pages").mkdir(parents=True)
    rows = []
    for form in FORMS:
        for k in range(3):
            words = words_of(form, k, *((12, -8, 1.02) if (form, k) == ("pay", 2) else ()))
            img = tmp_path / "src" / f"{form}{k}.png"
            img.parent.mkdir(exist_ok=True)
            Image.new("RGB", (W, H), "white").save(img)
            oj = tmp_path / "src" / f"{form}{k}.json"
            oj.write_text(json.dumps(ocr_json(words, img.name), ensure_ascii=False), encoding="utf-8")
            rows.append({"id": f"{form}{k}/p1", "doc": f"{form}{k}", "source": str(img), "page": 1, "ocr_json": str(oj), "truth": form})
    IM._write_json(b / "batch.json", {"name": "t", "source": {"kind": "docgen"}, "real_data": True, "public": False,
                                      "ocr": {"revision": "test", "cache_dir": str(tmp_path / "cache")}, "stage": "listed"})
    IM._write_jsonl(b / "pages.jsonl", rows)
    IM.run_ocr(b)
    return b


def test_group_formats(batch):
    fx = IM.run_group(batch)
    rows = {r["id"]: r for r in IM._jsonl(batch / "pages.jsonl")}
    groups = sorted(sorted(rows[p]["truth"] for p in f["pages"]) for f in fx["formats"])
    assert groups == [["pay"] * 3, ["tax"] * 3]
    assert {f["name"] for f in fx["formats"]} == {"급여명세서", "납세증명서"}
    # 사람이 정한 이름·결정은 다시 묶어도 남는다
    fid = fx["formats"][0]["id"]
    IM.set_decision(batch, fid, {"kind": "skip"}, "내 이름")
    again = {f["id"]: f for f in IM.run_group(batch)["formats"]}
    assert again[fid]["name"] == "내 이름" and again[fid]["decision"] == {"kind": "skip"}
    # 따로 떼기 → 새 포맷, 합치기 → 다시 하나
    one = again[fid]["pages"][:1]
    out = IM.split_pages(batch, one, "떼어 낸 것")
    new = next(f for f in out["formats"] if f["pages"] == one)
    assert new["name"] == "떼어 낸 것" and len(out["formats"]) == 3
    merged = IM.merge_formats(batch, new["id"], fid)
    assert len(merged["formats"]) == 2


def test_affine_alignment():
    ref = words_of("pay", 0)
    moved = words_of("pay", 0, 30, -20, 1.05)
    back = IM._aligned(ref, moved)
    for a, b in zip(ref, back):
        assert all(abs(x - y) < 0.5 for x, y in zip(a["bbox"], b["bbox"]))


def test_value_drafts_labels_and_values():
    sample = [words_of("pay", 0)]
    others = [[words_of("pay", 1)], [words_of("pay", 2, 12, -8, 1.02)], [words_of("tax", 0)]]   # 다른 서식은 견주기에서 빠진다
    dr = IM.value_drafts(sample, others, [(W, H)])
    got = {a["label"]: a["note"].split(": ", 1)[1] for a in dr["add"]}
    assert got == {"성명": "김하나", "지급총액": "3,100,000원", "공제총액": "210,000원", "실수령액": "2,890,000원"}
    assert len(dr["erase"]) == 4 and all(e["fill"] == "auto" for e in dr["erase"])
    x0, y0, x1, y1 = dr["erase"][0]["rect"]
    assert x0 < 300 < x1 and y0 < 315 < y1   # 값 단어를 덮는다


def test_template_private_and_drafts(batch, tmp_path, monkeypatch):
    from docgen import overrides as OV
    from docgen import realform as RF

    monkeypatch.setattr(RF, "IMAGE_FORMS", tmp_path / "public_forms")
    fx = IM.run_group(batch)
    pay = next(f for f in fx["formats"] if f["name"] == "급여명세서")
    with pytest.raises(ValueError, match="private_forms_dir"):   # 실서류 묶음은 저장소에 만들지 않는다
        IM.create_template(batch, pay["id"], pay["docs"]["pay0"], "img_pay_test", "급여", None)
    priv = tmp_path / "private"
    monkeypatch.setenv("DOCGEN_PRIVATE_FORMS", str(priv))
    res = IM.create_template(batch, pay["id"], pay["docs"]["pay0"], "img_pay_test", "급여", str(priv))
    assert res["private"] and res["drafts"] == 4 and (priv / "img_pay_test" / "page_0.png").exists()
    assert not (tmp_path / "public_forms").exists()
    lay = json.loads((priv / "img_pay_test" / "layout.json").read_text(encoding="utf-8"))
    assert lay["pages"][0]["width"] == pytest.approx(W / RF.BG_ZOOM, abs=0.01) and lay["texts"]
    assert OV.path("img_pay_test") == priv / "img_pay_test" / "overrides.json"   # 수정도 서식 폴더 (저장소 밖)
    ov = OV.load("img_pay_test")
    assert {a["label"] for a in ov["add"]} == {"성명", "지급총액", "공제총액", "실수령액"}
    # 지운 값은 배경 글자(합성 OCR 정답)에서 빠진다
    bg = X.background_words("img_pay_test")[0]
    assert "김하나" not in [w["text"] for w in bg] and "성명" in [w["text"] for w in bg]
    dec = next(f for f in IM.run_group(batch)["formats"] if f["id"] == pay["id"])["decision"]
    assert dec["kind"] == "template" and dec["form_id"] == "img_pay_test"


def test_ocr_review_and_reviewed_set(batch, tmp_path):
    root = tmp_path / "real" / "ocr_reviewed"
    page = OR.load_page(batch, "pay0/p1", root)
    assert page["reviewed_file"] is None and len(page["words"]) == len(page["original"]) == 9
    order = OR.suspicious_order(page)
    assert page["words"][order[0]]["confidence"] < 0.9   # 신뢰도 낮은 것 먼저
    ws = [dict(w) for w in page["words"]]
    ws[1]["text"] = "성 명"; ws[1]["edited"] = True          # 고침
    del ws[2]                                                  # 뺌
    ws.append({"text": "추가", "bbox": [700, 1300, 760, 1330]})  # 더함
    ws.append({"text": "", "bbox": [1, 1, 5, 5]})              # 빈 글자는 저장하지 않는다
    st = OR.save_page(batch, "pay0/p1", ws, root, "tester", done=False)
    assert st["status"] == "in_progress" and st["stats"]["changed"] == 1 and st["stats"]["added"] == 1 and st["stats"]["deleted"] == 1
    again = OR.load_page(batch, "pay0/p1", root)
    assert again["reviewed_file"] and "추가" in [w["text"] for w in again["words"]]
    assert OR.summary(root, "t") == {"done": 0, "in_progress": 1}
    with pytest.raises(ValueError, match="확인한 쪽이 없습니다"):
        IM.ocr_set_files(batch, tmp_path / "set0", None, "reviewed", "benchmark", root)
    st = OR.save_page(batch, "pay0/p1", again["words"], root, "tester", done=True)
    saved = json.loads((root / "t" / "pay0__p1.json").read_text(encoding="utf-8"))
    assert {i["confidence"] for i in saved["data"]["basicData"][0]} == {1.0}   # 확인한 쪽은 모두 사람이 본 글자
    assert OR.reviewed_pages(root, "t") == {"pay0/p1"} and OR.summary(root, "t")["done"] == 1
    # 검수본 정답으로 1부 세트
    info = IM.ocr_set_files(batch, tmp_path / "set", None, "reviewed", "benchmark", root)
    cfg = json.loads((tmp_path / "set" / "config.json").read_text(encoding="utf-8"))
    man = IM._jsonl(tmp_path / "set" / "manifest.jsonl")
    assert info["pages"] == 1 and man[0]["ocr_json"].endswith("pay0__p1.json")
    assert cfg["reference_type"] == "human_reviewed" and cfg["filters"]["benchmark"]["min_confidence"] == 0.0
    assert cfg["benchmark_only"] and cfg["studio"]["gt"] == "reviewed" and cfg["studio"]["real_data"]
    from bank_ocr.pipeline import prepare

    prepare(tmp_path / "set" / "config.json")
    done = json.loads((tmp_path / "set" / "prepared" / "DONE.json").read_text(encoding="utf-8"))
    assert done["reference_type"] == "human_reviewed" and done["human_reviewed"] is True
    task = json.loads((tmp_path / "set" / "prepared" / "benchmark_tasks.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert task["reference_type"] == "human_reviewed"
    # 사내 OCR 그대로는 예전 표시 그대로
    IM.ocr_set_files(batch, tmp_path / "set2", None, "pseudo", "benchmark", root)
    assert "reference_type" not in json.loads((tmp_path / "set2" / "config.json").read_text(encoding="utf-8"))


def test_reference_type_rejects_unknown(tmp_path, batch):
    from bank_ocr.pipeline import prepare

    IM.ocr_set_files(batch, tmp_path / "s", None, "pseudo", "benchmark", None, {"reference_type": "guess"})
    with pytest.raises(ValueError, match="reference_type"):
        prepare(tmp_path / "s" / "config.json")


def test_fingerprint_title():
    fp = F.fingerprint([dict(w, line_num=i) for i, w in enumerate(words_of("tax", 0))], W, H)
    assert fp["title"] == "납세증명서" and fp["tokens"]


def test_unreviewed_imported_forms_stay_out_of_builds(batch, tmp_path, monkeypatch):
    """가져온 서식은 등록되자마자 목록·편집기에 나오지만, 검수 전에는 "all"·그룹 선택으로 데이터셋에 들어가지 않는다."""
    from docgen import ocr_set
    from docgen import realform as RF
    from docgen.registry import REGISTRY

    priv = tmp_path / "private"
    monkeypatch.setenv("DOCGEN_PRIVATE_FORMS", str(priv))
    fx = IM.run_group(batch)
    pay = next(f for f in fx["formats"] if f["name"] == "급여명세서")
    IM.create_template(batch, pay["id"], pay["docs"]["pay0"], "img_pay_test", "급여", str(priv))
    monkeypatch.setitem(REGISTRY, "img_pay_test", None)   # 시험이 끝나면 등록을 지운다
    del REGISTRY["img_pay_test"]
    assert RF.register_images() == 1 and REGISTRY["img_pay_test"].group == "imported"
    monkeypatch.setattr(ocr_set, "_reviewed", lambda: set())
    assert "img_pay_test" not in ocr_set.select_ids({"types": "all"})
    assert ocr_set.select_ids({"types": ["imported"]}) == []
    assert ocr_set.select_ids({"types": ["img_pay_test"]}) == ["img_pay_test"]
    monkeypatch.setattr(ocr_set, "_reviewed", lambda: {"img_pay_test"})
    assert "img_pay_test" in ocr_set.select_ids({"types": "all"})
