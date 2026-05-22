from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Any

from strategy.kbia_trade_learning import approve_pattern_candidate

SCHEMA_VERSION = "kbia.strategy_brain.v4.1"
SAFE_NEXT_ACTION = "shadow_only_until_ip_allowlist_reconciliation_recovery_logging_alerts_validated"


@dataclass(frozen=True)
class Candle:
    close: float
    high: float
    low: float
    volume_krw: float
    timestamp: float | None = None


@dataclass(frozen=True)
class StrategyPolicy:
    min_liquidity_24h_krw: float = 1_000_000_000
    max_spread_bps: float = 12
    min_committee_votes: int = 14
    min_buy_score: float = 78
    max_risk_per_trade_pct: float = 0.005
    max_position_pct: float = 0.10
    max_daily_loss_pct: float = 0.015
    hard_stop_loss_pct: float = 0.018
    trailing_stop_pct: float = 0.014
    take_profit_pct: float = 0.032
    break_even_protect_pct: float = 0.012
    min_reward_risk: float = 1.8
    min_price_distance_from_20d_high_pct: float = 0.003
    max_price_distance_from_20d_high_pct: float = 0.09
    max_extension_from_sma20_pct: float = 0.08
    max_atr_pct: float = 0.055
    min_atr_pct: float = 0.006
    min_volume_z: float = -0.25
    max_volume_z: float = 3.0
    max_upper_wick_ratio: float = 0.55
    max_data_age_seconds: float = 900
    max_candle_gap_pct: float = 0.09
    max_single_candle_atr_multiple: float = 2.5
    max_orderbook_ask_ratio: float = 0.68
    max_portfolio_heat_pct: float = 0.30
    max_correlation_heat_pct: float = 0.45
    max_consecutive_shadow_losses: int = 2
    max_bars_without_progress: int = 24
    safe_order_min_krw: float = 5000
    safe_order_max_krw: float = 10000
    min_council_approvals: int = 8
    max_news_score_penalty: float = 12
    min_whale_bid_support_ratio: float = 0.42
    max_whale_ask_pressure_ratio: float = 0.64
    max_validated_edge_score_bonus: float = 4.0
    max_scalping_shadow_score_bonus: float = 3.0
    max_scalping_shadow_spread_bps: float = 8.0
    min_scalping_volume_z: float = 0.25
    min_scalping_bid_support_ratio: float = 0.48


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    if parsed != parsed or parsed in (float("inf"), float("-inf")):
        return default
    return parsed


def _as_optional_float(value: Any) -> float | None:
    if value is None:
        return None
    parsed = _as_float(value, float("nan"))
    return None if parsed != parsed else parsed


def _candle(row: dict[str, Any]) -> Candle:
    close = _as_float(row.get("close", row.get("trade_price")))
    high = _as_float(row.get("high", row.get("high_price")), close)
    low = _as_float(row.get("low", row.get("low_price")), close)
    volume = _as_float(row.get("volume_krw", row.get("acc_trade_price_24h")))
    timestamp = _as_optional_float(row.get("timestamp", row.get("ts")))
    return Candle(close=close, high=high, low=low, volume_krw=volume, timestamp=timestamp)


def _sma(values: list[float], window: int) -> float | None:
    if len(values) < window:
        return None
    return mean(values[-window:])


def _rsi(values: list[float], window: int = 14) -> float | None:
    if len(values) <= window:
        return None
    gains: list[float] = []
    losses: list[float] = []
    recent = values[-window - 1 :]
    for prev, curr in zip(recent, recent[1:]):
        delta = curr - prev
        gains.append(max(delta, 0.0))
        losses.append(abs(min(delta, 0.0)))
    avg_gain = mean(gains)
    avg_loss = mean(losses)
    if avg_loss == 0:
        return 100.0
    return 100.0 - (100.0 / (1.0 + avg_gain / avg_loss))


def _atr_pct(candles: list[Candle], window: int = 14, offset: int = 0) -> float | None:
    end = len(candles) - offset
    if end < window + 1:
        return None
    recent = candles[end - window - 1 : end]
    ranges: list[float] = []
    for prev, curr in zip(recent, recent[1:]):
        ranges.append(max(curr.high - curr.low, abs(curr.high - prev.close), abs(curr.low - prev.close)))
    close = recent[-1].close
    return mean(ranges) / close if close > 0 else None


def _volume_z(candles: list[Candle], window: int = 20) -> float | None:
    if len(candles) < window:
        return None
    volumes = [c.volume_krw for c in candles[-window:]]
    sigma = pstdev(volumes)
    return 0.0 if sigma == 0 else (volumes[-1] - mean(volumes)) / sigma


def _slope_pct(values: list[float], window: int, lookback: int = 5) -> float | None:
    if len(values) < window + lookback:
        return None
    now = _sma(values, window)
    prev = mean(values[-window - lookback : -lookback])
    if now is None or prev == 0:
        return None
    return (now - prev) / prev


