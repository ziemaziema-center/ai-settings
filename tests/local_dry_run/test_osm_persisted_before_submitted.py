from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "reports" / "offline_artifacts" / "local_dry_run" / "local_dry_run_result_v1.json"


class TestOsmPersistedBeforeSubmitted(unittest.TestCase):
    def test_osm_persisted_before_submitted(self) -> None:
        data = json.loads(RESULT.read_text(encoding="utf-8"))
        row = next(r for r in data["runs"] if r["scenario"] == "normal_candidate")
        self.assertIn("OSM_INTENT_PERSISTED", row["path"])
        self.assertTrue(row["persisted_before_submitted"])
        self.assertFalse(row["submitted"])


if __name__ == "__main__":
    unittest.main()
