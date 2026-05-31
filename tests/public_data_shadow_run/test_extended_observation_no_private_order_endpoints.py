import json
import unittest
from pathlib import Path


class TestExtendedObservationNoPrivateOrderEndpoints(unittest.TestCase):
    def test_flags(self):
        payload = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/public_data_extended_observation_result_v1.json").read_text(encoding="utf-8"))
        self.assertFalse(payload["private_account_endpoint_called"])
        self.assertFalse(payload["order_endpoint_called"])
        self.assertFalse(payload["withdraw_transfer_endpoint_called"])


if __name__ == "__main__":
    unittest.main()
