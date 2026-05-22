from __future__ import annotations

from dataclasses import dataclass
from typing import Any


SCHEMA_VERSION = "kbia.trade_learning.v1"
PROMOTION_LEVELS = (
    "OBSERVED_WIN",
    "REPEATED_WIN_PATTERN",
    "VALIDATED_EDGE_CANDIDATE",
    "LIVE_WEIGHT_APPROVED",
)
REINFORCEMENT_LEVELS = {"VALIDATED_EDGE_CANDIDATE", "LIVE_WEIGHT_APPROVED"}


@dataclass(frozen=True)
class LearningPolicy:
    material_profit_pct: float = 0.012
    min_independent_trades_for_repeat: int = 3
    max_bounded_score_weight: float = 4.0


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    if parsed != parsed or parsed in (float("inf"), float("-inf")):
        return default
    return parsed


def _bucket(value: float, buckets: tuple[tuple[float, str], ...], default: str) -> str:
    for limit, name in buckets:
        if value <= limit:
            return name
    return default


def _return_bucket(value: float) -> str:
    return _bucket(
        value,
        (
            (-0.03, "loss_gt_3pct"),
            (-0.01, "loss_1_to_3pct"),
            (0.0, "flat_or_small_loss"),
            (0.012, "small_win"),
            (0.03, "material_win"),
            (0.07, "large_win"),
        ),
        "outsized_win",
    )


def _spread_bucket(value: float) -> str:
    return _bucket(value, ((4, "tight"), (8, "normal"), (15, "wide"), (35, "very_wide")), "extreme")


def _hold_bucket(seconds: float) -> str:
    return _bucket(seconds, ((300, "under_5m"), (1800, "5m_to_30m"), (14400, "30m_to_4h"), (86400, "4h_to_1d")), "over_1d")


def _volatility_bucket(value: float) -> str:
    return _bucket(value, ((0.006, "compressed"), (0.018, "normal"), (0.04, "active"), (0.07, "high")), "extreme")


def _volume_bucket(value: float) -> str:
    return _bucket(value, ((-0.5, "below_normal"), (0.75, "normal"), (2.0, "elevated"), (4.0, "spike")), "extreme_spike")


def _promotion_level(observation_count: int, loss_case_checked: bool, shadow_validation_passed: bool, hq_review_passed: bool) -> str:
    if observation_count < 1:
        return "NO_PATTERN"
    if observation_count < LearningPolicy().min_independent_trades_for_repeat:
        return "OBSERVED_WIN"
    if not (loss_case_checked and shadow_validation_passed and hq_review_passed):
        return "REPEATED_WIN_PATTERN"
    return "VALIDATED_EDGE_CANDIDATE"


def sanitize_trade_features(trade: dict[str, Any], policy: LearningPolicy | None = None) -> dict[str, Any]:
    policy = policy or LearningPolicy()
    fee_adjusted_return = _as_float(trade.get("fee_adjusted_return_pct", trade.get("realized_return_pct")))
    hold_seconds = _as_float(trade.get("holding_seconds"))
    spread_bps = _as_float(trade.get("spread_bps"))
    orderbook_age_ms = _as_float(trade.get("orderbook_age_ms"))
    volatility = _as_float(trade.get("atr_pct_14", trade.get("volatility_pct")))
    volume_z = _as_float(trade.get("volume_z_20"))
    result = {
        "schema_version": SCHEMA_VERSION,
        "market": str(trade.get("market") or "UNKNOWN"),
        "side": str(trade.get("side") or "UNKNOWN"),
        "entry_time_bucket": str(trade.get("entry_time_bucket") or "unknown"),
        "exit_time_bucket": str(trade.get("exit_time_bucket") or "unknown"),
        "holding_time_bucket": _hold_bucket(hold_seconds),
        "fee_adjusted_return_bucket": _return_bucket(fee_adjusted_return),
        "realized_pnl_bucket": str(trade.get("realized_pnl_bucket") or _return_bucket(fee_adjusted_return)),
        "material_profit": fee_adjusted_return >= policy.material_profit_pct,
        "spread_bucket": _spread_bucket(spread_bps),
        "orderbook_freshness_bucket": "fresh" if 0 < orderbook_age_ms <= 10_000 else "stale_or_unknown",
        "fill_speed_bucket": str(trade.get("fill_speed_bucket") or "unknown"),
        "trend_1m": str(trade.get("trend_1m") or "unknown"),
        "trend_5m": str(trade.get("trend_5m") or "unknown"),
        "trend_15m": str(trade.get("trend_15m") or "unknown"),
        "volatility_bucket": _volatility_bucket(volatility),
        "volume_bucket": _volume_bucket(volume_z),
        "liquidity_bucket": str(trade.get("liquidity_bucket") or "unknown"),
        "news_bias": str(trade.get("news_bias") or "UNKNOWN"),
        "btc_eth_regime": str(trade.get("btc_eth_regime") or trade.get("btc_regime") or "UNKNOWN"),
        "brain_version": str(trade.get("brain_version") or "UNKNOWN"),
        "candidate_reason_codes": sorted(str(code) for code in trade.get("candidate_reason_codes", []) if code),
        "gate_summary": str(trade.get("gate_summary") or "unknown"),
        "position_size_bucket": str(trade.get("position_size_bucket") or "unknown"),
        "execution_allowed": False,
        "live_order_allowed": False,
        "automation_allowed": False,
        "order_endpoint_allowed": False,
        "cancel_endpoint_allowed": False,
        "market_sell_allowed": False,
        "no_profit_guarantee": True,
    }
    return result


