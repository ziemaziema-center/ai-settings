import json
import unittest
from pathlib import Path


class TestRepeatedObservationRequestLimit(unittest.TestCase):
    def test_limits(self):
        p = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/repeated_observation_result_v1.json").read_text(encoding="utf-8"))
        self.assertLessEqual(p["total_request_count"], 504)
        self.assertLessEqual(p["windows_completed"], 3)
        self.assertLessEqual(p["cycles_per_window"], 56)


if __name__ == "__main__":
    unittest.main()
