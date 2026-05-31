import json
import unittest
from pathlib import Path
from _test_utils import ROOT, run_backtest


class TestForbiddenStatesAbsent(unittest.TestCase):
    def test_forbidden_states_absent(self):
        result = run_backtest()
        self.assertEqual(result["metrics"]["forbidden_state_count"], 0)

        forbidden = {"SUBMITTED", "ACK_RECEIVED", "OPEN", "FILLED", "PARTIAL", "LIVE_ORDER", "SHADOW_ORDER"}
        for d in result["decisions"]:
            self.assertNotIn(d["state"], forbidden)
            for s in d.get("state_path", []):
                self.assertNotIn(s, forbidden)

        report_path = ROOT / "reports" / "offline_artifacts" / "offline_test_harness" / "offline_backtest_result_v1.json"
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        for d in payload["decisions"]:
            self.assertNotIn(d["state"], forbidden)
            for s in d.get("state_path", []):
                self.assertNotIn(s, forbidden)


if __name__ == "__main__":
    unittest.main()
