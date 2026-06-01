from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "reports/upbit_gate22_wf08_authorization_review_2026-06-01.md"
J = ROOT / "runtime/upbit_gate22_wf08_authorization_review_20260601.json"
Q = ROOT / "reports/upbit_gate22_wf08_authorization_review_closing_qa_2026-06-01.md"
V = ROOT / "reports/upbit_gate22_wf08_authorization_review_final_verdict_2026-06-01.md"

class Gate22ReviewTest(unittest.TestCase):
    def test_files_exist(self):
        for p in [R, J, Q, V, Path(__file__)]:
            self.assertTrue(p.exists(), str(p))

    def test_required_blocks(self):
        t = R.read_text(encoding="utf-8-sig")
        self.assertIn("What WF08 Is Forbidden To Execute", t)
        self.assertIn("Why Actual WF08 Remains Blocked", t)

    def test_flags_false(self):
        payload = json.loads(J.read_text(encoding="utf-8-sig"))
        a = payload["authorizations"]
        self.assertFalse(a["wf08_execution_authorized"])
        self.assertFalse(a["upbit_api_access"])
        self.assertFalse(a["credential_authorization"])
        self.assertFalse(a["scheduler_authorization"])
        self.assertFalse(a["live_trading_authorization"])

    def test_no_exec_endpoint_pattern(self):
        corpus = "\n".join([R.read_text(encoding="utf-8-sig"), J.read_text(encoding="utf-8-sig"), V.read_text(encoding="utf-8-sig")])
        self.assertIsNone(re.search(r"requests\.(get|post|put|delete)\(\s*['\"]https://api\.upbit\.com/v1/(orders|order|accounts|withdraws|transfers)", corpus, re.IGNORECASE))

    def test_verdict_key(self):
        self.assertIn("PASS_GATE22_WF08_AUTHORIZATION_REVIEW_ONLY", V.read_text(encoding="utf-8-sig"))

if __name__ == "__main__":
    unittest.main()
