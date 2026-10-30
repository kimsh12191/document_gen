"""칸 키는 한 곳에서: 영역 편집기가 보여 주는 키(realform.layout_keys)와 렌더링 정답의 키가 같고,
서명 칸 이름은 키 사전에서 정한 '누구의'를 따른다 (docgen/dictionary.py form_keys)."""
import pytest

from docgen import dictionary as DIC
from docgen import realform as RF
from docgen.entities import make_profile
from docgen.registry import load_all
from docgen.render import render

REG = load_all()
OVERLAY = sorted(i for i, s in REG.items() if s.template == "_real_form.html.j2")


@pytest.mark.parametrize("seed", [0, 7])
def test_editor_keys_match_rendered_keys(seed):
    """별지(인쇄된 줄을 넘친 표 행)의 칸은 편집기에 영역이 없다 — 같은 표·같은 열의 인쇄된 칸 키와 행 번호만 다르면 된다."""
    from docgen.formquestions import pattern

    bad = {}
    for doc_id in OVERLAY:
        keys = {k for v in RF.layout_keys(doc_id).values() for k in v["keys"]}
        _, fields, data = render(REG[doc_id], make_profile(seed), seed)
        cont = {c["key"] for t in data.get("extra_rows") or [] for r in t["rows"] for c in r["cells"]}
        extra = {f["key"] for f in fields} - keys - cont
        extra |= {k for k in cont if pattern(k) not in {pattern(x) for x in keys}}
        if extra:
            bad[doc_id] = sorted(extra)[:5]
    assert not bad, bad


def test_signer_name_follows_who():
    """은행·직원으로 정한 서명 칸에는 고객 이름을 쓰지 않는다."""
    hits = [(fid, k) for fid, ks in DIC.load("form_keys")["forms"].items() if fid in OVERLAY
            for k, e in ks.items() if e.get("who") == "bank" and k.endswith(".name") and k.startswith("signer")]
    assert hits
    for fid, k in hits[:20]:
        for seed in range(3):
            p = make_profile(seed)
            _, fields, _ = render(REG[fid], p, seed)
            v = next((f["value"] for f in fields if f["key"] == k), None)
            assert v != p.person.name, (fid, k)
