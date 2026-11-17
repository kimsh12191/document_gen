"""서식 전용 질문 qa.py (서식 폴더 docgen/forms/<ID>/qa.py): 이 서식에서만 묻는 질문과 정답. 쓰는 법은 docgen/forms/README.md.

    def 직위(v):                                   함수 하나 = 질문 하나 (함수 이름 = 질문 이름, _ 로 시작하면 도우미)
        return "직위만 답하세요.", v["employer.position"]

  v        이 문서에 그린 칸 값 {키: 값} — 질문 키(공통 키)와 서식의 원래 키 둘 다. 체크박스는 체크된 보기 글자
           (복수 선택은 목록), 도장·서명은 True/False. 빈 칸은 v 에 없다: v["키"] 로 읽으면 그 문서에서는 묻지 않는다
           (있는지 물으려면 v.get("키")).
  돌려주기 (질문, 정답). None 이면 이 문서에서는 묻지 않는다. 정답 꼴로 기본 채점이 정해진다:
           숫자 → number (숫자가 같은지) · True/False·"예"/"아니오" → yesno · 글 → text (띄어쓰기·문장부호 무시) ·
           dict/list → json (칸마다 같은지)
  채점을 다르게 하려면 train/scorers 의 채점 함수 (견본 train/scorers/form_qa_example.py) — 서식 폴더에는 두지 않는다.

데이터: docgen/bench/tasks/form_qa.py 가 문서마다 이 함수들을 불러 과제 form_qa 문항을 만든다 (평가 세트·학습 데이터 같이).
문항의 meta.question = "<서식ID>.<함수 이름>" (채점 함수·보고서에서 질문을 가를 때).
"""
from __future__ import annotations

import datetime as _dt
import importlib.util
import inspect
import re
import sys
from pathlib import Path

NAME = "qa.py"
KINDS = ("number", "yesno", "text", "json")
_cache: dict = {}


def path(doc_id: str) -> Path:
    from . import formdir

    return (formdir.folder(doc_id) or formdir.copy_dir(doc_id) or formdir.home(doc_id)) / NAME


def load(doc_id: str, p: Path | None = None):
    """이 서식의 qa.py 모듈 (없으면 None). 파일이 바뀌면 다시 읽는다."""
    p = p or path(doc_id)
    try:
        mt = p.stat().st_mtime_ns
    except OSError:
        return None
    hit = _cache.get(p)
    if hit and hit[0] == mt:
        return hit[1]
    name = "docgen.forms_qa." + re.sub(r"\W", "_", doc_id)
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(name, None)
        raise
    _cache[p] = (mt, mod)
    return mod


def questions(mod) -> list[tuple[str, callable]]:
    """qa.py 의 질문 함수들 (파일에 적은 차례). _ 로 시작하는 것과 다른 곳에서 가져온 것은 뺀다."""
    if mod is None:
        return []
    fns = [(n, f) for n, f in vars(mod).items()
           if inspect.isfunction(f) and not n.startswith("_") and f.__module__ == mod.__name__]
    return sorted(fns, key=lambda nf: nf[1].__code__.co_firstlineno)


def values(fields: list[dict]) -> dict:
    """그린 칸 목록 → v {키: 값}. 빈 칸은 뺀다."""
    from .bench.metrics import is_null

    v = {}
    for f in fields:
        if f["type"] in ("checkbox", "checkbox_multi"):
            on = [o["text"] for o in f.get("options") or [] if o.get("checked")]
            val = (on[0] if len(on) == 1 else on or None) if f["type"] == "checkbox" else on or None
        elif f["type"] in ("seal", "signature"):
            val = bool(f.get("present"))
        else:
            val = None if is_null(f.get("value")) else f["value"]
        if val is None:
            continue
        v.setdefault(f["key"], val)
    return v


def kind(answer) -> str:
    """정답 꼴 → 기본 채점 종류."""
    if isinstance(answer, bool) or answer in ("예", "아니오"):
        return "yesno"
    if isinstance(answer, (int, float)):
        return "number"
    if isinstance(answer, (dict, list)):
        return "json"
    return "text"


class QAError(ValueError):
    """qa.py 함수가 실패했을 때 (어느 서식·어느 질문인지와 함께)."""


