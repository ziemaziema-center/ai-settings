from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_MD = ROOT / r"reports/upbit_remaining_gates_blocker_map_2026-06-01.md"
MAP_JSON = ROOT / r"runtime/upbit_remaining_gates_blocker_map_20260601.json"
SENDOFF = ROOT / r"reports/upbit_remaining_gates_session_sendoff_2026-06-01.md"

class TestRemainingBlockerMap(unittest.TestCase):
    def test_outputs_exist(self) -> None:
        for p in [MAP_MD, MAP_JSON, SENDOFF]:
            self.assertTrue(p.exists(), str(p))

    def test_blocks_present(self) -> None:
        text = MAP_MD.read_text(encoding='utf-8-sig')
        self.assertIn('GATE_22 status: BLOCKED_WF08_NOT_AUTHORIZED', text)
        self.assertIn('GATE_23 status: BLOCKED_LIVE_AUTHORIZATION_NOT_GRANTED', text)

    def test_json_fields(self) -> None:
        payload = json.loads(MAP_JSON.read_text(encoding='utf-8-sig'))
        self.assertIn('gate_22_status', payload)
        self.assertIn('gate_23_status', payload)

if __name__ == '__main__':
    unittest.main()
