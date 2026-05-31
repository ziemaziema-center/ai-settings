import unittest
from pathlib import Path


class TestPublicDataRecorderNoCredentialsEnv(unittest.TestCase):
    def test_no_forbidden_env_credential_tokens(self):
        text = Path("reports/offline_artifacts/public_data_shadow_run/public_data_shadow_recorder.py").read_text(encoding="utf-8")
        forbidden = ["os.environ", "dotenv", "keyring", "win32cred", "pyupbit", "ccxt", "requests", "httpx", "aiohttp", "websocket", "websockets", "jwt"]
        for token in forbidden:
            self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
