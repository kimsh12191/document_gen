"""cross_check·review 용 불일치 사례 목록.

업무 묶음(한 고객이 한 업무로 낸 서류)에서 실제 심사에서 걸리는 불일치를 일부러 만든다.
사례마다 '깨끗한 서류에서는 관계가 맞는다'를 먼저 확인하고(맞지 않으면 그 사례는 건너뜀),
변조 문항은 서류 한 건의 값만 바꿔 다시 렌더링한다. 같은 사례의 정상 문항(변조 없음)도 같은 비율로 만든다.

분류 (category)
  typo          오기: 성명·주민번호·연락처·주소·계좌·생년월일 한 자리
  amount        금액 불일치: 신청↔약정 금액, 원천징수↔소득금액증명 소득 (소득 부풀리기)
  other_person  타인 서류: 같은 종류 서류를 다른 사람 것으로 바꿔 냄 (명의도용·가족 서류 혼입)
  logic         업무 논리 오류: 임대인·매도인 ≠ 등기부 소유자, 재직기간 부풀리기, 법인 대표자 불일치,
                약정일 < 신청일, 채권최고액 < 대출금, 전세대출 > 보증금, 업계약(대금 합계 불일치),
                송금 수취인 ≠ 송장 수출자
  format        표기만 다름 (정상 문항): 날짜 형식, 금액 '원' 표기, 주민번호 가림, 전화번호 하이픈, 주소 참고항목

사례 함수: (Ctx, tamper: bool, rng) -> Plan | None
  Plan = {"docs": [보여 줄 서류ID],
          "edits": {서류ID: {키: 새 값}},       변조할 값 (같은 서류 안에서 같은 값이 다른 칸에도 있으면 함께 바꿈)
          "swap": 서류ID | None,                이 서류를 다른 고객 것으로 바꿈
          "issue": {"doc", "key", "alt": [서류ID]} | None,   변조 문항의 정답 위치 (alt: 함께 짚어도 되는 서류)
          "question": 예/아니오 질문 | None, "yes": 질문의 정답이 '예'인지}
"""
from __future__ import annotations

import random
import re
from dataclasses import dataclass
from datetime import date
from typing import Callable

from .. import korean as K
from . import perturb
from .metrics import norm_text


@dataclass
class Case:
    id: str
    title: str
    category: str
    basis: str
    fn: Callable


class Ctx:
    def __init__(self, docs: dict[str, dict], customer_name: str):
        self.docs = docs
        self.customer = customer_name
        self.idx = {d: {f["key"]: i for i, f in enumerate(v["fields"])} for d, v in docs.items()}

    def has(self, *docs) -> bool:
        return all(d in self.docs for d in docs)

    def f(self, doc: str, key: str) -> dict | None:
        i = self.idx.get(doc, {}).get(key)
        return None if i is None else self.docs[doc]["fields"][i]

    def visible(self, doc: str, key: str) -> bool:
        i = self.idx.get(doc, {}).get(key)
        d = self.docs.get(doc)
        return i is not None and d["raw_keys"][i] in d["visible"] and d["fields"][i].get("value") is not None

    def val(self, doc, key):
        f = self.f(doc, key)
        return f and f.get("value")

    def num(self, doc, key) -> float | None:
        f = self.f(doc, key)
        n = f and f.get("norm")
        return float(n) if isinstance(n, (int, float)) and not isinstance(n, bool) else None

    def date(self, doc, key) -> date | None:
        f = self.f(doc, key)
        if not f or f.get("type") != "date":
            return None
        try:
            return date.fromisoformat(f["norm"])
        except (TypeError, ValueError):
            return None

    def name(self, doc) -> str:
        return self.docs[doc]["name"]

    def label(self, doc, key) -> str:
        return (self.f(doc, key) or {}).get("label") or key


# ---------------------------------------------------------------------------
# 값 바꾸기 도우미
# ---------------------------------------------------------------------------

_KNUM = re.compile(r"(?<![가-힣])([일이삼사오육칠팔구십백천만억조]+)(?=원)")
_DNUM = re.compile(r"\d{1,3}(?:,\d{3})+|\d{4,}")


