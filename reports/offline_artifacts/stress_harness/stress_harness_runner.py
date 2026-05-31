"""Run synthetic stress harness and produce local-only results."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Dict, List

from stress_safety_oracle import FORBIDDEN_STATES, evaluate_scenario
from synthetic_stress_scenario_generator import REQUIRED_SCENARIOS, generate_scenarios

OUTPUT_DIR = Path(__file__).resolve().parent
JSON_OUTPUT = OUTPUT_DIR / "stress_harness_result_v1.json"
MD_OUTPUT = OUTPUT_DIR / "stress_harness_result_v1.md"

NON_AUTH = "This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims."
PRE_SCORE = "Pre-live score measures local dry-run, documentation, governance, and validation completeness only; it does not authorize trading, does not predict profit, and does not indicate runtime, shadow, live, or WF08 readiness."


def run_stress_harness(write_reports: bool = True) -> Dict[str, object]:
    scenarios = generate_scenarios()
    outcomes: List[Dict[str, object]] = [evaluate_scenario(s) for s in scenarios]

    state_counts: Counter[str] = Counter(x["state"] for x in outcomes)
    forbidden = 0
    for item in outcomes:
        if item["state"] in FORBIDDEN_STATES:
            forbidden += 1

    result: Dict[str, object] = {
        "summary": {
            "scenario_count": len(outcomes),
            "required_scenario_count": len(REQUIRED_SCENARIOS),
            "all_required_scenarios_present": sorted(REQUIRED_SCENARIOS)
            == sorted([x["scenario"] for x in outcomes]),
            "forbidden_state_count": forbidden,
            "kill_trigger_count": sum(1 for x in outcomes if x["kill_triggered"]),
            "alert_required_count": sum(1 for x in outcomes if x["alert_required"]),
            "backoff_required_count": sum(1 for x in outcomes if x["backoff_required"]),
            "state_counts": dict(state_counts),
            "live_runtime_api_credential_actions": "none",
        },
        "outcomes": outcomes,
    }

    if write_reports:
        JSON_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=True), encoding="utf-8")
        _write_md(result)

    return result


def _write_md(result: Dict[str, object]) -> None:
    summary = result["summary"]
    lines = [
        "# STRESS HARNESS RESULT V1",
        "",
        "## Summary",
        "",
        f"- scenario_count: {summary['scenario_count']}",
        f"- required_scenario_count: {summary['required_scenario_count']}",
        f"- all_required_scenarios_present: {summary['all_required_scenarios_present']}",
        f"- forbidden_state_count: {summary['forbidden_state_count']}",
        f"- kill_trigger_count: {summary['kill_trigger_count']}",
        f"- alert_required_count: {summary['alert_required_count']}",
        f"- backoff_required_count: {summary['backoff_required_count']}",
        "",
        "## State Counts",
        "",
    ]

    for key, value in sorted(summary["state_counts"].items()):
        lines.append(f"- {key}: {value}")

    lines.extend(["", PRE_SCORE, "", NON_AUTH])
    MD_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run_stress_harness(write_reports=True)
