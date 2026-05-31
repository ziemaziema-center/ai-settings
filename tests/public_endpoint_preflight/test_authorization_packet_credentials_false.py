from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestAuthorizationPacketCredentialsFalse(unittest.TestCase):
    def test_authorization_packet_credentials_false(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_endpoint_preflight" / "public_endpoint_preflight_authorization_packet_template_v1.md").read_text(encoding="utf-8")
        self.assertIn("credential_use: false", text)
        self.assertIn("auth_header: absent", text)
if __name__ == "__main__":
    unittest.main()
