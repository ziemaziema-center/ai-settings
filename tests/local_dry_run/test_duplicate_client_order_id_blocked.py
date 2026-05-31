from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "reports" / "offline_artifacts" / "local_dry_run" / "local_dry_run_result_v1.json"


class TestDuplicateClientOrderIdBlocked(unittest.TestCase):
    def test_duplicate_client_order_id_blocked(self) -> None:
        data = json.loads(RESULT.read_text(encoding="utf-8"))
        row = next(r for r in data["runs"] if r["scenario"] == "duplicate_client_order")
        self.assertEqual(row["result_state"], "IDEM_RETRY_BLOCKED")
        self.assertEqual(row["reason"], "duplicate_client_order_id")


if __name__ == "__main__":
    unittest.main()
