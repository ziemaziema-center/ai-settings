import json
import unittest
from pathlib import Path


class TestExtendedObservationDigestsExist(unittest.TestCase):
    def test_cycle_digest_files(self):
        payload = json.loads(Path("reports/offline_artifacts/public_data_shadow_run/public_data_extended_observation_result_v1.json").read_text(encoding="utf-8"))
        digest_dir = Path("reports/offline_artifacts/public_data_shadow_run/extended_daily_digests")
        for i in range(1, payload["cycles_completed"] + 1):
            self.assertTrue((digest_dir / f"cycle_{i:03d}.md").exists())


if __name__ == "__main__":
    unittest.main()
