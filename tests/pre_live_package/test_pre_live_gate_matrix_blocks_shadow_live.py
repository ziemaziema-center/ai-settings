from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _row_status(text: str, gate: str) -> str:
    for line in text.splitlines():
        if line.strip().startswith(f"| {gate} |"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                return parts[3]
    return ""


class TestPreLiveGateMatrixBlocksShadowLive(unittest.TestCase):
    def test_pre_live_gate_matrix_blocks_shadow_live(self) -> None:
        matrix = ROOT / "reports" / "offline_artifacts" / "pre_live_package" / "pre_live_gate_evidence_matrix_v1.md"
        text = matrix.read_text(encoding="utf-8")
        self.assertEqual(_row_status(text, "SHADOW_MODE_N_DAYS_EXECUTED"), "BLOCKED")
        self.assertEqual(_row_status(text, "WF08_REVIEW"), "BLOCKED")
        self.assertEqual(_row_status(text, "LIVE_AUTHORIZATION"), "BLOCKED")


if __name__ == "__main__":
    unittest.main()
