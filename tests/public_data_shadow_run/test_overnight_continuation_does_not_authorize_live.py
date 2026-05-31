import unittest
from pathlib import Path


class TestOvernightContinuationDoesNotAuthorizeLive(unittest.TestCase):
    def test_non_authorization(self):
        text = Path("reports/offline_artifacts/overnight/overnight_public_data_shadow_continuation_decision_v1.md").read_text(encoding="utf-8")
        self.assertIn("does not authorize live trading", text)
        self.assertIn("authenticated shadow execution", text)


if __name__ == "__main__":
    unittest.main()
