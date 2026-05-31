import json
import unittest
from pathlib import Path


class TestExtendedObservationStubbedNotSent(unittest.TestCase):
    def test_stubbed_counts(self):
        payload = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/public_data_extended_observation_result_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["stubbed_not_sent_count"], payload["cycles_completed"])
        self.assertEqual(payload["live_order_count"], 0)
        self.assertEqual(payload["shadow_order_count"], 0)


if __name__ == "__main__":
    unittest.main()
