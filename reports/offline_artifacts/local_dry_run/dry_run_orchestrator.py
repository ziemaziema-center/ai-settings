"""Local dry-run orchestrator for governance-only validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from dry_run_alert import build_alert
from dry_run_idem import DryRunIdemStore
from dry_run_kill import is_kill_active
from dry_run_osm import persist_intent
from dry_run_ptrc import evaluate_ptrc
from dry_run_recon import detect_recon_drift

OUTPUT_DIR = Path(__file__).resolve().parent
JSON_OUTPUT = OUTPUT_DIR / "local_dry_run_result_v1.json"
MD_OUTPUT = OUTPUT_DIR / "local_dry_run_result_v1.md"

NON_AUTH = "This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims."
PRE_SCORE = "Pre-live score measures local dry-run, documentation, governance, and validation completeness only; it does not authorize trading, does not predict profit, and does not indicate runtime, shadow, live, or WF08 readiness."
FORBIDDEN = {"SUBMITTED", "ACK_RECEIVED", "OPEN", "FILLED", "PARTIAL", "LIVE_ORDER", "SHADOW_ORDER", "EXCHANGE_CONNECTED"}


def run_local_dry_run(write_reports: bool = True) -> Dict[str, object]:
    idem = DryRunIdemStore()

    scenarios = [
        {"name": "normal_candidate", "client_order_id": "CID-001", "kill_active": False, "recon_drift": False, "clock_skew": False},
        {"name": "duplicate_client_order", "client_order_id": "CID-001", "kill_active": False, "recon_drift": False, "clock_skew": False},
        {"name": "kill_active_case", "client_order_id": "CID-002", "kill_active": True, "recon_drift": False, "clock_skew": False},
        {"name": "recon_drift_case", "client_order_id": "CID-003", "kill_active": False, "recon_drift": True, "clock_skew": False},
        {"name": "clock_skew_case", "client_order_id": "CID-004", "kill_active": False, "recon_drift": False, "clock_skew": True},
    ]

    runs: List[Dict[str, object]] = []

    for row in scenarios:
        if is_kill_active(row):
            alert = build_alert(row["name"], critical=True)
            runs.append(
                {
                    "scenario": row["name"],
                    "path": ["SIGNAL_CANDIDATE", "SIGNAL_BLOCKED", alert["state"], "NO_ORDER_SUBMISSION"],
                    "result_state": "SIGNAL_BLOCKED",
                    "reason": "kill_active",
                    "alert_required": True,
                    "no_order_submission": True,
                    "persisted_before_submitted": True,
                    "submitted": False,
                }
            )
            continue

        if detect_recon_drift(row):
            alert = build_alert(row["name"], critical=True)
            runs.append(
                {
                    "scenario": row["name"],
                    "path": ["SIGNAL_CANDIDATE", "SIGNAL_BLOCKED", "RECON_DRIFT_DETECTED", alert["state"], "NO_ORDER_SUBMISSION"],
                    "result_state": "SIGNAL_BLOCKED",
                    "reason": "recon_drift",
                    "alert_required": True,
                    "no_order_submission": True,
                    "persisted_before_submitted": True,
                    "submitted": False,
                }
            )
            continue

        ptrc = evaluate_ptrc(row, kill_active=False, recon_drift=False, clock_skew=bool(row["clock_skew"]))
        if ptrc["status"] == "PTRC_REJECTED":
            runs.append(
                {
                    "scenario": row["name"],
                    "path": ["SIGNAL_CANDIDATE", "PTRC_REJECTED", "NO_ORDER_SUBMISSION"],
                    "result_state": "PTRC_REJECTED",
                    "reason": ptrc["reason"],
                    "alert_required": ptrc["reason"] in {"clock_skew"},
                    "no_order_submission": True,
                    "persisted_before_submitted": True,
                    "submitted": False,
                }
            )
            continue

        idem_result = idem.prepare(row["client_order_id"])
        if idem_result["status"] == "IDEM_RETRY_BLOCKED":
            runs.append(
                {
                    "scenario": row["name"],
                    "path": ["SIGNAL_CANDIDATE", "PTRC_ELIGIBLE", "IDEM_RETRY_BLOCKED", "NO_ORDER_SUBMISSION"],
                    "result_state": "IDEM_RETRY_BLOCKED",
                    "reason": idem_result["reason"],
                    "alert_required": True,
                    "no_order_submission": True,
                    "persisted_before_submitted": True,
                    "submitted": False,
                }
            )
            continue

        osm = persist_intent(row["client_order_id"])
        runs.append(
            {
                "scenario": row["name"],
                "path": ["SIGNAL_CANDIDATE", "PTRC_ELIGIBLE", "IDEM_PREPARED", osm["osm_state"], "NO_ORDER_SUBMISSION"],
                "result_state": "NO_ORDER_SUBMISSION",
                "reason": "dry_run_persist_only",
                "alert_required": False,
                "no_order_submission": True,
                "persisted_before_submitted": bool(osm["persisted_before_submitted"]),
                "submitted": bool(osm["submitted"]),
            }
        )

    forbidden_count = 0
    for run in runs:
        if run["result_state"] in FORBIDDEN:
            forbidden_count += 1
        for st in run["path"]:
            if st in FORBIDDEN:
                forbidden_count += 1

    result = {
        "summary": {
            "scenario_count": len(runs),
            "forbidden_state_count": forbidden_count,
            "kill_block_count": sum(1 for r in runs if r["reason"] == "kill_active"),
            "recon_block_count": sum(1 for r in runs if r["reason"] == "recon_drift"),
            "idem_block_count": sum(1 for r in runs if r["result_state"] == "IDEM_RETRY_BLOCKED"),
            "alert_required_count": sum(1 for r in runs if r["alert_required"]),
            "persisted_before_submitted_all": all(bool(r["persisted_before_submitted"]) for r in runs),
            "submitted_state_present": any(bool(r["submitted"]) for r in runs),
            "live_runtime_api_credential_actions": "none",
        },
        "runs": runs,
    }

    if write_reports:
        JSON_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=True), encoding="utf-8")
        _write_md(result)

    return result


def _write_md(result: Dict[str, object]) -> None:
    summary = result["summary"]
    lines = [
        "# LOCAL DRY RUN RESULT V1",
        "",
        "## Summary",
        "",
        f"- scenario_count: {summary['scenario_count']}",
        f"- forbidden_state_count: {summary['forbidden_state_count']}",
        f"- kill_block_count: {summary['kill_block_count']}",
        f"- recon_block_count: {summary['recon_block_count']}",
        f"- idem_block_count: {summary['idem_block_count']}",
        f"- alert_required_count: {summary['alert_required_count']}",
        f"- persisted_before_submitted_all: {summary['persisted_before_submitted_all']}",
        f"- submitted_state_present: {summary['submitted_state_present']}",
        "",
        PRE_SCORE,
        "",
        NON_AUTH,
    ]
    MD_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run_local_dry_run(write_reports=True)
