"""④ 서류 넣기 ❸ 건·업무 정하기 (studio/DESIGN.md 15.5): 사용자가 고른 기준(폴더 · 파일 이름 앞부분 · 추출 키)으로 건·업무를 묶고,
기준 값이 없는 서류는 고객 식별값으로 붙인다(자동). 업무는 기준이 없으면 건의 서류 조합을 기존 시나리오와 비교해 정한다.

  bases(묶음)            기준 후보와 각각의 미리보기 (덮는 서류 비율·건 수)
  infer(묶음, 기준)      건·업무를 정해 batch.json 의 "cases"(건마다 서류·업무·확실 여부·근거)와 "case_guess"(서류 → 건·업무)에 쓴다
                         case_guess 는 원본 데이터 나누기(intake_raw.case_of)와 시나리오 변경안(intake_plan)이 쓴다
  edit(묶음, ops)        사람이 서류 옮기기·건 합치기·업무 정하기·확인
  score(묶음, truth)     시험 폴더 정답으로 건 묶기(쌍 정밀도·재현율, 통째로 맞은 건)·업무 정확도

기준 {"case": {"kind": "folder" | "filename" | "key" | "auto", "key": 추출 키}, "task": {"kind": "folder" | "key" | "auto", "key": …}}
자동 묶기 (고객 식별값, 추출 결과의 고객 칸 + OCR 글자: 주민번호·휴대전화, 다른 서류에서 안 이름, 항목명(성명 …) 옆 이름):
  확실   주민번호 13자리·휴대전화·고객 계좌번호·법인 사업자번호가 같거나 (같은 번호는 생년월일 충돌을 보지 않음), 주민번호 앞 7자리(생년월일·성별)와 이름이 함께 같거나,
         이름 둘(법인명과 대표자, 고객과 가족)이 함께 같음
  확인 필요  이름만 또는 주민번호 앞 7자리만 같은 건이 하나뿐일 때 붙임. 근거가 없으면 서류 하나가 건 하나
  두 건의 고객 주민번호 앞 7자리가 두 글자 이상 다르면 합치지 않는다 (A–B, B–C 로 다른 고객이 이어지는 것을 막음). 기준으로 묶인 건끼리는 합치지 않는다.

  python -m studio.intake_cases <묶음 폴더> [--case folder|filename|key:<키>|auto] [--task folder|key:<키>|auto] [--truth truth.json]
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from . import importer as IM

TASK_MATCH = 0.5      # 서류 조합이 기존 시나리오와 이만큼(F1) 이상 겹치면 그 업무
NEW_TASK_SAME = 0.5   # 시나리오에 안 맞는 건끼리 이만큼(Jaccard) 이상 겹치면 같은 새 업무 후보
NAME_MERGE_MAX = 3    # 이름만 같은 건을 합치는 것은 그 이름이 이 수 이하의 건에만 나올 때
CASE_KEY = "document.case_no"
TASK_KEY = "document.task"

RRN = re.compile(r"(?<!\d)(\d{2}[01]\d[0-3]\d)\s*-\s*([1-8])([\d*●xX]{6})(?![\d*●])")
MOBILE = re.compile(r"(?<!\d)(01[016789])\s*-?\s*(\d{3,4})\s*-?\s*(\d{4})(?!\d)")


def _load(bdir: Path):
    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    rows = {r["id"]: r for r in IM._jsonl(bdir / "pages.jsonl")}
    fx = json.loads((bdir / "formats.json").read_text(encoding="utf-8"))
    return batch, rows, fx


def _digits(v) -> str:
    return re.sub(r"\D", "", str(v or ""))


def _norm_val(v) -> str:
    return re.sub(r"\s+", "", str(v or "")).strip()


def doc_forms(fx: dict) -> dict[str, dict]:
    """서류 → {format, form(등록된 서식 ID 또는 None), role(역할 ID, 새 서식은 new:<모양>)}. ❷ 결정을 따른다."""
    from docgen.registry import load_all
    from docgen.roles import index

    reg, roles = load_all(), index()
    out = {}
    for f in fx["formats"]:
        d = f.get("intake") or {}
        form = d.get("form_id") if d.get("form_id") in reg else None
        role = roles[form]["id"] if form in roles else (None if d.get("kind") == "skip" or not d else f"new:{f['id']}")
        for doc in f["docs"]:
            out[doc] = {"format": f["id"], "form": form, "role": role, "name": d.get("name") or f["name"]}
    return out


def _pred_items(batch: dict, doc: str) -> list[dict]:
    from .intake_judge import _pred

    return _pred(batch, doc)


# ---------------------------------------------------------------------------
# 기준 후보
# ---------------------------------------------------------------------------

def _prefix(doc: str) -> str | None:
    stem = doc.rsplit("/", 1)[-1]
    parts = re.split(r"[_\s]+", stem)
    return parts[0] if len(parts) > 1 and parts[0] else None


def _key_values(batch: dict, docs: list[str]) -> dict[str, dict[str, str]]:
    """추출 키 → {서류: 값}."""
    out: dict[str, dict[str, str]] = defaultdict(dict)
    for d in docs:
        for it in _pred_items(batch, d):
            v = _norm_val(it.get("value"))
            if v and it.get("type") not in ("seal", "signature", "checkbox"):
                out[it["key"]].setdefault(d, v)
    return out


def bases(bdir: Path) -> dict:
    """건·업무 기준 후보. 건: 폴더(있으면) · 파일 이름 앞부분(있으면) · 추출 키(서류 30% 이상에 있고 값이 겹치는 것) · 자동.
    업무: 폴더 · 추출 키(값 종류 20개 이하) · 자동. 키 사전에서 건 번호(document.case_no)·업무구분(document.task)에 이은 키는 맨 앞."""
    from docgen import dictionary as DIC

    batch, _, fx = _load(bdir)
    info = batch.get("intake", {}).get("docs", {})
    docs = list(info)
    n = len(docs) or 1
    forms = doc_forms(fx)
    case, task = [], []
    with_case = [d for d in docs if info[d].get("case")]
    if with_case:
        case.append({"kind": "folder", "coverage": round(len(with_case) / n, 3),
                     "groups": len({(info[d].get("scenario"), info[d]["case"]) for d in with_case})})
    pre = {d: _prefix(d) for d in docs}
    cnt = Counter(p for p in pre.values() if p)
    shared = [d for d in docs if pre[d] and cnt[pre[d]] >= 2]
    if len({pre[d] for d in shared}) >= 2:
        case.append({"kind": "filename", "coverage": round(len(shared) / n, 3), "groups": len({pre[d] for d in shared}),
                     "example": shared[0].rsplit("/", 1)[-1]})
    with_task = [d for d in docs if info[d].get("scenario")]
    if with_task:
        task.append({"kind": "folder", "coverage": round(len(with_task) / n, 3), "groups": len({info[d]["scenario"] for d in with_task})})
    for k, vals in _key_values(batch, docs).items():
        cover = len(vals) / n
        distinct = len(set(vals.values()))
        dt = next((DIC.doc_type_of(forms[d]["form"]) for d in vals if forms.get(d, {}).get("form")), None)
        ck = DIC.match_extracted(k, dt)
        row = {"kind": "key", "key": k, "coverage": round(cover, 3), "groups": distinct, "linked": ck in (CASE_KEY, TASK_KEY) and ck}
        if ck == CASE_KEY or (cover >= 0.3 and 2 <= distinct <= 0.8 * len(vals)):
            case.append(row)
        if ck == TASK_KEY or (cover >= 0.3 and 2 <= distinct <= 20 and distinct <= 0.5 * len(vals)):
            task.append(row)
    rank = lambda r, ck: (r["kind"] != "folder", r.get("linked") != ck, r["kind"] != "filename", -r["coverage"])  # noqa: E731
    case = sorted(case, key=lambda r: rank(r, CASE_KEY))[:12] + [{"kind": "auto"}]
    task = sorted(task, key=lambda r: rank(r, TASK_KEY))[:12] + [{"kind": "auto"}]
    default = {"case": next((r for r in case if r["kind"] in ("folder", "filename") or r.get("linked") == CASE_KEY), case[-1]),
               "task": next((r for r in task if r["kind"] == "folder" or r.get("linked") == TASK_KEY), task[-1])}
    return {"case": case, "task": task, "default": {k: {x: v[x] for x in ("kind", "key") if x in v} for k, v in default.items()},
            "saved": (batch.get("cases") or {}).get("basis")}


def _basis_value(batch: dict, basis: dict, kv: dict, doc: str) -> str | None:
    info = batch.get("intake", {}).get("docs", {}).get(doc, {})
    k = basis.get("kind")
    if k == "folder":
        return info.get("case") and f"{info.get('scenario') or '-'}/{info['case']}"
    if k == "filename":
        return _prefix(doc)
    if k == "key":
        return kv.get(basis.get("key"), {}).get(doc)
    return None


# ---------------------------------------------------------------------------
# 고객 식별값
# ---------------------------------------------------------------------------

def identities(batch: dict, rows: dict, fx: dict) -> dict[str, dict[str, set]]:
    """서류 → {name, rrn7, rrn13, mobile, acct, biz, cust7}. cust7 은 추출 결과 고객 칸의 주민번호 앞 7자리 (충돌 검사용).
    추출 결과의 고객·법인 칸에서 먼저, OCR 글자에서 주민번호·휴대전화와 (다른 서류에서 안) 고객 이름을 더 찾는다."""
    from docgen import dictionary as DIC

    from .intake_raw import KeyMapper

    forms = doc_forms(fx)
    o = IM._ocr_settings(batch)
    A = DIC.load("attributes").get("attributes", {})
    ids: dict[str, dict[str, set]] = {}
    mappers: dict = {}
    for f in fx["formats"]:
        keymap = (f.get("intake") or {}).get("keymap") or {}
        for doc, pids in f["docs"].items():
            t = ids[doc] = defaultdict(set)
            form = forms[doc]["form"]
            dt = DIC.doc_type_of(form) if form else None
            if form and form not in mappers:
                mappers[form] = KeyMapper(form, keymap)
            for it in _pred_items(batch, doc):
                if it.get("type") in ("seal", "signature", "checkbox") or not it.get("value"):
                    continue
                fk = mappers[form](it["key"]) if form else it["key"]
                r = DIC.resolve(fk, dt) if form else None
                if not r or r["party"] not in ("customer", "corp"):
                    ck = DIC.match_extracted(it["key"], dt)
                    if not ck:
                        continue
                    r = DIC.resolve(ck)
                    if r["party"] not in ("customer", "corp"):
                        continue
                attr, kind, v = r["attribute"], (A.get(r["attribute"]) or {}).get("kind"), str(it["value"])
                if r["party"] == "corp":
                    if kind == "biz_no" and len(_digits(v)) == 10:
                        t["biz"].add(_digits(v))
                    continue
                if attr in ("name", "name_en") and 2 <= len(_norm_val(v)) <= 30:
                    t["name"].add(_norm_val(v).upper())
                elif kind == "rrn" and (m := RRN.search(v)):
                    t["rrn7"].add(f"{m.group(1)}-{m.group(2)}")
                    t["cust7"].add(f"{m.group(1)}-{m.group(2)}")
                    if m.group(3).isdigit():
                        t["rrn13"].add(m.group(1) + m.group(2) + m.group(3))
                elif kind == "phone" and (m := MOBILE.search(v)):
                    t["mobile"].add("".join(m.groups()))
                elif kind == "account_no" and len(_digits(v)) >= 8:
                    t["acct"].add(_digits(v))
            words = [IM.page_words(rows[p], o["mapping"]) for p in pids if p in rows]
            t["_text"] = {"".join(w["text"] for w in ws) for ws in words}
            t["_label_names"] = {n for ws in words for n in label_names(ws)}
    names = {n for t in ids.values() for n in t["name"] if len(n) >= 2}
    for t in ids.values():
        text = "".join(t.pop("_text"))
        for m in RRN.finditer(text):
            t["rrn7"].add(f"{m.group(1)}-{m.group(2)}")
            if m.group(3).isdigit():
                t["rrn13"].add(m.group(1) + m.group(2) + m.group(3))
        for m in MOBILE.finditer(text):
            t["mobile"].add("".join(m.groups()))
        flat = re.sub(r"\s+", "", text).upper()
        t["name"] |= {n for n in names if n in flat} | t.pop("_label_names", set())
    return ids


NAME_LABEL = re.compile(r"^(?:성명|이름|고객명|예금주)\s*[:：]?\s*(?P<v>[가-힣]{3})?$")
SURNAMES = set("김이박최정강조윤장임한오서신권황안송류전홍고문양손배백허유남심노하곽성차주우구민진나지엄채원천방공현함변염여추도소석선설마길연위표기반왕금옥육인맹제모탁국어은편용예봉경사부")
HANGUL_NAME = re.compile(r"^[가-힣]{3}$")


def label_names(words: list[dict]) -> set[str]:
    """OCR 에서 항목명(성명·이름·고객명·예금주) 바로 오른쪽(같은 줄)의 한글 3자이고 흔한 성으로 시작하는 것 = 이름 (추출 결과가 없는
    서류도 이름으로 잇게). 안내문 낱말(확인·실명 …)이 이름으로 잡혀 다른 건끼리 이어지지 않게 좁게 잡는다."""
    out = set()
    for i, w in enumerate(words):
        m = NAME_LABEL.match(re.sub(r"\s+", "", w["text"]))
        if not m:
            continue
        if m.group("v"):
            if m.group("v")[0] in SURNAMES:
                out.add(m.group("v"))
            continue
        x0, y0, x1, y1 = w["bbox"]
        h = max(1.0, y1 - y0)
        right = [o for o in words if o is not w and o["bbox"][0] >= x1 - 2 and abs((o["bbox"][1] + o["bbox"][3]) / 2 - (y0 + y1) / 2) < 0.6 * h
                 and o["bbox"][0] - x1 < 12 * h]
        if right:
            v = re.sub(r"\s+", "", min(right, key=lambda o: o["bbox"][0])["text"])
            if HANGUL_NAME.match(v) and v[0] in SURNAMES and not NAME_LABEL.match(v):
                out.add(v)
    return out


# ---------------------------------------------------------------------------
# 건 묶기
# ---------------------------------------------------------------------------

def _near(a: str, b: str) -> bool:
    """주민번호 앞 7자리가 같거나 한 글자만 다름 (추출 오류 한 글자는 같은 사람으로 본다)."""
    return len(a) == len(b) and sum(x != y for x, y in zip(a, b)) <= 1


class _Groups:
    def __init__(self, docs, cust7):
        self.p = {d: d for d in docs}
        self.cust7 = {d: set(cust7.get(d, ())) for d in docs}
        self.basis = {d: False for d in docs}
        self.why: dict[str, set] = defaultdict(set)

    def find(self, d):
        while self.p[d] != d:
            self.p[d] = self.p[self.p[d]]
            d = self.p[d]
        return d

    def union(self, a, b, why, force=False, conflict=True) -> bool:
        """force: 기준으로 묶기(무조건). conflict=False: 같은 번호(주민번호 13자리·휴대전화·계좌·사업자번호)라 생년월일 충돌을 보지 않음
        (미성년 자녀 계좌처럼 서류의 '고객'이 다른 사람이어도 같은 건)."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return True
        if not force:
            if self.basis[ra] and self.basis[rb]:
                return False
            if conflict and self.cust7[ra] and self.cust7[rb] and not any(_near(a, b) for a in self.cust7[ra] for b in self.cust7[rb]):
                return False
        self.p[rb] = ra
        self.cust7[ra] |= self.cust7.pop(rb)
        self.basis[ra] = self.basis[ra] or self.basis.pop(rb)
        self.why[ra] |= self.why.pop(rb, set()) | {why}
        return True


