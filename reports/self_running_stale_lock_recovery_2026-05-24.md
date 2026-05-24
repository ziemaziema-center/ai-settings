# Self-Running Stale Lock Recovery - 2026-05-24

## Result

Implemented and deployed a safe self-running stale execution lock recovery path.

## Why

The automation was running, but a stale helper lock could require manual release. That made the system stop even when finality could be proven safely.

## Change

- Added helper endpoint:
  - `POST /execution-lock/recover-stale-finality`
- Added coordinator behavior:
  - check helper lock state every cycle,
  - if stale, ask helper to recover only after finality proof,
  - if the locked market still has an open order, keep monitoring that market,
  - auto-correct stale `active_market` when a different market has the open order.

## Current Runtime Observation

- `kbia-full-auto` is running.
- `upbit-helper` is healthy.
- Current active market is `KRW-ETC`.
- `KRW-ETC` has open_order_count `1`.
- ETC finality is `wait`.
- The stale lock recovery endpoint correctly refused recovery because `OPEN_ORDER_EXISTS`.

## Safety

- No market order.
- No cancel.
- No simultaneous live order.
- No owner token exposure.
- No raw Upbit payload exposure.
- No recovery unless `open_order_count=0` and finality is `done` or `cancel`.

## Validation

- Local py_compile passed.
- Local helper recovery tests passed.
- Local coordinator tests passed.
- Local live-sell helper regression passed.
- Local secret scan passed.
- Remote py_compile passed.
- Remote helper recovery tests passed.
- Remote coordinator tests passed.
- Remote secret scan passed.

## Elementary Version

이제 시스템은 이런 식으로 혼자 처리한다:

1. 주문이 걸려 있으면 새 주문을 안 낸다.
2. 어떤 코인 주문이 걸려 있는지 스스로 맞춘다.
3. 주문이 끝났는지 계속 본다.
4. 주문이 끝났고 미체결이 0이면 오래된 lock을 혼자 푼다.
5. 아직 주문이 남아 있으면 lock을 안 풀고 기다린다.
