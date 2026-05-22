# ETC Live Sell Once - 2026-05-20

## Execution

- market: `KRW-ETC`
- side: `ask`
- ord_type: `limit`
- market order used: `false`
- max KRW: `30,000`
- submitted estimate: `28,999.999899 KRW`
- price: `13,260`
- volume: `2.18702865`

## Precheck

- helper health: `ok`
- best_bid: `13,240`
- best_ask: `13,260`
- price above best_bid: `true`
- sell-test passed: `true`
- sell-test open_order_count: `0`
- asset balance sufficient: `true`
- maker-limit gate: `true`

## Live Sell

- live sell submitted: `true`
- live sell accepted: `true`
- http_status: `201`
- live sell count: `1`

## Post-Order State

- finality classification: `wait`
- open_order_count: `1`
- open_order_exists: `true`
- executed_volume: `0`
- remaining_volume: `2.18702865`
- trades_count: `0`
- uuid_masked: `91b1...a624`
- next_safe_action: `remain_stopped`
- DOT review allowed: `false`

## Safety

- cancel submitted: `false`
- retry/reorder loop: `false`
- workflow activated: `false`
- scheduler mutated: `false`
- secret/JWT/Auth header/raw payload/full UUID exposed: `false`

## Decision

The one allowed ETC live sell was accepted but remains open in `wait`.
The system must stay stopped until this order becomes `done` or `cancel` and open order count returns to `0`.