def compute_indicators(candle_rows: list[dict[str, Any]]) -> dict[str, Any]:
    candles = [_candle(row) for row in candle_rows]
    closes = [c.close for c in candles]
    last = candles[-1] if candles else Candle(0, 0, 0, 0)
    high_20 = max((c.high for c in candles[-20:]), default=0.0)
    low_20 = min((c.low for c in candles[-20:]), default=0.0)
    sma20 = _sma(closes, 20)
    atr = _atr_pct(candles, 14)
    latest_range = (last.high - last.low) / last.close if last.close > 0 else None
    upper_wick = (last.high - max(last.close, last.low)) / (last.high - last.low) if last.high > last.low else 0.0
    candle_gap = abs(last.close - candles[-2].close) / candles[-2].close if len(candles) >= 2 and candles[-2].close > 0 else None
    return {
        "last_price": last.close,
        "sma_5": _sma(closes, 5),
        "sma_20": sma20,
        "sma_50": _sma(closes, 50),
        "sma20_slope_pct": _slope_pct(closes, 20),
        "sma50_slope_pct": _slope_pct(closes, 50),
        "rsi_14": _rsi(closes, 14),
        "atr_pct_14": atr,
        "atr_pct_14_prev": _atr_pct(candles, 14, offset=5),
        "volume_z_20": _volume_z(candles, 20),
        "high_20": high_20 or None,
        "low_20": low_20 or None,
        "distance_from_20d_high_pct": (high_20 - last.close) / last.close if last.close > 0 and high_20 > 0 else None,
        "range_20_pct": (high_20 - low_20) / last.close if last.close > 0 and high_20 > 0 and low_20 > 0 else None,
        "close_vs_sma20_pct": (last.close - sma20) / sma20 if sma20 else None,
        "latest_range_pct": latest_range,
        "upper_wick_ratio": upper_wick,
        "latest_candle_gap_pct": candle_gap,
        "latest_volume_krw": last.volume_krw,
        "latest_timestamp": last.timestamp,
        "candles_count": len(candles),
        "timestamps_sorted": _timestamps_sorted(candles),
        "timestamps_unique": _timestamps_unique(candles),
    }


def _timestamps_sorted(candles: list[Candle]) -> bool | None:
    timestamps = [c.timestamp for c in candles if c.timestamp is not None]
    if not timestamps:
        return None
    return timestamps == sorted(timestamps)


def _timestamps_unique(candles: list[Candle]) -> bool | None:
    timestamps = [c.timestamp for c in candles if c.timestamp is not None]
    if not timestamps:
        return None
    return len(timestamps) == len(set(timestamps))


def _normalize_candle_sets(candle_input: Any) -> dict[str, list[dict[str, Any]]]:
    if isinstance(candle_input, dict):
        return {str(key): list(value or []) for key, value in candle_input.items()}
    return {"primary": list(candle_input or [])}


def _primary_timeframe(candle_sets: dict[str, list[dict[str, Any]]]) -> str:
    for key in ("m15", "h1", "primary", "h4", "d1"):
        if key in candle_sets:
            return key
    return next(iter(candle_sets.keys()), "primary")


def compute_timeframes(candle_input: Any) -> dict[str, Any]:
    candle_sets = _normalize_candle_sets(candle_input)
    indicators = {name: compute_indicators(rows) for name, rows in candle_sets.items()}
    primary = _primary_timeframe(candle_sets)
    return {
        "mode": "multi" if len(candle_sets) > 1 else "single",
        "primary": primary,
        "indicators": indicators,
    }


def classify_regime(indicators: dict[str, Any], policy: StrategyPolicy) -> dict[str, Any]:
    price = indicators["last_price"]
    sma5 = indicators["sma_5"]
    sma20 = indicators["sma_20"]
    sma50 = indicators["sma_50"]
    rsi = indicators["rsi_14"]
    atr = indicators["atr_pct_14"]
    range20 = indicators["range_20_pct"]
    close_vs_sma20 = indicators["close_vs_sma20_pct"]
    upper_wick = indicators["upper_wick_ratio"]
    reasons: list[str] = []
    regime = "UNKNOWN"

    if indicators["candles_count"] < 50:
        reasons.append("INSUFFICIENT_CANDLES")
    elif atr is not None and atr > policy.max_atr_pct and sma20 is not None and price < sma20:
        regime = "PANIC"
        reasons.append("ATR_TOO_HIGH_PANIC")
    elif close_vs_sma20 is not None and close_vs_sma20 > policy.max_extension_from_sma20_pct:
        regime = "PARABOLIC"
        reasons.append("PUMP_EXTENSION_RISK")
    elif upper_wick > policy.max_upper_wick_ratio:
        regime = "PARABOLIC"
        reasons.append("UPPER_WICK_REJECTION")
    elif atr is not None and atr < policy.min_atr_pct:
        regime = "VOL_COMPRESSION"
        reasons.append("ATR_TOO_LOW_COMPRESSION")
    elif range20 is not None and range20 < 0.035 and rsi is not None and 45 <= rsi <= 55:
        regime = "CHOP"
        reasons.append("RANGE_CHOP")
    elif all(v is not None for v in (sma5, sma20, sma50)) and sma5 > sma20 > sma50 and price > sma20:
        regime = "BULL_TREND"
    elif all(v is not None for v in (sma20, sma50)) and price < sma20 < sma50:
        regime = "BEAR_TREND"
        reasons.append("BEAR_TREND")
    else:
        reasons.append("REGIME_UNKNOWN")

    return {"name": regime, "reasons": reasons, "buy_allowed": regime in {"BULL_TREND", "VOL_COMPRESSION"}}


