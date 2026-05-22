from __future__ import annotations

from dataclasses import dataclass
from typing import Any


SCHEMA_VERSION = "kbia.portfolio_liquidation_brain.v3"
SAFE_NEXT_ACTION = "human_review_then_shadow_rehearsal_only_no_live_sell"


CORE_ASSETS = {"BTC", "ETH"}
CORE_GROWTH_ASSETS = {"SOL"}
MEME_ASSETS = {"DOGE"}
LEGACY_ALT_ASSETS = {"ETC", "DOT", "ALGO"}
ILLQ_OR_TAIL_ASSETS = {"FCT2", "NKN", "APENFT", "EVR", "RVN", "SALT", "SXP", "VTHO"}


@dataclass(frozen=True)
class PortfolioPolicy:
    target_cash_pct_after_cleanup: float = 0.25
    max_single_alt_pct: float = 0.05
    max_meme_pct: float = 0.03
    min_core_hold_pct: float = 0.45
    deep_drawdown_pct: float = -0.70
    severe_drawdown_pct: float = -0.85
    weak_drawdown_pct: float = -0.50
    max_safe_spread_bps: float = 35.0
    min_daily_liquidity_krw: float = 500_000_000.0
    min_bid_depth_coverage: float = 2.5
    max_bid_depth_slice_pct: float = 0.025
    max_sell_pressure_ratio: float = 0.62
    min_exit_value_krw: float = 5000.0
    max_first_slice_pct: float = 0.25
    max_first_slice_stressed_pct: float = 0.12
    max_first_slice_bad_execution_pct: float = 0.08
    max_daily_shadow_liquidation_pct: float = 0.35
    hq_cleanup_score_threshold: float = 60.0
    hq_exit_score_threshold: float = 74.0


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    if parsed != parsed or parsed in (float("inf"), float("-inf")):
        return default
    return parsed


def _asset_tier(symbol: str) -> str:
    symbol = symbol.upper()
    if symbol in CORE_ASSETS:
        return "CORE"
    if symbol in CORE_GROWTH_ASSETS:
        return "CORE_GROWTH"
    if symbol in MEME_ASSETS:
        return "MEME"
    if symbol in LEGACY_ALT_ASSETS:
        return "LEGACY_ALT"
    if symbol in ILLQ_OR_TAIL_ASSETS:
        return "TAIL_OR_ILLIQUID"
    return "UNKNOWN_ALT"


def _classification(symbol: str) -> dict[str, Any]:
    tier = _asset_tier(symbol)
    if tier == "CORE":
        return {"tier": tier, "classification_source": "locked_core_list", "classification_confidence": 0.95, "classification_reason": "BTC_ETH_CORE", "unknown_asset_review_required": False}
    if tier == "CORE_GROWTH":
        return {"tier": tier, "classification_source": "locked_core_growth_list", "classification_confidence": 0.8, "classification_reason": "HIGH_BETA_MAJOR", "unknown_asset_review_required": False}
    if tier == "MEME":
        return {"tier": tier, "classification_source": "locked_meme_list", "classification_confidence": 0.8, "classification_reason": "MEME_EXPOSURE_CAP", "unknown_asset_review_required": False}
    if tier == "LEGACY_ALT":
        return {"tier": tier, "classification_source": "locked_legacy_alt_list", "classification_confidence": 0.75, "classification_reason": "LEGACY_ALT_UNDERPERFORMANCE_RISK", "unknown_asset_review_required": False}
    if tier == "TAIL_OR_ILLIQUID":
        return {"tier": tier, "classification_source": "locked_tail_asset_list", "classification_confidence": 0.8, "classification_reason": "TAIL_OR_AIRDROP_OR_ILLIQUID", "unknown_asset_review_required": False}
    return {"tier": tier, "classification_source": "unknown_symbol", "classification_confidence": 0.2, "classification_reason": "UNKNOWN_ASSET_REQUIRES_MANUAL_CLASSIFICATION", "unknown_asset_review_required": True}


