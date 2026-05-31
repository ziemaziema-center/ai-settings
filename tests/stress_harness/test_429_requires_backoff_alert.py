from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HARNESS_RESULT = ROOT / "reports" / "offline_artifacts" / "stress_harness" / "stress_harness_result_v1.json"


class Test429RequiresBackoffAlert(unittest.TestCase):
    def test_429_requires_backoff_alert(self) -> None:
        result = json.loads(HARNESS_RESULT.read_text(encoding="utf-8"))
        row = next(x for x in result["outcomes"] if x["scenario"] == "rate_limit_429_storm")
        self.assertEqual(row["state"], "SIGNAL_BLOCKED")
        self.assertTrue(row["backoff_required"])
        self.assertTrue(row["alert_required"])


if __name__ == "__main__":
    unittest.main()
