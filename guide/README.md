# 사용 설명서

하려는 일의 문서 하나를 끝까지 따릅니다.

## studio — 웹 화면 (studio 컨테이너)

| 하려는 일 | 문서 |
|---|---|
| 화면 쓰는 법 (서식 보기·검수·고치기, 새 서식, 데이터셋) — 할 일별로 | [studio/studio.md](studio/studio.md) |
| 새 서식 추가 (그림 위에 칸 그리기) | [studio/new-forms.md](studio/new-forms.md) |
| 칸의 키 이름 정하기 | [studio/keys.md](studio/keys.md) |
| 원하는 값이 고르기 창에 없을 때 | [studio/generators.md](studio/generators.md) |
| 데이터셋 만들기 (레시피, 화면 없이 `remote_build.py`) | [studio/data.md](studio/data.md) |

이 다섯 문서는 studio **사용 가이드** 메뉴에서도 보입니다. html 서식(코드로 고치는 서식)은 [docgen/forms/README.md](../docgen/forms/README.md).

## train — 학습·평가 (GPU 학습 서버)

| 하려는 일 | 문서 |
|---|---|
| 실험 묶음(sweep)으로 학습·평가, 결과 보기 | [train/sweep.md](train/sweep.md) |
| 단계 하나씩 따로 · 학습 없이 평가만 · 보고서 다시 | [train/steps.md](train/steps.md) |
| 실서류 이미지로 OCR 데이터 준비 | [train/ocr.md](train/ocr.md) |

학습한 모델을 그림 한 장으로 써 보기는 [playground](../playground/README.md).

## reference — 찾아볼 때

| 궁금한 것 | 문서 |
|---|---|
| 말 뜻 | [reference/terms.md](reference/terms.md) |
| 과제마다 묻는 것·답의 꼴·채점 규칙·지표 | [reference/benchmark.md](reference/benchmark.md) |
| 질문 문장 원문 | [reference/questions.md](reference/questions.md) |
| 모든 과제의 실제 문항 (자동 생성) | [reference/tasks.md](reference/tasks.md) |
| 서류 이름 → 서식 ID (자동 생성) | [reference/documents.md](reference/documents.md) |
| 표가 있는 서식 점검 목록 (자동 생성) | [reference/table-audit.md](reference/table-audit.md) |

서식 하나의 칸·질문·답은 그 서식의 카드 `docgen/forms/<ID>/FORM.md` (studio 서식 › 개요 › 카드 원문).
자동 생성 문서는 손으로 고치지 않습니다 (다시 만드는 명령은 [docgen/README.md](../docgen/README.md)).
