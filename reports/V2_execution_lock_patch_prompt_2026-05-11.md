# V2 Execution Lock Implementation Patch Prompt Draft

Date: 2026-05-11  
Mode: Patch-prompt drafting only  
Runtime status: Controlled STOP state  

This document defines a future bounded Codex patch prompt for execution lock support. It does not authorize implementation execution.

## Future Codex Patch Prompt

### Role

You are Codex working on Upbit Investment Automation.

### Mode

Execution lock implementation only. Safety-first. Additive-only. Validation-first.

Implementation is allowed only for execution lock file handling and offline validation. No workflow integration and no live execution are approved.

### Current Verified State

- Helper detail endpoint deployed PASS.
- Automation disabled.
- Workflows inactive.
- Cron disabled.
- Live fuse disabled.
- `open_order_exists=false`.
- Execution lock design/scope completed.
- Lock schema defined.
- Active lock path approved:

```text
/home/ubuntu/kbia-logs/upbit-helper/execution-locks/active_execution_lock.json
```

- Lock journal path approved:

```text
/home/ubuntu/kbia-logs/upbit-helper/execution-lock-journal/execution_lock_YYYY-MM-DD.jsonl
```

### 1. Exact Bounded Implementation Scope

Implement only:

- execution lock file handling;
- active lock read;
- active lock create/acquire;
- active lock release with explicit request;
- stale lock detection;
- append-only lock journal;
- schema validation;
- atomic write handling;
- partial write protection;
- concurrent access protection;
- crash recovery classification;
- offline fixtures;
- offline regression runner;
- sanitized validation report.

This patch must not integrate the lock with workflows or live execution. The lock does not authorize order execution. The lock does not reset live fuse. The lock does not activate workflows.

### 2. Explicit Non-Goals

Do not implement:

- workflow patch;
- workflow activation;
- cron enablement;
- order placement;
- cancel;
- reorder;
- retry loop;
- Telegram runtime send;
- live fuse reset;
- investment decision logic;
- autonomous unlock;
- live execution;
- WF03 integration;
- WF04 integration;
- WF05 integration;
- helper order endpoint changes;
- helper live-order behavior changes;
- Docker/runtime restart unless separately approved.

### 3. Required Helper/Source Backup Steps

Before any file modification:

1. Create local backup folder:

```text
C:\Users\minho\Documents\02_work\03_AI\03_investment_automation\01_planning\backups\execution_lock_YYYYMMDD_HHMMSS
```

2. Back up any file that will be changed or created under code/test scope.
3. If helper source is touched in a future approved variant, back up:

```text
C:\Users\minho\Documents\02_work\03_AI\03_investment_automation\01_planning\upbit-helper
```

4. Do not copy secrets.
5. Do not print secrets.
6. Create rollback instructions before patching.

If backup fails, STOP.

### 4. Required Rollback Steps

Rollback instructions must be written before patching and must include:

1. Stop patch work.
2. Restore changed files from backup.
3. Validate Python syntax if Python files were touched.
4. Run offline lock regression tests.
5. Confirm no workflow files changed.
6. Confirm no runtime files changed outside approved scope.
7. Confirm no Docker/restart occurred.
8. Confirm no live API/order/cancel/reorder/Telegram calls occurred.
9. Write sanitized rollback report.

Rollback must not auto-unlock, reset fuse, activate workflows, enable cron, place orders, cancel, reorder, retry, or send Telegram runtime messages.

### 5. Active Lock Path

Use this active lock path:

```text
/home/ubuntu/kbia-logs/upbit-helper/execution-locks/active_execution_lock.json
```

For offline local tests, use a temporary fixture root under:

```text
C:\Users\minho\Documents\02_work\03_AI\03_investment_automation\01_planning\tests\execution_lock_runtime_fixture
```

Do not write to the real remote lock path unless a separate runtime implementation/deployment approval is given.

### 6. Lock Journal Path

Use this append-only lock journal path:

```text
/home/ubuntu/kbia-logs/upbit-helper/execution-lock-journal/execution_lock_YYYY-MM-DD.jsonl
```

For offline tests, use a temporary local fixture journal path.

Journal rules:

- append only;
- one JSON object per line;
- no overwrite;
- no delete;
- no update-in-place;
- no JWT;
- no Authorization header;
- no API secret;
- no raw balances;
- no raw order payload;
- no full UUID;
- no execution payload.

### 7. Lock Schema

Active lock schema:

