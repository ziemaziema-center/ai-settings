import unittest
from pathlib import Path


class TestHumanDecisionPacketRecommendsSafeOption(unittest.TestCase):
    def test_recommended_option(self):
        text = Path("reports/offline_artifacts/public_data_shadow_run/public_data_shadow_evidence_human_decision_packet_v1.md").read_text(encoding="utf-8")
        self.assertIn("## Recommended Option", text)
        self.assertIn("APPROVE_EXTENDED_PUBLIC_DATA_OBSERVATION_SCOPE", text)


if __name__ == "__main__":
    unittest.main()
