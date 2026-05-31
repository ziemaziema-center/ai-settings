from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestShadowBlockerMatrixContainsRequiredBlockers(unittest.TestCase):
    def test_shadow_blocker_matrix_contains_required_blockers(self) -> None:
        path = ROOT / "reports" / "offline_artifacts" / "shadow_governance" / "controlled_shadow_execution_blocker_matrix_v1.md"
        text = path.read_text(encoding="utf-8")
        required = [
            "CREDENTIAL_USE_NOT_APPROVED",
            "UPBIT_API_USE_NOT_APPROVED",
            "SCHEDULER_NOT_APPROVED",
            "N_DAY_SHADOW_NOT_STARTED",
            "N_DAY_SHADOW_NOT_COMPLETED",
            "WF08_REVIEW_BLOCKED",
            "LIVE_AUTHORIZATION_BLOCKED",
            "HUMAN_SHADOW_EXEC_AUTH_MISSING",
        ]
        for token in required:
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
