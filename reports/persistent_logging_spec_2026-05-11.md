# Persistent Logging Specification - 2026-05-11

## 1. Purpose

`staticData` alone is insufficient for safe trading automation.

n8n workflow static data is useful for local workflow state, but it is not enough as the system of record. It can be incomplete after import/export, ambiguous after restart, hard to audit externally, and insufficient for durable recovery. A trading system needs an append-only external audit trail that survives workflow edits, container restarts, EC2 recovery, staticData reset, and operator handoff.

Persistent logging must provide:
- durable evidence of every decision and block;
- reconstruction of duplicate/fuse/reconciliation state;
- proof that forbidden endpoints were not called;
- safe operator review without exposing secrets;
- recovery support after restart or interruption.

No execution should proceed without a persistent audit trail.

## 2. Required Log Categories

### precheck log
Purpose:
- Record input intent, precheck gates, read-only telemetry, and STOP/pass decision.

Examples:
- order shape validation;
- emergency stop state;
- duplicate lock state;
- account sufficiency band;
- open-order result.

### execution attempt log
Purpose:
- Record any dry-run trace, order-test trace, or explicitly authorized live attempt.

Examples:
- one-time fuse state;
- execution gate result;
- order-test telemetry;
- live attempt accepted/rejected telemetry.

### block log
Purpose:
- Record every STOP decision.

Examples:
- open order exists;
- duplicate state active or uncertain;
- helper unavailable;
- telemetry missing;
- stale wait;
- unknown state.

### reconciliation log
Purpose:
- Record read-only classification of exchange order lifecycle.

Examples:
- wait;
- partial_fill;
- done;
- cancel;
- unknown_stop.

### recovery log
Purpose:
- Record restart/recovery validations and decisions.

Examples:
- helper health after restart;
- workflow inactive check;
- fuse state recovered or uncertain;
- duplicate state recovered or uncertain.

### alert log
Purpose:
- Record read-only alert emission or skipped alert decision.

Examples:
- alert dry-run generated;
- Telegram not ready;
- alert blocked because live send not allowed.

### error log
Purpose:
- Record sanitized errors from helper, n8n, exchange telemetry, or local validation.

Examples:
- rate limited;
- auth failed;
- malformed telemetry;
- timeout;
- missing required fields.

### operator action log
Purpose:
- Record human decisions and approvals without embedding secrets.

Examples:
- operator approved one-time live attempt;
- operator requested read-only monitoring;
- operator requested documentation-only design.

## 3. Required Fields

Every log category should use this base schema where applicable:

- `timestamp_kst`
- `run_id`
- `workflow_name`
- `phase`
- `market`
- `side`
- `ord_type`
- `action`
- `result`
- `blocked_reason`
- `open_order_exists`
- `open_order_count`
- `order_state`
- `remaining_volume`
- `executed_volume`
- `duplicate_key`
- `fuse_state`
- `emergency_stop`
- `helper_health`
- `api_status`
- `forbidden_endpoint_check`
- `secrets_leak_check`

Recommended category-specific additions:

- Precheck log: `order_size_status`, `krw_balance_sufficient`, `krw_available_band`, `account_check_status`.
- Execution attempt log: `dry_run_blocked`, `order_test_passed`, `live_order_attempted`, `live_order_accepted`, `live_path_auto_disabled`.
- Block log: `stop_code`, `reason_codes`, `stop_stage`, `human_review_required`.
- Reconciliation log: `uuid_masked`, `created_at`, `trades_count`, `paid_fee_available`, `locked_available`, `classification`.
- Recovery log: `recovery_event`, `workflow_inactive`, `duplicate_state_recovered`, `fuse_state_recovered`, `state_uncertain`.
- Alert log: `alert_channel`, `alert_mode`, `alert_sent`, `alert_blocked_reason`, `action_buttons_present`.
- Error log: `error_name`, `error_message_sanitized`, `http_status`, `rate_limit_signal`.
- Operator action log: `operator_request`, `approval_scope`, `approval_expires_at`, `action_performed`.

## 4. Forbidden Log Data

Never log:

- JWT.
- Authorization header.
- API secret.
- Raw account balances.
- Raw order payload.
- Full account identifiers.
- Full API key.
- Full order UUID in general reports.
- Full wallet or deposit/withdrawal details.
- Telegram bot token.
- Telegram chat ID unless explicitly masked.

If a field is needed for correlation, log a masked version or write the full value only to a future approved secure internal store.

## 5. Storage Options

| Option | Strengths | Weaknesses | Fit |
| --- | --- | --- | --- |
| Local JSONL | Simple, append-only, easy to inspect, no external dependency | Host-local durability only; needs backup/rotation | Best minimum safe V1 |
| Google Sheets | Human-readable, easy review, simple sharing | API auth complexity; rate limits; accidental edits; external dependency | Good later for operator dashboards |
| GitHub committed logs | Versioned and reviewable | Risk of committing sensitive data; noisy commits; unsuitable for high-frequency logs | Use only for sanitized summaries/specs, not raw operational logs |
| SQLite | Durable local database, transactional, queryable | Needs schema migration and backup policy | Good V1.5/V2 when local JSONL becomes limiting |
| Postgres later | Strong durability, concurrent access, queryability, retention controls | More operational overhead | Best future production-grade store |

## 6. Minimum Safe V1 Recommendation

Recommended V1 path:

- Use local append-only JSONL files on the n8n host or a dedicated mounted logging path.
- Write one JSON object per event.
- Keep logs sanitized.
- Rotate by date.
- Mirror daily summaries into `reports/` for human handoff.
- Do not enable automation as part of logging implementation.

Minimum V1 file layout:

```text
kbia-logs/
  precheck/YYYY-MM-DD.jsonl
  execution/YYYY-MM-DD.jsonl
  block/YYYY-MM-DD.jsonl
  reconciliation/YYYY-MM-DD.jsonl
  recovery/YYYY-MM-DD.jsonl
  alert/YYYY-MM-DD.jsonl
  error/YYYY-MM-DD.jsonl
  operator/YYYY-MM-DD.jsonl
```

Minimum V1 rule:
- If the append-only log write fails, STOP.

## 7. Failure Handling

If persistent logging fails:

- STOP.
- Do not execute.
- Do not place a live order.
- Do not cancel.
- Do not reorder.
- Do not retry execution.
- Emit a local fallback report if possible.
- Require human review.

Fallback report requirements:
- sanitized fields only;
- explicit `logging_failed=true`;
- explicit `execution_allowed=false`;
- explicit blocked reason;
- no secrets or raw payloads.

Logging failure must never be treated as non-critical.

## 8. Final Rule

No execution without persistent audit trail.
