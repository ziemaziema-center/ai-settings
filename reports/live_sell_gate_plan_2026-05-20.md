# Live Sell Gate Plan - 2026-05-20

- timestamp_kst: `2026-05-20T12:37:35+09:00`
- portfolio_plan_valid: `True`
- news_bias: `DEFENSIVE_REFERENCE`
- primary_candidate: `KRW-ETC` / `EXIT_STAGED` / cap `30000` KRW
- live_sell_scheduler_allowed: `False`
- order_endpoint_allowed: `False`
- market_sell_allowed: `False`
- cancel_endpoint_allowed: `False`

## Cleanup Sequence

| rank | market | action | first shadow slice | single live cap | quality | liquidity | auto candidate |
|---:|---|---|---:|---:|---|---|---|
| 1 | KRW-ETC | EXIT_STAGED | 99816 | 30000 | GOOD | LIQUID | True |
| 2 | KRW-DOT | EXIT_STAGED | 34029 | 30000 | GOOD | LOW_LIQUIDITY | True |
| 3 | KRW-FCT2 | EXIT_STAGED | 55588 | 30000 | CAUTION | WIDE_SPREAD | False |
| 4 | KRW-ALGO | EXIT_STAGED | 21493 | 21493 | CAUTION | WIDE_SPREAD | False |
| 5 | KRW-DOGE | REDUCE_STAGED | 61996 | 30000 | CAUTION | WIDE_SPREAD | False |

## Scheduler Contract

- Coordinator may read health/news/account/open-order/orderbook/brain state repeatedly.
- It may submit at most one live sell only after all helper gates pass.
- After any accepted order, scheduler must stop order attempts and run read-only finality checks only.
- `wait`, `watch`, partial, unknown, rate-limit, auth failure, or helper error keeps the system stopped.
