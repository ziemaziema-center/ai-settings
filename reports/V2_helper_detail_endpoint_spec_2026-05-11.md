# V2 Helper Detail Endpoint Specification

Date: 2026-05-11  
Mode: Documentation-only, additive-only  
Runtime status: Controlled STOP state  

## 1. Endpoint Purpose

The V2 helper detail endpoint exists to improve read-only reconciliation visibility after SAFE LIMITED LIVE EXECUTION V1.

Current helper telemetry is sufficient for summary monitoring, but V2 reconciliation needs richer sanitized order detail to classify lifecycle state, detect duplicate risk, support append-only journaling, and preserve controlled STOP behavior.

The helper may read and summarize order/account detail. The helper must not place, cancel, modify, retry, reorder, activate, or decide any investment action.

## 2. Endpoint Name And Path Proposal

Proposed endpoint:

```text
POST /upbit/open-orders/detail-telemetry
```

This is the only proposed endpoint for the first V2 helper enhancement. It must be additive only and must not change any existing helper endpoint behavior.

## 3. Request Schema

Proposed request body:

```json
{
  "market": "KRW-BTC",
  "run_id": "safe-operator-generated-id",
  "include_recent_closed": true,
  "recent_closed_limit": 20,
  "journal_enabled": true,
  "correlation_hint": {
    "market": "KRW-BTC",
    "side": "bid",
    "ord_type": "limit",
    "created_at": "2026-05-10T12:46:37+09:00"
  }
}
```

Required fields:

- `market`

Optional fields:

- `run_id`
- `include_recent_closed`
- `recent_closed_limit`
- `journal_enabled`
- `correlation_hint.market`
- `correlation_hint.side`
- `correlation_hint.ord_type`
- `correlation_hint.created_at`

Forbidden request fields:

- raw JWT
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

## 4. Response Schema

Proposed response body:

```json
{
  "success": true,
  "endpoint": "/upbit/open-orders/detail-telemetry",
  "mode": "read_only_detail_telemetry",
  "market": "KRW-BTC",
  "open_order_exists": false,
  "open_order_count": 0,
  "duplicate_order_exists": false,
  "new_order_created_detected": false,
  "orders": [
    {
      "uuid_masked": "abcd...wxyz",
      "market": "KRW-BTC",
      "side": "bid",
      "ord_type": "limit",
      "state": "wait",
      "created_at": "2026-05-10T12:46:37+09:00",
      "remaining_volume": "0.0001",
      "executed_volume": "0",
      "trades_count": 0,
      "paid_fee": "0",
      "locked": "10000",
      "price": "100000000",
      "classification": "wait"
    }
  ],
  "classification_summary": {
    "final_classification": "wait",
    "blocked_reason": null,
    "next_safe_action": "remain_stopped"
  },
  "journal_write": {
    "attempted": true,
    "success": true,
    "path_masked": "order_journal/2026-05-11.jsonl"
  },
  "forbidden_endpoint_check": true,
  "secrets_leak_check": true
}
```

Error responses must use the same sanitized top-level shape with `success=false`, `classification_summary.final_classification=unknown_stop`, and a safe `blocked_reason`.

## 5. Allowed Read-Only Data Fields

Allowed fields:

- `market`
- `side`
- `ord_type`
- `state`
- `created_at`
- `remaining_volume`
- `executed_volume`
- `trades_count`
- `paid_fee`
- `locked`
- `price`
- `uuid_masked`
- `open_order_exists`
- `open_order_count`
- `duplicate_order_exists`
- `classification`
- `blocked_reason`
- `next_safe_action`
- safe helper status
- safe rate-limit metadata if available

All numeric values may be returned as strings to preserve exchange precision. Full UUID must not be returned; only masked UUID is allowed.

## 6. Explicitly Forbidden Mutation Fields And Actions

The endpoint must not accept, generate, infer, or execute any mutation action.

Forbidden actions:

- place order
- cancel order
- modify order
- reorder
- retry execution
- withdraw
- reset live fuse
- enable cron
- activate workflow
- send Telegram runtime message
- decide investment action

Forbidden endpoint usage:

- live-order endpoint
- cancel endpoint
- reorder endpoint
- withdrawal endpoint
- any exchange mutation endpoint
- any n8n workflow activation endpoint
- any Telegram send endpoint

Forbidden output fields:

- JWT
- Authorization header
- API secret
- raw balances
- raw order payload
- signing payload
- full UUID
- full account identifiers

## 7. Reconciliation Use Cases

The endpoint supports these read-only reconciliation use cases:

- confirm `open_order_exists=false`
- confirm `open_order_exists=true`
- classify `wait`
- classify `partial_fill`
- classify `done`
- classify `cancel`
- classify `unknown_stop`
- detect possible duplicate open orders for the same market/side/order type
- confirm no new order was created after controlled stop
- provide safe journal evidence for operator review
- support stale-wait escalation as report-only state

The endpoint must not act on any classification. Reconciliation is classification and evidence only.

## 8. Append-Only JSONL Journal Behavior

The approved storage direction is local append-only JSONL on the n8n host mounted logging path.

Journal behavior:

- write one sanitized JSON object per line
- append only
- no overwrite
- no delete
- no update-in-place
- no raw exchange payload
- no secrets
- no full UUID
- no order/cancel/retry commands

Suggested journal event shape:

