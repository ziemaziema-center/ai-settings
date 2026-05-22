from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path


CLASSIFIER_VERSION = "wf05-offline-classifier-2026-05-11-v1"
KST = timezone(timedelta(hours=9))
BASE_DIR = Path(__file__).resolve().parent
FIXTURE_PATH = BASE_DIR / "wf05_reconciliation_fixtures_2026-05-11.json"
REPORT_JSON_PATH = BASE_DIR / "wf05_offline_regression_report_2026-05-11.json"
REPORT_MD_PATH = BASE_DIR / "wf05_offline_regression_report_2026-05-11.md"

REQUIRED_CASE_IDS = {
    "wf05_wait",
    "wf05_partial_fill",
    "wf05_done_by_state",
    "wf05_done_by_volume",
    "wf05_cancel",
    "wf05_missing_state",
    "wf05_missing_volume",
    "wf05_malformed_numeric",
    "wf05_negative_volume",
    "wf05_inconsistent_done",
    "wf05_unsupported_state",
    "wf05_helper_error",
}


def parse_non_negative_decimal(value: object) -> Decimal | None:
    if value is None:
        return None
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
    if parsed < 0:
        return None
    return parsed


def classify_order(payload: dict) -> str:
    if payload.get("helper_success") is not True:
        return "unknown_stop"

    state = payload.get("state")
    if not isinstance(state, str) or not state:
        return "unknown_stop"

    remaining_volume = parse_non_negative_decimal(payload.get("remaining_volume"))
    executed_volume = parse_non_negative_decimal(payload.get("executed_volume"))
    if remaining_volume is None or executed_volume is None:
        return "unknown_stop"

    if state == "cancel":
        return "cancel"

    if state == "done":
        if executed_volume > 0 and remaining_volume == 0:
            return "done"
        return "unknown_stop"

    if remaining_volume == 0 and executed_volume > 0:
        return "done"

    if state == "wait" and executed_volume == 0 and remaining_volume > 0:
        return "wait"

    if state == "wait" and executed_volume > 0 and remaining_volume > 0:
        return "partial_fill"

    return "unknown_stop"


def load_fixtures() -> list[dict]:
    with FIXTURE_PATH.open("r", encoding="utf-8") as handle:
        suite = json.load(handle)

    safety_flags = {
        "mode": suite.get("mode"),
        "runtime_calls_allowed": suite.get("runtime_calls_allowed"),
        "workflow_execution_allowed": suite.get("workflow_execution_allowed"),
        "helper_call_allowed": suite.get("helper_call_allowed"),
        "upbit_call_allowed": suite.get("upbit_call_allowed"),
    }
    if safety_flags != {
        "mode": "offline_only",
        "runtime_calls_allowed": False,
        "workflow_execution_allowed": False,
        "helper_call_allowed": False,
        "upbit_call_allowed": False,
    }:
        raise ValueError(f"Fixture suite is not marked offline-only: {safety_flags}")

    fixtures = suite.get("fixtures")
    if not isinstance(fixtures, list):
        raise ValueError("Fixture suite must contain a fixtures list.")

    case_ids = {case.get("id") for case in fixtures}
    missing_case_ids = sorted(REQUIRED_CASE_IDS - case_ids)
    if missing_case_ids:
        raise ValueError(f"Missing required fixture cases: {missing_case_ids}")

    return fixtures


def run_regression() -> tuple[dict, list[dict]]:
    fixtures = load_fixtures()
    case_results = []

    for case in fixtures:
        case_id = case.get("id")
        actual = classify_order(case.get("input", {}))
        expected = case.get("expected_classification")
        passed = actual == expected
        case_results.append(
            {
                "id": case_id,
                "expected_classification": expected,
                "actual_classification": actual,
                "passed": passed,
            }
        )

    failed_case_ids = [result["id"] for result in case_results if not result["passed"]]
    passed_count = len(case_results) - len(failed_case_ids)
    safety_result = "PASS" if not failed_case_ids else "FAIL"
    report = {
        "timestamp_kst": datetime.now(KST).isoformat(timespec="seconds"),
        "fixture_count": len(case_results),
        "passed_count": passed_count,
        "failed_count": len(failed_case_ids),
        "failed_case_ids": failed_case_ids,
        "classifier_version": CLASSIFIER_VERSION,
        "safety_result": safety_result,
        "next_action": "Use this offline runner before any future WF05 patch.",
        "offline_safety": {
            "network_used": False,
            "secrets_loaded": False,
            "helper_called": False,
            "upbit_called": False,
            "n8n_called": False,
            "workflow_executed": False,
            "workflow_modified": False,
            "helper_modified": False,
        },
        "case_results": case_results,
    }
    return report, case_results


def write_json_report(report: dict) -> None:
    with REPORT_JSON_PATH.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def write_markdown_report(report: dict) -> None:
    rows = [
        "| Case ID | Expected | Actual | Result |",
        "| --- | --- | --- | --- |",
    ]
    for case in report["case_results"]:
        result = "PASS" if case["passed"] else "FAIL"
        rows.append(
            f"| {case['id']} | {case['expected_classification']} | "
            f"{case['actual_classification']} | {result} |"
        )

    markdown = f"""# WF05 Offline Regression Report - 2026-05-11

## Summary
- timestamp_kst: {report['timestamp_kst']}
- classifier_version: {report['classifier_version']}
- fixture_count: {report['fixture_count']}
- passed_count: {report['passed_count']}
- failed_count: {report['failed_count']}
- failed_case_ids: {json.dumps(report['failed_case_ids'])}
- safety_result: {report['safety_result']}
- next_action: {report['next_action']}

## Offline Safety
- network_used: false
- secrets_loaded: false
- helper_called: false
- upbit_called: false
- n8n_called: false
- workflow_executed: false
- workflow_modified: false
- helper_modified: false

## Case Results
{chr(10).join(rows)}

## Final Rule
If any fixture fails, STOP before any WF05 runtime patch, live telemetry check, or workflow execution.
"""
    REPORT_MD_PATH.write_text(markdown, encoding="utf-8")


def main() -> int:
    report, _ = run_regression()
    write_json_report(report)
    write_markdown_report(report)
    print(
        json.dumps(
            {
                "fixture_count": report["fixture_count"],
                "passed_count": report["passed_count"],
                "failed_count": report["failed_count"],
                "failed_case_ids": report["failed_case_ids"],
                "report_json_path": str(REPORT_JSON_PATH),
                "report_md_path": str(REPORT_MD_PATH),
                "network_used": False,
            },
            ensure_ascii=False,
        )
    )
    return 0 if report["failed_count"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
