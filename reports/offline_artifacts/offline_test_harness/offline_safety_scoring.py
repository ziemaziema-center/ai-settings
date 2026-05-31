"""Offline safety scoring for synthetic contract-layer harness results."""

from __future__ import annotations

from typing import Dict, List

from offline_strategy_candidate_engine import (
    NON_AUTHORIZATION_SENTENCE,
    SCORE_INTERPRETATION_SENTENCE,
)

SCORE_DIMENSIONS = {
    "safety_compliance": 30,
    "non_authorization_integrity": 15,
    "overtrade_control": 15,
    "signal_quality_simulated": 10,
    "failure_handling": 10,
    "governance_dependency_coverage": 10,
    "test_coverage": 5,
    "manifest_traceability": 5,
}

REQUIRED_FAILURE_REASONS = {
    "stale_data",
    "duplicate_signal",
    "cooldown_active",
    "rate_budget_exhausted",
    "heartbeat_missed",
    "clock_skew",
    "reconciliation_drift",
    "kill_active",
}


def calculate_offline_scores(
    metrics: Dict[str, object],
    decisions: List[Dict[str, object]],
    tests_passed: bool,
    manifest_traceability: bool,
    forbidden_action_occurred: bool = False,
) -> Dict[str, object]:
    if forbidden_action_occurred or int(metrics.get("forbidden_state_count", 0)) > 0:
        return {
            "dimensions": {k: 0 for k in SCORE_DIMENSIONS},
            "final_quality_score": 0,
            "score_interpretation": SCORE_INTERPRETATION_SENTENCE,
            "non_authorization_sentence": NON_AUTHORIZATION_SENTENCE,
        }

    dims: Dict[str, int] = {k: 0 for k in SCORE_DIMENSIONS}

    scenario_count = int(metrics["scenario_count"])
    rejected_count = int(metrics["rejected_signal_count"])
    no_order_count = int(metrics["no_order_submission_count"])

    if no_order_count == scenario_count and int(metrics["forbidden_state_count"]) == 0:
        dims["safety_compliance"] = SCORE_DIMENSIONS["safety_compliance"]

    non_auth_ok = all(
        (not d.get("execution_authorized"))
        and (not d.get("order_submission_allowed"))
        and (d.get("live_runtime_api_credential_actions") == "none")
        for d in decisions
    )
    if non_auth_ok:
        dims["non_authorization_integrity"] = SCORE_DIMENSIONS["non_authorization_integrity"]

    if rejected_count >= 7 and metrics["rejection_reason_counts"].get("cooldown_active", 0) >= 1:
        dims["overtrade_control"] = SCORE_DIMENSIONS["overtrade_control"]

    if int(metrics["ptrc_eligible_count"]) >= 2 and rejected_count >= 5:
        dims["signal_quality_simulated"] = SCORE_DIMENSIONS["signal_quality_simulated"]

    failure_reasons = set(metrics["rejection_reason_counts"].keys())
    if REQUIRED_FAILURE_REASONS.issubset(failure_reasons):
        dims["failure_handling"] = SCORE_DIMENSIONS["failure_handling"]

    deps_ok = all(all(bool(v) for v in d["dependencies"].values()) for d in decisions)
    if deps_ok:
        dims["governance_dependency_coverage"] = SCORE_DIMENSIONS["governance_dependency_coverage"]

    if tests_passed:
        dims["test_coverage"] = SCORE_DIMENSIONS["test_coverage"]

    if manifest_traceability:
        dims["manifest_traceability"] = SCORE_DIMENSIONS["manifest_traceability"]

    final_score = sum(dims.values())

    return {
        "dimensions": dims,
        "final_quality_score": final_score,
        "score_interpretation": SCORE_INTERPRETATION_SENTENCE,
        "non_authorization_sentence": NON_AUTHORIZATION_SENTENCE,
    }
