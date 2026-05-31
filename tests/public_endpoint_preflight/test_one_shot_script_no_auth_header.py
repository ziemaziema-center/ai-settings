import unittest
from pathlib import Path


class TestOneShotScriptNoAuthHeader(unittest.TestCase):
    def test_no_authorization_header_literal(self):
        path = Path("reports/offline_artifacts/public_endpoint_preflight/one_shot_public_quotation_preflight.py")
        text = path.read_text(encoding="utf-8")
        self.assertNotIn("Authorization", text)


if __name__ == "__main__":
    unittest.main()
