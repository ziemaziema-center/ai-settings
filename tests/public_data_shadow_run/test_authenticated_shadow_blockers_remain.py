import unittest
from pathlib import Path


class TestAuthenticatedShadowBlockersRemain(unittest.TestCase):
    def test_blockers_remain_blocked(self):
        text = Path("reports/offline_artifacts/shadow_governance/authenticated_shadow_review_blocker_matrix_v1.md").read_text(encoding="utf-8")
        self.assertIn("CRED_AUTH_MISSING", text)
        self.assertIn("WF08_BLOCKED", text)
        self.assertGreaterEqual(text.count("| BLOCKED |"), 10)


if __name__ == "__main__":
    unittest.main()
