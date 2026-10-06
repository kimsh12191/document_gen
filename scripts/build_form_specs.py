"""P3 서식의 선언형 스펙 모듈을 생성한다.

  python scripts/build_form_specs.py

입력
  add_template/field_specs/<분류>/<No>.json   PDF 에서 뽑은 기재란 (extract_form_fields.py)
  scripts/form_map.py                         서식별 판정 (P3 만 대상)
출력
  docgen/docs/forms_<모듈>.py                 FORM(...) 선언 묶음

라벨 → 키 변환
  LABEL_KEY 에 있는 라벨은 Profile 에서 값을 끌어오는 표준 키로 바꾼다 (성명 → customer.name).
  나머지는 라벨 끝말로 종류(date/amount/number/…)만 추론하고 키는 그 서식 안에서만 쓰는 이름을 준다.
  표준 키로 바뀐 항목은 같은 프로필의 다른 서류와 값이 일치한다.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from form_map import P3_MODULE, verdict  # noqa: E402

SPECS = ROOT / "add_template" / "field_specs"
OUT = ROOT / "docgen" / "docs"
CSV = ROOT / "add_template" / "하나은행_서식자료" / "다운로드_결과.csv"

# 분류 → docgen 그룹
GROUP = {"외환": "fx", "대출": "bank_form", "예금": "bank_form", "전자금융": "efinance",
         "퇴직연금": "retirement", "파생상품": "finance", "신탁/ISA": "finance", "펀드": "finance",
         "기타": "bank_form"}

# ---------------------------------------------------------------------------
# 라벨 → 표준 키 (Profile 에서 값을 끌어오는 항목)
# ---------------------------------------------------------------------------
LABEL_KEY: dict[str, str] = {}


def _reg(key: str, *labels: str) -> None:
    for x in labels:
        LABEL_KEY[x] = key


_reg("customer.name", "성명", "성명(사업자명)", "고객명", "신청인", "신청인명", "예금주", "성명(상호)",
     "위임인", "본인성명", "가입자", "가입자명", "성명(법인명)", "의뢰인", "신고인", "Name", "성명(명칭)")
_reg("customer.name_en", "영문성명", "성명(영문)", "EnglishName", "NameinEnglish")
_reg("customer.rrn", "주민등록번호", "주민번호", "실명번호", "주민등록번호(사업자등록번호)")
_reg("customer.birth", "생년월일", "생년월일(사업자번호)", "생년월일(사업자등록번호)", "DateofBirth", "생년월일(설립일)")
_reg("customer.address", "주소", "주소지", "자택주소", "주 소", "소재지(주소)", "Address", "현주소")
_reg("customer.phone", "연락처", "전화번호", "휴대폰번호", "휴대전화", "휴대폰", "전화", "연락전화",
     "핸드폰번호", "TelNo", "Telephone", "연락처(휴대폰)")
_reg("customer.email", "이메일", "E-mail", "이메일주소", "Email", "e-mail", "전자우편")
_reg("customer.nationality", "국적", "Nationality")
_reg("customer.job", "직업", "업종(직업)", "직업(업종)")
_reg("customer.zipcode", "우편번호", "ZipCode")
_reg("company.name", "기업명", "법인명", "상호", "업체명", "회사명", "상호또는성명", "사업장명",
     "법인(단체)명", "거래처명", "기업체명", "CompanyName")
_reg("company.biz_no", "사업자등록번호", "사업자번호", "사업자등록번호(고유번호)")
_reg("company.corp_no", "법인등록번호", "법인번호")
_reg("company.ceo", "대표자", "대표자명", "대표이사", "대표자성명")
_reg("company.address", "소재지", "사업장소재지", "본점소재지", "회사주소")
_reg("company.phone", "회사전화", "사업장전화", "대표전화")
_reg("company.fax", "팩스", "FAX", "팩스번호")
_reg("company.biz_type", "업태")
_reg("company.biz_item", "업종", "종목")
_reg("company.established", "설립일", "설립연월일", "개업일")
_reg("company.employees", "상시근로자수", "종업원수", "직원수")
_reg("company.capital", "자본금")
_reg("company.revenue", "매출액", "연매출")
_reg("company.department", "담당부서", "부서", "부서명")
_reg("employer.name", "직장명", "근무처", "소속회사")
_reg("employer.hire_date", "입사일자", "입사일")
_reg("employer.position", "직위", "직급")
_reg("employer.salary", "연소득", "연간소득", "소득금액")
_reg("bank", "은행명", "금융기관명", "거래은행", "취급은행")
_reg("branch", "취급점", "영업점", "지점명", "거래영업점")
_reg("account", "계좌번호", "출금계좌", "출금계좌번호", "입금계좌", "입금계좌번호", "결제계좌",
     "수수료출금계좌", "퇴직연금계좌번호", "계좌번호(카드번호)", "계좌(카드)번호", "AccountNo")
_reg("account.holder", "예금주명", "예금주성명")
_reg("agent.name", "대리인", "대리인성명", "대리인명", "수임인")
_reg("agent.birth", "대리인생년월일")
_reg("agent.relation", "본인과의관계", "관계", "위임인과의관계")
_reg("foreign.name", "상대방", "거래상대방", "수취인", "수취인명", "Beneficiary", "BeneficiaryName",
     "해외거래처", "상대방명")
_reg("foreign.address", "상대방주소", "수취인주소", "BeneficiaryAddress")
_reg("foreign.country", "국가", "상대국", "거래국가", "Country")
_reg("foreign.bank", "수취은행", "상대은행", "BeneficiaryBank")
_reg("foreign.swift", "SWIFT", "SWIFTCODE", "SwiftCode", "BIC")
_reg("foreign.account", "수취인계좌", "BeneficiaryAccount")
_reg("property.address", "부동산소재지", "담보물소재지", "물건소재지")
_reg("property.kind", "부동산종류", "담보물종류")
_reg("property.area", "면적", "전용면적")
_reg("property.price", "감정가액", "시가")
_reg("date", "작성일", "작성일자", "신청일", "신청일자", "신고일자", "년월일", "일자", "Date")

# ---------------------------------------------------------------------------
# 라벨 끝말 → 종류 (표준 키로 바뀌지 않은 항목)
# ---------------------------------------------------------------------------
KIND_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"(일자|년월일|일$|기간|만기|개시일|종료일|시작일)"), "date"),
    (re.compile(r"(금액|대금|가액|잔액|원금|이자|합계|^계$|수수료|보증금|한도|총액|백만원)"), "amount"),
    (re.compile(r"(외화금액|외화|US\$|USD)"), "fx_amount"),
    (re.compile(r"(이율|금리|비율|요율|율$|률$|%)"), "percent"),
    (re.compile(r"(환율)"), "rate"),
    (re.compile(r"(통화|통화코드|Currency)"), "currency"),
    (re.compile(r"(번호|No$|코드|ID)"), "number"),
    (re.compile(r"(수량|매수|건수|횟수|개수|매$)"), "count"),
]
# 기재란이지만 비워 두는 칸 (서식에만 있고 고객이 안 쓰는 자리)
BLANK_LABELS = re.compile(r"^(\(인\)|\(\)|\(서명/인\)|\(인/서명\)|선택항목|선택|기타|내용|비고)$")


def norm(s: str) -> str:
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s or ""))


def kind_of(label: str) -> str:
    for rx, kind in KIND_RULES:
        if rx.search(label):
            return kind
    return "text"


def slug(label: str, used: Counter) -> str:
    """표준 키가 없는 항목의 키 — 그 서식 안에서만 쓰는 이름."""
    kind = kind_of(label)
    base = {"date": "date", "amount": "amount", "fx_amount": "fx_amount", "percent": "rate",
            "rate": "fx_rate", "currency": "currency", "number": "no", "count": "count"}.get(kind, "item")
    used[base] += 1
    return f"{base}{used[base]}" if used[base] > 1 else base


def py(x) -> str:
    return json.dumps(x, ensure_ascii=False)


# 표가 인식되지 않은 서식에 쓰는 기본 기재란 (신청인 + 신청내용)
DEFAULT_FIELDS = [
    {"label": "성명", "kind": "text"}, {"label": "생년월일", "kind": "text"},
    {"label": "주소", "kind": "text"}, {"label": "연락처", "kind": "text"},
    {"label": "신청 내용", "kind": "text"}, {"label": "금액", "kind": "text"},
    {"label": "신청일자", "kind": "text"},
]
CORP_DEFAULT_FIELDS = [
    {"label": "상호", "kind": "text"}, {"label": "사업자등록번호", "kind": "text"},
    {"label": "대표자", "kind": "text"}, {"label": "소재지", "kind": "text"},
    {"label": "연락처", "kind": "text"}, {"label": "신청 내용", "kind": "text"},
    {"label": "금액", "kind": "text"}, {"label": "신청일자", "kind": "text"},
]
CORP_CLASSES = {"외환", "파생상품"}


def build(spec: dict) -> str | None:
    """field_specs JSON 하나 → FORM(...) 호출 코드."""
    cls, no = spec["class"], spec["no"]
    base = CORP_DEFAULT_FIELDS if cls in CORP_CLASSES else DEFAULT_FIELDS
    fields = spec["fields"]
    # 표 인식이 안 됐거나 항목이 너무 적은 서식은 기본 기재란(신청인 정보)으로 보강한다
    if len({norm(x["label"]) for x in fields}) < 3:
        fields = fields + [x for x in base if norm(x["label"]) not in {norm(y["label"]) for y in fields}]
    group = GROUP.get(cls, "bank_form")
    doc_id = f"hf{no:03d}"
    used, seen_label = Counter(), set()
    items: list[str] = []
    for fl in fields:
        label = norm(fl["label"])
        if not label or label in seen_label or BLANK_LABELS.match(label):
            continue
        seen_label.add(label)
        options = [norm(o) for o in (fl.get("options") or [])]
        options = [o for o in options if o][:6]
        key = LABEL_KEY.get(label)
        kind = "choice" if options else kind_of(label)
        if key is None:
            key = slug(label, used)
        items.append(f"        ({py(key)}, {py(fl['label'].strip())}, {py(kind)}"
                     + (f", {py(options)})" if options else ")"))
    if not items:
        return None
    # 섹션은 추출된 섹션 제목이 있으면 첫 번째를 쓰고, 없으면 '기재사항' 한 묶음으로 둔다
    title = next((s.split(". ", 1)[-1][:28] for s in spec["sections"] if len(s) < 40), "기재사항")
    code = spec["meta"].get("code", f"{cls}-{no:04d}")
    note = f"하나은행 공개 서식 No.{no} ({cls})"
    return (f'FORM({py(doc_id)}, {py(spec["name"][:60])}, {py(group)}, code={py(code)},\n'
            f'     title_note={py(note)},\n'
            f'     sections=[({py(title)}, [\n' + ",\n".join(items) + "\n     ])])\n")


def main() -> None:
    import csv
    rows = {int(r["No"]): r for r in csv.DictReader(CSV.read_text(encoding="utf-8-sig").splitlines(True))}
    by_module: dict[str, list[str]] = {}
    skipped = 0
    for path in sorted(SPECS.glob("*/*.json")):
        spec = json.loads(path.read_text(encoding="utf-8"))
        r = rows[spec["no"]]
        v, _, _ = verdict(spec["no"], r["분류"], " ".join(r["서식명"].split()), r["형식"])
        if v != "P3":
            continue
        code = build(spec)
        if code is None:
            skipped += 1
            continue
        by_module.setdefault(P3_MODULE.get(r["분류"], "forms_etc"), []).append(code)

    total = 0
    for mod, blocks in sorted(by_module.items()):
        header = (f'"""하나은행 공개 서식 — 선언형 스펙 ({len(blocks)}종).\n\n'
                  "scripts/build_form_specs.py 가 add_template/field_specs/ 에서 생성한다.\n"
                  "직접 고치지 말고 생성 스크립트의 라벨 표를 고칠 것.\n"
                  "서식 하나를 수제 템플릿으로 승격할 때는 여기서 해당 FORM 을 지운다.\n"
                  '"""\n'
                  "from ..formspec import FORM  # noqa: F401\n\n")
        (OUT / f"{mod}.py").write_text(header + "\n".join(blocks), encoding="utf-8")
        total += len(blocks)
        print(f"{mod:22s} {len(blocks):4d}종")
    print(f"\n합계 {total}종 (기재란이 없어 건너뜀 {skipped}종)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
