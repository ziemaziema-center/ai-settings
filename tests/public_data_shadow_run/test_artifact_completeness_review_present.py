import unittest
from pathlib import Path


class TestArtifactCompletenessReviewPresent(unittest.TestCase):
    def test_present(self):
        t = Path("reports/offline_artifacts/overnight/overnight_artifact_completeness_review_v1.md").read_text(encoding="utf-8")
        self.assertIn("artifact_completeness_status: PASS", t)
        self.assertIn("MEDIA_ARTIFACTS_NA", t)


if __name__ == "__main__":
    unittest.main()
