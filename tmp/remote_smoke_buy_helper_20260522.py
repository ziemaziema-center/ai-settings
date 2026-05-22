from __future__ import annotations

import json
import urllib.request


def post(path: str, payload: dict[str, object]) -> dict[str, object]:
    req = urllib.request.Request(
        f"http://127.0.0.1:8010{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    return json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8"))


blocked_test = post(
    "/upbit/buy-test/telemetry",
    {
        "market": "KRW-DOGE",
        "side": "bid",
        "ord_type": "market",
        "price": "1",
        "volume": "1",
        "estimated_krw_value": "1",
        "open_order_exists": False,
    },
)
blocked_live = post(
    "/upbit/live-buy/telemetry",
    {
        "market": "KRW-BTC",
        "side": "bid",
        "ord_type": "limit",
        "price": "100000000",
        "volume": "0.0001",
        "estimated_krw_value": "10000",
        "open_order_exists": False,
        "brain_schema_version": "kbia.strategy_brain.v4.1",
        "brain_action": "BUY_CANDIDATE",
        "brain_live_ready": True,
        "brain_candidate_score": "82",
        "news_bias": "BALANCED_REFERENCE",
        "scalping_candidate": True,
    },
)

assert blocked_test["live_buy_attempted"] is False
assert "LIVE_BUY_MARKET_NOT_ALLOWED" in blocked_test["error_name"]
assert "LIVE_BUY_LIMIT_ONLY" in blocked_test["error_name"]
assert blocked_live["live_buy_attempted"] is False
assert blocked_live["error_name"] == "LIVE_BUY_NOT_ENABLED"

print(
    json.dumps(
        {
            "passed": True,
            "buy_test_error": blocked_test["error_name"],
            "live_buy_error": blocked_live["error_name"],
            "live_buy_attempted": blocked_live["live_buy_attempted"],
        },
        separators=(",", ":"),
    )
)