def group_cases(docs: list[str], ids: dict, hard: dict[str, str | None]) -> dict[str, dict]:
    """서류 → {case, sure, why}. hard = 기준 값(같은 값이면 무조건 한 건)."""
    g = _Groups(docs, {d: ids[d]["cust7"] for d in docs})
    by_val = defaultdict(list)
    for d in docs:
        if hard.get(d):
            by_val[hard[d]].append(d)
    for v, ds in by_val.items():
        for d in ds:
            g.basis[d] = True
        for d in ds[1:]:
            g.union(ds[0], d, "기준", force=True)
    index = defaultdict(list)
    for d in docs:
        t = ids[d]
        for kind in ("rrn13", "mobile", "acct", "biz"):
            for v in t[kind]:
                index[(kind, v)].append(d)
        for r7 in t["rrn7"]:
            for n in t["name"]:
                index[("rrn7+name", r7, n)].append(d)
        names = sorted(t["name"])
        for i, a in enumerate(names):   # 이름 둘이 함께 (법인명·대표자, 고객·가족)
            for b in names[i + 1:]:
                index[("name2", a, b)].append(d)
    label = {"rrn13": "주민번호", "mobile": "휴대전화", "acct": "계좌번호", "biz": "사업자번호", "rrn7+name": "생년월일·이름",
             "name2": "이름 둘"}
    sure = {d: bool(hard.get(d)) for d in docs}
    exact = ("rrn13", "mobile", "acct", "biz")
    for key, ds in sorted(index.items(), key=lambda kv: kv[0][0] not in exact):
        for d in ds[1:]:
            if g.union(ds[0], d, label[key[0]], conflict=key[0] not in exact):
                sure[ds[0]] = sure[d] = True
    # 확인 필요: 확실한 근거가 없는 서류를 이름·생년월일(앞 7자리)이 같은 서류와 묶는다. 그 값이 확실한 건 둘 이상에 있으면(동명이인) 붙이지 않는다
    weak = set()
    toks = defaultdict(set)
    for d in docs:
        for kind in ("name", "rrn7"):
            for v in ids[d][kind]:
                toks[(kind, v)].add(d)
    for _, ds in sorted(toks.items(), key=lambda kv: len(kv[1])):
        roots = {g.find(x) for x in ds if sure[x]}
        loose = sorted(x for x in ds if not sure[x])
        if len(roots) > 1 or not loose:
            continue
        anchor = next(iter(roots)) if roots else loose[0]
        for x in loose:
            if x != anchor and g.union(anchor, x, "이름·생년월일만"):
                weak |= {x} | ({anchor} if not sure[anchor] else set())
    # 이름이 건 2~3개에만 나오고 그중 고객 생년월일이 있는 건이 하나 이하면 합친다 (생년월일 없는 쪽 서류는 확인 필요).
    # 동명이인은 둘 다 생년월일이 있어 막히고, 흔한 이름(건 4개 이상)은 합치지 않는다
    for (kind, v), ds in sorted(toks.items(), key=lambda kv: len(kv[1])):
        if kind != "name":
            continue
        roots = sorted({g.find(x) for x in ds})
        if 2 <= len(roots) <= NAME_MERGE_MAX and sum(bool(g.cust7[r]) for r in roots) <= 1:
            a, *rest = sorted(roots, key=lambda r: not g.cust7[r])
            for b in rest:
                moved = [x for x in docs if g.find(x) == g.find(b)]
                if g.union(a, b, "이름만 (다른 건)"):
                    weak |= set(moved)
    roots = {}
    out = {}
    for d in docs:
        r = g.find(d)
        cid = roots.setdefault(r, f"건{len(roots) + 1:03d}")
        why = sorted(g.why.get(r, set()))
        out[d] = {"case": cid, "sure": sure[d] and d not in weak, "why": why if sure[d] else (["이름·생년월일만"] if d in weak else ["근거 없음"])}
    return out


