"""영역 편집기의 생성 방법 고르기: 칸에 넣을 값을 어떻게 만들지 사람이 읽는 이름·예시 값으로 보여 준다.

고르면 칸 목록 fields.json 의 "source" 가 된다 (docgen/sources.py). 여기는 고르기 쉬운 목록과 예시만 만들고,
값을 실제로 만드는 코드는 아래 셋이다 (화면의 "새 생성 방법 만들기" 안내와 같은 내용, guide/new-forms.md 0절).

  코드 없이   키 사전 화면의 값 종류 (docgen/forms/_common/key_rules.json "kinds": 보기 목록·틀·프로필 경로)
              → 이 목록의 "키 사전에서 더한 것" 묶음에 나온다 (source = rule:<종류>)
  코드로      docgen/realform.py Values.by_kind 에 종류 하나 (if kind == "<이름>": return …)
              + docgen/sources.py RULE_KINDS 에 이름 + docgen/keyrules.py CODE_KINDS 에 설명 → "종류" 묶음에 나온다
  칸끼리 관계 (합계 = 행의 합, 시작일 ≤ 종료일 …) 는 생성 방법이 아니라 서식 폴더의 generate.py — html 서식만.
              overlay(그린 서식)는 아직 없다: docgen/realform.py build_form 이 값을 만들면서 바로 칸에 맞춰 배치하기 때문
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
        ("늘 빈 칸", "rule:empty", "인쇄만 있고 값을 쓰지 않는 칸"),
    ]),
]
AUTO = ("자동", "", "항목명으로 값 종류를 추정해 만듭니다. 추정 못 하면 빈 칸")
HOWTO = [
    {"title": "코드 없이 — 키 사전의 값 종류",
     "where": "studio 키 사전 화면 › 값 종류 (docgen/forms/_common/key_rules.json 의 \"kinds\")",
     "how": "이름·뜻과 만드는 법 하나: 보기 목록(가중치), 틀(# = 숫자, {A|B} = 하나 고르기), 프로필 경로. 저장하면 이 목록의 '키 사전에서 더한 것'에 나옵니다."},
    {"title": "코드로 — 새 값 종류",
     "where": "docgen/realform.py 의 Values.by_kind",
     "how": "if kind == \"<이름>\": return <값> 을 더하고 (난수는 self.r, 고객은 self.p), docgen/sources.py 의 RULE_KINDS 에 이름, "
            "docgen/keyrules.py 의 CODE_KINDS 에 설명을 넣습니다. studio 를 다시 띄우면 '날짜·금액·숫자' 등과 같이 나옵니다 (이름은 CODE_KINDS 설명)."},
    {"title": "칸끼리 관계 — 합계·순서·조건 (html 서식만)",
     "where": "서식 폴더의 generate.py (html 서식)",
     "how": "합계 = 행의 합, 시작일 ≤ 종료일, 잔액 같은 관계는 칸 하나의 생성 방법으로 안 됩니다. html 서식은 서식 폴더 generate.py 의 adjust 로 맞추고, "
            "그린 서식(overlay)은 아직 맞추는 곳이 없습니다. 관계가 중요한 서식이면 새 서식 추가 B(html 서식)로 만듭니다."},
]


def _examples(source: str, n: int = 3) -> list[str]:
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
    kinds = KR.load()["kinds"]
    if kinds:
        groups.append({"name": "키 사전에서 더한 것 (코드 없이 만든 값 종류)",
                       "items": [{"name": k.get("meaning") or name, "source": f"rule:{name}", "note": name, "examples": _examples(f"rule:{name}")}
                                 for name, k in kinds.items()]})
    return {"groups": groups, "auto": {"name": AUTO[0], "source": AUTO[1], "note": AUTO[2]}, "howto": HOWTO}
