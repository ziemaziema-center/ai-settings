# V2 Implementation Readiness Checklist - 2026-05-11

## Current Verified State

- SAFE LIMITED LIVE EXECUTION V1 completed.
- Controlled stop verification PASS.
- `open_order_exists=false`.
- `duplicate_order_exists=false`.
- Workflows inactive.
- Cron disabled.
- Live fuse disabled.
- V2 safety gate completed.
- V2 runtime architecture review completed.
- Automation remains disabled.

This checklist is documentation-only. It does not approve implementation, workflow modification, helper modification, restart, Docker changes, live API calls, orders, cancels, reorders, activation, cron enablement, or Telegram runtime sends.

## 1. Runtime Components That May Need Future Modification

Potential future components:

- [ ] WF03 PreCheck engine: read-only gate hardening and persistent logging integration only.
- [ ] WF04 Execution engine: live fuse and execution lock hardening only after V2 gate passes.
- [ ] WF05 Reconciliation read-only: lifecycle detail parsing, reporting, and offline test alignment.
- [ ] `upbit-helper`: additive read-only detail telemetry endpoint only.
- [ ] Persistent order journal: append-only local JSONL or later durable database.
- [ ] Telegram read-only alert renderer: visibility-only notifications, no execution buttons.
- [ ] Recovery validation artifacts: restart-safe state reconstruction design.

Not yet modifiable:

- [ ] Execution/live-order path.
- [ ] Cancel/reorder path.
- [ ] Cron/schedule activation.
- [ ] Helper JWT/signing/auth logic.
- [ ] Docker/runtime/service configuration.

## 2. Workflow Candidates And Why They Must Remain Inactive For Now

### WF03 PreCheck

- Candidate for future read-only gate hardening.
- Must remain inactive because precheck can influence execution eligibility.
- No activation until persistent logging, duplicate state, reconciliation, and safety gate validation pass.

### WF04 Execution

- Candidate for future fuse and execution lock hardening.
- Must remain inactive because it contains the live execution path.
- No changes to live order behavior until explicit safety-gated approval exists.

### WF05 Reconciliation_ReadOnly

- Candidate for future read-only reconciliation detail support.
- Must remain inactive/manual-only/read-only.
- No execution, cancel, reorder, Telegram send, cron, or activation behavior may be added.

## 3. Helper Endpoint Needs And Boundaries

Potential future need:

- [ ] Add one read-only detail telemetry endpoint for order lifecycle fields.

Allowed endpoint concept:

- [ ] `POST /upbit/open-orders/detail-telemetry`

Allowed fields:

- [ ] state
- [ ] remaining_volume
- [ ] executed_volume
- [ ] trades_count
- [ ] created_at
- [ ] paid_fee
- [ ] locked
- [ ] masked UUID only

Forbidden changes:

- [ ] JWT generation changes.
- [ ] Signing logic changes.
- [ ] Authorization header construction changes.
- [ ] API key loading changes.
- [ ] Live-order endpoint behavior changes.
- [ ] Order-test endpoint behavior changes.
- [ ] Cancel/reorder/withdrawal behavior.
- [ ] Raw balances or raw order payload returns.

## 4. Order State Machine Storage Decision Checklist

Before implementation, decide:

- [ ] Where order state is stored.
- [ ] Whether local JSONL is sufficient for V2.
- [ ] Whether SQLite/Postgres is deferred.
- [ ] How order correlation is stored without exposing full UUID in reports.
- [ ] How `wait`, `partial_fill`, `done`, `cancel`, and `unknown_stop` are represented.
- [ ] How stale wait is recorded without action.
- [ ] How manual cancel is recorded as external operator action.
- [ ] How missing/corrupt telemetry forces STOP.
- [ ] How restart recovery reconstructs state from the journal.

Hard requirement:

- [ ] Missing state must not default to clear.

## 5. Execution Lock Design Checklist

Required locks:

- [ ] Open-order lock.
- [ ] Duplicate tuple lock.
- [ ] Live fuse lock.
- [ ] Workflow activation lock.
- [ ] Recovery lock.
- [ ] Persistent logging lock.
- [ ] Emergency stop lock.

Lock rules:

- [ ] Missing lock means locked.
- [ ] Uncertain lock means locked.
- [ ] Open order means locked.
- [ ] Duplicate ambiguity means locked.
- [ ] Logging failure means locked.
- [ ] Restart ambiguity means locked.

## 6. Live Fuse Reset Checklist

Before live fuse reset can even be proposed:

- [ ] `open_order_exists=false`.
- [ ] `duplicate_order_exists=false`.
- [ ] Previous order reconciled as `done` or `cancel`.
- [ ] WF03 inactive.
- [ ] WF04 inactive.
- [ ] WF05 inactive/manual/read-only.
- [ ] Cron disabled.
- [ ] Emergency stop clear.
- [ ] Persistent order journal available.
- [ ] Backup/rollback path ready.
- [ ] Human approval explicitly scopes one attempt.

Fuse reset must remain:

- [ ] one-time;
- [ ] bounded;
- [ ] expiring if unused;
- [ ] consumed before live helper call;
- [ ] auto-disabled afterward.

## 7. Telegram Approval Gate Checklist

Telegram can support visibility, not execution.

Allowed:

- [ ] Render read-only alert templates.
- [ ] Log alert payloads.
- [ ] Send private bot visibility alerts only after approval.

Forbidden:

