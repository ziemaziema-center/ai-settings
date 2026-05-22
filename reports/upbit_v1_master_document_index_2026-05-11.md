# Upbit V1 Master Document Index - 2026-05-11

## Purpose

This index is the entry point for SAFE LIMITED LIVE EXECUTION V1 documentation.

Current system posture:
- Runtime unchanged by this index.
- Open order still waiting.
- Workflows inactive.
- Live fuse consumed/disabled.
- Documentation/read-only work only.

Final rule:

Do not patch runtime unless safety gate permits it.

## Core Reports And Logs

### `safe_rehearsal_validation_2026-05-11.md`

Purpose:
- Records the full safe rehearsal/validation sweep.
- Captures helper health, read-only telemetry, failure-path rehearsal, restart test blocker, reconciliation dry run, logging validation, and Telegram readiness blocker.

When to read:
- At the start of any session that needs to understand what was actually validated.
- Before claiming production readiness.

Decision controlled:
- Whether SAFE LIMITED LIVE EXECUTION V1 rehearsal passed or remained blocked.
- Whether any future work must remain STOP due to open order, stale wait, or missing safety layer.

Runtime modification allowed from it:
- No.

### `open_order_monitor_summary_2026-05-11.md`

Purpose:
- Consolidates read-only open-order monitoring checks from 2026-05-11.
- Shows helper health trend, open-order trend, state trend, remaining-volume trend, executed-volume trend, stale-wait status, and final monitoring classification.

When to read:
- Before any reconciliation, monitoring, or order-state discussion.
- Before deciding whether an order is still pending, partially filled, done, canceled, or unknown.

Decision controlled:
- Current monitoring classification: `still_waiting_safe_stop`.
- Whether continued monitoring remains read-only.

Runtime modification allowed from it:
- No.

### `operational_snapshot_2026-05-11.md`

Purpose:
- Provides the clean operational snapshot for future recovery/reference.
- Summarizes architecture, containers, helper role, workflow role separation, verified safe components, current live state, hard safety rules, non-production-ready areas, safe next phase order, and final status.

When to read:
- Immediately after this master index.
- Before any future Upbit automation session.
- Before any handoff or recovery conversation.

Decision controlled:
- Whether the system is in CONTROLLED STOP STATE.
- What safety boundaries are currently in force.

Runtime modification allowed from it:
- No.

## Safety And Design Specs

### `reconciliation_design_spec_2026-05-11.md`

Purpose:
- Defines future reconciliation design.
- Separates execution from reconciliation.
- Defines required order states, required telemetry fields, read-only reconciliation rules, safe state transitions, future safety checks, forbidden future behavior, and safe implementation order.

When to read:
- Before implementing any order lifecycle parser.
- Before interpreting wait, partial fill, done, cancel, or unknown state.
- Before building post-order finality logic.

Decision controlled:
- Whether a state is final, non-final, partial, canceled, or `unknown_stop`.
- Whether any post-order system path must remain STOP.

Runtime modification allowed from it:
- No.

### `restart_recovery_matrix_2026-05-11.md`

Purpose:
- Defines safe restart/recovery design.
- Covers n8n restart, helper restart, Docker container restart, EC2 reboot, network interruption, helper unavailable, telemetry timeout, stale open order state, partial telemetry corruption, duplicate lock loss, and staticData reset.

When to read:
- Before any restart test.
- Before any container/EC2 recovery work.
- Before enabling automation after interruption.

Decision controlled:
- Whether recovery state is safe or must STOP.
- Whether human-reviewed enablement is even eligible after recovery.

Runtime modification allowed from it:
- No.

### `persistent_logging_spec_2026-05-11.md`

Purpose:
- Defines external persistent logging requirements.
- Explains why staticData alone is insufficient.
- Defines log categories, required fields, forbidden log data, storage options, minimum safe V1 recommendation, logging failure handling, and final audit-trail rule.

When to read:
- Before implementing any logging, recovery, reconciliation, execution, alert, or operator action trail.
- Before relying on any state after restart.

Decision controlled:
- Whether logging is sufficient for future runtime changes.
- Whether a logging failure must block execution.

Runtime modification allowed from it:
- No.

### `telegram_readonly_alert_spec_2026-05-11.md`

Purpose:
- Defines Telegram as visibility-only, not execution.
- Lists allowed alert types, forbidden alert actions, safe message fields, severity levels, button policy, failure handling, and safe implementation order.

When to read:
- Before any Telegram-related design, dry-run, or implementation.
- Before adding buttons, callbacks, or alert routing.

Decision controlled:
- Whether a Telegram alert is read-only safe.
- Whether a button/action is forbidden.

Runtime modification allowed from it:
- No.

### `pre_implementation_safety_gate_2026-05-11.md`

Purpose:
- Defines the required safety gate before any future runtime patch.
- Covers preconditions, patch classes, approval requirements, hard reject conditions, and required output from future Codex patches.

When to read:
- Before any patch.
- Before any helper/workflow/runtime/config/logging/alert implementation work.
- Before classifying a future change as documentation-only, read-only observability, helper read-only, workflow read-only, execution logic, cancel logic, or automation enablement.

Decision controlled:
- Whether a patch may proceed.
- Which approval and validation requirements apply.
- Whether runtime modification is blocked.

Runtime modification allowed from it:
- Only if the safety gate explicitly permits the future patch class and all preconditions pass. This index itself does not permit runtime modification.

## Recommended Future Session Reading Order

1. this master index
2. operational snapshot
3. latest open order monitor summary
4. pre-implementation safety gate
5. reconciliation spec
6. recovery matrix
7. persistent logging spec
8. telegram read-only alert spec

## Runtime Rule

Do not patch runtime unless safety gate permits it.
