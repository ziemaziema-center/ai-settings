import json
import unittest
from pathlib import Path


class TestLongObservationResultSchema(unittest.TestCase):
    def test_schema(self):
        payload = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/public_data_long_observation_result_v1.json").read_text(encoding="utf-8"))
        required = [
            "cycles_requested", "cycles_completed", "total_request_count", "response_statuses",
            "auth_header_sent", "credential_use_in_this_run", "env_access_in_this_run", "scheduler_use_in_this_run",
            "private_account_endpoint_called", "order_endpoint_called", "withdraw_transfer_endpoint_called",
            "live_order_count", "shadow_order_count", "stubbed_not_sent_count", "run_result"
        ]
        for key in required:
            self.assertIn(key, payload)


if __name__ == "__main__":
    unittest.main()
