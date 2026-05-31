import unittest
from pathlib import Path


class TestPublicDataRecorderNoAuthHeader(unittest.TestCase):
    def test_no_authorization_header_literal(self):
        text = Path("reports/offline_artifacts/public_data_shadow_run/public_data_shadow_recorder.py").read_text(encoding="utf-8")
        self.assertNotIn("Authorization", text)


if __name__ == "__main__":
    unittest.main()
