# V2 Helper Detail Endpoint Patch Prompt Draft

Date: 2026-05-11  
Mode: Patch-planning only  
Runtime status: Controlled STOP state  
Automation status: disabled  
Workflow status: inactive  

This document defines the future bounded patch prompt for the V2 helper detail endpoint. It does not execute the patch and does not authorize runtime modification.

## 1. Exact Bounded Implementation Scope

Future implementation scope is limited to:

- one additive helper detail endpoint
- read-only Upbit order/account detail summarization needed for reconciliation
- sanitized response fields only
- append-only JSONL journaling only
- offline regression tests for classifier, schema, journal, and safety scans
- validation reports proving no forbidden runtime behavior was added

The helper is reconciliation authority only. It is not execution authority, order authority, cancel authority, retry authority, cron authority, fuse authority, workflow authority, or investment-decision authority.

Required principle:

```text
STOP > EXECUTE
```

## 2. Explicit Non-Goals

The future patch must not include:

- workflow patch
- workflow activation
- cron enablement
- order placement
- cancel
- reorder
- retry loop
- live execution
- Telegram runtime send
- live fuse reset
- Docker or network changes outside separately approved helper scope
- autonomous investment logic
- market selection logic
- profit optimization
- portfolio rebalancing
- cancel/reprice behavior
- hidden fallback execution path

Read-only only. Reconciliation only. No execution authority.

## 3. Required Helper Backup Steps

Before any future helper patch, the operator must create and verify a backup.

Required backup target:

```text
/home/ubuntu/upbit-helper
```

Required future backup directory pattern:

```text
C:\Users\minho\Documents\02_work\03_AI\03_investment_automation\01_planning\backups\helper_detail_endpoint_YYYYMMDD_HHMMSS
```

Required backup evidence:

- backup path
- copied helper source files
- copied helper dependency/config metadata if safe
- no `.env` secret contents exposed
- no API secret copied into reports
- backup verification result

If backup fails or exposes secrets, STOP. Do not patch.

## 4. Required Rollback Steps

Future rollback plan must be documented before patching:

1. Stop patch work immediately.
2. Restore helper files from the verified backup.
3. Validate syntax without exposing secrets.
4. Confirm existing endpoints are unchanged by diff review.
5. Run offline tests.
6. Run `/health` only if separately approved.
7. Do not restart unless separately approved.
8. Document rollback result in a sanitized report.

Rollback must not place orders, cancel orders, activate workflows, enable cron, reset live fuse, or send Telegram messages.

## 5. Exact Endpoint Allowed To Be Added

Only this endpoint may be added:

```text
POST /upbit/open-orders/detail-telemetry
```

No other endpoint may be added or modified in the same patch.

Forbidden endpoint additions or modifications:

- live-order endpoint
- order creation endpoint
- cancel endpoint
- reorder endpoint
- withdrawal endpoint
- Telegram send endpoint
- workflow activation endpoint
- cron enable endpoint
- live fuse reset endpoint

## 6. Exact Request And Response Constraints

Allowed request fields:

- `market`
- `run_id`
- `include_recent_closed`
- `recent_closed_limit`
- `journal_enabled`
- `correlation_hint.market`
- `correlation_hint.side`
- `correlation_hint.ord_type`
- `correlation_hint.created_at`

Forbidden request fields:

- JWT
- Authorization header
- API secret
- raw order payload
- raw account balance payload
- full UUID
- execution intent
- cancel intent
- reorder intent
- retry intent
- workflow activation intent
- cron enablement intent
- live fuse reset intent
- investment decision intent

Allowed response fields:

- `success`
- `endpoint`
- `mode`
- `market`
- `open_order_exists`
- `open_order_count`
- `duplicate_order_exists`
- `new_order_created_detected`
- `orders[].uuid_masked`
- `orders[].market`
- `orders[].side`
- `orders[].ord_type`
- `orders[].state`
- `orders[].created_at`
- `orders[].remaining_volume`
- `orders[].executed_volume`
- `orders[].trades_count`
- `orders[].paid_fee`
- `orders[].locked`
- `orders[].price`
- `orders[].classification`
- `classification_summary.final_classification`
- `classification_summary.blocked_reason`
- `classification_summary.next_safe_action`
- `journal_write.attempted`
- `journal_write.success`
- `journal_write.path_masked`
- `forbidden_endpoint_check`
- `secrets_leak_check`

