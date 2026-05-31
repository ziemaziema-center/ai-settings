import unittest
from pathlib import Path
from _test_utils import NON_AUTHORIZATION_SENTENCE, ROOT


class TestNonAuthorizationSentencePresent(unittest.TestCase):
    def test_non_authorization_sentence_present(self):
        paths = [
            ROOT / "reports" / "offline_artifacts" / "offline_test_harness" / "offline_synthetic_harness_design_v1.md",
            ROOT / "reports" / "offline_artifacts" / "offline_test_harness" / "offline_backtest_result_v1.md",
            ROOT / "reports" / "offline_artifacts" / "scoring" / "offline_strategy_quality_score_report_v1.md",
            ROOT / "reports" / "offline_artifacts" / "reviews" / "offline_synthetic_test_harness_closing_qa_report_v1.md",
            ROOT / "reports" / "offline_artifacts" / "reviews" / "offline_synthetic_test_harness_patch_manifest_v1.md",
            ROOT / "reports" / "offline_artifacts" / "reviews" / "offline_synthetic_test_harness_final_verdict_v1.md",
            ROOT / "reports" / "offline_artifacts" / "manifests" / "offline_synthetic_test_harness_manifest_v1.md",
        ]
        for path in paths:
            if path.exists():
                text = path.read_text(encoding="utf-8")
                self.assertIn(NON_AUTHORIZATION_SENTENCE, text)


if __name__ == "__main__":
    unittest.main()