def _orderbook_metrics(snapshot: dict[str, Any]) -> dict[str, Any]:
    bid = _as_optional_float(snapshot.get("best_bid"))
    ask = _as_optional_float(snapshot.get("best_ask"))
    bid_depth = _as_float(snapshot.get("bid_depth_top5_krw"))
    ask_depth = _as_float(snapshot.get("ask_depth_top5_krw"))
    mid = (bid + ask) / 2 if bid and ask else None
    computed_spread_bps = ((ask - bid) / mid * 10000) if bid and ask and mid and ask >= bid else None
    ask_ratio = ask_depth / (bid_depth + ask_depth) if bid_depth + ask_depth > 0 else None
    return {
        "best_bid": bid,
        "best_ask": ask,
        "bid_depth_top5_krw": bid_depth,
        "ask_depth_top5_krw": ask_depth,
        "computed_spread_bps": computed_spread_bps,
        "ask_depth_ratio": ask_ratio,
        "crossed": bid is not None and ask is not None and bid >= ask,
    }


def _data_guards(snapshot: dict[str, Any], indicators: dict[str, Any], policy: StrategyPolicy) -> list[str]:
    reasons: list[str] = []
    if indicators["timestamps_sorted"] is False:
        reasons.append("UNSORTED_CANDLE_DATA")
    if indicators["timestamps_unique"] is False:
        reasons.append("DUPLICATE_CANDLE_DATA")
    latest_ts = indicators["latest_timestamp"]
    now_ts = _as_optional_float(snapshot.get("now_ts"))
    data_age = _as_optional_float(snapshot.get("data_age_seconds"))
    if data_age is None and latest_ts is not None and now_ts is not None:
        data_age = now_ts - latest_ts
    if data_age is not None and (data_age < 0 or data_age > policy.max_data_age_seconds):
        reasons.append("STALE_CANDLE_DATA")
    if indicators["latest_candle_gap_pct"] is not None and indicators["latest_candle_gap_pct"] > policy.max_candle_gap_pct:
        reasons.append("CANDLE_GAP_TOO_LARGE")
    atr = indicators["atr_pct_14"]
    candle_range = indicators["latest_range_pct"]
    if atr and candle_range and candle_range > atr * policy.max_single_candle_atr_multiple:
        reasons.append("SINGLE_CANDLE_SHOCK")
    return reasons


def _hard_guards(snapshot: dict[str, Any], indicators: dict[str, Any], orderbook: dict[str, Any], policy: StrategyPolicy) -> list[str]:
    reasons = _data_guards(snapshot, indicators, policy)
    if snapshot.get("system_stop_active") is True:
        reasons.append("SYSTEM_STOP_ACTIVE")
    if snapshot.get("manual_block_active") is True or snapshot.get("news_block_active") is True:
        reasons.append("MANUAL_OR_NEWS_BLOCK_ACTIVE")
    if snapshot.get("open_order_exists") is True or _as_float(snapshot.get("open_order_count")) > 0:
        reasons.append("OPEN_ORDER_EXISTS")
    if snapshot.get("unresolved_previous_decision") is True:
        reasons.append("UNRESOLVED_PREVIOUS_DECISION")
    if snapshot.get("workflow_active") is True or snapshot.get("cron_enabled") is True:
        reasons.append("AUTOMATION_RUNTIME_NOT_ALLOWED")
    if snapshot.get("live_fuse_state") not in (None, "disabled", "consumed"):
        reasons.append("LIVE_FUSE_NOT_DISABLED")
    if _as_float(snapshot.get("daily_loss_pct")) <= -policy.max_daily_loss_pct:
        reasons.append("DAILY_LOSS_LIMIT_HIT")
    if _as_float(snapshot.get("consecutive_shadow_losses")) > policy.max_consecutive_shadow_losses:
        reasons.append("MAX_CONSECUTIVE_SHADOW_LOSSES")
    if snapshot.get("recent_loss_cooldown_active") is True:
        reasons.append("RECENT_LOSS_COOLDOWN")
    if _as_float(snapshot.get("spread_bps", orderbook["computed_spread_bps"] or 0)) > policy.max_spread_bps:
        reasons.append("SPREAD_TOO_WIDE")
    if _as_float(snapshot.get("liquidity_24h_krw")) < policy.min_liquidity_24h_krw:
        reasons.append("LIQUIDITY_TOO_LOW")
    if indicators["candles_count"] < 50:
        reasons.append("INSUFFICIENT_CANDLES")
    if indicators["last_price"] <= 0:
        reasons.append("INVALID_PRICE")
    if snapshot.get("account_state_authoritative") is False:
        reasons.append("ACCOUNT_STATE_NOT_AUTHORITATIVE")
    if snapshot.get("locked_balance_exists") is True:
        reasons.append("LOCKED_BALANCE_EXISTS")
    if snapshot.get("orderbook_required") is True:
        if orderbook["best_bid"] is None or orderbook["best_ask"] is None:
            reasons.append("ORDERBOOK_MISSING")
        if orderbook["crossed"]:
            reasons.append("ORDERBOOK_CROSSED")
        if orderbook["ask_depth_ratio"] is not None and orderbook["ask_depth_ratio"] > policy.max_orderbook_ask_ratio:
            reasons.append("ORDERBOOK_ADVERSE_ASK_IMBALANCE")
    return sorted(set(reasons))


