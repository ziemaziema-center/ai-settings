# V2 Execution Lock System Design Scope

Date: 2026-05-11  
Mode: Documentation-only, additive-only  
Runtime status: Controlled STOP state  

## Current Verified State

- SAFE LIMITED LIVE EXECUTION V1 completed.
- Clean shutdown verification PASS.
- Helper detail endpoint deployed.
- Helper health PASS.
- `open_order_exists=false`.
- `open_order_count=0`.
- Workflows inactive.
- Cron disabled.
- Live fuse disabled.
- Automation disabled.
- Helper detail endpoint is read-only reconciliation only.

This document does not authorize workflow patching, helper patching, restart, Docker changes, live API order/cancel/reorder calls, workflow activation, cron enablement, Telegram runtime sends, or live fuse reset.

## 1. Purpose Of Execution Lock

The V2 execution lock exists to prevent more than one live execution intent from being active, ambiguous, or repeatable at the same time.

The lock is a safety control, not a trading feature. It must force STOP whenever execution state is unclear.

Primary purpose:

- prevent duplicate live attempts;
- prevent concurrent workflow execution;
- prevent second live execution before reconciliation;
- preserve one-attempt-only behavior;
- preserve auditability across restarts;
- make live eligibility impossible unless lock, fuse, reconciliation, journal, and human approval all agree.

## 2. Risk It Prevents

The execution lock prevents:

- duplicate order exposure;
- race conditions between workflow runs;
- a second order after a partially observed first order;
- retry loops after helper/network/exchange ambiguity;
- live execution after restart with incomplete state;
- live execution while an order is open, partial, waiting, stale, or unknown;
- live execution when persistent logging is unavailable;
- live execution when workflow state or lock state is inconsistent.

## 3. Lock Authority Source

Lock authority must be layered.

Required authority sources:

- exchange read-only open-order telemetry;
- helper detail endpoint reconciliation;
- append-only order journal;
- append-only lock journal;
- active lock file;
- workflow inactive state;
- live fuse state;
- explicit human approval record.

No single source is enough.

Non-authoritative sources:

- n8n workflow staticData alone;
- workflow memory alone;
- previous chat/session memory alone;
- operator assumption without telemetry;
- helper response without journal evidence;
- stale lock auto-expiry alone.

If any authority source is missing, inconsistent, or unclear, the result is STOP.

## 4. Proposed Lock Storage Location

Proposed storage root:

```text
/home/ubuntu/kbia-logs/upbit-helper
```

Proposed active lock file:

```text
/home/ubuntu/kbia-logs/upbit-helper/execution-locks/active_execution_lock.json
```

Proposed append-only lock journal:

```text
/home/ubuntu/kbia-logs/upbit-helper/execution-lock-journal/execution_lock_YYYY-MM-DD.jsonl
```

Design rationale:

- local to the runtime host;
- compatible with the deployed helper journal pattern;
- persistent outside ephemeral container state;
- readable by helper-side validation;
- append-only audit trail can reconstruct lock state after restart.

The exact path must be reviewed and explicitly approved before implementation. This document only proposes the location.

## 5. Lock Schema

Active lock schema:

```json
{
  "schema_version": "v2.execution_lock.1",
  "lock_id": "operator-generated-or-system-generated-safe-id",
  "created_at_kst": "2026-05-11T00:00:00+09:00",
  "updated_at_kst": "2026-05-11T00:00:00+09:00",
  "created_by": "human_approved_runtime",
  "market": "KRW-BTC",
  "side": "bid",
  "ord_type": "limit",
  "lock_state": "active",
  "lock_reason": "LIVE_EXECUTION_APPROVAL_PENDING_OR_IN_PROGRESS",
  "run_id": "safe-run-id",
  "approval_id": "safe-approval-id",
  "fuse_id": "safe-fuse-id",
  "journal_ref": "masked-or-relative-journal-reference",
  "open_order_exists_at_acquire": false,
  "open_order_count_at_acquire": 0,
  "reconciliation_classification_at_acquire": "cancel",
  "workflow_active_at_acquire": false,
  "cron_enabled_at_acquire": false,
  "expires_at_kst": "2026-05-11T00:10:00+09:00",
  "release_required_by_human": true,
  "forbidden_endpoint_check": true,
  "secrets_leak_check": true
}
```