def build_pattern_candidate(observations: list[dict[str, Any]], policy: LearningPolicy | None = None) -> dict[str, Any]:
    policy = policy or LearningPolicy()
    material = [row for row in observations if row.get("material_profit") is True]
    common_codes: set[str] | None = None
    for row in material:
        codes = set(row.get("candidate_reason_codes") or [])
        common_codes = codes if common_codes is None else common_codes & codes
    return {
        "schema_version": SCHEMA_VERSION,
        "observation_count": len(material),
        "pattern_keys": sorted(common_codes or []),
        "promotion_level": _promotion_level(
            len(material),
            loss_case_checked=False,
            shadow_validation_passed=False,
            hq_review_passed=False,
        ),
        "bounded_score_weight": 0.0,
        "can_reinforce_brain": False,
        "loss_case_checked": False,
        "shadow_validation_passed": False,
        "hq_review_passed": False,
        "execution_allowed": False,
        "live_order_allowed": False,
        "automation_allowed": False,
        "order_endpoint_allowed": False,
        "cancel_endpoint_allowed": False,
        "market_sell_allowed": False,
        "max_bounded_score_weight": policy.max_bounded_score_weight,
        "no_profit_guarantee": True,
    }


def approve_pattern_candidate(candidate: dict[str, Any], policy: LearningPolicy | None = None) -> dict[str, Any]:
    policy = policy or LearningPolicy()
    observation_count = int(_as_float(candidate.get("observation_count")))
    loss_case_checked = candidate.get("loss_case_checked") is True
    shadow_validation_passed = candidate.get("shadow_validation_passed") is True
    hq_review_passed = candidate.get("hq_review_passed") is True
    level = str(candidate.get("promotion_level") or _promotion_level(observation_count, loss_case_checked, shadow_validation_passed, hq_review_passed))
    if level not in PROMOTION_LEVELS:
        level = _promotion_level(observation_count, loss_case_checked, shadow_validation_passed, hq_review_passed)
    can_reinforce = (
        level in REINFORCEMENT_LEVELS
        and observation_count >= policy.min_independent_trades_for_repeat
        and loss_case_checked
        and shadow_validation_passed
        and hq_review_passed
    )
    weight = min(policy.max_bounded_score_weight, max(0.0, _as_float(candidate.get("bounded_score_weight")))) if can_reinforce else 0.0
    approved = dict(candidate)
    approved.update(
        {
            "schema_version": SCHEMA_VERSION,
            "promotion_level": level,
            "bounded_score_weight": round(weight, 2),
            "can_reinforce_brain": can_reinforce,
            "execution_allowed": False,
            "live_order_allowed": False,
            "automation_allowed": False,
            "order_endpoint_allowed": False,
            "cancel_endpoint_allowed": False,
            "market_sell_allowed": False,
            "no_profit_guarantee": True,
        }
    )
    return approved
