from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET_DIRS = [
    ROOT / "reports" / "offline_artifacts" / "stress_harness",
    ROOT / "reports" / "offline_artifacts" / "local_dry_run",
]
FORBIDDEN_PATTERNS = ["os.environ", "dotenv", "keyring", "win32cred", "Credential Manager", "UPBIT_ACCESS_KEY", "UPBIT_SECRET_KEY"]


class TestNoEnvOrCredentialsPreLive(unittest.TestCase):
    def test_no_env_or_credentials_pre_live(self) -> None:
        offenders = []
        for directory in TARGET_DIRS:
            for file_path in sorted(directory.glob("*.py")):
                text = file_path.read_text(encoding="utf-8")
                for pattern in FORBIDDEN_PATTERNS:
                    if pattern in text:
                        offenders.append(f"{file_path}:{pattern}")
        self.assertFalse(offenders, f"Forbidden env/credential pattern found: {offenders}")


if __name__ == "__main__":
    unittest.main()
