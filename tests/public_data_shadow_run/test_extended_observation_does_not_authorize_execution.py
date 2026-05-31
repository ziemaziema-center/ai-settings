import unittest
from pathlib import Path


class TestExtendedObservationDoesNotAuthorizeExecution(unittest.TestCase):
    def test_non_approval_statement(self):
        text = Path("reports/offline_artifacts/public_data_shadow_run/public_data_extended_observation_readiness_v1.md").read_text(encoding="utf-8")
        self.assertIn("does not approve execution", text)
        self.assertIn("does not authorize live trading", text)


if __name__ == "__main__":
    unittest.main()
