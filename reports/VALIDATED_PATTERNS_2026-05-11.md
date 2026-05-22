# Upbit V1 Validated Patterns Registry - 2026-05-11

## Purpose

This registry documents patterns that were successfully validated during SAFE LIMITED LIVE EXECUTION V1.

Current system posture:
- Runtime unchanged by this document.
- Open order still waiting.
- Workflows inactive.
- Live fuse consumed/disabled.
- Documentation/read-only work only.

Prefer validated patterns over new untested runtime behavior.

## 1. Pattern ID Format

Pattern IDs use the format:

```text
VP-001
VP-002
VP-003
```

Rules:
- Prefix: `VP` for Validated Pattern.
- Numeric suffix: three digits.
- IDs are stable once assigned.
- New validated patterns must receive the next unused ID.
- Existing root-level `VALIDATED_PATTERNS.md` remains the baseline memory file; this report is the SAFE LIMITED LIVE EXECUTION V1 registry snapshot.

## 2. Validation Levels

### EXPERIMENTAL

Observed or designed, but not enough evidence exists for operational reliance.

### VALIDATED

Successfully exercised in the current safe operating context with expected behavior and no uncontrolled side effect.

### STRONGLY_VALIDATED

Exercised repeatedly or across multiple relevant paths with consistent expected behavior and no uncontrolled side effect.

## 3. Required Fields Per Pattern

Every validated pattern entry must include:

- `id`
- `title`
- `description`
- `validation_result`
- `validation_reason`
- `operational_benefit`
- `safe_usage_conditions`
- `forbidden_usage_conditions`
- `future_revalidation_needed`

## 4. Validated Patterns

### VP-001

id:
- VP-001

title:
- Helper microservice architecture

description:
- Upbit auth/JWT signing is isolated inside `upbit-helper`; n8n workflows call helper telemetry endpoints and do not create JWTs directly.

validation_result:
- VALIDATED

validation_reason:
- JWT isolation successful.
- Helper health, auth telemetry, accounts telemetry, open-order telemetry, order-test telemetry, and one-time live helper path were validated with sanitized outputs.

operational_benefit:
- Keeps secrets and signing logic outside n8n Code nodes.
- Reduces workflow exposure to JWT, Authorization headers, and raw Upbit payloads.
- Provides a clean boundary for sanitized telemetry.

safe_usage_conditions:
- Helper returns sanitized telemetry only.
- n8n calls helper endpoints only.
- JWT, Authorization headers, API secrets, raw balances, and raw order payloads are never logged.
- Helper unavailable state forces STOP.

forbidden_usage_conditions:
- n8n direct JWT signing.
- Returning JWT or Authorization headers from helper.
- Logging raw balances or raw order payloads.
- Bypassing helper for live Upbit private endpoints.

future_revalidation_needed:
- Revalidate after any helper code change.
- Revalidate after restart/recovery testing.
- Revalidate before production automation.

### VP-002

id:
- VP-002

title:
- One-time live fuse

description:
- WF04 live path uses a one-time manual fuse that is consumed before the helper live HTTP call and auto-disables the live path after use.

validation_result:
- VALIDATED

validation_reason:
- Live path auto-disabled correctly.
- One manual KRW-BTC limit bid order was accepted, the fuse was consumed, and no retry was attempted.

operational_benefit:
- Prevents accidental repeated live execution.
- Makes one-time live execution auditable and bounded.
- Keeps subsequent runs blocked after the allowed attempt is consumed.

safe_usage_conditions:
- Workflow remains inactive and manual-trigger only.
- Live flags must be explicit.
- `one_time_live_attempt_allowed` must be true only for the approved attempt.
- Open-order, duplicate-lock, system-stop, order-test, and order-shape gates must pass before the helper live path.

forbidden_usage_conditions:
- Resetting the fuse while an open order exists.
- Adding retries around the live path.
- Enabling cron or workflow activation for live execution.
- Reusing the fuse as a loop or automation control.

future_revalidation_needed:
- Revalidate fuse persistence after restart.
- Revalidate duplicate/fuse interaction with external persistent logging.
- Revalidate only after the current open order resolves and safety gate permits runtime work.

### VP-003

id:
- VP-003

title:
- Workflow inactive default

description:
- WF03 and WF04 remain inactive and manual-trigger only during the safe V1 operating mode.

validation_result:
- STRONGLY_VALIDATED

validation_reason:
- No unintended execution occurred.
- Multiple read-only checks confirmed workflows remained inactive while monitoring and documentation proceeded.

operational_benefit:
- Prevents scheduler-driven or automatic trading behavior.
- Keeps live execution under explicit human control.
- Reduces risk while open-order, reconciliation, and recovery gaps remain unresolved.

safe_usage_conditions:
- Workflows remain inactive.
- No cron or schedule nodes are enabled.
- Manual execution is used only for explicitly scoped validation.
- Workflow activation state is checked before high-risk work.

forbidden_usage_conditions:
- Activating WF03/WF04 during open-order state.
- Enabling cron or hidden schedules.
- Creating loops that can call execution paths.
- Assuming inactive workflow state after restart without validation.

future_revalidation_needed:
- Revalidate after n8n restart.
- Revalidate before any workflow patch.
- Revalidate before any future enablement discussion.

### VP-004

id:
- VP-004

title:
- Duplicate lock pattern

description:
- Duplicate lock state blocks repeat exposure for the same `market|side|ord_type` tuple and is treated as a STOP condition when active or uncertain.

validation_result:
- VALIDATED

validation_reason:
- No duplicate order observed.
- Duplicate protection state was inspected during the safe rehearsal and treated as part of the STOP posture.

operational_benefit:
- Reduces risk of repeated orders for the same market and side.
- Provides a separate protection layer beyond open-order telemetry.
- Supports additive failure-path documentation.

