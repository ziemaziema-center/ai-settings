from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestCommandDesignManualOnlyNoScheduler(unittest.TestCase):
    def test_command_design_manual_only_no_scheduler(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_endpoint_preflight" / "future_public_endpoint_preflight_command_design_v1.md").read_text(encoding="utf-8").lower()
        self.assertIn("manual-only command", text)
        self.assertIn("no scheduler", text)
if __name__ == "__main__":
    unittest.main()
