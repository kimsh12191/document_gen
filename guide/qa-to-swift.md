# image/qa JSON 폴더를 ms-swift JSONL로 변환

외부 패키지 없이 Python 표준 라이브러리만 사용합니다. 원본은 읽기만 하며 기존 출력 파일이 있으면 중단합니다.

입력 파일 하나의 구조:

```json
{"image": "data/images/first_masking_1/example.png", "qa": [{"question": "질문", "answer": "답"}, {"question": "항목들을 추출하세요.", "answer": {"항목": "값"}}]}
```

저장소 최상위에서 실행:

```bash
python -m train.qa_to_swift \
  <작업 폴더>/vqa/first_masking_1 \
  <작업 폴더>/first_masking_1_swift.jsonl \
  --image-root <작업 폴더> \
  --check-images
```

`--image-root`는 입력의 `data/images/...`가 실제로 들어 있는 기준 폴더로 바꾸세요. 위 예는 이미지가 `<작업 폴더>/data/images/...`에 있을 때입니다. 절대 경로 이미지는 기준 폴더를 붙이지 않습니다. 해당 서버의 Python으로 실행해야 서버 절대 경로를 올바르게 만들 수 있습니다.

스크립트 파일만 서버에 복사한 경우 `python qa_to_swift.py <입력폴더> <새출력.jsonl> ...`로도 실행할 수 있습니다.

- QA 한 쌍당 한 줄을 만듭니다. 파일명 순서와 각 파일의 QA 순서를 유지합니다.
- 질문은 앞에 `<image>`만 붙이고 보존합니다. 이미 태그가 하나 있으면 그대로 둡니다.
- 문자열 답은 그대로, 객체·배열·숫자·불리언·null 답은 JSON 문자열로 넣습니다. 항목명이나 답 구조를 key/value 목록으로 바꾸지 않습니다.
- `--image-root`를 생략하면 입력 이미지 경로를 유지합니다. 상대 경로를 쓸 경우 출력 JSONL 위치를 기준으로 이미지에 접근할 수 있어야 합니다. `--check-images`도 이 기준으로 검사합니다.
- 하위 폴더도 포함하려면 `--recursive`를 붙입니다. 기본은 해당 폴더의 `*.json`만 읽습니다.
- 잘못된 JSON·필수 필드 누락 시 파일명과 오류를 출력하고 중단하며, 이번 실행의 불완전 출력은 삭제합니다. 파일을 조용히 건너뛰지 않습니다.

출력 한 줄의 구조:

```json
{"messages": [{"role": "user", "content": "<image>항목들을 추출하세요."}, {"role": "assistant", "content": "{\"항목\": \"값\"}"}], "images": ["<작업 폴더>/data/images/first_masking_1/example.png"]}
```

이 명령은 변환만 수행하며 학습·평가나 데이터 분할은 하지 않습니다.

## Pipeline 채점 함수 연결

이 데이터에는 `train/scorers/vqa_scorer.py:score`를 붙입니다. 기본 `swift_default.py`는 일반 문자열과 필드 순서 없는 배열 정답을 처리하지 못합니다.

`train/configs/` 아래 pipeline JSON의 `data.benchmark`에 아래 항목을 추가하세요 (이름과 경로는 실제 평가 세트에 맞게 변경).

```json
{
  "id": "real_vqa_first_masking_1",
  "name": "실서류 VQA first_masking_1",
  "group": "real",
  "format": "swift-fields",
  "paths": ["<작업 폴더>/first_masking_1_swift.jsonl"],
  "scorer": "../scorers/vqa_scorer.py:score"
}
```

별도로 분리된 **학습용** JSONL을 `data.train`에 넣을 때도 같은 scorer를 지정합니다. 위 평가 파일이나 같은 이미지에서 나온 QA는 학습에 넣지 않습니다.

```json
{
  "path": "/path/to/separate_train_swift.jsonl",
  "format": "swift-fields",
  "scorer": "../scorers/vqa_scorer.py:score"
}
```

- 문자열: Unicode NFC·앞뒤/연속 공백만 정규화합니다. 대소문자·숫자·문장부호·마스킹 표기는 구분합니다.
- 객체: 키별 비교, 키 순서는 무시합니다. 배열: 인덱스별 비교, 순서와 중복을 유지합니다. 중첩 구조도 비교합니다.
- 주 지표 `f1`: 말단 경로와 값·타입이 맞은 수로 정밀도/재현율을 계산합니다. 누락은 재현율, 추가 답은 정밀도에 감점합니다. 빈 객체·배열·null도 별개 값으로 비교합니다.
- `doc_exact`: 정규화 후 문항 전체 일치. `field_acc`: 정답 말단 중 맞은 비율. `field_exact`: 공백 정규화 전 맞은 말단 비율.
- JSON 답변을 요구하는 문항에서 JSON 파싱에 실패하면 0점과 `parse_fail`을 기록합니다. JSON 코드 블록은 허용합니다. 설명 문장에서 JSON 일부만 추출하지 않습니다.
- JSON으로 해석 가능한 문자열 답(예: `123`, `null`)은 변환 결과만으로 원래 타입을 구별할 수 없어 JSON 값으로 채점합니다. 일반 텍스트 답은 텍스트로 채점합니다.
- 이 scorer는 정답 자체를 넣었을 때 만점인지 확인하는 학습 데이터 검사와 GRPO 보상에도 사용됩니다.