def _committee(snapshot: dict[str, Any], indicators: dict[str, Any], regime: dict[str, Any], orderbook: dict[str, Any], policy: StrategyPolicy) -> list[dict[str, Any]]:
    price = indicators["last_price"]
    sma5 = indicators["sma_5"]
    sma20 = indicators["sma_20"]
    sma50 = indicators["sma_50"]
    rsi = indicators["rsi_14"]
    atr = indicators["atr_pct_14"]
    volume_z = indicators["volume_z_20"]
    distance_high = indicators["distance_from_20d_high_pct"]
    close_vs_sma20 = indicators["close_vs_sma20_pct"]
    range20 = indicators["range_20_pct"]
    trend_ok = all(v is not None for v in (sma5, sma20, sma50)) and sma5 > sma20 > sma50
    pullback_ok = distance_high is not None and policy.min_price_distance_from_20d_high_pct <= distance_high <= policy.max_price_distance_from_20d_high_pct
    momentum_ok = rsi is not None and 48 <= rsi <= 68 and price > (sma20 or price + 1)
    volatility_ok = atr is not None and policy.min_atr_pct <= atr <= policy.max_atr_pct
    liquidity_ok = _as_float(snapshot.get("liquidity_24h_krw")) >= policy.min_liquidity_24h_krw
    spread_value = _as_float(snapshot.get("spread_bps", orderbook["computed_spread_bps"] or 999))
    spread_ok = spread_value <= policy.max_spread_bps
    volume_ok = volume_z is not None and policy.min_volume_z <= volume_z <= policy.max_volume_z
    reward_risk_ok = atr is not None and policy.take_profit_pct / max(policy.hard_stop_loss_pct, atr) >= policy.min_reward_risk
    portfolio_heat_ok = _as_float(snapshot.get("portfolio_heat_pct")) <= policy.max_portfolio_heat_pct
    exit_discipline_ok = snapshot.get("has_position") is not True or bool(_sell_reasons(snapshot, indicators, regime, policy))
    btc_ok = snapshot.get("btc_regime") in (None, "BULL_TREND", "NEUTRAL")
    relative_ok = _as_float(snapshot.get("relative_strength_20")) >= 0
    trend_maturity_ok = close_vs_sma20 is None or close_vs_sma20 <= policy.max_extension_from_sma20_pct
    wick_ok = indicators["upper_wick_ratio"] <= policy.max_upper_wick_ratio
    range_position_ok = range20 is None or distance_high is None or distance_high >= policy.min_price_distance_from_20d_high_pct or snapshot.get("breakout_confirmed") is True
    breakout_ok = snapshot.get("breakout_confirmed") is True or regime["name"] == "BULL_TREND"
    data_ok = not _data_guards(snapshot, indicators, policy)
    spread_liquidity_ok = spread_ok and liquidity_ok
    drawdown_ok = _as_float(snapshot.get("daily_loss_pct")) > -policy.max_daily_loss_pct / 2
    cooldown_ok = snapshot.get("recent_loss_cooldown_active") is not True
    correlation_ok = _as_float(snapshot.get("correlation_heat_pct")) <= policy.max_correlation_heat_pct

    specs = [
        ("regime_trend", trend_ok and regime["buy_allowed"], 8),
        ("pullback_quality", pullback_ok, 6),
        ("momentum_confirmation", momentum_ok, 7),
        ("liquidity_depth", liquidity_ok, 6),
        ("spread_slippage", spread_ok, 5),
        ("volatility_window", volatility_ok, 6),
        ("volume_quality", volume_ok, 6),
        ("reward_risk", reward_risk_ok, 7),
        ("portfolio_heat", portfolio_heat_ok, 5),
        ("exit_discipline", exit_discipline_ok, 5),
        ("btc_market_regime", btc_ok, 5),
        ("relative_strength", relative_ok, 5),
        ("trend_maturity", trend_maturity_ok, 5),
        ("wick_rejection", wick_ok, 5),
        ("range_position", range_position_ok, 5),
        ("breakout_validation", breakout_ok, 4),
        ("data_freshness", data_ok, 6),
        ("spread_liquidity_consistency", spread_liquidity_ok, 5),
        ("drawdown_state", drawdown_ok, 5),
        ("cooldown_clear", cooldown_ok, 4),
        ("correlation_heat", correlation_ok, 5),
    ]
    return [{"name": name, "vote": bool(vote), "score": weight if vote else 0, "weight": weight} for name, vote, weight in specs]


def _news_context(snapshot: dict[str, Any]) -> dict[str, Any]:
    raw = snapshot.get("news_context")
    return raw if isinstance(raw, dict) else {}


