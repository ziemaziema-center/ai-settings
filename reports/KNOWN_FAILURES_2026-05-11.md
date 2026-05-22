# Upbit V1 Known Failures Registry - 2026-05-11

## Purpose

This registry records recurring failure modes and unresolved safety risks for Upbit Investment Automation V1.

Current system posture:
- Runtime unchanged by this document.
- Open order still waiting.
- Workflows inactive.
- Live fuse consumed/disabled.
- Documentation/read-only work only.

Known failures must be reviewed before any runtime patch.

## 1. Failure ID Format

Failure IDs use the format:

```text
UF-001
UF-002
UF-003
```

Rules:
- Prefix: `UF` for Upbit Failure.
- Numeric suffix: three digits.
- IDs are stable once assigned.
- New recurring risks must receive the next unused ID.

## 2. Severity Definitions

### LOW

Low operational risk. Does not directly affect execution safety, cancellation safety, secret handling, or recovery integrity.

### WATCH

Requires operator attention and continued monitoring. Does not currently permit action, but may become unsafe if combined with missing telemetry or unclear state.

### HIGH

Material safety risk. Blocks related runtime patches until mitigated and validated.

### CRITICAL_STOP

Immediate stop condition. No execution, cancel, retry, activation, cron, or autonomous action is allowed while this condition is active or unresolved.

## 3. Required Fields Per Failure

Every failure entry must include:

- `id`
- `title`
- `description`
- `risk`
- `severity`
- `current_state`
- `mitigation`
- `blocked_actions`
- `future_validation_needed`

## 4. Current Known Failures And Risks

### UF-001

id:
- UF-001

title:
- Restart recovery ambiguity

description:
- Restart safety has not been runtime-validated for n8n, helper, Docker container restart, or EC2 reboot while an open order exists.

risk:
- Duplicate loss / unintended execution.

severity:
- CRITICAL_STOP

current_state:
- unresolved

mitigation:
- Keep workflows inactive.
- Keep live fuse disabled.
- Do not restart for validation while unrelated runtime impact is uncertain.
- Require read-only recovery design and human-reviewed validation before any restart test.

blocked_actions:
- Runtime restart.
- Workflow activation.
- Cron enablement.
- Live order.
- Retry after reboot.
- Automation enablement.

future_validation_needed:
- Validate helper restart behavior safely.
- Validate n8n restart behavior safely.
- Confirm live fuse state after restart.
- Confirm duplicate protection is preserved or safely reconstructed.
- Confirm open orders are re-read before any execution path.

### UF-002

id:
- UF-002

title:
- Stale open order wait state

description:
- A live KRW-BTC limit bid order remains in `wait` state with unchanged `remaining_volume=0.0001` and `executed_volume=0`.

risk:
- Reconciliation uncertainty.

severity:
- CRITICAL_STOP

current_state:
- active

mitigation:
- Continue read-only open-order monitoring.
- Do not place a second order while `open_order_exists=true`.
- Do not cancel unless a controlled cancel flow is separately designed and explicitly approved.

blocked_actions:
- Second order.
- Cancel.
- Reorder.
- Retry.
- Workflow activation.
- Automation enablement.

future_validation_needed:
- Build read-only reconciliation engine.
- Validate state classification for wait, partial_fill, done, cancel, and unknown_stop.
- Validate stale-wait reporting without action.
- Validate finality conditions before any future execution.

### UF-003

id:
- UF-003

title:
- Helper transport-unavailable path lacks structured safe log

description:
- The safe rehearsal found that helper transport-unavailable failure does not currently emit a complete structured downstream safe log node.

risk:
- Invisible failure state.

severity:
- HIGH

current_state:
- unresolved

mitigation:
- Treat helper unavailable as STOP.
- Require local fallback report if logging fails.
- Do not execute when helper health or telemetry is missing.

blocked_actions:
- Execution during helper unavailable state.
- Retry loop.
- Automation enablement.
- Production readiness claim.

future_validation_needed:
- Add read-only structured logging for helper-unavailable path after safety gate approval.
- Validate no order/cancel endpoint is reachable during helper failure.
- Validate failure is visible in persistent audit logs.

### UF-004

id:
- UF-004

title:
- Duplicate workflow naming ambiguity

description:
- Workflow naming or duplicate workflow copies can create ambiguity about which workflow is safe to inspect, patch, run, or activate.

risk:
- Wrong workflow modification.

severity:
- HIGH

current_state:
- unresolved

mitigation:
- Do not touch unrelated workflows.
- Confirm exact workflow identity before any future workflow read-only or runtime patch.
- Preserve backups before any approved workflow change.

blocked_actions:
- Workflow patch without exact identity confirmation.
- Workflow activation.
- Cron enablement.
- Touching Instagram/SNS or reel-service workflows.

future_validation_needed:
- Create workflow identity inventory.
- Confirm WF03 and WF04 IDs, names, active state, and latest safe versions.
- Validate no duplicate active workflow can execute unexpectedly.

### UF-005

id:
- UF-005

title:
- No production-grade reconciliation engine yet

description:
- Execution acceptance is not the same as order completion. The system has monitoring logs and design specs, but no production-grade reconciliation runtime has been implemented or validated.

risk:
- Execution != completion mismatch.

severity:
- CRITICAL_STOP

current_state:
- unresolved

mitigation:
- Keep system in controlled STOP state.
- Use read-only monitoring and documentation only.
- Require reconciliation implementation after open-order resolution or explicit read-only approval.

blocked_actions:
- Automation enablement.
- Additional live execution.
- Portfolio state update based only on order acceptance.
- Profit logic.

future_validation_needed:
- Implement read-only reconciliation first.
- Validate order lifecycle classification.
- Validate missing, inconsistent, or unknown telemetry forces STOP.
- Validate persistent reconciliation logging.

### UF-006

id:
- UF-006

title:
- No runtime-tested Telegram alert path

description:
- Telegram read-only alert design exists, but the live alert runtime path has not been validated for safe visibility-only behavior.

risk:
- Invisible critical stop.

severity:
- HIGH

current_state:
- unresolved

mitigation:
- Do not send Telegram live messages in the current phase.
- Do not add trade, cancel, retry, activate, or cron buttons.
- Use report/log artifacts as the current visibility layer.

blocked_actions:
- Telegram live send.
- Telegram execution buttons.
- Telegram cancel/retry buttons.
- Alert-driven runtime action.

future_validation_needed:
- Validate message template only.
- Validate dry-run render.
- Validate write-to-log behavior.
- Test private bot send only after explicit approval.
- Confirm Telegram failure logs safely and does not execute.

### UF-007

id:
- UF-007

title:
- Persistent state durability not fully validated

description:
- Duplicate state, fuse state, reconciliation state, execution history, and blocked reasons are not yet fully validated in durable external storage.

risk:
- Restart inconsistency.

severity:
- CRITICAL_STOP

current_state:
- unresolved

mitigation:
- Do not rely on staticData alone for production automation.
- Keep workflows inactive.
- Require external persistent logging before execution automation.

blocked_actions:
- Automation enablement.
- Retry after restart.
- Execution without audit trail.
- Runtime patch that depends only on volatile or ambiguous state.

future_validation_needed:
- Validate durable duplicate state.
- Validate durable fuse state.
- Validate reconciliation history.
- Validate execution and blocked-reason audit trail.
- Validate fallback report when external logging fails.

## 5. Final Rule

Known failures must be reviewed before any runtime patch.
