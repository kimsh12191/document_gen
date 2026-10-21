"""키 사전 자동 초안 docgen/dictionary/*.json (studio/DESIGN.md 16절). 다시 돌려도 사람이 정한 것(by: 사람, 합치기 결정)은 남는다.

  python docgen/scripts/build_dictionary.py

- 재료: docgen/keys.json (키 목록·이름 두 벌), guide/fields/fields.json (서식별 키·항목명·체크 보기), docgen/key_rules.json,
  docgen/document_roles.json·registry (문서 분류), docgen/scenarios.json (업무).
- 필드 키 = 서류 속 역할.(세부.)속성. 역할 → 당사자는 아래 ROLE_PARTY 표(사람이 읽고 고친 첫 추정)로 정하고, 모르면 미정.
- 생성 코드는 이 파일들을 읽지 않는다(첫판). 쓰는 쪽 연결은 DESIGN 16.5 K3.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

OUT = ROOT / "docgen" / "dictionary"
STD = re.compile(r"[a-z][a-z0-9_]*(\.[a-z0-9_*]+)*")
HUMAN = "사람"

PARTIES = {
    "customer": {"name": "고객 본인", "desc": "업무를 신청한 개인 고객", "profile": "person"},
    "family": {"name": "배우자·가족", "desc": "고객의 배우자·자녀·부모·세대원", "profile": "spouse"},
    "agent": {"name": "대리인", "desc": "고객을 대신해 서류를 낸 사람", "profile": None},
    "related": {"name": "보증인·공동 당사자", "desc": "보증인·연대보증인·공동 차주·담보 제공자 등 업무에 함께 묶인 사람", "profile": None},
    "employer": {"name": "직장", "desc": "고객이 다니는 회사·근무 이력", "profile": "employment.company"},
    "corp": {"name": "법인·사업자", "desc": "고객이 법인·개인사업자일 때 그 사업체 (임원·주주 포함)", "profile": "corporation"},
    "counterparty": {"name": "거래 상대(국내)", "desc": "매도인·임대인·채권자·중개사 등 국내 상대방", "profile": None},
    "foreign": {"name": "외국 거래 상대", "desc": "수취인·수입상·선사·외국 학교 등", "profile": "foreign"},
    "bank": {"name": "은행·직원", "desc": "접수 은행·지점·담당 직원·은행 사용란", "profile": "bank"},
    "issuer": {"name": "발급기관", "desc": "증명서를 발급한 기관·공증인", "profile": None},
    "property": {"name": "물건", "desc": "부동산·차량·화물 등 대상물", "profile": "property"},
    "deal": {"name": "거래", "desc": "대출·계좌·송금·무역 조건·상품·거래 내역", "profile": None},
    "finance": {"name": "재무·세무 수치", "desc": "재무제표·소득·세액 등 수치 표", "profile": None},
    "document": {"name": "문서 자체", "desc": "발급일·문서번호·약관·동의·질문 등 서류의 머리·몸", "profile": None},
    "unassigned": {"name": "미정", "desc": "아직 당사자를 정하지 않은 역할", "profile": None},
}

# 서류 속 역할 → 당사자 (첫 추정). 값 끝의 ? 는 확신 낮음.
ROLE_PARTY = {
    "customer": "customer", "applicant": "customer", "self": "customer", "person": "customer", "debtor": "customer",
    "holder": "customer", "taxpayer": "customer", "employee": "customer", "borrower": "customer", "earner": "customer",
    "payer": "customer", "remitter": "customer", "naturalization": "customer", "name_history": "customer", "name_change": "customer",
    "addresses": "customer", "past_addresses": "customer", "current_address": "customer", "residences": "customer",
    "person_changes": "customer", "edd": "customer", "mrz": "customer", "owner": "customer?", "owners": "customer?",
    "household_head": "customer?", "signer": "customer?", "contact": "customer?",
    "spouse": "family", "family": "family", "households": "family", "dependents": "family", "cohabitants": "family",
    "members": "family", "marriage": "family", "student": "family?",
    "agent": "agent", "legal_rep": "agent", "delegate": "agent",
    "co_borrower": "related", "co_guarantors": "related", "guarantor": "related", "guarantors": "related", "grantor": "related",
    "mortgagor": "related?", "co_mortgagor": "related", "co_owners": "related", "co_buyer": "related", "tax_agent": "related",
    "signer2": "related?", "signer3": "related?", "signer4": "related?", "signer5": "related?", "signer6": "related?",
    "signer7": "related?", "signer8": "related?", "signers": "related?",
    "employer": "employer", "work": "employer", "workplace": "employer", "employment": "employer", "job": "employer",
    "work_prev": "employer", "careers": "employer", "work_sum": "employer", "office_history": "employer?",
    "company": "corp?", "corp": "corp", "shareholders": "corp", "officers": "corp", "capital_history": "corp",
    "capital_change": "corp", "company_name_change": "corp", "head_office_change": "corp", "purpose_history": "corp",
    "purpose_change": "corp", "agendas": "corp", "attendees": "corp", "rep": "corp", "branches": "corp",
    "seller": "counterparty", "buyer": "counterparty", "landlord": "counterparty", "co_landlord": "counterparty",
    "tenant": "counterparty", "counterparty": "counterparty", "creditor": "counterparty", "biller": "counterparty",
    "co_seller": "counterparty", "brokers": "counterparty", "landlord_agent": "counterparty", "seller_agent": "counterparty",
    "foreign": "foreign", "beneficiary": "foreign", "beneficiary_bank": "foreign", "consignee": "foreign", "shipper": "foreign",
    "importer": "foreign", "notify": "foreign", "manufacturer": "foreign?", "university": "foreign",
    "bank": "bank", "bank_use": "bank", "check": "bank?", "staff": "bank",
    "issuer": "issuer", "notary": "issuer", "providers": "issuer?", "registered": "document?",
    "property": "property", "land": "property", "house": "property", "buildings": "property", "unit": "property",
    "land_right": "property", "house_prices": "property", "land_prices": "property", "joint_collateral": "property",
    "containers": "property", "exclusive": "property", "gapgu": "property", "eulgu": "property", "past_events": "property?",
    "loan": "deal", "loans": "deal", "extra_loans": "deal", "other_loans": "deal", "items": "deal", "rows": "deal",
    "remittance": "deal", "payment": "deal", "payments": "deal", "payments_irregular": "deal", "product": "deal",
    "extra_products": "deal", "transaction": "deal", "txs": "deal", "first_tx": "deal", "debit": "deal", "debts": "deal",
    "installments": "deal", "charges": "deal", "price_breakdown": "deal", "credit_items": "deal", "lc": "deal",
    "terms": "deal", "gtc_terms": "deal", "refund_account": "deal", "fee_per_100": "deal", "cost": "deal", "deferrals": "deal",
    "kinds": "deal", "sub_kinds": "deal", "calc_methods": "deal", "fixed_date": "deal", "ebank": "deal", "scholarship": "deal",
    "bs_accounts": "finance", "pl_accounts": "finance", "balance_sheet": "finance", "income_statement": "finance",
    "assets": "finance", "liabilities": "finance", "equity": "finance", "appropriation": "finance", "manufacturing_cost": "finance",
    "total_liabilities_equity": "finance", "sum": "finance", "summary": "finance?", "total": "finance", "tax": "finance",
    "tax_prev": "finance", "nontax": "finance", "national": "finance", "deductions": "finance", "deduction_items": "finance",
    "penalty_items": "finance", "prepaid_items": "finance", "incomes": "finance", "business_income": "finance",
    "filing_rows": "finance", "allowances": "finance", "grades": "family?",
    "clauses": "document", "consent": "document", "marketing": "document", "questions": "document", "correction": "document",
    "amended": "document", "amendment": "document", "handwritten": "document", "common": "document", "batch": "document",
    "probation": "document?", "household_formed": "document?", "birth": "document?",
}
# 역할이 아니라 이름 묶음인 앞 이름 (공식 대조 html 69종의 official.*): 키마다 합치기 후보로 진짜 키를 찾는다
NAMESPACES = {"official"}
WHO = {"customer", "family", "agent", "related", "employer", "corp", "counterparty", "foreign", "bank", "issuer"}   # 사람·기관 당사자
# 역할 없는 키의 값 종류(realform.kind_of) → 당사자 (추정)
KIND_PARTY = {"branch": "bank", "bank": "bank", "amount": "deal", "fx_amount": "deal", "percent": "deal", "rate": "deal", "count": "deal",
              "currency": "deal", "product": "deal", "loan_subject": "deal", "repay": "deal", "check_kind": "deal", "check_no": "deal",
              "goods": "deal", "account": "deal", "reason": "deal", "date": "document", "number": "document", "note": "document",
              "skip": "document", "seal": "document", "person": "customer", "address": "customer", "phone": "customer",
              "email": "customer", "passport": "customer", "biz_no": "corp", "company": "counterparty", "country": "foreign"}
# 역할 없는 한 단어 키(속성만) → 당사자
SINGLE_PARTY = {"bank": "bank", "branch": "bank", "bank_name": "bank", "date": "document", "issue_date": "document",
                "doc_no": "document", "issue_no": "document", "purpose": "deal", "amount": "deal", "account": "deal"}
GROUP_OF_TASK = {"account_opening": "deposit", "efinance_signup": "deposit", "inheritance": "deposit",
                 "personal_credit_loan": "loan", "mortgage": "loan", "jeonse_loan": "loan", "sole_proprietor_loan": "loan",
                 "corporate_credit": "loan", "fx_remittance": "fx", "study_abroad_remittance": "fx",
                 "irp_opening": "pension", "retirement_payout": "pension"}
TASK_GROUPS = {"deposit": "수신·전자금융", "loan": "여신", "fx": "외환", "pension": "퇴직연금"}
TASK_ROLES = {   # 업무마다 다른 역할 → 당사자
    "mortgage": {"buyer": "customer", "seller": "counterparty", "owner": "customer", "owners": "customer"},
    "jeonse_loan": {"tenant": "customer", "landlord": "counterparty"},
    "fx_remittance": {"remitter": "customer", "beneficiary": "foreign", "buyer": "customer", "seller": "foreign",
                      "importer": "customer", "shipper": "foreign"},
    "study_abroad_remittance": {"remitter": "customer", "student": "family", "beneficiary": "foreign", "university": "foreign"},
    "inheritance": {"heir": "customer", "deceased": "family"},
    "corporate_credit": {"company": "corp", "borrower": "corp", "applicant": "corp"},
    "sole_proprietor_loan": {"company": "corp"},
}
TASK_ALIASES = {"mortgage": ["주담대", "주택담보"], "jeonse_loan": ["전세대출", "전세자금"], "personal_credit_loan": ["신용대출"],
                "fx_remittance": ["해외송금", "당발송금", "외화송금"], "study_abroad_remittance": ["유학송금"],
                "account_opening": ["계좌개설", "신규"], "irp_opening": ["IRP", "개인형퇴직연금"], "corporate_credit": ["기업여신"],
                "sole_proprietor_loan": ["사업자대출"], "retirement_payout": ["퇴직급여"], "efinance_signup": ["전자금융", "인터넷뱅킹"],
                "inheritance": ["상속"]}


def _load(name: str, default):
    p = OUT / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def _write(name: str, obj) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def split_key(key: str) -> tuple[str | None, list[str], str]:
    """필드 키 → (역할, 세부, 속성). seal.applicant → (applicant, [], seal) / rows.*.amount → (rows, ['*'], amount)."""
    key = re.sub(r"\[\]", ".*", key)   # owners[].name → owners.*.name (반복 행)
    parts = key.split(".")
    if parts[0] in ("seal", "sign") and len(parts) >= 2:
        return ".".join(parts[1:]) if parts[1] != "staff" else "staff", [], parts[0]
    if len(parts) == 1:
        return None, [], parts[0]
    return parts[0], parts[1:-1], parts[-1]


def party_of(role: str | None, attr: str) -> tuple[str, bool]:
    """(당사자, 확신) — 표에 없으면 미정."""
    p = ROLE_PARTY.get(role) if role else SINGLE_PARTY.get(attr)
    if p is None and role:
        base = re.sub(r"\d+$", "", role.removeprefix("co_"))   # signer3 → signer, co_xxx → xxx
        p = ROLE_PARTY.get(base) or ROLE_PARTY.get(base.rstrip("s"))
        p = (p.rstrip("?") + "?") if p else None
    if p is None:
        return "unassigned", False
    return p.rstrip("?"), not p.endswith("?")


SKIP_PARTIES = {"document", "deal", "finance", "unassigned", "bank", "issuer"}   # 대조 후보에서 뺄 당사자 (서류마다 다른 값)


def build_relations(fields: dict, types: dict, tasks: dict, roles: dict, merges: list) -> dict:
    """업무 → 문서 종류 → 당사자 키 (그리고 거꾸로). 업무 안에서 둘 이상의 문서 종류에 나오는 사람·기관 당사자 키 = 대조 후보."""
    accepted = {m["from"]: m["into"] for m in merges if m["dict"] == "field" and m["status"] == "accepted"}
    form_type = {f: tid for tid, t in types.items() for f in t["forms"]}

    def pkey(key, task=None):
        key = accepted.get(key, key)
        role, sub, attr = split_key(key)
        party = (tasks.get(task, {}).get("roles", {}).get(role) if task and role else None) \
            or (roles.get(role, {}).get("party") if role else SINGLE_PARTY.get(attr, "unassigned")) or "unassigned"
        mark = attr in ("seal", "sign")
        return ".".join(([attr] if mark else []) + [party] + sub + ([] if mark else [attr])), party

    doc_keys = defaultdict(set)
    for fid, f in fields.items():
        tid = form_type.get(fid)
        if tid:
            doc_keys[tid].update(k["key"] for k in f["keys"])
    out_docs = {tid: {"keys": len(ks), "party_keys": sorted({pkey(k)[0] for k in ks}), "tasks": []} for tid, ks in doc_keys.items()}
    out_tasks, by_pk = {}, defaultdict(lambda: {"doc_types": set(), "tasks": set()})
    for sid, t in tasks.items():
        dts = list(dict.fromkeys(form_type[d] for d in t["docs"] if d in form_type))
        where = defaultdict(set)
        for tid in dts:
            out_docs.setdefault(tid, {"keys": 0, "party_keys": [], "tasks": []})["tasks"].append(sid)
            for k in doc_keys.get(tid, ()):
                pk, party = pkey(k, sid)
                if party not in SKIP_PARTIES and "*" not in pk:
                    where[pk].add(tid)
        shared = sorted(({"party_key": pk, "doc_types": sorted(ds)} for pk, ds in where.items() if len(ds) >= 2),
                        key=lambda x: (-len(x["doc_types"]), x["party_key"]))
        out_tasks[sid] = {"doc_types": dts, "shared": shared}
    for tid, d in out_docs.items():
        for pk in d["party_keys"]:
            by_pk[pk]["doc_types"].add(tid)
            by_pk[pk]["tasks"].update(d["tasks"])
    party_keys = {pk: {"doc_types": len(v["doc_types"]), "tasks": sorted(v["tasks"])} for pk, v in sorted(by_pk.items())}
    return {"doc_types": out_docs, "tasks": out_tasks, "party_keys": party_keys}


def build() -> dict:
    keys = json.loads((ROOT / "docgen" / "keys.json").read_text(encoding="utf-8"))
    fields = json.loads((ROOT / "guide" / "fields" / "fields.json").read_text(encoding="utf-8"))
    rules = json.loads((ROOT / "docgen" / "key_rules.json").read_text(encoding="utf-8"))
    from docgen import realform as RF
    from docgen.registry import GROUPS, SCENARIOS, load_all

    reg = load_all()

    # --- 필드 키 → 역할·속성 ---------------------------------------------------
    role_forms, role_keys, attr_types, attr_labels, attr_keys = Counter(), defaultdict(set), defaultdict(Counter), defaultdict(Counter), defaultdict(set)
    nonstd = []
    for k in keys["keys"]:
        if not STD.fullmatch(k["key"]):
            nonstd.append(k)
            continue
        role, _, attr = split_key(k["key"])
        if role:
            role_forms[role] += k["forms"]
            role_keys[role].add(k["key"])
        attr_types[attr][k["type"]] += k["forms"]
        attr_labels[attr].update({lab: 1 for lab in k.get("labels", [])[:5]})
        attr_keys[attr].add(k["key"])

    old_roles = _load("roles.json", {"roles": {}})["roles"]
    roles = {}
    for role in sorted(role_forms, key=lambda r: (-role_forms[r], r)):
        prev = old_roles.get(role, {})
        if prev.get("by") == HUMAN:
            roles[role] = prev
            continue
        party, sure = party_of(role, "")
        if role in NAMESPACES:
            party, sure = "unassigned", False
        roles[role] = {"party": party, "sure": sure, "by": "자동", "forms": role_forms[role], "keys": len(role_keys[role]),
                       **({"namespace": True} if role in NAMESPACES else {}),
                       **{k: prev[k] for k in ("name", "by_doc_type", "by_task") if prev.get(k)}}

    old_attrs = _load("attributes.json", {"attributes": {}})["attributes"]
    syn = rules["synonyms"]
    attrs = {}
    for a in sorted(attr_keys):
        prev = old_attrs.get(a, {})
        if prev.get("by") == HUMAN:
            attrs[a] = prev
            continue
        kind = attr_types[a].most_common(1)[0][0]
        attrs[a] = {"name": (attr_labels[a].most_common(1) or [("", 0)])[0][0], "kind": kind, "by": "자동",
                    "keys": len(attr_keys[a]), "aliases": sorted(x for x, y in syn.items() if y == a), **({"merged_into": syn[a]} if a in syn else {})}

    # --- 문서 분류 ---------------------------------------------------------------
    old_docs = _load("doc_types.json", {"types": {}})["types"]
    droles = json.loads((ROOT / "docgen" / "document_roles.json").read_text(encoding="utf-8"))["roles"]
    in_role = {f for r in droles for f in r["forms"]}
    types = {}
    for r in droles:
        forms = [f for f in r["forms"] if f in reg]
        if forms:
            types[r["id"]] = {"name": r["name"], "group": reg[forms[0]].group, "forms": forms,
                              "aliases": sorted({reg[f].name for f in forms} - {r["name"]}), "by": "자동"}
    for fid, spec in reg.items():
        if fid not in in_role:
            types[fid] = {"name": spec.name, "group": spec.group, "forms": [fid], "aliases": [], "by": "자동"}
    for tid, prev in old_docs.items():
        if prev.get("by") == HUMAN:
            types[tid] = prev
    doc_types = {"groups": dict(GROUPS), "types": dict(sorted(types.items(), key=lambda x: (x[1]["group"], x[1]["name"])))}

    # --- 업무 ----------------------------------------------------------------------
    old_tasks = _load("tasks.json", {"tasks": {}})["tasks"]
    tasks = {}
    for sid, (name, docs) in SCENARIOS.items():
        prev = old_tasks.get(sid, {})
        if prev.get("by") == HUMAN:
            tasks[sid] = prev
            continue
        tasks[sid] = {"name": name, "group": GROUP_OF_TASK.get(sid, "deposit"), "aliases": TASK_ALIASES.get(sid, []),
                      "docs": docs, "roles": TASK_ROLES.get(sid, {}), "by": "자동"}

    # --- 체크 보기 ---------------------------------------------------------------
    options: dict[str, dict] = {}
    for fid, f in fields.items():
        for k in f["keys"]:
            if k.get("options"):
                role, _, attr = split_key(k["key"]) if STD.fullmatch(k["key"]) else (None, [], k["key"])
                o = options.setdefault(attr, {"options": Counter(), "keys": set(), "forms": set()})
                o["options"].update(k["options"])
                o["keys"].add(k["key"])
                o["forms"].add(fid)
    options = {a: {"options": [x for x, _ in o["options"].most_common()], "keys": sorted(o["keys"])[:20], "forms": len(o["forms"])}
               for a, o in sorted(options.items(), key=lambda x: -len(x[1]["forms"]))}

    # --- 합치기 후보 ---------------------------------------------------------------
    old_m = {(m["dict"], m["from"], m["into"]): m for m in _load("merges.json", {"items": []})["items"]}
    cand = []

    def add(dict_, frm, into, reason):
        if frm != into:
            cand.append({"dict": dict_, "from": frm, "into": into, "reason": reason, "status": "proposed", "applied": False})

    for a in attrs:   # 속성 이름 꼴: x_no ↔ x, x_name ↔ x (같은 값으로 보이는 것)
        for suf in ("_no", "_number", "_num"):
            base = a[: -len(suf)]
            if a.endswith(suf) and base in attrs and attrs[a]["kind"] == attrs[base]["kind"] != "text":   # passbook_no ≠ passbook
                add("attribute", a, base, f"끝말 {suf} 만 다르고 값 종류가 같음")
    for r in roles:   # 역할 단수·복수
        if r.endswith("s") and r[:-1] in roles:
            add("role", r, r[:-1], "단수·복수")
    last = None   # "위와 같다": 바로 위 제안의 방향(역할)을 따른다
    for d in keys.get("duplicates", []):   # 방향: 결정에 든 키, 없으면 제안 글에 먼저 나오는 키로
        text = d.get("decision") or d.get("proposal") or ""
        pos = {k: min([i for i in (text.find(k), text.find(k.split(".")[-1]) if d.get("decision") else -1,
                                   text.find(k.split(".")[0] + ".")) if i >= 0] or [10 ** 6]) for k in d["keys"]}
        if all(v == 10 ** 6 for v in pos.values()) and last:
            pos = {k: 0 if k.split(".")[0] == last else 1 for k in d["keys"]}
        into = min(d["keys"], key=lambda k: pos[k])
        last = into.split(".")[0]
        for frm in d["keys"]:
            if frm != into:
                cand.append({"dict": "field", "from": frm, "into": into, "reason": f"이름 두 벌: {d['meaning']}",
                             "status": "accepted" if d.get("decision") else "proposed", "applied": False, "note": d.get("proposal")})
    person_roles = {r for r in set(roles) | set(ROLE_PARTY) if party_of(r, "")[0] in WHO}
    for a in attrs:   # 속성에 사람·기관 역할이 섞인 것: x.holder_phone → x.holder.phone, bank.bank_name → bank.name
        m = re.fullmatch(r"([a-z]+(?:_[a-z]+)?)_([a-z]+)", a)
        if m and m.group(1) in person_roles and m.group(2) in attrs and m.group(2) != "no":   # corp_no·employee_no 는 번호 속성 그대로
            r, b = m.groups()
            for key in sorted(attr_keys[a])[:10]:
                up = key.split(".")[:-1]
                into = ".".join(up + [b] if up and up[-1] == r else up + [r, b])
                add("field", key, into, f"속성에 역할({r})이 섞임")
    alias = {re.sub(r"[^a-z0-9]", "", a.lower()): k for k, v in rules["keys"].items() for a in [k, *v.get("aliases", [])]}
    by_label = defaultdict(Counter)   # 항목명 → 그 항목명을 쓰는 영어 표준 키
    for k in keys["keys"]:
        if STD.fullmatch(k["key"]) and k["key"].split(".")[0] not in NAMESPACES:
            for lab in k.get("labels", []):
                by_label[RF.norm(lab).lower()][k["key"]] += k["forms"]
    for k in keys["keys"]:   # 이름공간(official.*): 역할이 속성 자리에 있거나(official.debtor), 같은 항목명의 표준 키로
        ns, _, attr = k["key"].partition(".")
        if ns not in NAMESPACES or not attr:
            continue
        base = attr.removesuffix("_copy")
        if base != attr:
            add("field", k["key"], f"{ns}.{base}", "보관본·사본의 같은 값 (_copy)")
            continue
        if base in ROLE_PARTY and party_of(base, "")[0] in WHO:
            add("field", k["key"], f"{base}.name", "역할 이름이 속성 자리에 (official.debtor → debtor.name)")
            continue
        same = Counter()
        for lab in k.get("labels", []):
            same.update(by_label.get(RF.norm(lab).lower(), {}))
        if same:
            add("field", k["key"], same.most_common(1)[0][0], f"이름공간 {ns}: 같은 항목명을 쓰는 표준 키")
    for k in nonstd:   # 영어 표준꼴이 아닌 키 (주로 하나은행 영문 서식의 항목명 그대로)
        into = next((RF.key_of(lab) for lab in [k["key"], *k.get("labels", [])] if RF.key_of(lab)), None) \
            or alias.get(re.sub(r"[^a-z0-9]", "", k["key"].lower()))
        if into:
            add("field", k["key"], into, "항목명·이름이 표준 키 규칙·동의어에 맞음")
            continue
        same = Counter()
        for lab in [k["key"], *k.get("labels", [])]:
            same.update(by_label.get(RF.norm(lab).lower(), {}))
        if same:
            add("field", k["key"], same.most_common(1)[0][0], "같은 항목명을 쓰는 표준 키")
            continue
        snake = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|[^A-Za-z0-9]+", "_", k["key"]).strip("_").lower()
        if re.fullmatch(r"[a-z][a-z0-9_]{2,}", snake) and not snake.isdigit():
            add("field", k["key"], snake, "영어 표준꼴로 (뜻 확인 필요)")
    for c in cand:
        prev = old_m.get((c["dict"], c["from"], c["into"]))
        if prev and prev["status"] != "proposed":
            c.update(status=prev["status"], applied=prev.get("applied", False))
    seen = set()
    merges = [c for c in cand if not ((c["dict"], c["from"], c["into"]) in seen or seen.add((c["dict"], c["from"], c["into"])))]

    relations = build_relations(fields, doc_types["types"], tasks, roles, merges)
    stats = {"roles": len(roles), "roles_unassigned": sum(1 for r in roles.values() if r["party"] == "unassigned"),
             "roles_unsure": sum(1 for r in roles.values() if not r.get("sure", True)), "attributes": len(attrs),
             "nonstd_keys": len(nonstd), "doc_types": len(types), "tasks": len(tasks), "options": len(options), "merges": len(merges),
             "key_forms_assigned": round(sum(r["forms"] for r in roles.values() if r["party"] != "unassigned") /
                                         max(1, sum(r["forms"] for r in roles.values())), 4)}
    about = "키 사전 (studio/DESIGN.md 16절). docgen/scripts/build_dictionary.py 가 자동 초안을 만들고 studio 키 사전 화면이 고친다. by: 사람 인 것은 다시 만들어도 남는다."
    _write("parties.json", {"about": about, "parties": PARTIES})
    prev_roles = _load("roles.json", {})
    human = set(prev_roles.get("single_human", []))
    single, unsure = dict(SINGLE_PARTY), []
    for fid, f in fields.items():   # 역할 없이 속성만 있는 키: 항목명 규칙의 값 종류로 당사자를 추정 (확신 낮음)
        for k in f["keys"]:
            role, _, attr = split_key(k["key"])
            if role is not None or attr in single:
                continue
            base = re.sub(r"\d+$", "", attr) or attr
            if base in single:
                single[attr] = single[base]
                continue
            std = RF.key_of(k.get("label") or attr) or RF.key_of(attr)
            if std:
                single[attr] = party_of(std.split(".")[0] if "." in std else None, std)[0]
            else:
                single[attr] = KIND_PARTY.get(RF.kind_of(k.get("label") or attr, None, None), "unassigned")
            unsure.append(attr)
    for a in human:   # 사람이 정한 것 유지
        if a in prev_roles.get("single", {}):
            single[a] = prev_roles["single"][a]
    _write("roles.json", {"about": about + " single 은 역할 없이 속성만 있는 키(bank, date, 취급점 …)의 당사자, single_unsure 는 추정한 것,"
                                           " single_human 은 사람이 정한 것.", "roles": roles, "single": single,
                          "single_unsure": sorted(set(unsure) - human), "single_human": sorted(human)})
    _write("attributes.json", {"about": about, "attributes": attrs})
    _write("doc_types.json", {"about": about, **doc_types})
    _write("tasks.json", {"about": about, "groups": TASK_GROUPS, "tasks": tasks})
    _write("options.json", {"about": about, "options": options})
    _write("merges.json", {"about": about, "items": merges})
    _write("relations.json", {"about": about + " relations 는 매번 새로 만든다(사람이 고치지 않음).", **relations})
    stats["cross_check_candidates"] = sum(len(t["shared"]) for t in relations["tasks"].values())
    _write("stats.json", stats)
    return stats


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=1))
