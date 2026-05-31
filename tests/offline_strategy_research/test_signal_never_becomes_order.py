import unittest
from _test_utils import load_module


class TestSignalNeverBecomesOrder(unittest.TestCase):
    def test_signal_never_becomes_order(self):
        generator = load_module("synthetic_generator", "synthetic_market_data_generator.py")
        engine = load_module("candidate_engine", "offline_strategy_candidate_engine.py")
        snap = next(x for x in generator.generate_synthetic_market_data() if x["scenario"] == "normal_trend")
        decision = engine.evaluate_candidate(snap)
        self.assertFalse(decision["order_submission_allowed"])
        self.assertFalse(decision["execution_authorized"])
        self.assertEqual(decision["live_runtime_api_credential_actions"], "none")


if __name__ == "__main__":
    unittest.main()