def amount_like(old: str, n: int) -> str | None:
    """금액 표시 형식은 그대로 두고 금액만 n 으로 바꾼다. '금 오억원정 (₩500,000,000)' 의 한글·숫자 모두."""
    out, hit = old, False
    if _KNUM.search(out):
        out, k = _KNUM.subn(K.won_korean(n), out)
        hit |= k > 0
    if _DNUM.search(out):
        out = _DNUM.sub(lambda m: f"{n:,}" if "," in m.group() else str(n), out)
        hit = True
    return out if hit and out != old else None


def other_name(rng: random.Random, avoid: str) -> str:
    for _ in range(20):
        n = K.make_name(rng, rng.choice("MF"))[0]
        if n != avoid and n[0] != avoid[:1]:
            return n
    return K.make_name(rng, "M")[0]


_DATE_RE = re.compile(r"\d{4}\s*[.\-/년]\s*\d{1,2}\s*[.\-/월]\s*\d{1,2}")


def shift_first_date(value: str, days: int) -> str | None:
    """'2020.08.19 ~ 현재' 같은 값의 첫 날짜만 옮긴다."""
    m = _DATE_RE.search(value)
    if not m:
        return None
    parts = [int(x) for x in re.findall(r"\d+", m.group())]
    try:
        iso = date(*parts).isoformat()
    except ValueError:
        return None
    new = perturb.shift_date(m.group(), iso, days)
    return new and value[:m.start()] + new + value[m.end():]


def _round(n: float, unit: int) -> int:
    return max(unit, int(round(n / unit)) * unit)


def _plan(docs, tamper, edits=None, issue=None, question=None, yes_when_clean=True, swap=None):
    return {"docs": docs, "edits": (edits or {}) if tamper else {}, "swap": swap if tamper else None,
            "issue": issue if tamper else None, "question": question,
            "yes": yes_when_clean != tamper}


# ---------------------------------------------------------------------------
# 사례
# ---------------------------------------------------------------------------

TYPO_KINDS = {"name", "rrn", "phone", "address", "account_no"}


def c_typo(ctx: Ctx, tamper, rng):
    from .build import field_kind

    ids = list(ctx.docs)
    groups = perturb.candidates([ctx.docs[d] for d in ids])
    groups = [g for g in groups if field_kind(ctx.docs[ids[g[0][0]]]["fields"][g[0][1]]) in TYPO_KINDS
              or "생년월일" in (ctx.docs[ids[g[0][0]]]["fields"][g[0][1]].get("label") or "")]
    if not groups:
        return None
    g = rng.choice(groups)
    di, fi = rng.choice(g)
    target, f = ids[di], ctx.docs[ids[di]]["fields"][fi]
    others = sorted({ids[d] for d, _ in g} - {target})
    shown = [target] + rng.sample(others, min(len(others), rng.randint(1, 2)))
    new = perturb.mutate(f, rng)
    if not new or norm_text(new) == norm_text(f["value"]):
        return None
    return _plan(shown, tamper, {target: {f["key"]: new}}, {"doc": target, "key": f["key"], "alt": []})


OTHER_OK = ["resident_registration_copy", "family_relation_certificate", "employment_certificate", "income_certificate",
            "withholding_receipt", "seal_certificate", "health_insurance_qualification", "pay_stub",
            "business_registration_certificate", "tax_payment_certificate", "local_tax_payment_certificate",
            "basic_certificate", "resident_id_card"]
APP_DOCS = ["loan_application", "account_opening_application", "overseas_remittance_application", "customer_due_diligence",
            "privacy_consent"]


def _name_key(ctx: Ctx, doc: str) -> str | None:
    for f in ctx.docs[doc]["fields"]:
        if f.get("value") == ctx.customer and f["type"] == "text" and ctx.visible(doc, f["key"]):
            return f["key"]
    return None


