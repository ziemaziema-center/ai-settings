import unittest
from pathlib import Path


class TestPublicDataRunDailyDigests(unittest.TestCase):
    def test_day_01_to_day_14_exist(self):
        base = Path("reports/offline_artifacts/public_data_shadow_run/daily_digests")
        expected = [base / f"day_{i:02d}.md" for i in range(1, 15)]
        for path in expected:
            self.assertTrue(path.exists(), str(path))


if __name__ == "__main__":
    unittest.main()
