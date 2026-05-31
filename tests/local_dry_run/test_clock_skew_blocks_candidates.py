from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "reports" / "offline_artifacts" / "local_dry_run" / "local_dry_run_result_v1.json"


class TestClockSkewBlocksCandidates(unittest.TestCase):
    def test_clock_skew_blocks_candidates(self) -> None:
        data = json.loads(RESULT.read_text(encoding="utf-8"))
        row = next(r for r in data["runs"] if r["scenario"] == "clock_skew_case")
        self.assertEqual(row["result_state"], "PTRC_REJECTED")
        self.assertEqual(row["reason"], "clock_skew")
        self.assertIn("PTRC_REJECTED", row["path"])


if __name__ == "__main__":
    unittest.main()