def _liquidity_state(market: dict[str, Any], policy: PortfolioPolicy) -> str:
    if market.get("listed") is False:
        return "UNLISTED_OR_NO_PUBLIC_MARKET"
    spread = _as_float(market.get("spread_bps"), 999.0)
    liquidity = _as_float(market.get("acc_trade_price_24h"), 0.0)
    if spread > policy.max_safe_spread_bps:
        return "WIDE_SPREAD"
    if liquidity < policy.min_daily_liquidity_krw:
        return "LOW_LIQUIDITY"
    return "LIQUID"


def _execution_quality(market: dict[str, Any], valuation_krw: float, policy: PortfolioPolicy) -> dict[str, Any]:
    best_bid = _as_float(market.get("best_bid"))
    best_ask = _as_float(market.get("best_ask"))
    bid_depth = _as_float(market.get("bid_depth_top5_krw"))
    ask_depth = _as_float(market.get("ask_depth_top5_krw"))
    spread = _as_float(market.get("spread_bps"), 999.0)
    depth_coverage = bid_depth / max(valuation_krw, 1.0)
    sell_pressure_ratio = ask_depth / (bid_depth + ask_depth) if bid_depth + ask_depth > 0 else 1.0
    flags: list[str] = []
    if best_bid <= 0 or best_ask <= 0:
        flags.append("ORDERBOOK_MISSING")
    if bid_depth <= 0:
        flags.append("ZERO_BID_DEPTH")
    if spread > policy.max_safe_spread_bps:
        flags.append("SPREAD_TOO_WIDE_FOR_CLEAN_EXIT")
    if depth_coverage < policy.min_bid_depth_coverage:
        flags.append("BID_DEPTH_THIN_FOR_POSITION_SIZE")
    if sell_pressure_ratio > policy.max_sell_pressure_ratio:
        flags.append("ASK_PRESSURE_HEAVY")
    quality = "GOOD"
    if len(flags) >= 2:
        quality = "BAD"
    elif flags:
        quality = "CAUTION"
    return {
        "quality": quality,
        "bid_depth_top5_krw": round(bid_depth, 2),
        "ask_depth_top5_krw": round(ask_depth, 2),
        "bid_depth_coverage": round(depth_coverage, 4),
        "sell_pressure_ratio": round(sell_pressure_ratio, 4),
        "max_first_slice_by_depth_krw": round(bid_depth * policy.max_bid_depth_slice_pct, 0),
        "flags": sorted(flags),
    }


def _trend_state(market: dict[str, Any]) -> str:
    change_rate = _as_float(market.get("signed_change_rate"), 0.0)
    if change_rate <= -0.05:
        return "DAY_DUMP"
    if change_rate >= 0.04:
        return "DAY_BOUNCE"
    return "NEUTRAL"


