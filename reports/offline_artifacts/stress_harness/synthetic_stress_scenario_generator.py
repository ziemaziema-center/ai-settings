"""Synthetic stress scenario generator for local-only pre-live validation."""

from __future__ import annotations

from typing import Dict, List

REQUIRED_SCENARIOS = [
    "order_candidate_rate_10x",
    "rate_limit_429_storm",
    "rate_limit_418_ban_event",
    "exchange_5xx_storm",
    "websocket_disconnect",
    "heartbeat_missed",
    "stale_market_data",
    "clock_skew",
    "partial_fill_flurry_synthetic",
    "duplicate_signal_id",
    "duplicate_client_order_id",
    "hash_chain_break",
    "version_mismatch",
    "config_hash_drift",
    "kill_active_state",
    "replay_after_crash",
    "recovery_after_disconnect",
    "orphan_exchange_order_synthetic",
    "local_order_missing_on_exchange_synthetic",
    "exchange_order_missing_locally_synthetic",
]


def generate_scenarios() -> List[Dict[str, object]]:
    scenarios: List[Dict[str, object]] = []
    for index, name in enumerate(REQUIRED_SCENARIOS, start=1):
        scenarios.append(
            {
                "scenario_id": f"STRESS-{index:03d}",
                "scenario": name,
                "severity": "CRITICAL"
                if name
                in {
                    "rate_limit_418_ban_event",
                    "heartbeat_missed",
                    "hash_chain_break",
                    "version_mismatch",
                    "config_hash_drift",
                    "kill_active_state",
                }
                else "HIGH",
                "synthetic_only": True,
            }
        )
    return scenarios


if __name__ == "__main__":
    for item in generate_scenarios():
        print(item)
