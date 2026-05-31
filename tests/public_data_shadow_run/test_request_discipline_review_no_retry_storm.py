import unittest
from pathlib import Path


class TestRequestDisciplineReviewNoRetryStorm(unittest.TestCase):
    def test_no_retry_storm(self):
        text = Path("reports/offline_artifacts/public_data_shadow_run/public_data_request_discipline_review_v1.md").read_text(encoding="utf-8")
        self.assertIn("no retry loop implemented", text)


if __name__ == "__main__":
    unittest.main()
