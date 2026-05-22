# V2 Safety Gate Design - 2026-05-11

## Current Verified State

- `open_order_exists=false`
- `duplicate_order_exists=false`
- WF03 inactive
- WF04 inactive
- WF05 inactive/manual-only/read-only
- live fuse disabled
- cron disabled
- SAFE LIMITED LIVE EXECUTION V1 completed
- SYSTEM REMAINS IN CONTROLLED STOP STATE

This document is design-only. It does not authorize workflow patching, helper patching, restart, Docker changes, live API calls, orders, cancels, reorders, activation, cron enablement, or Telegram runtime sends.

## 1. Purpose Of V2 Safety Gate

The V2 safety gate exists to prevent any future live execution from occurring until the system proves that observation, reconciliation, logging, recovery, and human approval controls are all working.

V2 must convert the V1 lessons into explicit preconditions:
- no unresolved order exposure;
- no duplicate ambiguity;
- no stale wait ambiguity;
- no hidden activation path;
- no runtime action without persistent audit evidence;
- no execution without explicit human approval.

The gate is a STOP-first control, not a profit filter.

## 2. Lessons Learned From V1

- A successful order submission is not finality.
- Accepted execution and reconciled lifecycle state are separate.
- Open order state must block every second-order path.
- Stale wait must remain report-only.
- A one-time live fuse is effective only if consumed before the live helper call and left disabled afterward.
- Inactive/manual workflows reduce accidental execution risk.
- Read-only monitoring and reconciliation must exist before any next execution.
- Helper summary telemetry is useful but insufficient for production-grade reconciliation.
- Documentation and offline regression fixtures reduce ambiguity before runtime work.
- Manual cancel must be treated as an external human action, never as automation behavior to emulate.

## 3. stale_wait Handling Policy

`stale_wait=true` means:
- report-only visibility;
- no automatic cancel;
- no reorder;
- no second order;
- no retry loop;
- no escalation to execution.

Required handling:
- classify stale wait as STOP;
- write sanitized log/report;
- require human review;
- continue read-only monitoring/reconciliation only.

Future controlled cancel lifecycle must be designed separately before any stale-wait action is allowed.

## 4. max_live_orders Policy

V2 maximum live open orders:
- `max_live_orders=1` for the entire system unless a future portfolio design explicitly changes this.
- For the same market/side/order type tuple, maximum allowed pending exposure is zero before new execution.

Execution is blocked if:
- any open order exists for target market;
- open-order telemetry is missing;
- open-order telemetry is inconsistent;
- duplicate state is uncertain;
- reconciliation state is not final.

No second order is allowed while any order is `wait`, `partial_fill`, `unknown_stop`, or otherwise unresolved.

## 5. Duplicate-Order Hard Block

Duplicate-order checks must run before live execution eligibility.

Hard block conditions:
- duplicate lock active;
- duplicate lock missing or uncertain;
- more than one recent matching order candidate;
- open order exists;
- prior order lifecycle not reconciled;
- staticData reset or duplicate persistence ambiguity.

The duplicate block must fail closed. Missing duplicate evidence is not permission to execute.

## 6. Live Fuse Reset Rules

Live fuse reset is forbidden by default.

A future fuse reset requires:
- `open_order_exists=false`;
- duplicate state clear;
- previous order lifecycle reconciled;
- persistent audit log written;
- WF03/WF04 inactive;
- no cron/schedule active;
- explicit human approval naming market, side, order type, value bound, and one-time scope;
- backup and rollback path verified;
- pre-live dry-run and read-only validation report complete.

Fuse reset must:
- be one-time;
- expire if unused;
- be consumed before any live helper call;
- auto-disable after the attempt;
- never be reset by workflow logic.

## 7. Required Manual Approval Gates

Manual approval is required for:
- helper patch;
- workflow patch;
- workflow activation;
- cron enablement;
- live fuse reset;
- live execution;
- cancel lifecycle work;
- Telegram runtime send;
- restart/recovery validation;
- any use of full identifiers in a secure context.

Approval must include:
- exact scope;
- exact files/workflows affected;
- forbidden actions;
- validation plan;
- rollback path;
- expected output artifacts;
- expiration or one-time boundary.

## 8. Read-Only Reconciliation Requirements

Before future execution, reconciliation must prove:
- `open_order_exists=false`;
- prior order final state is `done` or `cancel`;
- no `wait`, `partial_fill`, or `unknown_stop` remains;
- duplicate order does not exist;
- no new order was created unexpectedly;
- required fields are present and sanitized;
- missing/inconsistent telemetry forces STOP.