# ---------------------------------------------------------------------------
# 업무
# ---------------------------------------------------------------------------

def scenario_roles() -> dict[str, set]:
    from docgen.registry import SCENARIOS
    from docgen.roles import index

    roles = index()
    return {sc: {roles[d]["id"] for d in docs if d in roles} for sc, (_, docs) in SCENARIOS.items()}


def _task_name(v: str) -> str | None:
    from docgen import dictionary as DIC
    from docgen.registry import SCENARIOS

    if v in SCENARIOS:
        return v
    t = DIC.task_of(v)
    if t in SCENARIOS:
        return t
    return next((k for k, (name, _) in SCENARIOS.items() if _norm_val(name) == _norm_val(v)), None)


def assign_tasks(cases: dict[str, list[str]], forms: dict, basis_vals: dict[str, str | None]) -> dict[str, dict]:
    """건 → {scenario | None, new | None, score, by}. 기준 값이 있으면 그 값(시나리오 ID·이름·업무 사전으로 찾고, 없으면 새 업무 이름),
    없으면 서류 조합이 가장 많이 겹치는 시나리오. 어디에도 안 맞는 건은 조합이 비슷한 것끼리 새 업무 후보 A, B …"""
    sroles = scenario_roles()
    out, left = {}, []
    for cid, docs in cases.items():
        vals = Counter(basis_vals[d] for d in docs if basis_vals.get(d))
        if vals:
            v = vals.most_common(1)[0][0]
            sc = _task_name(v)
            out[cid] = {"scenario": sc, "new": None if sc else v, "score": None, "by": "기준"}
            continue
        R = {forms[d]["role"] for d in docs if forms.get(d, {}).get("role")}
        best, score = None, 0.0
        for sc, S in sroles.items():
            inter = len(R & S)
            f1 = 2 * inter / (len(R) + len(S)) if R and S else 0.0
            if f1 > score:
                best, score = sc, f1
        if best and score >= TASK_MATCH:
            out[cid] = {"scenario": best, "new": None, "score": round(score, 3), "by": "서류 조합"}
        else:
            left.append((cid, R))
    groups: list[tuple[set, list[str]]] = []
    for cid, R in left:
        for G, members in groups:
            if R and len(R & G) / len(R | G) >= NEW_TASK_SAME:
                G |= R
                members.append(cid)
                break
        else:
            groups.append((set(R), [cid]))
    for i, (_, members) in enumerate(groups):
        for cid in members:
            out[cid] = {"scenario": None, "new": f"새 업무 후보 {chr(65 + i) if i < 26 else i + 1}", "score": None, "by": "서류 조합"}
    return out


