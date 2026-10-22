"""가이드의 실제 OCR 예시를 Studio에서도 읽는다. 예시·이미지를 복제하지 않는다."""
from __future__ import annotations

import json
import re
from pathlib import Path

from docgen.bench.ocr_tasks import PROMPTS

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "guide/tasks.md"
IMAGES = ROOT / "guide/examples/img"


def examples() -> dict:
    text = SOURCE.read_text(encoding="utf-8")
    items = []
    for section in re.split(r"(?m)^### ", text)[1:]:
        heading = section.splitlines()[0]
        match = re.match(r"1-\d+\. (\w+) — (.+)", heading)
        if not match or match[1] not in PROMPTS:
            continue
        task, title = match.groups()
        blocks = re.findall(r"(?m)^```[^\n]*\n(.*?)\n```", section, re.S)
        if len(blocks) != 4:
            raise ValueError(f"OCR 예시 {task}: 질문·정답·모델 답·원본 문항 4개가 필요합니다")
        row = json.loads(blocks[3])
        target = json.loads(blocks[1])
        if row["task"] != task or json.loads(row["target"]) != target:
            raise ValueError(f"OCR 예시 {task}: 문항과 정답이 다릅니다")
        names = re.findall(r'<img src="examples/img/([^"/]+)"', section)
        if not names or any(not (IMAGES / name).is_file() for name in names):
            raise ValueError(f"OCR 예시 {task}: 예시 이미지가 없습니다")
        how = re.search(r"\*\*어떻게 만드나:\*\* (.+)", section)
        score = re.search(r"\*\*채점:\*\* (.+)", section)
        items.append({"task": task, "title": title, "how": how[1] if how else "",
                      "score": score[1] if score else "", "prompt": blocks[0], "target": target,
                      "model_answer": blocks[2], "record": row,
                      "input_image": f"/ocr-example-images/{names[0]}",
                      "annotated_images": [f"/ocr-example-images/{n}" for n in names[1:]]})
    if set(x["task"] for x in items) != set(PROMPTS):
        raise ValueError("가이드에 OCR 8과제 예시가 모두 있어야 합니다")
    return {"source": "guide/tasks.md", "examples": items,
            "note": "가이드와 같은 합성 예시입니다. 실제 고객 문서가 아닙니다. 생성기 라벨을 OCR 결과 형식으로 바꾼 뒤 OCR 준비 코드로 만들었습니다. 이미지는 긴 변 1000px 이하의 설명용 사본이며, 정답 좌표는 0~1000 상대 좌표입니다. 원본 문항은 OCR 준비 형식(target)이고 모델 답은 SFT 출력 형식입니다."}
