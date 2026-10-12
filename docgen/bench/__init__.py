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
    kie          서류 + 항목 목록(키·항목명) → 값 JSON         항목 정확도·F1 (타입별 정규화 비교)
    marks        서류 + 체크박스·도장·서명 목록 → 상태 JSON     항목 정확도
  [은행 업무] — 한 고객이 한 업무로 낸 서류 묶음
    doc_check    필수 서류 목록 + 제출 서류 첫 쪽들 → 빠진 서류·불필요 서류·타인 서류   완전 일치·F1
    cross_check  서류 2~3건 → 불일치 찾기 (불일치 사례 14종: 오기, 타인 서류, 금액, 임대인≠소유자,
                 재직기간 부풀리기, 업계약 … 과 표기만 다른 정상 문항, cases.py)  탐지·위치 정확도·오탐률
    review       심사 질문(LTV, 만 나이, 서류 유효기간, 합계 …) → 답   정확도 (숫자 허용오차)

평가 세트의 고객 seed 는 학습용 기본 seed(0부터)와 겹치지 않게 1,000,000 이상을 쓴다.
"""
