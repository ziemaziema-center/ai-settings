# DOT Live Sell Once - 2026-05-20

## HQ Resolution

- HQ/agents called: `true`
- DOT blocker classification: legitimate safety block plus telemetry gap
- Patch scope: orderbook diagnostics and clock-skew detection
- Stale threshold changed: `false`
- Helper deployment: `PASS`
- Workflow/scheduler changed: `false`

## Execution

- market: `KRW-DOT`
- side: `ask`
- ord_type: `limit`
- market order used: `false`
- max KRW: `30,000`
- submitted estimate: `28,999.99999176 KRW`
- price: `1,843`
- volume: `15.73521432`

## Precheck

- helper health: `ok`
- open order before DOT: `0`
- KRW band: `30000+`
- DOT present: `true`
- best_bid: `1,840`
- best_ask: `1,843`
- price above best_bid: `true`

## Sell-Test

- sell-test passed: `true`
- orderbook_age_ms: `6538`
- maker-limit gate: `true`

## Live Sell

- DOT live sell submitted: `true`
- DOT live sell accepted: `true`
- http_status: `201`
- orderbook_age_ms: `6722`
- live sell count: `1`

## Post-Order State

- finality classification: `wait`
- open_order_count: `1`
- open_order_exists: `true`
- executed_volume: `0`
- remaining_volume: `15.73521432`
- trades_count: `0`
- uuid_masked: `f089...0a09`
- next_safe_action: `remain_stopped`
- later candidate review allowed: `false`

## Safety

- cancel submitted: `false`
- retry/reorder loop: `false`
- workflow activated: `false`
- scheduler mutated: `false`
- secret/JWT/Auth/raw payload/full UUID exposed: `false`

## Decision

The one allowed DOT live sell was accepted but remains open in `wait`.
The system must stay stopped until this order becomes `done` or `cancel` and open order count returns to `0`.
