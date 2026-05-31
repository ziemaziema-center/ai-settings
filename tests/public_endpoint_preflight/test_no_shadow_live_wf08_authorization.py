from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestNoShadowLiveWf08Authorization(unittest.TestCase):
    def test_no_shadow_live_wf08_authorization(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_endpoint_preflight" / "public_quotation_endpoint_preflight_review_v1.md").read_text(encoding="utf-8")
        self.assertIn("WF08_REVIEW_BLOCKED", text)
        self.assertIn("LIVE_AUTHORIZATION_BLOCKED", text)
if __name__ == "__main__":
    unittest.main()
