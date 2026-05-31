from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestNoSubmitArchitectureBlocksScheduler(unittest.TestCase):
    def test_no_submit_architecture_blocks_scheduler(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "real_shadow_review" / "real_shadow_no_submit_architecture_v1.md").read_text(encoding="utf-8")
        self.assertIn("scheduler disabled", text.lower())


if __name__ == "__main__":
    unittest.main()
