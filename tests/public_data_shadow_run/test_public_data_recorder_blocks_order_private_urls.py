import unittest
from pathlib import Path


class TestPublicDataRecorderBlocksOrderPrivateUrls(unittest.TestCase):
    def test_forbidden_endpoints_defined(self):
        text = Path("reports/offline_artifacts/public_data_shadow_run/public_data_shadow_recorder.py").read_text(encoding="utf-8")
        for token in ['"/v1/accounts"', '"/v1/orders"', '"/v1/order"', '"/v1/withdraws"', '"/v1/deposits"', '"/v1/transfers"']:
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
