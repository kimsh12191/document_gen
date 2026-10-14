from pathlib import Path
import unittest

from bank_ocr.tasks import PROMPTS

ROOT = Path(__file__).resolve().parents[1]


class PromptsDocTests(unittest.TestCase):
    def test_guide_quotes_every_training_prompt(self):
        """docs/PROMPTS.md is what users copy; it must match the prompts the model was trained on."""
        guide = (ROOT / "docs" / "PROMPTS.md").read_text(encoding="utf-8")
        for task, templates in PROMPTS.items():
            self.assertIn(f"### {task}", guide)
            for template in templates:
                with self.subTest(task=task, template=template[:40]):
                    self.assertIn(f"`{template.replace('{{', '{').replace('}}', '}')}`", guide)


if __name__ == "__main__":
    unittest.main()
