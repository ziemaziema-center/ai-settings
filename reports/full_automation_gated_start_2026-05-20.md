# Gated Full Automation Start - 2026-05-20

## GitHub

- Pushed repo: `ziemaziema-center/ai-settings`
- Branch: `main`
- Commit: `448a60b`
- Message: `docs: update ops telemetry`
- Note: the main trading project folder is not a Git repository, so only `ai-settings` could be pushed.

## Automation

- Remote session: `kbia-full-auto`
- Status: `running`
- Runner: `/tmp/kbia_full_automation_coordinator_20260520.py`
- Interval: `1800 seconds`
- State: `/home/ubuntu/kbia-logs/full-automation/state.json`
- Events: `/home/ubuntu/kbia-logs/full-automation/events.jsonl`

## Contract

- One order at a time.
- If any open order exists, read-only monitoring only.
- Sell branch requires helper sell-test pass, maker-limit pass, balance pass, orderbook freshness, spread gate, fingerprint, and one-time live-sell gate.
- Buy branch remains blocked until Brain v4 emits a valid `BUY_CANDIDATE`.
- Market orders, automatic cancel, retry/reorder loops, and scheduler/n8n mutation remain forbidden.

## Current State

- ETC: `done`, open order `0`
- DOT: `done`, open order `0`
- BTC/ETC/DOT/FCT2/ALGO/DOGE open orders: all `0`

## First Automation Cycles

- FCT2: blocked by `LIVE_SELL_ORDERBOOK_STALE|LIVE_SELL_SPREAD_TOO_WIDE`
- ALGO: blocked by `LIVE_SELL_SPREAD_TOO_WIDE`
- DOGE: blocked by `LIVE_SELL_SPREAD_TOO_WIDE`

No new order was submitted by the coordinator start cycles.

## Safety

- new live order submitted: `false`
- new live sell submitted after start: `false`
- cancel submitted: `false`
- n8n/workflow mutated: `false`
- secret/JWT/Auth/raw payload/full UUID exposed: `false`
