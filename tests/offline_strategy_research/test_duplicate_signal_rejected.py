import unittest
from _test_utils import run_backtest


class TestDuplicateSignalRejected(unittest.TestCase):
    def test_duplicate_signal_rejected(self):
        result = run_backtest()
        item = next(d for d in result["decisions"] if d["scenario"] == "duplicate_signal")
        self.assertEqual(item["state"], "RISK_FILTER_REJECTED")
        self.assertIn("duplicate_signal", item["reason_codes"])


if __name__ == "__main__":
    unittest.main()
