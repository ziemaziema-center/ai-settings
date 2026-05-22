# V2 Runtime Architecture Review - 2026-05-11

## Current Verified State

- SAFE LIMITED LIVE EXECUTION V1 completed.
- Controlled stop verification PASS.
- `open_order_exists=false`.
- `duplicate_order_exists=false`.
- Workflows inactive.
- Cron disabled.
- Live fuse disabled.
- V2 safety gate document completed.
- Automation remains disabled.

This review is documentation-only. It does not authorize workflow patching, helper patching, restart, Docker changes, live API calls, orders, cancels, reorders, activation, cron enablement, or Telegram runtime sends.

## 1. V2 Runtime Architecture Goals

V2 should make the system safer before it becomes more capable.

Primary goals:
- STOP > EXECUTE.
- Fail-safe over fail-forward.
- Separate observation, reconciliation, approval, and execution.
- Prevent autonomous retry loops.
- Prevent automatic cancel/reprice.
- Prevent any second live order without reconciliation.
- Preserve helper signing isolation.
- Make every state transition auditable.
- Keep live execution disabled unless every safety gate passes and a human explicitly approves one bounded attempt.

The V2 runtime should be designed as a controlled state machine, not a trading bot.

## 2. Lessons Learned From V1 Live Execution

V1 proved that a limited live path can work, but it also showed why execution cannot imply completion.

Lessons:
- Accepted order telemetry is only an acceptance event.
- Open-order monitoring is mandatory after any live attempt.
- `wait` and `stale_wait` must not trigger automatic action.
- Manual cancellation must be reconciled as an external human action, not as an automation feature.
- The one-time live fuse prevented retries and should remain core to V2.
- Inactive/manual workflows reduced unintended execution risk.
- Summary-only helper telemetry limits reconciliation quality.
- Offline regression fixtures are useful before any runtime patch.
- Documentation and audit artifacts are necessary for continuity across sessions.

## 3. Proposed Order State Machine

Proposed V2 states:

```text
idle_safe
-> precheck_read_only
-> approval_required
-> fuse_armed_once
-> live_attempt_submitted
-> reconciliation_required
-> wait_stop
-> partial_fill_stop
-> done_final
-> cancel_final
-> unknown_stop
```

State rules:
- `idle_safe`: no open order, automation disabled.
- `precheck_read_only`: helper and telemetry checks only.
- `approval_required`: human approval required before fuse arm.
- `fuse_armed_once`: one bounded live attempt allowed.
- `live_attempt_submitted`: immediate transition to reconciliation; no retry.
- `reconciliation_required`: read-only lifecycle classification.
- `wait_stop`: open order still waiting; STOP.
- `partial_fill_stop`: partial exposure; STOP.
- `done_final`: order fully filled; no automatic next order.
- `cancel_final`: order canceled; no automatic replacement.
- `unknown_stop`: missing, inconsistent, or unsupported state; STOP.

No state may transition directly from unresolved exposure to a new live order.

## 4. Execution Lock System Design

V2 should use layered locks:

- open-order lock: blocks if any target-market open order exists.
- duplicate tuple lock: blocks same `market|side|ord_type` while recent intent exists.
- live fuse lock: permits exactly one approved attempt.
- workflow activation lock: blocks execution if workflow state is unexpected.
- recovery lock: blocks after restart until state is reconstructed.
- logging lock: blocks if persistent audit logging is unavailable.

Lock behavior:
- Missing lock state means locked.
- Uncertain lock state means locked.
- Static-only locks are not enough for production automation.
- Durable lock reconstruction must use exchange state and append-only execution history.

## 5. Live Fuse Lifecycle Design

Fuse lifecycle:

```text
disabled
-> human_approved_once
-> armed_once
-> consumed_before_live_call
-> disabled_consumed
```

Fuse requirements:
- disabled by default;
- armed only by explicit human approval;
- scoped to one market, one side, one order type, one value bound, one attempt;
- consumed before helper live-order call;
- auto-disabled after attempt;
- never reset by workflow logic;
- never reset while any order state is unresolved.

If execution fails after fuse consumption, the fuse stays consumed. V2 must fail safe, not retry.

## 6. stale_wait Escalation Flow

`stale_wait` is an observation signal, not an action trigger.

Flow:

```text
wait detected
-> monitor read-only
-> stale_wait report flag
-> operator review
-> controlled cancel design required if action is desired
-> no automatic cancel or reprice
```

Rules:
- no automatic cancel;
- no automatic reorder;
- no second order;
- no price adjustment;
- no retry loop;
- alerting may notify only.

## 7. Reconciliation Cadence Strategy

Recommended cadence:
- manual read-only reconciliation after any live attempt;
- short-interval manual checks while open order exists;
- final reconciliation after `open_order_exists=false`;
- no autonomous execution after final reconciliation;
- no cron-driven reconciliation until recovery/logging/alerting are validated.

Future read-only cadence may be scheduled only after:
- restart behavior is validated;
- persistent logs are durable;
- helper detail telemetry is safe;
- alerts are read-only;
- no execution path is reachable from the cadence.

## 8. Persistent Order Journal Concept

V2 should use an append-only order journal as the runtime memory source.

Required journal events:
- precheck started;
- precheck blocked;
- approval granted;
- fuse armed;
- fuse consumed;
- live attempt submitted;
- live attempt accepted/rejected;
- reconciliation state observed;
- stale wait observed;
- partial fill observed;
- done observed;
- cancel observed;
- unknown stop observed;
- recovery event;
- operator action.

