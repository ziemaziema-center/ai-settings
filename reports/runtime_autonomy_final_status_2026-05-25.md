# Runtime Autonomy Final Status - 2026-05-25

## Scope

Runtime status check after GitHub Actions recovery.

No live order, cancel, workflow activation, scheduler change, credential readout, or secret logging was performed during this check.

## Remote Runtime

- host: `ubuntu@43.201.227.194`
- helper container: `upbit-helper`, image `upbit-helper:cancel-stale-20260525`, status `Up`
- helper health: `ok=true`, `service=upbit-helper`
- active runner: `python3 runners/kbia_parallel_smart_coordinator_20260524.py --loop --sleep 180`
- runner state path: `/home/ubuntu/kbia-logs/parallel-smart-automation/state.json`
- runner event path: `/home/ubuntu/kbia-logs/parallel-smart-automation/events.jsonl`

## Current Trading Safety State

- execution lock: `unlocked`
- lock exists: `false`
- stale lock: `false`
- partial lock files: `[]`
- active market: `null`
- live order count across watched markets: `0`

Watched market open order counts:

| Market | Open order count |
| --- | ---: |
| KRW-BTC | 0 |
| KRW-ETH | 0 |
| KRW-SOL | 0 |
| KRW-ETC | 0 |
| KRW-DOT | 0 |
| KRW-FCT2 | 0 |
| KRW-ALGO | 0 |
| KRW-DOGE | 0 |
| KRW-RVN | 0 |

## Cleanup Progress

- `KRW-DOT`: completed; current sell test reports insufficient balance.
- `KRW-ETC`: completed; latest finality classification `done`, remaining volume `0`.
- `KRW-FCT2`: still held, but live sell test is blocked by stale or wide orderbook conditions.
- `KRW-ALGO`: still held, but live sell test is blocked by wide or stale orderbook conditions.
- `KRW-DOGE`: still held, but live sell test is blocked by wide spread conditions.

## Current Blocker

The system is not stopped because of a crash. It is waiting because no candidate passed the helper sell gate.

Recent blocker pattern:

- `KRW-FCT2`: `LIVE_SELL_ORDERBOOK_STALE|LIVE_SELL_SPREAD_TOO_WIDE`
- `KRW-ALGO`: `LIVE_SELL_ORDERBOOK_STALE|LIVE_SELL_SPREAD_TOO_WIDE`
- `KRW-DOGE`: `LIVE_SELL_SPREAD_TOO_WIDE`
- `KRW-DOT`: `LIVE_SELL_ASSET_BALANCE_NOT_SUFFICIENT`
- `KRW-ETC`: `LIVE_SELL_ASSET_BALANCE_NOT_SUFFICIENT`

## Safety Result

The automation is running and self-monitoring.

It is allowed to:

- scan candidates in parallel,
- place at most one helper-gated live limit order after all gates pass,
- remain idle when spread, orderbook freshness, balance, lock, or finality gates fail.

It is still forbidden to:

- force market orders,
- bypass spread or orderbook gates,
- place simultaneous live orders,
- guarantee profit or recovery,
- expose secrets or raw order payloads.

## Final Classification

`RUNNING_SAFE_IDLE`

Meaning:

- infrastructure is alive,
- open order count is zero,
- lock is clear,
- no stuck order remains,
- current no-trade state is a safety decision, not an execution failure.
