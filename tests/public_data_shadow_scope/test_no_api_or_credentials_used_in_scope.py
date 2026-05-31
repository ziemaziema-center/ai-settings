from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestNoApiOrCredentialsUsedInScope(unittest.TestCase):
    def test_no_api_or_credentials_used_in_scope(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_data_shadow_scope" / "public_data_only_shadow_scope_v1.md").read_text(encoding="utf-8")
        self.assertIn("no Upbit API call is made in this run", text)
        self.assertIn("no credential is used", text)
if __name__ == "__main__":
    unittest.main()
