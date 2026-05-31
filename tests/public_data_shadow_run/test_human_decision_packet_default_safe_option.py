import unittest
from pathlib import Path


class TestHumanDecisionPacketDefaultSafeOption(unittest.TestCase):
    def test_recommend_safe(self):
        text = Path("reports/offline_artifacts/public_data_shadow_run/public_data_shadow_evidence_human_decision_packet_v2.md").read_text(encoding="utf-8")
        self.assertIn("recommended_human_option: CONTINUE_PUBLIC_DATA_ONLY_OBSERVATION", text)


if __name__ == "__main__":
    unittest.main()
