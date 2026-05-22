# Next Safe Work Package While Open Order Waits - 2026-05-11

## 1. Current Blocked Runtime State

- `open_order_exists=true`
- `market=KRW-BTC`
- `state=wait`
- `stale_wait=true`
- User manually confirmed an active limit buy reservation/order exists.
- WF03/WF04/WF05 remain inactive.
- Live fuse is consumed/disabled.
- No automation is enabled.
- System posture is CONTROLLED STOP STATE.

## 2. Why No Runtime Work Is Allowed

No runtime work is allowed because an unresolved open order creates exposure and duplicate-risk ambiguity.

While `open_order_exists=true`:
- a second order could duplicate exposure;
- cancellation is not approved or designed;
- reorder/cancel-replace behavior is forbidden;
- restart recovery is not runtime-tested;
- helper detail telemetry is deferred;
- Telegram runtime alerts are not validated;
- persistent state durability is not production-ready.

The only safe runtime-facing work is read-only monitoring/reconciliation. Any implementation that could affect execution, helper behavior, workflow activation, cron, restart, or Telegram runtime messaging must remain blocked.

## 3. Safe Work That Can Continue While The Order Waits

Allowed safe work:
- Read-only open-order monitoring.
- WF05 read-only reconciliation checks.
- Offline WF05 regression runner execution.
- Documentation updates.
- Registry updates for known failures and validated patterns.
- Artifact indexing and session handoff documentation.
- Design-only planning for reconciliation, recovery, logging, Telegram read-only alerts, and helper backup/rollback.
- Mocked/offline tests that do not call helper, Upbit, n8n, Docker, Telegram, or workflow runtime.

Not allowed during wait:
- Any live order.
- Any cancel.
- Any reorder.
- Any workflow activation.
- Any cron.
- Any restart.
- Any helper patch.
- Any workflow patch unless separately approved as read-only and safety-gated.

## 4. Required Checks After `open_order_exists` Becomes False

After `open_order_exists=false`, do not immediately resume execution. First complete:

1. Confirm helper `/health` is PASS.
2. Confirm read-only open-order telemetry returns `open_order_exists=false`.
3. Confirm order lifecycle final state is classified safely: `done`, `cancel`, or `unknown_stop`.
4. Confirm no partial fill ambiguity remains.
5. Confirm duplicate lock and live fuse state are understood.
6. Confirm workflows remain inactive.
7. Confirm no cron/schedule is enabled.
8. Confirm persistent logging path is ready.
9. Run WF05 offline regression runner and require 12/12 PASS.
10. Create a post-resolution read-only reconciliation report.

If any field is missing, inconsistent, or unknown, remain stopped.

## 5. Conditions Before Any Workflow Reactivation

Workflow reactivation is not allowed until all of the following are true:

- `open_order_exists=false`.
- Reconciliation state is final and understood.
- Restart recovery plan has been validated or explicitly deferred by human decision.
- Persistent logging path exists and can record audit events.
- Telegram read-only alerts are validated without execution buttons, if alerts are in scope.
- Duplicate protection is durable or safely reconstructable.
- Live fuse state is clear and intentionally configured.
- Pre-implementation safety gate passes.
- Exact workflow identity is confirmed.
- Human approval explicitly names the workflow and activation scope.

No cron or schedule may be enabled until limited automation is separately designed and approved.

## 6. Conditions Before Any Future Live Execution

Future live execution requires all of the following:

- No open order exists.
- Previous order lifecycle is fully reconciled.
- No stale/partial/unknown order state remains.
- WF03 precheck passes with read-only helper telemetry.
- WF04 execution path remains manual and explicitly gated.
- Live fuse is intentionally set for a single approved attempt only.
- Duplicate lock is clear and durable enough for the approved scope.
- Order shape is limit-only and bounded.
- Persistent logging is available.
- Forbidden endpoint scan passes.
- Secret leak scan passes.
- Human approval explicitly states market, side, order type, value bounds, and one-time scope.

Any failure or ambiguity means STOP.

## 7. Human Approval Gates

Human approval is required before:

- Any workflow patch.
- Any helper patch.
- Any Docker/runtime change.
- Any restart.
- Any workflow activation.
- Any cron/schedule.
- Any Telegram live send.
- Any cancel lifecycle work.
- Any live execution.
- Any live fuse reset.
- Any use of full order UUID outside approved secure context.

Approval must define:
- exact scope;
- exact files/workflows affected;
- forbidden actions;
- rollback path;
- validation output expected.

## 8. Explicit Forbidden Actions

Do not:

- place a second order;
- cancel the current order;
- reorder or cancel-replace;
- enable cron;
- activate workflows;
- add retries;
- add hidden loops;
- patch helper runtime;
- patch execution logic;
- restart containers/services;
- send Telegram runtime messages;
- add Telegram trade/cancel/retry/activate buttons;
- expose JWT, Authorization headers, API secrets, raw balances, raw order payloads, or full UUIDs.

## 9. Recommended Next Codex Prompt After Order Resolves

```text
Read-only post-resolution reconciliation only.
Check KRW-BTC open order status and classify final lifecycle state.
Do not place orders.
Do not cancel.
Do not reorder.
Do not activate workflows.
Do not enable cron.
Do not restart services.
Do not send Telegram runtime messages.
Run WF05 offline regression first if any WF05 logic is referenced.
Report safe telemetry only and create an additive post-resolution reconciliation report.
```

SYSTEM REMAINS IN CONTROLLED STOP STATE UNTIL OPEN ORDER RESOLVES.
