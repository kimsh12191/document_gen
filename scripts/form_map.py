"""하나은행 공개 서식 441건 → docgen 템플릿 전수 분류 지도.

  python scripts/form_map.py > docs/FORM_MAP.md

입력
  add_template/하나은행_서식자료/다운로드_결과.csv   서식명·분류·원본 URL
  add_template/field_specs/<분류>/<No>.json          PDF 에서 뽑은 기재란 명세
                                                     (scripts/extract_form_fields.py)

판정
  기존   이미 만들어 둔 서류로 덮인다 (그 서류 ID 를 적는다)
  P1     1차 신규 구현 — 수제 템플릿
  P2     신규 그룹(퇴직연금·전자금융) 구현 — 수제 템플릿
  P3     선언형 폼 스펙으로 넣는다 (공용 템플릿이 렌더)
  제외   템플릿화 대상이 아님 (약관 전문, 안내 인쇄물, 은행 내부 점검표 등)

서식이 늘거나 판정을 바꾸려면 아래 표만 고치면 된다.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "add_template" / "하나은행_서식자료" / "다운로드_결과.csv"
SPECS = ROOT / "add_template" / "field_specs"

# ---------------------------------------------------------------------------
# 1) 이미 있는 서류로 덮이는 것 — No → (서류 ID, 비고)
# ---------------------------------------------------------------------------
MAPPED: dict[int, tuple[str, str]] = {
    2: ("account_opening_application", "영문 서식 변형"),
    3: ("account_opening_application", "하나은행의 계좌개설 서식 본체"),
    6: ("auto_transfer_application", ""),
    22: ("integrated_change_report", "영문 변형 — P1 서식과 같은 서식"),
    27: ("bank_power_of_attorney", "영문 변형 — P1 서식과 같은 서식"),
    47: ("loan_application", "보금자리론 상담·신청 변형"),
    48: ("loan_application", "가계형 소호 차입신청 변형"),
    49: ("loan_application", "가계 대출신청서 본체"),
    54: ("loan_application", "주택도시기금 가계 변형"),
    55: ("loan_application", "디딤돌 상담·신청 변형"),
    58: ("loan_application_corp", "기업 융자상담·차입신청 본체"),
    100: ("loan_application", "창구대출신청서 변형"),
    136: ("loan_application_corp", "한도 내 개별·분할실행 변형"),
    154: ("loan_application_corp", "무역금융 차입신청 변형"),
    199: ("overseas_remittance_application", "해외송금 본체"),
    413: ("corporate_customer_due_diligence", ""),
}

# 이름에 이 말이 들어가면 그 서류로 덮인다 (위의 No 지정이 우선).
MAPPED_KW: list[tuple[str, str, str]] = [
    ("FATCA", "fatca_crs", "FATCA/CRS 본인확인서 변형"),
    ("CRS", "fatca_crs", "FATCA/CRS 본인확인서 변형"),
    ("개인(신용)정보", "privacy_consent", "상품·용도별 동의서 변형 (문구만 다르다)"),
    ("신용정보 제공 동의", "privacy_consent", "동의서 변형"),
    ("금융거래정보 이용제공 동의", "privacy_consent", "동의서 변형"),
    ("금융거래정보이용제공동의", "privacy_consent", "동의서 변형"),
    ("고객정보 활용 동의", "privacy_consent", "동의서 변형"),
    ("금융거래 정보제공 동의", "privacy_consent", "동의서 변형"),
    ("기업가치 및 기업정보 제공활용 동의", "privacy_consent", "동의서 변형"),
    ("본인 행정정보 제공 요구서", "privacy_consent", "공공마이데이터 제공요구 — 동의서 변형"),
]

# ---------------------------------------------------------------------------
# 2) 1차 신규 구현 (P1) — No → (서류 ID, 서류명, 모듈)
# ---------------------------------------------------------------------------
P1: dict[int, tuple[str, str, str]] = {
    1: ("inheritance_deposit_claim", "상속예금 지급·명의변경 의뢰서", "bank_form_deposit"),
    11: ("balance_certificate_request", "예금(신탁)잔액증명 의뢰서", "bank_form_deposit"),
    15: ("integrated_change_report", "통합제신고서", "bank_form_deposit"),
    24: ("financial_info_disclosure", "금융거래정보제공(요구·동의)서", "bank_form_deposit"),
    25: ("safe_deposit_box_application", "대여금고 신규·변경·해지 신청서", "bank_form_deposit"),
    28: ("bank_power_of_attorney", "위임장(은행 거래용)", "bank_form_deposit"),
    51: ("loan_withdrawal_request", "대출계약 철회신청서", "bank_form_loan2"),
    61: ("suitability_check", "적합성·적정성 고객정보 확인서(개인)", "bank_form_loan2"),
    62: ("suitability_check_corp", "적합성·적정성 고객정보 확인서(법인)", "bank_form_loan2"),
    63: ("loan_product_description", "대출상품설명서(권유용)", "bank_form_loan2"),
}

# ---------------------------------------------------------------------------
# 3) 신규 그룹 구현 (P2) — No → (그룹, 서류 ID, 서류명)
# ---------------------------------------------------------------------------
P2: dict[int, tuple[str, str, str]] = {
    168: ("retirement", "default_option_designation", "퇴직연금 사전지정운용방법(디폴트옵션) 지정 신청서"),
    169: ("retirement", "dc_participant_application", "퇴직연금 가입자 거래신청서(DC·기업형IRP)"),
    171: ("retirement", "irp_account_application", "퇴직연금 거래신청서(개인형IRP)"),
    173: ("retirement", "investor_profile_retirement", "투자자확인서(퇴직연금용)"),
    177: ("retirement", "dc_product_selection", "퇴직연금 운용상품지정 신청서(DC)"),
    179: ("retirement", "retirement_benefit_claim", "퇴직연금 퇴직급여 지급신청서(DB)"),
    335: ("efinance", "sms_notice_application", "입출금 거래내역 문자통지서비스 신청서"),
    337: ("efinance", "efinance_application_personal", "개인 전자금융 서비스 신청서"),
    340: ("efinance", "efinance_application_corp", "기업 전자금융서비스 신청서(은행용)"),
    373: ("efinance", "electronic_note_issue", "전자어음 교부 신청서"),
}

# P2 서식의 영문·고객용 변형 (같은 서식이므로 '기존' 으로 덮는다)
MAPPED_P2_VARIANT: dict[int, tuple[str, str]] = {
    336: ("efinance/efinance_application_personal", "영문 변형"),
    338: ("efinance/efinance_application_corp", "영문 변형"),
    339: ("efinance/efinance_application_corp", "고객용 신청확인서 — 영문 변형"),
    341: ("efinance/efinance_application_corp", "고객용 신청확인서 변형"),
    361: ("efinance/efinance_application_personal", "고객용 신청확인서 변형"),
    170: ("retirement/dc_participant_application", "기업형IRP 계약이전 변형"),
    186: ("retirement/dc_participant_application", "DB 거래신청 변형"),
}

# ---------------------------------------------------------------------------
# 4) 템플릿화 대상이 아닌 것 — 이름에 이 말이 들어가면 제외
# ---------------------------------------------------------------------------
EXCLUDE_KW: list[tuple[str, str]] = [
    ("약관", "약관 전문 — 고객이 기재하는 항목이 없다"),
    ("안내장", "안내 인쇄물 — 기재란이 없다"),
    ("체크리스트", "은행 내부 점검표 — 고객 기재란이 없다"),
    ("일반위험고지문", "고지 인쇄물 — 기재란이 없다"),
    ("상품설명서", "상품 설명 인쇄물 (대출상품설명서는 P1 로 따로 만든다)"),
    ("중요내용 설명서", "설명 인쇄물"),
    ("환전장부", "영업점 장부 — 고객 서식이 아니다"),
    ("과목분류표", "내부 분류표"),
    ("관리대장", "영업점 관리대장 — 고객 서식이 아니다"),
    ("제출서류 목록", "서류 목록 인쇄물"),
]

EXCLUDE_NO: dict[int, str] = {
    12: "보이스피싱 피해 예방 안내 인쇄물",
    13: "금융거래 목적 확인 안내 인쇄물 (서식 본체는 financial_transaction_purpose 로 이미 있다)",
    14: "한도계좌 개설 안내 인쇄물",
    40: "고발장 — 은행이 수사기관에 내는 문서",
    57: "엑셀 계산 시트 — 서식이 아니다",
    143: "기업여신과목분류표 — 내부 분류표",
    187: "상품설명 인쇄물",
    200: "EXE(서식 뷰어 설치파일) — 서식 원본이 아니다",
    257: "영업점 장부",
    404: "고지 인쇄물",
}

# P3 를 넣을 스펙 모듈 (분류 → 모듈명)
P3_MODULE = {"외환": "forms_fx", "대출": "forms_loan", "예금": "forms_deposit",
             "전자금융": "forms_efinance", "퇴직연금": "forms_retirement",
             "파생상품": "forms_derivative", "신탁/ISA": "forms_trust", "펀드": "forms_trust",
             "기타": "forms_etc"}


def verdict(no: int, cls: str, name: str, fmt: str) -> tuple[str, str, str]:
    """(판정, 대상, 비고)"""
    if no in EXCLUDE_NO:
        return "제외", "", EXCLUDE_NO[no]
    if no in P1:
        doc_id, label, mod = P1[no]
        return "P1", f"bank_form/{doc_id}", f"{label} — {mod}.py"
    if no in P2:
        grp, doc_id, label = P2[no]
        return "P2", f"{grp}/{doc_id}", label
    if no in MAPPED:
        doc_id, note = MAPPED[no]
        return "기존", doc_id, note
    if no in MAPPED_P2_VARIANT:
        target, note = MAPPED_P2_VARIANT[no]
        return "기존", target, note
    for kw, reason in EXCLUDE_KW:
        if kw in name:
            return "제외", "", reason
    if fmt == "EXE":
        return "제외", "", "실행파일 — 서식 원본이 아니다"
    for kw, doc_id, note in MAPPED_KW:
        if kw in name:
            return "기존", doc_id, note
    note = f"{fmt} 원본 — 레이아웃 근거 확인 필요" if fmt in ("XLS", "DOC") else ""
    return "P3", P3_MODULE.get(cls, "forms_etc"), note


def load_spec(cls: str, no: int) -> dict | None:
    p = SPECS / cls / f"{no:03d}.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def main() -> None:
    rows = list(csv.DictReader(CSV.read_text(encoding="utf-8-sig").splitlines(True)))
    out: list[dict] = []
    for r in rows:
        no = int(r["No"])
        name = " ".join(r["서식명"].split())
        v, target, note = verdict(no, r["분류"], name, r["형식"])
        spec = load_spec(r["분류"], no)
        out.append({"no": no, "cls": r["분류"], "name": name, "fmt": r["형식"], "verdict": v,
                    "target": target, "note": note, "url": r["원본 URL"],
                    "n_fields": len(spec["fields"]) if spec else None,
                    "n_choices": len(spec["choices"]) if spec else None,
                    "pages": spec["pages"] if spec else None})

    cnt = Counter(x["verdict"] for x in out)
    by_cls: dict[str, Counter] = {}
    for x in out:
        by_cls.setdefault(x["cls"], Counter())[x["verdict"]] += 1
    have = [x for x in out if x["n_fields"] is not None]

    p = print
    p("# 하나은행 공개 서식 441건 — 템플릿 전수 분류 지도\n")
    p("`python scripts/form_map.py > docs/FORM_MAP.md` 로 자동 생성된다. "
      "판정 기준은 [scripts/form_map.py](../scripts/form_map.py) 안의 표에 있다.\n")
    p("원본은 `add_template/하나은행_서식자료/` (하나은행 홈페이지 공개 서식). "
      "'기재란'·'보기'·'쪽' 은 `scripts/extract_form_fields.py` 가 PDF 에서 뽑아 "
      "`add_template/field_specs/` 에 넣은 수치다 — 서식을 만들 때의 작업지시서가 된다.\n")

    p("## 판정 구분\n")
    p("| 판정 | 뜻 | 건수 |\n|---|---|---:|")
    for k, desc in [("기존", "이미 만들어 둔 서류로 덮인다 (문구·변형 차이만 있다)"),
                    ("P1", "1차 신규 구현 — 수제 템플릿"),
                    ("P2", "신규 그룹(퇴직연금·전자금융) 구현 — 수제 템플릿"),
                    ("P3", "선언형 폼 스펙으로 넣는다 (공용 템플릿이 렌더)"),
                    ("제외", "템플릿화 대상 아님 (약관 전문·안내 인쇄물·내부 점검표 등)")]:
        p(f"| **{k}** | {desc} | {cnt[k]} |")
    p(f"| | **합계** | **{len(out)}** |\n")

    p("## 분류별 판정\n")
    p("| 분류 | 기존 | P1 | P2 | P3 | 제외 | 합계 | P3 스펙 모듈 |\n|---|---:|---:|---:|---:|---:|---:|---|")
    for cls, c in by_cls.items():
        mod = P3_MODULE.get(cls, "forms_etc")
        p(f"| {cls} | {c['기존']} | {c['P1']} | {c['P2']} | {c['P3']} | {c['제외']} | {sum(c.values())} "
          f"| `{mod}.py` |")
    p(f"| **합계** | **{cnt['기존']}** | **{cnt['P1']}** | **{cnt['P2']}** | **{cnt['P3']}** "
      f"| **{cnt['제외']}** | **{len(out)}** | |\n")

    if have:
        tot_f = sum(x["n_fields"] for x in have)
        p(f"기재란 추출: {len(have)}건에서 총 {tot_f}개 (서식당 평균 {tot_f / len(have):.1f}개)\n")

    p("## 1차 구현 대상 (P1 · P2)\n")
    p("| No | 판정 | 서식명 | 만들 서류 | 쪽 | 기재란 | 비고 |\n|---:|---|---|---|---:|---:|---|")
    for x in out:
        if x["verdict"] in ("P1", "P2"):
            p(f"| {x['no']} | {x['verdict']} | {x['name']} | `{x['target']}` | "
              f"{x['pages'] or ''} | {x['n_fields'] if x['n_fields'] is not None else ''} | {x['note']} |")
    p("")

    p("## 전체 목록\n")
    for cls in by_cls:
        items = [x for x in out if x["cls"] == cls]
        p(f"### {cls} ({len(items)}건)\n")
        p("| No | 서식명 | 형식 | 쪽 | 기재란 | 보기 | 판정 | 대상 | 비고 |\n"
          "|---:|---|---|---:|---:|---:|---|---|---|")
        for x in items:
            t = f"`{x['target']}`" if x["target"] else ""
            p(f"| {x['no']} | [{x['name']}]({x['url']}) | {x['fmt']} | {x['pages'] or ''} | "
              f"{x['n_fields'] if x['n_fields'] is not None else ''} | "
              f"{x['n_choices'] if x['n_choices'] is not None else ''} | "
              f"{x['verdict']} | {t} | {x['note']} |")
        p("")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
