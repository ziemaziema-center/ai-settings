import unittest
from _test_utils import run_backtest


class TestBacktestResultSchema(unittest.TestCase):
    def test_backtest_result_schema(self):
        result = run_backtest()
        metrics = result["metrics"]
        required = {
            "scenario_count",
            "candidate_count",
            "rejected_signal_count",
            "ptrc_eligible_count",
            "no_order_submission_count",
            "forbidden_state_count",
            "rejection_reason_counts",
            "max_drawdown_simulated",
            "fee_drag_simulated",
            "overtrade_score",
            "safety_score",
            "governance_score",
            "final_quality_score",
        }
        self.assertTrue(required.issubset(set(metrics.keys())))


if __name__ == "__main__":
    unittest.main()
