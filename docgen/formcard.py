"""서식 카드 FORM.md: 서식 폴더만 보고 "이 서식은 무엇을, 어디서 뽑고, 어떻게 묻고, 답이 어떤 모양인지"를 알게 하는 읽는 문서.

자동 생성물이다 (직접 고치지 않는다). 고치는 곳은 카드의 "고치려면" 표에 있다.
  python -m docgen.formdir card <ID>… | --all [--stale] [--workers N]   만들기 (그림을 실제로 그려 위치를 잰다)
  python -m docgen.formdir card --all --check                          오래된 카드 (원본이 바뀐 뒤 안 다시 만든 것)

카드 머리의 card-hash 는 이 서식의 파일(서식 해시)·fields.json(질문 설정 q 포함)·questions.json·공통 기본 질문·키 규칙·키 사전의
해시다. 그중 하나라도 바뀌면 "오래됨".
엔진 코드(그리기·채점)가 바뀌는 것은 카드를 오래됨으로 만들지 않는다.
"""
from __future__ import annotations

import hashlib
import json
import re
import tempfile
from pathlib import Path

NAME = "FORM.md"
VERSION = "3"   # 카드 꼴이 바뀌면 올린다 (모든 카드가 오래됨)
ROOT = Path(__file__).resolve().parents[1]
SHARED = Path(__file__).resolve().parent / "forms" / "_common"
TASK_TITLE = {"classify": "서류 분류", "ocr_page": "전체 받아쓰기", "ocr_field": "값 칸 읽기", "kie": "정보 추출",
              "freetext": "기타 칸 정리", "marks": "체크·도장·서명", "form_qa": "서식 전용 질문"}
MAIN = {"classify": "acc", "ocr_page": "recall", "ocr_field": "exact", "kie": "vl_f1 (값+위치)", "freetext": "f1",
        "marks": "vl_f1 (값+위치)", "form_qa": "acc"}


def path(doc_id: str) -> Path:
    from . import formdir

    return (formdir.folder(doc_id) or formdir.copy_dir(doc_id) or formdir.home(doc_id)) / NAME


def _digest(paths) -> str:
    h = hashlib.sha1()
    for p in paths:
        h.update(str(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p).encode())
        h.update(p.read_bytes() if p.exists() else b"-")
    return h.hexdigest()


def card_hash(doc_id: str) -> str:
    from . import formfields
    from . import formquestions as FQ
    from .preview import source_hash

    shared = [SHARED / "questions.json", SHARED / "key_rules.json", *sorted((SHARED / "dictionary").glob("*.json"))]
    from . import formqa

    own = [FQ.path(doc_id), formfields.path(doc_id)] + ([formqa.path(doc_id)] if formqa.path(doc_id).exists() else [])
    return hashlib.sha1("|".join([VERSION, source_hash(doc_id, common=False), _digest(own),
                                  _digest(shared)]).encode()).hexdigest()[:12]


def stale(doc_id: str) -> bool:
    p = path(doc_id)
    if not p.exists():
        return True
    m = re.search(r"card-hash: (\w+)", p.read_text(encoding="utf-8")[:600])
    return not m or m.group(1) != card_hash(doc_id)


# ---------------------------------------------------------------------------
# 재료
# ---------------------------------------------------------------------------

def kind_of(doc_id: str) -> str:
    from .registry import load_all

    spec = load_all()[doc_id]
    if spec.template.startswith("@form/"):
        return "html"
    if spec.template == "_real_form.html.j2":
        return "image" if spec.group == "imported" else "overlay"
    return "code"


KIND_NAME = {"code": "코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)", "html": "html 서식 (값은 fields.json 의 값 출처, 모양은 템플릿)",
             "overlay": "원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)",
             "image": "가져온 그림 서식 (견본 그림 위에 칸을 얹음, 칸은 fields.json items)"}


def _rel(p: Path | None) -> str:
    if p is None:
        return "-"
    p = Path(p).resolve()
    return str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)


def _line_of(text: str | None, *needles: str, after: int = 0, nth: int = 1) -> int | None:
    """after 줄 뒤에서 needles 가 모두 들어 있는 nth 번째 줄 번호 (1부터)."""
    if not text:
        return None
    for n, line in enumerate(text.splitlines(), 1):
        if n > after and all(x in line for x in needles):
            nth -= 1
            if nth == 0:
                return n
    return None


