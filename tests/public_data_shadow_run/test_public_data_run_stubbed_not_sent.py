import json
import unittest
from pathlib import Path


class TestPublicDataRunStubbedNotSent(unittest.TestCase):
    def test_stubbed_not_sent_count(self):
        payload = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/public_data_shadow_run_result_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["stubbed_not_sent_count"], payload["cycles_completed"])


if __name__ == "__main__":
    unittest.main()
