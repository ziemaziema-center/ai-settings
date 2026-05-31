from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestPublicDataScopeDoesNotMarkExecutionComplete(unittest.TestCase):
    def test_public_data_scope_does_not_mark_execution_complete(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_data_shadow_scope" / "public_data_only_shadow_scope_v1.md").read_text(encoding="utf-8").lower()
        self.assertIn("execution_status: not_executed", text)
if __name__ == "__main__":
    unittest.main()
