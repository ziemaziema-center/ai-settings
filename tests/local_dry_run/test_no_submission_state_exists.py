from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "reports" / "offline_artifacts" / "local_dry_run" / "local_dry_run_result_v1.json"
FORBIDDEN = {"SUBMITTED", "ACK_RECEIVED", "OPEN", "FILLED", "PARTIAL", "LIVE_ORDER", "SHADOW_ORDER", "EXCHANGE_CONNECTED"}


class TestNoSubmissionStateExists(unittest.TestCase):
    def test_no_submission_state_exists(self) -> None:
        data = json.loads(RESULT.read_text(encoding="utf-8"))
        self.assertFalse(data["summary"]["submitted_state_present"])
        self.assertEqual(data["summary"]["forbidden_state_count"], 0)
        for row in data["runs"]:
            self.assertNotIn(row["result_state"], FORBIDDEN)
            self.assertNotIn("SUBMITTED", row["path"])


if __name__ == "__main__":
    unittest.main()
