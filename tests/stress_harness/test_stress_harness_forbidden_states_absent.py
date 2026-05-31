from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HARNESS_DIR = ROOT / "reports" / "offline_artifacts" / "stress_harness"
FORBIDDEN = {"SUBMITTED", "ACK_RECEIVED", "OPEN", "FILLED", "PARTIAL", "LIVE_ORDER", "SHADOW_ORDER", "EXCHANGE_CONNECTED"}


class TestStressHarnessForbiddenStatesAbsent(unittest.TestCase):
    def test_stress_harness_forbidden_states_absent(self) -> None:
        result = json.loads((HARNESS_DIR / "stress_harness_result_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(result["summary"]["forbidden_state_count"], 0)
        for outcome in result["outcomes"]:
            self.assertNotIn(outcome["state"], FORBIDDEN)
            self.assertIs(outcome["forbidden_state_present"], False)


if __name__ == "__main__":
    unittest.main()
