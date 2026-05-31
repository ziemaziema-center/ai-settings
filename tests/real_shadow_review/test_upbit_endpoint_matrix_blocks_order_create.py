from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestUpbitEndpointMatrixBlocksOrderCreate(unittest.TestCase):
    def test_upbit_endpoint_matrix_blocks_order_create(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "real_shadow_review" / "upbit_endpoint_allow_block_matrix_v1.md").read_text(encoding="utf-8")
        self.assertIn("order create", text.lower())
        self.assertIn("HARD_BLOCKED", text)


if __name__ == "__main__":
    unittest.main()
