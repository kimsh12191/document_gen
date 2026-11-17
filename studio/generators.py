"""영역 편집기의 생성 방법 고르기: 칸에 넣을 값을 어떻게 만들지 사람이 읽는 이름·예시 값으로 보여 준다.

고르면 칸 목록 fields.json 의 "source" 가 된다 (docgen/sources.py). 여기는 고르기 쉬운 목록과 예시만 만들고,
원하는 것이 없을 때 (화면의 "원하는 생성 방법이 없으면" 안내와 같은 내용, guide/studio/generators.md):

  1. 고르기 창에서 적기   보기 중 하나 (rule:choice + choices), 틀로 만들기 (rule:pattern + pattern) — 그 칸에만
                          (예전에 key_rules.json "kinds" 에 저장한 공통 값 종류는 "공통 값 종류" 묶음으로 계속 나옴)
  2. 값 하나를 만드는 함수 docgen/forms/_common/generators.py 에 @generator 함수 (docgen/usergen.py)
                          → "직접 만든 생성기" 묶음 (source = rule:<함수 이름>)
  3. 칸끼리 관계 맞추기   합계 = 행의 합, 시작일 ≤ 종료일 … 은 칸 하나의 생성 방법이 아니라 서식 폴더 generate.py 의 adjust
                          (html·overlay 모두. overlay 견본: python -m docgen.formdir adjust <ID> --new)
"""
from __future__ import annotations

import random

# (묶음, [(이름, source, 설명)]) — 자주 쓰는 것을 앞에. 프로필 경로는 고객 정보 (같은 고객의 다른 서류와 같은 값)
PRESETS = [
    ("고객 정보 — 가짜 고객 한 명의 값 (한 문서 안에서 서로 맞음)", [
        ("고객 이름", "profile.person.name", ""),
        ("영문 이름", "profile.person.name_en", ""),
        ("생년월일", "profile.person.birth", ""),
        ("주민등록번호", "profile.person.rrn", ""),
        ("휴대전화", "profile.person.mobile", ""),
        ("이메일", "profile.person.email", ""),
        ("주소", "profile.person.address.road_short", ""),
        ("우편번호", "profile.person.address.zipcode", ""),
        ("직장명", "profile.employment.company.name", ""),
        ("직장 주소", "profile.employment.company.address.road_short", ""),
        ("직장 전화", "profile.employment.company.phone", ""),
        ("부서", "profile.employment.department", ""),
        ("직위", "profile.employment.position", ""),
        ("입사일", "profile.employment.hire_date", ""),
        ("연봉", "profile.employment.annual_salary", ""),
        ("사업자등록번호 (직장)", "profile.employment.company.biz_no", ""),
        ("서류 날짜 (발급·작성일)", "profile.issue_date", "이 문서의 발급·작성일"),
    ]),
    ("날짜·금액·숫자 — 문서마다 새로", [
        ("날짜", "rule:date", "최근 날짜. 키 설명에 만기·기한·종료가 있으면 앞날짜"),
        ("행마다 늘어나는 날짜", "rule:date_seq", "표의 날짜 열 (거래일 등)"),
        ("원화 금액", "rule:amount", ""),
        ("외화 금액", "rule:fx_amount", ""),
        ("비율·이율", "rule:percent", ""),
        ("환율", "rule:rate", ""),
        ("수량·건수·기간", "rule:count", ""),
        ("번호·코드", "rule:number", ""),
    ]),
    ("기관·금융 — 문서마다 새로", [
        ("은행", "rule:bank", ""), ("지점", "rule:branch", ""), ("계좌번호", "rule:account", ""),
        ("회사명", "rule:company", ""), ("금융 상품명", "rule:product", ""), ("대출 과목", "rule:loan_subject", ""),
        ("상환 방법", "rule:repay", ""), ("통화", "rule:currency", ""), ("국가", "rule:country", ""),
        ("품목", "rule:goods", ""), ("수표·어음 번호", "rule:check_no", ""), ("수표 종류", "rule:check_kind", ""),
        ("여권번호", "rule:passport", ""), ("사업자등록번호", "rule:biz_no", ""),
        ("기관·회사 전화", "rule:office_phone", ""), ("다른 사람 이름", "rule:other_person", "담당자·직원 (고객 아님)"),
        ("사람 이름 (고객 또는 다른 사람)", "rule:person", ""),
    ]),
    ("글자", [
        ("사유·목적", "rule:reason", ""), ("비고", "rule:note", "대개 '해당 없음'"),
        ("짧은 자유 문장", "rule:free_text", "가끔 빈 칸"),
    ]),
    ("직접 정하기", [
        ("보기 중 하나", "rule:choice", "보기 목록을 적습니다 (예: 이체·입금·출금)"),
        ("늘 같은 글자", "rule:fixed", "글자를 적습니다"),
        ("틀로 만들기", "rule:pattern", "틀을 적습니다: # 숫자, A 대문자, a 소문자, {가|나} 하나 고르기 (예: HN-####-{A|B})"),
        ("늘 빈 칸", "rule:empty", "인쇄만 있고 값을 쓰지 않는 칸"),
    ]),
]
AUTO = ("자동", "", "키가 고객 정보 키(name·birth 등)면 그 값, 아니면 이 칸의 값 종류대로. 둘 다 아니면 빈 칸")
HOWTO = [
    {"title": "1. 고르기 창에서 적기 (코드 없음)",
     "when": "몇 개 중 하나, 정해진 꼴의 번호",
     "example": "보기 중 하나: 이체 / 입금 / 출금 · 틀로 만들기: HN-####-{A|B} → HN-4821-B",
     "how": "위 '직접 정하기' 묶음에서 고르고 칸 오른쪽에 보기 목록(한 줄에 하나)이나 틀(# 숫자, A 대문자, a 소문자, {가|나} 하나)을 적습니다. "
            "이 칸에만 적용됩니다. 여러 서식에서 같은 값이 필요하면 2번(함수)으로 만듭니다."},
    {"title": "2. 값 하나를 만드는 함수 (코드)",
     "when": "계산이 들어간 값 하나 — 가린 계좌번호, 행마다 1회·2회, 비율을 정한 보기",
     "example": "@generator(\"상환 회차\")\ndef repay_round(p, rng, item, row):\n    return f\"{row + 1}회\"",
     "how": "docgen/forms/_common/generators.py 끝에 함수 하나를 붙이고 저장 → studio 재시작 없이 이 창의 '직접 만든 생성기'에 나옵니다. "
            "난수는 rng 만, 고객 값은 p 에서. 순서·빈 틀·예: guide/studio/generators.md 2절."},
    {"title": "3. 칸끼리 관계 맞추기 (코드, 이 서식만)",
     "when": "여러 칸이 서로 맞아야 할 때 — 합계 = 행의 합, 시작일 ≤ 종료일, 잔액",
     "example": "def adjust(d, p, rng):   # 값을 칸마다 다 만든 뒤 한 번 불림\n"
                "    total = sum(to_amount(r.get(\"in\")) or 0 for r in rows(d, \"deals\"))\n"
                "    put(d, \"total.in\", amount_like(total, \"1,000\"))   # 합계 = 행의 합\n"
                "    return d",
     "how": "칸 하나의 생성 방법으로는 안 됩니다. 영역 편집 위 '칸끼리 관계: [견본 만들기]' → 서식 폴더에 generate.py (이 서식의 칸 키가 적힘) → "
            "adjust(d, p, rng) 를 채웁니다. 설명·예: guide/studio/generators.md 3절."},
]


