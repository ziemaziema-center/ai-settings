from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestNoApiOrCredentialsUsedInReview(unittest.TestCase):
    def test_no_api_or_credentials_used_in_review(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "real_shadow_review" / "real_shadow_data_access_review_v1.md").read_text(encoding="utf-8")
        self.assertIn("no Upbit API call is made", text)
        self.assertIn("no credential is read", text)


if __name__ == "__main__":
    unittest.main()
