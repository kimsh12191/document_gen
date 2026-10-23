# 사용 설명서

은행 서류 VLM을 학습·평가하기 위한 데이터를 만들고, 학습하고, 결과를 봅니다. 하려는 일에 맞는 문서 하나를 고르세요.

| 하려는 일 | 문서 |
|---|---|
| 서식 보기·고치기, 합성 데이터 만들기, 내 서류 넣기, 채점 | [studio.md](studio.md) |
| 내가 가진 이미지로 OCR 학습·평가 데이터 만들기 | [ocr.md](ocr.md) |
| 데이터셋을 모아 학습하기 | [training.md](training.md) |
| 학습 없이 평가만 다시 하기 (새 평가 세트) | [eval.md](eval.md) |
| 결과 점수표 읽기 | [results.md](results.md) |

agent에게 일을 맡길 때는 저장소 최상위의 [AGENTS.md](../AGENTS.md)부터 읽게 하세요. 절차는 [agent-workflow.md](agent-workflow.md)입니다.

## 흐름

```text
studio: 데이터셋 만들기 ─┐
                         ├─▶ 학습 서버: python -m train ─▶ 점수표 ─▶ studio에서 문항별 답 보기
학습 서버: 내 이미지 OCR ─┘
```

## 찾아보는 자료

| 궁금한 것 | 문서 |
|---|---|
| 서류별 추출 항목·연결 업무 | [catalog.md](catalog.md) (기계용 [catalog.json](catalog.json)) |
| 모델에게 묻는 질문 문장과 답 형식 | [questions.md](questions.md) |
| 모든 과제의 실제 데이터 예시 | [tasks.md](tasks.md) |
| 업무 과제·대조 사례·채점 규칙 | [benchmark.md](benchmark.md) |
| 업무·시나리오별 구성과 점수 추적 | [benchmark-tracking.md](benchmark-tracking.md) |
| 서류 이름, 업무별 필수 서류 | [documents.md](documents.md) |
| 서류별 항목 키·타입 | [fields/](fields/README.md) |
| 프로젝트 소개 (팀 공유용) | [overview.md](overview.md), 발표 자료 [slides/](slides/README.md) |

## 알아 둘 점

- **같은 질문 문장으로 물으세요.** 모델은 [questions.md](questions.md)의 문장으로 학습했습니다.
- **찍어도 나오는 점수가 있습니다.** 서류 대조는 항상 "문제없음"이라고 해도 약 60%. 점수는 [results.md](results.md)의 기준선과 함께 봅니다.
- **합성 데이터 점수는 실서류보다 높게 나옵니다.** 실서류 성능은 실서류 평가 세트로 따로 봅니다.

## 문서 갱신 (개발자)

```bash
python -m studio.guidebook                              # catalog.md·catalog.json
python docgen/scripts/build_schema.py                   # fields/
python -m docgen list --markdown > guide/documents.md   # documents.md
bash guide/examples/make_examples.sh <작업 폴더> --docs   # tasks.md, examples/img/, 발표 부록 (약 10분)
```

`tasks.md`, `documents.md`, `fields/`, `catalog.*`는 자동 생성 파일이라 직접 고치지 않습니다.
