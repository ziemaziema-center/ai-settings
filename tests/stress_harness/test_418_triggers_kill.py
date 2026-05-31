from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HARNESS_RESULT = ROOT / "reports" / "offline_artifacts" / "stress_harness" / "stress_harness_result_v1.json"


class Test418TriggersKill(unittest.TestCase):
    def test_418_triggers_kill(self) -> None:
        result = json.loads(HARNESS_RESULT.read_text(encoding="utf-8"))
        row = next(x for x in result["outcomes"] if x["scenario"] == "rate_limit_418_ban_event")
        self.assertEqual(row["state"], "KILL_TRIGGERED")
        self.assertTrue(row["kill_triggered"])
        self.assertTrue(row["alert_required"])


if __name__ == "__main__":
    unittest.main()
