from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HARNESS_RESULT = ROOT / "reports" / "offline_artifacts" / "stress_harness" / "stress_harness_result_v1.json"


class TestHeartbeatMissedRequiresKillOrAlert(unittest.TestCase):
    def test_heartbeat_missed_requires_kill_or_alert(self) -> None:
        result = json.loads(HARNESS_RESULT.read_text(encoding="utf-8"))
        row = next(x for x in result["outcomes"] if x["scenario"] == "heartbeat_missed")
        self.assertIn(row["state"], {"KILL_TRIGGERED", "SIGNAL_BLOCKED", "HUMAN_REVIEW_REQUIRED"})
        self.assertTrue(row["kill_triggered"] or row["alert_required"])


if __name__ == "__main__":
    unittest.main()
