"""학습 실행 하나 — OCR·문서 이해·업무 처리 과제를 한 번에 (studio/DESIGN.md 17절, 옛 ocr/ 1부·bank/ 2부를 합침).

  python -m train --config train/configs/<이름>.json [--smoke | --dry-run | --from sft | --only report]

데이터는 studio 데이터셋(과제 폴더 docgen-tasks: meta.json + tasks/<과제>.jsonl)을 그대로 쓴다. 단계:
  prepare     데이터셋 섞기 (mix.py): 학습 SFT·GRPO 후보·평가 문항, 이미지 토큰 예산
  eval_base   출발 모델 평가 (GPU마다 vLLM 서버 하나)
  sft         SFT (launch.py → ms-swift)
  eval_sft    SFT 모델 평가, GRPO 후보 답 (골라 뽑기용)
  select      GRPO 문항 고르기 (mine · random · all)
  grpo        GRPO, 보상 = docgen.bench.evaluate.reward (reward_plugin.py)
  eval_grpo   GRPO 모델 평가
  report      reports/benchmark.{csv,md,html}
채점·보상은 모두 docgen.bench.evaluate (studio 평가와 같은 함수).
"""