def infer(bdir: Path, basis: dict | None = None) -> dict:
    """건·업무를 정해 batch.json 에 쓴다. basis 를 안 주면 bases() 의 기본값."""
    batch, rows, fx = _load(bdir)
    basis = basis or (batch.get("cases") or {}).get("basis") or bases(bdir)["default"]
    docs = list(batch.get("intake", {}).get("docs", {}))
    kv = _key_values(batch, docs) if "key" in (basis["case"].get("kind"), basis["task"].get("kind")) else {}
    hard = {d: _basis_value(batch, basis["case"], kv, d) for d in docs}
    ids = identities(batch, rows, fx)
    for d in docs:
        ids.setdefault(d, defaultdict(set))
    got = group_cases(docs, ids, hard)
    cases: dict[str, list[str]] = defaultdict(list)
    for d, g in got.items():
        cases[g["case"]].append(d)
    forms = doc_forms(fx)
    tvals = {d: _basis_value(batch, basis["task"], kv, d) for d in docs}
    if basis["task"].get("kind") == "folder":
        tvals = {d: batch["intake"]["docs"][d].get("scenario") for d in docs}
    tasks = assign_tasks(cases, forms, tvals)
    names = defaultdict(set)   # 같은 이름이 나오는 다른 건 (동명이인일 수 있어 합치지 않고 '합칠 후보'로만)
    for c, ds in cases.items():
        for d in ds:
            for n in ids[d]["name"]:
                names[n].add(c)
    batch["cases"] = {"basis": basis, "cases": {c: {"docs": ds, "sure": all(got[d]["sure"] for d in ds),
                                                    "why": sorted({w for d in ds for w in got[d]["why"]}), **tasks[c],
                                                    "same_name": sorted({o for d in ds for n in ids[d]["name"] for o in names[n]} - {c})}
                                                for c, ds in cases.items()},
                      "unsure_docs": sum(1 for g in got.values() if not g["sure"])}
    batch["case_guess"] = {d: {"case": g["case"], "scenario": tasks[g["case"]]["scenario"] or tasks[g["case"]]["new"], "sure": g["sure"]}
                           for d, g in got.items()}
    IM._write_json(bdir / "batch.json", batch)
    if basis["case"].get("kind") == "key" or basis["task"].get("kind") == "key":
        remember_keys(basis)
    return summary(batch)