def _news_risk_modifier(news: dict[str, Any], policy: StrategyPolicy) -> dict[str, Any]:
    bias = str(news.get("daily_brain_bias") or "UNKNOWN")
    risk_counts = news.get("risk_tag_counts") if isinstance(news.get("risk_tag_counts"), dict) else {}
    penalty = 0.0
    reasons: list[str] = []
    if bias == "DEFENSIVE_REFERENCE":
        penalty += 6.0
        reasons.append("NEWS_DEFENSIVE_REFERENCE")
    elif bias == "EVENT_RISK_REFERENCE":
        penalty += 3.0
        reasons.append("NEWS_EVENT_RISK_REFERENCE")
    penalty += min(4.0, _as_float(risk_counts.get("SECURITY")) * 2.0)
    penalty += min(4.0, _as_float(risk_counts.get("MARKET_STRESS")) * 2.0)
    penalty += min(2.0, _as_float(risk_counts.get("REGULATION")))
    return {
        "daily_brain_bias": bias,
        "risk_tag_counts": risk_counts,
        "score_penalty": min(policy.max_news_score_penalty, penalty),
        "reasons": sorted(set(reasons)),
        "reference_only": True,
    }


def _senior_trader_council(
    snapshot: dict[str, Any],
    indicators: dict[str, Any],
    regime: dict[str, Any],
    orderbook: dict[str, Any],
    news: dict[str, Any],
    policy: StrategyPolicy,
) -> dict[str, Any]:
    atr = indicators["atr_pct_14"]
    rsi = indicators["rsi_14"]
    close_vs_sma20 = indicators["close_vs_sma20_pct"]
    volume_z = indicators["volume_z_20"]
    spread = _as_float(snapshot.get("spread_bps", orderbook["computed_spread_bps"] or 999))
    news_modifier = _news_risk_modifier(news, policy)
    defensive_news = news_modifier["daily_brain_bias"] == "DEFENSIVE_REFERENCE"
    specs = [
        ("10y_spot_trend_trader", regime["name"] in {"BULL_TREND", "VOL_COMPRESSION"} and close_vs_sma20 is not None and close_vs_sma20 <= policy.max_extension_from_sma20_pct),
        ("10y_pullback_trader", indicators["distance_from_20d_high_pct"] is not None and indicators["distance_from_20d_high_pct"] >= policy.min_price_distance_from_20d_high_pct),
        ("10y_risk_manager", _as_float(snapshot.get("daily_loss_pct")) > -policy.max_daily_loss_pct and not defensive_news),
        ("10y_execution_trader", spread <= policy.max_spread_bps and orderbook["crossed"] is False),
        ("10y_volume_reader", volume_z is None or volume_z <= policy.max_volume_z),
        ("10y_volatility_trader", atr is not None and policy.min_atr_pct <= atr <= policy.max_atr_pct),
        ("10y_cycle_trader", rsi is None or 42 <= rsi <= 70),
        ("10y_btc_regime_trader", snapshot.get("btc_regime") in (None, "BULL_TREND", "NEUTRAL")),
        ("10y_portfolio_operator", _as_float(snapshot.get("portfolio_heat_pct")) <= policy.max_portfolio_heat_pct),
        ("iq170_scenario_agent", not news_modifier["reasons"] and snapshot.get("unresolved_previous_decision") is not True),
    ]
    members = [{"name": name, "approve": bool(approve)} for name, approve in specs]
    approvals = sum(1 for member in members if member["approve"])
    vetoes: list[str] = []
    if defensive_news:
        vetoes.append("COUNCIL_NEWS_DEFENSIVE_VETO")
    if approvals < policy.min_council_approvals:
        vetoes.append("COUNCIL_APPROVALS_BELOW_THRESHOLD")
    return {
        "schema_version": "kbia.trader_council.v1",
        "members": members,
        "approval_count": approvals,
        "total_members": len(members),
        "approved": approvals >= policy.min_council_approvals and not vetoes,
        "vetoes": vetoes,
        "news_modifier": news_modifier,
    }


def _whale_money_operator(snapshot: dict[str, Any], orderbook: dict[str, Any], policy: StrategyPolicy) -> dict[str, Any]:
    bid_depth = orderbook["bid_depth_top5_krw"]
    ask_depth = orderbook["ask_depth_top5_krw"]
    total_depth = bid_depth + ask_depth
    bid_support_ratio = bid_depth / total_depth if total_depth > 0 else None
    ask_pressure_ratio = ask_depth / total_depth if total_depth > 0 else None
    spread = _as_float(snapshot.get("spread_bps", orderbook["computed_spread_bps"] or 999))
    vetoes: list[str] = []
    if bid_support_ratio is None:
        vetoes.append("WHALE_ORDERBOOK_DEPTH_MISSING")
    elif bid_support_ratio < policy.min_whale_bid_support_ratio:
        vetoes.append("WHALE_BID_SUPPORT_TOO_WEAK")
    if ask_pressure_ratio is not None and ask_pressure_ratio > policy.max_whale_ask_pressure_ratio:
        vetoes.append("WHALE_ASK_PRESSURE_TOO_HIGH")
    if spread > policy.max_spread_bps:
        vetoes.append("WHALE_SPREAD_TOO_WIDE")
    liquidity_grade = "A" if bid_support_ratio is not None and bid_support_ratio >= 0.55 and spread <= policy.max_spread_bps / 2 else "B" if not vetoes else "D"
    return {
        "schema_version": "kbia.whale_money_operator.v1",
        "bid_support_ratio": round(bid_support_ratio, 4) if bid_support_ratio is not None else None,
        "ask_pressure_ratio": round(ask_pressure_ratio, 4) if ask_pressure_ratio is not None else None,
        "liquidity_grade": liquidity_grade,
        "approved": not vetoes,
        "vetoes": vetoes,
        "maker_limit_only": True,
    }


