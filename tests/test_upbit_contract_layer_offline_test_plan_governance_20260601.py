from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/upbit_contract_layer_offline_test_plan_governance_2026-06-01.md"
RUNTIME = ROOT / "runtime/upbit_contract_layer_offline_test_plan_governance_20260601.json"
TESTFILE = ROOT / "tests/test_upbit_contract_layer_offline_test_plan_governance_20260601.py"
QA = ROOT / "reports/upbit_contract_layer_offline_test_plan_closing_qa_2026-06-01.md"
VERDICT = ROOT / "reports/upbit_contract_layer_offline_test_plan_final_verdict_2026-06-01.md"

LAYERS = ["PTRC", "IDEM", "RECON", "KILL", "ALERT", "HEART", "BUDGET", "OSM"]
REQUIRED_ASSERTIONS = [
    "every order intent must pass pre-trade validation",
    "any failed check rejects order",
    "rejection logs reason/check_id/raw_intent_hash",
    "alert dependency exists",
    "repeated rejection escalates to KILL evaluation",
    "limit order only",
    "market order hard rejected",
    "no margin/leverage",
    "capital threshold breach cancels outstanding orders and disables new entry",
    "UUIDv4 client_order_id required",
    "client_order_id persisted before network send",
    "timeout/5xx/ambiguous response never creates duplicate",
    "retry uses same client_order_id",
    "exchange UUID maps 1:1 to client_order_id",
    "local intent and exchange reality drift detected",
    "orphan exchange order is cancelled",
    "unresolved drift triggers KILL",
    "cold-start full reconciliation required",
    "recovery full reconciliation required after disconnect",
    "KILL is sticky",
    "KILL disables new order entry",
    "KILL cancels open orders",
    "re-arm requires human approval, root cause, reconciliation, hash-chain verification",
    "no auto-clear",
    "actionable alert generated within 5 seconds for KILL/PTRC cluster/RECON drift",
    "alert includes required fields",
    "email-only/silent logging forbidden",
    "stale market data blocks new orders",
    "disconnect beyond grace triggers KILL",
    "clock skew triggers STOP + alert",
    "dead-man watchdog rule exists",
    "Remaining-Req tracked",
    "local token bucket exists",
    "safety margin below Upbit limit",
    "429 triggers backoff + alert",
    "418 triggers KILL + human escalation",
    "every state transition logged",
    "hash-chain covers every transition",
    "LOST state triggers KILL evaluation",
    "no transition without log entry",
]

class OfflineContractLayerTestPlanGovernanceTests(unittest.TestCase):
    def test_all_required_artifacts_exist(self) -> None:
        for p in [REPORT, RUNTIME, TESTFILE, QA, VERDICT]:
            self.assertTrue(p.exists(), str(p))

    def test_all_layers_present(self) -> None:
        text = REPORT.read_text(encoding="utf-8-sig")
        for layer in LAYERS:
            self.assertIn(layer, text)

    def test_required_future_assertions_present(self) -> None:
        text = REPORT.read_text(encoding="utf-8-sig")
        for item in REQUIRED_ASSERTIONS:
            self.assertIn(item, text)

    def test_authorizations_remain_false(self) -> None:
        payload = json.loads(RUNTIME.read_text(encoding="utf-8-sig"))
        auth = payload["authorizations"]
        self.assertFalse(auth["live_trading_authorization"])
        self.assertFalse(auth["credential_authorization"])
        self.assertFalse(auth["wf08_authorization"])
        self.assertFalse(auth["scheduler_authorization"])
        self.assertFalse(auth["upbit_api_access"])
        self.assertFalse(auth["parser_execution"])
        self.assertFalse(auth["fixture_creation"])

    def test_final_verdict_key_present(self) -> None:
        text = VERDICT.read_text(encoding="utf-8-sig")
        self.assertIn("PASS_OFFLINE_TEST_PLAN_GOVERNANCE_ONLY", text)

    def test_no_private_endpoint_executable_call(self) -> None:
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
        for pattern in patterns:
            self.assertIsNone(re.search(pattern, corpus, re.IGNORECASE))

    def test_no_secret_like_strings(self) -> None:
        corpus = "\n".join([
            REPORT.read_text(encoding="utf-8-sig"),
            RUNTIME.read_text(encoding="utf-8-sig"),
            QA.read_text(encoding="utf-8-sig"),
            VERDICT.read_text(encoding="utf-8-sig"),
        ])
        secret_patterns = [
            r"AKIA[0-9A-Z]{16}",
            r"-----BEGIN (?:RSA|EC|OPENSSH|DSA)? ?PRIVATE KEY-----",
            r"UPBIT_SECRET_KEY\s*=\s*\S+",
            r"access_key\s*[:=]\s*['\"][A-Za-z0-9_-]{12,}",
            r"secret\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}",
        ]
        for pattern in secret_patterns:
            self.assertIsNone(re.search(pattern, corpus, re.IGNORECASE))

    def test_no_ready_for_live_wording_unless_negated(self) -> None:
        text = REPORT.read_text(encoding="utf-8-sig") + "\n" + VERDICT.read_text(encoding="utf-8-sig")
        for line in text.splitlines():
            low = line.lower()
            if "ready for live" in low:
                self.assertTrue("not ready for live" in low or "false" in low)


if __name__ == "__main__":
    unittest.main()
