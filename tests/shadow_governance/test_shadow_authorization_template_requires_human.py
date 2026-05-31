from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestShadowAuthorizationTemplateRequiresHuman(unittest.TestCase):
    def test_shadow_authorization_template_requires_human(self) -> None:
        path = ROOT / "reports" / "offline_artifacts" / "shadow_governance" / "controlled_shadow_authorization_packet_template_v1.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("human_approver", text)
        self.assertIn("This template is not an approval.", text)


if __name__ == "__main__":
    unittest.main()
