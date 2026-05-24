# Portfolio Execution Update - 2026-05-24

## Read-Only Snapshot

- automation runner before action: `RUNNING`
- cycle_count before action: `353`
- open orders before action: `0`
- available KRW: about `72,244`
- marked portfolio value from helper snapshot: about `2.35M KRW`
- adjusted with manually checked live KRW tickers for SOL/ALGO/FCT2: about `3.55M-3.58M KRW`

## Sell-Test Probe

| Market | Result | Reason |
| --- | --- | --- |
| `KRW-ETC` | PASS | fresh orderbook, maker-limit ok |
| `KRW-DOT` | PASS | fresh enough orderbook, maker-limit ok |
| `KRW-FCT2` | BLOCKED | spread too wide |
| `KRW-ALGO` | BLOCKED | spread too wide |
| `KRW-DOGE` | BLOCKED | spread too wide |

## Executed Action

- Paused `kbia-full-auto` before manual staged cleanup.
- Submitted one `KRW-ETC` staged limit ask slice through helper gates.
- No market order was used.
- No cancel was submitted.
- No DOT order was submitted because one-order-at-a-time rule stopped the sequence after ETC remained open.

Order shape:

- market: `KRW-ETC`
- side: `ask`
- ord_type: `limit`
- price: `13420`
- volume: `2.16095380`
- estimated KRW: about `29,000`

## Updated Finality

- `KRW-ETC` finality later reached `done`.
- ETC executed_volume: `2.1609538`.
- ETC remaining_volume: `0`.
- ETC open_order_count after finality: `0`.
- ETC execution lock was released through the validated recovery path.
- The parallel smart coordinator later submitted one `KRW-DOT` staged limit ask after gates passed.
- DOT finality reached `done`.
- DOT executed_volume: `15.11991657`.
- DOT remaining_volume: `0`.
- Current tracked open order count: `0`.
- Current execution lock state: `unlocked`.

## Current Decision

- Continue the bounded `kbia-full-auto` parallel smart coordinator.
- Parallel scan is allowed.
- Live orders remain limited to one helper-gated limit order until finality.
- No automatic cancel, market order, simultaneous live order, or gate bypass is allowed.
- Buy branch remains available only through the bounded live-buy helper gate; it is not an unlimited auto-buy branch.

## Notes

- FCT2/ALGO/DOGE are still opportunity-cost cleanup candidates, but current spread gates block live execution.
- BTC/ETH/SOL remain core recovery holdings for now.
- The 10M KRW target still requires high return from a reduced capital base; no guaranteed-profit claim is valid.
