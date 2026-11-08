"""영역 편집기의 생성 방법 고르기: 칸에 넣을 값을 어떻게 만들지 사람이 읽는 이름·예시 값으로 보여 준다.

고르면 칸 목록 fields.json 의 "source" 가 된다 (docgen/sources.py). 여기는 고르기 쉬운 목록과 예시만 만들고,
새 생성 방법을 더하는 길 (화면의 "원하는 생성 방법이 없으면" 안내와 같은 내용, guide/new-forms.md 0절):

  칸에서 바로    보기 중 하나 (rule:choice + choices), 틀로 만들기 (rule:pattern + pattern: # 숫자, A 대문자, {가|나} 고르기)
  다시 쓰게 저장 그 보기·틀을 키 사전의 값 종류로 저장 (PUT /api/keyrules/kinds/<이름>, key_rules.json "kinds")
                 → 이 목록의 "키 사전에서 더한 것" 묶음 (source = rule:<종류>)
  코드로         docgen/forms/_common/generators.py 에 @generator 함수 하나 (docgen/usergen.py)
                 → "직접 만든 생성기 (코드)" 묶음 (source = rule:<함수 이름>)
  칸끼리 관계    (합계 = 행의 합, 시작일 ≤ 종료일 …) 는 칸 하나의 생성 방법이 아니라 서식 폴더의 generate.py 의 adjust
                 (html·overlay 모두. overlay 견본: python -m docgen.formdir adjust <ID> --new)
"""
from __future__ import annotations

import random

# (묶음, [(이름, source, 설명)]) — 자주 쓰는 것을 앞에. 프로필 경로는 고객 정보 (같은 고객의 다른 서류와 같은 값)
PRESETS = [
    ("고객 정보 — 같은 고객의 다른 서류와 같은 값 (서류 대조에 필요)", [
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
        ("서류 날짜 (발급·작성일)", "profile.issue_date", "그 고객의 서류 묶음에서 같은 날"),
    ]),
    ("날짜·금액·숫자 — 문서마다 새로", [
        ("날짜", "rule:date", "최근 날짜. 항목명에 만기·기한·종료가 있으면 앞날짜"),
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
AUTO = ("자동", "", "항목명으로 값 종류를 추정해 만듭니다. 추정 못 하면 빈 칸")
HOWTO = [
    {"title": "1. 코드 없이 이 칸에서 — 보기 중 하나 · 틀로 만들기",
     "where": "이 창의 '직접 정하기'",
     "how": "보기 목록(한 줄에 하나)이나 틀(# 숫자, A 대문자, a 소문자, {가|나} 하나 고르기 — 예: HN-####-{A|B})을 적습니다. "
            "칸 오른쪽의 [값 종류로 저장]을 누르면 다른 칸·다른 서식에서도 고를 수 있게 됩니다."},
    {"title": "2. 코드 없이 다시 쓰게 — 키 사전의 값 종류",
     "where": "studio 키 사전 › 값 종류 (docgen/forms/_common/key_rules.json 의 \"kinds\")",
     "how": "이름·뜻 + 만드는 법 하나: 보기 목록(가중치), 틀, 프로필 경로. 이 창의 '키 사전에서 더한 것'에 나옵니다."},
    {"title": "3. 코드로 — 직접 만든 생성기",
     "where": "docgen/forms/_common/generators.py (설명 docgen/usergen.py)",
     "how": "@generator(\"화면 이름\") 를 붙인 함수 def 이름(p, rng, item, row): return 값 — p 고객 프로필, rng 난수(이것만), item 칸 정보, row 표 행 번호. "
            "파일을 저장하면 studio 를 다시 띄우지 않아도 이 창의 '직접 만든 생성기'에 나옵니다. 예시 함수 3개가 들어 있습니다."},
    {"title": "4. 칸끼리 관계 — 합계·순서·조건",
     "where": "서식 폴더의 generate.py (adjust 함수)",
     "how": "합계 = 행의 합, 시작일 ≤ 종료일, 잔액 같은 관계는 칸 하나의 생성 방법으로 안 됩니다. 영역 편집 위의 [칸끼리 관계 견본 만들기] "
            "(= python -m docgen.formdir adjust <ID> --new)로 이 서식의 칸 키가 적힌 견본을 만들고 adjust 를 고칩니다."},
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
    """{groups: [{name, items: [{name, source, note, examples}]}], auto, howto}. 키 사전에서 더한 종류도 한 묶음."""
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
        groups.append({"name": "키 사전에서 더한 것 (코드 없이 만든 값 종류)",
                       "items": [{"name": k.get("meaning") or name, "source": f"rule:{name}", "note": name, "examples": _examples(f"rule:{name}")}
                                 for name, k in kinds.items()]})
    return {"groups": groups, "auto": {"name": AUTO[0], "source": AUTO[1], "note": AUTO[2]}, "howto": HOWTO,
            "formats": [{"id": k, "name": v[0], "example": v[1]} for k, v in FORMATS.items()],
            "fills": [{"id": k, "name": v} for k, v in FILLS.items()], "generator_error": gen_error}
