import json
import unittest
from pathlib import Path


class TestExtendedObservationNoAuthCredentialsEnv(unittest.TestCase):
    def test_flags(self):
        payload = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/public_data_extended_observation_result_v1.json").read_text(encoding="utf-8"))
        self.assertFalse(payload["auth_header_sent"])
        self.assertFalse(payload["credential_use_in_this_run"])
        self.assertFalse(payload["env_access_in_this_run"])


if __name__ == "__main__":
    unittest.main()
