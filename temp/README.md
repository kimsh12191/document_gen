# temp

일회성·임시 스크립트를 두는 곳입니다. 파이프라인(`train/`, `docgen/`, `studio/`)은 이 폴더를 쓰지 않고, 테스트도 없습니다. 다 쓰면 지웁니다.

| 파일 | 하는 일 |
|---|---|
| `swift_to_kie_tmp.py` | swift 추출 `.jsonl`의 질문·답을 kie 꼴(한국어 질문, `{키: 값}` 객체 답)로 바꾼 새 `.jsonl`을 만듦. 키는 질문의 `in order: [...]`에서 자동으로 뽑음 |

```bash
python temp/swift_to_kie_tmp.py <입력.jsonl> <출력.jsonl>
```

- 원본은 고치지 않습니다. 바꿀 수 없는 줄은 건너뛰고 수를 알려 줍니다.
- 바꾼 파일을 평가 세트로 쓸 때는 `"format": "swift-fields"`에 채점 함수 [`train/scorers/swift_kie_scorer.py`](../train/scorers/swift_kie_scorer.py)를 붙입니다. 예시는 [`train/configs/pipeline.example.json`](../train/configs/pipeline.example.json)의 `real_po_kie`입니다.

  ```json
  {"id": "real_po_kie", "format": "swift-fields", "paths": ["<바꾼 .jsonl>"], "scorer": "../scorers/swift_kie_scorer.py:score"}
  ```

  경로는 설정 파일 기준입니다 (`train/configs/`에서는 `../scorers/…`). 채점 함수를 붙이지 않으면 `swift_default.py`로 채점합니다. 이 함수는 `{키: 값}` 답만 읽고, 값만 담은 배열 답은 형식 오류(0점)로 셉니다. 질문의 키 줄에서 순서를 읽는 `swift_kie_scorer.py`는 배열 답도 채점합니다.
