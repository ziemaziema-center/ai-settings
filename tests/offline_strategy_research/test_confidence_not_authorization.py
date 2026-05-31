import unittest
from _test_utils import load_module


class TestConfidenceNotAuthorization(unittest.TestCase):
    def test_confidence_not_authorization(self):
        generator = load_module("synthetic_generator", "synthetic_market_data_generator.py")
        engine = load_module("candidate_engine", "offline_strategy_candidate_engine.py")
        snap = next(x for x in generator.generate_synthetic_market_data() if x["scenario"] == "sudden_spike")
        decision = engine.evaluate_candidate(snap)
        self.assertIn(decision["confidence_bucket"], {"LOW", "MEDIUM", "HIGH"})
        self.assertFalse(decision["confidence_authorizes_trading"])
        self.assertFalse(decision["execution_authorized"])


if __name__ == "__main__":
    unittest.main()