Required fields:
- market;
- state;
- remaining_volume;
- executed_volume;
- created_at;
- trades_count if available;
- paid_fee if available;
- locked if available;
- masked UUID only if needed.

Reconciliation must never place, cancel, reorder, or retry.

## 9. Workflow Activation Requirements

Workflow activation is forbidden until:
- V2 safety gate passes;
- open-order state is clear;
- persistent logging is available;
- recovery behavior is validated or explicitly blocked from automation scope;
- exact workflow identity is confirmed;
- workflow has no cron unless separately approved;
- workflow has no hidden execution loop;
- forbidden endpoint scan passes;
- secret leak scan passes;
- rollback path is ready;
- human approval explicitly authorizes activation.

Activation approval for one workflow does not authorize any other workflow.

## 10. Cron Activation Requirements

Cron activation is forbidden by default.

Before any cron discussion:
- read-only reconciliation must be stable;
- recovery after restart must be validated;
- persistent audit logging must be durable;
- Telegram read-only alerts must be safe if used;
- duplicate protection must be durable;
- emergency stop must be verified;
- no open order can exist;
- no live execution can be reachable from cron unless a later limited automation design explicitly permits it.

Cron must never be enabled as part of a live execution test.

## 11. Emergency Stop Conditions

Emergency STOP is required if any of these are true:
- open order exists;
- duplicate state uncertain;
- helper unavailable;
- auth telemetry fails;
- open-order telemetry missing;
- reconciliation state unknown;
- stale wait detected;
- partial fill detected;
- logging fails;
- workflow active state unexpected;
- cron/schedule unexpected;
- live fuse uncertain;
- restart ambiguity;
- rate limit or temporary ban signal;
- secret exposure risk;
- any forbidden endpoint usage detected.

STOP means no order, no cancel, no reorder, no retry, no activation, and no cron.

## 12. Forbidden Automation Behaviors

Do not build:
- auto rebuy;
- auto martingale;
- auto revenge trade;
- recursive retry;
- hidden loops;
- cancel-replace loops;
- automatic cancel;
- automatic second order;
- execution during unknown state;
- execution after stale wait;
- startup auto-resume;
- cron-triggered live execution without a future approved automation design;
- Telegram buttons for trade, cancel, retry, activate, or cron.

## 13. Required Telemetry/Logging

Every future safety-gated action must emit sanitized telemetry:
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
- fuse_state;
- emergency_stop;
- helper_health;
- api_status;
- forbidden_endpoint_check;
- secrets_leak_check.

Forbidden log data:
- JWT;
- Authorization header;
- API secret;
- raw balances;
- raw order payload;
- full account identifiers;
- full UUID in general reports.

If persistent logging fails, STOP.

## 14. Safe Rollback Philosophy

Rollback must be prepared before runtime work.

Rollback policy:
- backup first;
- patch small;
- isolate helper and workflow changes;
- validate syntax before runtime checks;
- verify endpoint inventory after restore;
- verify workflows remain inactive after restore;
- do not restart unless separately approved;
- treat rollback uncertainty as STOP.

Rollback is not a license to take higher risk. It is a requirement for controlled recovery.

## 15. Exact Conditions Before Any Future Live Execution Is Allowed

Future live execution is allowed only if all conditions are true:

1. `open_order_exists=false`.
2. `duplicate_order_exists=false`.
3. Previous order lifecycle is fully reconciled as `done` or `cancel`.
4. No stale wait, partial fill, unknown state, or telemetry ambiguity remains.
5. WF03/WF04 are inactive before manual validation.
6. WF05 read-only reconciliation passes.
7. WF05 offline regression runner passes.
8. Helper health passes.
9. Auth telemetry passes.
10. Open-order telemetry passes.
11. Duplicate lock is clear and durable enough for scope.
12. Live fuse is disabled until explicit one-time approval.
13. Persistent logging path is available.
14. Forbidden endpoint scan passes.
15. Secret leak scan passes.
16. No cron/schedule is active for the execution path.
17. Emergency stop is clear.
18. Backup/rollback path is ready.
19. Human approval explicitly authorizes one market, one side, one limit order, one bounded value, one attempt.
20. The live fuse is consumed before the live helper call and auto-disabled afterward.

If any condition fails, the result is STOP.

NO FUTURE LIVE EXECUTION IS ALLOWED WITHOUT EXPLICIT SAFETY-GATED HUMAN APPROVAL.
