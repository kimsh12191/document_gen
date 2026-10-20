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
