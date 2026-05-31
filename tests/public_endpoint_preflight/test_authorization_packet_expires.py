from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestAuthorizationPacketExpires(unittest.TestCase):
    def test_authorization_packet_expires(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_endpoint_preflight" / "public_endpoint_preflight_authorization_packet_template_v1.md").read_text(encoding="utf-8")
        self.assertIn("approval_expiration_utc", text)
if __name__ == "__main__":
    unittest.main()
