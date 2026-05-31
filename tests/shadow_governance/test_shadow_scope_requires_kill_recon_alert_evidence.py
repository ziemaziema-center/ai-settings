from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestShadowScopeRequiresKillReconAlertEvidence(unittest.TestCase):
    def test_shadow_scope_requires_kill_recon_alert_evidence(self) -> None:
        path = ROOT / "reports" / "offline_artifacts" / "shadow_governance" / "controlled_shadow_execution_blocker_matrix_v1.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("SHADOW_KILL_ALERT_RECON_EVIDENCE_LINK_REQUIRED", text)


if __name__ == "__main__":
    unittest.main()
