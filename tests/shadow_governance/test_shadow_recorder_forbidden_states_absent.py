from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestShadowRecorderForbiddenStatesAbsent(unittest.TestCase):
    def test_shadow_recorder_forbidden_states_absent(self) -> None:
        path = ROOT / "reports" / "offline_artifacts" / "shadow_governance" / "shadow_recorder_execution_contract_v1.md"
        text = path.read_text(encoding="utf-8")
        forbidden = ["SUBMITTED", "ACK_RECEIVED", "OPEN", "FILLED", "PARTIAL", "LIVE_ORDER", "EXCHANGE_CONNECTED", "CREDENTIAL_READ"]
        for token in forbidden:
            self.assertIn(f"- {token}", text)


if __name__ == "__main__":
    unittest.main()
