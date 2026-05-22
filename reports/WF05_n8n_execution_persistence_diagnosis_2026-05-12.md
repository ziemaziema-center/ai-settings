# WF05 n8n Execution Persistence Diagnosis

Date: 2026-05-12 KST

Mode: read-only n8n execution persistence diagnosis

## Result

overall_status: PASS

The diagnosis completed without executing WF05 or any workflow.

## Findings

- n8n version: `2.18.5`
- n8n container state: running
- execution-related env overrides found on `n8n` container: none
- WF05 workflow-level settings: `{ "executionOrder": "v1" }`
- WF05 workflow-level save overrides: none
- execution history DB readable: true
- n8n Public API execution list readable: true
- total `execution_entity` rows observed: `4441`
- WF05 execution rows found: `0`
- latest execution history contains unrelated workflow rows, proving execution history is generally being persisted and visible.
- latest 100 Public API execution rows contain no `mode=manual` rows and no `WF05LockROV2A11` rows.

## n8n Execution Saving Settings

No explicit env override was found for:

- `EXECUTIONS_DATA_SAVE_MANUAL_EXECUTIONS`
- `EXECUTIONS_DATA_SAVE_ON_SUCCESS`
- `EXECUTIONS_DATA_SAVE_ON_ERROR`
- `EXECUTIONS_DATA_PRUNE`
- `EXECUTIONS_DATA_MAX_AGE`
- `EXECUTIONS_DATA_PRUNE_MAX_COUNT`

According to n8n execution env docs, defaults are:

- manual execution save: `true`
- save on success: `all`
- save on error: `all`
- execution pruning: `true`
- max age: `336` hours
- prune max count: `10000`

The observed DB count `4441` is below the default count cap, and the current latest executions are visible. This does not support pruning as the reason WF05 disappeared immediately.

## Likely Reason

Most likely reason not detected:

```text
The human editor action did not create a persisted WF05 execution record.
```

Possible operational explanations:

- the editor click did not actually start the workflow;
- the editor was not on the runtime workflow `WF05LockROV2A11`;
- the run failed before n8n created an execution row;
- the UI action was preview/listen/editor-local behavior that did not persist as an execution;
- the execution list was checked against the correct runtime id, but no record exists.

The diagnosis does not support:

- global execution history unreadable;
- WF05 hidden in the Public API execution list;
- pruning immediately deleting the WF05 execution;
- workflow activation changing;
- cron-triggered execution;
- CLI/API-run execution by Codex.

## Safety

- wf05_executed: `false`
- any_workflow_executed: `false`
- workflow_modified: `false`
- activation_changed: `false`
- cron_enabled: `false`
- restart_attempted: `false`
- env_modified: `false`
- db_modified: `false`
- live_api_called: `false`

## Artifacts

- diagnosis_report_path: `reports/WF05_n8n_execution_persistence_diagnosis_2026-05-12.md`
- diagnosis_log_path: `logs/WF05_n8n_execution_persistence_diagnosis_2026-05-12.json`

## Sources

- n8n docs: `https://docs.n8n.io/hosting/configuration/environment-variables/executions/`
- n8n docs: `https://docs.n8n.io/workflows/settings/`
- n8n docs: `https://docs.n8n.io/workflows/executions/`

## Next Action

Have the operator capture the visible n8n editor execution id/status immediately after clicking `Execute Workflow`.