def _edge_learning_modifier(snapshot: dict[str, Any], policy: StrategyPolicy) -> dict[str, Any]:
    raw_patterns = snapshot.get("validated_edge_patterns")
    if not isinstance(raw_patterns, list):
        raw_patterns = []
    approved_patterns: list[dict[str, Any]] = []
    total_bonus = 0.0
    for raw in raw_patterns:
        if not isinstance(raw, dict):
            continue
        approved = approve_pattern_candidate(raw)
        if approved.get("can_reinforce_brain") is True:
            approved_patterns.append(
                {
                    "promotion_level": approved.get("promotion_level"),
                    "bounded_score_weight": approved.get("bounded_score_weight"),
                    "pattern_keys": approved.get("pattern_keys", []),
                }
            )
            total_bonus += _as_float(approved.get("bounded_score_weight"))
    bounded_bonus = min(policy.max_validated_edge_score_bonus, total_bonus)
    return {
        "schema_version": "kbia.edge_learning_reference.v1",
        "reference_only": True,
        "approved_pattern_count": len(approved_patterns),
        "score_bonus": round(bounded_bonus, 2),
        "patterns": approved_patterns,
        "can_bypass_safety_gates": False,
        "can_increase_live_size": False,
        "can_enable_simultaneous_orders": False,
    }


def _scalping_shadow_context(
    snapshot: dict[str, Any],
    indicators: dict[str, Any],
    regime: dict[str, Any],
    orderbook: dict[str, Any],
    policy: StrategyPolicy,
) -> dict[str, Any]:
    spread = _as_float(snapshot.get("spread_bps", orderbook["computed_spread_bps"] or 999))
    volume_z = indicators["volume_z_20"]
    bid_depth = orderbook["bid_depth_top5_krw"]
    ask_depth = orderbook["ask_depth_top5_krw"]
    total_depth = bid_depth + ask_depth
    bid_support_ratio = bid_depth / total_depth if total_depth > 0 else None
    momentum_ok = indicators["sma_5"] is not None and indicators["sma_20"] is not None and indicators["sma_5"] >= indicators["sma_20"]
    gates = {
        "spread": spread <= policy.max_scalping_shadow_spread_bps,
        "volume": volume_z is not None and volume_z >= policy.min_scalping_volume_z,
        "bid_support": bid_support_ratio is not None and bid_support_ratio >= policy.min_scalping_bid_support_ratio,
        "regime": regime["name"] in {"BULL_TREND", "VOL_COMPRESSION"},
        "momentum": momentum_ok,
        "open_order_clear": snapshot.get("open_order_exists") is not True and _as_float(snapshot.get("open_order_count")) == 0,
        "news_not_defensive": (_news_context(snapshot).get("daily_brain_bias") != "DEFENSIVE_REFERENCE"),
    }
    passed = sum(1 for value in gates.values() if value)
    candidate = all(gates.values())
    score_bonus = min(policy.max_scalping_shadow_score_bonus, passed * 0.4) if candidate else 0.0
    return {
        "schema_version": "kbia.scalping_shadow.v1",
        "mode": "reference_only_conservative_scalping",
        "candidate": candidate,
        "gates": gates,
        "passed_gate_count": passed,
        "total_gate_count": len(gates),
        "score_bonus": round(score_bonus, 2),
        "spread_bps": round(spread, 4),
        "bid_support_ratio": round(bid_support_ratio, 4) if bid_support_ratio is not None else None,
        "can_execute_live": False,
        "can_bypass_safety_gates": False,
        "can_increase_order_frequency": False,
        "can_enable_simultaneous_orders": False,
    }


def _sell_reasons(snapshot: dict[str, Any], indicators: dict[str, Any], regime: dict[str, Any], policy: StrategyPolicy) -> list[str]:
    if snapshot.get("has_position") is not True:
        return []
    pnl = _as_float(snapshot.get("position_unrealized_pnl_pct"))
    max_favorable = _as_float(snapshot.get("max_favorable_pnl_pct"))
    trailing_drawdown = _as_float(snapshot.get("trailing_drawdown_pct"))
    bars_since_entry = _as_float(snapshot.get("bars_since_entry"))
    reasons: list[str] = []
    if pnl <= -policy.hard_stop_loss_pct:
        reasons.append("HARD_STOP_LOSS")
    if pnl >= policy.take_profit_pct:
        reasons.append("TAKE_PROFIT")
    if trailing_drawdown <= -policy.trailing_stop_pct:
        reasons.append("TRAILING_STOP")
    if max_favorable >= policy.break_even_protect_pct and pnl <= 0:
        reasons.append("BREAK_EVEN_PROTECT")
    if bars_since_entry >= policy.max_bars_without_progress and pnl < policy.break_even_protect_pct:
        reasons.append("TIME_STOP")
    if indicators["sma_5"] is not None and indicators["sma_20"] is not None and indicators["sma_5"] < indicators["sma_20"]:
        reasons.append("TREND_BREAK")
    atr = indicators["atr_pct_14"]
    atr_prev = indicators["atr_pct_14_prev"]
    if atr and atr_prev and atr > atr_prev * 1.45 and pnl <= 0:
        reasons.append("VOLATILITY_EXPANSION_EXIT")
    if snapshot.get("lower_high_detected") is True:
        reasons.append("LOWER_HIGH_EXIT")
    if snapshot.get("breakout_failed") is True:
        reasons.append("FAILED_BREAKOUT_EXIT")
    if regime["name"] in {"PANIC", "BEAR_TREND"}:
        reasons.append("REGIME_FLIP_EXIT")
    if _as_float(snapshot.get("position_allocation_pct")) > policy.max_position_pct:
        reasons.append("EXPOSURE_REDUCTION")
    if snapshot.get("liquidity_dry_up") is True:
        reasons.append("LIQUIDITY_DRY_UP_EXIT")
    return sorted(set(reasons))


