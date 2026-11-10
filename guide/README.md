# 사용 설명서

하려는 일에 맞는 문서 하나를 끝까지 따릅니다. 처음이면 [start.md](start.md)(만들기 → 학습 → 결과를 한 번) 부터, 말 뜻은 [terms.md](terms.md)(용어 한 장).

## studio 에서 하는 일 (서식 · 새 서식 추가 · 데이터셋)

studio 화면 쓰는 법은 **[studio.md](studio.md)** 한 문서에 있습니다. 각 일의 자세한 것은 아래.

| 하려는 일 | 문서 |
|---|---|
| **서식** 보기·고치기·검수 (직접 또는 LLM 에게) | [서식 고치기](../docgen/forms/README.md) |
| **새 서식 추가** | [new-forms.md](new-forms.md) — 칸의 키 이름 [keys.md](keys.md), 고르기 창에 원하는 값이 없을 때 [generators.md](generators.md) |
| **데이터셋** 만들기 (평가 세트·학습 데이터, 레시피, 명령 `remote_build.py`) | [data.md](data.md) |
| 실서류 이미지로 OCR 데이터 | [ocr.md](ocr.md) |

## GPU 학습 서버에서 하는 일

| 하려는 일 | 문서 |
|---|---|
| 학습하기, 설정을 바꾼 모델 여러 개 | [training.md](training.md) |
| 평가 세트·채점 방식, 학습 없이 평가만, 다시 채점, 다른 모델을 API 로 평가 | [eval.md](eval.md) |
| 결과 보기·읽기 | [results.md](results.md) |
| 학습한 모델을 그림 한 장으로 써 보기 | [playground](../playground/README.md) |

agent 에게 맡길 때는 저장소 최상위의 [AGENTS.md](../AGENTS.md) 부터 읽게 하세요.

## 찾아보는 자료

| 궁금한 것 | 문서 |
|---|---|
| 서류 이름 → 서식 ID, 업무별 필수 서류 | [documents.md](documents.md) |
| 업무 12종의 서류·대조 사례·심사 규칙 | [catalog.md](catalog.md) (기계용 [catalog.json](catalog.json)) |
| 서식 하나의 칸·위치·질문→답 | 그 서식의 카드 `docgen/forms/<ID>/FORM.md` (studio 서식 › 개요 › 카드 원문) |
| 과제마다 묻는 것·답의 꼴·채점 규칙 | [benchmark.md](benchmark.md) |
| 질문 문장 원문 (모든 서식 공통 기본) | [questions.md](questions.md) |
| 모든 과제의 실제 문항 (그림·질문·정답) | [tasks.md](tasks.md) |
| 값 만드는 방법(생성 방법) 전체 목록 | [생성 방법 목록](../docgen/forms/_common/values.md) |
| 키 이름 규칙 전체, 모든 서식에 같은 것 | [docgen/forms/_common/README.md](../docgen/forms/_common/README.md) |
| 표가 있는 서식 점검 목록 | [table-audit.md](table-audit.md) |
| image/qa JSON 폴더 → ms-swift JSONL 변환 | [qa-to-swift.md](qa-to-swift.md) |

## 개발자

| | |
|---|---|
| 코드 구조 | [docgen/README.md](../docgen/README.md) (생성기) · [studio/README.md](../studio/README.md) (화면 ↔ 코드·저장 파일) · [studio/DESIGN.md](../studio/DESIGN.md) · [train/README.md](../train/README.md) |
| 설치·내부망 반입 | [docker/README.md](../docker/README.md) |
| html 서식 파일 형식 (코드로 고칠 때) | [NEW_FORM_SPEC.md](../docgen/manual/NEW_FORM_SPEC.md), 모양만 고치기 [FORM_SHELL_GUIDE.md](../docgen/manual/FORM_SHELL_GUIDE.md) |

자동 생성 문서(`tasks.md`, `documents.md`, `catalog.*`, `table-audit.md`, 서식 카드 `FORM.md`, `values.md`)는 손으로 고치지 않습니다. 다시 만드는 명령은 [docgen/README.md](../docgen/README.md) "문서 자동 생성".
