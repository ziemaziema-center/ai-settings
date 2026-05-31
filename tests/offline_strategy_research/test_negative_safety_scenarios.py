import unittest
from _test_utils import run_backtest


class TestNegativeSafetyScenarios(unittest.TestCase):
    def test_negative_scenarios_rejected(self):
        result = run_backtest()
        expected = {
            "rate_budget_exhausted": "rate_budget_exhausted",
            "heartbeat_missed": "heartbeat_missed",
            "clock_skew": "clock_skew",
            "reconciliation_drift": "reconciliation_drift",
            "kill_active": "kill_active",
        }

        for scenario, reason in expected.items():
            d = next(item for item in result["decisions"] if item["scenario"] == scenario)
            self.assertEqual(d["state"], "RISK_FILTER_REJECTED")
            self.assertIn(reason, d["reason_codes"])
            self.assertFalse(d["order_submission_allowed"])
            self.assertFalse(d["execution_authorized"])


if __name__ == "__main__":
    unittest.main()
