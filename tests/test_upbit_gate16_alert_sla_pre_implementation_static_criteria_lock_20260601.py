from __future__ import annotations
import json
import re
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / r"reports/upbit_gate16_alert_sla_pre_implementation_static_criteria_lock_2026-06-01.md"
RUNTIME = ROOT / r"runtime/upbit_gate16_alert_sla_pre_implementation_static_criteria_lock_20260601.json"
TESTFILE = ROOT / r"tests/test_upbit_gate16_alert_sla_pre_implementation_static_criteria_lock_20260601.py"
QA = ROOT / r"reports/upbit_gate16_alert_sla_pre_implementation_static_criteria_lock_closing_qa_2026-06-01.md"
VERDICT = ROOT / r"reports/upbit_gate16_alert_sla_pre_implementation_static_criteria_lock_final_verdict_2026-06-01.md"
PHASE_ID = "GATE_16_ALERT_SLA_PRE_IMPLEMENTATION_STATIC_CRITERIA_LOCK"
VERDICT_KEY = "PASS_GATE16_ALERT_SLA_PRE_IMPLEMENTATION_STATIC_ONLY"
class TestGATE16ALERT(unittest.TestCase):
    def test_artifacts_exist(self) -> None:
        for p in [REPORT, RUNTIME, TESTFILE, QA, VERDICT]:
            self.assertTrue(p.exists(), str(p))
    def test_phase_id_present(self) -> None:
        self.assertIn(PHASE_ID, REPORT.read_text(encoding="utf-8-sig"))
        self.assertIn(PHASE_ID, VERDICT.read_text(encoding="utf-8-sig"))
    def test_criteria_lock_exists(self) -> None:
        txt = REPORT.read_text(encoding="utf-8-sig")
        self.assertIn("## Static Criteria Lock", txt)
        self.assertIn("Scope is offline governance/spec/static-review only.", txt)
    def test_authorizations_false(self) -> None:
        payload = json.loads(RUNTIME.read_text(encoding="utf-8-sig"))
        auth = payload["authorizations"]
        self.assertFalse(auth["implementation_created"])
        self.assertFalse(auth["upbit_api_access"])
        self.assertFalse(auth["credential_authorization"])
        self.assertFalse(auth["wf08_authorization"])
        self.assertFalse(auth["scheduler_authorization"])
        self.assertFalse(auth["live_trading_authorization"])
        self.assertFalse(auth["parser_execution"])
        self.assertFalse(auth["fixture_creation"])
    def test_no_executable_private_endpoint_call(self) -> None:
        corpus = "\n".join([
            REPORT.read_text(encoding="utf-8-sig"),
            RUNTIME.read_text(encoding="utf-8-sig"),
            QA.read_text(encoding="utf-8-sig"),
            VERDICT.read_text(encoding="utf-8-sig"),
        ])
        patterns = [
            r"requests\.(get|post|put|delete)\(\s*['\"]https://api\.upbit\.com/v1/(orders|order|accounts|withdraws|transfers)",
            r"curl\s+.*api\.upbit\.com/v1/(orders|order|accounts|withdraws|transfers)",
        ]
        for pat in patterns:
            self.assertIsNone(re.search(pat, corpus, re.IGNORECASE))
    def test_no_unsafe_readiness_claim(self) -> None:
        text = REPORT.read_text(encoding="utf-8-sig") + "\n" + VERDICT.read_text(encoding="utf-8-sig")
        for line in text.splitlines():
            low = line.lower()
            if "ready for live" in low:
                self.assertTrue("not ready for live" in low or "false" in low)
    def test_verdict_key_present(self) -> None:
        txt = VERDICT.read_text(encoding="utf-8-sig")
        self.assertIn(VERDICT_KEY, txt)
        for field in [
            "phase_id",
            "overall_status",
            "scope",
            "artifacts_created",
            "tests_run",
            "tests_passed",
            "static_scan_status",
            "closing_qa_status",
            "implementation_created: false",
            "upbit_api_access: false",
            "credential_authorization: false",
            "wf08_authorization: false",
            "scheduler_authorization: false",
            "live_trading_authorization: false",
            "parser_execution: false",
            "fixture_creation: false",
            "git_commit_status",
            "git_push_status",
            "remaining_blockers",
            "next_action",
        ]:
            self.assertIn(field, txt)
if __name__ == "__main__":
    unittest.main()
