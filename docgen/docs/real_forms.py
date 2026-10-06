"""하나은행 공개 서식 — 원본 PDF 를 배경으로 쓰는 서식 전부 (docgen/realform.py).

add_template/layouts/ 에 레이아웃이 있는 서식이 모두 hf<No> 로 등록된다.
레이아웃은 scripts/extract_form_layout.py 가 PDF 에서 뽑는다.
"""
from ..realform import register_all

register_all()
