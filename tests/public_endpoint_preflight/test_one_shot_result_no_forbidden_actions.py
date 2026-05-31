import json
import unittest
from pathlib import Path


class TestOneShotResultNoForbiddenActions(unittest.TestCase):
    def test_forbidden_flags_are_false(self):
        path = Path("reports/offline_artifacts/public_endpoint_preflight/one_shot_public_quotation_preflight_result_v1.json")
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertFalse(payload["auth_header_sent"])
        self.assertFalse(payload["credential_read_attempted"])
        self.assertFalse(payload["env_access_attempted"])
        self.assertFalse(payload["private_endpoint_called"])
        self.assertFalse(payload["order_endpoint_called"])
        self.assertFalse(payload["scheduler_used"])
        self.assertTrue(payload["local_output_only"])


if __name__ == "__main__":
    unittest.main()