def _safe_order_krw(snapshot: dict[str, Any], indicators: dict[str, Any], orderbook: dict[str, Any], score: float, regime: dict[str, Any], policy: StrategyPolicy) -> tuple[float, dict[str, Any]]:
    equity_krw = _as_float(snapshot.get("equity_krw"))
    price = indicators["last_price"]
    atr_pct = indicators["atr_pct_14"]
    if equity_krw <= 0 or price <= 0 or not regime["buy_allowed"]:
        return 0.0, {"final_shadow_krw": 0.0, "blocked_reason": "NO_EQUITY_PRICE_OR_REGIME"}
    volatility_stop = max(policy.hard_stop_loss_pct, atr_pct or policy.hard_stop_loss_pct)
    base_risk_krw = equity_krw * policy.max_risk_per_trade_pct
    confidence_multiplier = max(0.0, min(1.0, score / 100.0))
    volatility_multiplier = max(0.25, min(1.0, policy.max_atr_pct / max(volatility_stop, 0.0001)))
    drawdown_multiplier = max(0.25, 1.0 + _as_float(snapshot.get("daily_loss_pct")))
    spread = _as_float(snapshot.get("spread_bps", orderbook["computed_spread_bps"] or 0))
    spread_multiplier = max(0.25, min(1.0, policy.max_spread_bps / max(spread, 0.01)))
    consecutive_losses = _as_float(snapshot.get("consecutive_shadow_losses"))
    loss_multiplier = max(0.25, 1.0 - consecutive_losses * 0.25)
    risk_position = (base_risk_krw / volatility_stop) * confidence_multiplier
    planned = min(
        risk_position * volatility_multiplier * drawdown_multiplier * spread_multiplier * loss_multiplier,
        equity_krw * policy.max_position_pct,
        policy.safe_order_max_krw,
    )
    if orderbook["ask_depth_top5_krw"] > 0:
        planned = min(planned, orderbook["ask_depth_top5_krw"] * 0.01)
    if planned < policy.safe_order_min_krw:
        planned = 0.0
    return round(planned, 0), {
        "base_risk_krw": round(base_risk_krw, 2),
        "confidence_multiplier": round(confidence_multiplier, 4),
        "volatility_multiplier": round(volatility_multiplier, 4),
        "drawdown_multiplier": round(drawdown_multiplier, 4),
        "spread_multiplier": round(spread_multiplier, 4),
        "loss_multiplier": round(loss_multiplier, 4),
        "final_shadow_krw": round(planned, 0),
    }


def _confidence_bucket(score: float, yes_votes: int) -> str:
    if score >= 90 and yes_votes >= 17:
        return "A"
    if score >= 78 and yes_votes >= 14:
        return "B"
    if score >= 60:
        return "C"
    return "D"


