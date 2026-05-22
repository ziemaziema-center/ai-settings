# DOT Live Sell Attempt Blocked - 2026-05-20

## Result

- Requested flow: 10 tasks.
- Completed: 1-7.
- Blocked at: DOT sell-test.
- Reason: `LIVE_SELL_ORDERBOOK_STALE`.
- DOT live-sell submitted: `false`.
- Final DOT open order count: `0`.

## Completed

1. ETC finality recorded: `done`
2. KRW account band checked: `30000+`
3. open order precheck: `0`
4. DOT candidate rechecked
5. DOT orderbook checked
6. DOT sell quantity calculated
7. DOT sell-test executed

## DOT Plan That Was Tested

- market: `KRW-DOT`
- side: `ask`
- ord_type: `limit`
- best_bid: `1,842`
- best_ask: `1,846`
- price above best_bid: `true`
- estimated KRW: `28,999.99999962`
- max KRW: `30,000`

## Blocked

8. DOT live-sell: blocked
9. DOT post-order stop: not needed, no order submitted
10. later candidates: blocked until DOT test can pass or DOT is skipped by a new decision gate

## Safety

- new live order submitted: `false`
- DOT live sell submitted: `false`
- cancel submitted: `false`
- retry/reorder loop: `false`
- workflow activated: `false`
- scheduler mutated: `false`
- secret/JWT/Auth/raw payload/full UUID exposed: `false`
