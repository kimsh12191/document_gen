# E01_add-realocr

| 항목 | 내용 |
|---|---|
| 상태 | 진행 (2026-10-23 시작) |
| 기간 | 2026-10-23 ~ |
| 담당 | |
| 묶음 파일 | `train/configs/E01_add-realocr.json` (base `train/configs/pipeline.json`) |
| 결과 폴더 | `train/runs/E01_add-realocr/` — 비교표 `compare.md`·`compare.html`, 진행 `python -m train sweep --config train/configs/E01_add-realocr.json --status` |

## 무엇을 보려는 실험인가

합성 데이터로 학습한 기준 모델에 **실서류 OCR 데이터를 도메인 하나씩 더해 가며** 실서류 성능이 어떻게 바뀌는지 봅니다.
검사부 1차와 2차는 **서로 다른 도메인**입니다. 외환(매입추심·BL) 추출은 학습 어디에도 없는 도메인입니다.

| # | 질문 | 비교 | 평가 세트 |
|---|---|---|---|
| 1 | 합성 데이터만으로 실서류 성능이 좋아지나 | `a1` vs 출발 모델 | 실서류 4개 |
| 2 | 다른 도메인의 OCR을 학습하면 (학습에 없는 도메인의) 추출이 좋아지나 | `a2`·`a3` vs `a1` | `real-fx-po`, `real-fx-bl` |
| 3a | 같은 도메인 OCR이 좋아지나 | `a2` vs `a1` | 검사부 1차 |
|  |  | `a3` vs `a2` | 검사부 2차 |
| 3b | 다른 도메인 OCR이 좋아지나 | `a2` vs `a1` | 검사부 2차 (a2 는 1차 도메인만 학습) |
| 3c | 도메인을 하나 더 넣으면 기존 도메인이 떨어지나 | `a3` vs `a2` | 검사부 1차 |
| 부가 | 합성 학습에서 하나은행 서식을 모두 뺐을 때 하나은행 서식 성능 (처음 보는 서식) | 모든 모델 | `bank_synthetic_v1`의 서식 그룹별 점수 (`slices.group`) |

## 설계

경로 앞부분: studio 데이터셋 `/database/docgen_studio/workspace/datasets/` (= `DS/`), 실서류 `/share/tom/env/2026_PROJECT/PT/docgen_studio/data/` (= `REAL/`).

| 모델 (`label`) | 설명 | 학습 데이터 |
|---|---|---|
| (출발 모델) | Qwen3.5-9B, 학습 없음 | — |
| `a1-syn` | 기준: 합성 업무·OCR (하나은행 서식 제외), 실서류 없음 | `DS/bank-train-part-v1-2026-10-23`, `DS/ocr-train-part-v1-2026-10-23/prepared` |
| `a2-syn-real1` | 기준 + 검사부 1차 실서류 OCR | a1 + `REAL/ocr-first-300` |
| `a3-syn-real1-2` | 기준 + 검사부 1차·2차 실서류 OCR | a1 + `REAL/ocr-first-300` + `REAL/ocr-second-300` |

| 평가 세트 (`id`) | 이름 | 경로 | 정답 |
|---|---|---|---|
| `bank_synthetic_v1` | 합성 문서·은행 업무 (전체 서식, 하나은행 포함) | `DS/bank-bench-2026-10-22` | 생성 정답 |
| `ocr_synthetic_v1` | 합성 OCR (전체 서식) | `DS/ocr-bench-2026-10-23/prepared` | 생성 정답 |
| `ocr_real_first_inspect_v1` | 실문서 OCR (검사부 1차 마스킹) | `REAL/ocr-first-300-eval` | 사내 OCR |
| `ocr_real_second_inspect_v1` | 실문서 OCR (검사부 2차 마스킹) | `REAL/ocr-second-300-eval` | 사내 OCR |
| `real-fx-po` | 실서류 매입추심 추출 (swift) | `REAL/FE_eval/eval_qa_PO.jsonl` | 사람 검수 |
| `real-fx-bl` | 실서류 BL 추출 (swift) | `REAL/FE_eval/eval_qa_BL.jsonl` | 사람 검수 |

