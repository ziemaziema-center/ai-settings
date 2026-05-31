from __future__ import annotations
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestEndpointMatrixHardBlocksOrderCancel(unittest.TestCase):
    def test_endpoint_matrix_hard_blocks_order_cancel(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "public_data_shadow_scope" / "public_data_shadow_endpoint_hard_block_matrix_v1.md").read_text(encoding="utf-8")
        self.assertIn("order cancel endpoint class", text)
        self.assertIn("HARD_BLOCKED", text)
if __name__ == "__main__":
    unittest.main()
