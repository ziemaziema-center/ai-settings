"""Run local-only synthetic backtests for offline governance validation."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Dict, List

from offline_strategy_candidate_engine import (
    FORBIDDEN_STATES,
    NON_AUTHORIZATION_SENTENCE,
    SCORE_INTERPRETATION_SENTENCE,
    evaluate_candidate,
)
from offline_safety_scoring import calculate_offline_scores
from synthetic_market_data_generator import generate_synthetic_market_data

OUTPUT_DIR = Path(__file__).resolve().parent
JSON_OUTPUT = OUTPUT_DIR / "offline_backtest_result_v1.json"
MD_OUTPUT = OUTPUT_DIR / "offline_backtest_result_v1.md"


def run_offline_backtest(
    *,
    write_reports: bool = True,
    tests_passed: bool = False,
    manifest_traceability: bool = False,
) -> Dict[str, object]:
    snapshots = generate_synthetic_market_data()
    decisions: List[Dict[str, object]] = [evaluate_candidate(s) for s in snapshots]

    rejection_reason_counts: Counter[str] = Counter()
    rejected_signal_count = 0
    ptrc_eligible_count = 0
    no_order_submission_count = 0
    forbidden_state_count = 0

    for decision in decisions:
        if decision["state"] == "RISK_FILTER_REJECTED":
            rejected_signal_count += 1
            for reason in decision["reason_codes"]:
                rejection_reason_counts[reason] += 1
        if decision["state"] == "PTRC_PRECHECK_ELIGIBLE":
            ptrc_eligible_count += 1
        if not decision["order_submission_allowed"]:
            no_order_submission_count += 1

        if decision["state"] in FORBIDDEN_STATES:
            forbidden_state_count += 1
        if any(state in FORBIDDEN_STATES for state in decision.get("state_path", [])):
            forbidden_state_count += 1

    metrics: Dict[str, object] = {
        "scenario_count": len(snapshots),
        "candidate_count": len(decisions),
        "rejected_signal_count": rejected_signal_count,
        "ptrc_eligible_count": ptrc_eligible_count,
        "no_order_submission_count": no_order_submission_count,
        "forbidden_state_count": forbidden_state_count,
        "rejection_reason_counts": dict(rejection_reason_counts),
        "max_drawdown_simulated": max(float(s["drawdown_simulated"]) for s in snapshots),
        "fee_drag_simulated": round(sum(float(s["fee_drag_simulated"]) for s in snapshots), 4),
        "overtrade_score": 100 if rejection_reason_counts.get("cooldown_active", 0) >= 1 else 60,
        "safety_score": 100 if forbidden_state_count == 0 else 0,
        "governance_score": 100
        if all(all(bool(v) for v in d["dependencies"].values()) for d in decisions)
        else 0,
    }

    score = calculate_offline_scores(
        metrics,
        decisions,
        tests_passed=tests_passed,
        manifest_traceability=manifest_traceability,
        forbidden_action_occurred=False,
    )
    metrics["final_quality_score"] = score["final_quality_score"]

    result = {
        "metrics": metrics,
        "scores": score,
        "decisions": decisions,
        "live_runtime_api_credential_actions": "none",
    }

    if write_reports:
        JSON_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=True), encoding="utf-8")
        _write_markdown_report(result)

    return result


def _write_markdown_report(result: Dict[str, object]) -> None:
    metrics = result["metrics"]
    lines = [
        "# OFFLINE BACKTEST RESULT V1",
        "",
        "## Metrics",
        "",
        f"- scenario_count: {metrics['scenario_count']}",
        f"- candidate_count: {metrics['candidate_count']}",
        f"- rejected_signal_count: {metrics['rejected_signal_count']}",
        f"- ptrc_eligible_count: {metrics['ptrc_eligible_count']}",
        f"- no_order_submission_count: {metrics['no_order_submission_count']}",
        f"- forbidden_state_count: {metrics['forbidden_state_count']}",
        f"- max_drawdown_simulated: {metrics['max_drawdown_simulated']}",
        f"- fee_drag_simulated: {metrics['fee_drag_simulated']}",
        f"- overtrade_score: {metrics['overtrade_score']}",
        f"- safety_score: {metrics['safety_score']}",
        f"- governance_score: {metrics['governance_score']}",
        f"- final_quality_score: {metrics['final_quality_score']}",
        "",
        "## Rejection Reason Counts",
        "",
    ]
    for reason, cnt in sorted(metrics["rejection_reason_counts"].items()):
        lines.append(f"- {reason}: {cnt}")

    lines.extend(
        [
            "",
            NON_AUTHORIZATION_SENTENCE,
            "",
            SCORE_INTERPRETATION_SENTENCE,
        ]
    )

    MD_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run_offline_backtest(write_reports=True)
