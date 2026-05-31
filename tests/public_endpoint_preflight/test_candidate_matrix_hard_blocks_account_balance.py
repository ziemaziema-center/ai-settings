from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestCandidateMatrixHardBlocksAccountBalance(unittest.TestCase):
    def test_candidate_matrix_hard_blocks_account_balance(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_endpoint_preflight" / "public_quotation_endpoint_candidate_matrix_v1.md").read_text(encoding="utf-8")
        self.assertIn("account/balance endpoint", text)
        self.assertIn("HARD_BLOCKED", text)
if __name__ == "__main__":
    unittest.main()
