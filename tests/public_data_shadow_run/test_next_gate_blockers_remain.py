import unittest
from pathlib import Path


class TestNextGateBlockersRemain(unittest.TestCase):
    def test_blockers(self):
        text = Path("reports/offline_artifacts/public_data_shadow_run/public_data_shadow_next_gate_blocker_matrix_v1.md").read_text(encoding="utf-8")
        self.assertIn("credential authorization missing", text)
        self.assertIn("WF08 review blocked", text)
        self.assertGreaterEqual(text.count("| BLOCKED |"), 8)


if __name__ == "__main__":
    unittest.main()
