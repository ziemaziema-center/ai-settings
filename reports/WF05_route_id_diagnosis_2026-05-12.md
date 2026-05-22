# WF05 Route ID Diagnosis

Date: 2026-05-12

## Result

overall_status: `PASS`

`WF05LockROV2A11` is the actual n8n workflow ID and expected editor route ID for `WF05_Reconciliation_ReadOnly`. It is not merely an artifact key.

## Evidence

- n8n Public API `GET /workflows/WF05LockROV2A11`: found
- workflow display name: `WF05_Reconciliation_ReadOnly`
- active: `false`
- archived: `false`
- version id: `f56874e1-991e-4055-a648-d27e4788bc76`
- trigger count: `0`
- node count: `8`
- connection source count: `7`
- exact workflow-name matches in API list: `1`
- SQLite `workflow_entity.id`: `WF05LockROV2A11`
- SQLite `workflow_entity.name`: `WF05_Reconciliation_ReadOnly`
- SQLite `shared_workflow.workflowId`: `WF05LockROV2A11`
- SQLite `workflow_history.workflowId`: `WF05LockROV2A11`

## Expected Editor URL

Expected editor route:

```text
http://43.201.227.194:5678/workflow/WF05LockROV2A11
```

The route pattern with `?new=true` is the new-workflow editor path, not the WF05 stored workflow path:

```text
http://43.201.227.194:5678/workflow?new=true
```

## Editor Accessibility

Codex could not confirm authenticated editor access because the available browser session redirects to n8n sign-in. Therefore:

- route ID exists: `true`
- expected editor route is known: `true`
- editor accessible from Codex browser session: `false`

## Likely Redirect Reason

If the authenticated UI redirects to `?new=true`, the most likely reason is UI navigation/router/session state or opening the new-workflow route, not a wrong stored route ID. The stored workflow ID, workflow list entry, DB row, share row, and history row all agree on `WF05LockROV2A11`.

## Safety

No workflow was executed, modified, imported, exported, activated, or repaired. No restart, CLI execution, workflow run API, live order, cancel, reorder, or Telegram send was used.