```json
{
  "timestamp_kst": "2026-05-11T00:00:00+09:00",
  "run_id": "safe-operator-generated-id",
  "source": "upbit-helper",
  "endpoint": "/upbit/open-orders/detail-telemetry",
  "market": "KRW-BTC",
  "open_order_exists": false,
  "open_order_count": 0,
  "duplicate_order_exists": false,
  "state": "cancel",
  "remaining_volume": "0",
  "executed_volume": "0",
  "classification": "cancel",
  "blocked_reason": null,
  "forbidden_endpoint_check": true,
  "secrets_leak_check": true,
  "next_safe_action": "remain_stopped"
}
```

If journal writing fails, the endpoint must return a blocked read-only failure state. No execution path may continue without a persistent audit trail.

## 9. Journal And Lock Path Requirements

Required future configuration:

- journal path must be mounted and persistent outside ephemeral container storage
- lock path must be mounted and persistent outside ephemeral container storage
- paths must be explicitly configured
- paths must not expose secrets
- permissions must allow append-only logging by the helper process
- daily rotation is allowed only by creating new files, not rewriting existing files

Suggested environment names for future design discussion:

- `KBIA_ORDER_JOURNAL_DIR`
- `KBIA_EXECUTION_LOCK_DIR`

These names are specification placeholders only. This document does not approve changing environment, Docker, or runtime configuration.

## 10. Timeout Behavior

The endpoint must use bounded read-only request timeouts.

Required behavior:

- no unbounded waits
- no infinite retry loop
- no execution fallback
- no cancel fallback
- no reorder fallback
- timeout classifies as `unknown_stop`
- timeout writes a sanitized failure journal event if journaling is available

Recommended initial timeout target:

- one bounded read-only exchange request with a 10 to 15 second ceiling

## 11. Error Response Behavior

All errors must be sanitized.

Required error fields:

- `success=false`
- `market`
- `classification_summary.final_classification=unknown_stop`
- `blocked_reason`
- `forbidden_endpoint_check`
- `secrets_leak_check`

Allowed error names:

- `HELPER_DETAIL_TIMEOUT`
- `HELPER_DETAIL_RATE_LIMITED`
- `HELPER_DETAIL_TELEMETRY_MISSING`
- `HELPER_DETAIL_TELEMETRY_MALFORMED`
- `HELPER_DETAIL_JOURNAL_WRITE_FAILED`
- `HELPER_DETAIL_UNKNOWN_STOP`

Forbidden error output:

- raw response payload
- raw request payload
- Authorization header
- JWT
- API secret
- full account details
- full UUID

## 12. Idempotency Expectations

The endpoint must be idempotent with respect to exchange and workflow state.

Repeated calls may append repeated journal observations, but must not:

- create an order
- cancel an order
- modify an order
- change live fuse state
- change workflow activation state
- change cron state
- send Telegram messages

If `run_id` is supplied, it is used only for correlation. It must not unlock execution or mutate prior records.

## 13. Security Boundaries

Security boundaries:

- existing JWT/signing/auth internals must remain isolated
- no secret-bearing values may be returned to callers
- no secret-bearing values may be written to journal
- full UUID must be masked
- raw balances must not be logged or returned
- raw order payload must not be logged or returned
- signing payloads must not be logged or returned
- helper must not decide investment action

Any future diff that touches auth, signing, key loading, live-order behavior, or mutation endpoints must be rejected for this endpoint scope.

## 14. Rate-Limit Handling

Rate-limit handling must be read-only and fail-safe.

Required behavior:

- detect Upbit rate-limit response if available
- return sanitized `HELPER_DETAIL_RATE_LIMITED`
- classify as `unknown_stop`
- append sanitized blocked journal entry if possible
- do not retry in a loop
- do not call fallback mutation endpoints
- require human review before further runtime work

## 15. Failure Handling Path

All failure paths must stop safely.

Failure conditions:

- helper detail timeout
- helper unavailable
- exchange read timeout
- rate limit
- malformed numeric telemetry
- missing state
- inconsistent volume
- journal write failure
- duplicate ambiguity
- unexpected endpoint response
- secret leak scan failure
- forbidden endpoint scan failure

Required outcome:

- classify `unknown_stop`
- emit sanitized blocked response
- append safe journal entry if possible
- do not place, cancel, reorder, retry, activate, enable cron, reset fuse, or send Telegram

## 16. Required Offline Tests

Before any helper patch prompt is drafted, the future implementation plan must require offline tests for:

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

Offline tests must use no network, no helper runtime, no Upbit call, no n8n runtime execution, and no secrets.

## 17. Required Review Checklist Before Helper Patch Prompt

Before drafting any future helper patch prompt, the operator must confirm:

- explicit human approval exists for helper detail endpoint implementation
- helper backup path exists
- rollback method is documented
- diff scope is additive endpoint only
- no signing function change
- no auth header creation change
- no API key loading change
- no live-order endpoint change
- no cancel/reorder/withdrawal strings introduced
- no Docker/runtime config change without separate approval
- no workflow patch
- no Telegram send path
- offline fixtures pass
- secret leak scan passes
- forbidden endpoint scan passes
- expected journal path is defined and approved
- failure behavior returns STOP, not fallback execution

If any checklist item fails, do not draft the helper patch prompt.

## 18. Conditions That Must Remain Blocked After This Spec

This specification does not unblock runtime work.

Still blocked:

- helper patch without explicit future implementation approval
- workflow patch
- WF03 activation
- WF04 activation
- WF05 activation
- cron enablement
- live order
- second order
- cancel
- reorder
- withdrawal
- Telegram runtime send
- live fuse reset
- autonomous investment decision
- automatic retry loop
- automatic cancel/reprice loop
- V2 live execution discussion without complete safety validation

THIS SPEC DOES NOT APPROVE IMPLEMENTATION; IT ONLY DEFINES THE REQUIRED CONTRACT FOR A FUTURE HELPER PATCH PROMPT.
