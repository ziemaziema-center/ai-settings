from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestNoSubmitArchitectureBlocksPrivateEndpoints(unittest.TestCase):
    def test_no_submit_architecture_blocks_private_endpoints(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_data_shadow_scope" / "public_data_shadow_no_submit_architecture_v1.md").read_text(encoding="utf-8").lower()
        self.assertIn("no private endpoint", text)
if __name__ == "__main__":
    unittest.main()
