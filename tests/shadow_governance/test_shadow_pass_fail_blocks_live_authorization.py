from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestShadowPassFailBlocksLiveAuthorization(unittest.TestCase):
    def test_shadow_pass_fail_blocks_live_authorization(self) -> None:
        path = ROOT / "reports" / "offline_artifacts" / "shadow_governance" / "controlled_n_day_shadow_pass_fail_criteria_v1.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("SHADOW_RUN_EVIDENCE_READY_FOR_WF08_REVIEW", text)
        self.assertIn("does not mean live authorized", text.lower())


if __name__ == "__main__":
    unittest.main()