def _examples(source: str, n: int = 3) -> list[str]:
    if source == "rule:pattern":
        return ["HN-4821-B", "HN-0937-A"]
    from docgen import sources as SRC
    from docgen.entities import make_profile

    out = []
    for seed in range(n * 3):
        if len(out) >= n:
            break
        try:
            v = SRC.value(source, make_profile(seed), random.Random(seed), {"label": "", "choices": ["보기1", "보기2"], "text": "(적은 글자)"}, row=seed % 3)
        except Exception:  # noqa: BLE001 — 예시를 못 만들면 예시 없이
            v = None
        if v not in (None, "") and str(v) not in out:
            out.append(str(v))
    return out


def catalog() -> dict:
    """{groups: [{name, items: [{name, source, note, examples}]}], auto, howto}. key_rules.json 의 공통 값 종류도 한 묶음."""
    from docgen import keyrules as KR

    groups = [{"name": g, "items": [{"name": n, "source": s, "note": note, "examples": _examples(s) if s not in ("rule:empty",) else []}
                                   for n, s, note in items]} for g, items in PRESETS]
    from docgen import sources as SRC

    shown = {i["source"] for g in groups for i in g["items"]}
    more = [k for k in SRC.RULE_KINDS if f"rule:{k}" not in shown and k not in ("phone", "address", "email")]   # 셋은 고객 정보와 같은 값
    if more:   # 코드로 새로 더한 값 종류 (Values.by_kind + RULE_KINDS)
        groups.append({"name": "그 밖의 값 종류 (코드)", "items": [{"name": KR.CODE_KINDS.get(k, k), "source": f"rule:{k}", "note": k,
                                                                  "examples": _examples(f"rule:{k}")} for k in more]})
    from docgen import usergen
    from docgen.formkit import FORMATS
    from docgen.realform import FILLS

    try:
        gens = usergen.all_generators()
        gen_error = None
    except ValueError as e:
        gens, gen_error = {}, str(e)
    groups.append({"name": "직접 만든 생성기 (코드: docgen/forms/_common/generators.py)", "file": str(usergen.path()),
                   "items": [{"name": g["name"], "source": f"rule:{name}", "note": g["note"] or name, "examples": _examples(f"rule:{name}")}
                             for name, g in gens.items()]})
    kinds = KR.load()["kinds"]
    if kinds:
        groups.append({"name": "공통 값 종류 (docgen/forms/_common/key_rules.json)",
                       "items": [{"name": k.get("meaning") or name, "source": f"rule:{name}", "note": name, "examples": _examples(f"rule:{name}")}
                                 for name, k in kinds.items()]})
    return {"groups": groups, "auto": {"name": AUTO[0], "source": AUTO[1], "note": AUTO[2]}, "howto": HOWTO,
            "formats": [{"id": k, "name": v[0], "example": v[1]} for k, v in FORMATS.items()],
            "fills": [{"id": k, "name": v} for k, v in FILLS.items()], "generator_error": gen_error,
            "floats": _floats()}


def _floats() -> dict:
    """자유 위치 도장·번호의 종류·영역·색 (docgen/floats.py) — 영역 편집기·표시 요소 화면."""
    from docgen import floats as FL

    return {"presets": [{"id": k, **v} for k, v in FL.PRESETS.items()], "areas": [{"id": k, "name": FL.AREA_NAMES[k]} for k in FL.AREAS],
            "colors": {"red": "빨강", "blue": "파랑"}, "styles": {"print": "인쇄", "stamp": "스탬프 (색·기울기)", "hand": "손글씨"}}
