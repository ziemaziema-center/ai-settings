import unittest
from pathlib import Path


class TestMultiWindowStabilityReviewAcceptsPublicDataOnly(unittest.TestCase):
    def test_verdict(self):
        text = Path("reports/offline_artifacts/public_data_shadow_run/public_data_multi_window_stability_review_v1.md").read_text(encoding="utf-8")
        self.assertIn("PUBLIC_DATA_MULTI_WINDOW_STABILITY_ACCEPTED", text)


if __name__ == "__main__":
    unittest.main()