def c_other_person(ctx: Ctx, tamper, rng):
    cands = [d for d in OTHER_OK if d in ctx.docs and _name_key(ctx, d)]
    apps = [d for d in APP_DOCS + ["resident_id_card"] if d in ctx.docs and _name_key(ctx, d)]
    if not cands or not apps:
        return None
    doc = rng.choice(cands)
    app = next((a for a in apps if a != doc), None)
    if not app:
        return None
    key = _name_key(ctx, doc)
    q = f"'{ctx.name(doc)}'의 본인(명의자) 성명이 '{ctx.name(app)}'의 고객 성명과 같습니까?"
    return _plan([app, doc], tamper, issue={"doc": doc, "key": key, "alt": []}, question=q, swap=doc)


def c_loan_vs_agreement(ctx: Ctx, tamper, rng):
    for a, b in (("loan_application", "credit_agreement"), ("loan_application_corp", "credit_agreement_corp")):
        if ctx.has(a, b) and ctx.visible(a, "loan.amount") and ctx.visible(b, "loan.amount"):
            break
    else:
        return None
    na, nb = ctx.num(a, "loan.amount"), ctx.num(b, "loan.amount")
    if not na or na != nb:
        return None
    target = rng.choice([a, b])
    n2 = _round(na * rng.choice([0.8, 0.9, 1.1, 1.2, 1.5]), 1_000_000)
    edits = {target: {k: amount_like(ctx.val(target, k), n2) for k in ("loan.amount", "loan.amount_korean")
                      if ctx.visible(target, k)}}
    if not all(edits[target].values()):
        return None
    q = f"'{ctx.name(a)}'의 {ctx.label(a, 'loan.amount')}과 '{ctx.name(b)}'의 {ctx.label(b, 'loan.amount')}이 같습니까?"
    return _plan([a, b], tamper, edits, {"doc": target, "key": "loan.amount", "alt": [b if target == a else a]}, q)


def c_income_inflated(ctx: Ctx, tamper, rng):
    w, c = "withholding_receipt", "income_certificate"
    if not ctx.has(w, c) or not ctx.visible(w, "work.total"):
        return None
    year, total = ctx.val(w, "year"), ctx.num(w, "work.total")
    row = next((k[: -len(".year")] for k, i in ctx.idx[c].items()
                if re.fullmatch(r"rows\.\d+\.year", k) and ctx.val(c, k) == year), None)
    if not row or ctx.num(c, f"{row}.amount") != total:
        return None
    delta = _round(total * rng.uniform(0.2, 0.6), 10_000)
    edits = {w: {"work.total": amount_like(ctx.val(w, "work.total"), int(total + delta))}}
    sal = ctx.num(w, "work.salary")
    if sal and ctx.visible(w, "work.salary"):
        edits[w]["work.salary"] = amount_like(ctx.val(w, "work.salary"), int(sal + delta))
    if not all(edits[w].values()):
        return None
    q = (f"'{ctx.name(w)}'의 주(현)근무지 급여 합계(계)와 '{ctx.name(c)}'의 {year}년 소득금액(과세대상급여액)이 "
         "같습니까?")
    return _plan([w, c], tamper, edits, {"doc": w, "key": "work.total", "alt": [c]}, q)


def _registry_owner(ctx: Ctx, reg: str) -> tuple[str, list[str]] | None:
    """등기부의 현재 소유자 이름과, 그 이름이 찍힌 칸들의 키.
    갑구가 있으면 마지막 소유권 등기의 명의인, 요약본이면 '주요 등기사항 요약'의 등기명의인."""
    best = None
    for k in ctx.idx.get(reg, {}):
        m = re.fullmatch(r"gapgu\.(\d+)\.holder\.name", k)
        if m and "소유권" in (ctx.val(reg, f"gapgu.{m.group(1)}.purpose") or "") and ctx.visible(reg, k):
            if best is None or int(m.group(1)) > int(best.split(".")[1]):
                best = k
    if best:
        owner = ctx.val(reg, best)
    elif ctx.visible(reg, "summary.owners.0.name") and not ctx.visible(reg, "summary.owners.1.name"):
        owner = re.sub(r"\s*\(.*\)\s*$", "", ctx.val(reg, "summary.owners.0.name"))
    else:
        return None
    keys = [best] if best else []
    keys += [k for k in ctx.idx[reg] if re.fullmatch(r"summary\.(owners\.\d+\.name|rights\.\d+\.target_owner)", k)
             and ctx.visible(reg, k) and owner in ctx.val(reg, k)]
    return owner, keys


