from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestShadowRecorderStubbedNotSentRequired(unittest.TestCase):
    def test_shadow_recorder_stubbed_not_sent_required(self) -> None:
        path = ROOT / "reports" / "offline_artifacts" / "shadow_governance" / "shadow_recorder_execution_contract_v1.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("SHADOW_SUBMISSION_STUBBED_NOT_SENT", text)


if __name__ == "__main__":
    unittest.main()