def ask(doc_id: str, fields: list[dict], mod=None) -> list[dict]:
    """이 문서에 묻는 서식 전용 질문: [{"name", "prompt", "answer", "kind"}]. 칸이 없어서(KeyError) 못 묻는 질문은 뺀다."""
    mod = mod if mod is not None else load(doc_id)
    if mod is None:
        return []
    v = values(fields)
    out = []
    for name, fn in questions(mod):
        try:
            r = fn(dict(v))
        except KeyError:
            continue
        except Exception as e:
            raise QAError(f"{doc_id}/qa.py {name}(): {type(e).__name__}: {e}") from e
        if r is None:
            continue
        if not (isinstance(r, tuple) and len(r) == 2 and isinstance(r[0], str) and r[0].strip()):
            raise QAError(f"{doc_id}/qa.py {name}(): (질문 글, 정답) 두 개를 돌려줘야 합니다 — 받은 것: {r!r}"[:300])
        q, a = r
        if a is None:
            continue
        if isinstance(a, bool):
            a = "예" if a else "아니오"
        if isinstance(a, float) and a.is_integer():
            a = int(a)
        out.append({"name": name, "prompt": q, "answer": a, "kind": kind(a)})
    return out


# ---------------------------------------------------------------------------
# qa.py 에서 쓰는 도우미:  from docgen.formqa import number, date, months
# ---------------------------------------------------------------------------

def number(text) -> float | int | None:
    """'1,234원'·'금 이억원정'·'12.5%' → 숫자 (정수면 int). 못 읽으면 None."""
    from .bench.metrics import to_number

    n = to_number(text)
    return int(n) if n is not None and float(n).is_integer() else n


def date(text) -> _dt.date | None:
    """'2025-05-21'·'2025.5.21'·'2025년 5월 21일'·'20250521' → 날짜. 못 읽으면 None."""
    nums = re.findall(r"\d+", str(text or ""))
    if len(nums) == 1 and len(nums[0]) == 8:
        nums = [nums[0][:4], nums[0][4:6], nums[0][6:]]
    if len(nums) < 3:
        return None
    y, m, d = (int(x) for x in nums[:3])
    try:
        return _dt.date(y + 2000 if y < 100 else y, m, d)
    except ValueError:
        return None


def months(start, end) -> int | None:
    """두 날짜 사이 개월 수 (끝 날의 일이 시작 일보다 작으면 한 달 덜). 못 읽으면 None."""
    a, b = (x if isinstance(x, _dt.date) else date(x) for x in (start, end))
    if a is None or b is None:
        return None
    return (b.year - a.year) * 12 + b.month - a.month - (b.day < a.day)


# ---------------------------------------------------------------------------
# 검사·견본
# ---------------------------------------------------------------------------

def check_dir(d: Path) -> list[str]:
    """서식 폴더의 qa.py 를 읽을 수 있는지 (서식 다시 읽기). 없으면 []."""
    p = Path(d) / NAME
    if not p.exists():
        return []
    try:
        compile(p.read_text(encoding="utf-8"), str(p), "exec")
    except SyntaxError as e:
        return [f"{NAME} 문법 오류: {e.lineno}번째 줄 {e.msg}"]
    return []


