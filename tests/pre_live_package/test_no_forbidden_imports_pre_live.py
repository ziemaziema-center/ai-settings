from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET_DIRS = [
    ROOT / "reports" / "offline_artifacts" / "stress_harness",
    ROOT / "reports" / "offline_artifacts" / "local_dry_run",
]
FORBIDDEN_TOKENS = ["requests", "httpx", "aiohttp", "websocket", "websockets", "jwt", "pyupbit", "ccxt", "upbit"]


class TestNoForbiddenImportsPreLive(unittest.TestCase):
    def test_no_forbidden_imports_pre_live(self) -> None:
        offenders = []
        for directory in TARGET_DIRS:
            for file_path in sorted(directory.glob("*.py")):
                text = file_path.read_text(encoding="utf-8")
                for token in FORBIDDEN_TOKENS:
                    if f"import {token}" in text or f"from {token} import" in text:
                        offenders.append(f"{file_path}:{token}")
        self.assertFalse(offenders, f"Forbidden imports found: {offenders}")


if __name__ == "__main__":
    unittest.main()
