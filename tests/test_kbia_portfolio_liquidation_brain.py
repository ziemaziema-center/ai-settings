import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy.kbia_portfolio_liquidation_brain import evaluate_portfolio


def portfolio_fixture():
    return {
        "total_value_krw": 3_583_421,
        "cash_krw": 14_272,
        "positions": [
            {"symbol": "BTC", "market": "KRW-BTC", "valuation_krw": 616_078, "buy_amount_krw": 770_884, "pnl_pct": -0.2008, "weight_pct": 0.172},
            {"symbol": "ETH", "market": "KRW-ETH", "valuation_krw": 897_749, "buy_amount_krw": 1_426_270, "pnl_pct": -0.3706, "weight_pct": 0.251},
            {"symbol": "SOL", "market": "KRW-SOL", "valuation_krw": 881_632, "buy_amount_krw": 2_001_938, "pnl_pct": -0.5596, "weight_pct": 0.246},
            {"symbol": "ETC", "market": "KRW-ETC", "valuation_krw": 399_263, "buy_amount_krw": 1_999_938, "pnl_pct": -0.8004, "weight_pct": 0.111},
            {"symbol": "FCT2", "market": "KRW-FCT2", "valuation_krw": 222_352, "buy_amount_krw": 2_753_878, "pnl_pct": -0.9193, "weight_pct": 0.062},
            {"symbol": "DOT", "market": "KRW-DOT", "valuation_krw": 136_115, "buy_amount_krw": 3_849_055, "pnl_pct": -0.9646, "weight_pct": 0.038},
            {"symbol": "ALGO", "market": "KRW-ALGO", "valuation_krw": 85_971, "buy_amount_krw": 1_369_858, "pnl_pct": -0.9372, "weight_pct": 0.024},
            {"symbol": "DOGE", "market": "KRW-DOGE", "valuation_krw": 247_984, "buy_amount_krw": 770_659, "pnl_pct": -0.6782, "weight_pct": 0.069},
        ],
    }


def liquid_market(change=0.0):
    return {
        "listed": True,
        "best_bid": 100,
        "best_ask": 100.1,
        "spread_bps": 8,
        "bid_depth_top5_krw": 20_000_000,
        "ask_depth_top5_krw": 12_000_000,
        "acc_trade_price_24h": 5_000_000_000,
        "signed_change_rate": change,
    }


def test_core_assets_are_not_forced_exit():
    market = {symbol: liquid_market() for symbol in ["BTC", "ETH", "SOL", "ETC", "FCT2", "DOT", "ALGO", "DOGE"]}
    result = evaluate_portfolio(portfolio_fixture(), market)
    decisions = {row["symbol"]: row for row in result["decisions"]}
    assert decisions["BTC"]["action"] == "KEEP_CORE"
    assert decisions["ETH"]["action"] == "KEEP_CORE"
    assert decisions["SOL"]["action"] in {"KEEP_OR_TRIM_ON_BOUNCE", "TRIM_ON_STRENGTH"}
    assert decisions["BTC"]["live_sell_allowed"] is False


def test_deep_drawdown_tail_asset_is_exit_staged():
    market = {symbol: liquid_market() for symbol in ["BTC", "ETH", "SOL", "ETC", "FCT2", "DOT", "ALGO", "DOGE"]}
    result = evaluate_portfolio(portfolio_fixture(), market)
    decisions = {row["symbol"]: row for row in result["decisions"]}
    assert decisions["FCT2"]["action"] == "EXIT_STAGED"
    assert decisions["FCT2"]["shadow_first_slice_pct"] <= 0.25
    assert "SEVERE_DRAWDOWN" in decisions["FCT2"]["risk_flags"]


def test_dogecoin_is_reduced_not_core_kept():
    market = {symbol: liquid_market() for symbol in ["BTC", "ETH", "SOL", "ETC", "FCT2", "DOT", "ALGO", "DOGE"]}
    result = evaluate_portfolio(portfolio_fixture(), market)
    decisions = {row["symbol"]: row for row in result["decisions"]}
    assert decisions["DOGE"]["action"] == "REDUCE_STAGED"
    assert decisions["DOGE"]["shadow_total_sell_pct"] > 0


