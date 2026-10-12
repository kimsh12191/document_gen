"""MS-SWIFT external plugin. Install this project before launching distributed training."""
from swift.rewards import ORM, orms

from bank_ocr.metrics import reward


class BankOCRReward(ORM):
    def __call__(self, completions, task, target, **kwargs):
        if len(task) != len(completions) or len(target) != len(completions):
            raise ValueError("Reward column batch lengths do not match completions")
        return [reward(c, t, gold) for c, t, gold in zip(completions, task, target)]


orms["bank_ocr"] = BankOCRReward
