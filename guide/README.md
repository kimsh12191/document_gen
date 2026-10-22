# 데이터 생성·사용 설명서

은행 서류 이미지, 추출 항목, 질문과 정답을 함께 만드는 프로젝트입니다. **Studio는 서식·필드·업무 시나리오를 관리하는 화면**, `docgen`은 생성기, `train`은 학습·평가 실행기입니다. 데이터만 필요한 사람이나 Research agent는 아래 순서대로 읽으면 됩니다.

## 이 순서로 사용하세요

| 순서 | 확인할 내용 | 설명서 | Studio에서 찾는 곳 |
|---|---|---|---|
| 1. 무엇을 만들까 | 연구 목적별 데이터·과제·조절 범위·한계 | [생성 가능 범위](research-agent.md) | 사용 가이드 → 생성 가능 범위 |
| 2. 어떤 서류·항목을 쓸까 | 전체 서류의 필드·문항 키·연결 업무·추출/비교 설정 | [서류·추출 카탈로그](catalog.md), [기계용 JSON](catalog.json) | 사용 가이드 → 서류·추출 카탈로그 / 서식 → 추출·시나리오 |
| 3. 어떻게 묻고 답할까 | 질문·정답·좌표 규격과 실제 예시 | [질문·정답](questions.md), [실제 데이터](tasks.md) | 서식 → 문항 Q/A / 시나리오·묶음 → 처리 설정 |
| 4. 어떻게 만들까 | 연결·목록 조회·레시피·생성·진행 확인 | [원격 생성](remote-build.md) | 데이터셋 → 새로 만들기 / 사용 가이드 → 원격 생성 |
| 5. 결과를 어떻게 쓸까 | 파일·경로·과제 선택·검증·변환 | [결과 가져오기](remote-build.md#6-결과), [검증 절차](research-agent.md#5-생성-결과를-연구에-가져가기) | 데이터셋 → 문항·묶음 |

Research agent에는 이 README부터 읽도록 안내하세요. 목적과 필요한 과제를 정하고 → 카탈로그에서 서류·필드를 선택하고 → 레시피로 소량 생성하고 → 이미지·정답을 확인한 뒤 본 데이터를 만듭니다. 결과를 사용하려면 서버 폴더 접근 또는 복사 경로도 필요합니다.

## 가장 작은 사용 예

이미 실행 중인 Studio가 있을 때 저장소 루트의 PowerShell에서:

```powershell
$env:STUDIO_URL = "http://<서버IP>:8765"
python docker/remote_build.py types --find 재직
python docker/remote_build.py catalog --form employment_certificate
python docker/remote_build.py build --name employment-pilot-001 --types employment_certificate --per-doc 2 --split train
python docker/remote_build.py paths
```

재직증명서 2건과 관련 문항을 만듭니다. 정보 추출만 필요하면 결과의 `tasks/kie.jsonl`과 참조 이미지를 사용합니다. `per_doc`은 문서 수이며 문항 수가 아닙니다. 서버 설치가 필요하면 [처음부터 따라하기](tutorial.md)를 읽으세요. 업무 묶음·OCR·JSON 레시피 예시는 [생성 가능 범위](research-agent.md), 연결과 오류 해결은 [원격 생성](remote-build.md)에 있습니다.

## Studio와 문서가 공유하는 내용

생성 구성을 업무·시나리오·정답 구조별로 확인하고 같은 구분으로 학습 평가 결과를 보려면 [벤치마크 구성·추적](benchmark-tracking.md)을 읽으세요. Studio에서는 **데이터셋 → 구성·추적**에서 확인합니다.

- **서식 → 추출·시나리오:** 원본 필드 키, 공통 문항 키, 항목명·타입·예시, 연결 업무와 추출/비교 설정을 확인합니다.
- **OCR 예시:** 데이터셋을 만들기 전에도 8개 OCR 과제의 입력 이미지·질문·정답·채점 기준을 함께 봅니다. [화면 사용법](ocr-examples.md), [동일한 원본 예시](tasks.md#ocr-과제)를 제공합니다.
- **서식 → 문항 Q/A:** 특정 고객 seed에서 실제 생성되는 질문과 정답을 확인합니다. 가능한 필드 목록과 실제 샘플의 값·문항은 다를 수 있습니다.
- **시나리오·묶음:** 필수 서류, 후보 서식, 직접 추출·비교할 필드와 기본 구비·대조·심사 설정을 보고 수정합니다.
- **사용 가이드:** 이 설명서와 생성 방법을 화면에서 읽고 현재 서류 카탈로그를 검색합니다.

[catalog.md](catalog.md)와 [catalog.json](catalog.json)은 등록부·필드 스키마·시나리오에서 생성한 스냅샷입니다. Studio의 `/api/guide/catalog`는 같은 코드로 현재 설정을 읽습니다. 설정 변경 후 저장소 문서도 공유하려면 아래 갱신 명령을 실행하세요. 필드 스키마가 오래되면 미수집·이전 항목이 있을 수 있으므로 실제 문항 Q/A도 확인합니다.

## 추가 설명이 필요할 때

| 궁금한 것 | 파일 |
|---|---|
| **Research agent가 필요한 데이터를 직접 선택·생성·사용하기** (생성 범위, 목적별 선택, 레시피, 결과 형식) | [research-agent.md](research-agent.md) |
| **처음부터 직접 돌려 보기** (설치, OCR 서버, 설정 파일, 실행, 확인, 에러 해결) | [tutorial.md](tutorial.md) |
| 이 프로젝트가 **무엇을 했는지** (팀 공유용 소개) | [overview.md](overview.md) |
| 발표 자료 (웹 슬라이드, 뒤쪽 부록에 모든 과제의 데이터 예시) | [slides/](slides/README.md) |
| **모든 과제의 실제 데이터** (이미지·질문 전문·정답·채점 정보·meta·학습 레코드, 서류 대조 사례 14종, 심사 질의 규칙 전부) | [tasks.md](tasks.md) (자동 생성) |
| 은행 업무를 모델에게 **어떻게 묻고**, 답이 **어떤 형식으로** 오나 | [questions.md](questions.md) |
| 글자·박스 읽기(OCR 과제)는 어떻게 묻나 | [tasks.md](tasks.md#ocr-과제) — 질문 문장 원본은 `docgen/bench/ocr_tasks.py`의 `PROMPTS` |
| 이 서류에서 **어떤 항목**을 뽑을 수 있나 (키·항목명·체크박스 보기) | [fields/](fields/README.md) — 서류 그룹별 파일 (자동 생성) |
| **서류 이름**과 **업무별 필수 서류** | [documents.md](documents.md) (자동 생성) |
| **벤치마크**는 무엇을 묻고 어떻게 채점하나 (과제, 문항 만드는 방법, 불일치 14종과 근거) | [benchmark.md](benchmark.md) |
| **가진 서류 이미지**로 OCR 학습·평가 데이터를 만들어 학습에 넣기 (`ocr_prepare`, 평가 전용 세트) | [ocr_prepare.md](ocr_prepare.md) |
| 파이프라인 **결과 지표**는 어떻게 읽나 (점수표, 학습 로그, 이상 신호) | [results.md](results.md) |

실행 방법의 원본: 학습 [studio/TRAINING.md](../studio/TRAINING.md)·[train/configs/pipeline.example.json](../train/configs/pipeline.example.json), 생성기 [docgen/README.md](../docgen/README.md), 화면 [studio/README.md](../studio/README.md), 도커 [docker/README.md](../docker/README.md).

## 과제 한눈에

| 과제 | 넣는 것 | 답 |
|---|---|---|
| 서류 구비 확인 `doc_check` | 제출 서류 첫 쪽들 + 업무·필수 서류 목록 | 빠진·불필요·타인 서류 JSON |
| 서류 대조 `cross_check` | 서류 2~3건 | 불일치 여부와 문제 서류·항목·값 JSON |
| 심사 질의 `review` | 관련 서류 + 질문 | 숫자 또는 예/아니오 |
| 정보 추출 `kie` | 서류 한 건 + 항목 목록 | 항목별 값과 위치 JSON 목록 (`bbox_2d`, `page`) |
| 체크·도장·서명 `marks` | 서류 한 건 + 항목·보기 | 체크된 보기, 도장·서명 true/false, 그 위치 |
| 서류 분류 `classify` | 서류 한 건 | 서류명 |
| 값 문자열 읽기 `ocr_page` | 서류 한 건 | 보이는 값 필드의 문자열 목록 (전체 페이지 전사는 OCR 경로) |
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
  - 평가·학습·studio가 같은 문장(`docgen/bench/prompts.py`)을 씁니다.
- **법인등기부 발급일:**
  - 발급용에만 발행일(`issue_date`)이 있고, 열람용은 열람일시(`viewed_at`)만 있습니다.
  - 발행일은 `서기 2025년 05월 19일` 꼴 그대로 채점합니다. 날짜 형식으로 비교하려면 `issue_date_short`를 쓰세요.
- **하나은행 원본 서식은 빈 칸이 많습니다.** 정보 추출 정답의 약 절반이 `null`입니다. F1(주 지표인 값+위치 F1도)은 빈 칸을 맞혀도 오르지 않아서 부풀지 않습니다.
- **아무렇게나 답해도 나오는 점수가 있습니다.**
  - 서류 대조: 항상 "문제없음"이라고 하면 약 63%
  - 심사 질의 예/아니오: 항상 "아니오"라고 하면 약 57%
  - 체크·도장·서명: 전부 비었다고 하면 약 40%
  - 그래서 점수는 세부 지표와 함께 보세요. → [results.md](results.md)

## 문서와 카탈로그 갱신

필드 구조를 바꿨다면 `python docgen/scripts/build_schema.py`로 필드 스키마를 먼저 갱신합니다. 시나리오·키 사전 설정만 바꿨다면 아래 카탈로그 갱신만 실행해도 됩니다.

```bash
python -m studio.guidebook                 # catalog.md·catalog.json 갱신
```

`tasks.md`, `documents.md`, `fields/`는 자동 생성 파일이라 직접 고치지 않습니다. 생성기 코드를 바꾸면 저장소 최상위에서 다시 만듭니다.

```bash
python docgen/scripts/build_schema.py                   # fields/ (약 1분)
python -m docgen list --markdown > guide/documents.md   # documents.md
bash guide/examples/make_examples.sh <작업 폴더> --docs   # tasks.md, examples/img/, 발표 부록 (약 10분)
```

`make_examples.sh`는 합성 서류 생성 → 사내 OCR 형식 JSON(`examples/labels_to_ocr.py`) → `scan`·OCR 준비(`docgen.bench.ocr_prepare`) → `docgen.bench build` → 과제별 예시 고르기(`examples/make_catalog.py`) → 부록 슬라이드(`slides/make_appendix.py`) 순서로 돌립니다. 명령과 바꾼 설정값이 스크립트 안에 그대로 있습니다.

`questions.md`의 질문 문장은 테스트(`docgen/tests/test_bench.py`)가 `docgen/bench/prompts.py`와 같은지 확인합니다.