def edit(bdir: Path, ops: dict) -> dict:
    """사람이 고치기: {"move": {서류: 건}, "merge": [[건, 건, …]], "task": {건: 시나리오 ID 또는 새 업무 이름}, "confirm": [건, …]}.
    옮기거나 합친 건·업무를 정한 건·확인한 건은 확실(근거 '사람')이 된다. 새 건 이름으로 옮기면 그 건을 만든다."""
    from docgen.registry import SCENARIOS

    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    cs = batch["cases"]["cases"]
    touched = set()

    def take(doc):
        for c in cs.values():
            if doc in c["docs"]:
                c["docs"].remove(doc)
                return

    for doc, cid in (ops.get("move") or {}).items():
        if doc not in batch.get("case_guess", {}):
            raise KeyError(doc)
        take(doc)
        cs.setdefault(cid, {"docs": [], "sure": True, "why": [], "scenario": None, "new": "새 업무", "score": None, "by": "사람",
                            "same_name": []})["docs"].append(doc)
        touched.add(cid)
    for group in ops.get("merge") or []:
        if any(c not in cs for c in group):
            raise KeyError(group)
        a = group[0]
        for b in group[1:]:
            cs[a]["docs"] += cs.pop(b)["docs"]
        touched.add(a)
    for cid, t in (ops.get("task") or {}).items():
        if cid not in cs:
            raise KeyError(cid)
        sc = t if t in SCENARIOS else _task_name(t)
        cs[cid].update(scenario=sc, new=None if sc else t, by="사람", score=None)
        touched.add(cid)
    touched |= set(ops.get("confirm") or [])
    for cid in list(cs):
        if not cs[cid]["docs"]:
            del cs[cid]
    for cid in touched & set(cs):
        cs[cid].update(sure=True, why=sorted(set(cs[cid]["why"]) | {"사람"}))
    batch["case_guess"] = {d: {"case": cid, "scenario": c["scenario"] or c["new"], "sure": c["sure"] or bool(batch["case_guess"].get(d, {}).get("sure"))}
                           for cid, c in cs.items() for d in c["docs"]}
    for cid in touched & set(cs):
        for d in cs[cid]["docs"]:
            batch["case_guess"][d]["sure"] = True
    batch["cases"]["unsure_docs"] = sum(1 for g in batch["case_guess"].values() if not g["sure"])
    IM._write_json(bdir / "batch.json", batch)
    return summary(batch)


