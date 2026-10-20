# 모델 사용 가이드

학습한 모델을 쓰거나 결과를 해석할 때 필요한 정보를 모은 폴더입니다. 질문 방법, 서류별로 뽑을 수 있는 항목, 서류 목록, 벤치마크 설명이 들어 있습니다.

## 이럴 땐 이 파일

| 궁금한 것 | 파일 |
|---|---|
| **처음부터 직접 돌려 보기** (설치, OCR 서버, 설정 파일, 실행, 확인, 에러 해결) | [tutorial.md](tutorial.md) |
| 발표 자료 (웹 슬라이드, 뒤쪽 부록에 모든 과제의 데이터 예시) | [slides/](slides/README.md) |
| 이 프로젝트가 **무엇을 했는지** (팀 공유용 소개: OCR 학습과 은행 업무 학습 각각의 컨셉·데이터 구조·학습·평가·viewer, 생성기·벤치마크 상세 부록) | [overview.md](overview.md) |
| **모든 과제의 실제 데이터** (이미지·질문 전문·정답·채점 정보·meta·학습 레코드, 서류 대조 사례 14종, 심사 질의 규칙 전부) | [tasks.md](tasks.md) |
| 은행 업무를 모델에게 **어떻게 묻고**, 답이 **어떤 형식으로** 오나 | [questions.md](questions.md) |
| 글자·박스 읽기(OCR 과제)는 어떻게 묻나 | [ocr/docs/PROMPTS.md](../ocr/docs/PROMPTS.md) — OCR 브랜치와 같이 쓰는 파일이라 그 자리에 둡니다 |
| 이 서류에서 **어떤 항목**을 뽑을 수 있나 (키·항목명·체크박스 보기) | [fields/](fields/README.md) — 서류 그룹별 파일 |
| 학습한 **서류 이름** 476종, **업무별 필수 서류** | [documents.md](documents.md) |
| **벤치마크**는 무엇을 묻고 어떻게 채점하나 | [benchmark.md](benchmark.md) |
| 파이프라인 **결과 지표**는 어떻게 읽나 (점수표, 학습 로그, 이상 신호) | [results.md](results.md) |

## 과제 한눈에

| 과제 | 넣는 것 | 답 |
|---|---|---|
| 서류 구비 확인 `doc_check` | 제출 서류 첫 쪽들 + 업무·필수 서류 목록 | 빠진·불필요·타인 서류 JSON |
| 서류 대조 `cross_check` | 서류 2~3건 | 불일치 여부와 문제 서류·항목·값 JSON |
| 심사 질의 `review` | 관련 서류 + 질문 | 숫자 또는 예/아니오 |
| 정보 추출 `kie` | 서류 한 건 + 항목 목록 | 항목별 값 JSON |
| 체크·도장·서명 `marks` | 서류 한 건 + 항목·보기 | 체크된 보기, 도장·서명 true/false |
| 서류 분류 `classify` | 서류 한 건 | 서류명 |
| 전체 받아쓰기 `ocr_page` | 서류 한 건 | 글자 |
| 값 칸 읽기 `ocr_field` | 잘라낸 값 칸 | 글자 |
| OCR 과제 8종 | 페이지·잘라낸 이미지 + 좌표나 글자 | 글자 또는 `[{"bbox_2d": …, "label": …}]` |

## 자주 찾는 서류

| 서류 | 항목 목록 | 자주 쓰는 키 |
|---|---|---|
| 사업자등록증 (개인 / 법인) | [business.md](fields/business.md) | 개인: `biz_no`, `trade_name`, `name`, `address`, `opened`<br>법인: `biz_no`, `corp_name`, `ceo`, `address`, `opened` |
| 법인 등기사항전부증명서 | [corporate.md](fields/corporate.md) | `company_name`, `corp_reg_no`, `head_office`, `officers.0.name`, 발급일 `issue_date`(발급용) / `viewed_at`(열람용) |
| 법인인감증명서 | [corporate.md](fields/corporate.md) | `company_name`, `rep_name`, `issue_date` |
| 인감증명서 (개인) | [identity.md](fields/identity.md) | `person.name`, `person.address`, `issue_date` |
| 주민등록증 | [identity.md](fields/identity.md) | `name`, `rrn`, `address`, `issue_date` |
| 대출거래신청서 | [bank_form.md](fields/bank_form.md) | `applicant.name`, `loan.amount`, `apply_date` |

## 알아 둘 점

- **같은 질문 문장으로 물으세요.**
  - 모델은 [questions.md](questions.md)의 문장으로 학습했습니다.
  - 문장을 바꾸면 답 형식이 흐트러질 수 있습니다.
  - viewer의 직접 테스트가 같은 문장을 씁니다.
- **법인등기부 발급일:**
  - 발급용에만 발행일(`issue_date`)이 있고, 열람용은 열람일시(`viewed_at`)만 있습니다.
  - 발행일은 `서기 2025년 05월 19일` 꼴 그대로 채점합니다. 날짜 형식으로 비교하려면 `issue_date_short`를 쓰세요.
- **하나은행 원본 서식은 빈 칸이 많습니다.** 정보 추출 정답의 약 절반이 `null`입니다. 주 지표인 F1은 빈 칸을 맞혀도 오르지 않아서 부풀지 않습니다.
- **아무렇게나 답해도 나오는 점수가 있습니다.**
  - 서류 대조: 항상 "문제없음"이라고 하면 약 63%
  - 심사 질의 예/아니오: 항상 "아니오"라고 하면 약 57%
  - 체크·도장·서명: 전부 비었다고 하면 약 40%
  - 그래서 점수는 세부 지표와 함께 보세요. → [results.md](results.md)

## 다시 만들기

생성기 코드를 바꾸면 자동 생성 파일을 다시 만듭니다.

```bash
python docgen/scripts/build_schema.py                          # fields/ (약 1분)
python -m docgen list --markdown > guide/documents.md   # documents.md
bash guide/examples/make_examples.sh <작업 폴더> --docs   # tasks.md, examples/img/, 발표 부록 (약 10분)
```

`make_examples.sh`는 합성 서류 생성 → 사내 OCR 형식 JSON(`examples/labels_to_ocr.py`) → `bank_ocr scan`·`prepare` → `docgen.bench build` → 과제별 예시 고르기(`examples/make_catalog.py`) → 부록 슬라이드(`slides/make_appendix.py`) 순서로 돌립니다. 명령과 바꾼 설정값이 스크립트 안에 그대로 있습니다.

`questions.md`의 질문 문장은 테스트(`bank/tests/test_bank_task.py`)가 `docgen/bench/prompts.py`와 같은지 확인합니다.
