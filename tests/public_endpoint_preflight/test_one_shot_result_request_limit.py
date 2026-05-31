import json
import unittest
from pathlib import Path


class TestOneShotResultRequestLimit(unittest.TestCase):
    def test_request_count_within_limit(self):
        path = Path("reports/offline_artifacts/public_endpoint_preflight/one_shot_public_quotation_preflight_result_v1.json")
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertLessEqual(payload["request_count"], 3)


if __name__ == "__main__":
    unittest.main()
