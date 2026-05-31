from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "reports" / "offline_artifacts" / "local_dry_run" / "local_dry_run_result_v1.json"


class TestReconDriftBlocksCandidates(unittest.TestCase):
    def test_recon_drift_blocks_candidates(self) -> None:
        data = json.loads(RESULT.read_text(encoding="utf-8"))
        row = next(r for r in data["runs"] if r["scenario"] == "recon_drift_case")
        self.assertEqual(row["reason"], "recon_drift")
        self.assertIn("RECON_DRIFT_DETECTED", row["path"])
        self.assertEqual(row["result_state"], "SIGNAL_BLOCKED")


if __name__ == "__main__":
    unittest.main()