Forbidden response fields:

- JWT
- Authorization header
- API secret
- raw balances
- raw order payload
- signing payload
- full UUID
- full account identifiers

## 7. Exact Append-Only JSONL Constraints

The future endpoint may write only sanitized append-only JSONL journal events.

Required constraints:

- one JSON object per line
- append only
- no overwrite
- no delete
- no update-in-place
- no raw exchange payload
- no raw account balances
- no secrets
- no full UUID
- no execution commands
- no cancel commands
- no retry commands
- no workflow commands
- no Telegram commands

Approved storage direction:

```text
local append-only JSONL on n8n host mounted logging path
```

The exact mounted path must be confirmed before implementation. If the path is unclear, missing, not persistent, or not writable for append-only journaling, STOP.

## 8. Exact Forbidden Behaviors

The future patch must not:

- place an order
- cancel an order
- modify an order
- reorder
- retry execution
- call withdrawal
- reset live fuse
- enable cron
- activate any workflow
- send Telegram runtime messages
- decide investment action
- create autonomous trading logic
- create fallback execution logic
- add hidden loops
- alter existing helper live-order behavior
- alter auth/signing/JWT behavior
- alter API key loading
- alter Docker/runtime/network config without separate approval

Read-only only. Reconciliation only. Fail-safe first.

## 9. Required Offline Regression Tests

Before any live or helper-runtime validation, future implementation must run offline tests only.

Required test coverage:

- request schema validation
- response schema validation
- wait classification
- partial_fill classification
- done classification
- cancel classification
- missing state
- missing volume
- malformed numeric
- negative volume
- inconsistent done state
- unsupported state
- helper error
- timeout error
- rate-limit error
- journal write failure
- forbidden endpoint string scan
- secret leak scan
- no auth/signing/live-order diff scan
- no workflow file modification scan
- no Telegram send path scan

Offline tests must use:

- no network
- no helper runtime
- no Upbit call
- no n8n runtime execution
- no secrets

If any offline test fails, STOP. Do not patch further. Do not run live telemetry.

## 10. Required Validation Sequence

Future validation sequence must run in this order:

1. Confirm explicit human approval for helper-only patch execution.
2. Confirm helper backup exists.
3. Confirm rollback path exists.
4. Review diff scope before editing.
5. Apply additive helper endpoint patch only.
6. Run syntax validation.
7. Run offline regression tests.
8. Run forbidden endpoint scan.
9. Run secret leak scan.
10. Run diff scan for auth/signing/live-order changes.
11. Confirm no workflow files changed.
12. Confirm no Docker/runtime/network files changed unless separately approved.
13. Create sanitized validation report.
14. Stop and wait for human review before any runtime deployment or restart.

No runtime activation is part of this sequence.

## 11. Required Post-Patch Verification

Future post-patch verification report must include:

- backup path
- files changed
- helper files changed
- workflow files changed
- Docker/runtime files changed
- endpoint added
- offline tests result
- forbidden endpoint scan result
- secret leak scan result
- auth/signing diff result
- live-order behavior diff result
- journal behavior result
- rollback path
- safety result
- next safe action

Expected safety values:

- `workflow_modified=false`
- `workflow_activation_changed=false`
- `cron_enabled=false`
- `live_order_attempted=false`
- `cancel_attempted=false`
- `reorder_attempted=false`
- `restart_attempted=false unless separately approved`
- `telegram_live_send_attempted=false`

## 12. Required Fail-Safe Behavior

The endpoint must fail closed.

Required fail-safe behavior:

