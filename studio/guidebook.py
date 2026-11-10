"""studio 사용 가이드 화면이 보여 주는 문서 목록 (guide/*.md 와 서식 만들기 참고 문서)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = {
    "studio.md": "studio 사용법 · 서식 / 새 서식 추가 / 데이터셋",
    "terms.md": "용어 한 장 · 같은 것의 여러 이름",
    "README.md": "사용 설명서 · 전체 문서 목록",
    "start.md": "처음부터 끝까지 한 번 · 만들기 → 학습 → 결과",
    "data.md": "데이터셋 만들기 · studio 화면·remote_build.py·레시피",
    "training.md": "학습 설정·실행",
    "eval.md": "평가 세트·채점 함수·평가만·다시 채점",
    "results.md": "결과 해석",
    "new-forms.md": "새 서식 추가 · 그림 위에 칸 그리기 → 검수",
    "keys.md": "칸의 키 이름 정하기 · 새 서식·외주용",
    "generators.md": "원하는 값이 고르기 창에 없을 때 · 보기·틀 / 값 하나 함수 / 칸끼리 관계",
    "ocr.md": "내 이미지로 OCR 데이터 준비",
    "benchmark.md": "과제와 채점 규칙",
    "questions.md": "질문과 정답 형식",
    "tasks.md": "실제 데이터 예시",
    "documents.md": "서류 이름 목록",
}
# 서식 만들기 참고 문서 (docgen/manual, 저장소 기준 경로를 ID 로): 새 서식 가이드가 링크한다.
MANUALS = {
    "docgen/forms/README.md": "서식 폴더 설명서 · 칸·값·질문·답·qa.py·채점·검사",
    "docgen/manual/NEW_FORM_SPEC.md": "html 서식 파일 형식 · 템플릿·칸 목록·키·생성 스크립트 (코드로 고칠 때)",
    "docgen/manual/FORM_SHELL_GUIDE.md": "서식 모양(껍데기)만 고치기 · VLM 에게 맡길 때",
    "docker/README.md": "설치·내부망 반입 · studio 컨테이너 띄우기",
}
DOCUMENTS.update({k: v for k, v in MANUALS.items() if (ROOT / k).exists()})
# 추가 참고 문서도 guide 내부에서 이동할 수 있다. 경로는 서버가 수집한 목록만 허용한다.
for _path in sorted((ROOT / "guide").rglob("*.md")):
    _name = _path.relative_to(ROOT / "guide").as_posix()
    if _name not in DOCUMENTS:
        DOCUMENTS[_name] = _path.read_text(encoding="utf-8").splitlines()[0].lstrip("# ") or _name


def document(name: str) -> str:
    if name not in DOCUMENTS:
        raise KeyError(name)
    return (ROOT / name if name in MANUALS else ROOT / "guide" / name).read_text(encoding="utf-8")


if __name__ == "__main__":
    print("\n".join(f"{k}\t{v}" for k, v in DOCUMENTS.items()))
