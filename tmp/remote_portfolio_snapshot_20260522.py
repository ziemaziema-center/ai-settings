from __future__ import annotations

import json
from decimal import Decimal
from urllib import request

from app.main import _decimal_or_none, _upbit_get


def valid_krw_markets() -> set[str]:
    with request.urlopen("https://api.upbit.com/v1/market/all?is_details=false", timeout=15) as response:
        rows = json.loads(response.read().decode("utf-8"))
    return {str(row.get("market")) for row in rows if isinstance(row, dict) and str(row.get("market", "")).startswith("KRW-")}


def public_tickers(markets: list[str]) -> dict[str, Decimal]:
    prices: dict[str, Decimal] = {}
    valid_markets = sorted(set(markets) & valid_krw_markets())
    for offset in range(0, len(valid_markets), 30):
        batch = valid_markets[offset : offset + 30]
        if not batch:
            continue
        url = "https://api.upbit.com/v1/ticker?markets=" + ",".join(batch)
        with request.urlopen(url, timeout=15) as response:
            rows = json.loads(response.read().decode("utf-8"))
        for row in rows:
            if isinstance(row, dict) and row.get("market"):
                price = _decimal_or_none(row.get("trade_price"))
                if price is not None:
                    prices[str(row["market"])] = price
    return prices


accounts_result = _upbit_get("/v1/accounts")
accounts = accounts_result.get("body") if isinstance(accounts_result.get("body"), list) else []
asset_markets = []
for row in accounts:
    currency = str(row.get("currency", ""))
    balance = _decimal_or_none(row.get("balance")) or Decimal("0")
    locked = _decimal_or_none(row.get("locked")) or Decimal("0")
    if currency and currency != "KRW" and balance + locked > 0:
        asset_markets.append(f"KRW-{currency}")

prices = public_tickers(asset_markets)
holdings = []
total_value = Decimal("0")
total_buy = Decimal("0")
for row in accounts:
    currency = str(row.get("currency", ""))
    balance = _decimal_or_none(row.get("balance")) or Decimal("0")
    locked = _decimal_or_none(row.get("locked")) or Decimal("0")
    amount = balance + locked
    avg_buy_price = _decimal_or_none(row.get("avg_buy_price")) or Decimal("0")
    if currency == "KRW":
        value = amount
        market = "KRW"
        current_price = Decimal("1")
        buy_amount = amount
    else:
        market = f"KRW-{currency}"
        current_price = prices.get(market, Decimal("0"))
        value = amount * current_price
        buy_amount = amount * avg_buy_price
    if amount <= 0 and value <= 0:
        continue
    total_value += value
    total_buy += buy_amount
    pnl = value - buy_amount if currency != "KRW" else Decimal("0")
    pnl_pct = (pnl / buy_amount * Decimal("100")) if buy_amount > 0 and currency != "KRW" else Decimal("0")
    holdings.append(
        {
            "currency": currency,
            "market": market,
            "balance": float(balance),
            "locked": float(locked),
            "avg_buy_price": float(avg_buy_price),
            "current_price": float(current_price),
            "value_krw": int(value),
            "buy_amount_krw": int(buy_amount),
            "pnl_krw": int(pnl),
            "pnl_pct": round(float(pnl_pct), 2),
        }
    )

holdings.sort(key=lambda row: row["value_krw"], reverse=True)
asset_buy = sum(Decimal(str(row["buy_amount_krw"])) for row in holdings if row["currency"] != "KRW")
asset_value = sum(Decimal(str(row["value_krw"])) for row in holdings if row["currency"] != "KRW")
print(
    json.dumps(
        {
            "success": accounts_result.get("status") == 200,
            "holding_count": len(holdings),
            "total_value_krw": int(total_value),
            "asset_value_krw": int(asset_value),
            "krw_available": next((row["value_krw"] for row in holdings if row["currency"] == "KRW"), 0),
            "asset_buy_amount_krw": int(asset_buy),
            "asset_pnl_krw": int(asset_value - asset_buy),
            "asset_pnl_pct": round(float((asset_value - asset_buy) / asset_buy * Decimal("100")), 2) if asset_buy > 0 else 0.0,
            "holdings": holdings,
        },
        ensure_ascii=True,
        separators=(",", ":"),
    )
)
