import unittest
from pathlib import Path


class TestEvidenceAcceptanceMatrixAllPass(unittest.TestCase):
    def test_all_rows_pass(self):
        text = Path("reports/offline_artifacts/public_data_shadow_run/public_data_n_day_shadow_evidence_acceptance_matrix_v1.md").read_text(encoding="utf-8")
        self.assertNotIn("| FAIL |", text)
        self.assertIn("| CYCLES_14_COMPLETED |", text)


if __name__ == "__main__":
    unittest.main()
