"""Candidate-state simulation engine for offline-only governance tests."""

from __future__ import annotations

from typing import Dict, List

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

ALLOWED_STATES = {
    "NO_SIGNAL",
    "SIGNAL_CANDIDATE_CREATED",
    "RISK_FILTER_REJECTED",
    "PTRC_PRECHECK_ELIGIBLE",
    "NO_ORDER_SUBMISSION",
}

FORBIDDEN_STATES = {
    "SUBMITTED",
    "ACK_RECEIVED",
    "OPEN",
    "FILLED",
    "PARTIAL",
    "LIVE_ORDER",
    "SHADOW_ORDER",
}


def _confidence_bucket(volatility_state: str) -> str:
    if volatility_state in {"SPIKE", "CRASH"}:
        return "HIGH"
    if volatility_state == "CHOP":
        return "LOW"
    return "MEDIUM"


def evaluate_candidate(snapshot: Dict[str, object]) -> Dict[str, object]:
    reason_codes: List[str] = []
    state = "PTRC_PRECHECK_ELIGIBLE"

    if bool(snapshot.get("kill_active")):
        state = "RISK_FILTER_REJECTED"
        reason_codes.append("kill_active")
    elif bool(snapshot.get("reconciliation_drift")):
        state = "RISK_FILTER_REJECTED"
        reason_codes.append("reconciliation_drift")
    elif bool(snapshot.get("heartbeat_missed")):
        state = "RISK_FILTER_REJECTED"
        reason_codes.append("heartbeat_missed")
    elif int(snapshot.get("clock_skew_ms", 0)) > 5000:
        state = "RISK_FILTER_REJECTED"
        reason_codes.append("clock_skew")
    elif int(snapshot.get("market_data_age_sec", 0)) > 120:
        state = "RISK_FILTER_REJECTED"
        reason_codes.append("stale_data")
    elif bool(snapshot.get("duplicate_signal")):
        state = "RISK_FILTER_REJECTED"
        reason_codes.append("duplicate_signal")
    elif bool(snapshot.get("cooldown_active")):
        state = "RISK_FILTER_REJECTED"
        reason_codes.append("cooldown_active")
    elif bool(snapshot.get("rejection_cluster")):
        state = "RISK_FILTER_REJECTED"
        reason_codes.append("rejection_cluster")
    elif bool(snapshot.get("rate_budget_exhausted")):
        state = "RISK_FILTER_REJECTED"
        reason_codes.append("rate_budget_exhausted")
    elif float(snapshot.get("spread_pct", 0.0)) > 0.015:
        state = "RISK_FILTER_REJECTED"
        reason_codes.append("spread_widening")

    if not reason_codes and state == "PTRC_PRECHECK_ELIGIBLE":
        reason_codes.append("candidate_passed_local_filters")

    confidence = _confidence_bucket(str(snapshot.get("volatility_state", "NORMAL")))

    return {
        "scenario": snapshot["scenario"],
        "signal_id": f"SIG-{snapshot['snapshot_id']}",
        "state": state,
        "state_path": ["NO_SIGNAL", "SIGNAL_CANDIDATE_CREATED", state, "NO_ORDER_SUBMISSION"],
        "reason_codes": reason_codes,
        "confidence_bucket": confidence,
        "confidence_authorizes_trading": False,
        "execution_authorized": False,
        "order_submission_allowed": False,
        "no_order_without_ptrc": True,
        "dependencies": {
            "ptrc_required": True,
            "idem_required": True,
            "osm_required": True,
            "recon_required": True,
            "kill_required": True,
        },
        "live_runtime_api_credential_actions": "none",
    }
