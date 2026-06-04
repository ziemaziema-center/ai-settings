from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
RUNTIME = ROOT / "runtime"

FINAL = REPORTS / "upbit_v2_final_verdict_2026-06-01.md"
GATE_MAP = REPORTS / "upbit_v2_gate_dependency_map_2026-06-01.md"
RUNTIME_JSON = RUNTIME / "upbit_v2_total_completion_20260601.json"

REQUIRED_FILES = [
    REPORTS / "upbit_v2_total_completion_reconciliation_2026-06-01.md",
    REPORTS / "upbit_v2_gate_dependency_map_2026-06-01.md",
    REPORTS / "upbit_v2_immediate_next_action_2026-06-01.md",
    REPORTS / "upbit_v2_open_questions_2026-06-01.md",
    REPORTS / "upbit_v2_risk_reality_check_2026-06-01.md",
    REPORTS / "upbit_v2_completion_scorecard_2026-06-01.md",
    REPORTS / "upbit_v2_closing_qa_report_2026-06-01.md",
    REPORTS / "upbit_v2_patch_manifest_2026-06-01.md",
    FINAL,
    RUNTIME_JSON,
]

FORBIDDEN_AUTH_CLAIMS = [
    "live trading authorized",
    "upbit api authorized",
    "credential authorized",
    "wf08 authorized",
    "scheduler authorized",
    "ready for live",
]

SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9_-]{20,}",
    r"sk-proj-[A-Za-z0-9_-]{20,}",
    r"UPBIT_SECRET_KEY\s*=\s*\S+",
    r"UPBIT_ACCESS_KEY\s*=\s*\S+",
    r"KBIA_TELEGRAM_BOT_TOKEN\s*=\s*\S+",
]

class UpbitV2TotalCompletionTests(unittest.TestCase):
    def test_required_artifacts_exist(self) -> None:
        for p in REQUIRED_FILES:
            self.assertTrue(p.exists(), str(p))

    def test_output_blocks_exist(self) -> None:
        text = FINAL.read_text(encoding="utf-8-sig")
        for block in [
            "[OUTPUT_BLOCK_1] V1_V2_RECONCILIATION_MATRIX",
            "[OUTPUT_BLOCK_2] V2_GATE_DEPENDENCY_MAP",
            "[OUTPUT_BLOCK_3] IMMEDIATE_NEXT_ACTION",
            "[OUTPUT_BLOCK_4] OPEN_QUESTIONS_FOR_HUMAN",
            "[OUTPUT_BLOCK_5] RISK_AND_REALITY_CHECK",
        ]:
            self.assertIn(block, text)

    def test_gate_7_through_23_present(self) -> None:
        text = GATE_MAP.read_text(encoding="utf-8-sig")
        for i in range(7, 24):
            self.assertIn(f"GATE_{i}", text)

    def test_no_forbidden_authorization_claimed(self) -> None:
        corpus = "\n".join(p.read_text(encoding="utf-8-sig") for p in REQUIRED_FILES if p.suffix in {".md", ".json"})
        lower = corpus.lower()
        for claim in FORBIDDEN_AUTH_CLAIMS:
            self.assertNotIn(claim, lower)

    def test_live_credential_wf08_scheduler_blocked(self) -> None:
        payload = json.loads(RUNTIME_JSON.read_text(encoding="utf-8-sig"))
        self.assertFalse(payload["live_trading_authorization"])
        self.assertFalse(payload["credential_authorization"])
        self.assertFalse(payload["wf08_authorization"])
        self.assertFalse(payload["scheduler_authorization"])
        self.assertFalse(payload["upbit_api_access"])

    def test_spec_completion_not_live_authorization_phrase(self) -> None:
        text = FINAL.read_text(encoding="utf-8-sig")
        self.assertIn("SPEC COMPLETION != LIVE AUTHORIZATION", text)

    def test_no_private_order_withdraw_transfer_executable_calls(self) -> None:
        corpus = "\n".join(p.read_text(encoding="utf-8-sig") for p in REQUIRED_FILES if p.suffix in {".md", ".json"})
        forbidden_call_patterns = [
            r"requests\.(get|post|delete|put)\(\s*['\"]https://api\.upbit\.com/v1/(orders|order|accounts|withdraws|transfers)",
            r"curl\s+.*api\.upbit\.com/v1/(orders|order|accounts|withdraws|transfers)",
        ]
        for pattern in forbidden_call_patterns:
            self.assertIsNone(re.search(pattern, corpus, flags=re.IGNORECASE))

    def test_no_secrets(self) -> None:
        corpus = "\n".join(p.read_text(encoding="utf-8-sig") for p in REQUIRED_FILES if p.suffix in {".md", ".json"})
        for pattern in SECRET_PATTERNS:
            self.assertIsNone(re.search(pattern, corpus))

if __name__ == "__main__":
    unittest.main()

