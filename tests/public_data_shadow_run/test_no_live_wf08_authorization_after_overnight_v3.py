import unittest
from pathlib import Path


class TestNoLiveWf08AuthorizationAfterOvernightV3(unittest.TestCase):
    def test_no_live_wf08(self):
        t = Path("reports/offline_artifacts/overnight/overnight_public_data_continuation_decision_v3.md").read_text(encoding="utf-8")
        self.assertIn("WF08", t)
        self.assertIn("live trading is not approved", t)


if __name__ == "__main__":
    unittest.main()