Append-only lock journal event schema:

```json
{
  "timestamp_kst": "2026-05-11T00:00:00+09:00",
  "event_type": "lock_acquire_attempt",
  "result": "blocked_or_acquired_or_released",
  "lock_id": "safe-lock-id",
  "market": "KRW-BTC",
  "side": "bid",
  "ord_type": "limit",
  "run_id": "safe-run-id",
  "approval_id": "safe-approval-id",
  "fuse_state": "disabled_or_armed_once_or_consumed",
  "open_order_exists": false,
  "open_order_count": 0,
  "reconciliation_classification": "cancel",
  "blocked_reason": null,
  "next_safe_action": "remain_stopped",
  "forbidden_endpoint_check": true,
  "secrets_leak_check": true
}
```

Forbidden lock fields:

- JWT;
- Authorization header;
- API secret;
- raw balances;
- raw order payload;
- full UUID;
- full account identifiers;
- execution payload.

## 6. Lock Acquisition Rules

Lock acquisition may only be attempted after every precondition passes.

Required preconditions:

- explicit human approval exists;
- workflows remain inactive before validation;
- cron remains disabled;
- live fuse is disabled until separately armed;
- helper health PASS;
- helper detail endpoint PASS;
- `open_order_exists=false`;
- `open_order_count=0`;
- duplicate order not detected;
- previous order reconciled as final state `done` or `cancel`;
- order journal is writable;
- lock journal is writable;
- no active execution lock exists;
- no stale execution lock exists;
- no unknown lock state exists;
- forbidden endpoint scan PASS;
- secrets leak scan PASS.

Acquisition outcome rules:

- if lock status is unclear -> STOP;
- if lock exists -> STOP;
- if stale lock exists -> STOP + human review;
- if journal write fails -> STOP;
- if reconciliation is `wait`, `partial_fill`, or `unknown_stop` -> STOP;
- if workflow active state is unexpected -> STOP;
- if cron is enabled unexpectedly -> STOP.

## 7. Lock Release Rules

Lock release must be explicit and evidence-backed.

Allowed release conditions:

- live attempt was never made and human cancels the approved attempt;
- live attempt was submitted and reconciliation reached final `done`;
- live attempt was submitted and reconciliation reached final `cancel`;
- operator performs manual review and records a release decision;
- rollback restores pre-lock state and records release reason.

Release requirements:

- append release event to lock journal;
- preserve historical lock events;
- remove or mark active lock only after journal write succeeds;
- record release reason;
- record reconciliation state at release;
- record fuse state at release;
- keep automation disabled after release.

Release must not imply permission for another execution.

## 8. Lock Expiry / Stale Lock Policy

Expiry is a warning, not an unlock.

Policy:

- lock may include `expires_at_kst`;
- expired lock becomes `stale_lock`;
- stale lock forces STOP;
- stale lock requires human review;
- stale lock must not auto-unlock;
- stale lock must not auto-retry;
- stale lock must not arm or reset live fuse;
- stale lock must not trigger cancel/reorder/reprice.

Stale lock resolution requires:

- read-only reconciliation;
- order journal review;
- lock journal review;
- workflow inactive check;
- cron disabled check;
- human approval for manual unlock documentation;
- append-only release or supersede event.

## 9. Duplicate Execution Prevention

Duplicate execution prevention uses multiple gates:

- active lock file;
- lock journal reconstruction;
- order journal reconstruction;
- exchange open-order telemetry;
- helper detail endpoint duplicate detection;
- live fuse consumed state;
- workflow execution id/run id;
- market/side/ord_type tuple.

Duplicate key:

