from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "reports/upbit_current_safe_scope_closure_report_2026-06-01.md"
J = ROOT / "runtime/upbit_current_safe_scope_closure_report_20260601.json"
S = ROOT / "reports/upbit_next_boundary_session_sendoff_2026-06-01.md"

class SafeScopeClosureTest(unittest.TestCase):
    def test_files_exist(self):
        for p in [R, J, S]:
            self.assertTrue(p.exists(), str(p))

    def test_core_fields(self):
        t = R.read_text(encoding="utf-8-sig")
        self.assertIn("highest_completed_safe_gate: GATE_22_WF08_AUTHORIZATION_REVIEW_ONLY", t)
        self.assertIn("gate23_live_authorization_status: BLOCKED", t)

    def test_json_verdict(self):
        payload = json.loads(J.read_text(encoding="utf-8-sig"))
        self.assertEqual(payload["final_safety_verdict"], "PASS_CURRENT_SAFE_SCOPE_CLOSURE_REVIEW_ONLY")

if __name__ == "__main__":
    unittest.main()
