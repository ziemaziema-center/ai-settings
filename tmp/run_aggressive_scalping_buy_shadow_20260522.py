from __future__ import annotations

import json
import sys
from datetime import datetime
from decimal import Decimal, ROUND_DOWN
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy.kbia_strategy_kernel import StrategyPolicy, evaluate_strategy


def _candles(start: float, step: float, count: int = 72) -> list[dict[str, float]]:
    rows = []
    price = start
    for i in range(count):
        price *= 1 + step
        if i % 11 == 0:
            price *= 0.998
        rows.append(
            {
                "close": round(price, 4),
                "high": round(price * 1.006, 4),
                "low": round(price * 0.994, 4),
                "volume_krw": 2_200_000_000 + i * 19_000_000,
            }
        )
    return rows


def _news_context() -> dict[str, object]:
    date_str = datetime.now().date().isoformat()
    digest_path = ROOT / "reports" / f"daily_crypto_news_digest_{date_str}.json"
    if not digest_path.exists():
        return {"daily_brain_bias": "UNKNOWN_REFERENCE", "risk_tag_counts": {}, "symbol_counts": {}}
    digest = json.loads(digest_path.read_text(encoding="utf-8"))
    return {
        "daily_brain_bias": digest.get("daily_brain_bias"),
        "risk_tag_counts": digest.get("risk_tag_counts", {}),
        "symbol_counts": digest.get("symbol_counts", {}),
    }


def _volume_for_krw(price: Decimal, krw: Decimal) -> str:
    return format((krw / price).quantize(Decimal("0.00000001"), rounding=ROUND_DOWN), "f")


def _shadow_case(market: str, price: Decimal, spread_bps: Decimal, news: dict[str, object], loop_no: int) -> dict[str, object]:
    best_bid = price
    best_ask = price * (Decimal("1") + spread_bps / Decimal("10000"))
    maker_bid = best_bid
    plan_krw = Decimal("10000")
    volume = _volume_for_krw(maker_bid, plan_krw)
    estimated = (maker_bid * Decimal(volume)).quantize(Decimal("1"), rounding=ROUND_DOWN)
    effective_news = dict(news)
    if loop_no == 3:
        effective_news["daily_brain_bias"] = "DEFENSIVE_REFERENCE"
    snapshot = {
        "market": market,
        "equity_krw": 3_500_000,
        "liquidity_24h_krw": 12_000_000_000,
        "spread_bps": float(spread_bps),
        "open_order_exists": False,
        "open_order_count": 0,
        "workflow_active": False,
        "cron_enabled": False,
        "system_stop_active": False,
        "live_fuse_state": "disabled",
        "daily_loss_pct": 0,
        "portfolio_heat_pct": 0.08,
        "correlation_heat_pct": 0.12,
        "relative_strength_20": 0.04,
        "btc_regime": "BULL_TREND",
        "has_position": False,
        "best_bid": float(best_bid),
        "best_ask": float(best_ask),
        "bid_depth_top5_krw": 1_700_000_000,
        "ask_depth_top5_krw": 1_050_000_000,
        "news_context": effective_news,
    }
    decision = evaluate_strategy(snapshot, _candles(float(price), 0.004 + loop_no * 0.0003), StrategyPolicy())
    helper_payload = {
        "market": market,
        "side": "bid",
        "ord_type": "limit",
        "price": format(maker_bid, "f"),
        "volume": volume,
        "estimated_krw_value": format(estimated, "f"),
        "open_order_exists": False,
        "brain_schema_version": decision["schema_version"],
        "brain_action": decision["action"],
        "brain_live_ready": decision["live_start_readiness"]["ready"],
        "brain_candidate_score": decision["committee_score"],
        "news_bias": effective_news.get("daily_brain_bias"),
        "scalping_candidate": decision["scalping_shadow"]["candidate"],
    }
    ready_for_test_endpoint = (
        decision["action"] == "BUY_CANDIDATE"
        and decision["live_start_readiness"]["ready"] is True
        and decision["scalping_shadow"]["candidate"] is True
        and decision["committee_score"] >= 78
        and effective_news.get("daily_brain_bias") != "DEFENSIVE_REFERENCE"
    )
    return {
        "loop_no": loop_no,
        "market": market,
        "decision": {
            "schema_version": decision["schema_version"],
            "action": decision["action"],
            "committee_score": decision["committee_score"],
            "confidence_bucket": decision["confidence_bucket"],
            "stage_pass": decision["stage_pass"],
            "scalping_shadow": decision["scalping_shadow"],
            "live_start_readiness": decision["live_start_readiness"],
            "execution_allowed": decision["execution_allowed"],
            "live_order_allowed": decision["live_order_allowed"],
            "order_endpoint_allowed": decision["order_endpoint_allowed"],
            "cancel_endpoint_allowed": decision["cancel_endpoint_allowed"],
        },
        "helper_buy_test_payload": helper_payload,
        "ready_for_buy_test_endpoint": ready_for_test_endpoint,
        "live_buy_submitted": False,
    }


