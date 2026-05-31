from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestPublicDataScopeBlocksCredentials(unittest.TestCase):
    def test_public_data_scope_blocks_credentials(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_data_shadow_scope" / "public_data_only_shadow_scope_v1.md").read_text(encoding="utf-8").lower()
        self.assertIn("credential", text)
        self.assertIn("hard blocked", text)
if __name__ == "__main__":
    unittest.main()
