import unittest
from pathlib import Path


class TestOneShotResultDoesNotAuthorizeShadowLive(unittest.TestCase):
    def test_non_authorization_sentence_present(self):
        path = Path("reports/offline_artifacts/public_endpoint_preflight/one_shot_public_quotation_preflight_result_v1.md")
        text = path.read_text(encoding="utf-8")
        self.assertIn("does not authorize live trading", text)
        self.assertIn("does not authorize credential use, shadow execution", text)


if __name__ == "__main__":
    unittest.main()
