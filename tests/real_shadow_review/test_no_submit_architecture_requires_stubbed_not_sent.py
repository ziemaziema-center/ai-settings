from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestNoSubmitArchitectureRequiresStubbedNotSent(unittest.TestCase):
    def test_no_submit_architecture_requires_stubbed_not_sent(self) -> None:
        text = (ROOT / "reports" / "offline_artifacts" / "real_shadow_review" / "real_shadow_no_submit_architecture_v1.md").read_text(encoding="utf-8")
        self.assertIn("STUBBED_NOT_SENT", text)
        self.assertIn("no exchange submission", text)


if __name__ == "__main__":
    unittest.main()
