"""원본 서식(overlay) 칸 목록에 키·값 종류를 적어 굳힌다 (한 번만 돌리는 옮기기).

예전에는 fields.json 에 key·kind 를 적지 않은 칸이 많았고, 그릴 때마다 모든 서식 공통 규칙이 항목명(지금 이름: 키 설명)을 보고
정했다 (key_rules.json 의 label_rules·kind_rules, 대리인·받는 분 구역, 금액 단위, 서명 칸 주인은 키 사전 form_keys).
이제 키는 서식마다 독립이라 그 결과를 각 서식의 fields.json 에 적어 두고, 그리는 코드(docgen/realform.py)는 칸에 적힌 것만 읽는다.
서류 분류 정답(키 사전의 문서명·다른 이름)은 서식 폴더 questions.json 의 classify 로 옮긴다.

  python -m docgen.scripts.freeze_keys                      저장소 서식 전부 (바뀌는 서식 수만 보임)
  python -m docgen.scripts.freeze_keys --write              적는다
  python -m docgen.scripts.freeze_keys --dir <서식 폴더들> --write   저장소 밖 서식(사내 서식 폴더 private_forms_dir)도 같은 방법으로

규칙은 이 파일 옆 freeze_keys_rules.json (옮기기 전 key_rules.json 의 label_rules·kind_rules 그대로).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RULES = json.loads((Path(__file__).with_name("freeze_keys_rules.json")).read_text(encoding="utf-8"))
_LABEL = [(re.compile(rx), k) for rx, k in RULES["label_rules"]]
_KIND = [(re.compile(rx), k) for rx, k in RULES["kind_rules"]]
AGENT_SEC = re.compile(r"대리|수임|위임장|위임받|피위임")
FOREIGN_SEC = re.compile(r"받는|받으실|수취|Beneficiary|BENEFICIARY|상대방")
MONEY_UNITS = ("원", "천원", "만원", "백만원", "억원", "%", "명", "개", "건", "회")


def norm(s: str | None) -> str:
    from docgen.realform import norm as _n

    return _n(s)


def key_of(label: str) -> str | None:
    n = norm(label)
    return next((k for rx, k in _LABEL if rx.match(n)), None)


def kind_of(label: str, unit: str | None, hint: str | None) -> str:
    if unit in ("원", "천원", "백만원", "만원", "억원", "원정"):
        return "amount"
    if unit == "%":
        return "percent"
    if unit in ("개월", "년", "회", "건", "명", "주", "개", "매", "좌", "세", "일간", "개년"):
        return "count"
    n = norm(label)
    return next((k for rx, k in _KIND if rx.search(n)), "text")


def text_key(it: dict) -> tuple[str | None, str]:
    """예전 realform._text_key 그대로: 칸의 키(없으면 None)와 값 종류."""
    label = it.get("label") or ""
    skey = it.get("key") or key_of(label)
    kind = it.get("kind") or kind_of(label, it.get("unit"), it.get("hint"))
    if not it.get("key") and it.get("unit") in MONEY_UNITS:
        skey = None
    sec = norm(it.get("section") or "")
    if it.get("key"):
        pass
    elif skey and AGENT_SEC.search(sec) and skey.startswith("customer."):
        skey = "agent." + skey.split(".", 1)[1]
    elif skey and FOREIGN_SEC.search(sec) and (skey.startswith("customer.") or skey == "account"):
        skey = "foreign." + (skey.split(".", 1)[1] if "." in skey else "account")
    return skey, kind


def freeze_items(items: list[dict], sign_who: dict[int, dict]) -> int:
    """칸 목록을 고쳐 적는다 (바꾼 칸 수). sign_who: 서명 칸 순번 → {who, what}."""
    rows: dict[tuple, int] = {}
    for it in items:
        if it["t"] == "text" and it.get("row"):
            k = (it["page"], it.get("group") or "", norm(it.get("label")))
            rows[k] = rows.get(k, 0) + 1
    n = 0
    for i, it in enumerate(items):
        before = json.dumps(it, sort_keys=True, ensure_ascii=False)
        label = it.get("label") or ""
        t = it["t"]
        if t == "text" and it.get("row") and rows[(it["page"], it.get("group") or "", norm(label))] > 1:
            if not it.get("key"):
                base = f"{norm(it.get('group') or '')}_목록" if norm(it.get("group") or "") else "목록"
                it["key"] = f"{base}.{{i}}.{norm(label) or 'value'}"
            it.setdefault("kind", kind_of(label, it.get("unit"), it.get("hint")))
        elif t == "text":
            skey, kind = text_key(it)
            it["kind"] = kind
            if not (kind == "seal" and not skey):   # 도장 자리(키 없는 seal)는 키를 적지 않는다
                if not skey:
                    it["std"] = False   # 고객 정보가 아니라 값 종류로 만드는 칸 (예전 '항목명 그대로' 키)
                it["key"] = skey or norm(label) or "value"
        elif t == "check" and it.get("options") and not it.get("key"):
            texts = [o["text"] or f"보기{j + 1}" for j, o in enumerate(it["options"])]
            it["key"] = "check." + (norm(label) or norm(texts[0])[:12] or "item")
        elif t == "date" and not it.get("key"):
            it["key"] = (key_of(label) or "date") if label else "date"
        elif t == "sign" and i in sign_who:
            for k, v in sign_who[i].items():
                if v and not it.get(k):
                    it[k] = v
        n += json.dumps(it, sort_keys=True, ensure_ascii=False) != before
    return n


def sign_owners(doc_id: str, items: list[dict]) -> dict[int, dict]:
    """키 사전(form_keys)이 정한 서명 칸의 주인: 칸 순번 → {who, what}. 예전 realform._signer_name 과 같은 찾기."""
    from docgen import dictionary as DIC
    from docgen.realform import _uniq_fn

    fk = DIC.form_entries(doc_id)
    if not fk:
        return {}
    # 서명 칸의 자리 이름(role)은 그릴 때 모든 칸이 같이 쓰는 번호 붙이기로 정해진다 — layout_keys 와 같은 순서로 다시 센다
    from docgen import realform as RF

    keys = RF.layout_keys(doc_id)
    by_id = {it.get("_id"): i for i, it in enumerate(items)}
    out = {}
    for iid, info in keys.items():
        if info["t"] != "sign" or iid not in by_id:
            continue
        role = next(k[5:] for k in info["keys"] if k.startswith("seal."))
        e = fk.get(f"{role}.name") or fk.get(f"sign.{role}") or fk.get(f"seal.{role}") or {}
        who, what = e.get("who"), (fk.get(f"{role}.name") or {}).get("what")
        if who:
            out[by_id[iid]] = {"who": who, **({"what": what} if what else {})}
    _ = _uniq_fn
    return out


def classify_answer(doc_id: str, name: str) -> dict | None:
    """키 사전의 문서명·다른 이름이 서식 이름과 다르면 questions.json 의 classify 로 적을 것."""
    from docgen import dictionary as DIC

    answer, aliases = DIC.doc_name(doc_id, name)
    if answer == name and not aliases:
        return None
    return {"answer": answer, **({"aliases": aliases} if aliases else {})}


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dir", help="이 폴더 아래 서식 폴더들만 (기본: 저장소 docgen/forms)")
    a = ap.parse_args(argv)
    from docgen import formdir
    from docgen import formquestions as FQ
    from docgen.realform import form_layout
    from docgen.registry import load_all

    reg = load_all()
    root = Path(a.dir).resolve() if a.dir else None
    changed_f = changed_q = 0
    for doc_id, spec in reg.items():
        d = formdir.folder(doc_id)
        if d is None or (root and root not in d.resolve().parents):
            continue
        if not a.dir and "docgen/forms" not in d.resolve().as_posix():
            continue
        if spec.template == "_real_form.html.j2" and (d / "fields.json").exists():
            body = json.loads((d / "fields.json").read_text(encoding="utf-8"))
            if "items" in body:
                lay, _ = form_layout(doc_id)   # _id 를 붙인 사본 (서명 칸 찾기용)
                owners = sign_owners(doc_id, lay["items"])
                n = freeze_items(body["items"], owners)
                if n:
                    changed_f += 1
                    if a.write:
                        (d / "fields.json").write_text(json.dumps(body, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        cl = classify_answer(doc_id, spec.name)
        q = FQ.read(doc_id) or {}
        if cl and not (q.get("classify") or {}).get("answer"):
            changed_q += 1
            if a.write:
                q["classify"] = {**(q.get("classify") or {}), **cl}
                FQ.write(doc_id, q)
    print(f"fields.json {changed_f}개, questions.json(분류 정답) {changed_q}개 {'적음' if a.write else '바뀔 것 (--write 로 적기)'}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
