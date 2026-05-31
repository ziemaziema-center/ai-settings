from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "reports" / "offline_artifacts" / "local_dry_run" / "local_dry_run_result_v1.json"


class TestAlertRequiredForCriticalEvents(unittest.TestCase):
    def test_alert_required_for_critical_events(self) -> None:
        data = json.loads(RESULT.read_text(encoding="utf-8"))
        self.assertGreaterEqual(data["summary"]["alert_required_count"], 3)
        critical_names = {"kill_active_case", "recon_drift_case", "clock_skew_case"}
        for row in data["runs"]:
            if row["scenario"] in critical_names:
                self.assertTrue(row["alert_required"])


if __name__ == "__main__":
    unittest.main()
