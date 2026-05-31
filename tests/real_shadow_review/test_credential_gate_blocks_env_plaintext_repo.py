from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestCredentialGateBlocksEnvPlaintextRepo(unittest.TestCase):
    def test_credential_gate_blocks_env_plaintext_repo(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "credential_governance" / "real_shadow_credential_data_access_gate_review_v1.md").read_text(encoding="utf-8")
        self.assertIn("no .env storage", text)
        self.assertIn("no plaintext storage", text)
        self.assertIn("no repository storage", text)


if __name__ == "__main__":
    unittest.main()
