# temp

일회성·임시 스크립트를 두는 곳입니다. 파이프라인(`train/`, `docgen/`, `studio/`)은 이 폴더를 쓰지 않고, 테스트도 없습니다. 다 쓰면 지웁니다.

| 파일 | 하는 일 |
|---|---|
| `swift_to_kie_tmp.py` | swift 추출 `.jsonl`의 질문·답을 kie 꼴(한국어 질문, `{키: 값}` 객체 답)로 바꾼 새 `.jsonl`을 만듦. 키는 질문의 `in order: [...]`에서 자동으로 뽑음 |

```bash
python temp/swift_to_kie_tmp.py <입력.jsonl> <출력.jsonl>
```

- 원본은 고치지 않습니다. 바꿀 수 없는 줄은 건너뛰고 수를 알려 줍니다.
- 바꾼 파일을 평가 세트로 쓸 때도 `"format": "swift-fields"`로 넣습니다. 답이 `{키: 값}` 객체여도 기본 채점 함수(`train/scorers/swift_default.py`)가 읽습니다 ([guide/eval.md](../guide/eval.md#1-평가-세트-정하기)).
