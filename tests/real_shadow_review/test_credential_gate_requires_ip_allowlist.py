from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestCredentialGateRequiresIpAllowlist(unittest.TestCase):
    def test_credential_gate_requires_ip_allowlist(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "credential_governance" / "real_shadow_credential_data_access_gate_review_v1.md").read_text(encoding="utf-8")
        self.assertIn("IP allowlist mandatory", text)
        self.assertIn("STOP if IP allowlist is missing", text)


if __name__ == "__main__":
    unittest.main()
