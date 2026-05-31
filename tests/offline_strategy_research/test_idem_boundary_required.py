import unittest
from _test_utils import run_backtest


class TestIDEMBoundaryRequired(unittest.TestCase):
    def test_idem_boundary_required(self):
        result = run_backtest()
        for d in result["decisions"]:
            self.assertTrue(d["dependencies"]["idem_required"])


if __name__ == "__main__":
    unittest.main()
