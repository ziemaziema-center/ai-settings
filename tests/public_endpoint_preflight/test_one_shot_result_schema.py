import json
import unittest
from pathlib import Path


class TestOneShotResultSchema(unittest.TestCase):
    def test_required_fields_exist(self):
        path = Path("reports/offline_artifacts/public_endpoint_preflight/one_shot_public_quotation_preflight_result_v1.json")
        payload = json.loads(path.read_text(encoding="utf-8"))
        required_fields = [
            "executed_at_utc",
            "request_count",
            "endpoints_attempted",
            "methods_used",
            "auth_header_sent",
            "credential_read_attempted",
            "env_access_attempted",
            "private_endpoint_called",
            "order_endpoint_called",
            "scheduler_used",
            "response_statuses",
            "response_schema_summary",
            "local_output_only",
            "preflight_result",
        ]
        for field in required_fields:
            self.assertIn(field, payload)


if __name__ == "__main__":
    unittest.main()