def main() -> int:
    date_str = datetime.now().date().isoformat()
    news = _news_context()
    cases = [
        _shadow_case("KRW-BTC", Decimal("100000000"), Decimal("5"), news, 1),
        _shadow_case("KRW-ETH", Decimal("5000000"), Decimal("7"), news, 2),
        _shadow_case("KRW-SOL", Decimal("280000"), Decimal("6"), news, 3),
    ]
    report = {
        "date": date_str,
        "mode": "aggressive_scalping_buy_shadow_v1",
        "purpose": "prepare live buy gate inputs without submitting live orders",
        "upgrade_stages": [
            "stage_a_live_buy_helper_gate_payload",
            "stage_b_aggressive_scalping_shadow_candidate_loop",
            "stage_c_three_loop_blocker_and_candidate_evidence",
        ],
        "news_context": news,
        "loop_count": len(cases),
        "ready_for_buy_test_count": sum(1 for case in cases if case["ready_for_buy_test_endpoint"]),
        "live_buy_submitted": False,
        "live_order_count": 0,
        "cases": cases,
        "safety": {
            "runtime_mutated": False,
            "live_buy_submitted": False,
            "live_sell_submitted": False,
            "cancel_submitted": False,
            "market_order_allowed": False,
            "scheduler_started": False,
            "secret_exposure": False,
        },
    }
    report_json = ROOT / "reports" / f"aggressive_scalping_buy_shadow_{date_str}.json"
    report_md = ROOT / "reports" / f"aggressive_scalping_buy_shadow_{date_str}.md"
    report_json.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")
    lines = [
        f"# Aggressive Scalping Buy Shadow - {date_str}",
        "",
        f"- mode: `{report['mode']}`",
        f"- loop_count: `{report['loop_count']}`",
        f"- ready_for_buy_test_count: `{report['ready_for_buy_test_count']}`",
        "- live_buy_submitted: `false`",
        "- live_order_count: `0`",
        "",
        "## Loop Summary",
    ]
    for case in cases:
        decision = case["decision"]
        lines.extend(
            [
                "",
                f"- loop {case['loop_no']} market `{case['market']}`",
                f"  - action: `{decision['action']}`",
                f"  - score: `{decision['committee_score']}`",
                f"  - scalping_candidate: `{decision['scalping_shadow']['candidate']}`",
                f"  - live_ready: `{decision['live_start_readiness']['ready']}`",
                f"  - ready_for_buy_test_endpoint: `{case['ready_for_buy_test_endpoint']}`",
            ]
        )
    lines.extend(
        [
            "",
            "## Safety",
            "",
            "- actual live buy: `not submitted`",
            "- actual live sell: `not submitted`",
            "- cancel: `not submitted`",
            "- market order: `blocked by design`",
        ]
    )
    report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "passed": True,
                "report_json": str(report_json),
                "loop_count": report["loop_count"],
                "ready_for_buy_test_count": report["ready_for_buy_test_count"],
                "live_order_count": report["live_order_count"],
            },
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
