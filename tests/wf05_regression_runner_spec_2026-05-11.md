# WF05 Offline Regression Runner Specification - 2026-05-11

## 1. Purpose

Every future `WF05_Reconciliation_ReadOnly` patch must run offline fixtures first because reconciliation is a safety boundary.

WF05 must never convert ambiguous order state into action. The offline fixture runner is intended to prove that classifier behavior remains stable before any workflow, helper, logging, or observability patch is considered.

The runner is a future design only. It is not implemented by this document.

Required outcome before future WF05 runtime work:
- All fixtures pass offline.
- No network is used.
- No helper is called.
- No Upbit API is called.
- No n8n workflow is executed.
- No secrets are loaded.
- No runtime patch proceeds if any fixture fails.

## 2. Input

Fixture JSON path:

```text
tests/wf05_reconciliation_fixtures_2026-05-11.json
```

Expected top-level schema:
- `suite`: string
- `version`: string
- `mode`: must be `offline_only`
- `runtime_calls_allowed`: must be `false`
- `workflow_execution_allowed`: must be `false`
- `helper_call_allowed`: must be `false`
- `upbit_call_allowed`: must be `false`
- `fixtures`: array

Expected fixture schema:
- `id`: stable string fixture ID
- `description`: string
- `input`: object
- `expected_classification`: one of `wait`, `partial_fill`, `done`, `cancel`, `unknown_stop`

Classification input fields:
- `helper_success`
- `market`
- `open_order_exists`
- `open_order_count`
- `state`
- `executed_volume`
- `remaining_volume`
- `error_name`
- `error_message`

Required expected output field:
- `expected_classification`

## 3. Test Flow

The future runner must:

1. Load fixture JSON from disk.
2. Validate top-level fixture schema.
3. Validate every fixture has `id`, `description`, `input`, and `expected_classification`.
4. Validate fixture IDs are unique.
5. Validate no fixture contains forbidden secret-like fields.
6. Run a pure classification function against each fixture input.
7. Compare `actual_classification` against `expected_classification`.
8. Produce a deterministic PASS/FAIL report.
9. Block runtime patch if any fixture fails.

The classification function must be pure:
- No network.
- No filesystem writes during classification.
- No helper calls.
- No Upbit calls.
- No n8n runtime execution.
- No environment secret reads.

## 4. Required Cases

The runner must require all 12 existing fixtures:

1. `wf05_wait`
2. `wf05_partial_fill`
3. `wf05_done_by_state`
4. `wf05_done_by_volume`
5. `wf05_cancel`
6. `wf05_missing_state`
7. `wf05_missing_volume`
8. `wf05_malformed_numeric`
9. `wf05_negative_volume`
10. `wf05_inconsistent_done`
11. `wf05_unsupported_state`
12. `wf05_helper_error`

If any required fixture is missing, the runner must fail before classification.

## 5. Failure Policy

If any fixture fails:

- STOP.
- Do not patch runtime.
- Do not run live telemetry.
- Generate failure report.
- Require human review.

Additional failure conditions:
- Fixture JSON cannot be parsed.
- Fixture schema is invalid.
- Fixture count is below required cases.
- A required case ID is missing.
- A fixture contains forbidden fields.
- The classifier emits anything outside the approved classification set.

Approved classification set:
- `wait`
- `partial_fill`
- `done`
- `cancel`
- `unknown_stop`

## 6. Required Output Report

The future runner must produce an offline report containing:

- `timestamp_kst`
- `fixture_count`
- `passed_count`
- `failed_count`
- `failed_case_ids`
- `classifier_version`
- `safety_result`
- `next_action`

Recommended additional fields:
- `runner_mode`
- `network_used`
- `helper_called`
- `upbit_called`
- `workflow_executed`
- `secrets_loaded`
- `runtime_patch_allowed`

Required safety values for a passing report:
- `runner_mode=offline_only`
- `network_used=false`
- `helper_called=false`
- `upbit_called=false`
- `workflow_executed=false`
- `secrets_loaded=false`
- `runtime_patch_allowed=true only for separately approved future patch`

## 7. Future Implementation Rules

The future runner must be:

- offline
- deterministic
- no network
- no secrets
- no helper
- no Upbit
- no n8n runtime execution

The future runner must not:
- place orders
- cancel orders
- reorder
- enable workflow activation
- enable cron
- restart containers
- send Telegram messages
- read raw balances
- log JWT or Authorization headers
- consume API credentials

## Final Rule

Offline regression must pass before any future WF05 patch is considered.
