import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy.kbia_trade_learning import approve_pattern_candidate, build_pattern_candidate, sanitize_trade_features


def test_sanitize_profitable_trade_features_without_execution_flags():
    features = sanitize_trade_features(
        {
            "market": "KRW-DOGE",
            "side": "bid",
            "fee_adjusted_return_pct": 0.025,
            "holding_seconds": 900,
            "spread_bps": 5,
            "orderbook_age_ms": 700,
            "atr_pct_14": 0.018,
            "volume_z_20": 1.5,
            "candidate_reason_codes": ["tight_spread", "volume_elevated"],
            "brain_version": "kbia.strategy_brain.v4.1",
        }
    )
    assert features["material_profit"] is True
    assert features["fee_adjusted_return_bucket"] == "material_win"
    assert features["spread_bucket"] == "normal"
    assert features["orderbook_freshness_bucket"] == "fresh"
    assert features["execution_allowed"] is False
    assert features["order_endpoint_allowed"] is False


def test_repeated_pattern_stays_non_reinforcing_until_validated():
    observations = [
        sanitize_trade_features({"market": "KRW-DOGE", "fee_adjusted_return_pct": 0.02, "candidate_reason_codes": ["tight_spread", "volume_elevated"]}),
        sanitize_trade_features({"market": "KRW-ETC", "fee_adjusted_return_pct": 0.018, "candidate_reason_codes": ["tight_spread", "volume_elevated"]}),
        sanitize_trade_features({"market": "KRW-DOT", "fee_adjusted_return_pct": 0.021, "candidate_reason_codes": ["tight_spread", "volume_elevated"]}),
    ]
    candidate = build_pattern_candidate(observations)
    assert candidate["promotion_level"] == "REPEATED_WIN_PATTERN"
    assert candidate["can_reinforce_brain"] is False
    assert candidate["bounded_score_weight"] == 0.0


def test_validated_pattern_can_only_add_bounded_reference_weight():
    candidate = {
        "observation_count": 5,
        "promotion_level": "VALIDATED_EDGE_CANDIDATE",
        "bounded_score_weight": 99,
        "loss_case_checked": True,
        "shadow_validation_passed": True,
        "hq_review_passed": True,
    }
    approved = approve_pattern_candidate(candidate)
    assert approved["can_reinforce_brain"] is True
    assert approved["bounded_score_weight"] == 4.0
    assert approved["live_order_allowed"] is False
    assert approved["automation_allowed"] is False


if __name__ == "__main__":
    test_sanitize_profitable_trade_features_without_execution_flags()
    test_repeated_pattern_stays_non_reinforcing_until_validated()
    test_validated_pattern_can_only_add_bounded_reference_weight()
    print("KBIA_TRADE_LEARNING_TESTS_PASS")
