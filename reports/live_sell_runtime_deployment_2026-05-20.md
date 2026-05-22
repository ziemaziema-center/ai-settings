# Live Sell Runtime Deployment - 2026-05-20

## Result

- Runtime scope: `upbit-helper` only.
- Deployment result: `PASS`.
- Remote backup: `/home/ubuntu/kbia_backups/upbit-helper-live-sell-20260520_123919`.
- Rollback image: `upbit-helper:rollback-live-sell-20260520_123919`.
- Helper health: `PASS`.

## Endpoints Added

- `POST /upbit/sell-test/telemetry`
- `POST /upbit/live-sell/telemetry`

## Remote Smoke Validation

- health_ok: `true`
- market_order_blocked: `true`
- bid_sell_test_blocked: `true`
- sell_test_success: `true`
- live_sell_blocked_without_flags: `true`
- live_sell_attempted during smoke: `false`
- open_order_count_btc: `0`
- open_order_count_etc: `0`
- open_order_exists_btc: `false`
- open_order_exists_etc: `false`

## Cleanup Candidate Decision

- portfolio_plan_valid: `true`
- news_bias: `DEFENSIVE_REFERENCE`
- first candidate: `KRW-ETC`
- first action: `EXIT_STAGED`
- first shadow slice: `99,816 KRW`
- single live cap: `30,000 KRW`
- sequence: `ETC -> DOT -> FCT2 -> ALGO -> DOGE`

## Scheduler Contract

- Coordinator read loop may run only as read/decision.
- Order loop remains disabled.
- Scheduler activation was not performed.
- Any accepted order must stop further order attempts immediately.
- Next order may only happen after finality check confirms `done` or `cancel` and global open order count returns to `0`.

## Safety

- live order submitted: `false`
- live sell submitted: `false`
- cancel submitted: `false`
- retry loop started: `false`
- workflow activated: `false`
- project scheduler mutated: `false`
- secret/JWT/Auth header/raw payload/full UUID exposed: `false`
