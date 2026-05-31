import unittest
from pathlib import Path


class TestEvidenceReviewAccepts14Cycles(unittest.TestCase):
    def test_verdict_and_cycle_count(self):
        text = Path("reports/offline_artifacts/public_data_shadow_run/public_data_n_day_shadow_recorder_evidence_review_v1.md").read_text(encoding="utf-8")
        self.assertIn("PUBLIC_DATA_RECORDER_EVIDENCE_ACCEPTED", text)
        self.assertIn("cycles_completed: 14 / 14", text)


if __name__ == "__main__":
    unittest.main()