- 같게 둔 것: 출발 모델, SFT 설정(`sft.yaml`), seed, `sft_max_examples` 20000, `task_mix`, 평가 세트 6개, GPU 7번 1장.
- `part`: `sft` (GRPO 없음). 출발 모델 평가는 `a1-syn`에서 한 번.
- 판단 기준: (정할 것)

## 실행

| 모델 | workdir | 시작 | 끝 | 비고 |
|---|---|---|---|---|
| `a1-syn` | `train/runs/E01_add-realocr/a1-syn` | 2026-10-23 | | |
| `a2-syn-real1` | `train/runs/E01_add-realocr/a2-syn-real1` | | | |
| `a3-syn-real1-2` | `train/runs/E01_add-realocr/a3-syn-real1-2` | | | |

## 결과

(`train/runs/E01_add-realocr/compare.md`에서 옮김)

## 해석

## 다음

- 실서류 OCR을 "더한" 효과와 "합성 OCR 일부를 바꾼" 효과를 나누려면: `sft_max_examples`를 올리거나, 실서류 문항 수를 `count`로 맞춘 모델을 추가.
- 외환 도메인의 OCR만 학습(추출 정답 없이)했을 때 외환 추출이 오르는지 (예전 설계의 "대상 문서 OCR만 추가").
- 외환 실서류 OCR 평가 세트가 생기면 [eval.md](../guide/eval.md)로 다시 채점.

## 해석할 때 주의

- **"더하기"가 아니라 "바꾸기"에 가깝습니다.** SFT 문항 수 상한(20000)과 과제별 몫(`task_mix`) 안에서 섞으므로, 실서류 OCR을 넣으면 같은 OCR 과제(`bbox_ocr`, `grounding` 등)의 합성 문항이 그만큼 빠집니다. 모델마다 실제 구성은 `<root>/<label>/data/DONE.json`의 `counts.sft_rows_by_task`·`sources`에서 확인해 결과에 적습니다.
- **외환 추출은 영어 지시문**(`in order: [...]`, 값만 배열로)입니다. 합성 학습의 한국어 추출 질문과 형식이 달라, 점수가 낮으면 도메인 때문인지 질문 형식 때문인지가 섞입니다. 형식 오류율(보고서의 답 형식 오류 표)을 함께 봅니다.
- **검사부 OCR 평가의 정답은 사내 OCR 결과(의사정답)**입니다. 사내 OCR 과 비슷하게 읽을수록 점수가 높습니다.
- **추출 점수는 세 가지**: `field_acc`(띄어쓰기 등 표기 차이 허용), `f1`, `field_exact`(글자 그대로). 질문이 "적힌 그대로"를 요구하므로 `field_exact`도 봅니다.
- **평가에서 빠진 문항**: 그림 16장 초과(`<workdir>/benchmark_over_image_limit.jsonl`), swift 에서 읽지 못한 줄(`DONE.json`의 `sources.benchmark.<파일>.skipped`). 수를 결과에 적습니다.

## 확인할 것

- [ ] 학습 데이터에 하나은행 서식이 없는지 (업무 묶음 포함). 0이어야 합니다.
  ```bash
  python - <<'EOF'
  import json, re
  d = "/database/docgen_studio/workspace/datasets/bank-train-part-v1-2026-10-23"
  print("묶음 속 하나은행 서식", sum(len(re.findall(r'"doc_id": "h(?:f\d|ana_)', l)) for l in open(f"{d}/bundles.jsonl")))
  o = json.load(open("/database/docgen_studio/workspace/datasets/ocr-train-part-v1-2026-10-23/ocr_set.json"))
  print("OCR 빼는 서식", len(o.get("recipe", {}).get("exclude", [])))
  EOF
  ```
- [ ] 검사부 학습 폴더(`ocr-first-300`, `ocr-second-300`)와 평가 폴더(`-eval`)의 문서가 겹치지 않는지
- [ ] 판단 기준(몇 점 차이면 효과 있다고 볼지)
