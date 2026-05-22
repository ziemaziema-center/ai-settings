# WF05 Corrected Status-Only Runtime Validation

Date: 2026-05-12 KST

Mode: safety-gated WF05 runtime validation

## Result

overall_status: BLOCKED

## Blocker

The approved existing-running-n8n API execution path was reached, but the deployed n8n instance returned:

```text
405 POST method not allowed
```

for:

```text
POST /api/v1/workflows/:id/run
```

No fallback execution path was used because the hard limit allows only:

- `POST /api/v1/workflows/:id/run` on the already running n8n instance; or
- one human-driven n8n editor `Execute Workflow` action.

The API path could not execute WF05, and the operator did not perform the UI fallback in this turn. Therefore the required result is `BLOCKED`.

## Mandatory Pre-Steps

- WF05 inactive: `true`
- cron disabled: `true`
- automation disabled: `true`
- live fuse disabled: `true`
- open_order_exists: `false`
- open_order_count: `0`
- duplicate_order_exists: `false`
- no active execution lock exists: `true`
- lock_state: `unlocked`
- lock_exists: `false`
- stale_lock: `false`
- WF03 inactive: `true`
- WF04 inactive: `true`
- execution method confirmed as already-running n8n API server: `true`

## Execution

- wf05_manual_execution_started: `false`
- wf05_manual_execution_completed: `false`
- execution_method_used: `POST /api/v1/workflows/:id/run` on existing running n8n API server
- api_result: `405 POST method not allowed`
- n8n_execution_id: `null`
- wf05_execution_count_before: `0`
- wf05_execution_count_after: `0`
- wf05_execution_count_delta: `0`

## Validation

- reconciliation_status_path: `false`
- helper_endpoint_reachable: `preflight_true_runtime_not_started`
- stop_path_reachable: `false`
- duplicate_unclear_stop_path: `not_runtime_reached_existing_offline_validation_pass`
- reconciliation_unclear_stop_path: `not_runtime_reached_existing_offline_validation_pass`
- live_api_called: `false`

## Safety

- wf03_executed: `false`
- wf04_executed: `false`
- workflow_activation_changed: `false`
- cron_enabled: `false`
- live_order_attempted: `false`
- cancel_attempted: `false`
- reorder_attempted: `false`
- telegram_runtime_send_attempted: `false`
- live_fuse_reset_attempted: `false`
- cli_execution_used: `false`
- restart_attempted: `false`
- multiple_execution_attempted: `false`
- lock_acquire_attempted: `false`
- lock_release_attempted: `false`
- webhook_triggered_execution_attempted: `false`
- cron_triggered_execution_attempted: `false`

## Artifacts

- execution_report_path: `reports/WF05_corrected_status_only_runtime_validation_BLOCKED_2026-05-12.md`
- execution_log_path: `logs/WF05_corrected_status_only_runtime_validation_BLOCKED_2026-05-12.json`

## Next Action

Use the single human-driven n8n editor `Execute Workflow` fallback only after a separate operator action/confirmation.
