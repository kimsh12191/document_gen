# document_gen: 은행 서류 VLM (OCR · 문서 이해)

은행 서류 이미지로 VLM(Qwen3.5-9B)에 **글자·위치 읽기**(OCR), **문서 이해**(분류·값 추출·체크·도장·서명·표)를
학습시키고, 고정한 평가 세트로 모델끼리 비교합니다.

## 이 저장소가 하는 일

실제 고객 서류는 학습에 쓸 수 없고, "이 칸의 값은 무엇이고 어디에 있나" 같은 정답을 사람이 다는 비용도 큽니다.
그래서 **서식 545종에 가짜 고객 값을 채워 서류 그림을 직접 그리고**, 그린 값과 잰 위치를 그대로 정답으로 씁니다. 정답은 사람이 적지 않습니다.
서식을 고치면 다음에 만드는 데이터도 그대로 따라 바뀝니다.

```text
서식 docgen/forms/<ID>/          데이터 만들기 (studio)                         학습·평가 (GPU 서버, python -m train)
  모양·칸·값·질문      ──►   서식 × 가짜 고객마다 그림 + 질문 + 정답   ──►   섞기 → SFT → GRPO → 평가 세트 채점
                              = 데이터셋 폴더 (평가 세트 / 학습 데이터)            → summary.html (모델끼리 점수표)
실서류 이미지·검수한 추출 데이터 ─────────────────────────────────────────►   같은 학습·평가에 함께
```

| 폴더 | 하는 일 | 어디서 실행 |
|---|---|---|
| [`docgen/`](docgen/README.md) | 서식별 합성 데이터 생성기. 서식(서식 하나 = 폴더 `docgen/forms/<ID>/` 하나), 문항 만들기, 채점 | studio 컨테이너 (생성), 학습 서버 (채점) |
| [`studio/`](guide/studio.md) | 웹 화면: **서식** 보기·고치기·검수, **새 서식 추가**, **데이터셋** 만들기. 사용법 [guide/studio.md](guide/studio.md), 개발 [studio/README.md](studio/README.md) | studio 도커 컨테이너 ([docker/README.md](docker/README.md)) |
| [`train/`](train/README.md) | `python -m train`: 데이터 섞기 → SFT → GRPO → 평가 → 비교표. 채점 함수 견본 `train/scorers/` | GPU 학습 서버 |
| [`playground/`](playground/README.md) | 웹 화면: GPU 를 보고 모델을 띄워, 그림 한 장에 벤치마크 질문이나 직접 쓴 질문을 물어 보기 | GPU 학습 서버 |
| [`guide/`](guide/README.md) | 사용 설명서 | |

문항 하나는 그림 + 질문 + 정답입니다. 예 (값 추출 `kie`):

```text
그림   대출거래신청서 (가짜 고객 김나우, 스캔한 것처럼 흔든 것)
질문   이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. …  - applicant.name: 성명  - loan.amount: 대출신청금액 …
정답   [{"key": "applicant.name", "value": "김나우", "bbox_2d": [264, 231, 384, 249], "page": 1}, …]
```

과제는 두 묶음이고, 모두 서류 한 건으로 묻습니다 (과제마다 질문·답·채점은 [guide/benchmark.md](guide/benchmark.md), 실제 문항은 [guide/tasks.md](guide/tasks.md)).

- **OCR:** 잘라낸 글자 읽기, 박스 안 글자, 글자 위치 찾기 등 8종 + 값 칸 읽기 `ocr_field`, 전체 받아쓰기 `ocr_page`
- **문서 이해:** 서류 분류 `classify`, 값·위치 추출 `kie`, 체크·도장·서명 `marks`, 표 `table`·`table_read`·`table_find`·`table_qa`, 기타 칸 정리 `freetext`, 서식 전용 질문 `form_qa`

## 누구시면 어디부터

| 누구 | 하는 일 | 먼저 읽을 것 |
|---|---|---|
| **처음 오신 분 · 관리자** | 무엇을 하는 저장소인지, 결과가 어떤지 | 이 문서 → [용어 한 장](guide/terms.md) → [결과 읽는 법](guide/results.md) |
| **studio 사용자** (서식 검수, 데이터셋 만들기) | 웹 화면에서 서식을 보고 고치고 검수, 데이터셋 만들기 | [studio 사용법](guide/studio.md) |
| **새 서식을 맡은 외주 개발자** | 서식 그림에서 새 서식을 만들어 넘기기 | [새 서식 추가](guide/new-forms.md) (맨 위 "외주 체크리스트") |
| **학습 담당** (GPU 서버) | 학습·평가 돌리고 결과 보고 | [처음부터 끝까지 한 번](guide/start.md) → [학습](guide/training.md) |
| **agent (LLM)** | 위 일을 맡아서 | [AGENTS.md](AGENTS.md) |
| **코드 개발자** | 생성기·studio·학습 코드 고치기 | [docgen/README.md](docgen/README.md) · [studio/README.md](studio/README.md) · [train/README.md](train/README.md) |
| **설치 담당** | 내부망 서버에 studio 컨테이너 띄우기 | [docker/README.md](docker/README.md) |

전체 문서 목록은 [guide/README.md](guide/README.md). 실험 기록 [experiments/](experiments/README.md), 지난 작업 기록 [archive/](archive/README.md).

## 알아 둘 점

- **평가 세트는 고정합니다.** 실험끼리 비교하려면 같은 평가 세트를 씁니다. 평가 세트와 같은 데이터를 학습에 넣지 않습니다 (섞기에서 멈춤).
- **채점은 한 곳입니다.** 평가 점수와 GRPO 보상이 같은 함수(`docgen/bench/evaluate.py`)입니다. 기준이 다른 세트만 `train/scorers/` 의 채점 함수를 붙입니다.
- **합성 데이터 점수는 실서류보다 높게 나옵니다.** 학습과 평가가 같은 생성기라 고객만 다르기 때문입니다. 실서류 성능은 검수한 실서류 평가 세트로 따로 봅니다.
- **찍어도 나오는 점수가 있습니다.** 체크·도장·서명은 전부 비었다고 해도 약 40%. 점수는 [results.md](guide/results.md) 의 기준선과 함께 봅니다.
- **실서류 이미지는 외부 모델·서비스에 보내지 않습니다.** 모든 합성 데이터는 실존 인물·사업자와 무관합니다.
