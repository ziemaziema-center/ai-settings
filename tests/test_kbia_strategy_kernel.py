import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy.kbia_strategy_kernel import evaluate_strategy


def rising_candles(count=60):
    rows = []
    price = 100.0
    for i in range(count):
        price *= 1.006
        if i > count - 8:
            price *= 0.996
        rows.append(
            {
                "close": round(price, 4),
                "high": round(price * 1.012, 4),
                "low": round(price * 0.988, 4),
                "volume_krw": 1_600_000_000 + i * 10_000_000,
            }
        )
    return rows


def falling_candles(count=60):
    rows = []
    price = 130.0
    for i in range(count):
        price *= 0.995
        rows.append(
            {
                "close": round(price, 4),
                "high": round(price * 1.01, 4),
                "low": round(price * 0.99, 4),
                "volume_krw": 1_500_000_000,
            }
        )
    return rows


def base_snapshot():
    return {
        "market": "KRW-BTC",
        "equity_krw": 2_000_000,
        "liquidity_24h_krw": 2_500_000_000,
        "spread_bps": 4,
        "open_order_exists": False,
        "open_order_count": 0,
        "workflow_active": False,
        "cron_enabled": False,
        "system_stop_active": False,
        "live_fuse_state": "disabled",
        "daily_loss_pct": 0,
        "portfolio_heat_pct": 0.1,
        "correlation_heat_pct": 0.1,
        "relative_strength_20": 0.02,
        "btc_regime": "BULL_TREND",
        "has_position": False,
        "best_bid": 100,
        "best_ask": 100.05,
        "bid_depth_top5_krw": 800_000_000,
        "ask_depth_top5_krw": 700_000_000,
    }


def test_open_order_forces_stop():
    snapshot = base_snapshot()
    snapshot["open_order_exists"] = True
    result = evaluate_strategy(snapshot, rising_candles())
    assert result["action"] == "STOP"
    assert "OPEN_ORDER_EXISTS" in result["decision_reason"]
    assert result["execution_allowed"] is False
    assert result["order_endpoint_allowed"] is False


def test_buy_candidate_requires_committee_edge_but_remains_shadow_only():
    result = evaluate_strategy(base_snapshot(), rising_candles())
    assert result["action"] in {"BUY_CANDIDATE", "HOLD"}
    assert result["committee_total_votes"] >= 18
    assert result["schema_version"] == "kbia.strategy_brain.v4.1"
    assert result["trader_council"]["total_members"] == 10
    assert result["whale_money_operator"]["maker_limit_only"] is True
    assert result["scalping_shadow"]["can_execute_live"] is False
    assert result["edge_learning"]["can_bypass_safety_gates"] is False
    assert result["execution_allowed"] is False
    assert result["live_order_allowed"] is False
    assert result["planned_order"]["ord_type"] == "limit"
    assert result["shadow_review_required"] is True


def test_sell_candidate_on_hard_stop_loss():
    snapshot = base_snapshot()
    snapshot["has_position"] = True
    snapshot["position_unrealized_pnl_pct"] = -0.025
    result = evaluate_strategy(snapshot, rising_candles())
    assert result["action"] == "SELL_CANDIDATE"
    assert "HARD_STOP_LOSS" in result["sell_reasons"]
    assert result["cancel_endpoint_allowed"] is False


def test_hold_when_market_edge_is_weak():
    result = evaluate_strategy(base_snapshot(), falling_candles())
    assert result["action"] in {"HOLD", "STOP"}
    assert result["execution_allowed"] is False


def test_required_orderbook_crossed_forces_stop():
    snapshot = base_snapshot()
    snapshot.update({"orderbook_required": True, "best_bid": 101, "best_ask": 100})
    result = evaluate_strategy(snapshot, rising_candles())
    assert result["action"] == "STOP"
    assert "ORDERBOOK_CROSSED" in result["hard_guards"]


