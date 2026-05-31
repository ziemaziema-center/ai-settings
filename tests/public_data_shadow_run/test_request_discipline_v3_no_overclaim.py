import unittest
from pathlib import Path


class TestRequestDisciplineV3NoOverclaim(unittest.TestCase):
    def test_no_overclaim(self):
        t = Path("reports/offline_artifacts/public_data_shadow_run/public_data_request_discipline_review_v3.md").read_text(encoding="utf-8")
        self.assertIn("no_overclaim", t)
        self.assertIn("does not claim complete Upbit rate-limit proof", t)


if __name__ == "__main__":
    unittest.main()
