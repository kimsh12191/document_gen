# studio 데이터셋으로 학습하기

studio에서 만들거나 등록한 데이터셋을 학습(`train/`, `python -m train`)에 넣고, 학습 결과를 다시 studio에서 보는 방법이다. 설계는 [DESIGN.md 9.9·17절](DESIGN.md#17-ocr은행-업무-통합--과제-형식채점학습보기-하나로-2026-10-21).

- **학습은 하나다.** OCR·문서 이해·업무 처리 과제 데이터셋을 함께 골라 섞는다. 예전의 1부 OCR·2부 은행 업무 학습과 OCR replay·ocr_check 는 없어졌다(OCR 데이터셋을 학습·평가 목록에 그대로 넣는다).
- **데이터셋은 학습 코드가 그대로 읽는 폴더다.** 모든 데이터셋이 같은 과제 폴더 형식(`meta.json` + `tasks/<과제>.jsonl`)이라, 설정에 경로만 적는다.
- **두 컨테이너가 폴더를 공유한다.** studio는 docgen 컨테이너에서 띄우고([docker/README.md 4절](../docker/README.md#4-studio-띄우기-같은-컨테이너)), 학습은 따로 있는 학습 컨테이너에서 한다. studio가 만든 데이터셋은 공유 폴더에 둔다(설정의 `workspace_dir`, 예: `/out/studio_workspace`).
- 같은 폴더가 두 컨테이너에서 다른 경로로 보이면 studio 설정의 `path_map`에 적는다(예: `{"/out": "/share/me/docgen_data"}`). 학습 설정을 내보낼 때 studio가 학습 컨테이너 쪽 경로로 바꿔 쓴다.
- 처음부터 끝까지 명령줄로 하는 방법은 [guide/tutorial.md](../guide/tutorial.md), 학습 설정 칸은 [train/README.md](../train/README.md)에 있다.

## 전체 그림

```
docgen 컨테이너: studio ⑥ 데이터셋          학습 컨테이너: train/                       docgen 컨테이너: studio ⑦ 평가
──────────────────────────────────          ─────────────────────                         ──────────────────────────────
OCR 과제 데이터셋 (합성·실서류 OCR 준비) ┐
문서·업무 과제 데이터셋 (docgen.bench)    ├──▶ python -m train → runs/<실험>/    ───▶  답·점수 보기, 비교
라벨 있는 데이터·원본 데이터로           ┘      (섞기 → SFT → GRPO → 평가 → 비교표)
   "학습 설정 내보내기": 설정 파일 + 실행할 명령 한 줄      진행(state.json)을 읽어 보여 주고, 끝나면 결과를 평가 세트마다 자동으로 붙임
              (모두 공유 폴더를 거친다)
```

## 1. 데이터셋 고르기

⑥ 데이터셋 › 데이터셋 하나 › **학습** 탭에서 고른다.

| 칸 | 고르는 데이터셋 |
|---|---|
| 학습 데이터 | 학습 문항이 있는 데이터셋 (`docgen.bench --split train` 폴더, 학습용 OCR 준비 결과 등). 여러 개, 데이터셋마다 **문항 수**를 적으면 그만큼만 무작위로 (예: OCR 20000) |
| 평가 세트 | 평가 문항이 있는 데이터셋, **고정** 권장. 여러 개 (예: 은행 업무 평가 세트 + OCR 평가 세트). 학습용 OCR 준비 결과도 그 안의 평가 문서로 평가 세트가 될 수 있다 |

| 출처 | 정답 | 언제 쓰나 |
|---|---|---|
| 합성 (`docgen.bench`, `docgen.ocr_set`) | 생성 정답 (정확) | 기본. 실서류가 적은 서식을 보충할 때 |
| 이미지 묶음·결과 폴더 (사내 OCR) | 의사정답 | 실서류 OCR 학습 |
| OCR 검수·라벨 검수 | 사람이 고친 정답 | 사내 OCR·추론이 자주 틀리는 서식을 바로잡아 학습·평가할 때 |

- 같은 고객·문서가 학습과 평가에 함께 들어가면 학습의 준비 단계가 멈춘다.
- 문서·업무 과제는 학습 데이터와 평가 세트의 생성기 버전이 같아야 한다 (다르면 studio 가 경고).

## 2. 설정 만들기

**설정 미리보기**로 확인하고 **설정 파일 쓰기**를 누르면 `train/configs/studio-<이름>.json` 에 쓴다. 고른 칸만 채우고 나머지(모델 경로, GPU, `task_mix`, SFT·GRPO 설정)는 [train/configs/pipeline.example.json](../train/configs/pipeline.example.json) 값을 쓴다.

```jsonc
// train/configs/studio-exp1.json — studio 가 채우는 칸
{
  "workdir": "../runs/exp1",
  "data": {
    "train": [{"path": "/share/studio_workspace/datasets/bank-train-3.0"},
              {"path": "/share/studio_workspace/datasets/ocr-train/prepared", "count": 20000}],
    "benchmark": ["/share/studio_workspace/datasets/bank-bench-3.0", "/share/studio_workspace/datasets/ocr-bench/prepared"],
    "output_dir": "../data/mixed-exp1"
  }
}
```

- `data.output_dir`은 섞은 결과가 생기는 곳이다. 데이터셋이 바뀌면 **새 이름**으로 한다(이미 있으면 다시 섞지 않고 그대로 쓴다).
- 모델 경로(`model`)는 직접 확인한다.

## 3. 학습

studio가 보여 주는 명령을 학습 컨테이너의 저장소 최상위에서 실행한다.

```bash
python -m train --config train/configs/studio-exp1.json --smoke    # 리허설
nohup python -m train --config train/configs/studio-exp1.json > train-exp1.log 2>&1 &
```

## 4. 학습이 끝난 뒤

1. 학습하는 동안 studio의 데이터셋 화면(학습 기록)에 단계별 진행이 보인다(학습이 공유 폴더에 남기는 `state.json`). 학습 결과 폴더(`train/runs/<실험>/`)도 공유 폴더에 둔다.
2. 학습이 끝나면 studio가 결과 폴더를 고른 평가 세트마다 모델 답으로 붙인다. 명령줄로만 돌린 학습이면 ⑥ 데이터셋 › 모델 답 탭에서 결과 폴더를 직접 붙인다.
3. ⑦ 평가에서 모델별 점수(과제 묶음 OCR·문서 이해·업무 처리마다 표), ⑥ 문항 탭에서 문항마다 정답과 답, 틀린 것부터 보기를 본다. 점수는 학습의 `reports/*.json`과 같은 함수(`docgen.bench.evaluate`)로 낸다.
4. 내보낸 설정과 결과 폴더가 등록부의 학습 기록으로 이어진다. 데이터셋 설명서의 "이 데이터셋을 쓴 학습"에 그 학습이 생긴다.

## 확인 목록

- [ ] 데이터셋(`workspace_dir`)과 학습 결과(`train/runs/`)가 두 컨테이너가 함께 보는 공유 폴더에 있다
- [ ] `path_map`이 맞다 (첫 학습에서 내보낸 설정의 경로가 학습 컨테이너에 실제로 있는지 한 번 확인)
- [ ] 평가 세트는 고정했다
- [ ] 문서·업무 과제의 학습 데이터와 평가 세트의 생성기 버전이 같다
- [ ] 실서류 평가 세트에 쓴 결과 폴더가 학습 데이터에 들어가 있지 않다 (같은 문서 ID 는 학습이 막지만, 다른 이름으로 복사한 것은 모른다. DESIGN.md 13절)
- [ ] 섞은 결과 폴더(`data.output_dir`)는 새 이름이다
