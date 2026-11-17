"""studio 사용 가이드 화면이 보여 주는 문서: guide/studio/ 의 화면 쓰는 법만 (학습·평가·OCR 준비는 저장소 guide/train/)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = {
    "studio.md": "studio 사용법 · 할 일별로 (서식 보기·검수·고치기 · 새 서식 · 데이터셋)",
    "new-forms.md": "새 서식 추가 · 그림 위에 칸 그리기 (도구·표·날짜·자유 위치)",
    "keys.md": "칸의 키 이름 정하기",
    "generators.md": "원하는 값이 고르기 창에 없을 때",
    "data.md": "데이터셋 만들기 · 레시피 · 명령(remote_build.py)",
}


def document(name: str) -> str:
    if name not in DOCUMENTS:
        raise KeyError(name)
    return (ROOT / "guide" / "studio" / name).read_text(encoding="utf-8")


if __name__ == "__main__":
    print("\n".join(f"{k}\t{v}" for k, v in DOCUMENTS.items()))
