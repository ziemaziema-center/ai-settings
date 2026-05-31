from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestRealShadowReviewDoesNotMarkExecutionComplete(unittest.TestCase):
    def test_real_shadow_review_does_not_mark_execution_complete(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "real_shadow_review" / "real_shadow_data_access_review_v1.md").read_text(encoding="utf-8").lower()
        self.assertIn("execution_status: not_executed", text)


if __name__ == "__main__":
    unittest.main()
