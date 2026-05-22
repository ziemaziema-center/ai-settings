from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = [
    ROOT / "upbit-helper",
    ROOT / "strategy",
    ROOT / "tests",
    ROOT / "tmp",
    ROOT / "reports",
    ROOT / "workflows",
    ROOT / ".github",
]
SKIP_DIR_NAMES = {".git", "__pycache__", ".pytest_cache"}
SKIP_SUFFIXES = {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".zip", ".pem", ".key"}

PATTERNS = [
    ("AUTH_BEARER_TOKEN", re.compile(r"Authorization['\"]?\s*:\s*['\"]Bearer\s+[A-Za-z0-9_\-.]{20,}", re.I)),
    ("RAW_JWT", re.compile(r"eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}")),
    ("UPBIT_ACCESS_KEY_VALUE", re.compile(r"UPBIT_ACCESS_KEY\s*=\s*[A-Za-z0-9]{20,}")),
    ("UPBIT_SECRET_KEY_VALUE", re.compile(r"UPBIT_SECRET_KEY\s*=\s*[A-Za-z0-9]{20,}")),
    ("TELEGRAM_BOT_TOKEN_VALUE", re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{30,}\b")),
]


def should_scan(path: Path) -> bool:
    if any(part in SKIP_DIR_NAMES for part in path.parts):
        return False
    if path.suffix.lower() in SKIP_SUFFIXES:
        return False
    return path.is_file()


findings: list[dict[str, object]] = []
for base in SCAN_DIRS:
    if not base.exists():
        continue
    for path in base.rglob("*"):
        if not should_scan(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for name, pattern in PATTERNS:
            for match in pattern.finditer(text):
                line_no = text.count("\n", 0, match.start()) + 1
                findings.append({"file": str(path.relative_to(ROOT)), "line": line_no, "type": name})

if findings:
    raise SystemExit("SECRET_SCAN_FAILED " + repr(findings[:20]))

print("SECRET_SCAN_PASS")
