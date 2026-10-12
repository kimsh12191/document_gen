"""MS-SWIFT external plugin for the banking-task GRPO: the reward is the docgen benchmark's own scorer.
Needs this project and the docgen code importable (run_bank_pipeline.py sets PYTHONPATH and DOCGEN_ROOT)."""
import json

from swift.rewards import ORM, orms

from bank_task.score import reward


class BankTaskReward(ORM):
    def __call__(self, completions, bench_item, **kwargs):
        if len(bench_item) != len(completions):
            raise ValueError("Reward column batch lengths do not match completions")
        return [reward(c, json.loads(item)) for c, item in zip(completions, bench_item)]


orms["bank_task"] = BankTaskReward
