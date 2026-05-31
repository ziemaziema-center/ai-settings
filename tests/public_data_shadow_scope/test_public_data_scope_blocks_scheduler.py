from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestPublicDataScopeBlocksScheduler(unittest.TestCase):
    def test_public_data_scope_blocks_scheduler(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_data_shadow_scope" / "manual_execution_no_scheduler_scope_v1.md").read_text(encoding="utf-8").lower()
        self.assertIn("scheduler is not authorized", text)
        self.assertIn("stop if scheduler appears", text)
if __name__ == "__main__":
    unittest.main()
