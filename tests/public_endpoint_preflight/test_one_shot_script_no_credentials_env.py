import unittest
from pathlib import Path


class TestOneShotScriptNoCredentialsEnv(unittest.TestCase):
    def test_no_env_or_credential_import_or_access(self):
        path = Path("reports/offline_artifacts/public_endpoint_preflight/one_shot_public_quotation_preflight.py")
        text = path.read_text(encoding="utf-8")
        forbidden_tokens = ["os.environ", "dotenv", "keyring", "win32cred", "pyupbit", "ccxt", "jwt"]
        for token in forbidden_tokens:
            self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
