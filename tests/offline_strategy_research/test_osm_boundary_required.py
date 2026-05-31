import unittest
from _test_utils import run_backtest


class TestOSMBoundaryRequired(unittest.TestCase):
    def test_osm_boundary_required(self):
        result = run_backtest()
        for d in result["decisions"]:
            self.assertTrue(d["dependencies"]["osm_required"])


if __name__ == "__main__":
    unittest.main()
