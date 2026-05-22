# Live Buy Helper Shadow Freeze Manifest - 2026-05-22

## Scope

- Implemented bounded `buy-test` and `live-buy` helper gates.
- Deployed helper code to EC2 bounded workspace.
- Rebuilt and restarted only the `upbit-helper` container.
- Ran aggressive scalping buy shadow loop 3 times.
- No live buy order was submitted.
- No live sell order was submitted by this task.
- No cancel request was submitted.
- No market order is allowed by the new buy gate.

## Files

- `upbit-helper/app/main.py`
- `tests/test_helper_live_buy_endpoints.py`
- `tmp/run_aggressive_scalping_buy_shadow_20260522.py`
- `tmp/remote_smoke_buy_helper_20260522.py`
- `reports/aggressive_scalping_buy_shadow_2026-05-22.json`
- `reports/aggressive_scalping_buy_shadow_2026-05-22.md`

## New Helper Gates

- `/upbit/buy-test/telemetry`
- `/upbit/live-buy/telemetry`

Both endpoints require:

- allowed market only: `KRW-BTC`, `KRW-ETH`, `KRW-SOL`
- `side=bid`
- `ord_type=limit`
- KRW value between `5000` and `10000`
- no open order
- valid Brain v4 schema
- `BUY_CANDIDATE`
- Brain live-ready
- candidate score at least `78`
- non-defensive news
- scalping candidate
- fresh orderbook
- spread not wider than `12 bps`
- maker-limit price that does not cross best ask

`/upbit/live-buy/telemetry` additionally requires:

- `live_buy_enabled=true`
- `execution_allowed=true`
- `execution_mode=live`
- `all_pass=true`
- duplicate lock clear
- system stop false
- prior buy-test passed
- matching buy-test fingerprint
- one-time live buy fuse true

## Validation

- `python tests/test_helper_live_buy_endpoints.py` passed locally and remotely.
- `python tests/test_helper_live_sell_endpoints.py` passed locally.
- `python tests/test_helper_detail_no_journal.py` passed twice locally.
- `python tests/test_kbia_news_brain.py` passed twice locally.
- `python tests/test_kbia_portfolio_liquidation_brain.py` passed twice locally.
- `python tests/test_kbia_strategy_kernel.py` passed twice locally.
- `python tests/test_kbia_trade_learning.py` passed twice locally.
- `python tests/wf05_offline_regression_runner_2026-05-11.py` passed twice locally.
- `python tmp/v2_execution_lock_offline_validation_20260511.py` passed twice locally.
- `python -m py_compile ...` passed locally and remotely.
- Remote helper smoke passed with blocked payloads only.

## Shadow Run Evidence

- aggressive scalping loop count: `3`
- ready_for_buy_test_count: `0`
- live_order_count: `0`
- reason: current news/Brain gates did not produce a live-ready buy candidate.

## Remote Runtime Evidence

- helper health: `ok`
- container: `upbit-helper` running on `127.0.0.1:8010`
- automation mode: `gated_full_automation`
- completed cleanup markets: `KRW-DOT`, `KRW-ETC`
- active_market: `null`
- open_order_count by tracked market: `0`
- remaining blocked cleanup markets:
  - `KRW-FCT2`: `LIVE_SELL_ORDERBOOK_STALE|LIVE_SELL_SPREAD_TOO_WIDE`
  - `KRW-ALGO`: `LIVE_SELL_SPREAD_TOO_WIDE`
  - `KRW-DOGE`: `LIVE_SELL_SPREAD_TOO_WIDE`

## Freeze

- live buy endpoint exists but is gated.
- buy branch remains blocked until Brain produces a live-ready candidate and all helper gates pass.
- live_order_count verified as `0`.