def summary(batch: dict) -> dict:
    c = (batch.get("cases") or {}).get("cases", {})
    per_task = Counter(x["scenario"] or x["new"] for x in c.values())
    return {"basis": batch["cases"]["basis"], "cases": len(c), "sure": sum(1 for x in c.values() if x["sure"]),
            "unsure_docs": batch["cases"]["unsure_docs"], "single": sum(1 for x in c.values() if len(x["docs"]) == 1),
            "tasks": dict(per_task.most_common())}


def remember_keys(basis: dict) -> None:
    """고른 추출 키를 키 사전의 건 번호·업무구분 공통 키의 다른 이름으로 남긴다 (다음 묶음에서 기준이 먼저 골라짐)."""
    from docgen import dictionary as DIC

    common = DIC.load("common")
    changed = False
    for side, ck, name in (("case", CASE_KEY, "건 번호(접수번호)"), ("task", TASK_KEY, "업무구분")):
        b = basis.get(side) or {}
        if b.get("kind") != "key" or not b.get("key"):
            continue
        e = common.setdefault("keys", {}).setdefault(ck, {"name": name, "kind": "text", "docs": 0, "by": "사람"})
        if b["key"] not in e.setdefault("aliases", []):
            e["aliases"].append(b["key"])
            changed = True
    if changed:
        DIC.save("common", common)