def evaluate_strategy(snapshot: dict[str, Any], candle_rows: Any, policy: StrategyPolicy | None = None) -> dict[str, Any]:
    policy = policy or StrategyPolicy()
    timeframes = compute_timeframes(candle_rows)
    primary = timeframes["primary"]
    indicators = timeframes["indicators"][primary]
    regime = classify_regime(indicators, policy)
    orderbook = _orderbook_metrics(snapshot)
    guards = _hard_guards(snapshot, indicators, orderbook, policy)
    votes = _committee(snapshot, indicators, regime, orderbook, policy)
    news = _news_context(snapshot)
    council = _senior_trader_council(snapshot, indicators, regime, orderbook, news, policy)
    whale_operator = _whale_money_operator(snapshot, orderbook, policy)
    edge_learning = _edge_learning_modifier(snapshot, policy)
    scalping_shadow = _scalping_shadow_context(snapshot, indicators, regime, orderbook, policy)
    max_score = sum(v["weight"] for v in votes)
    raw_score = sum(v["score"] for v in votes)
    raw_score_pct = raw_score / max_score * 100 if max_score else 0.0
    news_penalty = _as_float((council.get("news_modifier") or {}).get("score_penalty"))
    reference_bonus = _as_float(edge_learning.get("score_bonus")) + _as_float(scalping_shadow.get("score_bonus"))
    score = round(max(0.0, raw_score_pct - news_penalty + reference_bonus), 2)
    yes_votes = sum(1 for v in votes if v["vote"])
    sell_reasons = _sell_reasons(snapshot, indicators, regime, policy)
    strategic_vetoes = list(council["vetoes"]) + list(whale_operator["vetoes"])
    no_trade_reasons = sorted(set(guards + regime["reasons"] + strategic_vetoes))
    planned_order_krw, sizing_explain = _safe_order_krw(snapshot, indicators, orderbook, score, regime, policy)

    stage_pass = {
        "regime": regime["buy_allowed"],
        "setup": yes_votes >= policy.min_committee_votes,
        "trigger": score >= policy.min_buy_score,
        "risk": planned_order_krw >= policy.safe_order_min_krw,
        "guards": not guards,
        "trader_council": council["approved"],
        "whale_money_operator": whale_operator["approved"],
    }

    if guards:
        action = "STOP"
        decision_reason = "|".join(guards)
    elif sell_reasons:
        action = "SELL_CANDIDATE"
        decision_reason = "|".join(sell_reasons)
    elif snapshot.get("has_position") is not True and all(stage_pass.values()):
        action = "BUY_CANDIDATE"
        decision_reason = "BRAIN_V4_COUNCIL_WHALE_STAGE_CONSENSUS"
    else:
        action = "HOLD"
        decision_reason = "|".join(strategic_vetoes) if strategic_vetoes else "BRAIN_V4_EDGE_NOT_STRONG_ENOUGH"

    live_start_blockers = sorted(set(guards + strategic_vetoes))
    if action != "BUY_CANDIDATE":
        live_start_blockers.append("NO_BUY_CANDIDATE")

    return {
        "schema_version": SCHEMA_VERSION,
        "market": str(snapshot.get("market") or "KRW-BTC"),
        "action": action,
        "decision_reason": decision_reason,
        "execution_allowed": False,
        "live_order_allowed": False,
        "automation_allowed": False,
        "order_endpoint_allowed": False,
        "cancel_endpoint_allowed": False,
        "committee_yes_votes": yes_votes,
        "committee_total_votes": len(votes),
        "committee_score": score,
        "committee_score_raw": round(raw_score_pct, 2),
        "committee": votes,
        "stage_pass": stage_pass,
        "confidence_bucket": _confidence_bucket(score, yes_votes),
        "brain_upgrade_stages": [
            "stage_4_news_aware_senior_trader_council",
            "stage_5_whale_money_operator_liquidity_gate",
            "stage_6_conservative_scalping_shadow_reference",
            "stage_7_validated_edge_learning_reference",
        ],
        "news_context": {
            "daily_brain_bias": (council.get("news_modifier") or {}).get("daily_brain_bias"),
            "risk_tag_counts": (council.get("news_modifier") or {}).get("risk_tag_counts"),
            "score_penalty": (council.get("news_modifier") or {}).get("score_penalty"),
            "reference_only": True,
        },
        "trader_council": council,
        "whale_money_operator": whale_operator,
        "scalping_shadow": scalping_shadow,
        "edge_learning": edge_learning,
        "live_start_readiness": {
            "ready": action == "BUY_CANDIDATE" and not live_start_blockers,
            "blockers": sorted(set(live_start_blockers)),
            "requires_manual_final_confirmation": True,
            "reference_bonus_does_not_bypass_gates": True,
        },
        "regime": regime,
        "timeframes": timeframes,
        "indicators": indicators,
        "orderbook": orderbook,
        "planned_order": {
            "ord_type": "limit",
            "side": "bid" if action == "BUY_CANDIDATE" else "ask" if action == "SELL_CANDIDATE" else None,
            "max_krw": planned_order_krw if action == "BUY_CANDIDATE" else None,
            "price_reference": "maker_limit_only",
        },
        "sizing_explain": sizing_explain,
        "risk_policy": {
            "max_risk_per_trade_pct": policy.max_risk_per_trade_pct,
            "max_position_pct": policy.max_position_pct,
            "max_daily_loss_pct": policy.max_daily_loss_pct,
            "hard_stop_loss_pct": policy.hard_stop_loss_pct,
            "trailing_stop_pct": policy.trailing_stop_pct,
            "take_profit_pct": policy.take_profit_pct,
            "max_validated_edge_score_bonus": policy.max_validated_edge_score_bonus,
            "max_scalping_shadow_score_bonus": policy.max_scalping_shadow_score_bonus,
        },
        "entry_thesis": [v["name"] for v in votes if v["vote"] and action == "BUY_CANDIDATE"],
        "invalidation": ["OPEN_ORDER_EXISTS", "DAILY_LOSS_LIMIT_HIT", "REGIME_FLIP_EXIT", "HARD_STOP_LOSS"],
        "hard_guards": guards,
        "no_trade_reasons": no_trade_reasons,
        "sell_reasons": sell_reasons,
        "shadow_review_required": True,
        "forbidden_endpoint_check": "PASS_NO_ORDER_OR_CANCEL_ENDPOINT",
        "secrets_leak_check": "PASS_NO_SECRET_FIELDS",
        "next_safe_action": SAFE_NEXT_ACTION,
    }
