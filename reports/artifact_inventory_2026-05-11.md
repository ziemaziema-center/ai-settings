# Upbit V1 Artifact Inventory - 2026-05-11

## Summary

Current posture:
- WF05 implemented read-only.
- Offline runner created and passed 12/12 fixtures.
- Helper detail endpoint implementation deferred.
- Runtime remains controlled STOP.

Artifact count in this inventory: 39.

## Current Blockers

- Open order remains `state=wait` / stale.
- `open_order_exists=true` blocks any second order or automation.
- Helper open-orders telemetry remains summary-only.
- Restart recovery is not runtime-tested.
- Telegram runtime alerts are not implemented.
- Helper backup/rollback path is planned but not verified.
- No cancel lifecycle is approved.

## Reports

| Path | Purpose | Runtime impact | Read in future sessions |
| --- | --- | --- | --- |
| `reports/safe_rehearsal_validation_2026-05-11.md` | Safe rehearsal validation result and blockers | none | yes |
| `reports/open_order_monitor_summary_2026-05-11.md` | Consolidated open-order monitoring summary | none | yes |
| `reports/open_order_monitor_summary_2026-05-11.json` | Machine-readable monitor summary | none | yes |
| `reports/operational_snapshot_2026-05-11.md` | Operational snapshot for future recovery/reference | none | yes |
| `reports/reconciliation_design_spec_2026-05-11.md` | Read-only reconciliation state design | none | yes |
| `reports/restart_recovery_matrix_2026-05-11.md` | Restart/recovery safety matrix | none | yes |
| `reports/persistent_logging_spec_2026-05-11.md` | External persistent logging design | none | yes |
| `reports/telegram_readonly_alert_spec_2026-05-11.md` | Telegram read-only alert design | none | yes |
| `reports/pre_implementation_safety_gate_2026-05-11.md` | Safety gate before future patches | none | yes |
| `reports/upbit_v1_master_document_index_2026-05-11.md` | Master index of V1 safety docs | none | yes |
| `reports/KNOWN_FAILURES_2026-05-11.md` | V1 known failures registry | none | yes |
| `reports/VALIDATED_PATTERNS_2026-05-11.md` | V1 validated patterns registry | none | yes |
| `reports/wf05_reconciliation_readonly_validation_2026-05-11.md` | WF05 read-only implementation validation | none | yes |
| `reports/wf05_post_implementation_summary_2026-05-11.md` | WF05 post-implementation summary | none | yes |
| `reports/wf05_operator_reconciliation_summary_2026-05-11.md` | Operator-facing WF05 reconciliation summary | none | yes |
| `reports/wf05_operator_summary_validation_2026-05-11.md` | WF05 operator summary validation | none | yes |
| `reports/registry_update_wf05_2026-05-11.md` | Registry update recommendation for WF05 | none | yes |
| `reports/registry_update_wf05_offline_runner_2026-05-11.md` | Registry update for offline runner validation | none | yes |
| `reports/helper_backup_rollback_plan_2026-05-11.md` | Helper backup/rollback validation plan | none | yes |
| `reports/helper_diff_review_checklist_2026-05-11.md` | Helper patch diff-review checklist | none | yes |
| `reports/artifact_inventory_2026-05-11.md` | Human-readable artifact inventory | none | yes |
| `reports/artifact_inventory_2026-05-11.json` | Machine-readable artifact inventory | none | yes |

## Logs

| Path | Purpose | Runtime impact | Read in future sessions |
| --- | --- | --- | --- |
| `logs/safe_rehearsal_validation_2026-05-11.json` | Safe rehearsal telemetry log | read-only | yes |
| `logs/open_order_monitor_2026-05-11_134133.json` | Open-order monitor checkpoint | read-only | no |
| `logs/open_order_monitor_2026-05-11_140339.json` | Open-order monitor checkpoint | read-only | no |
| `logs/open_order_monitor_2026-05-11_140614.json` | Open-order monitor checkpoint | read-only | no |
| `logs/open_order_monitor_2026-05-11_140946.json` | Open-order monitor checkpoint | read-only | no |
| `logs/open_order_monitor_2026-05-11_141159.json` | Open-order monitor checkpoint | read-only | no |
| `logs/wf05_reconciliation_readonly_log_2026-05-11.json` | WF05 read-only reconciliation log | read-only | yes |
| `logs/wf05_operator_reconciliation_summary_2026-05-11.json` | WF05 operator summary JSON log | read-only | yes |

## Tests

| Path | Purpose | Runtime impact | Read in future sessions |
| --- | --- | --- | --- |
| `tests/wf05_reconciliation_fixtures_2026-05-11.json` | WF05 classifier fixture suite | none | yes |
| `tests/wf05_reconciliation_fixture_spec_2026-05-11.md` | Fixture suite specification | none | yes |
| `tests/wf05_regression_runner_spec_2026-05-11.md` | Offline runner design spec | none | yes |
| `tests/wf05_offline_regression_runner_2026-05-11.py` | Offline classifier regression runner | none | yes |
| `tests/wf05_offline_regression_report_2026-05-11.md` | Offline regression result report | none | yes |
| `tests/wf05_offline_regression_report_2026-05-11.json` | Machine-readable offline regression result | none | yes |

## Workflows

| Path | Purpose | Runtime impact | Read in future sessions |
| --- | --- | --- | --- |
| `workflows/05_WF_Post_Execution.json` | WF05_Reconciliation_ReadOnly inactive/manual workflow artifact | workflow-file-only | yes |

## Backups

| Path | Purpose | Runtime impact | Read in future sessions |
| --- | --- | --- | --- |
| `backups/wf05_reconciliation_readonly_20260511_164117` | Backup before WF05 read-only implementation | none | yes |
| `backups/wf05_operator_summary_20260511_173012` | Backup before WF05 operator summary enhancement | none | yes |

## Next Safe Action

Continue read-only monitoring/reconciliation only. Do not implement helper detail telemetry until the open order resolves or explicit read-only helper approval is granted with verified backup/rollback.
