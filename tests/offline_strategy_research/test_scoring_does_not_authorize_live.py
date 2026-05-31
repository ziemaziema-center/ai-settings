import unittest
from pathlib import Path
from _test_utils import ROOT, SCORE_INTERPRETATION_SENTENCE, run_backtest


class TestScoringDoesNotAuthorizeLive(unittest.TestCase):
    def test_scoring_does_not_authorize_live(self):
        run_backtest()
        report = ROOT / "reports" / "offline_artifacts" / "scoring" / "offline_strategy_quality_score_report_v1.md"
        self.assertTrue(report.exists(), "Score report is missing")

        text = report.read_text(encoding="utf-8")
        self.assertIn(SCORE_INTERPRETATION_SENTENCE, text)
        self.assertIn("does not authorize trading", text)
        self.assertIn("does not authorize shadow/live/WF08", text)
        self.assertNotIn("profit guarantee", text.lower())


if __name__ == "__main__":
    unittest.main()