def test_low_liquidity_limits_first_slice():
    market = {symbol: liquid_market() for symbol in ["BTC", "ETH", "SOL", "ETC", "DOT", "ALGO", "DOGE"]}
    market["FCT2"] = {"listed": True, "spread_bps": 80, "acc_trade_price_24h": 10_000_000, "signed_change_rate": 0.0}
    result = evaluate_portfolio(portfolio_fixture(), market)
    fct2 = {row["symbol"]: row for row in result["decisions"]}["FCT2"]
    assert fct2["liquidity_state"] == "WIDE_SPREAD"
    assert fct2["shadow_first_slice_pct"] <= 0.25


def test_portfolio_output_is_shadow_only():
    market = {symbol: liquid_market() for symbol in ["BTC", "ETH", "SOL", "ETC", "FCT2", "DOT", "ALGO", "DOGE"]}
    result = evaluate_portfolio(portfolio_fixture(), market)
    assert result["execution_allowed"] is False
    assert result["live_sell_allowed"] is False
    assert result["order_endpoint_allowed"] is False
    assert result["cancel_endpoint_allowed"] is False
    assert result["market_sell_allowed"] is False
    assert result["no_profit_guarantee"] is True
    assert result["plan_valid"] is True
    assert result["schema_version"] == "kbia.portfolio_liquidation_brain.v3"


def test_unknown_asset_requires_classification_review():
    portfolio = portfolio_fixture()
    portfolio["positions"].append({"symbol": "NEWX", "market": "KRW-NEWX", "valuation_krw": 50_000, "buy_amount_krw": 500_000, "pnl_pct": -0.9, "weight_pct": 0.014})
    market = {symbol: liquid_market() for symbol in ["BTC", "ETH", "SOL", "ETC", "FCT2", "DOT", "ALGO", "DOGE", "NEWX"]}
    result = evaluate_portfolio(portfolio, market)
    newx = {row["symbol"]: row for row in result["decisions"]}["NEWX"]
    assert newx["action"] == "REVIEW_CLASSIFICATION"
    assert newx["shadow_first_slice_value_krw"] == 0
    assert newx["classification"]["unknown_asset_review_required"] is True


def test_missing_orderbook_prevents_first_slice():
    portfolio = portfolio_fixture()
    market = {symbol: liquid_market() for symbol in ["BTC", "ETH", "SOL", "ETC", "DOT", "ALGO", "DOGE"]}
    market["FCT2"] = {"listed": True, "spread_bps": 8, "acc_trade_price_24h": 5_000_000_000, "signed_change_rate": 0.0}
    result = evaluate_portfolio(portfolio, market)
    fct2 = {row["symbol"]: row for row in result["decisions"]}["FCT2"]
    assert "ORDERBOOK_MISSING" in fct2["execution_quality"]["flags"]
    assert fct2["shadow_first_slice_value_krw"] == 0


def test_portfolio_validation_catches_duplicate_market():
    portfolio = portfolio_fixture()
    portfolio["positions"][1]["market"] = "KRW-BTC"
    market = {symbol: liquid_market() for symbol in ["BTC", "ETH", "SOL", "ETC", "FCT2", "DOT", "ALGO", "DOGE"]}
    result = evaluate_portfolio(portfolio, market)
    assert result["plan_valid"] is False
    assert "DUPLICATE_MARKETS" in result["validation_errors"]


if __name__ == "__main__":
    test_core_assets_are_not_forced_exit()
    test_deep_drawdown_tail_asset_is_exit_staged()
    test_dogecoin_is_reduced_not_core_kept()
    test_low_liquidity_limits_first_slice()
    test_portfolio_output_is_shadow_only()
    test_unknown_asset_requires_classification_review()
    test_missing_orderbook_prevents_first_slice()
    test_portfolio_validation_catches_duplicate_market()
    print("KBIA_PORTFOLIO_LIQUIDATION_BRAIN_TESTS_PASS")