Journal rules:
- append-only;
- sanitized fields only;
- masked UUID in general reports;
- no JWT, Authorization header, API secret, raw balances, or raw order payload;
- logging failure forces STOP.

## 9. Operator Approval UX Flow

Operator approval should be explicit and bounded:

1. Review precheck report.
2. Review reconciliation state.
3. Review duplicate/open-order lock state.
4. Review live fuse status.
5. Confirm order shape and value bound.
6. Approve one attempt only.
7. Record approval in persistent journal.
8. Arm fuse.
9. Submit one attempt.
10. Return immediately to reconciliation-required STOP state.

Approval UI must not include:
- retry button;
- cancel button;
- rebuy button;
- activate workflow button;
- enable cron button.

## 10. Telegram Alert Policy Boundaries

Telegram is visibility only.

Allowed:
- helper failure alert;
- open order still waiting alert;
- stale wait alert;
- partial fill alert;
- done alert;
- cancel alert;
- unknown STOP alert;
- logging failure alert;
- recovery ambiguity alert.

Forbidden:
- approve trade button;
- execute trade button;
- cancel order button;
- retry order button;
- rebuy button;
- activate workflow button;
- enable cron button.

If Telegram fails, log the failure and STOP. Do not retry indefinitely.

## 11. Helper Detail Endpoint Boundaries

Future helper detail telemetry must be additive and read-only.

Allowed endpoint concept:
- `POST /upbit/open-orders/detail-telemetry`

Allowed fields:
- state;
- remaining_volume;
- executed_volume;
- trades_count;
- created_at;
- paid_fee;
- locked;
- masked UUID.

Forbidden changes:
- JWT/signing logic changes;
- auth header creation changes;
- API key loading changes;
- live-order behavior changes;
- order-test behavior changes;
- cancel/reorder/withdrawal behavior;
- raw payload returns.

Existing endpoints must remain unchanged.

## 12. Emergency Freeze Path

Emergency freeze must override all other states.

Freeze triggers:
- open order exists unexpectedly;
- duplicate state uncertain;
- helper unavailable;
- telemetry missing;
- reconciliation unknown;
- logging failure;
- restart ambiguity;
- workflow active unexpectedly;
- cron enabled unexpectedly;
- live fuse uncertain;
- secret exposure risk;
- forbidden endpoint usage detected.

Freeze behavior:
- disable live eligibility;
- block fuse reset;
- block workflow activation;
- block cron;
- block order/cancel/reorder;
- emit sanitized report;
- require human review.

## 13. Failure Containment Philosophy

V2 must contain failures at the smallest possible boundary.

Principles:
- STOP > EXECUTE.
- Fail-safe over fail-forward.
- No autonomous retry loops.
- No automatic cancel/reprice.
- No second live order without reconciliation.
- Missing telemetry is not a pass.
- Missing logs are not a pass.
- Unknown state is not a pass.
- Manual action is not automation precedent.

Every failure should become a blocked state with evidence, not a fallback execution path.

## 14. Required Telemetry Structure

Base telemetry fields:
- timestamp_kst;
- run_id;
- workflow_name;
- phase;
- market;
- side;
- ord_type;
- action;
- result;
- blocked_reason;
- open_order_exists;
- open_order_count;
- order_state;
- remaining_volume;
- executed_volume;
- duplicate_key;
- duplicate_state;
- fuse_state;
- emergency_stop;
- helper_health;
- api_status;
- workflow_active;
- cron_enabled;
- forbidden_endpoint_check;
- secrets_leak_check;
- next_safe_action.

Forbidden telemetry:
- JWT;
- Authorization header;
- API secret;
- raw balances;
- raw order payload;
- full account identifiers;
- full UUID in general reports.

## 15. Runtime Validation Sequence

Future V2 validation sequence:

1. Read safety docs and current artifact inventory.
2. Run WF05 offline regression fixtures.
3. Validate helper health.
4. Validate auth telemetry read-only.
5. Validate open-order telemetry read-only.
6. Validate detailed reconciliation read-only if endpoint exists.
7. Validate duplicate lock state.
8. Validate live fuse disabled.
9. Validate workflows inactive.
10. Validate cron disabled.
11. Validate emergency stop clear.
12. Validate persistent journal write.
13. Validate forbidden endpoint scan.
14. Validate secret leak scan.
15. Create validation report.
16. Require explicit human approval before any next phase.

No validation step may place, cancel, reorder, activate, enable cron, restart, or send Telegram runtime commands.

## 16. Conditions Required Before V2 Live Execution Can Even Be Discussed

V2 live execution may be discussed only when all of the following are true:

- `open_order_exists=false`;
- `duplicate_order_exists=false`;
- previous order state reconciled as `done` or `cancel`;
- no stale wait, partial fill, or unknown state remains;
- helper health is PASS;
- auth telemetry is PASS;
- open-order telemetry is PASS;
- workflow identities are confirmed;
- WF03/WF04/WF05 are inactive;
- cron is disabled;
- live fuse is disabled/consumed until reapproved;
- WF05 offline regression passes;
- persistent order journal is ready;
- rollback path is ready;
- helper detail endpoint, if implemented, passed diff review and read-only validation;
- Telegram, if used, is read-only and has no execution buttons;
- emergency stop conditions are clear;
- human approval is explicit, scoped, and one-time.

Discussion is not approval. Approval must be a separate safety-gated step.

NO V2 LIVE EXECUTION MAY PROCEED WITHOUT COMPLETE SAFETY VALIDATION AND EXPLICIT HUMAN APPROVAL.
