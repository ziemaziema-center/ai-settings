import unittest
from pathlib import Path


class TestDataShapeV3NoTradingParser(unittest.TestCase):
    def test_no_parser(self):
        t = Path("reports/offline_artifacts/public_data_shadow_run/public_data_shape_stability_review_v3.md").read_text(encoding="utf-8")
        self.assertIn("STOP parser implementation", t)
        self.assertIn("out of scope", t)


if __name__ == "__main__":
    unittest.main()
