# ETC Live Sell Follow-Up - 2026-05-20

## Result

- Requested flow: 10 steps.
- Completed: steps 1-4 only.
- Blocked at: ETC order still `wait`.
- Next safe action: `remain_stopped`.

## Current ETC State

- market: `KRW-ETC`
- classification: `wait`
- open_order_count: `1`
- open_order_exists: `true`
- price: `13,260`
- executed_volume: `0`
- remaining_volume: `2.18702865`
- trades_count: `0`
- DOT review allowed: `false`

## Why It Stopped

DOT and later candidates require:

- ETC finality is `done` or `cancel`
- global open order count is `0`

Current state fails both requirements.

## Safety

- new live order submitted: `false`
- new live sell submitted: `false`
- cancel submitted: `false`
- retry/reorder loop: `false`
- workflow activated: `false`
- scheduler mutated: `false`
- secret/JWT/Auth/raw payload/full UUID exposed: `false`
