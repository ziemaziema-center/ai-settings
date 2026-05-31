import json
import unittest
from pathlib import Path


class TestRepeatedObservationDigestsExist(unittest.TestCase):
    def test_count(self):
        p = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/repeated_observation_result_v1.json").read_text(encoding="utf-8"))
        d = sorted(Path("reports/offline_artifacts/public_data_shadow_run/repeated_observation_digests").glob("window_*/cycle_*.md"))
        self.assertEqual(len(d), p["total_cycles_completed"])


if __name__ == "__main__":
    unittest.main()
