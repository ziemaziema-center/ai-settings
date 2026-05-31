import json
import unittest
from pathlib import Path


class TestPublicDataRunResultSchema(unittest.TestCase):
    def test_required_fields_exist(self):
        payload = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/public_data_shadow_run_result_v1.json").read_text(encoding="utf-8"))
        required = [
            "executed_at_utc", "cycles_requested", "cycles_completed", "total_request_count",
            "endpoints_attempted", "methods_used", "auth_header_sent", "credential_read_attempted",
            "env_access_attempted", "private_endpoint_called", "order_endpoint_called",
            "withdraw_transfer_endpoint_called", "scheduler_used", "live_order_count", "shadow_order_count",
            "stubbed_not_sent_count", "response_statuses", "daily_digest_count", "forbidden_state_count",
            "local_output_only", "run_result"
        ]
        for key in required:
            self.assertIn(key, payload)


if __name__ == "__main__":
    unittest.main()
