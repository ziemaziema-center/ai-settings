from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestCredentialFreeChecklistBlocksEnvCredentials(unittest.TestCase):
    def test_credential_free_checklist_blocks_env_credentials(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_endpoint_preflight" / "credential_free_public_endpoint_feasibility_checklist_v1.md").read_text(encoding="utf-8")
        self.assertIn("must not read `.env`", text)
        self.assertIn("must not read Windows Credential Manager", text)
if __name__ == "__main__":
    unittest.main()
