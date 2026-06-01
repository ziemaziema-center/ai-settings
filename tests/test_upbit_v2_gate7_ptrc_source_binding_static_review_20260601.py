from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/upbit_v2_gate7_ptrc_source_binding_static_review_2026-06-01.md"
RUNTIME = ROOT / "runtime/upbit_v2_gate7_ptrc_source_binding_static_review_20260601.json"
VERDICT = ROOT / "reports/upbit_v2_gate7_ptrc_final_verdict_2026-06-01.md"
QA = ROOT / "reports/upbit_v2_gate7_ptrc_closing_qa_2026-06-01.md"

REQUIRED_ITEMS = [
    "max_order_notional_krw",
    "max_position_notional_krw",
    "max_aggregate_exposure_krw",
    "pre_held_krw_balance_required",
    "daily_loss_cap",
    "intraday_drawdown_cap",
    "max_price_deviation_pct_vs_last_trade",
    "max_price_deviation_pct_vs_orderbook_mid",
    "min_tick_size_compliance",
    "min_order_size_compliance",
    "ord_type == limit",
    "ord_type != market",
    "no_leverage",
    "no_margin",
    "per_second_budget_remaining",
    "per_market_order_burst_limit",
    "per_minute_max_orders",
    "client_order_id_unique_in_window",
    "no_identical_order_within_N_seconds",
    "market_in_allowlist",
    "market_warning_status == NONE",
    "wallet_state == working",
    "can_trade flag verified",
    "not restricted",
    "not scheduled maintenance",
]

REQUIRED_FINAL_REPORT_FIELDS = [
    "working_directory_status",
    "overall_status",
    "gate",
    "ptrc_source_binding_status",
    "ptrc_required_items_count",
    "ptrc_items_passed",
    "ptrc_items_blocked",
    "live_trading_authorization: false",
    "credential_authorization: false",
    "wf08_authorization: false",
    "scheduler_authorization: false",
    "upbit_api_access: false",
    "parser_execution: false",
    "fixture_creation: false",
    "tests_run",
    "tests_passed",
    "closing_qa_status",
    "files_created",
    "files_modified",
    "git_commit_status",
    "git_push_status",
    "remaining_blockers",
    "next_action",
    "final_safety_verdict",
]


class Gate7PtrcSourceBindingTests(unittest.TestCase):
    def test_artifacts_exist(self) -> None:
        for p in [REPORT, RUNTIME, VERDICT, QA]:
            self.assertTrue(p.exists(), str(p))

    def test_all_required_ptrc_items_present(self) -> None:
        text = REPORT.read_text(encoding="utf-8-sig")
        for item in REQUIRED_ITEMS:
            self.assertIn(item, text)

    def test_all_items_remain_spec_only_not_implemented_blocked(self) -> None:
        text = REPORT.read_text(encoding="utf-8-sig")
        self.assertIn("implementation_status_uniform: SPEC_ONLY", text)
        self.assertIn("runtime_status_uniform: NOT_IMPLEMENTED", text)
        self.assertIn("live_status_uniform: BLOCKED", text)

    def test_no_live_or_credential_authorization(self) -> None:
        payload = json.loads(RUNTIME.read_text(encoding="utf-8-sig"))
        auth = payload["authorizations"]
        self.assertFalse(auth["live_trading_authorization"])
        self.assertFalse(auth["credential_authorization"])
        self.assertFalse(auth["wf08_authorization"])
        self.assertFalse(auth["scheduler_authorization"])
        self.assertFalse(auth["upbit_api_access"])

    def test_no_private_order_account_withdraw_transfer_calls(self) -> None:
        corpus = "\n".join([
            REPORT.read_text(encoding="utf-8-sig"),
            RUNTIME.read_text(encoding="utf-8-sig"),
            VERDICT.read_text(encoding="utf-8-sig"),
        ])
        forbidden_call_patterns = [
            r"requests\.(get|post|delete|put)\(\s*['\"]https://api\.upbit\.com/v1/(orders|order|accounts|withdraws|transfers)",
            r"curl\s+.*api\.upbit\.com/v1/(orders|order|accounts|withdraws|transfers)",
        ]
        for pattern in forbidden_call_patterns:
            self.assertIsNone(re.search(pattern, corpus, re.IGNORECASE))

    def test_rejection_behavior_and_capital_breach_requirements(self) -> None:
        text = REPORT.read_text(encoding="utf-8-sig")
        self.assertIn("STOP + LOG + ALERT", text)
        self.assertIn("cancel outstanding orders + disable new entry + human re-arm", text)

    def test_final_verdict_static_review_only_not_implementation(self) -> None:
        text = VERDICT.read_text(encoding="utf-8-sig")
        self.assertIn("GATE_7 is static-review complete only, not implementation complete.", text)
        self.assertIn("PASS_GATE7_PTRC_SPEC_SOURCE_BINDING_ONLY", text)

    def test_final_report_fields_present(self) -> None:
        text = VERDICT.read_text(encoding="utf-8-sig")
        for field in REQUIRED_FINAL_REPORT_FIELDS:
            self.assertIn(field, text)

    def test_final_lines_present(self) -> None:
        text = VERDICT.read_text(encoding="utf-8-sig")
        self.assertIn("GATE_7 PTRC SPEC SOURCE-BINDING STATIC REVIEW COMPLETED.", text)
        self.assertIn("PTRC IMPLEMENTATION STILL BLOCKED.", text)
        self.assertIn("LIVE TRADING STILL BLOCKED.", text)
        self.assertIn("NO UPBIT API/CREDENTIAL/ORDER/SCHEDULER/WF08 AUTHORIZATION GRANTED.", text)


if __name__ == "__main__":
    unittest.main()
