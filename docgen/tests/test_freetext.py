"""기타 칸 정리(freetext): 글과 정답 만들기, 칸 고르기, 생성 중 모으기, 채점."""
import json
import random
from datetime import date

from docgen import freetext as FT
from docgen.bench import evaluate as E
from docgen.bench.prompts import freetext_prompt
from docgen.bench.runner import oracle_output


def test_record_matches_text():
    today = date(2026, 10, 24)
    for i in range(300):
        r = random.Random(i)
        text, rec, level = FT.make(r, today, ["purpose", "reason", "note"][i % 3], r.choice([2, 3, 4]))
        assert set(rec) <= {*FT.KEYS, "approx"} and rec and None not in rec.values()
        assert level in ("simple", "abbrev", "relative", "approx")
        for k in ("purpose", "reason", "request"):
            if k in rec:
                assert rec[k] in FT.VOCAB[k]
        if "memo" in rec:
            assert rec["memo"] in text
        if "date" in rec:
            assert date.fromisoformat(rec["date"]) > today
        assert set(rec.get("approx", [])) <= set(rec)
        assert (level == "approx") == bool(rec.get("approx"))


def test_relative_dates():
    today = date(2026, 12, 20)
    seen = {}
    for i in range(400):
        d, text, rough, rel = FT._date(random.Random(i), today)
        seen[text] = (d, rough)
    assert seen["다음달 말"] == (date(2027, 1, 31), False)
    assert seen["다음달 중순"] == (date(2027, 1, 15), True)
    assert seen["다음주"] == (date(2026, 12, 27), True)


def test_amount_words():
    assert FT.korean_number(3000) == "삼천" and FT.korean_number(1500) == "천오백" and FT.korean_number(25) == "이십오"
    for i in range(200):
        won, text, _ = FT._amount(random.Random(i))
        if text.endswith("천"):   # '3천' = 3천만원
            assert won == int(text[:-1]) * 10_000_000


def test_slot_of():
    assert FT.slot_of("비 고") == "note" and FT.slot_of("기타") == "note"
    assert FT.slot_of("해지사유") == "reason" and FT.slot_of("자금용도") == "purpose"
    assert FT.slot_of("수집·이용목적") is None and FT.slot_of("성명") is None and FT.slot_of("口EIN口GIIN口기타") is None


def test_fill_records_answer_and_respects_fit():
    with FT.collect() as sink:
        texts = [FT.fill("비고", f"k{i}", date(2026, 1, 1), lambda s: True) for i in range(50)]
        never = [FT.fill("비고", f"k{i}", date(2026, 1, 1), lambda s: False) for i in range(50)]
    got = [t for t in texts if t]
    assert 5 < len(got) < 45 and not any(never)
    assert set(got) == set(sink) and all(sink[t]["basis"] == "2026-01-01" for t in got)
    assert FT.fill("성명", "k", date(2026, 1, 1), lambda s: True) is None
    assert FT.fill("비고", "k3", date(2026, 1, 1), lambda s: True) == texts[3]   # 같은 칸이면 같은 글


def _item(answer):
    return {"task": "freetext", "answer": answer, "prompt": freetext_prompt("비고", "2026-10-24"), "meta": {}}


def test_score():
    it = _item({"purpose": "생활자금", "amount": 30000000, "date": "2026-11-30", "memo": "배우자 동의함", "approx": ["amount"]})
    m = E.s_freetext(it, oracle_output(it))["metrics"]
    assert m["f1"] == 1.0 and m["doc_exact"] == 1.0 and m["extra_key"] == 0.0
    # 표기가 달라도 같은 값으로 봐 주지 않는다 (kie 와 다름). memo 만 띄어쓰기 허용
    r = E.s_freetext(it, json.dumps({"purpose": "생활비", "amount": "30,000,000", "date": "2026.11.30",
                                     "memo": "배우자동의함", "approx": ["amount"]}, ensure_ascii=False))
    assert dict((k, ok) for _, k, ok in r["sub"]) == {"purpose": False, "amount": True, "date": False, "memo": True}
    # 정답에 없는 키를 지어내면 정밀도·extra_key
    m = E.s_freetext(it, json.dumps({**it["answer"], "request": "전화 연락"}, ensure_ascii=False))["metrics"]
    assert m["extra_key"] == 0.2 and m["f1"] < 1.0 and m["doc_exact"] == 0.0
    # null 은 답하지 않은 것으로
    m = E.s_freetext(it, json.dumps({**it["answer"], "reason": None}, ensure_ascii=False))["metrics"]
    assert m["f1"] == 1.0
    assert E.s_freetext(it, "모르겠습니다")["parse_fail"]
    assert E.reward("freetext", oracle_output(it), it) == 1.0


def test_prompt_lists_choices():
    p = freetext_prompt("해지사유", "2026-10-24")
    assert "'해지사유' 칸" in p and "2026-10-24" in p
    assert all(c in p for c in [*FT.PURPOSES, *FT.REASONS, *FT.REQUESTS])


def test_render_puts_text_on_form():
    """원본 서식을 그리면 기타 칸에 글이 들어가고, 그 글의 정답이 data["_freetext"] 로 나온다 (bench build 가 문항으로)."""
    from docgen.entities import make_profile
    from docgen.registry import load_all
    from docgen.render import render

    spec = load_all()["hf430"]   # 민원신청서: 기타·비고 칸
    found = 0
    for seed in range(12):
        _, raw, data = render(spec, make_profile(seed), seed)
        values = {f["value"] for f in raw}
        for text, ft in (data.get("_freetext") or {}).items():
            assert text in values and ft["answer"] and ft["level"]
            found += 1
    assert found
