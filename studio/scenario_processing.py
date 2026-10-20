"""③ 처리 설정 시험 실행. 합성 정답으로 계산하며 모델을 호출하지 않는다."""
from __future__ import annotations

import random

from docgen.bench import processing as P
from docgen.bench.cases import CASES, Ctx
from docgen.bench.rules import Bundle, RULES, r_doc_valid
from docgen.bench.prompts import P_DOC_CHECK, P_CROSS, P_REVIEW
from docgen.bench.runner import oracle_output
from docgen.entities import make_profile
from docgen.registry import load_all


class EvidenceBundle(Bundle):
    def __init__(self, scenario, docs):
        super().__init__(scenario, docs)
        self.used = []

    def f(self, doc, key):
        field = super().f(doc, key)
        if field and (doc, key) not in self.used:
            self.used.append((doc, key))
        return field


def run(scenario: dict, seed: int, render) -> dict:
    ids = scenario.get("docs")
    if not isinstance(ids, list) or not ids or any(not isinstance(d, str) or d not in load_all() for d in ids):
        raise ValueError("묶음에 등록된 서류를 하나 이상 넣으세요")
    extra = scenario.get("extra") or {}
    if not isinstance(extra, dict):
        raise ValueError("프로필 값은 JSON 객체여야 합니다")
    conf = P.validate(scenario.get("processing"), ids)
    sid = scenario.get("id") or "draft"
    labels = {did: render(did, seed=seed, extra={**extra, "scenario": sid, "form_bank": "하나은행"}) for did in ids}
    docs = {did: {**label, "name": label["doc_name"], "images": label["images"],
                  "raw_keys": label.get("raw_keys", [f["key"] for f in label["fields"]]),
                  "visible": set(label.get("visible", [f["key"] for f in label["fields"] if f.get("bbox")]))} for did, label in labels.items()}
    customer = make_profile(seed).person.name
    task_name = scenario.get("name") or sid
    def qa(task, dids, prompt, answer, evaluation, suffix, first_page=False):
        images = [im for did in dict.fromkeys(dids) for im in (docs[did]["images"][:1] if first_page else docs[did]["images"])]
        item = {"id": f"{task}/{sid}_{seed}/{suffix}", "task": task, "images": images,
                "prompt": prompt, "answer": answer, "eval": evaluation,
                "meta": {"scenario": sid, "customer": customer, "preview": "original"}}
        return {**item, "image_urls": ["/preview/" + p.replace("\\", "/") for p in images], "model_answer": oracle_output(item)}
    rows = []
    rows.append({"id": "doc_check", "kind": "doc_check", "name": "필수 서류 구비 검사",
                 "status": "ready" if conf["doc_check"] else "disabled", "sources": [{"doc": did, "name": docs[did]["name"]} for did in ids],
                 "answer": {"missing": [], "not_required": [], "not_customer": []},
                 "question": "같은 고객으로 생성한 필수 서류 원본입니다. 실제 빌드에서는 레시피의 빠짐·타인·불필요 서류 비율을 적용합니다."})
    required = "\n".join(f"{i + 1}. {docs[did]['name']}" for i, did in enumerate(ids))
    if conf["doc_check"]:
        rows[0]["qa"] = [qa("doc_check", ids, P_DOC_CHECK.format(customer=customer, task=task_name, required=required),
                            rows[0]["answer"], {"required": [docs[did]["name"] for did in ids], "names": [docs[did]["name"] for did in ids]}, "original", first_page=True)]
    for result in P.execute(conf, docs):
        row = {k: v for k, v in result.items() if k != "item"}
        if (item := result.get("item")) is not None:
            n_pages = sum(len(docs[did]["images"]) for did in item["docs"])
            prompt = item.get("prompt") or P_REVIEW.format(task=task_name, pages=n_pages, question=item["question"])
            row["qa"] = [qa(item["task"], item["docs"], prompt, item["answer"], item["eval"], f"operation_{row['id']}")]
        rows.append(row)
    ctx = Ctx(docs, customer)
    for case in CASES:
        row = {"id": case.id, "kind": "case", "name": case.title, "question": case.basis, "sources": []}
        rows.append(row)
        if not conf["cross_check"] or not P.selected(conf, "case_ids", case.id):
            row.update(status="disabled", reason="꺼진 대조 사례")
            continue
        rng = random.Random(f"bench:case:{sid}_{seed}:{case.id}")
        if case.category != "format":
            rng.random()  # build가 변조 여부를 뽑는 순서
        try:
            original_rng_state = rng.getstate()
            plan = case.fn(ctx, case.category != "format", rng)
            if not plan:
                row.update(status="skipped", reason="현재 고객의 서류·값·정상 관계가 사례의 적용 조건을 만족하지 않습니다")
                continue
            if sum(len(docs[d]["images"]) for d in plan["docs"]) > 10:
                row.update(status="skipped", reason="대조 문항의 최대 10쪽을 넘습니다")
                continue
            refs = [(did, key) for did, changes in plan["edits"].items() for key in changes]
            row["sources"] = [P.source(did, ctx.f(did, key), docs) for did, key in refs if ctx.f(did, key)]
            linked = {x["doc"] for x in row["sources"]}
            row["sources"] += [{"doc": did, "name": docs[did]["name"]} for did in plan["docs"] if did not in linked]
            row.update(status="ready", answer="표기만 다른 정상 문항 후보" if case.category == "format" else "정상·변조 문항 생성 후보",
                       changes=[{"doc": did, "key": key, "old": ctx.val(did, key), "new": val}
                                for did, edits in plan["edits"].items() for key, val in edits.items()])
            n_pages = sum(len(docs[did]["images"]) for did in plan["docs"])
            row["qa"] = [qa("cross_check", plan["docs"], P_CROSS.format(customer=customer, task=task_name, n=len(plan["docs"]), pages=n_pages),
                            {"consistent": True, "issues": []}, {"documents": [docs[did]["name"] for did in plan["docs"]]}, case.id)]
            if conf["review"]:
                clean_rng = random.Random()
                clean_rng.setstate(original_rng_state)
                clean_plan = case.fn(ctx, False, clean_rng)
                if clean_plan and clean_plan.get("question"):
                    clean_pages = sum(len(docs[did]["images"]) for did in clean_plan["docs"])
                    question = clean_plan["question"] + " ('예' 또는 '아니오'로만 답하세요)"
                    row["qa"].append(qa("review", clean_plan["docs"], P_REVIEW.format(task=task_name, pages=clean_pages, question=question),
                                        "예" if clean_plan["yes"] else "아니오", {"answer_type": "yesno", "tol": 0}, f"case_{case.id}"))
        except (KeyError, TypeError, ValueError) as e:
            row.update(status="error", reason=f"사례 계산 오류: {e}")
    B = EvidenceBundle(sid, docs)
    rng = random.Random(f"bench:review:{sid}_{seed}")
    for rid, fn in {**RULES, "doc_valid": r_doc_valid}.items():
        row = {"id": rid, "kind": "rule", "name": P.RULE_TITLES[rid], "sources": []}
        rows.append(row)
        B.used = []
        try:
            q = fn(B, rng)
            if not conf["review"] or not P.selected(conf, "rule_ids", rid):
                row.update(status="disabled", reason="꺼진 심사 규칙")
            elif q:
                row.update(status="ready", answer=q["answer"], question=q["question"])
                n_pages = sum(len(docs[did]["images"]) for did in dict.fromkeys(q["docs"]))
                row["qa"] = [qa("review", q["docs"], P_REVIEW.format(task=task_name, pages=n_pages, question=q["question"]),
                                q["answer"], {"answer_type": q["answer_type"], "tol": q["tol"], **q.get("info", {})}, rid)]
                used = [(did, key) for did, key in B.used if did in q["docs"]]
                # 표 행을 직접 순회하는 계산도 실제로 더하거나 나눈 칸까지 연결한다.
                if rid == "invoice_sum":
                    used += [("commercial_invoice", key) for key, f in B.idx["commercial_invoice"].items()
                             if key.startswith("items.") and key.endswith(".amount") and isinstance(f.get("norm"), (int, float))]
                elif rid == "debt_ratio":
                    for key, f in B.idx["financial_statements"].items():
                        if key.startswith(("liabilities.", "equity.")) and key.endswith(".account") and str(f.get("value", "")).replace(" ", "") in ("부채총계", "자본총계"):
                            amount_key = key[:-len("account")] + "current"
                            if amount_key in B.idx["financial_statements"]:
                                used += [("financial_statements", key), ("financial_statements", amount_key)]
                row["sources"] = [P.source(did, B.f(did, key), docs) for did, key in dict.fromkeys(used)]
                linked = {x["doc"] for x in row["sources"]}
                row["sources"] += [{"doc": did, "name": docs[did]["name"]} for did in dict.fromkeys(q["docs"]) if did not in linked]
            else:
                row.update(status="skipped", reason="필요한 서류·숫자·날짜가 없어 계산할 수 없습니다")
        except (KeyError, TypeError, ValueError, ZeroDivisionError) as e:
            row.update(status="error", reason=f"규칙 계산 오류: {e}")
    return {"customer": customer, "seed": seed, "rows": rows, "labels": labels}
