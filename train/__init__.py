"""학습·평가 (SFT 까지): python -m train … — 지도는 train/README.md.

  python -m train --config <학습 설정>      학습 실행 하나 (pipeline.py): 데이터 준비 → 출발 모델 평가 → SFT → SFT 평가 → 보고서
  python -m train sweep --config <묶음>     평가 세트를 고정하고 학습 설정을 바꾼 모델 여러 개 (sweep.py)
  python -m train eval --config <평가 설정>  학습 없이 모델 경로들을 평가 (evaluate.py)
  python -m train report <결과 폴더>         저장된 답으로 보고서 다시 (report.py)
채점은 모두 docgen.bench.evaluate (studio 와 같은 함수). 평가 세트·줄인 그림·모델 답은 cache_dir 에 두고 실험끼리 같이 쓴다.
"""