- [ ] Approve Trade button.
- [ ] Execute Trade button.
- [ ] Cancel Order button.
- [ ] Retry Order button.
- [ ] Rebuy button.
- [ ] Activate Workflow button.
- [ ] Enable Cron button.

Before Telegram runtime send:

- [ ] Message template reviewed.
- [ ] No execution buttons present.
- [ ] Token/secret handling verified.
- [ ] Failure behavior logs and stops.
- [ ] Human approval granted for send test.

## 8. Reconciliation Checklist

Before any next runtime work:

- [ ] `open_order_exists=false`.
- [ ] Duplicate order does not exist.
- [ ] Prior order final state is `done` or `cancel`.
- [ ] No `wait`, `partial_fill`, or `unknown_stop`.
- [ ] Required fields available or missing fields force STOP.
- [ ] Full UUID not logged in general reports.
- [ ] WF05 offline regression passes.
- [ ] Reconciliation output is append-only.
- [ ] Reconciliation cannot place, cancel, reorder, retry, activate, enable cron, or send Telegram commands.

## 9. Offline Regression Test Expansion Checklist

Existing WF05 offline regression must remain required.

Future expansion cases:

- [ ] `cancel` with partial execution.
- [ ] `done` with fee/locked fields present.
- [ ] `wait` with stale wait metadata.
- [ ] duplicate candidate detected.
- [ ] missing created_at.
- [ ] malformed trades_count.
- [ ] helper detail endpoint unavailable.
- [ ] journal write failure.
- [ ] restart recovery ambiguous.
- [ ] rate-limit telemetry.
- [ ] secret leak fixture scan.
- [ ] forbidden endpoint fixture scan.

Rule:

- [ ] If any offline fixture fails, STOP before runtime patch.

## 10. Rollback Checklist

Before any patch prompt:

- [ ] Backup path defined.
- [ ] Backup created before changes.
- [ ] Files changed listed.
- [ ] Restore method documented.
- [ ] Validation after restore documented.
- [ ] Syntax/static validation documented.
- [ ] Endpoint inventory comparison planned.
- [ ] Workflow inactive check planned.
- [ ] No restart required unless separately approved.

Rollback philosophy:

- [ ] Rollback uncertainty means STOP.

## 11. Human Approval Checklist

Human approval must state:

- [ ] Exact objective.
- [ ] Exact allowed files.
- [ ] Exact forbidden actions.
- [ ] Patch class.
- [ ] Backup path.
- [ ] Rollback path.
- [ ] Validation commands/checks.
- [ ] Runtime impact.
- [ ] Whether live API is forbidden or read-only allowed.
- [ ] Whether restart is forbidden.
- [ ] Whether Telegram send is forbidden.
- [ ] Expiration or one-time boundary.

Approval for documentation does not approve runtime work.

## 12. Absolute Blockers Before Implementation

Implementation is blocked if any are true:

- [ ] Open order exists.
- [ ] Duplicate state uncertain.
- [ ] Workflow active state uncertain.
- [ ] Cron state uncertain.
- [ ] Live fuse state uncertain.
- [ ] Helper health unavailable.
- [ ] Auth telemetry failing.
- [ ] Reconciliation unknown.
- [ ] Persistent logging unavailable.
- [ ] Rollback path missing.
- [ ] Secret exposure risk.
- [ ] Patch touches auth/signing without explicit approval.
- [ ] Patch touches live-order behavior without explicit approval.
- [ ] Patch could cancel, reorder, retry, activate, enable cron, or send Telegram command.
- [ ] User approval is ambiguous.

## 13. Minimum Conditions Before Any Patch Prompt May Be Written

Before writing any future implementation prompt:

- [ ] Read `SESSION_BOOT.md`.
- [ ] Read current `KNOWN_FAILURES`.
- [ ] Read current `VALIDATED_PATTERNS`.
- [ ] Read `V2_safety_gate_design_2026-05-11.md`.
- [ ] Read `V2_runtime_architecture_review_2026-05-11.md`.
- [ ] Confirm current open-order state.
- [ ] Confirm workflows inactive.
- [ ] Confirm cron disabled.
- [ ] Confirm live fuse disabled.
- [ ] Define patch class.
- [ ] Define exact files in scope.
- [ ] Define exact files out of scope.
- [ ] Define validation plan.
- [ ] Define rollback plan.
- [ ] Define final output format.

If any condition is missing, write a plan only.

## 14. Minimum Conditions Before Any V2 Live Execution May Be Discussed

Before V2 live execution can be discussed:

- [ ] `open_order_exists=false`.
- [ ] `duplicate_order_exists=false`.
- [ ] Previous order reconciled as `done` or `cancel`.
- [ ] No stale wait, partial fill, or unknown state remains.
- [ ] WF03/WF04/WF05 inactive.
- [ ] Cron disabled.
- [ ] Live fuse disabled until reapproved.
- [ ] WF05 offline regression passes.
- [ ] Persistent order journal ready.
- [ ] Helper health and auth telemetry pass.
- [ ] Open-order telemetry pass.
- [ ] Emergency stop clear.
- [ ] Rollback path ready.
- [ ] Human approval explicitly scopes a one-time discussion or attempt.

Discussion is not approval. A separate approval gate is required for any implementation or live action.

IMPLEMENTATION IS NOT APPROVED BY THIS DOCUMENT; THIS DOCUMENT ONLY DEFINES READINESS REQUIREMENTS.
