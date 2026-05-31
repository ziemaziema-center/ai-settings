from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestAuthorizationTemplateRequiresHuman(unittest.TestCase):
    def test_authorization_template_requires_human(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_data_shadow_scope" / "public_data_shadow_authorization_packet_template_v1.md").read_text(encoding="utf-8")
        self.assertIn("human_approver", text)
        self.assertIn("This template is not approval.", text)
if __name__ == "__main__":
    unittest.main()
