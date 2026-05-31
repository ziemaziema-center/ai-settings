from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NON_AUTH = "This document does not authorize live trading, real shadow mode execution, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims."


class TestRealShadowReviewNonAuthorization(unittest.TestCase):
    def test_real_shadow_review_non_authorization(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "real_shadow_review" / "real_shadow_data_access_review_v1.md").read_text(encoding="utf-8")
        self.assertIn(NON_AUTH, text)
        self.assertIn("review is not execution", text.lower())


if __name__ == "__main__":
    unittest.main()
