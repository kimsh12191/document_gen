# document_gen: 은행 서류 VLM (OCR · 문서 이해)

은행 서류 이미지로 VLM(Qwen3.5-9B)에 **글자·위치 읽기**(OCR)와 **문서 이해**(분류·값 추출·체크·도장·서명·표)를 학습시키고,
고정한 평가 세트로 모델끼리 비교합니다.

실서류는 학습에 쓸 수 없고 정답을 사람이 다는 비용도 큽니다. 그래서 **서식 545종에 가짜 고객 값을 채워 서류 그림을 직접 그리고**,
그린 값과 위치를 그대로 정답으로 씁니다.

## 흐름은 둘

```text
① studio (웹 화면, studio 컨테이너)                        ② 학습 (GPU 서버, python -m train)
  서식 보기·고치기·검수 · 새 서식 추가                          pipeline.json (평가 세트 고정) + sweep.json (모델마다 바꿀 것)
  → 데이터셋 만들기 (평가 세트 / 학습 데이터)   ──경로──►     → 모델마다 섞기 · SFT · 평가 → report.html · answers.html
                                         실서류 swift .jsonl · 실서류 OCR 준비 ──►
```

| 하는 사람 | 읽을 것 |
|---|---|
| ① studio 로 서식 검수·데이터셋 만들기 | [guide/studio/studio.md](guide/studio/studio.md) |
| ② 학습·평가 돌리고 결과 보기 | [guide/train/sweep.md](guide/train/sweep.md) |
| agent (LLM) 에게 맡길 때 | [AGENTS.md](AGENTS.md) |
| 설치 (내부망 서버에 studio 띄우기) | [docker/README.md](docker/README.md) |

문서 전체는 [guide/README.md](guide/README.md).

## 문항

문항 하나는 그림 + 질문 + 정답입니다. 예 (값 추출 `kie`):

```text
그림   대출거래신청서 (가짜 고객 김나우, 스캔한 것처럼 흔든 것)
질문   이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. …  - applicant.name: 성명  - loan.amount: 대출신청금액 …
정답   [{"key": "applicant.name", "value": "김나우", "bbox_2d": [264, 231, 384, 249], "page": 1}, …]
```

- **OCR:** 잘라낸 글자 읽기·박스 안 글자·글자 위치 찾기 등 8종, 값 칸 읽기 `ocr_field`, 전체 받아쓰기 `ocr_page`
- **문서 이해:** 분류 `classify`, 값·위치 추출 `kie`, 체크·도장·서명 `marks`, 표 `table`·`table_read`·`table_find`·`table_qa`, 기타 칸 정리 `freetext`, 서식 전용 질문 `form_qa`

과제마다 질문·답·채점은 [guide/reference/benchmark.md](guide/reference/benchmark.md).

## 폴더

| 폴더 | 하는 일 |
|---|---|
| `docgen/` | 합성 데이터 생성기. 서식 하나 = 폴더 `docgen/forms/<ID>/` 하나, 문항 만들기, 채점 ([개발 문서](docgen/README.md)) |
| `studio/` | 웹 화면 ([개발 문서](studio/README.md)) |
| `train/` | 학습·평가 (`python -m train`), 채점 함수 견본 `train/scorers/` ([코드 지도](train/README.md)) |
| `playground/` | 학습한 모델을 띄워 그림 한 장에 물어 보는 화면 ([README](playground/README.md)) |
| `formagent/` | 서식 이미지 → 서식 추가 에이전트: 사내 모델이 ReLab 으로 스킬 `form-from-image` 를 회차마다 돌림, `python -m formagent` ([사용법](formagent/README.md), [계획](formagent/PLAN.md)) |
| `guide/` | 사용 설명서 — `studio/`, `train/`, `reference/` |

## 알아 둘 점

- **평가 세트는 고정합니다.** 실험끼리 같은 평가 세트를 쓰고, 평가 세트와 같은 문서는 학습에 넣지 않습니다 (섞기에서 멈춤).
- **합성 세트 점수는 실서류보다 높게 나옵니다.** 실서류 성능은 검수한 실서류 평가 세트로 따로 봅니다.
- **실서류 이미지는 외부 모델·서비스에 보내지 않습니다.** 합성 데이터는 실존 인물·사업자와 무관합니다.