def _where_defined(kind: str, key: str, label: str | None, tpl: str | None, fields_text: str | None,
                   gen_text: str | None, tpl_name: str, nth: int = 1) -> str:
    """이 칸이 정해지는 곳 (파일:줄). key 는 서식의 원래 키 (반복 행은 *)."""
    out = []
    if kind in ("code", "html"):
        last = key.rsplit(".", 1)[-1]
        if "*" in key:
            head = key.split(".*", 1)[0]
            n = (_line_of(tpl, f'"{head}.', f'".{last}"') or _line_of(tpl, f"'{head}.", f"'.{last}'")
                 or _line_of(tpl, f'".{last}"') or _line_of(tpl, f"'.{last}'"))
        else:
            n = _line_of(tpl, f'"{key}"') or _line_of(tpl, f"'{key}'")
        if n:
            out.append(f"{tpl_name}:{n}")
        if fields_text:
            f = _line_of(fields_text, f'"{key if "*" not in key else last}"')
            if f and kind == "html":
                out.append(f"fields.json:{f}")
    else:
        f = _line_of(fields_text, f'"label": {json.dumps(label, ensure_ascii=False)}', nth=nth) if label else None
        if f:
            out.append(f"fields.json:{f}")
    return " · ".join(out) or "-"


def _source_of(kind: str, key: str, declared: dict) -> str:
    """값 출처 (fields.json 의 source, 코드 서식은 generate.py)."""
    fields = declared.get("fields") or {}
    src = None
    if "*" in key:
        head, last = key.split(".*", 1)[0], key.rsplit(".", 1)[-1]
        src = (((declared.get("lists") or {}).get(head) or {}).get("fields") or {}).get(last, {}).get("source")
    else:
        src = (fields.get(key) or {}).get("source")
    if kind == "code":
        return "generate.py" if src in (None, "code") else f"`{src}` (fields.json 이 덮어씀)"
    if kind == "html":
        return f"`{src}`" if src else "-"
    return "원본 칸 (항목명 → 값 종류)"


def _pos(f: dict | None, sizes) -> str:
    if not f or not f.get("bbox"):
        return "-"
    from .bench.metrics import normalize_box

    pg = f.get("page", 0)
    if pg >= len(sizes):
        return "-"
    return f"{pg + 1}쪽 {normalize_box(f['bbox'], *sizes[pg])}"


def _scenarios(doc_id: str) -> list[str]:
    from .registry import SCENARIO_SAMPLING, SCENARIOS

    out = []
    for sid, (name, ids) in SCENARIOS.items():
        cands = {d for c in (SCENARIO_SAMPLING.get(sid) or {}).values() for d in c.get("forms", [])}
        if doc_id in ids or doc_id in cands:
            out.append(name)
    return out


# ---------------------------------------------------------------------------
# 카드
# ---------------------------------------------------------------------------