```text
market|side|ord_type|approval_id|fuse_id
```

Duplicate block rules:

- same `market|side|ord_type` with active lock -> STOP;
- same tuple with unresolved journal event -> STOP;
- any open order for target market -> STOP;
- live fuse consumed -> STOP;
- duplicate state uncertain -> STOP.

## 10. Concurrent Workflow Prevention

The execution lock must prevent concurrency even while workflows remain inactive/manual.

Required future checks:

- confirm WF03 inactive;
- confirm WF04 inactive;
- confirm WF05 inactive/manual/read-only;
- confirm no duplicate active Upbit workflow exists;
- confirm no cron schedule exists for Upbit execution path;
- confirm no execution workflow is already running if runtime APIs are approved for read-only status checks.

If runtime workflow state cannot be read safely, STOP.

## 11. Interaction With Live Fuse

Execution lock and live fuse are separate controls.

Rules:

- lock acquisition does not arm fuse by itself;
- fuse cannot be armed if lock exists from another run;
- fuse cannot be reset by lock logic;
- fuse cannot be reset by workflow logic;
- fuse must be consumed before live order call in any future approved execution;
- consumed fuse blocks repeat execution even if lock is released;
- lock release does not reset fuse;
- fuse ambiguity forces STOP.

Required order:

```text
reconciliation PASS
-> human approval
-> lock acquisition
-> journal acquisition event
-> fuse arm approval
-> fuse armed once
-> one bounded execution attempt
-> fuse consumed
-> reconciliation required
-> lock release only after final state review
```

## 12. Interaction With Order Journal

The order journal is the durable execution memory.

Lock system must:

- read or reconstruct recent order intent from order journal;
- append lock events to lock journal;
- reference order journal events without copying raw payloads;
- refuse execution if order journal is missing;
- refuse execution if order journal is inconsistent;
- refuse execution if order journal write fails;
- refuse execution if previous order lacks final reconciliation.

Order journal and lock journal should be independently append-only.

## 13. Interaction With Helper Detail Endpoint

The helper detail endpoint remains read-only reconciliation authority.

Allowed interactions:

- read `open_order_exists`;
- read `open_order_count`;
- read `duplicate_order_exists`;
- read `new_order_created_detected`;
- read `classification_summary.final_classification`;
- read `blocked_reason`;
- append sanitized reconciliation journal evidence if configured.

Forbidden interactions:

- helper detail endpoint must not acquire lock;
- helper detail endpoint must not release lock;
- helper detail endpoint must not arm fuse;
- helper detail endpoint must not place, cancel, reorder, retry, activate, enable cron, or send Telegram.

Future lock implementation may consume helper detail telemetry as evidence only.

## 14. Failure Behavior

Failure behavior must be fail-safe.

Failure conditions:

- lock file missing when expected;
- lock file malformed;
- lock journal missing;
- lock journal write failure;
- active lock exists;
- stale lock exists;
- duplicate lock event exists;
- order journal unavailable;
- helper detail endpoint unavailable;
- helper detail endpoint returns `unknown_stop`;
- open order exists;
- duplicate order exists;
- workflow state unclear;
- cron state unclear;
- live fuse state unclear;
- secret scan fails;
- forbidden endpoint scan fails.

Required outcome:

- STOP;
- no lock acquisition;
- no lock release;
- no live fuse reset;
- no order;
- no cancel;
- no reorder;
- no retry;
- no workflow activation;
- no cron enablement;
- no Telegram runtime send;
- create sanitized blocked report.

## 15. Manual Unlock Rules

Manual unlock is a controlled documentation and state-update action, not an automatic recovery path.

Manual unlock requires:

- explicit human approval;
- read-only reconciliation PASS;
- `open_order_exists=false`;
- `open_order_count=0`;
- duplicate order not detected;
- previous order final state `done` or `cancel`;
- order journal reviewed;
- lock journal reviewed;
- stale lock reason documented;
- rollback impact understood;
- append-only unlock event written before active lock is cleared or superseded.

