"""ms-swift GRPO 보상 플러그인 하나 (옛 bank_ocr_reward.py·bank_task_reward.py): 보상 = docgen.bench.evaluate.reward —
평가 채점과 같은 함수 (OCR 과제는 글자 유사도·박스 IoU, 업무 과제는 부분 점수). launch.py 가 절대 경로로 붙인다."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # 저장소 최상위 (docgen)

from swift.rewards import ORM, orms  # noqa: E402

from docgen.bench.evaluate import reward  # noqa: E402


class DocgenReward(ORM):
    def __call__(self, completions, task, bench_item, **kwargs):
        if len(task) != len(completions) or len(bench_item) != len(completions):
            raise ValueError("Reward column batch lengths do not match completions")
        return [reward(t, c, json.loads(item)) for c, t, item in zip(completions, task, bench_item)]


orms["docgen"] = DocgenReward
