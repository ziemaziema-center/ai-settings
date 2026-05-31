from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NON_AUTH = "This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims."


class TestNonAuthorizationSentencePresent(unittest.TestCase):
    def test_non_authorization_sentence_present(self) -> None:
        target_dirs = [
            ROOT / "reports" / "offline_artifacts" / "pre_live_package",
            ROOT / "reports" / "offline_artifacts" / "stress_harness",
            ROOT / "reports" / "offline_artifacts" / "local_dry_run",
            ROOT / "reports" / "offline_artifacts" / "shadow_governance",
            ROOT / "reports" / "offline_artifacts" / "runtime_governance",
            ROOT / "reports" / "offline_artifacts" / "credential_governance",
            ROOT / "reports" / "offline_artifacts" / "deployment_governance",
        ]
        missing = []
        for directory in target_dirs:
            for file_path in sorted(directory.glob("*.md")):
                text = file_path.read_text(encoding="utf-8")
                if NON_AUTH not in text:
                    missing.append(str(file_path))
        self.assertFalse(missing, f"Missing non-authorization sentence: {missing}")


if __name__ == "__main__":
    unittest.main()
