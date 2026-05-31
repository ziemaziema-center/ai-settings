from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NON_AUTH = "This document does not authorize live trading, shadow mode execution, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims."


class TestShadowScopeNonAuthorization(unittest.TestCase):
    def test_shadow_scope_non_authorization(self) -> None:
        path = ROOT / "reports" / "offline_artifacts" / "shadow_governance" / "controlled_n_day_shadow_scope_v1.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn(NON_AUTH, text)
        self.assertIn("not shadow execution", text.lower())


if __name__ == "__main__":
    unittest.main()
