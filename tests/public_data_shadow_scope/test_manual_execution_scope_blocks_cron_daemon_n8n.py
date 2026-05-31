from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestManualExecutionScopeBlocksCronDaemonN8N(unittest.TestCase):
    def test_manual_execution_scope_blocks_cron_daemon_n8n(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_data_shadow_scope" / "manual_execution_no_scheduler_scope_v1.md").read_text(encoding="utf-8").lower()
        self.assertIn("no cron", text)
        self.assertIn("no background daemon", text)
        self.assertIn("no n8n workflow activation", text)
if __name__ == "__main__":
    unittest.main()
