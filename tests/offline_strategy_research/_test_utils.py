from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[2]
HARNESS_DIR = ROOT / "reports" / "offline_artifacts" / "offline_test_harness"
SCORING_DIR = ROOT / "reports" / "offline_artifacts" / "scoring"

if str(HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(HARNESS_DIR))

NON_AUTHORIZATION_SENTENCE = (
    "This document does not authorize live trading, shadow mode, Upbit API access, credential use, "
    "scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, "
    "implementation, or production-readiness claims."
)

SCORE_INTERPRETATION_SENTENCE = (
    "Offline quality score measures offline artifact/test completeness only; it does not indicate "
    "profit expectation, trading performance, runtime readiness, shadow readiness, live readiness, "
    "or WF08 readiness."
)


def load_module(module_name: str, file_name: str):
    file_path = HARNESS_DIR / file_name
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module: {file_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_backtest(*, tests_passed: bool = False, manifest_traceability: bool = False) -> Dict[str, Any]:
    runner = load_module("offline_backtest_runner", "offline_backtest_runner.py")
    return runner.run_offline_backtest(
        write_reports=True,
        tests_passed=tests_passed,
        manifest_traceability=manifest_traceability,
    )


def read_backtest_json() -> Dict[str, Any]:
    path = HARNESS_DIR / "offline_backtest_result_v1.json"
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def harness_python_files():
    return sorted(HARNESS_DIR.glob("*.py"))


def harness_md_reports():
    return sorted(HARNESS_DIR.glob("*.md"))
