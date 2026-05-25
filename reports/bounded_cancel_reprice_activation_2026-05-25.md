# Bounded Cancel/Reprice Activation - 2026-05-25

## Result

Activated bounded cancel/reprice for stale unfilled cleanup sell orders.

## Runtime Result

- Existing `KRW-ETC` order was stale and unfilled.
- Cancel gate accepted exactly one cancel.
- ETC finality after cancel: `cancel`.
- Open order count after cancel: `0`.
- Stale lock recovery released the old lock.
- Coordinator immediately rescanned candidates.
- ETC sell-test passed.
- New `KRW-ETC` live limit ask was accepted.
- Current ETC state after reprice: `wait`.
- Current ETC open_order_count: `1`.
- Current helper lock state: `active`.

## Safety Contract

- No market order.
- No cancel loop.
- No simultaneous live order.
- No raw UUID exposure.
- No secret exposure.
- No cancel after partial fill.
- No cancel before minimum open age.
- No reprice without full helper sell-test/live-sell gates.

## Files

- `upbit-helper/app/main.py`
- `runners/kbia_parallel_smart_coordinator_20260524.py`
- `tests/test_helper_cancel_stale_order.py`
- `tests/test_parallel_smart_coordinator.py`

## Validation

- Local py_compile passed.
- Local cancel helper tests passed.
- Local coordinator tests passed.
- Local live sell/buy helper regression passed.
- Local secret scan passed.
- Remote py_compile passed.
- Remote cancel helper tests passed.
- Remote coordinator tests passed.
- Remote secret scan passed.

## Elementary Version

돈이 주문 하나에 너무 오래 묶이면:

1. 시스템이 그 주문이 오래 안 팔렸는지 본다.
2. 하나만 걸려 있고, 하나도 체결 안 됐고, 안전 조건이 맞으면 취소한다.
3. 취소가 끝났는지 확인한다.
4. 다시 좋은 가격 조건을 확인한다.
5. 조건이 맞으면 새 지정가 주문을 낸다.

지금 이 과정이 ETC에서 실제로 한 번 작동했다.