def _owner_case(ctx: Ctx, tamper, rng, contract: str, party_key: str, role: str):
    reg = "real_estate_registry"
    if not ctx.has(contract, reg) or not ctx.visible(contract, party_key):
        return None
    found = _registry_owner(ctx, reg)
    if not found or not found[1] or norm_text(found[0]) != norm_text(ctx.val(contract, party_key)):
        return None
    owner, keys = found
    new = other_name(rng, owner)
    q = f"'{ctx.name(contract)}'의 {role}이 '{ctx.name(reg)}'의 현재 소유자와 같은 사람입니까?"
    return _plan([contract, reg], tamper, {reg: {k: ctx.val(reg, k).replace(owner, new) for k in keys}},
                 {"doc": reg, "key": keys[0], "alt": [contract]}, q)


def c_lease_owner(ctx, tamper, rng):
    return _owner_case(ctx, tamper, rng, "lease_contract", "landlord_name", "임대인")


def c_seller_owner(ctx, tamper, rng):
    return _owner_case(ctx, tamper, rng, "sales_contract", "seller.name", "매도인")


def c_hire_date(ctx: Ctx, tamper, rng):
    e = "employment_certificate"
    if not ctx.has(e) or not ctx.visible(e, "employment.period"):
        return None
    m = _DATE_RE.search(ctx.val(e, "employment.period") or "")
    if not m:
        return None
    try:
        start = date(*[int(x) for x in re.findall(r"\d+", m.group())])
    except ValueError:
        return None
    comp = None
    if ctx.has("health_insurance_qualification"):
        rows = sorted((int(k.split(".")[1]), k) for k in ctx.idx["health_insurance_qualification"]
                      if re.fullmatch(r"rows\.\d+\.start", k))
        if rows and ctx.visible("health_insurance_qualification", rows[-1][1]):
            comp = ("health_insurance_qualification", rows[-1][1])
    if comp is None and ctx.has("loan_application") and ctx.visible("loan_application", "workplace.hire_date"):
        comp = ("loan_application", "workplace.hire_date")
    if comp is None or ctx.date(*comp) != start:
        return None
    new = shift_first_date(ctx.val(e, "employment.period"), -rng.randint(365, 1500))
    if not new:
        return None
    q = f"'{ctx.name(e)}'의 입사일(재직기간 시작일)과 '{ctx.name(comp[0])}'의 {ctx.label(*comp)}이 같습니까?"
    return _plan([e, comp[0]], tamper, {e: {"employment.period": new}},
                 {"doc": e, "key": "employment.period", "alt": [comp[0]]}, q)


def c_rep_director(ctx: Ctx, tamper, rng):
    s, a = "corporate_seal_certificate", "loan_application_corp"
    if not ctx.has(s, a) or not ctx.visible(s, "rep_name") or not ctx.visible(a, "company.ceo"):
        return None
    if norm_text(ctx.val(s, "rep_name")) != norm_text(ctx.val(a, "company.ceo")):
        return None
    new = other_name(rng, ctx.val(s, "rep_name"))
    q = f"'{ctx.name(s)}'의 대표자와 '{ctx.name(a)}'의 대표자가 같은 사람입니까?"
    return _plan([a, s], tamper, {s: {"rep_name": new}}, {"doc": s, "key": "rep_name", "alt": [a]}, q)


def c_contract_before_apply(ctx: Ctx, tamper, rng):
    for a, b in (("loan_application", "credit_agreement"), ("loan_application_corp", "credit_agreement_corp")):
        if ctx.has(a, b) and ctx.visible(b, "contract_date"):
            break
    else:
        return None
    da, db = ctx.date(a, "apply_date"), ctx.date(b, "contract_date")
    if not da or not db or db < da:
        return None
    f = ctx.f(b, "contract_date")
    new = perturb.shift_date(f["value"], f["norm"], (da - db).days - rng.randint(3, 40))
    if not new:
        return None
    q = f"'{ctx.name(b)}'의 약정일이 '{ctx.name(a)}'의 신청일과 같거나 그 이후입니까?"
    return _plan([a, b], tamper, {b: {"contract_date": new}}, {"doc": b, "key": "contract_date", "alt": [a]}, q)


