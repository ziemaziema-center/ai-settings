from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestShadowScopeRequiresDailyReview(unittest.TestCase):
    def test_shadow_scope_requires_daily_review(self) -> None:
        path = ROOT / "reports" / "offline_artifacts" / "shadow_governance" / "controlled_n_day_shadow_scope_v1.md"
        text = path.read_text(encoding="utf-8").lower()
        self.assertIn("daily review requirement", text)
        self.assertIn("daily human reviewer", text)


if __name__ == "__main__":
    unittest.main()
