from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestShadowNDaysNotMarkedComplete(unittest.TestCase):
    def test_shadow_n_days_not_marked_complete(self) -> None:
        path = ROOT / "reports" / "offline_artifacts" / "shadow_governance" / "controlled_n_day_shadow_scope_v1.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("N-day completion cannot be claimed", text)
        self.assertNotIn("SHADOW_MODE_N_DAYS_EXECUTED: PASS", text)


if __name__ == "__main__":
    unittest.main()
