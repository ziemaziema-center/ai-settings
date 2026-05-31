import unittest
from _test_utils import run_backtest


class TestPTRCDependencyRequired(unittest.TestCase):
    def test_ptrc_dependency_required(self):
        result = run_backtest()
        for d in result["decisions"]:
            self.assertTrue(d["dependencies"]["ptrc_required"])


if __name__ == "__main__":
    unittest.main()
