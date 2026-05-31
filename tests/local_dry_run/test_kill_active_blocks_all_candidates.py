from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "reports" / "offline_artifacts" / "local_dry_run" / "local_dry_run_result_v1.json"


class TestKillActiveBlocksAllCandidates(unittest.TestCase):
    def test_kill_active_blocks_all_candidates(self) -> None:
        data = json.loads(RESULT.read_text(encoding="utf-8"))
        row = next(r for r in data["runs"] if r["scenario"] == "kill_active_case")
        self.assertEqual(row["reason"], "kill_active")
        self.assertEqual(row["result_state"], "SIGNAL_BLOCKED")
        self.assertTrue(row["no_order_submission"])


if __name__ == "__main__":
    unittest.main()
