import json
import unittest
from pathlib import Path


class TestLongObservationRequestLimit(unittest.TestCase):
    def test_limit(self):
        payload = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/public_data_long_observation_result_v1.json").read_text(encoding="utf-8"))
        self.assertLessEqual(payload["total_request_count"], 336)
        self.assertLessEqual(payload["cycles_completed"], 112)


if __name__ == "__main__":
    unittest.main()
