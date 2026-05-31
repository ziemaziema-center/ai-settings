import unittest
from _test_utils import run_backtest


class TestCooldownBlocksOvertrade(unittest.TestCase):
    def test_cooldown_blocks_overtrade(self):
        result = run_backtest()
        item = next(d for d in result["decisions"] if d["scenario"] == "cooldown_active")
        self.assertEqual(item["state"], "RISK_FILTER_REJECTED")
        self.assertIn("cooldown_active", item["reason_codes"])


if __name__ == "__main__":
    unittest.main()
