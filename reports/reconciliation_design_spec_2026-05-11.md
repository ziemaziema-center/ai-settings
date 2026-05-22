# Reconciliation Design Specification - 2026-05-11

## 1. Purpose

Execution is not reconciliation.

Execution is the act of submitting an order after explicit safety gates pass. Reconciliation is the later, read-only process that determines what happened to that order and what state the system must remain in.

Reconciliation must be designed as a classification and evidence layer first. It must never assume that a successful order acceptance means the order is filled, final, safe to repeat, or safe to cancel. Acceptance only means the exchange received the order.

The current system state is `still_waiting_safe_stop`:
- One live order exists.
- `open_order_exists=true`
- `state=wait`
- `remaining_volume=0.0001`
- `executed_volume=0`
- `stale_wait=true`
- WF03/WF04 are inactive.
- The live fuse is consumed/disabled.

## 2. Required Order States

### wait
Meaning:
- The order is accepted by the exchange but not fully filled.
- `remaining_volume` is nonzero.
- `executed_volume` may be zero or greater than zero depending on exchange representation.

Safe handling:
- STOP.
- Do not place another order.
- Do not cancel automatically.
- Continue read-only monitoring.
- Preserve evidence in sanitized logs.

### partial_fill
Meaning:
- The order is not final.
- `executed_volume` is greater than zero and `remaining_volume` is greater than zero.
- The exchange may still report `state=wait` or similar non-final state.

Safe handling:
- STOP.
- Do not place another order.
- Do not cancel automatically.
- Classify as partial exposure.
- Require human-reviewed reconciliation before any further action.

### done
Meaning:
- The order is fully filled.
- Expected evidence: `state=done`, `remaining_volume=0`, and `executed_volume>0`.

Safe handling:
- Mark order as filled only after all required evidence is present.
- Archive sanitized finality evidence.
- Do not trigger a new order automatically.
- Any follow-up workflow must remain gated by a separate future production-ready design.

### cancel
Meaning:
- The exchange reports the order as canceled.
- There may or may not be partial execution before cancellation.

Safe handling:
- STOP.
- Archive sanitized cancellation evidence.
- Reconcile executed and remaining volumes before any future decision.
- Do not place a replacement order automatically.

### unknown_stop
Meaning:
- State is missing, inconsistent, unsupported, unavailable, or contradictory.
- Telemetry fetch failed or returned malformed data.
- Required fields are missing.

Safe handling:
- STOP.
- Escalate to human review through future read-only alerting only.
- Do not place, cancel, reorder, retry execution, or activate any workflow.

## 3. Required Fields

Reconciliation telemetry should capture the following fields, with sanitization rules:

- `uuid`: required for correlation; log only masked form unless a future secure internal store is approved.
- `market`: required, for example `KRW-BTC`.
- `side`: required, expected `bid` or `ask`.
- `ord_type`: required, current safe rule allows only `limit`.
- `state`: required exchange lifecycle state.
- `created_at`: required exchange timestamp.
- `remaining_volume`: required numeric string or decimal.
- `executed_volume`: required numeric string or decimal.
- `trades_count`: required if available; otherwise mark missing and STOP until handling is designed.
- `paid_fee`: required for final reconciliation when safely available.
- `locked`: required for open-order/exposure accounting when safely available.
- `price`: required for limit order validation.
- `avg_buy_price`: optional future field, only if safely available later and sanitized.

No raw balances, raw order payloads, Authorization headers, JWTs, API secrets, or full account details may be logged.

## 4. Safe Reconciliation Rules

- Reconciliation never places orders.
- Reconciliation never cancels automatically.
- Reconciliation is read-only classification first.
- Unknown states force STOP.
- Inconsistent state forces STOP.
- Missing telemetry forces STOP.
- Missing required fields force STOP.
- Any non-final order state forces STOP.
- Any partial fill forces STOP until human-reviewed handling exists.
- A completed fill must not trigger a new order automatically.
- A canceled order must not trigger a replacement order automatically.
- Stale wait is a report-only signal until a controlled human-reviewed cancel flow exists.
- Reconciliation output must be sanitized and append-only.

## 5. State Transition Model

Safe model:

```text
accepted
-> wait
-> partial_fill
-> done

accepted
-> wait
-> cancel

accepted
-> unknown_stop
```

Notes:
- `accepted` is not a final state.
- `wait` is not a permission to retry.
- `partial_fill` is not a permission to complete the order with a new order.
- `done` is finality evidence only, not an automation trigger.
- `cancel` is finality evidence only, not a replacement trigger.
- `unknown_stop` must halt all execution paths.

## 6. Required Future Safety Checks

Future reconciliation implementation must include:

- Restart recovery: recover the last known order state safely after n8n/helper/container restarts.
- Duplicate persistence: persist order correlation and duplicate-lock evidence outside volatile workflow state.
- Stale wait timeout handling: classify stale waits without automatic cancel or reorder.
- Partial fill handling: represent partial exposure, fees, remaining volume, and locked funds without action.
- Exchange inconsistency handling: STOP on contradictory exchange fields.
- Reconciliation retry policy: read-only only, bounded, rate-limit aware, and never connected to execution retries.
- Safe archival logging: append-only, sanitized, durable logs with masked identifiers.

## 7. Explicitly Forbidden Future Behavior

Do not build:

- Auto rebuy.
- Auto martingale.
- Auto revenge trade.
- Recursive retry.
- Hidden loops.
- Cancel-replace loops.
- Execution during unknown state.
- Execution after stale wait without human-reviewed cancel lifecycle.
- Execution after partial fill without human-reviewed exposure reconciliation.
- Any alert button that places, retries, cancels, or replaces an order.

## 8. Safe Implementation Order

1. reconciliation read-only
2. reconciliation logging
3. reconciliation alerts
4. restart-safe persistence
5. controlled human-reviewed cancel flow
6. only then limited automation

## Final Constraint

Until this design is implemented and validated, the system remains in:

CONTROLLED STOP STATE
