"""은행 제출 서류 합성 데이터 생성기.

가상 고객으로 서류 476종(HTML 템플릿 70 + 하나은행 원본 서식 406)을 만들고 정답 라벨을 함께 낸다.
명령: python -m docgen (list·generate·check), python -m docgen.bench (은행 업무 평가 세트·학습 데이터),
python -m docgen.ocr_set (합성 OCR 세트). 안내는 docgen/README.md.
"""
