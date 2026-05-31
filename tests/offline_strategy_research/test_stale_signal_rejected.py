import unittest
from _test_utils import run_backtest


class TestStaleSignalRejected(unittest.TestCase):
    def test_stale_signal_rejected(self):
        result = run_backtest()
        stale = next(d for d in result["decisions"] if d["scenario"] == "stale_data")
        self.assertEqual(stale["state"], "RISK_FILTER_REJECTED")
        self.assertIn("stale_data", stale["reason_codes"])


if __name__ == "__main__":
    unittest.main()
