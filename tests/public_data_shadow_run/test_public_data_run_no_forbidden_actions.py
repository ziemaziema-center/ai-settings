import json
import unittest
from pathlib import Path


class TestPublicDataRunNoForbiddenActions(unittest.TestCase):
    def test_safety_flags(self):
        payload = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/public_data_shadow_run_result_v1.json").read_text(encoding="utf-8"))
        self.assertFalse(payload["auth_header_sent"])
        self.assertFalse(payload["credential_read_attempted"])
        self.assertFalse(payload["env_access_attempted"])
        self.assertFalse(payload["private_endpoint_called"])
        self.assertFalse(payload["order_endpoint_called"])
        self.assertFalse(payload["withdraw_transfer_endpoint_called"])
        self.assertFalse(payload["scheduler_used"])
        self.assertEqual(payload["live_order_count"], 0)
        self.assertEqual(payload["shadow_order_count"], 0)
        self.assertEqual(payload["forbidden_state_count"], 0)


if __name__ == "__main__":
    unittest.main()