def c_collateral_short(ctx: Ctx, tamper, rng):
    c, a = "collateral_agreement", "credit_agreement"
    if not ctx.has(c, a) or not ctx.visible(c, "max_amount"):
        return None
    mx, loan = ctx.num(c, "max_amount"), ctx.num(a, "loan.amount")
    if not mx or not loan or mx <= loan:
        return None
    n2 = _round(loan * rng.uniform(0.6, 0.95), 1_000_000)
    edits = {c: {k: amount_like(ctx.val(c, k), n2) for k in ("max_amount", "max_amount_korean") if ctx.visible(c, k)}}
    if not all(edits[c].values()):
        return None
    q = f"'{ctx.name(c)}'의 채권최고액이 '{ctx.name(a)}'의 대출(한도)금액보다 큽니까?"
    return _plan([a, c], tamper, edits, {"doc": c, "key": "max_amount", "alt": [a]}, q)


def c_jeonse_over(ctx: Ctx, tamper, rng):
    a, l = "loan_application", "lease_contract"
    if not ctx.has(a, l) or not ctx.visible(a, "loan.amount") or not ctx.visible(l, "deposit"):
        return None
    loan, dep = ctx.num(a, "loan.amount"), ctx.num(l, "deposit")
    if not loan or not dep or loan > dep:
        return None
    n2 = _round(dep * rng.uniform(1.05, 1.3), 10_000_000)
    edits = {a: {k: amount_like(ctx.val(a, k), n2) for k in ("loan.amount", "loan.amount_korean") if ctx.visible(a, k)}}
    if not all(edits[a].values()):
        return None
    q = f"'{ctx.name(a)}'의 대출신청금액이 '{ctx.name(l)}'의 보증금 이하입니까?"
    return _plan([a, l], tamper, edits, {"doc": a, "key": "loan.amount", "alt": [l]}, q)


def c_sales_sum(ctx: Ctx, tamper, rng):
    s = "sales_contract"
    if not ctx.has(s) or not ctx.visible(s, "payment.price"):
        return None
    price, down = ctx.num(s, "payment.price"), ctx.num(s, "payment.down")
    mid, bal = ctx.num(s, "payment.middle") or 0, ctx.num(s, "payment.balance")
    if not price or down is None or bal is None or abs(down + mid + bal - price) > 0.5:
        return None
    new = amount_like(ctx.val(s, "payment.price"), _round(price * rng.uniform(1.08, 1.25), 10_000_000))
    if not new:
        return None
    shown = [s] + (["loan_application"] if ctx.has("loan_application") else [])
    q = f"'{ctx.name(s)}'의 계약금·중도금·잔금을 모두 더한 금액이 매매대금과 같습니까?"
    return _plan(shown, tamper, {s: {"payment.price": new}}, {"doc": s, "key": "payment.price", "alt": []}, q)


FX_NAMES = ["Golden Harbor Trading Ltd.", "Pacific Rim Commerce Co.", "Eastwind Import Export LLC", "Sunrise Global Ltd."]


def c_fx_beneficiary(ctx: Ctx, tamper, rng):
    r, i = "overseas_remittance_application", "commercial_invoice"
    if not ctx.has(r, i) or not ctx.visible(r, "beneficiary.name") or not ctx.visible(i, "shipper.name"):
        return None
    if norm_text(ctx.val(r, "beneficiary.name")) != norm_text(ctx.val(i, "shipper.name")):
        return None
    new = rng.choice([n for n in FX_NAMES if n != ctx.val(r, "beneficiary.name")])
    q = f"'{ctx.name(r)}'의 수취인이 '{ctx.name(i)}'의 수출자(Shipper)와 같습니까?"
    return _plan([r, i], tamper, {r: {"beneficiary.name": new}}, {"doc": r, "key": "beneficiary.name", "alt": [i]}, q)


