# Telegram Read-Only Alert Specification - 2026-05-11

## 1. Purpose

Telegram is for visibility, not execution.

Telegram alerts must help an operator understand system state, blocked reasons, and where to review reports. Telegram must not become a trading interface. It must not contain buttons or callbacks that place orders, cancel orders, retry orders, activate workflows, enable cron, or change runtime state.

Current status:
- One live order exists.
- `state=wait`
- `stale_wait=true`
- WF03/WF04 are inactive.
- Live fuse is consumed/disabled.
- Reconciliation, recovery, and persistent logging specs exist.

## 2. Allowed Alert Types

Allowed read-only alert types:

- helper health failure
- open order still waiting
- partial fill detected
- filled done detected
- canceled detected
- unknown state STOP
- duplicate block
- emergency stop block
- logging failure
- recovery ambiguity

Each alert must be informational and must preserve STOP semantics unless a future human-reviewed process explicitly changes the state outside Telegram.

## 3. Forbidden Alert Actions

The following Telegram actions are explicitly forbidden:

- Approve Trade
- Execute Trade
- Cancel Order
- Retry Order
- Rebuy
- Enable Cron
- Activate Workflow

Also forbidden:
- any callback that triggers live order execution;
- any callback that triggers cancel/reorder;
- any callback that changes workflow active state;
- any callback that starts a retry loop;
- any hidden command that changes helper, workflow, or runtime state.

## 4. Message Format

Safe Telegram message fields:

- `title`
- `severity`
- `timestamp_kst`
- `market`
- `state`
- `classification`
- `blocked_reason`
- `next_safe_action`
- `report_path`

Recommended message template:

```text
<title>
Severity: <severity>
Time KST: <timestamp_kst>
Market: <market>
State: <state>
Classification: <classification>
Blocked reason: <blocked_reason>
Next safe action: <next_safe_action>
Report: <report_path>
```

Message constraints:
- No raw balances.
- No JWT.
- No Authorization header.
- No API secret.
- No raw order payload.
- No full account identifiers.
- No full UUID in general chat messages.

## 5. Severity Levels

### INFO
Use when the system reports a normal read-only observation.

Examples:
- helper health PASS summary;
- order still waiting within expected monitoring flow;
- report generated.

### WATCH
Use when the system remains safe but needs continued observation.

Examples:
- open order still waiting;
- stale wait report-only flag;
- reconciliation pending.

### BLOCKED
Use when the system intentionally stops a workflow path.

Examples:
- duplicate block;
- emergency stop block;
- open order exists;
- logging failure blocked execution;
- missing telemetry.

### CRITICAL_STOP
Use when an operator must review before any future change.

Examples:
- unknown state STOP;
- helper unavailable during recovery;
- exchange inconsistency;
- rate-limit signal;
- recovery ambiguity.

## 6. Button Policy

Allowed buttons only:

- Open Report
- Acknowledge
- Mark Reviewed

Allowed button behavior:
- Open Report may link to a static report location or dashboard.
- Acknowledge may record that a human saw the alert, if implemented as a logging-only action.
- Mark Reviewed may record review status, if implemented as a logging-only action.

Forbidden buttons:

- trade
- cancel
- retry
- activate
- cron

Button design rules:
- No button may call an order endpoint.
- No button may call a cancel endpoint.
- No button may activate a workflow.
- No button may enable a cron or schedule.
- No button may restart a container.
- No button may mutate helper configuration.
- No button may bypass reconciliation or persistent logging.

## 7. Failure Handling

If Telegram fails:

- log failure;
- do not execute;
- do not retry infinitely;
- require human review.

Additional rules:
- Telegram failure must not block read-only local logging if local logging is available.
- Telegram failure must not trigger fallback execution.
- Telegram failure must not trigger duplicate sends in an unbounded loop.
- Telegram failure must produce a sanitized alert/error log entry.

## 8. Safe Implementation Order

1. message template only
2. dry-run render
3. write to log
4. test send to private bot only
5. no execution buttons

## Final Rule

Telegram must remain read-only. It may inform, acknowledge, and link to reports, but it must never trade, cancel, retry, activate, enable cron, or change runtime state.
