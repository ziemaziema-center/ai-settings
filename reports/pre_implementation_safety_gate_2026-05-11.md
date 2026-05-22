# Pre-Implementation Safety Gate Checklist - 2026-05-11

## 1. Purpose

No runtime patch is allowed unless this checklist passes.

This checklist applies before any future Codex work that could modify workflows, helper code, runtime configuration, credentials, containers, schedules, execution paths, cancel paths, alerts, or persistent state.

Current safety context:
- A live order exists.
- `state=wait`
- `stale_wait=true`
- WF03/WF04 are inactive.
- Live fuse is consumed/disabled.
- Reconciliation, recovery, persistent logging, and Telegram read-only alert specs exist.

If this checklist does not pass, the patch must not proceed.

## 2. Required Preconditions

Required before any runtime patch:

- `open_order_exists=false` OR explicit human-approved read-only patch only.
- Workflows inactive.
- Live fuse disabled.
- Duplicate lock understood.
- Emergency stop default safe.
- Persistent logging path ready.
- Rollback path ready.
- Backup path ready.
- No unrelated workflow impact.

Additional required evidence:
- Scope is explicitly bounded.
- Forbidden endpoints are identified and excluded.
- Secrets handling is documented.
- Validation plan is documented before changes.
- Output artifacts are planned.

## 3. Patch Classification

### DOC_ONLY
Documentation, reports, summaries, or design specs only.

Examples:
- Markdown design spec.
- Summary JSON.
- Monitoring report.

### READ_ONLY_OBSERVABILITY
Adds or adjusts read-only monitoring/reporting without changing execution behavior.

Examples:
- Read-only health checks.
- Report-only stale flags.
- Dry-run render templates.

### HELPER_READ_ONLY
Changes helper code to add or harden read-only telemetry only.

Examples:
- Add sanitized read-only endpoint.
- Improve helper health metadata.
- Add defensive error classification without execution side effects.

### WORKFLOW_READ_ONLY
Changes inactive workflow nodes for read-only validation, logging, or alert preparation only.

Examples:
- Add STOP-only log payload.
- Add read-only telemetry attachment.
- Add dry-run-only message render.

### EXECUTION_LOGIC
Any change that affects order-test, live order eligibility, live order payloads, execution gates, or order submission paths.

### CANCEL_LOGIC
Any change that touches cancel lifecycle, cancel endpoints, cancel decisions, cancel alerts, or cancel-related helper/workflow paths.

### AUTOMATION_ENABLEMENT
Any change that activates workflows, enables cron/schedules, adds loops, adds autonomous decisions, or allows runtime execution without direct manual invocation.

## 4. Approval Requirements

| Patch class | Approval requirement |
| --- | --- |
| DOC_ONLY | allowed |
| READ_ONLY_OBSERVABILITY | allowed only if no runtime side effect |
| HELPER_READ_ONLY | requires backup and dry-run |
| WORKFLOW_READ_ONLY | requires backup and inactive workflow only |
| EXECUTION_LOGIC | blocked while open order exists |
| CANCEL_LOGIC | blocked until controlled cancel design approved |
| AUTOMATION_ENABLEMENT | blocked until reconciliation + recovery + logging + alerts validated |

Additional approval notes:
- Human approval must state scope and exact allowed files.
- Approval for one class does not imply approval for a higher-risk class.
- Any ambiguity upgrades the classification to the higher-risk class.

## 5. Hard Reject Conditions

Reject any patch if it:

- could place order;
- could cancel order;
- could enable cron;
- could activate workflow;
- could retry;
- could expose secrets;
- touches unrelated workflows;
- lacks rollback;
- lacks validation output.

Also reject if it:
- changes `reel-service` or Instagram/SNS workflows;
- writes secrets to files;
- logs raw balances or raw order payloads;
- adds Telegram trade/cancel/retry/activate buttons;
- bypasses helper signing boundary;
- depends on staticData as the only durable state for production automation;
- cannot prove workflows remain inactive after the patch.

## 6. Required Output From Future Codex Patches

Every future Codex patch must return:

- `backup_path`
- `files_changed`
- `workflows_changed`
- `runtime_modified`
- `validation_result`
- `rollback_path`
- `safety_result`
- `next_action`

Recommended expanded output:

- `patch_classification`
- `forbidden_endpoint_check`
- `secrets_leak_check`
- `workflow_activation_changed`
- `restart_attempted`
- `telegram_live_send_attempted`
- `open_order_guard_status`

## 7. Final Rule

When unsure, do not patch.
