import unittest
from pathlib import Path


class TestEvidenceLedgerContainsAllRuns(unittest.TestCase):
    def test_runs(self):
        t = Path("reports/offline_artifacts/public_data_shadow_run/public_data_observation_evidence_ledger_v1.md").read_text(encoding="utf-8")
        for x in ["one_shot_preflight", "14_cycle_recorder", "56_cycle_extended", "56_cycle_long", "repeated_windows_v1"]:
            self.assertIn(x, t)


if __name__ == "__main__":
    unittest.main()
