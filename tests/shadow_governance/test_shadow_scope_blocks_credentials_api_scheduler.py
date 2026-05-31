from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class TestShadowScopeBlocksCredentialsApiScheduler(unittest.TestCase):
    def test_shadow_scope_blocks_credentials_api_scheduler(self) -> None:
        path = ROOT / "reports" / "offline_artifacts" / "shadow_governance" / "controlled_n_day_shadow_scope_v1.md"
        text = path.read_text(encoding="utf-8").lower()
        self.assertIn("no upbit api", text)
        self.assertIn("no credentials", text)
        self.assertIn("no scheduler activation", text)


if __name__ == "__main__":
    unittest.main()
