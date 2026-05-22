# Restart Recovery Matrix - 2026-05-11

## 1. Purpose

Restart safety is mandatory before automation.

The system has already proven a limited live execution path, but production automation cannot be considered until restart and recovery behavior is explicitly safe. A restart, reboot, network interruption, helper outage, or state-store reset must never cause hidden execution, duplicate orders, automatic cancellation, or automatic resume.

Current status:
- One live order exists.
- `state=wait`
- `open_order_exists=true`
- `stale_wait=true`
- WF03/WF04 are inactive.
- Live fuse is consumed/disabled.
- Restart testing is currently blocked for safety.

This document is design only. It does not authorize restart testing, workflow activation, cron enablement, cancel behavior, reorder behavior, or any live order action.

## 2. Failure Scenarios

### n8n restart
Safe handling:
- Assume workflow static state may be incomplete until proven otherwise.
- Verify WF03/WF04 remain inactive.
- Verify no startup trigger or cron became active.
- Re-read open orders before any execution decision.
- STOP if workflow active state, static data, or execution history is ambiguous.

### helper restart
Safe handling:
- Verify helper `/health`.
- Verify auth with read-only telemetry only.
- Re-read open orders through helper.
- STOP if helper health, auth, or telemetry is unavailable.

### Docker container restart
Safe handling:
- Treat any restarted `n8n` or `upbit-helper` container as a recovery event.
- Re-run read-only health and telemetry checks.
- Verify no workflow activation changed.
- STOP until duplicate, fuse, and reconciliation state are understood.

### EC2 reboot
Safe handling:
- Treat as full recovery mode.
- Confirm all relevant containers are present and expected.
- Confirm workflows remain inactive.
- Confirm helper health.
- Re-read open orders before any future enablement.
- STOP if any service, state, or workflow status is unknown.

### network interruption
Safe handling:
- Do not infer order state from missing data.
- Do not retry execution.
- Do not cancel.
- Retry policy, if later implemented, must be read-only, bounded, and rate-limit aware.
- STOP until read-only telemetry is restored.

### helper unavailable
Safe handling:
- STOP.
- Do not fall back to n8n-side JWT signing.
- Do not call Upbit directly from n8n.
- Do not execute based on cached state.

### telemetry timeout
Safe handling:
- STOP.
- Mark telemetry as missing.
- Do not assume wait, done, cancel, or fill.
- Do not place, cancel, reorder, or retry execution.

### stale open order state
Safe handling:
- Classify as report-only stale wait.
- STOP.
- Continue read-only monitoring or future human-reviewed alerting.
- Do not auto-cancel.
- Do not place replacement or second order.

### partial telemetry corruption
Safe handling:
- STOP.
- Treat corrupted or contradictory fields as `unknown_stop`.
- Do not derive finality from partial data.
- Archive sanitized error context only.

### duplicate lock loss
Safe handling:
- STOP.
- Reconstruct safely only from durable execution history and exchange state.
- Do not assume lock is clear because static data is empty.
- Do not execute until duplicate protection is re-established.

### staticData reset
Safe handling:
- STOP.
- Treat fuse and duplicate state as uncertain.
- Re-read exchange state.
- Require durable recovery evidence before any future human-reviewed enablement.

## 3. Required Recovery Checks

Required validations after any restart or recovery event:

- Workflows remain inactive.
- Live fuse state is preserved, or uncertainty is classified as STOP.
- Duplicate protection is preserved or reconstructed safely.
- Open orders are re-read before any execution path is considered.
- Emergency stop defaults safe.
- Unknown state forces STOP.
- Missing state forces STOP.
- Helper health is PASS.
- Auth validation succeeds through read-only helper telemetry.
- No workflow gained cron/schedule activation.
- No queued or startup execution is pending.
- No raw secret, JWT, Authorization header, raw balance, or raw order payload is logged.

## 4. Recovery Decision Table

| Condition | Action |
| --- | --- |
| `open_order_exists=true` | STOP |
| Missing telemetry | STOP |
| Duplicate state uncertain | STOP |
| Helper unavailable | STOP |
| State mismatch | STOP |
| Runtime ambiguity | STOP |
| Workflow active unexpectedly | STOP |
| Cron or schedule present unexpectedly | STOP |
| Live fuse missing or uncertain | STOP |
| Static data reset detected | STOP |
| Network interruption during recovery | STOP |
| Telemetry timeout | STOP |
| Partial telemetry corruption | STOP |
| Unknown exchange state | STOP |
| Rate limit or temporary ban signal | STOP |
| Reconciliation not completed | STOP |
| All recovery checks passed and no open order exists | Human-reviewed enablement only |

## 5. Safe Startup Order

Future safe startup sequence:

1. helper health
2. auth validation
3. read-only telemetry
4. open-order reconciliation
5. duplicate-lock validation
6. fuse validation
7. workflow inactive validation
8. only then human-reviewed enablement

No step in this startup order may place, cancel, reorder, retry execution, activate workflows, enable cron, or send Telegram action buttons.

## 6. Required Future Persistence

The following state must be durably persisted before limited automation can be considered:

- Duplicate state.
- Fuse state.
- Reconciliation state.
- Execution history.
- Audit logs.
- Blocked reasons.
- Last known order correlation key.
- Last known exchange state.
- Last known recovery decision.

Persistence requirements:
- Append-only audit history.
- Sanitized fields only.
- Masked order identifiers in general reports.
- Full identifiers only in an approved secure internal store if needed.
- Recovery must treat missing persistence as STOP, not clear.

## 7. Explicitly Forbidden Recovery Behavior

Do not build or allow:

- Auto resume trading.
- Auto retry after reboot.
- Hidden startup execution.
- Startup cron execution.
- Auto cancel on recovery.
- Auto rebuy on recovery.
- Execution before reconciliation.
- Execution when duplicate state is uncertain.
- Execution when fuse state is uncertain.
- Execution while any open order exists.
- Execution from cached pre-restart state.
- Cancel-replace loops after restart.
- Telegram buttons that execute, cancel, retry, or replace orders during recovery.

## 8. Final Recovery Principle

When uncertain after restart, remain stopped.
