# 사용 설명서

하려는 일에 맞는 문서 하나를 끝까지 따릅니다. 처음이면 [start.md](start.md) 부터.

| 하려는 일 | 문서 |
|---|---|
| 처음부터 끝까지 한 번 (만들기 → 학습 → 결과) | [start.md](start.md) |
| 데이터셋 만들기 (평가 세트·학습 데이터) | [data.md](data.md) |
| 학습하기, 설정을 바꾼 모델 여러 개 | [training.md](training.md) |
| 평가 세트·채점 방식, 학습 없이 평가만, 다시 채점, 다른 모델을 API 로 평가 | [eval.md](eval.md) |
| 결과 보기·읽기 | [results.md](results.md) |
| 학습한 모델을 그림 한 장으로 써 보기 (GPU 고르기·모델 띄우기 화면) | [playground](../playground/README.md) |
| 서식 고치기 (직접 또는 LLM 에게) | [서식 고치기](../docgen/forms/README.md) |
| 새 서식 추가 | [new-forms.md](new-forms.md), 칸의 키 이름 [keys.md](keys.md) |
| 실서류 이미지로 OCR 데이터 | [ocr.md](ocr.md) |

agent 에게 맡길 때는 저장소 최상위의 [AGENTS.md](../AGENTS.md) 부터 읽게 하세요.

## 찾아보는 자료

| 궁금한 것 | 문서 |
|---|---|
| 서류 이름 → 서식 ID, 업무별 필수 서류 | [documents.md](documents.md) |
| 업무 12종의 서류·대조 사례·심사 규칙 | [catalog.md](catalog.md) (기계용 [catalog.json](catalog.json)) |
| 서식 하나의 칸·위치·질문→답 | 그 서식의 카드 `docgen/forms/<ID>/FORM.md` (studio 서식 › 카드) |
| 과제마다 묻는 것·답의 꼴·채점 규칙 | [benchmark.md](benchmark.md) |
| 질문 문장 원문 (모든 서식 공통 기본) | [questions.md](questions.md) |
| 모든 과제의 실제 문항 (그림·질문·정답) | [tasks.md](tasks.md) |
| 표가 있는 서식 점검 (행 수·순서·합계·번호 붙은 반복 칸) | [table-audit.md](table-audit.md) |
| 키 이름 규칙, 모든 서식에 같은 것 | [docgen/forms/_common/README.md](../docgen/forms/_common/README.md) |

## 문서 갱신 (개발자)

```bash
python -m studio.guidebook                              # catalog.md·catalog.json
python docgen/scripts/build_schema.py                   # fields/fields.json (studio 카탈로그의 재료)
python -m docgen list --markdown > guide/documents.md   # documents.md
bash guide/examples/make_examples.sh <작업 폴더> --docs   # tasks.md, examples/img/ (약 10분)
python -m docgen.formdir card --all --stale --workers 4 # 서식 카드 FORM.md
python -m docgen.bench.table_audit --workers 4 --out guide/table-audit.md   # 표 점검 목록 (약 5분)
```

`tasks.md`, `documents.md`, `fields/fields.json`, `catalog.*`, `FORM.md`, `table-audit.md` 는 자동 생성 파일이라 직접 고치지 않습니다.
