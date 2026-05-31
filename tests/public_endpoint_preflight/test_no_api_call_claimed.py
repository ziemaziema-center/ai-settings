from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestNoApiCallClaimed(unittest.TestCase):
    def test_no_api_call_claimed(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_endpoint_preflight" / "public_quotation_endpoint_preflight_review_v1.md").read_text(encoding="utf-8")
        self.assertIn("no Upbit API call is made in this run", text)
if __name__ == "__main__":
    unittest.main()
