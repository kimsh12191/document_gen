# temp

일회성으로 시작한 변환 스크립트 모음입니다. 파이프라인 코드(`train/`, `docgen/`, `studio/`)는 이 폴더를 불러오지 않고 테스트도 없지만, **실서류 평가 세트 변환**([guide/train/sweep.md 2절](../guide/train/sweep.md#2-평가-세트-databenchmark)의 채점 견본 `swift_kie_scorer.py`·`kie_list_scorer.py`)이 아래 스크립트로 만든 파일을 전제로 하므로 지우지 않습니다.

| 파일 | 하는 일 |
|---|---|
| `swift_to_kie_tmp.py` | swift 추출 `.jsonl`의 질문·답을 kie 꼴(한국어 질문, `{키: 값}` 객체 답)로 바꾼 새 `.jsonl`을 만듦. 키는 질문의 `in order: [...]`에서 자동으로 뽑음 |
| `swift_to_kie_v3_tmp.py` | v3: **합성 kie 와 같은 꼴**로 바꿈. 질문은 `docgen/bench/prompts.py` 의 `P_KIE` 그대로 + `- 키: 항목명`, 정답은 `[{"key", "value"}]` 목록 (위치 없음), 항목 40개마다 나눔. 채점 `train/scorers/kie_list_scorer.py` (합성과 같은 값 채점, 주 지표 f1) |
| `pairs_to_swift_kie_tmp.py` | 그림 + 라벨 json 쌍 폴더(`007009.jpg` ↔ `007009.json`, `{항목명: 값}`)를 ms-swift `.jsonl`로. 정답은 v3 와 같은 `[{"key", "value"}]` 목록, 빈 값은 null, 항목 40개마다 나눔. 질문은 기본 값만 묻는 문장(`--prompt value`, 학습용), `--prompt synthetic` 이면 v3 와 같은 `P_KIE` |
| `swift_to_kie_v2_tmp.py` | v2: 질문 문장만 고쳐 다시 씀 (그림·정답 그대로). 답 꼴 예시를 그 문항의 실제 키로(`{"HSCODE": "…", …}`, 예시 베끼기 방지), 키 옆에 한국어 항목명(`--labels` 표). 입력은 v1 변환본이나 swift 원본 |

```bash
python temp/swift_to_kie_tmp.py <입력.jsonl> <출력.jsonl>

# v2: 키 목록 → 항목명 표 채우기 → 변환
python temp/swift_to_kie_v2_tmp.py keys <eval_qa_PO_kie.jsonl> <eval_qa_BL_kie.jsonl> > labels.json   # 값 칸에 한국어 항목명
python temp/swift_to_kie_v2_tmp.py convert <eval_qa_PO_kie.jsonl> <eval_qa_PO_kie_v2.jsonl> --labels labels.json
```

- v2 는 평가 세트를 새 `id` 로 넣습니다 (예: `real-fx-po-v2`). 질문이 바뀌면 v1 점수와 같은 시험이 아닙니다. 채점 함수는 v1 과 같은 `swift_kie_scorer.py`.
- `--labels` 없이 돌리면 항목명은 `-` 그대로이고 답 꼴 예시만 바뀝니다.

```bash
# v3: 합성 kie 와 같은 꼴 (항목명 표는 v2 와 같은 labels.json)
python temp/swift_to_kie_v3_tmp.py convert <eval_qa_PO_kie.jsonl> <eval_qa_PO_kie_v3.jsonl> --labels labels.json
```

```json
{"id": "real-fx-po-v3", "format": "swift-fields", "gt": "reviewed", "paths": ["<eval_qa_PO_kie_v3.jsonl>"], "scorer": "../scorers/kie_list_scorer.py:score"}
```

- 원본은 고치지 않습니다. 바꿀 수 없는 줄은 건너뛰고 수를 알려 줍니다.
- v1·v2로 바꾼 파일을 평가 세트로 쓸 때는 `"format": "swift-fields"`에 채점 함수 [`train/scorers/swift_kie_scorer.py`](../train/scorers/swift_kie_scorer.py)를 붙입니다. 예시는 [`train/configs/pipeline.example.json`](../train/configs/pipeline.example.json)의 `real_po_kie`입니다.

  ```json
  {"id": "real_po_kie", "format": "swift-fields", "paths": ["<바꾼 .jsonl>"], "scorer": "../scorers/swift_kie_scorer.py:score"}
  ```

  경로는 설정 파일 기준입니다 (`train/configs/`에서는 `../scorers/…`). 채점 함수를 붙이지 않으면 `swift_default.py`로 채점합니다. 이 함수는 `{키: 값}` 답만 읽고, 값만 담은 배열 답은 형식 오류(0점)로 셉니다. 질문의 키 줄에서 순서를 읽는 `swift_kie_scorer.py`는 배열 답도 채점합니다.

```bash
# 그림 + 라벨 json 쌍 폴더 → swift .jsonl (하위 폴더까지는 --recursive)
python temp/pairs_to_swift_kie_tmp.py <폴더> <출력.jsonl>
python temp/pairs_to_swift_kie_tmp.py keys <폴더> > labels.json   # 키에 항목명을 따로 붙일 때만 (--labels labels.json)
```
