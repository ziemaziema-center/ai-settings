import json
import unittest
from pathlib import Path


class TestLongObservationDigestsExist(unittest.TestCase):
    def test_digests(self):
        payload = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/public_data_long_observation_result_v1.json").read_text(encoding="utf-8"))
        digest_dir = Path("reports/offline_artifacts/public_data_shadow_run/long_observation_digests")
        digests = sorted(digest_dir.glob("cycle_*.md"))
        self.assertEqual(len(digests), payload["cycles_completed"])


if __name__ == "__main__":
    unittest.main()
