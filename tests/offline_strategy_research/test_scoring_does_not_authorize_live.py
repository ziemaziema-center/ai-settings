import unittest
from pathlib import Path
from _test_utils import ROOT, SCORE_INTERPRETATION_SENTENCE, run_backtest


class TestScoringDoesNotAuthorizeLive(unittest.TestCase):
    def test_scoring_does_not_authorize_live(self):
        run_backtest()
        report = ROOT / "reports" / "offline_artifacts" / "scoring" / "offline_strategy_quality_score_report_v1.md"
        if report.exists():
            text = report.read_text(encoding="utf-8")
            self.assertIn(SCORE_INTERPRETATION_SENTENCE, text)


if __name__ == "__main__":
    unittest.main()
