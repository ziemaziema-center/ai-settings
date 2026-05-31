import unittest
from pathlib import Path


class TestBlockerMatrixV3PreservesHardBlocks(unittest.TestCase):
    def test_blocks(self):
        t = Path("reports/offline_artifacts/public_data_shadow_run/public_data_shadow_next_gate_blocker_matrix_v3.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(t.count("| BLOCKED |"), 8)
        self.assertIn("credential authorization missing", t)
        self.assertIn("live authorization blocked", t)


if __name__ == "__main__":
    unittest.main()