def render_card(doc_id: str, builder) -> str:
    """builder: docgen.bench.build.Builder (그림을 그려 위치를 잰다)."""
    from . import dictionary as DIC
    from . import formdir, formfields
    from . import formquestions as FQ
    from .bench import tasks as T
    from .bench.build import SPLITS
    from .entities import make_profile
    from .registry import load_all

    spec = load_all()[doc_id]
    kind = kind_of(doc_id)
    folder = path(doc_id).parent
    seed = SPLITS["test"][0]
    stem = f"images/{doc_id}_{seed}"
    r = builder.render_doc(doc_id, make_profile(seed), seed, stem, "clean")
    recs = T.make_single(r, stem, builder.out, 2, 40)
    docs = FQ.seen_fields(doc_id)
    view = FQ.resolved(doc_id, docs)
    fields = {f["key"]: f for f in DIC.apply(doc_id, r["fields"])}
    from . import fieldinfo

    info = fieldinfo.entries(doc_id)
    by_pattern = {}
    for f in fields.values():
        by_pattern.setdefault(FQ.pattern(f["key"]), f)

    tpl_path = formdir.template(doc_id) if kind in ("code", "html") else None
    tpl = tpl_path.read_text(encoding="utf-8") if tpl_path and tpl_path.exists() else None
    fp = formfields.path(doc_id)
    declared = formfields.read(doc_id) or {} if fp.exists() else {}
    gen = folder / "generate.py"
    gen_text = gen.read_text(encoding="utf-8") if gen.exists() else None
    tpl_name = _rel(tpl_path).replace(_rel(folder) + "/", "") if tpl_path else "-"
    q_exists = FQ.path(doc_id).exists()
    from . import formqa

    qa = formqa.check(doc_id, docs)   # 서식 폴더 qa.py (이 서식만의 질문)

    L = [f"# {spec.name} (`{doc_id}`)", "",
         f"<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card {doc_id} · card-hash: {card_hash(doc_id)} -->", "",
         f"- **종류:** {KIND_NAME[kind]}",
         f"- **그룹:** {spec.group} · **쪽 수:** {len(r['images'])} (seed {seed} 로 그린 것) · **분류 정답:** {view['classify']['answer']}"
         + (f" (다른 이름: {', '.join(view['classify']['aliases'])})" if view["classify"]["aliases"] else ""),
         f"- **쓰이는 업무:** {', '.join(_scenarios(doc_id)) or '없음 (서류 한 건 과제에만)'}",
         "- **질문·답:** " + ("이 폴더의 `questions.json` 에서 바꾼 것이 있음 (아래 ← 바꿈)" if q_exists
                              else "모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`"),
         "- **이 서식만의 질문:** " + (f"`qa.py` 의 {len(qa['rows'])}개 (아래)" if qa["rows"]
                                   else f"없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa {doc_id} --new`)"),
         "- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지",
         ""]
    if spec.description:
        L += ["> " + spec.description.splitlines()[0], ""]

    # 파일
    L += ["## 파일", "", "| 파일 | 정하는 것 |", "|---|---|"]
    roles = {"look/template.html.j2": "모양·칸 자리 (`{{ f(\"키\", label=\"항목명\") }}`)", "fields.json": "칸 목록·값 출처",
             "generate.py": "값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계)", "questions.json": "기본 과제의 질문 문장·답 틀 (기본과 다른 것만)",
             "qa.py": "이 서식만의 질문·정답 (함수 하나 = 질문 하나)",
             "form.json": "이름·그룹·출처", "layout.json": "원본에서 자동 추출한 칸 자리 (초안)", "look/original.pdf": "원본 PDF",
             "variants": "레이아웃 변형", "source.png": "원본 그림 (검수용)"}
    for rel, role in roles.items():
        if (folder / rel).exists():
            L.append(f"| `{rel}` | {role} |")
    if kind == "code" and gen_text:
        helpers = sorted(set(re.findall(r"^\s*from docgen\.docs\.(\w+) import", gen_text, re.M)) - {"_common"})
        if helpers:
            L.append(f"| {', '.join(f'`docgen/docs/{h}.py`' for h in helpers)} (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |")
    L += ["| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |", ""]

    # 추출 항목
    for task in ("kie", "marks"):
        v = view[task]
        if not v["items"]:
            continue
        title = "추출 항목 (정보 추출 kie)" if task == "kie" else "체크·도장·서명 (marks)"
        L += [f"## {title} — {sum(it['ask'] for it in v['items'])}칸", "",
              "| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |", "|---|---|---|---|---|---|---|---|---|"]
        label_seen: dict = {}
        for it in v["items"]:
            f = by_pattern.get(it["key"])
            key = f"`{it['key']}`" + (f" ← `{it['from']}`" if it.get("from") else "")
            first_label = (it["labels"] or [None])[0]
            label_seen[first_label] = label_seen.get(first_label, 0) + 1
            label = it["q_label"] or " / ".join(str(x) for x in it["labels"])
            if "label" in it["changed"]:
                label += f" ← 바꿈 (칸: {it['label']})"
            typ = (f or {}).get("type") or it.get("kind") or "-"
            if task == "marks" and it.get("options"):
                typ += f" ({' / '.join(it['options'])})"
            seen = "늘" if it["seen"] == it["of"] else f"{it['seen']}/{it['of']}"
            pos = _pos(f, r["sizes"]) + (" (1행)" if "*" in it["key"] else "")
            orig = it.get("from") or it["key"]
            ask = ("묻기" if it["ask"] else "안 묻기") + (" ← 바꿈" if "ask" in it["changed"] else "")
            e = info.get(orig) or {}
            if kind in ("code", "html"):
                tline = _where_defined(kind, orig, first_label, tpl, None, None, tpl_name)
                key_from, value_from = "템플릿", e.get("value_from") or _source_of(kind, orig, declared)
                where = " · ".join(x for x in (tline if tline != "-" else None, e.get("where"), e.get("q_where")) if x) or "-"
            else:
                key_from, value_from, where = e.get("key_from", "-"), e.get("value_from", "-"), e.get("where", "-")
            L.append(f"| {key} | {label} | {typ} | {pos} | {seen} | {key_from} | {value_from} | {where} | {ask} |")
        L.append("")
    L += ["- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.",
          "- **키 `a` ← `b`:** 질문·정답은 공통 키 a, 서식의 원래 키는 b (키 사전이 정함).",
          "- **키는·값은:** 어디서 정해지나. 원본 서식의 \"규칙\"·\"항목명 자동\" 은 키 사전(studio 키 사전 화면, `_common/key_rules.json`)이 "
          "항목명으로 정한 것 — 모든 서식에 같이 적용. 이 서식의 그 칸만 바꾸려면 **고칠 곳** 줄(칸)에 `\"key\"`·`\"kind\"`·`\"source\"` 를 적습니다.",
          "- **고칠 곳:** html·코드 서식은 템플릿 줄(칸 자리·키·항목명)과 fields.json 줄(값 출처·질문 설정 q), 원본 서식은 fields.json 의 그 칸"
          "(박스 `rect`·항목명·키·값·q). html·코드 서식에서 fields.json 에 줄이 없는 칸의 질문 설정은 fields.json 맨 위 `\"q\": {\"키\": {…}}` 묶음에.", ""]

    # 질문 → 답
    L += [f"## 질문 → 답 (seed {seed} 로 그린 실제 문항)", "",
          "질문은 모델에게 가는 글 전부, 답은 데이터의 정답 (그린 문서의 값·위치). 질문 문장·답 꼴은 "
          + ("이 폴더 `questions.json` 과 " if q_exists else "") + "공통 `docgen/forms/_common/questions.json`.", ""]
    shown = {}
    for rec in recs:
        t = rec["task"]
        shown[t] = shown.get(t, 0) + 1
        if shown[t] > (2 if t in ("ocr_field", "freetext") else 1) or t == "form_qa":   # form_qa 는 아래 qa.py 절에
            continue
        L += [f"### {TASK_TITLE.get(t, t)} `{t}` · 채점 {MAIN.get(t, '-')}", ""]
        if t in ("kie", "marks"):
            v = view[t]
            ch = lambda k: " ← 이 서식에서 바꿈" if k in v["changed"] else ""
            L += [f"틀 (질문의 항목 한 줄 · 답 항목 하나 · 빈 칸일 때) — `questions.json` 의 `{t}`:", "", "```",
                  f"item:         {v['item']}{ch('item')}",
                  f"answer:       {json.dumps(v['answer'], ensure_ascii=False)}{ch('answer')}",
                  f"answer_empty: {json.dumps(v['answer_empty'], ensure_ascii=False)}{ch('answer_empty')}", "```", ""]
        prose = isinstance(rec["answer"], str) and "\n" in rec["answer"]   # 줄글 답은 글 그대로
        L += ["질문:", "", "```", rec["prompt"], "```", "", "답:", "", "```" if prose else "```json",
              rec["answer"] if prose else _answer_text(rec["answer"]), "```", ""]
    L += ["## 이 서식만의 질문 `qa.py` (과제 form_qa)", ""]
    if qa["rows"]:
        L += ["함수 하나 = 질문 하나. 정답은 그린 문서의 칸 값으로 함수가 만든다. 채점은 정답 꼴로 기본 채점 "
              "(다르게 하려면 `train/scorers` 의 채점 함수 — `meta.question` 으로 가름).", "",
              "| 질문 (함수) | 묻는 문서 | 정답 꼴 → 기본 채점 | 예시 질문 | 예시 정답 |", "|---|---|---|---|---|"]
        cell = lambda x: str(x).replace("|", "\\|").replace("\n", " ⏎ ")
        for row in qa["rows"]:
            ex = row["example"] or {}
            L.append(f"| `{row['name']}` | {row['asked']}/{row['of']} | {row['kind'] or '-'} | {cell(ex.get('prompt', '-'))} | "
                     f"{cell(json.dumps(ex['answer'], ensure_ascii=False) if 'answer' in ex else '-')} |")
        L += ["", f"- **묻는 문서:** 여러 seed 로 그린 {qa['rows'][0]['of']}개 문서 중 이 질문이 나온 수 (칸이 빈 문서에서는 묻지 않음).",
              "- **기본 채점:** number 숫자가 같은지 · yesno 예/아니오 · text 띄어쓰기·문장부호 무시하고 같은지 · json 칸마다 같은지.", ""]
        L += [f"- 문제: {p}" for p in qa["problems"]] + ([""] if qa["problems"] else [])
    else:
        L += [f"없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa {doc_id} --new`):", "",
              "```python", "def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)",
              '    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감', "```", ""]

    # 고치려면
    L += ["## 고치려면", "", "칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.",
          "고친 뒤 `python -m docgen.formdir check " + doc_id + "` → `python -m docgen.formdir card " + doc_id + "` (실제 질문→답 확인).", "",
          "| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |", "|---|---|---|"]
    if kind in ("code", "html"):
        L += [f"| 칸(추출 항목) 더하기 | `{tpl_name}` 에 `{{{{ f(\"키\", label=\"항목명\") }}}}` + "
              + ("`generate.py` 가 돌려주는 dict 에 그 키 값" if kind == "code" else "`fields.json` 의 `fields` 에 키·source")
              + " | 다시 |",
              f"| 답의 키·칸의 항목명 | `{tpl_name}` 의 `f(\"키\", label=…)`" + (" + `fields.json` 의 그 키" if kind == "html" else "") + " | 다시 |",
              "| 답의 값 | " + ("`generate.py` (값 만드는 함수). 파이썬 대신 정하려면 `fields.json` 의 그 칸 `source`" if kind == "code"
                              else "`fields.json` 의 그 칸 `source` ([값 출처 목록](../_common/values.md))") + " | 다시 |",
              "| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py`" + ("" if kind == "code" else " 의 `adjust(d, p, rng)`") + " | 다시 |",
              f"| 답의 위치 (박스) | `{tpl_name}` 배치 (studio html 편집). 숫자로 고정하려면 `fields.json` `regions` | 다시 |"]
    else:
        L += ["| 칸(추출 항목) 더하기 | studio ① 서식 › 영역 편집에서 그리기 (`fields.json` items 에 한 칸) | 다시 |",
              "| 답의 위치 (박스) | `fields.json` 그 칸의 `rect` [x0, y0, x1, y1] (pt) — 또는 영역 편집 | 다시 |",
              "| 답의 키 | `fields.json` 그 칸에 `\"key\"` (없으면 규칙이 항목명으로 정함 — 모든 서식 공통 규칙은 studio 키 사전) | 다시 |",
              "| 답의 값 | `fields.json` 그 칸에 `\"source\"` ([값 출처 목록](../_common/values.md)) 또는 값 종류 `\"kind\"` | 다시 |",
              "| 칸의 항목명 | `fields.json` 그 칸의 `label` | 다시 |"]
    if kind in ("code", "html"):
        L.append('| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |')
    L += ['| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |',
          '| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |',
          '| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |',
          '| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\\n{items}"}}` | 필요 없음 |',
          '| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |',
          '| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |',
          f'| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa {doc_id} --new`) | 필요 없음 |',
          '| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |',
          "| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |", "",
          "\"다시\" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.",
          f"확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions {doc_id} --show` · `python -m docgen.preview {doc_id} --out work/{doc_id}`", ""]
    return "\n".join(L)


