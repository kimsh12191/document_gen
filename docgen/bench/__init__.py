"""OCR·은행업무 벤치마크.

docgen 이 만드는 합성 서류로 고정된 평가 세트를 만들고(build), 모델을 돌리고(run), 채점한다(eval).

  python -m docgen.bench build --out bench_out                       평가 세트 만들기
  python -m docgen.bench run --bench bench_out --pred preds/my_model \\
         --base-url http://localhost:8000/v1 --model <모델>            OpenAI 호환 API 로 예측
  python -m docgen.bench eval --bench bench_out --pred preds/my_model   채점 (report.md, report.json)

과제 (tasks/<과제>.jsonl):
  [OCR]
    ocr_field    값 칸 잘라낸 이미지 → 글자 그대로          정확도·CER (인쇄체/손글씨, 깨끗/스캔/촬영/팩스)
    ocr_page     서류 전체 → 전체 글자 받아쓰기              값 재현율 (정답 값이 받아쓴 글에 들어 있는 비율)
  [문서 이해]
    classify     서류 → 서류명                              정확도
    kie          서류 + 항목 목록(키·키 설명) → 값 JSON         항목 정확도·F1 (타입별 정규화 비교)
    marks        서류 + 체크박스·도장·서명 목록 → 상태 JSON     항목 정확도

평가 세트의 고객 seed 는 학습용 기본 seed(0부터)와 겹치지 않게 1,000,000 이상을 쓴다.
"""
