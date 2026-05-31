from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HARNESS_DIR = ROOT / "reports" / "offline_artifacts" / "stress_harness"


class TestStressHarnessResultSchema(unittest.TestCase):
    def test_stress_harness_result_schema(self) -> None:
        schema = json.loads((HARNESS_DIR / "stress_result_schema_v1.json").read_text(encoding="utf-8-sig"))
        result = json.loads((HARNESS_DIR / "stress_harness_result_v1.json").read_text(encoding="utf-8-sig"))
        for key in schema["required_top_level_keys"]:
            self.assertIn(key, result)
        for key in schema["summary_required_keys"]:
            self.assertIn(key, result["summary"])
        self.assertTrue(result["outcomes"])
        for key in schema["outcome_required_keys"]:
            self.assertIn(key, result["outcomes"][0])


if __name__ == "__main__":
    unittest.main()
