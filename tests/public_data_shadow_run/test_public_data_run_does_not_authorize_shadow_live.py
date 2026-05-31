import unittest
from pathlib import Path


class TestPublicDataRunDoesNotAuthorizeShadowLive(unittest.TestCase):
    def test_non_authorization_sentence_present(self):
        text = Path("reports/offline_artifacts/public_data_shadow_run/public_data_shadow_run_result_v1.md").read_text(encoding="utf-8")
        self.assertIn("does not authorize live trading", text)
        self.assertIn("does not authorize credential use, authenticated shadow execution", text)


if __name__ == "__main__":
    unittest.main()