def _market_regime(market_data: dict[str, dict[str, Any]]) -> dict[str, Any]:
    btc_change = _as_float(market_data.get("BTC", {}).get("signed_change_rate"))
    core_changes = [
        _as_float(market_data.get(symbol, {}).get("signed_change_rate"))
        for symbol in ("BTC", "ETH", "SOL")
        if symbol in market_data
    ]
    alt_changes = [
        _as_float(row.get("signed_change_rate"))
        for symbol, row in market_data.items()
        if symbol not in {"BTC", "ETH", "SOL"} and row.get("listed") is not False
    ]
    weak_assets = sum(1 for change in core_changes + alt_changes if change <= -0.04)
    strong_assets = sum(1 for change in core_changes + alt_changes if change >= 0.04)
    checked = len(core_changes) + len(alt_changes)
    name = "NEUTRAL"
    sell_aggression_multiplier = 1.0
    cleanup_bias = "NORMAL"
    if btc_change <= -0.045 or (checked and weak_assets / checked >= 0.5):
        name = "RISK_OFF"
        sell_aggression_multiplier = 0.45
        cleanup_bias = "PROTECT_FROM_PANIC_SELL"
    elif btc_change >= 0.025 and strong_assets >= max(1, checked // 4):
        name = "RISK_ON_BOUNCE"
        sell_aggression_multiplier = 1.15
        cleanup_bias = "USE_STRENGTH_FOR_CLEANUP"
    elif btc_change <= -0.02:
        name = "SOFT_RISK_OFF"
        sell_aggression_multiplier = 0.7
        cleanup_bias = "SMALLER_SLICES"
    return {
        "name": name,
        "btc_signed_change_rate": round(btc_change, 4),
        "weak_assets": weak_assets,
        "strong_assets": strong_assets,
        "checked_assets": checked,
        "sell_aggression_multiplier": sell_aggression_multiplier,
        "cleanup_bias": cleanup_bias,
    }


def _relative_strength_map(market_data: dict[str, dict[str, Any]]) -> dict[str, str]:
    changes = [
        (symbol, _as_float(row.get("signed_change_rate")))
        for symbol, row in market_data.items()
        if row.get("listed") is not False
    ]
    if not changes:
        return {}
    ordered = sorted(changes, key=lambda item: item[1], reverse=True)
    result: dict[str, str] = {}
    last_index = len(ordered) - 1
    for index, (symbol, _) in enumerate(ordered):
        if index <= last_index * 0.33:
            result[symbol] = "LEADER"
        elif index >= last_index * 0.67:
            result[symbol] = "LAGGARD"
        else:
            result[symbol] = "MID"
    return result


def _target_weight_pct(symbol: str, policy: PortfolioPolicy) -> float:
    tier = _asset_tier(symbol)
    if tier == "CORE":
        return 0.18
    if tier == "CORE_GROWTH":
        return 0.12
    if tier == "MEME":
        return policy.max_meme_pct
    if tier in {"LEGACY_ALT", "TAIL_OR_ILLIQUID", "UNKNOWN_ALT"}:
        return policy.max_single_alt_pct
    return 0.0


def _hq_committee(
    symbol: str,
    tier: str,
    pnl_pct: float,
    weight_pct: float,
    target_weight: float,
    liquidity: str,
    trend: str,
    relative_strength: str,
    execution_quality: dict[str, Any],
    market_regime: dict[str, Any],
    policy: PortfolioPolicy,
) -> dict[str, Any]:
    specs = [
        ("hq_capital_rotation", tier in {"LEGACY_ALT", "TAIL_OR_ILLIQUID", "UNKNOWN_ALT"} and pnl_pct <= policy.weak_drawdown_pct, 10),
        ("survival_quality", tier not in {"CORE", "CORE_GROWTH"} and pnl_pct <= policy.deep_drawdown_pct, 9),
        ("core_anchor_protection", tier not in {"CORE", "CORE_GROWTH"}, 8),
        ("concentration_risk", weight_pct > max(target_weight * 1.35, 0.025), 7),
        ("liquidity_exit_quality", liquidity == "LIQUID" and execution_quality["quality"] != "BAD", 8),
        ("avoid_panic_dump", trend != "DAY_DUMP" and market_regime["name"] != "RISK_OFF", 7),
        ("relative_weakness", relative_strength == "LAGGARD", 6),
        ("meme_tail_risk", tier in {"MEME", "TAIL_OR_ILLIQUID"}, 6),
        ("cash_rebuild_need", symbol not in CORE_ASSETS, 5),
        ("spread_depth_discipline", not execution_quality["flags"], 4),
    ]
    votes = [{"name": name, "vote": bool(vote), "score": weight if vote else 0, "weight": weight} for name, vote, weight in specs]
    max_score = sum(vote["weight"] for vote in votes)
    raw_score = sum(vote["score"] for vote in votes)
    return {
        "role": "HQ_20Y_TRADING_MASTER_PLUS_IQ180_CRYPTO_AGENTS",
        "yes_votes": sum(1 for vote in votes if vote["vote"]),
        "total_votes": len(votes),
        "score": round(raw_score / max_score * 100, 2) if max_score else 0.0,
        "votes": votes,
    }


def _execution_plan(symbol: str, action: str, sell_pct: float, first_slice_pct: float, valuation: float, trend: str, execution_quality: dict[str, Any], market_regime: dict[str, Any]) -> dict[str, Any]:
    if sell_pct <= 0:
        return {
            "profile": "NO_ACTION",
            "slices": [],
            "limit_only": True,
            "market_order_allowed": False,
            "stop_conditions": ["OPEN_ORDER_EXISTS", "WIDE_SPREAD", "RISK_OFF_PANIC", "MANUAL_REVIEW_REQUIRED"],
        }
    profile = "BOUNCE_CLEANUP" if market_regime["name"] == "RISK_ON_BOUNCE" else "CAUTIOUS_CLEANUP"
    if trend == "DAY_DUMP" or market_regime["name"] == "RISK_OFF":
        profile = "WAIT_FOR_STABILIZATION"
    if execution_quality["quality"] == "BAD":
        profile = "MICRO_SLICES_ONLY"
    slices = []
    remaining = sell_pct
    first = min(first_slice_pct, remaining)
    if first > 0:
        slices.append({"slice": 1, "pct": round(first, 4), "shadow_value_krw": round(valuation * first, 0), "condition": "maker_limit_near_best_ask_after_spread_check"})
        remaining -= first
    slice_index = 2
    while remaining > 0.0001 and slice_index <= 5:
        pct = min(first_slice_pct, remaining)
        slices.append({"slice": slice_index, "pct": round(pct, 4), "shadow_value_krw": round(valuation * pct, 0), "condition": "only_after_previous_slice_final_and_no_new_open_order"})
        remaining -= pct
        slice_index += 1
    return {
        "profile": profile,
        "slices": slices,
        "limit_only": True,
        "market_order_allowed": False,
        "stop_conditions": ["OPEN_ORDER_EXISTS", "SPREAD_TOO_WIDE", "BID_DEPTH_COLLAPSE", "RATE_LIMIT", "MANUAL_REVIEW_REQUIRED"],
    }


def evaluate_position(
    position: dict[str, Any],
    market: dict[str, Any] | None,
    total_value_krw: float,
    policy: PortfolioPolicy | None = None,
    market_regime: dict[str, Any] | None = None,
    relative_strength: str = "UNKNOWN",
) -> dict[str, Any]:
    policy = policy or PortfolioPolicy()
    market = market or {}
    market_regime = market_regime or {"name": "NEUTRAL", "sell_aggression_multiplier": 1.0}
    symbol = str(position.get("symbol", "")).upper()
    valuation = _as_float(position.get("valuation_krw"))
    buy_amount = _as_float(position.get("buy_amount_krw"))
    pnl_pct = _as_float(position.get("pnl_pct"))
    weight_pct = _as_float(position.get("weight_pct"), valuation / total_value_krw if total_value_krw > 0 else 0.0)
    classification = _classification(symbol)
    tier = classification["tier"]
    liquidity = _liquidity_state(market, policy)
    trend = _trend_state(market)
    execution_quality = _execution_quality(market, valuation, policy)
    reasons: list[str] = []
    risk_flags: list[str] = []

    if valuation < policy.min_exit_value_krw:
        risk_flags.append("DUST_VALUE")
    if pnl_pct <= policy.severe_drawdown_pct:
        risk_flags.append("SEVERE_DRAWDOWN")
    elif pnl_pct <= policy.deep_drawdown_pct:
        risk_flags.append("DEEP_DRAWDOWN")
    elif pnl_pct <= policy.weak_drawdown_pct:
        risk_flags.append("WEAK_DRAWDOWN")
    if liquidity != "LIQUID":
        risk_flags.append(liquidity)
    risk_flags.extend(execution_quality["flags"])
    if relative_strength == "LAGGARD":
        risk_flags.append("RELATIVE_STRENGTH_LAGGARD")
    if weight_pct > _target_weight_pct(symbol, policy) * 1.5 and tier not in {"CORE", "CORE_GROWTH"}:
        risk_flags.append("OVER_TARGET_ALT_WEIGHT")

    target_weight = _target_weight_pct(symbol, policy)
    sell_pct = 0.0
    action = "REVIEW"
    priority = 50

    hq = _hq_committee(symbol, tier, pnl_pct, weight_pct, target_weight, liquidity, trend, relative_strength, execution_quality, market_regime, policy)

    if tier == "CORE":
        action = "KEEP_CORE"
        priority = 10
        reasons.append("BTC_ETH_CORE_LIQUIDITY_ANCHOR")
        if weight_pct > target_weight * 1.6 and trend == "DAY_BOUNCE":
            action = "TRIM_ON_STRENGTH"
            sell_pct = min(0.15, (weight_pct - target_weight) / max(weight_pct, 0.0001))
            priority = 35
            reasons.append("CORE_OVERWEIGHT_TRIM_ONLY_ON_STRENGTH")
    elif tier == "CORE_GROWTH":
        action = "KEEP_OR_TRIM_ON_BOUNCE"
        priority = 25
        reasons.append("SOL_HIGH_BETA_CORE_GROWTH_NOT_PANIC_EXIT")
        if weight_pct > target_weight * 1.7 and trend == "DAY_BOUNCE":
            sell_pct = min(0.20, (weight_pct - target_weight) / max(weight_pct, 0.0001))
            action = "TRIM_ON_STRENGTH"
            priority = 40
    elif tier == "MEME":
        action = "REDUCE_STAGED"
        sell_pct = 0.35 if pnl_pct > policy.deep_drawdown_pct else 0.50
        priority = 65
        reasons.append("MEME_EXPOSURE_NOT_CORE_CAPITAL")
        if liquidity != "LIQUID":
            sell_pct = min(sell_pct, 0.25)
            reasons.append("LIMIT_FIRST_SLICE_BECAUSE_LIQUIDITY_WEAK")
    elif tier in {"LEGACY_ALT", "TAIL_OR_ILLIQUID", "UNKNOWN_ALT"}:
        if tier == "UNKNOWN_ALT":
            action = "REVIEW_CLASSIFICATION"
            sell_pct = 0.0
            priority = 55
            reasons.append("UNKNOWN_ASSET_NOT_AUTO_LIQUIDATED")
        elif pnl_pct <= policy.severe_drawdown_pct or tier == "TAIL_OR_ILLIQUID" or hq["score"] >= policy.hq_exit_score_threshold:
            action = "EXIT_STAGED"
            sell_pct = 0.75 if liquidity == "LIQUID" and trend != "DAY_DUMP" else 0.35
            priority = 90 if pnl_pct <= policy.severe_drawdown_pct else 80
            reasons.append("CAPITAL_RECYCLING_FROM_DEAD_ALT")
        elif pnl_pct <= policy.weak_drawdown_pct or hq["score"] >= policy.hq_cleanup_score_threshold:
            action = "REDUCE_STAGED"
            sell_pct = 0.50 if trend != "DAY_DUMP" else 0.25
            priority = 70
            reasons.append("WEAK_LEGACY_ALT_REDUCE_AFTER_LONG_UNDERPERFORMANCE")
        else:
            action = "REVIEW"
            sell_pct = 0.20 if weight_pct > target_weight else 0.0
            priority = 45
            reasons.append("ALT_REVIEW_NOT_FORCED_EXIT")

    if valuation < policy.min_exit_value_krw:
        action = "REVIEW_DUST"
        sell_pct = 0.0
        priority = 20
        reasons.append("BELOW_SAFE_EXIT_VALUE")

    sell_pct = round(sell_pct * _as_float(market_regime.get("sell_aggression_multiplier"), 1.0), 4)
    if action in {"KEEP_CORE", "KEEP_OR_TRIM_ON_BOUNCE", "REVIEW_DUST", "REVIEW_CLASSIFICATION"}:
        sell_pct = 0.0
    first_slice_cap = policy.max_first_slice_pct
    if market_regime["name"] in {"RISK_OFF", "SOFT_RISK_OFF"}:
        first_slice_cap = min(first_slice_cap, policy.max_first_slice_stressed_pct)
        reasons.append("MARKET_STRESS_SMALLER_SLICES")
    if execution_quality["quality"] == "BAD":
        first_slice_cap = min(first_slice_cap, policy.max_first_slice_bad_execution_pct)
        reasons.append("BAD_EXECUTION_QUALITY_MICRO_SLICES")
    first_slice_pct = min(sell_pct, first_slice_cap)
    shadow_sell_value_krw = round(valuation * sell_pct, 0)
    first_slice_value_krw = round(valuation * first_slice_pct, 0)
    depth_cap = _as_float(execution_quality.get("max_first_slice_by_depth_krw"))
    if first_slice_value_krw > 0 and depth_cap <= 0:
        first_slice_value_krw = 0.0
        first_slice_pct = 0.0
        reasons.append("NO_BID_DEPTH_NO_FIRST_SLICE")
    elif first_slice_value_krw > depth_cap > 0:
        first_slice_value_krw = round(depth_cap, 0)
        first_slice_pct = round(first_slice_value_krw / valuation, 4) if valuation > 0 else 0.0
        reasons.append("FIRST_SLICE_CAPPED_BY_BID_DEPTH")
    execution_plan = _execution_plan(symbol, action, sell_pct, first_slice_pct, valuation, trend, execution_quality, market_regime)
    return {
        "symbol": symbol,
        "market": position.get("market", f"KRW-{symbol}"),
        "tier": tier,
        "classification": classification,
        "action": action,
        "priority": priority,
        "valuation_krw": round(valuation, 0),
        "buy_amount_krw": round(buy_amount, 0),
        "pnl_pct": round(pnl_pct, 4),
        "weight_pct": round(weight_pct, 4),
        "target_weight_pct": round(target_weight, 4),
        "liquidity_state": liquidity,
        "trend_state": trend,
        "relative_strength": relative_strength,
        "market_regime": market_regime["name"],
        "execution_quality": execution_quality,
        "hq_committee": hq,
        "risk_flags": sorted(set(risk_flags)),
        "reasons": sorted(set(reasons)),
        "shadow_total_sell_pct": round(sell_pct, 4),
        "shadow_first_slice_pct": round(first_slice_pct, 4),
        "shadow_total_sell_value_krw": shadow_sell_value_krw,
        "shadow_first_slice_value_krw": first_slice_value_krw,
        "execution_plan": execution_plan,
        "execution_allowed": False,
        "live_sell_allowed": False,
        "order_endpoint_allowed": False,
        "cancel_endpoint_allowed": False,
}


def _portfolio_validation_errors(portfolio: dict[str, Any], decisions: list[dict[str, Any]], total_value: float, cash_krw: float, policy: PortfolioPolicy) -> list[str]:
    errors: list[str] = []
    positions = list(portfolio.get("positions") or [])
    markets = [str(position.get("market") or "") for position in positions if position.get("market")]
    if len(markets) != len(set(markets)):
        errors.append("DUPLICATE_MARKETS")
    if any(_as_float(position.get("valuation_krw")) < 0 for position in positions):
        errors.append("NEGATIVE_VALUATION")
    if any(_as_float(position.get("buy_amount_krw")) < 0 for position in positions):
        errors.append("NEGATIVE_BUY_AMOUNT")
    position_value = sum(_as_float(position.get("valuation_krw")) for position in positions) + cash_krw
    if total_value > 0 and abs(total_value - position_value) / total_value > 0.08:
        errors.append("PORTFOLIO_TOTAL_MISMATCH")
    core_value = sum(row["valuation_krw"] for row in decisions if row["tier"] in {"CORE", "CORE_GROWTH"})
    planned_core_sell = sum(row["shadow_first_slice_value_krw"] for row in decisions if row["tier"] in {"CORE", "CORE_GROWTH"})
    projected_core_pct = (core_value - planned_core_sell) / total_value if total_value > 0 else 0.0
    if projected_core_pct < policy.min_core_hold_pct:
        errors.append("CORE_FLOOR_BREACH")
    max_daily_value = total_value * policy.max_daily_shadow_liquidation_pct
    if sum(row["shadow_first_slice_value_krw"] for row in decisions) > max_daily_value + 1:
        errors.append("DAILY_LIQUIDATION_CAP_BREACH")
    if any(row["shadow_first_slice_value_krw"] > 0 and "ORDERBOOK_MISSING" in row["execution_quality"]["flags"] for row in decisions):
        errors.append("PLANNED_SLICE_WITH_MISSING_ORDERBOOK")
    if any(row["shadow_first_slice_value_krw"] > 0 and row["classification"]["unknown_asset_review_required"] for row in decisions):
        errors.append("UNKNOWN_ASSET_HAS_PLANNED_SLICE")
    return sorted(set(errors))


def evaluate_portfolio(portfolio: dict[str, Any], market_data: dict[str, dict[str, Any]] | None = None, policy: PortfolioPolicy | None = None) -> dict[str, Any]:
    policy = policy or PortfolioPolicy()
    market_data = market_data or {}
    positions = list(portfolio.get("positions") or [])
    total_value = _as_float(portfolio.get("total_value_krw"), sum(_as_float(p.get("valuation_krw")) for p in positions))
    cash_krw = _as_float(portfolio.get("cash_krw"))
    market_regime = _market_regime(market_data)
    relative_strength = _relative_strength_map(market_data)
    decisions = [
        evaluate_position(
            position,
            market_data.get(str(position.get("symbol", "")).upper()),
            total_value,
            policy,
            market_regime,
            relative_strength.get(str(position.get("symbol", "")).upper(), "UNKNOWN"),
        )
        for position in positions
    ]
    decisions = sorted(decisions, key=lambda row: (-row["priority"], -row["shadow_first_slice_value_krw"], row["symbol"]))
    core_value = sum(row["valuation_krw"] for row in decisions if row["tier"] in {"CORE", "CORE_GROWTH"})
    planned_first_slice = sum(row["shadow_first_slice_value_krw"] for row in decisions)
    max_daily_value = round(total_value * policy.max_daily_shadow_liquidation_pct, 0)
    if planned_first_slice > max_daily_value and planned_first_slice > 0:
        scale = max_daily_value / planned_first_slice
        for row in decisions:
            row["shadow_first_slice_pct"] = round(row["shadow_first_slice_pct"] * scale, 4)
            row["shadow_first_slice_value_krw"] = round(row["shadow_first_slice_value_krw"] * scale, 0)
        planned_first_slice = sum(row["shadow_first_slice_value_krw"] for row in decisions)

    exit_candidates = [row["symbol"] for row in decisions if row["action"] == "EXIT_STAGED"]
    reduce_candidates = [row["symbol"] for row in decisions if row["action"] in {"REDUCE_STAGED", "TRIM_ON_STRENGTH"}]
    keep_candidates = [row["symbol"] for row in decisions if row["action"].startswith("KEEP")]
    projected_cash = cash_krw + planned_first_slice
    projected_cash_pct = projected_cash / total_value if total_value > 0 else 0.0
    validation_errors = _portfolio_validation_errors(portfolio, decisions, total_value, cash_krw, policy)
    return {
        "schema_version": SCHEMA_VERSION,
        "mode": "portfolio_shadow_liquidation_plan",
        "portfolio_total_value_krw": round(total_value, 0),
        "cash_krw": round(cash_krw, 0),
        "cash_pct": round(cash_krw / total_value, 4) if total_value > 0 else 0.0,
        "core_value_krw": round(core_value, 0),
        "core_pct": round(core_value / total_value, 4) if total_value > 0 else 0.0,
        "market_regime": market_regime,
        "target_cash_pct_after_cleanup": policy.target_cash_pct_after_cleanup,
        "projected_cash_after_first_slice_krw": round(projected_cash, 0),
        "projected_cash_after_first_slice_pct": round(projected_cash_pct, 4),
        "planned_first_slice_krw": round(planned_first_slice, 0),
        "planned_total_shadow_sell_krw": round(sum(row["shadow_total_sell_value_krw"] for row in decisions), 0),
        "plan_valid": not validation_errors,
        "validation_errors": validation_errors,
        "exit_candidates": exit_candidates,
        "reduce_candidates": reduce_candidates,
        "keep_candidates": keep_candidates,
        "decisions": decisions,
        "hq_upgrade_layers": [
            "stage_1_market_regime_overlay",
            "stage_2_hq_committee_asset_scoring",
            "stage_3_execution_quality_and_slice_schedule",
        ],
        "portfolio_action": "CLEANUP_SHADOW_ONLY" if exit_candidates or reduce_candidates else "HOLD_SHADOW_ONLY",
        "execution_allowed": False,
        "live_sell_allowed": False,
        "automation_allowed": False,
        "order_endpoint_allowed": False,
        "cancel_endpoint_allowed": False,
        "market_sell_allowed": False,
        "scheduler_allowed": False,
        "no_profit_guarantee": True,
        "review_required": True,
        "next_safe_action": SAFE_NEXT_ACTION,
    }
