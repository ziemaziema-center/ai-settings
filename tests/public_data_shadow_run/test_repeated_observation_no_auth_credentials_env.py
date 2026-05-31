import json
import unittest
from pathlib import Path


class TestRepeatedObservationNoAuthCredentialsEnv(unittest.TestCase):
    def test_flags(self):
        p = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/repeated_observation_result_v1.json").read_text(encoding="utf-8"))
        self.assertFalse(p["auth_header_sent"])
        self.assertFalse(p["credential_use_in_this_run"])
        self.assertFalse(p["env_access_in_this_run"])


if __name__ == "__main__":
    unittest.main()
