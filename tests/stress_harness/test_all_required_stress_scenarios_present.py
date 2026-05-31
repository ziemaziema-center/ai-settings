from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HARNESS_DIR = ROOT / "reports" / "offline_artifacts" / "stress_harness"
if str(HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(HARNESS_DIR))


def _load_generator_module():
    path = HARNESS_DIR / "synthetic_stress_scenario_generator.py"
    spec = importlib.util.spec_from_file_location("synthetic_stress_scenario_generator", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestAllRequiredStressScenariosPresent(unittest.TestCase):
    def test_all_required_stress_scenarios_present(self) -> None:
        generator = _load_generator_module()
        required = sorted(generator.REQUIRED_SCENARIOS)
        result = json.loads((HARNESS_DIR / "stress_harness_result_v1.json").read_text(encoding="utf-8"))
        observed = sorted(item["scenario"] for item in result["outcomes"])
        self.assertEqual(observed, required)
        self.assertTrue(result["summary"]["all_required_scenarios_present"])


if __name__ == "__main__":
    unittest.main()