Manual unlock must not:

- trigger execution;
- reset fuse;
- enable cron;
- activate workflow;
- place second order;
- cancel or reorder.

## 16. Forbidden Auto-Unlock Behavior

Forbidden forever unless a future safety design explicitly supersedes this document:

- auto-unlock by timeout;
- auto-unlock after helper restart;
- auto-unlock after n8n restart;
- auto-unlock after EC2 reboot;
- auto-unlock after successful health check only;
- auto-unlock after `open_order_exists=false` only;
- auto-unlock after Telegram acknowledgement;
- auto-unlock before journal write;
- auto-unlock that resets live fuse;
- auto-unlock that triggers retry or second order.

No auto-unlock. No auto-retry.

## 17. Offline Tests Required

Future implementation must include offline tests before any runtime patch.

Required cases:

- no lock exists -> acquisition allowed only if all other mocked gates pass;
- active lock exists -> STOP;
- stale lock exists -> STOP + human review;
- malformed lock file -> STOP;
- missing lock journal -> STOP;
- lock journal write failure -> STOP;
- order journal missing -> STOP;
- open order exists -> STOP;
- duplicate order exists -> STOP;
- helper detail `unknown_stop` -> STOP;
- workflow active unexpectedly -> STOP;
- cron enabled unexpectedly -> STOP;
- fuse consumed -> STOP;
- fuse ambiguous -> STOP;
- manual unlock with complete evidence -> unlock event allowed;
- manual unlock with missing evidence -> STOP;
- secret leak scan -> PASS required;
- forbidden endpoint scan -> PASS required.

Offline tests must use:

- no live API;
- no helper runtime call;
- no workflow execution;
- no Docker restart;
- no order;
- no cancel;
- no reorder;
- no Telegram send.

## 18. Minimum Implementation Scope

Minimum future implementation scope should be small and non-executing:

- create lock schema validator;
- create lock state reader;
- create lock journal append helper;
- create offline fixtures;
- create offline regression runner;
- create read-only lock status report;
- no workflow patch;
- no helper mutation endpoint;
- no live execution integration;
- no live fuse reset logic;
- no Telegram runtime send.

First implementation should be documentation + offline utility only unless explicitly approved otherwise.

## 19. Absolute Blockers Before Implementation

Implementation must be blocked if:

- lock storage path is not explicitly approved;
- order journal path is not validated;
- helper detail endpoint health is not PASS;
- workflows are active;
- cron is enabled;
- live fuse state is unclear;
- open order exists;
- duplicate order exists;
- previous order finality is unclear;
- rollback path is missing;
- offline tests are not defined;
- secret scan is not available;
- forbidden endpoint scan is not available;
- implementation scope includes execution;
- implementation scope includes cancel/reorder;
- implementation scope includes workflow activation;
- implementation scope includes cron.

## 20. Approval Gate Before Patch Prompt

Patch prompt is not allowed now.

Required before any patch prompt:

1. Human reviews this design/scope document.
2. Human explicitly approves the proposed lock storage location.
3. Human explicitly approves implementation class.
4. Human confirms scope is offline/read-only first unless separately expanded.
5. Human confirms no workflow activation, cron, live execution, cancel, reorder, Telegram runtime send, or fuse reset is included.
6. Required offline tests are listed in the patch prompt.
7. Rollback and validation report requirements are listed in the patch prompt.

Approval for this design is not approval for live execution.

## Design Decision Summary

- Proposed lock storage location: `/home/ubuntu/kbia-logs/upbit-helper/execution-locks/active_execution_lock.json` plus append-only `/home/ubuntu/kbia-logs/upbit-helper/execution-lock-journal/execution_lock_YYYY-MM-DD.jsonl`.
- Lock schema: defined.
- Patch prompt allowed now: false.

NO EXECUTION LOCK PATCH MAY BE WRITTEN UNTIL THIS DESIGN/SCOPE IS REVIEWED AND EXPLICITLY APPROVED.
