"""Safety oracle for synthetic stress scenario outcomes."""

from __future__ import annotations

from typing import Dict

ALLOWED_STATES = {
    "SCENARIO_CREATED",
    "SIGNAL_BLOCKED",
    "PTRC_REJECTED",
    "IDEM_RETRY_BLOCKED",
    "RECON_DRIFT_DETECTED",
    "KILL_TRIGGERED",
    "ALERT_REQUIRED",
    "HUMAN_REVIEW_REQUIRED",
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
    "EXCHANGE_CONNECTED",
}


CRITICAL_EVENTS = {
    "rate_limit_418_ban_event",
    "heartbeat_missed",
    "hash_chain_break",
    "version_mismatch",
    "config_hash_drift",
    "kill_active_state",
}


def evaluate_scenario(scenario: Dict[str, object]) -> Dict[str, object]:
    name = str(scenario["scenario"])

    state = "NO_ORDER_SUBMISSION"
    reason = "safe_block"
    kill = False
    alert = True
    backoff = False

    if name == "rate_limit_429_storm":
        state = "SIGNAL_BLOCKED"
        reason = "429_backoff_required"
        backoff = True
    elif name == "rate_limit_418_ban_event":
        state = "KILL_TRIGGERED"
        reason = "418_ban_event"
        kill = True
    elif name == "duplicate_client_order_id":
        state = "IDEM_RETRY_BLOCKED"
        reason = "duplicate_client_order_id"
    elif name in {"orphan_exchange_order_synthetic", "local_order_missing_on_exchange_synthetic", "exchange_order_missing_locally_synthetic"}:
        state = "RECON_DRIFT_DETECTED"
        reason = "recon_drift_path"
    elif name in {"clock_skew", "stale_market_data", "websocket_disconnect", "order_candidate_rate_10x", "duplicate_signal_id"}:
        state = "SIGNAL_BLOCKED"
        reason = name
    elif name in CRITICAL_EVENTS:
        state = "KILL_TRIGGERED"
        reason = name
        kill = True
    elif name in {"exchange_5xx_storm", "partial_fill_flurry_synthetic", "replay_after_crash", "recovery_after_disconnect"}:
        state = "HUMAN_REVIEW_REQUIRED"
        reason = name

    if state not in ALLOWED_STATES:
        raise ValueError(f"Invalid oracle state: {state}")

    return {
        "scenario_id": scenario["scenario_id"],
        "scenario": name,
        "state": state,
        "reason": reason,
        "kill_triggered": kill,
        "alert_required": alert or (name in CRITICAL_EVENTS),
        "backoff_required": backoff,
        "no_order_submission": True,
        "forbidden_state_present": False,
        "critical_event": name in CRITICAL_EVENTS,
    }
