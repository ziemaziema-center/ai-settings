import unittest
from pathlib import Path


class TestOneShotScriptBlocksOrderPrivateUrls(unittest.TestCase):
    def test_forbidden_endpoints_are_listed_for_blocking(self):
        path = Path("reports/offline_artifacts/public_endpoint_preflight/one_shot_public_quotation_preflight.py")
        text = path.read_text(encoding="utf-8")
        required_forbidden = [
            '"/v1/accounts"',
            '"/v1/orders"',
            '"/v1/order"',
            '"/v1/withdraws"',
            '"/v1/deposits"',
            '"/v1/transfers"',
        ]
        for token in required_forbidden:
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