def test_stale_candle_data_forces_stop():
    rows = rising_candles()
    for i, row in enumerate(rows):
        row["timestamp"] = 1000 + i * 60
    snapshot = base_snapshot()
    snapshot["now_ts"] = 1000 + 10_000
    result = evaluate_strategy(snapshot, rows)
    assert result["action"] == "STOP"
    assert "STALE_CANDLE_DATA" in result["hard_guards"]


def test_time_stop_sell_candidate():
    snapshot = base_snapshot()
    snapshot["has_position"] = True
    snapshot["bars_since_entry"] = 30
    snapshot["position_unrealized_pnl_pct"] = 0.002
    result = evaluate_strategy(snapshot, rising_candles())
    assert result["action"] == "SELL_CANDIDATE"
    assert "TIME_STOP" in result["sell_reasons"]


def test_defensive_news_reduces_live_readiness_without_execution_permission():
    snapshot = base_snapshot()
    snapshot["news_context"] = {
        "daily_brain_bias": "DEFENSIVE_REFERENCE",
        "risk_tag_counts": {"MARKET_STRESS": 1, "REGULATION": 1},
    }
    result = evaluate_strategy(snapshot, rising_candles())
    assert result["news_context"]["score_penalty"] > 0
    assert "COUNCIL_NEWS_DEFENSIVE_VETO" in result["trader_council"]["vetoes"]
    assert result["live_start_readiness"]["ready"] is False
    assert result["order_endpoint_allowed"] is False


def test_open_order_blocks_live_start_readiness():
    snapshot = base_snapshot()
    snapshot["open_order_exists"] = True
    snapshot["open_order_count"] = 1
    result = evaluate_strategy(snapshot, rising_candles())
    assert result["action"] == "STOP"
    assert "OPEN_ORDER_EXISTS" in result["live_start_readiness"]["blockers"]


def test_validated_edge_learning_adds_bounded_reference_bonus_only():
    snapshot = base_snapshot()
    snapshot["validated_edge_patterns"] = [
        {
            "observation_count": 5,
            "promotion_level": "VALIDATED_EDGE_CANDIDATE",
            "bounded_score_weight": 99,
            "loss_case_checked": True,
            "shadow_validation_passed": True,
            "hq_review_passed": True,
            "pattern_keys": ["tight_spread", "volume_elevated"],
        }
    ]
    result = evaluate_strategy(snapshot, rising_candles())
    assert result["edge_learning"]["approved_pattern_count"] == 1
    assert result["edge_learning"]["score_bonus"] == 4.0
    assert result["edge_learning"]["can_increase_live_size"] is False
    assert result["live_start_readiness"]["reference_bonus_does_not_bypass_gates"] is True
    assert result["order_endpoint_allowed"] is False


def test_scalping_shadow_is_reference_only_and_news_gated():
    snapshot = base_snapshot()
    snapshot["news_context"] = {"daily_brain_bias": "DEFENSIVE_REFERENCE"}
    result = evaluate_strategy(snapshot, rising_candles())
    assert result["scalping_shadow"]["mode"] == "reference_only_conservative_scalping"
    assert result["scalping_shadow"]["gates"]["news_not_defensive"] is False
    assert result["scalping_shadow"]["can_increase_order_frequency"] is False
    assert result["automation_allowed"] is False


if __name__ == "__main__":
    test_open_order_forces_stop()
    test_buy_candidate_requires_committee_edge_but_remains_shadow_only()
    test_sell_candidate_on_hard_stop_loss()
    test_hold_when_market_edge_is_weak()
    test_required_orderbook_crossed_forces_stop()
    test_stale_candle_data_forces_stop()
    test_time_stop_sell_candidate()
    test_defensive_news_reduces_live_readiness_without_execution_permission()
    test_open_order_blocks_live_start_readiness()
    test_validated_edge_learning_adds_bounded_reference_bonus_only()
    test_scalping_shadow_is_reference_only_and_news_gated()
    print("KBIA_STRATEGY_KERNEL_TESTS_PASS")