# ---------------------------------------------------------------------------
# 채점
# ---------------------------------------------------------------------------

def score(bdir: Path, truth_path: Path) -> dict:
    """건 묶기: 같은 건 서류 쌍의 정밀도·재현율, 통째로 맞은 건 비율, '확실'인데 틀린 서류 수. 업무: 서류마다 정한 업무가 정답 업무와 같은 비율.
    정답에 건이 없는 서류(업무 밖 외부 문서)는 뺀다. without_external = 건에 끼워 넣은 외부 문서(고객 값이 없어 묶을 수 없음)까지 뺀 것."""
    truth = json.loads(truth_path.read_text(encoding="utf-8"))["documents"]
    by = {**truth, **{v["flat"]: v for v in truth.values()}}
    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    guess = batch["case_guess"]
    return {**_score(guess, by, lambda d: True), "without_external": _score(guess, by, lambda d: not by[d].get("external"))}


def _score(guess: dict, by: dict, keep) -> dict:
    from itertools import combinations

    docs = [d for d in guess if d in by and by[d].get("case") and keep(d)]
    tcase = {d: (by[d]["scenario"], by[d]["case"]) for d in docs}
    gcase = {d: guess[d]["case"] for d in docs}
    tp = fp = fn = 0
    for a, b in combinations(docs, 2):
        same_t, same_g = tcase[a] == tcase[b], gcase[a] == gcase[b]
        tp += same_t and same_g
        fp += same_g and not same_t
        fn += same_t and not same_g
    tsets = defaultdict(set)
    gsets = defaultdict(set)
    for d in docs:
        tsets[tcase[d]].add(d)
        gsets[gcase[d]].add(d)
    exact = sum(1 for s in tsets.values() if s in gsets.values())
    major = {g: Counter(tcase[d] for d in s).most_common(1)[0][0] for g, s in gsets.items()}
    sure_wrong = [d for d in docs if guess[d]["sure"] and major[gcase[d]] != tcase[d]]
    task_ok = sum(1 for d in docs if guess[d]["scenario"] == by[d]["scenario"])
    P = tp / (tp + fp) if tp + fp else 1.0
    R = tp / (tp + fn) if tp + fn else 1.0
    return {"documents": len(docs), "true_cases": len(tsets), "guessed_cases": len(gsets), "pair_precision": round(P, 4),
            "pair_recall": round(R, 4), "exact_cases": round(exact / len(tsets), 4) if tsets else None,
            "sure_wrong": len(sure_wrong), "unsure": sum(1 for d in docs if not guess[d]["sure"]),
            "task_acc": round(task_ok / len(docs), 4) if docs else None, "sure_wrong_docs": sure_wrong[:10]}


def _parse_basis(s: str) -> dict:
    return {"kind": "key", "key": s[4:]} if s.startswith("key:") else {"kind": s}


def main(argv=None) -> None:
    import argparse

    ap = argparse.ArgumentParser(prog="python -m studio.intake_cases", description=__doc__.split("\n")[0])
    ap.add_argument("batch")
    ap.add_argument("--case")
    ap.add_argument("--task")
    ap.add_argument("--truth")
    a = ap.parse_args(argv)
    b = Path(a.batch)
    basis = None
    if a.case or a.task:
        d = bases(b)["default"]
        basis = {"case": _parse_basis(a.case) if a.case else d["case"], "task": _parse_basis(a.task) if a.task else d["task"]}
    print(json.dumps(infer(b, basis), ensure_ascii=False))
    if a.truth:
        print(json.dumps(score(b, Path(a.truth)), ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