def equivalent(f: dict, rng) -> str | None:
    """같은 값을 다른 표기로: 날짜 형식, 금액 '원', 주민번호 뒷자리 가림, 전화번호 하이픈, 주소 참고항목."""
    from .build import field_kind

    v, kind = f["value"], field_kind(f)
    if kind == "date":
        try:
            d = date.fromisoformat(f["norm"])
        except (TypeError, ValueError):
            return None
        opts = [K.fmt_date(d, s) for s in ("dot", "dash", "kor_short")]
        opts = [o for o in opts if norm_text(o) != norm_text(v)]
        return rng.choice(opts) if opts else None
    if kind == "amount" and re.fullmatch(r"[\d,]+원?", v.strip()):
        return v.strip()[:-1] if v.strip().endswith("원") else v.strip() + "원"
    if kind == "rrn" and re.fullmatch(r"\d{6}-\d{7}", v.strip()):
        return K.mask_rrn(v.strip())
    if kind == "phone" and "-" in v:
        return v.replace("-", "")
    if kind == "address" and re.search(r"\s*\([^)]*\)\s*$", v):
        return re.sub(r"\s*\([^)]*\)\s*$", "", v)
    return None


def c_format_only(ctx: Ctx, tamper, rng):
    """정상 문항: 같은 값을 한 서류에서만 다른 표기로 쓴다. 불일치가 아니다."""
    ids = list(ctx.docs)
    groups = perturb.candidates([ctx.docs[d] for d in ids])
    rng.shuffle(groups)
    for g in groups:
        di, fi = rng.choice(g)
        f = ctx.docs[ids[di]]["fields"][fi]
        new = equivalent(f, rng)
        if not new:
            continue
        others = sorted({ids[d] for d, _ in g} - {ids[di]})
        shown = [ids[di]] + rng.sample(others, min(len(others), 2))
        return {"docs": shown, "edits": {ids[di]: {f["key"]: new}}, "swap": None, "issue": None, "question": None,
                "yes": True}
    return None


CASES = [
    Case("typo", "성명·번호·주소 오기", "typo", "신청서·약정서 기재 오류 (성명·주민번호·연락처·주소 한 자리)", c_typo),
    Case("other_person", "타인 명의 서류", "other_person", "명의도용·가족 서류 혼입, 대리 제출 시 타인 서류", c_other_person),
    Case("loan_vs_agreement", "신청금액 ≠ 약정금액", "amount", "신청서와 약정서 금액 상이 (약정서 작성 오류·변조)", c_loan_vs_agreement),
    Case("income_inflated", "소득 부풀리기", "amount", "작업대출: 원천징수영수증 위·변조로 소득 과다 기재", c_income_inflated),
    Case("lease_owner", "임대인 ≠ 등기부 소유자", "logic", "전세사기: 계약서상 임대인이 등기부 소유자가 아님", c_lease_owner),
    Case("seller_owner", "매도인 ≠ 등기부 소유자", "logic", "무권리자 매도·허위 매매계약", c_seller_owner),
    Case("hire_date", "재직기간 부풀리기", "logic", "작업대출: 재직증명서 입사일 ≠ 건강보험 자격취득일", c_hire_date),
    Case("rep_director", "법인 대표자 불일치", "logic", "대표이사 변경 미반영·권한 없는 자의 신청", c_rep_director),
    Case("contract_before_apply", "약정일 < 신청일", "logic", "서류 작성일 순서 오류 (사후 작성·소급 작성)", c_contract_before_apply),
    Case("collateral_short", "채권최고액 < 대출금", "logic", "근저당 설정 금액 부족", c_collateral_short),
    Case("jeonse_over", "전세대출 > 보증금", "logic", "허위 임대차계약·보증금 부풀리기", c_jeonse_over),
    Case("sales_sum", "업계약 (대금 합계 불일치)", "logic", "업계약: 대출 한도를 늘리려 매매대금을 부풀림", c_sales_sum),
    Case("fx_beneficiary", "송금 수취인 ≠ 송장 수출자", "logic", "증빙과 다른 상대방에게 송금 (외국환 증빙 불일치)", c_fx_beneficiary),
    Case("format_only", "표기만 다름 (정상)", "format", "날짜·금액·주민번호·전화·주소 표기 차이는 불일치가 아님", c_format_only),
]
