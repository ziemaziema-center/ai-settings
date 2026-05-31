from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestCommandDesignNoExecutableNetworkCode(unittest.TestCase):
    def test_command_design_no_executable_network_code(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_endpoint_preflight" / "future_public_endpoint_preflight_command_design_v1.md").read_text(encoding="utf-8")
        self.assertIn("Do not create executable network code in this run.", text)
if __name__ == "__main__":
    unittest.main()