```json
{
  "schema_version": "v2.execution_lock.1",
  "lock_id": "safe-lock-id",
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
  "journal_ref": "relative-or-masked-journal-reference",
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

Allowed `lock_state` values:

- `active`
- `released`
- `stale_stop`
- `unknown_stop`

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

### 8. Lock Acquisition Rules

Acquire lock only if all mocked/offline gate inputs pass:

- explicit human approval field exists;
- `open_order_exists=false`;
- `open_order_count=0`;
- duplicate order not detected;
- reconciliation classification is `done` or `cancel`;
- workflow active is false;
- cron enabled is false;
- fuse state is safe for lock acquisition but not reset;
- no active lock exists;
- no stale lock exists;
- lock journal is writable;
- order journal evidence is present;
- forbidden endpoint check is true;
- secrets leak check is true.

STOP rules:

- if lock status unclear -> STOP;
- if active lock exists -> STOP;
- if stale lock exists -> STOP + human review;
- if open order exists -> STOP;
- if duplicate order exists -> STOP;
- if reconciliation is `wait`, `partial_fill`, or `unknown_stop` -> STOP;
- if workflow active -> STOP;
- if cron enabled -> STOP;
- if fuse state unclear -> STOP;
- if journal write fails -> STOP.

### 9. Lock Release Rules

Release lock only through explicit release input.

Allowed release preconditions:

- explicit human release approval;
- active lock exists and is valid;
- reconciliation state is final `done` or `cancel`, or release reason is `approved_abort_before_execution`;
- open order check is false;
- lock journal append succeeds;
- release reason is recorded.

Release behavior:

- append release event first;
- then move, rename, or replace active lock with a released marker using atomic write;
- never delete historical journal events;
- never reset fuse;
- never trigger execution;
- never activate workflow;
- never enable cron.

### 10. Stale Lock Policy

Stale lock means STOP.

Rules:

- expired lock is stale;
- malformed timestamp is `unknown_stop`;
- stale lock requires human review;
- stale lock must not auto-unlock;
- stale lock must not auto-retry;
- stale lock must not reset fuse;
- stale lock must not trigger cancel/reorder/reprice;
- stale lock must produce blocked report.

### 11. Manual Unlock Rules

Manual unlock requires explicit human approval and complete evidence.

Required evidence:

- active or stale lock file present;
- order journal reviewed;
- lock journal reviewed;
- read-only reconciliation final state `done` or `cancel`;
- `open_order_exists=false`;
- `open_order_count=0`;
- duplicate order not detected;
- workflow inactive;
- cron disabled;
- fuse state documented;
- release reason documented.

Manual unlock must append a journal event before changing active lock state.

Manual unlock does not authorize live execution.

### 12. Forbidden Auto-Unlock Behavior

Do not implement:

- auto-unlock by timeout;
- auto-unlock after helper restart;
- auto-unlock after n8n restart;
- auto-unlock after EC2 reboot;
- auto-unlock after health check;
- auto-unlock after `open_order_exists=false` only;
- auto-unlock after Telegram acknowledgement;
- auto-unlock before journal write;
- auto-unlock that resets fuse;
- auto-unlock that triggers retry;
- auto-unlock that enables second order.

### 13. Atomic Write / Partial Write Safety

Active lock writes must be atomic.

Required method:

1. Write full JSON to a temp file in the same directory.
2. Flush file contents.
3. Replace active lock using atomic rename/replace.
4. Validate by reading back JSON.
5. Append journal event.

Partial write handling:

- temp file left behind -> STOP and report;
- active lock invalid JSON -> STOP;
- active lock missing after write -> STOP;
- journal append failure -> STOP.

### 14. Concurrent Access Safety

Concurrent access must be fail-safe.

Required behavior:

- use exclusive create where available;
- if active lock appears during acquisition -> STOP;
- if lock file changes while validating -> STOP;
- if multiple acquire attempts race -> only one may succeed;
- all losers must append blocked journal event if safe;
- no retry loop.

If atomic concurrency cannot be guaranteed in the current implementation environment, implement read/report only and return BLOCKED for acquisition.

### 15. Crash Recovery Behavior

Crash recovery must never resume trading.

On recovery:

- read active lock;
- read lock journal;
- read order journal;
- read helper detail endpoint only if runtime validation is separately approved;
- classify state as active, released, stale_stop, or unknown_stop;
- if any mismatch exists -> STOP;
- if active lock exists -> STOP;
- if stale lock exists -> STOP + human review;
- if journal missing -> STOP;
- no auto-unlock;
- no auto-retry;
- no live execution.

### 16. Offline Tests Required

Create offline fixtures and regression tests for:

- no lock exists and all gates pass -> acquire allowed;
- no lock exists but open order exists -> STOP;
- no lock exists but reconciliation unknown -> STOP;
- active lock exists -> STOP;
- stale lock exists -> STOP + human review;
- malformed lock file -> STOP;
- missing lock journal -> STOP;
- journal append failure -> STOP;
- temp file/partial write exists -> STOP;
- concurrent acquire simulation -> one acquire at most;
- release with approval and final reconciliation -> release allowed;
- release without approval -> STOP;
- release with open order -> STOP;
- manual unlock with complete evidence -> unlock event allowed;
- manual unlock with missing evidence -> STOP;
- fuse consumed -> STOP;
- fuse ambiguous -> STOP;
- workflow active -> STOP;
- cron enabled -> STOP;
- secret leak scan -> PASS;
- forbidden endpoint scan -> PASS.

Offline tests must use:

- no live API;
- no helper runtime call;
- no workflow execution;
- no Docker restart;
- no order;
- no cancel;
- no reorder;
- no Telegram send.

### 17. Post-Patch Validation Sequence

Validation must run in this order:

1. Confirm backup and rollback instructions exist.
2. Confirm no workflow files changed.
3. Confirm no helper live-order behavior changed.
4. Confirm no Docker/runtime files changed.
5. Run syntax checks.
6. Run offline fixture tests.
7. Run concurrent acquisition simulation.
8. Run atomic write/partial write test.
9. Run forbidden endpoint scan.
10. Run secret leak scan.
11. Create sanitized validation report.
12. Update patch history and daily telemetry.

No runtime deployment, restart, workflow activation, cron enablement, live API call, order, cancel, reorder, or Telegram runtime send is part of this validation.

### 18. STOP Conditions

STOP immediately if:

- scope includes workflow patch;
- scope includes live execution;
- scope includes helper mutation endpoint;
- scope includes order/cancel/reorder;
- scope includes retry loop;
- scope includes Telegram runtime send;
- scope includes live fuse reset;
- backup missing;
- rollback missing;
- lock path unclear;
- lock journal path unclear;
- active lock exists;
- stale lock exists;
- lock state unclear;
- atomic write cannot be made safe;
- concurrent access cannot be made safe;
- journal append fails;
- offline test fails;
- forbidden endpoint scan fails;
- secret leak scan fails.

### 19. Required Telemetry Output

Future implementation must return:

```text
[RESULT]
overall_status:
- PASS / BLOCKED / FAIL

