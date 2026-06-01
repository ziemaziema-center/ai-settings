from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / r"reports/upbit_gate19_offline_stress_simulation_execution_2026-06-01.md"
RUNTIME = ROOT / r"runtime/upbit_gate19_offline_stress_simulation_execution_20260601.json"
TESTFILE = ROOT / r"tests/test_upbit_gate19_offline_stress_simulation_execution_20260601.py"
QA = ROOT / r"reports/upbit_gate19_offline_stress_simulation_execution_closing_qa_2026-06-01.md"
VERDICT = ROOT / r"reports/upbit_gate19_offline_stress_simulation_execution_final_verdict_2026-06-01.md"
PHASE = "GATE_19_OFFLINE_STRESS_SIMULATION_EXECUTION"
VERDICT_KEY = "PASS_GATE19_OFFLINE_STRESS_SIMULATION_ONLY"

class PhaseTest(unittest.TestCase):
    def test_artifacts_exist(self) -> None:
        for path in [REPORT, RUNTIME, TESTFILE, QA, VERDICT]:
            self.assertTrue(path.exists(), str(path))

    def test_phase_and_verdict(self) -> None:
        self.assertIn(PHASE, REPORT.read_text(encoding='utf-8-sig'))
        self.assertIn(VERDICT_KEY, VERDICT.read_text(encoding='utf-8-sig'))

    def test_authorization_flags_false(self) -> None:
        payload = json.loads(RUNTIME.read_text(encoding='utf-8-sig'))
        auth = payload['authorizations']
        for k in [
            'implementation_created','upbit_api_access','credential_authorization','wf08_authorization',
            'scheduler_authorization','live_trading_authorization','parser_execution','fixture_creation'
        ]:
            self.assertFalse(auth[k])

    def test_no_forbidden_endpoint_execution(self) -> None:
        corpus = '\n'.join([
            REPORT.read_text(encoding='utf-8-sig'),
            RUNTIME.read_text(encoding='utf-8-sig'),
            QA.read_text(encoding='utf-8-sig'),
            VERDICT.read_text(encoding='utf-8-sig'),
        ])
        patterns = [
            r"requests\.(get|post|put|delete)\(\s*['\"]https://api\.upbit\.com/v1/(orders|order|accounts|withdraws|transfers)",
            r"curl\s+.*api\.upbit\.com/v1/(orders|order|accounts|withdraws|transfers)",
        ]
        for pat in patterns:
            self.assertIsNone(re.search(pat, corpus, re.IGNORECASE))

    def test_no_unnegated_live_readiness_claim(self) -> None:
        text = REPORT.read_text(encoding='utf-8-sig') + '\n' + VERDICT.read_text(encoding='utf-8-sig')
        for line in text.splitlines():
            low = line.lower()
            if 'ready for live' in low:
                self.assertTrue(('not ready for live' in low) or ('false' in low))

    def test_required_fields_in_verdict(self) -> None:
        txt = VERDICT.read_text(encoding='utf-8-sig')
        required = [
            'phase_id','overall_status','scope','artifacts_created','tests_run','tests_passed','static_scan_status',
            'closing_qa_status','implementation_created: false','upbit_api_access: false','credential_authorization: false',
            'wf08_authorization: false','scheduler_authorization: false','live_trading_authorization: false',
            'parser_execution: false','fixture_creation: false','git_commit_status','git_push_status','remaining_blockers','next_action'
        ]
        for f in required:
            self.assertIn(f, txt)

if __name__ == '__main__':
    unittest.main()
