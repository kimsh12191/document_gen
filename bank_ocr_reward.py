"""MS-SWIFT external plugin. Install this project before launching distributed training."""
from swift.rewards import ORM, orms

from bank_ocr.metrics import reward


class BankOCRReward(ORM):
    def __call__(self, completions, task, target_text, target_bbox, ocr_items, **kwargs):
        columns = (task, target_text, target_bbox, ocr_items)
        if any(len(column) != len(completions) for column in columns):
            raise ValueError("Reward column batch lengths do not match completions")
        return [reward(c, t, text, box, items) for c, t, text, box, items in zip(completions, *columns)]


orms["bank_ocr_cycle"] = BankOCRReward