def _answer_text(a) -> str:
    if isinstance(a, list) and a and all(isinstance(x, dict) for x in a):
        return "[" + ",\n ".join(json.dumps(x, ensure_ascii=False) for x in a) + "]"
    return json.dumps(a, ensure_ascii=False, indent=1) if isinstance(a, (dict, list)) else json.dumps(a, ensure_ascii=False)


# ---------------------------------------------------------------------------
# 만들기
# ---------------------------------------------------------------------------

_B = None


def _init():
    global _B
    from multiprocessing.util import Finalize

    from .bench.build import Builder

    td = tempfile.mkdtemp(prefix="formcard_")
    _B = Builder(Path(td), 1.0)
    Finalize(_B, _B.close, exitpriority=10)


def _one(doc_id: str) -> str:
    text = render_card(doc_id, _B)
    path(doc_id).write_text(text, encoding="utf-8")
    return doc_id


def write_many(ids: list[str], workers: int = 1) -> list[str]:
    """카드를 만든다 (그림을 그리므로 브라우저가 필요). 만든 ID 목록."""
    if not ids:
        return []
    if workers <= 1:
        global _B
        from .bench.build import Builder

        with tempfile.TemporaryDirectory(prefix="formcard_") as td:
            _B = Builder(Path(td), 1.0)
            try:
                return [_one(i) for i in ids]
            finally:
                _B.close()
    from multiprocessing import get_context

    with get_context("spawn").Pool(workers, initializer=_init) as pool:
        return list(pool.imap(_one, ids, chunksize=4))


