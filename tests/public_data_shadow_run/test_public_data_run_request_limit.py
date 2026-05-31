import json
import unittest
from pathlib import Path


class TestPublicDataRunRequestLimit(unittest.TestCase):
    def test_limits(self):
        payload = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/public_data_shadow_run_result_v1.json").read_text(encoding="utf-8"))
        self.assertLessEqual(payload["cycles_requested"], 14)
        self.assertLessEqual(payload["total_request_count"], 42)


if __name__ == "__main__":
    unittest.main()
