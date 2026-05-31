"""Local-only synthetic market data generator for offline contract-layer testing."""

from __future__ import annotations

import random
from typing import Dict, List


def generate_synthetic_market_data(seed: int = 42) -> List[Dict[str, object]]:
    random.seed(seed)

    scenarios = [
        "normal_trend",
        "sideways_chop",
        "sudden_spike",
        "sudden_crash",
        "spread_widening",
        "stale_data",
        "duplicate_signal",
        "cooldown_active",
        "rejection_cluster",
        "rate_budget_exhausted",
        "heartbeat_missed",
        "clock_skew",
        "reconciliation_drift",
        "kill_active",
    ]

    base_price = 100000.0
    rows: List[Dict[str, object]] = []

    for idx, scenario in enumerate(scenarios, start=1):
        price = base_price + random.uniform(-2500, 2500)
        spread_pct = 0.002 + random.uniform(0, 0.003)
        liquidity_score = 0.7 + random.uniform(-0.15, 0.15)

        row: Dict[str, object] = {
            "scenario": scenario,
            "snapshot_id": f"SNAP-{idx:03d}",
            "market": "KRW-BTC",
            "price": round(price, 2),
            "spread_pct": round(spread_pct, 6),
            "liquidity_score": round(liquidity_score, 4),
            "market_data_age_sec": 3,
            "duplicate_signal": False,
            "cooldown_active": False,
            "rejection_cluster": False,
            "rate_budget_exhausted": False,
            "heartbeat_missed": False,
            "clock_skew_ms": 50,
            "reconciliation_drift": False,
            "kill_active": False,
            "volatility_state": "NORMAL",
            "drawdown_simulated": round(random.uniform(0.2, 1.8), 4),
            "fee_drag_simulated": round(random.uniform(0.01, 0.08), 4),
            "synthetic_only": True,
        }

        if scenario == "sideways_chop":
            row["volatility_state"] = "CHOP"
        elif scenario == "sudden_spike":
            row["volatility_state"] = "SPIKE"
            row["drawdown_simulated"] = 2.3
        elif scenario == "sudden_crash":
            row["volatility_state"] = "CRASH"
            row["drawdown_simulated"] = 3.1
        elif scenario == "spread_widening":
            row["spread_pct"] = 0.021
        elif scenario == "stale_data":
            row["market_data_age_sec"] = 250
        elif scenario == "duplicate_signal":
            row["duplicate_signal"] = True
        elif scenario == "cooldown_active":
            row["cooldown_active"] = True
        elif scenario == "rejection_cluster":
            row["rejection_cluster"] = True
        elif scenario == "rate_budget_exhausted":
            row["rate_budget_exhausted"] = True
        elif scenario == "heartbeat_missed":
            row["heartbeat_missed"] = True
        elif scenario == "clock_skew":
            row["clock_skew_ms"] = 9500
        elif scenario == "reconciliation_drift":
            row["reconciliation_drift"] = True
        elif scenario == "kill_active":
            row["kill_active"] = True

        rows.append(row)

    return rows


if __name__ == "__main__":
    for item in generate_synthetic_market_data():
        print(item)