# ---------------------------------------------------------------------------
# 공통 값 출처 목록 docgen/forms/_common/values.md (코드에서 만든다 — 손으로 고치지 않음)
# ---------------------------------------------------------------------------

def values_md() -> str:
    """fields.json 의 "source" 에 쓸 수 있는 것 전부: rule:<종류>, 키 사전에서 더한 종류, profile.<경로>(예시 값)."""
    from . import keyrules as R
    from . import sources as S
    from .entities import make_profile

    L = ["# 값 출처 (fields.json 의 source)", "",
         "<!-- 자동 생성: python -m docgen.formdir values · 코드(docgen/sources.py, docgen/keyrules.py, docgen/entities.py)에서 만든다 -->", "",
         "서식 칸 목록 `fields.json` 의 `\"source\"` 에 쓰는 것. 칸 하나의 값을 문서를 그릴 때마다 여기서 만든다.",
         "칸끼리 관계(합계·날짜 순서·조건)는 값 출처가 아니라 서식 폴더의 `generate.py` 로 맞춘다.", "",
         "## 특별한 것", "", "| source | 값 |", "|---|---|",
         "| `rule:choice` | 칸의 `choices` 목록에서 하나 |", "| `rule:fixed` | 칸의 `text` 그대로 |",
         "| `rule:free_text` | 짧은 자유 기재 문장 (가끔 빈 칸) |", "| `rule:empty` | 늘 빈 칸 |",
         "| `rule:date_seq` | 반복 행에서 행마다 늘어나는 날짜 (`span_days`, `step_days`) |",
         "| `code` | (코드 서식) 값 만드는 함수 generate.py 가 만든 값 그대로 |", "",
         "## 값 종류 `rule:<종류>` — 코드로 만드는 것 (docgen/realform.py Values.by_kind)", "", "| source | 값 |", "|---|---|"]
    L += [f"| `rule:{k}` | {v} |" for k, v in R.CODE_KINDS.items() if k not in ("skip", "seal")]
    kinds = R.load().get("kinds", {})
    if kinds:
        L += ["", "## 값 종류 `rule:<종류>` — 키 사전에서 더한 것 (key_rules.json 의 kinds, studio 키 사전 화면이 고침)", "",
              "| source | 뜻 | 만드는 법 |", "|---|---|---|"]
        for k, v in kinds.items():
            how = v.get("how")
            what = {"source": f"프로필 `{v.get('source')}`", "pattern": f"틀 `{v.get('pattern')}`",
                    "choices": "보기 " + ", ".join(list(v.get("choices", {}))[:6])}.get(how, how or "-")
            L.append(f"| `rule:{k}` | {v.get('meaning', '')} | {what} |")
    L += ["", "## 고객 프로필 `profile.<경로>` (예시 값은 seed 0 고객)", "",
          "한 문서·한 업무 묶음 안에서 같은 사람의 값이 서로 맞아야 하면 이쪽 (성명·주민번호·주소·직장 …).", "",
          "| source | 예시 |", "|---|---|"]
    for row in S.profile_paths(make_profile(0)):
        ex = str(row.get("example", "")).replace("|", "\\|").replace("\n", " ")
        L.append(f"| `{row['source']}` | {ex[:60]} |")
    return "\n".join(L) + "\n"
