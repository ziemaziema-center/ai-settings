import unittest
from _test_utils import run_backtest


class TestReconKillDependencyRequired(unittest.TestCase):
    def test_recon_kill_dependency_required(self):
        result = run_backtest()
        for d in result["decisions"]:
            self.assertTrue(d["dependencies"]["recon_required"])
            self.assertTrue(d["dependencies"]["kill_required"])


if __name__ == "__main__":
    unittest.main()
