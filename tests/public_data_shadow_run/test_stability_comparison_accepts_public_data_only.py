import unittest
from pathlib import Path


class TestStabilityComparisonAcceptsPublicDataOnly(unittest.TestCase):
    def test_conclusion(self):
        text = Path("reports/offline_artifacts/public_data_shadow_run/public_data_observation_stability_comparison_v1.md").read_text(encoding="utf-8")
        self.assertIn("EXTENDED_PUBLIC_DATA_OBSERVATION_ACCEPTED", text)
        self.assertIn("does not authorize live trading", text)


if __name__ == "__main__":
    unittest.main()
