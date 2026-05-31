import unittest
from pathlib import Path


class TestNoLiveWf08AuthorizationAfterOvernight(unittest.TestCase):
    def test_no_live_wf08(self):
        text = Path("reports/offline_artifacts/overnight/overnight_public_data_continuation_decision_v2.md").read_text(encoding="utf-8")
        self.assertIn("live trading is not approved", text)
        self.assertIn("WF08", text)


if __name__ == "__main__":
    unittest.main()