- missing telemetry -> `unknown_stop`
- malformed telemetry -> `unknown_stop`
- inconsistent volume -> `unknown_stop`
- rate limit -> `unknown_stop`
- timeout -> `unknown_stop`
- helper detail error -> `unknown_stop`
- journal write failure -> blocked response
- secret scan failure -> blocked response
- forbidden endpoint scan failure -> blocked response
- duplicate ambiguity -> blocked response

The endpoint must never recover from an error by placing, canceling, reordering, retrying, activating, enabling cron, resetting fuse, or sending Telegram.

## 13. Exact STOP Conditions

STOP immediately if:

- backup missing
- rollback path missing
- helper path unclear
- journal path unclear
- journal path not persistent
- journal write fails
- auth/signing/JWT code touched
- API key loading touched
- live-order path touched
- cancel/reorder/withdrawal strings introduced
- workflow files touched
- Docker/network/runtime config touched without separate approval
- offline tests fail
- forbidden endpoint scan fails
- secret leak scan fails
- rate-limit behavior retries
- timeout behavior retries in a loop
- any mutation capability appears
- any investment decision logic appears
- any Telegram runtime send path appears

STOP > EXECUTE.

## 14. Exact Telemetry And Report Format Expected After Future Execution

Future patch execution must return this exact style of sanitized result:

```text
[RESULT]
overall_status:
- PASS / BLOCKED / FAIL

implementation:
- helper_detail_endpoint_added:
- endpoint_path:
- runtime_modified:
- workflow_modified:
- docker_modified:

validation:
- backup_created:
- syntax_validation:
- offline_regression_tests:
- forbidden_endpoint_scan:
- secret_leak_scan:
- auth_signing_diff_scan:
- live_order_diff_scan:
- workflow_diff_scan:
- journal_append_only_check:

artifacts:
- backup_path:
- helper_files_changed:
- validation_report_path:
- rollback_path:

safety:
- live_api_called:
- live_order_attempted: false
- cancel_attempted: false
- reorder_attempted: false
- workflow_activation_changed: false
- cron_enabled: false
- restart_attempted:
- telegram_live_send_attempted: false

blockers:
- list any blockers

next_action:
- one safe next action only
```

No secrets, raw balances, raw order payloads, Authorization headers, JWTs, API secrets, or full UUIDs may appear in telemetry or reports.

## 15. Workflows Remain Untouched And Inactive

The future helper patch must not modify:

- WF03
- WF04
- WF05
- any n8n workflow JSON
- workflow activation state
- cron state
- workflow credentials
- Telegram workflow paths
- Instagram/SNS workflows
- reel-service

Workflows remain inactive. Automation remains disabled. The helper detail endpoint is read-only reconciliation support only.

## Patch Prompt Body For Future Use

Use the following only after explicit human approval for patch execution:

```text
Implement only the additive V2 helper detail endpoint:

POST /upbit/open-orders/detail-telemetry

Scope is helper-only, read-only, reconciliation-only, append-only JSONL journaling only.

Do not modify workflows.
Do not activate workflows.
Do not enable cron.
Do not place orders.
Do not cancel orders.
Do not modify orders.
Do not reorder.
Do not add retry loops.
Do not reset the live fuse.
Do not send Telegram runtime messages.
Do not add investment decision logic.
Do not alter existing auth/signing/JWT/API-key-loading/live-order behavior.

Create a verified helper backup before editing.
Document rollback before editing.
Add only sanitized response fields.
Write only sanitized append-only JSONL journal events.
Mask UUIDs.
Never emit JWT, Authorization, API secret, raw balances, raw order payload, signing payload, full UUID, or full account identifiers.

Run offline regression tests first.
Run syntax validation.
Run forbidden endpoint scan.
Run secret leak scan.
Run auth/signing/live-order diff scan.
Run workflow diff scan.
If any check fails, STOP.

Return only sanitized telemetry and one safe next action.

STOP > EXECUTE.
```

THIS DOCUMENT DOES NOT AUTHORIZE PATCH EXECUTION; IT ONLY DEFINES THE FUTURE BOUNDED PATCH PROMPT.
