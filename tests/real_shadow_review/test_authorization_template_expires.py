from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestAuthorizationTemplateExpires(unittest.TestCase):
    def test_authorization_template_expires(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "real_shadow_review" / "real_shadow_execution_authorization_packet_template_v1.md").read_text(encoding="utf-8")
        self.assertIn("authorization_expiration_utc", text)
        self.assertIn("approval expiration", text)


if __name__ == "__main__":
    unittest.main()
