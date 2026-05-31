from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestRealShadowReviewBlocksLiveWf08(unittest.TestCase):
    def test_real_shadow_review_blocks_live_wf08(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "reviews" / "real_shadow_data_access_review_final_verdict_v1.md").read_text(encoding="utf-8")
        self.assertIn("live_authorization_status: BLOCKED", text)
        self.assertIn("wf08_status: BLOCKED", text)


if __name__ == "__main__":
    unittest.main()
