import unittest
from pathlib import Path


class TestRollingStabilityReviewAcceptsPublicDataOnly(unittest.TestCase):
    def test_verdict(self):
        t = Path("reports/offline_artifacts/public_data_shadow_run/public_data_rolling_stability_review_v1.md").read_text(encoding="utf-8")
        self.assertIn("PUBLIC_DATA_ROLLING_STABILITY_ACCEPTED", t)


if __name__ == "__main__":
    unittest.main()
