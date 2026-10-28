"""ocr_page — 전체 받아쓰기. 서류 한 건의 모든 쪽을 보고 보이는 글자를 전부 옮긴다.

질문: P_OCR_PAGE (고정 문장)
정답: 그림에 보이는 칸 값의 줄 목록 (doc.visible 의 값을 줄바꿈으로 나눠, 같은 줄은 한 번). 고정 인쇄 문구는 정답에 없다 —
      모델은 전체를 받아쓰고, 채점은 이 값 줄들을 얼마나 찾았는지 본다. 보이는 값이 하나도 없으면 문항을 만들지 않는다
채점: evaluate.s_ocr_page, 주 지표 recall
"""
from .. import prompts
from ..metrics import norm_text
from . import STRINGS

TASK = "ocr_page"
NAME = "문서 OCR"
PROMPT = prompts.P_OCR_PAGE
ANSWER = STRINGS
EXAMPLE = ["홍길동", "2026년 1월 31일"]
NOTES = ("데이터의 answer는 채점할 값 문자열의 목록입니다. 모델은 줄바꿈한 전체 텍스트를 출력합니다. "
         "고정 인쇄 문구까지 정답인 합성 OCR 세트와 구분합니다.")


def make(doc):
    lines: list[str] = []
    for f in doc.visible:
        for ln in str(f["value"]).split("\n"):
            if norm_text(ln) and ln.strip() not in lines:
                lines.append(ln.strip())
    if not lines:
        return []
    return [{"id": f"ocr_page/{doc.sid}", "task": TASK, "prompt": PROMPT, "answer": lines, **doc.base}]
