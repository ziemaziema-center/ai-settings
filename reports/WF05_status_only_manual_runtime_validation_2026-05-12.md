# WF05 Status-Only Manual Runtime Validation

Date: 2026-05-12 KST

Mode: corrected WF05 status-only manual runtime validation

## Result

overall_status: FAIL

## Execution Result

WF05 manual execution was attempted once through the n8n CLI, but the workflow did not start successfully.

Failure reason:

```text
n8n Task Broker's port 5679 is already in use. Do you have another instance of n8n running already?
```

Interpretation:

- The running n8n service already owns the task broker port.
- The one-shot `n8n execute` CLI process exited before creating a WF05 execution record.
- No second execution attempt was made.

## Pre-Execution Gates

- helper_health_ok: `true`
- open_order_exists: `false`
- open_order_count: `0`
- lock_state: `unlocked`
- lock_exists: `false`
- stale_lock: `false`
- WF05 active: `false`
- WF05 trigger_count before: `0`
- manual_trigger_only: `true`
- cron_present: `false`
- helper_detail_endpoint_present: `true`
- lock_status_endpoint_present: `true`
- lock_acquire_present: `false`
- lock_release_present: `false`
- live_order_path_present: `false`
- cancel_reorder_withdraw_path_present: `false`
- telegram_send_present: `false`
- WF05 execution_count before: `0`

## Post-Attempt State

- WF05 execution_count after: `0`
- WF05 execution_count delta: `0`
- WF05 remains inactive: `true`
- cron remains disabled: `true`
- WF03 executed: `false`
- WF04 executed: `false`
- workflow activation changed: `false`
- live API called: `false`
- live order attempted: `false`
- cancel attempted: `false`
- reorder attempted: `false`
- Telegram runtime send attempted: `false`
- live fuse reset attempted: `false`

## Validation Status

- reconciliation_status_path: `false`
- helper_endpoint_reachable in WF05 runtime execution: `false`
- stop_path_reachable in WF05 runtime execution: `false`
- duplicate_unclear_stop_path: `validated_offline_before_runtime`
- reconciliation_unclear_stop_path: `validated_offline_before_runtime`

## Remote Evidence

- remote_run_dir: `/home/ubuntu/kbia_backups/wf05-status-only-runtime-validation-20260512`
- stdout_path: `/home/ubuntu/kbia_backups/wf05-status-only-runtime-validation-20260512/wf05_execute_stdout.json`
- stderr_path: `/home/ubuntu/kbia_backups/wf05-status-only-runtime-validation-20260512/wf05_execute_stderr.txt`
- summary_path: `/home/ubuntu/kbia_backups/wf05-status-only-runtime-validation-20260512/wf05_status_only_runtime_validation_summary.json`

## Next Safe Action

Design a separate n8n-safe manual execution method that does not start a competing task broker, then review it before any second WF05 runtime execution attempt.