safe_usage_conditions:
- Duplicate key is explicit and stable.
- Duplicate state is checked before any execution path.
- Uncertain duplicate state forces STOP.
- Duplicate behavior is reconciled with open-order telemetry.

forbidden_usage_conditions:
- Ignoring duplicate state when open order exists.
- Clearing duplicate state without human-approved recovery logic.
- Using staticData-only duplicate state for production automation.
- Executing when duplicate state is missing or ambiguous.

future_revalidation_needed:
- Revalidate persistence after restart.
- Revalidate with external durable logging.
- Revalidate against duplicate workflow naming ambiguity.

### VP-005

id:
- VP-005

title:
- Read-only monitoring flow

description:
- Open-order monitoring reads helper health and sanitized KRW-BTC open-order telemetry, compares against prior logs, classifies state, and writes safe monitor/report artifacts without action.

validation_result:
- STRONGLY_VALIDATED

validation_reason:
- Multiple safe monitoring passes completed.
- Four monitor checks and a consolidated summary confirmed `wait`, unchanged remaining volume, unchanged executed volume, and `still_waiting_safe_stop`.

operational_benefit:
- Provides visibility while preserving STOP state.
- Separates observation from execution.
- Creates safe artifacts for later reconciliation design.

safe_usage_conditions:
- Read-only helper endpoints only.
- No cancel, reorder, retry, or live order calls.
- No Telegram live send.
- Monitor logs exclude secrets, raw balances, raw order payloads, and full UUIDs.

forbidden_usage_conditions:
- Acting automatically on stale-wait.
- Triggering cancel/reorder based on monitoring.
- Turning monitor checks into a retry loop.
- Using monitoring classification as permission to trade.

future_revalidation_needed:
- Revalidate after helper or network interruption.
- Revalidate once order state changes from wait.
- Revalidate parser against partial_fill, done, cancel, and unknown_stop.

### VP-006

id:
- VP-006

title:
- Dry-run isolation

description:
- Default workflow execution mode remains dry-run with live execution disabled unless explicit gates are intentionally set for a one-time manual live path.

validation_result:
- VALIDATED

validation_reason:
- No bleed into live execution.
- WF04 dry-run defaults remained disabled after the manual live attempt was consumed and restored to safe state.

operational_benefit:
- Keeps validation and execution behavior separated.
- Supports safe rehearsals without unintended live calls.
- Preserves explicit operator control for high-risk paths.

safe_usage_conditions:
- `execution_mode=dry_run` by default.
- `execution_allowed=false` by default.
- `live_order_enabled=false` by default.
- Dry-run validation must not call live order endpoints.

forbidden_usage_conditions:
- Treating dry-run success as automatic live approval.
- Adding hidden fallback from dry-run to live.
- Adding retries or loops around dry-run blocks.
- Letting dry-run paths mutate live state.

future_revalidation_needed:
- Revalidate after any WF04 or helper execution-path change.
- Revalidate before future order-test or live-path work.
- Revalidate against workflow activation state.

### VP-007

id:
- VP-007

title:
- Forbidden endpoint enforcement

description:
- Cancel, reorder, withdrawal, and unintended live-order endpoint usage are excluded from current safe work and must remain blocked unless separately designed and approved.

validation_result:
- VALIDATED

validation_reason:
- No cancel/reorder/withdrawal path used.
- Safe rehearsal and monitoring runs reported no forbidden endpoint calls.

operational_benefit:
- Prevents unreviewed lifecycle actions.
- Keeps the project focused on observation, reconciliation design, and controlled STOP state.
- Avoids hidden side effects during documentation and monitoring phases.

safe_usage_conditions:
- Endpoint usage is checked explicitly in reports.
- Cancel/reorder/withdrawal paths remain out of scope.
- Live-order path remains disabled after consumed fuse.
- Any unknown endpoint use forces STOP.

forbidden_usage_conditions:
- Cancel endpoint calls.
- Reorder or cancel-replace loops.
- Withdrawal endpoint calls.
- Hidden retry or fallback execution.
- Telegram buttons that trigger trade, cancel, retry, activate, or cron behavior.

future_revalidation_needed:
- Revalidate via static endpoint scan before runtime patches.
- Revalidate before controlled cancel design.
- Revalidate after helper or workflow imports.

### VP-008

id:
- VP-008

title:
- Additive documentation-first workflow

description:
- Safety-critical gaps are documented as reports, specs, registries, and checklists before runtime implementation is attempted.

validation_result:
- STRONGLY_VALIDATED

validation_reason:
- Extensive planning/spec generation without runtime risk.
- Reconciliation, recovery, persistent logging, Telegram read-only alerts, safety gate, master index, known failures, and validated patterns were documented additively.

operational_benefit:
- Reduces ambiguity before patches.
- Preserves a recoverable audit trail.
- Forces runtime work through explicit safety gates.

safe_usage_conditions:
- Documentation changes do not modify workflow/helper/runtime/configuration.
- Reports exclude secrets, JWTs, Authorization headers, raw balances, raw order payloads, and full identifiers.
- Existing logs are not rewritten unless explicitly permitted by project telemetry rules.
- Runtime patch decisions reference the safety gate and known failures registry.

forbidden_usage_conditions:
- Treating a design document as runtime approval.
- Modifying workflow/helper/runtime files under documentation-only scope.
- Skipping memory files before work.
- Using documentation work to bypass the open-order STOP condition.

future_revalidation_needed:
- Revalidate document index and registries before future sessions.
- Revalidate safety gate alignment before any runtime patch.
- Revalidate that generated docs still match actual runtime state.

## 5. Final Rule

Prefer validated patterns over new untested runtime behavior.
