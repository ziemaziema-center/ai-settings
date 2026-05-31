import unittest
from _test_utils import run_backtest


class TestForbiddenStatesAbsent(unittest.TestCase):
    def test_forbidden_states_absent(self):
        result = run_backtest()
        self.assertEqual(result["metrics"]["forbidden_state_count"], 0)


if __name__ == "__main__":
    unittest.main()
