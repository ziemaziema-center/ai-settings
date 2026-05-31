import unittest
from pathlib import Path


class TestDataShapeReviewNoTradingParser(unittest.TestCase):
    def test_no_trading_parser(self):
        text = Path("reports/offline_artifacts/public_data_shadow_run/public_data_shape_stability_review_v1.md").read_text(encoding="utf-8")
        self.assertIn("Do not derive trading action", text)
        self.assertIn("out of scope", text)


if __name__ == "__main__":
    unittest.main()
