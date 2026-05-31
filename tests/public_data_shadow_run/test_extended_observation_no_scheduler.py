import json
import unittest
from pathlib import Path


class TestExtendedObservationNoScheduler(unittest.TestCase):
    def test_scheduler_false(self):
        payload = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/public_data_extended_observation_result_v1.json").read_text(encoding="utf-8"))
        self.assertFalse(payload["scheduler_use_in_this_run"])


if __name__ == "__main__":
    unittest.main()
