from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NON_AUTH = "This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims."


class TestShadowRecorderNotAuthorized(unittest.TestCase):
    def test_shadow_recorder_not_authorized(self) -> None:
        base = ROOT / "reports" / "offline_artifacts" / "shadow_governance"
        files = [
            base / "shadow_recorder_stub_design_v1.md",
            base / "shadow_recorder_stub_contract_v1.md",
            base / "shadow_mode_not_authorized_notice_v1.md",
        ]
        for file_path in files:
            text = file_path.read_text(encoding="utf-8")
            self.assertIn(NON_AUTH, text, f"Missing non-authorization sentence: {file_path}")
            self.assertTrue("not authorized" in text.lower() or "requires future approval" in text.lower())


if __name__ == "__main__":
    unittest.main()
