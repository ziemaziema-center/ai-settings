import json
import unittest
from pathlib import Path


class TestPublicDataRunNextActionNotStale(unittest.TestCase):
    def test_next_action_updated(self):
        payload = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/public_data_shadow_run_result_v1.json").read_text(encoding="utf-8"))
        self.assertNotEqual(payload.get("next_action"), "OFFLINE_TEST_PLAN_GOVERNANCE_FOR_CONTRACT_LAYER")


if __name__ == "__main__":
    unittest.main()
