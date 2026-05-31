import unittest
from pathlib import Path


class TestMorningDecisionPacketRecommendsSafeOption(unittest.TestCase):
    def test_option(self):
        t = Path("reports/offline_artifacts/overnight/morning_human_decision_packet_v1.md").read_text(encoding="utf-8")
        self.assertIn("recommended_human_option: CONTINUE_PUBLIC_DATA_ONLY_OBSERVATION", t)


if __name__ == "__main__":
    unittest.main()
