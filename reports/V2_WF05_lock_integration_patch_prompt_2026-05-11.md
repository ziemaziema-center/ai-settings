# V2 WF05 Lock Integration Patch Prompt

Date: 2026-05-11 KST

Mode: patch-prompt drafting only

Runtime status: unchanged by this document

This document is a future bounded Codex patch prompt for `WF05_Reconciliation_ReadOnly` read-only lock integration. It does not approve or perform workflow patching.

## Future Patch Prompt

```text
[ROLE]
You are Codex working on Upbit Investment Automation.

[MODE]
Implementation allowed only within strictly bounded WF05 read-only lock integration scope.
Safety-first.
Validation-first.
Additive-only.

[USER EXPLICIT APPROVAL REQUIRED]
The human operator must explicitly approve:
- WF05 read-only lock integration implementation

No other approval is granted.

[OBJECTIVE]
Patch only WF05_Reconciliation_ReadOnly so it can perform read-only reconciliation plus execution-lock status checks and operator-facing STOP reporting.

This is not live execution.
This is not workflow activation.
This is not cron enablement.
This is not order/cancel/reorder logic.

[CURRENT REQUIRED STATE BEFORE PATCH]
- helper detail endpoint deployed PASS
- execution lock runtime deployed PASS
- helper health PASS
- lock final state unlocked
- open_order_exists=false
- open_order_count=0
- workflows inactive
- cron disabled
- automation disabled
- live fuse disabled

[STRICT SCOPE]
Allowed:
- WF05_Reconciliation_ReadOnly only
- workflow JSON backup
- read-only helper health check
- read-only helper detail endpoint call
- read-only execution-lock status check
- optional report-only lock state normalization
- sanitized append-only log/report artifact
- offline regression fixtures for lock states
- dry-run/manual validation while workflow remains inactive

Forbidden:
- WF03 patch
- WF04 patch
- helper patch
- Docker/runtime change
- workflow activation
- cron/schedule enablement
- live order execution
- cancel
- reorder
- retry loop
- Telegram runtime send
- live fuse reset
- investment decision logic
- autonomous unlock
- execution-lock acquire/release unless separately approved in a future dry-run-only gate
- workflow auto-activation

[EXACT WF05-ONLY INTEGRATION SCOPE]
Patch only:
- workflows/05_WF_Post_Execution.json

Do not touch:
- workflows/03_WF_PreCheck_Engine.json
- workflows/04_WF_Execution_Engine.json
- upbit-helper/app/main.py
- Docker/container/runtime config
- reel-service
- Instagram/SNS workflows
- Telegram runtime send paths
- credentials/secrets

WF05 must remain:
- inactive
- manual-trigger only
- read-only
- no cron
- no schedule trigger
- no execution authority

[EXPLICIT NON-GOALS]
Do not implement:
- live execution
- order placement
- cancel flow
- reorder flow
- retry loop
- live fuse reset
- Telegram live send
- Telegram execution buttons
- workflow activation
- cron enablement
- autonomous unlock
- investment decision logic
- any WF03/WF04 behavior change

[REQUIRED WORKFLOW BACKUP STEPS]
Before editing WF05:
1. Create backup folder:
   C:\Users\minho\Documents\02_work\03_AI\03_investment_automation\01_planning\backups\wf05_lock_integration_YYYYMMDD_HHMMSS
2. Copy current `workflows/05_WF_Post_Execution.json` into the backup.
3. Write rollback instructions into the backup folder.
4. Confirm backup exists before patching.

[REQUIRED ROLLBACK STEPS]
Rollback method must be documented before patching:
1. Restore backed-up `05_WF_Post_Execution.json`.
2. Validate JSON syntax.
3. Confirm WF05 remains inactive.
4. Confirm manual trigger only.
5. Confirm no cron/schedule.
6. Confirm no live-order/cancel/reorder/withdrawal/Telegram send endpoints.
7. Confirm WF03/WF04 unchanged.

[EXACT LOCK CHECK SEQUENCE]
WF05 read-only lock integration sequence:

1. Manual trigger only.
2. Build safe input context.
3. Call helper `/health`.
4. If helper unavailable -> STOP.
5. Call helper `/upbit/open-orders/detail-telemetry` in read-only mode.
6. If detail telemetry missing, malformed, inconsistent, or unknown -> STOP.
7. If `open_order_exists=true` -> STOP.
8. If `open_order_count != 0` -> STOP.
9. If `duplicate_order_exists=true` -> STOP.
10. If duplicate-order status is missing or unclear -> STOP.
11. If reconciliation classification is not final/unambiguous -> STOP.
12. Call helper `/execution-lock/status`.
13. If lock unavailable -> STOP.
14. If `lock_state=unlocked` and `lock_exists=false` -> report lock clear.
15. If active lock exists -> STOP.
16. If stale lock exists -> STOP + human review.
17. If lock status unclear or malformed -> STOP.
18. Produce sanitized WF05 report/log.
19. End without execution action.

[EXACT HELPER DETAIL ENDPOINT USAGE SEQUENCE]
Use only:
- `GET /health`
- `POST /upbit/open-orders/detail-telemetry`
- `POST /execution-lock/status`

Do not use:
- `/upbit/live-order/telemetry`
- `/upbit/order-test/telemetry` unless separately approved for a future test-only gate
- `/execution-lock/acquire`
- `/execution-lock/release`
- any cancel/reorder/withdrawal endpoint
- Telegram send endpoint

Helper detail request must be read-only:
- market: `KRW-BTC`
- include_recent_closed: true only if already safe in helper
- journal_enabled: true only for sanitized append-only reconciliation evidence
- no raw order payload logging
- no full UUID logging

[REQUIRED STOP CONDITIONS]
WF05 must STOP if:
- helper health fails;
- helper detail endpoint fails;
- execution lock status endpoint fails;
- lock unavailable;
- active lock exists;
- stale lock exists;
- lock response malformed;
- partial lock write is reported;
- reconciliation unclear;
- duplicate-order status unclear;
- duplicate order exists;
- open order exists;
- open order count is not zero;
- cron status is unknown;
- workflow active status is unknown;
- live fuse state is unknown or ambiguous;
- persistent log write fails;
- forbidden endpoint scan fails;
- secret leak scan fails.

[REQUIRED STALE LOCK HANDLING]
If stale lock exists:
- classify as `stale_lock_stop`;
- set `human_review_required=true`;
- do not auto-unlock;
- do not acquire another lock;
- do not release lock;
- do not retry;
- do not execute;
- create sanitized report/log only;
- next safe action: `human_review_required`.

[REQUIRED RECONCILIATION HANDLING]
Allowed classifications:
- `done`
- `cancel`
- `wait`
- `partial_fill`
- `unknown_stop`

Rules:
- `done` or `cancel` may proceed to read-only lock status check.
- `wait`, `partial_fill`, `unknown_stop`, missing, or inconsistent classification must STOP.
- no action may be taken based on fill or cancel state.
- no second order may be created.

[DUPLICATE-ORDER UNCERTAINTY HANDLING]
If duplicate-order status is:
- true -> STOP
- false -> continue to lock status only
- missing -> STOP
- unknown -> STOP
- malformed -> STOP

Duplicate-order clear does not authorize execution.

[REQUIRED OFFLINE REGRESSION CASES]
Add and pass offline fixtures for:
1. helper health failure -> STOP
2. detail endpoint failure -> STOP
3. open order exists -> STOP
4. open order count nonzero -> STOP
5. duplicate order exists -> STOP
6. duplicate-order missing -> STOP
7. reconciliation done + lock unlocked -> read-only PASS
8. reconciliation cancel + lock unlocked -> read-only PASS
9. reconciliation wait -> STOP
10. reconciliation partial_fill -> STOP
11. reconciliation unknown_stop -> STOP
12. lock unavailable -> STOP
13. active lock exists -> STOP
14. stale lock exists -> STOP + human review
15. lock malformed -> STOP
16. partial lock write -> STOP
17. journal/log write failure -> STOP
18. forbidden endpoint string present -> FAIL
19. Telegram send node present -> FAIL
20. cron/schedule node present -> FAIL

[REQUIRED DRY-RUN VALIDATION CASES]
After patch, validate:
1. WF05 JSON syntax PASS.
2. WF05 remains inactive.
3. WF05 manual trigger only.
4. no cron/schedule node.
5. no workflow activation performed.
6. no WF03/WF04 file change.
7. no helper file change.
8. no live-order endpoint string.
9. no cancel/reorder/withdrawal endpoint string.
10. no Telegram send node.
11. no execution-lock acquire/release call unless separately approved.
12. lock status unlocked path produces read-only report only.
13. active lock fixture blocks.
14. stale lock fixture blocks and marks human review required.
15. helper unavailable fixture blocks.
16. duplicate uncertainty fixture blocks.
17. secret leak scan PASS.
18. forbidden endpoint scan PASS.
19. output log/report sanitized.
20. no live API order/cancel/reorder executed.

[REQUIRED TELEMETRY OUTPUT]
Future patch final result must include:
- overall_status
- backup_path
- workflow_path
- wf05_modified
- wf05_active
- trigger_type
- cron_present
- helper_modified
- wf03_modified
- wf04_modified
- live_execution_included
- lock_status_endpoint_used
- helper_detail_endpoint_used
- lock_acquire_used
- lock_release_used
- offline_regression_result
- dry_run_validation_result
- forbidden_endpoint_scan
- secret_leak_scan
- report_path
- rollback_ready
- next_safe_action

[REQUIRED POST-PATCH VALIDATION]
Post-patch validation must prove:
- WF05 inactive after patch;
- manual trigger only;
- cron disabled;
- no schedule trigger;
- no live execution introduced;
- no live-order endpoint;
- no cancel endpoint;
- no reorder endpoint;
- no withdrawal endpoint;
- no retry loop;
- no Telegram runtime send;
- no auto-unlock;
- no execution-lock acquire/release unless separately approved;
- helper unchanged;
- WF03 unchanged;
- WF04 unchanged;
- workflow activation unchanged;
- offline regression PASS;
- dry-run validation PASS;
- rollback instructions present.

[EXPLICIT INACTIVE WORKFLOW STATEMENT]
WF05 must remain inactive after patch.

[EXPLICIT CRON STATEMENT]
Cron must remain disabled. No cron or schedule trigger may be added.

[EXPLICIT NO LIVE EXECUTION STATEMENT]
No live execution is introduced by this patch. The patch may only observe helper detail telemetry and execution lock status, classify STOP/PASS read-only state, and write sanitized reports/logs.

[FINAL STOP RULES]
If lock unavailable -> STOP.
If active lock exists -> STOP.
If stale lock exists -> STOP + human review.
If reconciliation unclear -> STOP.
If duplicate-order status unclear -> STOP.
If any live execution path appears -> STOP.
If any workflow activation is required -> STOP.
If any cron activation is required -> STOP.
If any helper modification is required -> STOP.
If anything exceeds WF05 read-only scope -> STOP.

[OUTPUT FORMAT]
Return exact telemetry required by the future implementation prompt, including backup path, files changed, validation results, rollback readiness, and safety booleans.
```

## Scope Decision For This Prompt Draft

- wf05_only: true
- live_execution_included: false
- cron_activation_included: false
- workflow_activation_included: false
- helper_patch_included: false
- WF03_patch_included: false
- WF04_patch_included: false

## Final Line

THIS DOCUMENT DOES NOT AUTHORIZE WORKFLOW PATCHING; IT ONLY DEFINES THE FUTURE BOUNDED WF05 READ-ONLY LOCK INTEGRATION PATCH PROMPT.
