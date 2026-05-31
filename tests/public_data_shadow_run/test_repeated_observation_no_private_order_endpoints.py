import json
import unittest
from pathlib import Path


class TestRepeatedObservationNoPrivateOrderEndpoints(unittest.TestCase):
    def test_flags(self):
        p = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/repeated_observation_result_v1.json").read_text(encoding="utf-8"))
        self.assertFalse(p["private_account_endpoint_called"])
        self.assertFalse(p["order_endpoint_called"])
        self.assertFalse(p["withdraw_transfer_endpoint_called"])


if __name__ == "__main__":
    unittest.main()
