"""④ 서류 넣기 시험 폴더 (studio/intake_testset.py): 두 벌이 결과 폴더 검사를 통과하고 정답과 맞는다."""
import json

import pytest

from studio import intake_testset as T
from studio import results as R


@pytest.fixture(scope="module")
def made(tmp_path_factory):
    out = tmp_path_factory.mktemp("intake")
    truth = T.build(out, ["fx_remittance"], 2, ["commercial_invoice"], scale=1.0, conditions=(("clean", 1.0),),
                    missing=0.0, no_pred=0.0, p_wrong=0.0, p_drop=0.0, log=lambda *a: None)
    return out, truth


def test_both_sets_pass_results_check(made):
    out, truth = made
    for name in ("structured", "flat"):
        res = R.check(str(out / name))
        assert res["ok"], res["errors"]
        assert res["summary"]["documents"] == len(truth["documents"])
        assert res["summary"]["with_pred"] == len(truth["documents"])


def test_truth_maps_structured_and_flat(made):
    out, truth = made
    docs = truth["documents"]
    assert {d["case"] for d in docs.values()} == {"C70000", "C70001"}
    assert {d["role"] for d in docs.values()} == set(truth["scenarios"]["fx_remittance"]["roles"])
    assert any(d["new_form"] for d in docs.values()) and all(d["new_form"] == (d["form"] == "commercial_invoice") for d in docs.values())
    for rel, d in docs.items():
        assert rel.startswith(f"fx_remittance/{d['case']}/d")
        assert d["form"] not in rel and d["form"] not in d["flat"]           # 경로에 서식 ID 가 드러나지 않는다
        assert len(list((out / "structured/images" / rel).glob("p*"))) == d["pages"]
        assert len(list((out / "flat/images" / d["flat"]).glob("p*"))) == d["pages"]
        a = json.loads((out / "structured/pred" / f"{rel}.json").read_text(encoding="utf-8"))
        b = json.loads((out / "flat/pred" / f"{d['flat']}.json").read_text(encoding="utf-8"))
        assert a == b and a["items"]


def test_pred_matches_ocr_words(made):
    """오류를 넣지 않았으면 추출 값의 글자는 같은 쪽 OCR 에 들어 있고, 박스는 OCR 단어와 겹친다."""
    out, truth = made
    for rel, d in truth["documents"].items():
        items = json.loads((out / "structured/pred" / f"{rel}.json").read_text(encoding="utf-8"))["items"]
        for it in [x for x in items if x.get("type") is None and x.get("bbox_2d")][:5]:
            page = json.loads((out / "structured/ocr" / rel / f"p{it['page']}.json").read_text(encoding="utf-8"))
            words = page["data"]["basicData"][0]
            text = "".join(w["text"] for w in words).replace(" ", "")
            first = it["value"].split()[0]
            assert first.replace(" ", "") in text, (rel, it)


def test_noisy_records_errors():
    import random

    items = [{"key": "customer.name", "value": "홍길동"}, {"key": "loan.amount", "value": "1,000"}]
    out, errs = T.noisy(items, random.Random(1), p_wrong=1.0, p_drop=0.0)
    assert out[0]["key"] == "name"                                            # 다른 키 이름
    assert all(e["kind"] == "wrong" for e in errs) and len(errs) >= 1
    assert all(o["value"] != i["value"] for o, i in zip(out, items) if any(e["key"] == i["key"] for e in errs))


def test_external_bundle_placed_into_cases(tmp_path):
    truth = T.build(tmp_path / "o", ["fx_remittance"], 2, [], scale=1.0, conditions=(("clean", 1.0),), missing=0.0,
                    external=T.EXTERNAL, log=lambda *a: None)
    ext = {r: d for r, d in truth["documents"].items() if d.get("external")}
    assert len(ext) == 15
    fx = [r for r, d in ext.items() if d["scenario"] == "fx_remittance"]
    assert len(fx) == 12 and all(r.split("/")[1] in ("C70000", "C70001") and r.split("/")[2].startswith("d") for r in fx)
    assert all(d["license"] in ("MIT", "Apache-2.0") and len(d["sha256"]) == 64 and d["source"].startswith("https://github.com/")
               for d in ext.values())
    # 업무가 없는 종류(account_opening 에 넣을 서식·기타)는 external/ 그대로
    assert {d["scenario"] for r, d in ext.items() if r not in fx} == {"external"}
    res = R.check(str(tmp_path / "o" / "structured"))
    assert res["ok"], res["errors"]


def test_external_locate_variants():
    from studio import intake_external as E

    words = [{"text": t, "bbox": [i * 10, 0, i * 10 + 8, 10]} for i, t in enumerate(["Date:", "8-9-2022", "Total", "EUR", "4.904,94"])]
    assert E.locate("2022-09-08", words) == [10, 0, 18, 10]       # 0 없이 찍힌 날짜
    assert E.locate(4904.94, words) == [40, 0, 48, 10]            # 소수점 쉼표·천 단위 점
    assert E.locate("nl", [{"text": "SCONL0303", "bbox": [0, 0, 90, 10]}]) is None   # 짧은 값은 단어 안 일부로 찾지 않는다
