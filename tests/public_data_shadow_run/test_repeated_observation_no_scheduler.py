import json
import unittest
from pathlib import Path


class TestRepeatedObservationNoScheduler(unittest.TestCase):
    def test_flag(self):
        p = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/repeated_observation_result_v1.json").read_text(encoding="utf-8"))
        self.assertFalse(p["scheduler_use_in_this_run"])


if __name__ == "__main__":
    unittest.main()