implementation:
- execution_lock_support_created:
- lock_files_created:
- runtime_modified:
- workflow_modified:
- helper_live_order_behavior_changed:

lock_paths:
- active_lock_path:
- lock_journal_path:

validation:
- backup_check:
- rollback_check:
- syntax_check:
- offline_fixture_tests:
- concurrent_access_test:
- atomic_write_test:
- stale_lock_test:
- manual_unlock_test:
- forbidden_endpoint_scan:
- secret_leak_scan:

safety:
- workflow_patch_included: false
- live_execution_included: false
- live_order_attempted: false
- cancel_attempted: false
- reorder_attempted: false
- cron_enabled: false
- workflow_activation_changed: false
- telegram_live_send_attempted: false
- live_fuse_reset_attempted: false

artifacts:
- backup_path:
- files_changed:
- validation_report_path:
- rollback_path:

blockers:
- list any blockers

next_action:
- one safe next action only
```

### 20. Workflows Remain Untouched And Inactive

The patch must not touch:

- `workflows/03_WF_PreCheck_Engine.json`;
- `workflows/04_WF_Execution_Engine.json`;
- `workflows/05_WF_Post_Execution.json`;
- any n8n runtime workflow state;
- any cron or schedule;
- any Telegram runtime path.

Workflows must remain inactive. Automation must remain disabled.

### Final Safety Statement

The execution lock is a STOP control only. It does not authorize order execution. It does not reset live fuse. It does not activate workflows. It does not enable cron. It does not retry. It does not auto-unlock.

THIS DOCUMENT DOES NOT AUTHORIZE EXECUTION LOCK PATCHING; IT ONLY DEFINES THE FUTURE BOUNDED PATCH PROMPT.