def check(doc_id: str, docs: list[list[dict]]) -> dict:
    """qa.py 를 여러 seed 로 그린 문서에 돌려 본다: {"problems", "notes", "rows": [{"name", "asked", "of", "kind", "example"}]}.
    문제: 읽기·실행 오류, 한 번도 묻지 않는 질문(없는 키), 정답을 답으로 넣어도 만점이 아닌 질문."""
    from .bench.evaluate import s_form_qa
    from .bench.runner import oracle_output

    p = path(doc_id)
    if not p.exists():
        return {"problems": [], "notes": [], "rows": []}
    try:
        mod = load(doc_id)
    except Exception as e:  # noqa: BLE001  사람이 쓴 파일
        return {"problems": [f"qa.py 를 읽지 못함: {type(e).__name__}: {e}"], "notes": [], "rows": []}
    fns = questions(mod)
    if not fns:
        return {"problems": [], "notes": ["qa.py 에 질문 함수가 없습니다"], "rows": []}
    problems, rows = [], {n: {"name": n, "asked": 0, "of": len(docs), "kind": None, "example": None, "missing": set()}
                          for n, _ in fns}
    for fields in docs:
        v = values(fields)
        for n, fn in fns:
            try:
                fn(dict(v))
            except KeyError as e:
                rows[n]["missing"].add(str(e.args[0]) if e.args else "?")
            except Exception:  # noqa: BLE001, S110  아래 ask 가 오류를 알린다
                pass
        try:
            got = ask(doc_id, fields, mod)
        except QAError as e:
            problems.append(str(e))
            break
        for it in got:
            r = rows[it["name"]]
            r["asked"] += 1
            r["kind"] = r["kind"] or it["kind"]
            r["example"] = r["example"] or it
            item = {"task": "form_qa", "answer": it["answer"], "eval": {"answer_type": it["kind"]}}
            if s_form_qa(item, oracle_output(item))["metrics"]["acc"] < 1:
                problems.append(f"qa.py {it['name']}(): 정답을 답으로 넣어도 기본 채점이 맞다고 하지 않습니다 "
                                f"(정답 {it['answer']!r}) — 정답 꼴을 바꾸거나 train/scorers 의 채점 함수로")
    notes, failed = [], bool(problems)   # 실행 오류가 났으면 그 뒤 문서는 돌리지 않았으니 "안 물음" 은 따지지 않는다
    for r in rows.values():
        if not r["asked"] and not failed:
            miss = sorted(r["missing"] - {f["key"] for fs in docs for f in fs})
            problems.append(f"qa.py {r['name']}(): 그려 본 {len(docs)}개 문서에서 한 번도 묻지 않습니다"
                            + (f" — 칸에 없는 키 {miss}" if miss else " (칸이 늘 비었거나 None 을 돌려줌)"))
        elif r["asked"] < len(docs):
            notes.append(f"qa.py {r['name']}(): {len(docs)}개 문서 중 {r['asked']}개에서만 묻습니다 (칸이 빈 문서는 뺌)")
    return {"problems": sorted(set(problems), key=problems.index), "notes": notes,
            "rows": [{k: v for k, v in r.items() if k != "missing"} for r in rows.values()]}


SKELETON = '''"""{doc_id} ({name}) 서식 전용 질문. 쓰는 법: docgen/forms/README.md 의 "서식 전용 질문 qa.py".

함수 하나 = 질문 하나. v = 이 문서에 그린 칸 값 {{키: 값}} (키는 카드 FORM.md 의 키 열).
(질문, 정답)을 돌려주면 평가 세트·학습 데이터에 과제 form_qa 문항으로 들어간다. None 이면 이 문서에서는 묻지 않는다.
v["키"] 의 칸이 빈 문서에서는 그 질문을 묻지 않는다. 기본 채점은 정답 꼴로: 숫자·예/아니오·글·JSON.
"""
from docgen.formqa import date, months, number  # noqa: F401  도우미: 금액·날짜 글자 → 숫자·날짜, 개월 수

# 아래는 견본입니다. 주석(#)을 풀고 고쳐 쓰세요.
{examples}
'''


def skeleton(doc_id: str, docs: list[list[dict]]) -> str:
    """qa.py 견본: 이 서식에서 실제로 나오는 칸 키로 쓴 예시 함수 (주석으로)."""
    from .registry import load_all

    seen = {}   # 키 → 항목명 (값이 글자인 칸, 반복 행 빼고, 문서 순서)
    for fields in docs:
        for f in fields:
            k = f["key"]
            if (k not in seen and f["type"] not in ("checkbox", "checkbox_multi", "seal", "signature") and f.get("label")
                    and not any(p.isdigit() for p in k.split(".")) and k in values([f])):
                seen[k] = f["label"]
    keys = list(seen)[:2]
    ex = []
    if keys:
        k = keys[0]
        fn = re.sub(r"\W", "_", seen[k])
        ex += [f"# def {fn}(v):", f'#     return "{seen[k]}만 답하세요.", v["{k}"]', "#"]
    if len(keys) > 1:
        a, b = keys
        ex += ["# def 두_칸(v):   # 칸 여러 개를 엮은 답 (JSON)",
               (f'#     return \'{seen[a]}·{seen[b]}을 {{"{seen[a]}": …, "{seen[b]}": …}} 로 답하세요.\', '
                f'{{"{seen[a]}": v["{a}"], "{seen[b]}": v["{b}"]}}'), "#"]
    k = keys[0] if keys else "키"
    ex += ["# def 적혀_있나(v):   # 예/아니오 (True/False 를 돌려주면 예/아니오)",
           f'#     return "{seen.get(k, k)} 칸이 적혀 있습니까? 예/아니오로 답하세요.", v.get("{k}") is not None']
    return SKELETON.format(doc_id=doc_id, name=load_all()[doc_id].name, examples="\n".join(ex))
