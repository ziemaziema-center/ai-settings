# WF05 UI Redirect Root-Cause Diagnosis

Date: 2026-05-12

## Result

overall_status: `PASS`

The stored WF05 workflow exists and is structurally intact. The redirect to a different workflow URL with `?new=true` is not explained by a missing workflow, archived workflow, ownership loss, or backend HTTP redirect.

Most likely root cause: the operator is opening the raw IP/HTTP editor URL while n8n is configured for the HTTPS domain editor origin.

## Evidence

### Workflow Existence

- API workflow id: `WF05LockROV2A11`
- display name: `WF05_Reconciliation_ReadOnly`
- active: `false`
- trigger count: `0`
- node count: `8`
- connection source count: `7`
- API exact name match count: `1`
- DB workflow row exists: `true`
- DB archived: `false`

### Project And Owner Access

- `shared_workflow.workflowId`: `WF05LockROV2A11`
- project id: `M3e6xHUu7VezXSBg`
- project type: `personal`
- project relation role: `project:personalOwner`
- owner user enabled: `true`
- owner role: `global:owner`

No DB-side project/owner access problem was found.

### Backend Route Behavior

Read-only HTTP checks on the n8n host showed:

- `/workflow/WF05LockROV2A11` returns the n8n SPA shell with HTTP `200`
- `/workflow?new=true` also returns the n8n SPA shell with HTTP `200`
- no backend HTTP 30x redirect from `/workflow/WF05LockROV2A11` to `?new=true` was observed

Therefore the `?new=true` transition is frontend router/session behavior after the SPA loads, not a backend route redirect.

### Public URL / Origin Configuration

The n8n container is configured with:

- `N8N_EDITOR_BASE_URL=https://n8n.mykindredai.com/`
- `WEBHOOK_URL=https://n8n.mykindredai.com/`
- `N8N_HOST=n8n.mykindredai.com`
- `N8N_PROTOCOL=https`
- `N8N_TRUST_PROXY=true`
- `N8N_SECURE_COOKIE=false`

The problematic operator URL is:

```text
http://43.201.227.194:5678/workflow/WF05LockROV2A11
```

This is not the configured editor origin. That can split browser session/cookie/local-storage context and cause the frontend to resolve navigation as a new workflow route or stale editor state.

## Route Format

Expected safe editor URL:

```text
https://n8n.mykindredai.com/workflow/WF05LockROV2A11
```

Fallback navigation path:

```text
https://n8n.mykindredai.com/home/workflows
```

Then open `WF05_Reconciliation_ReadOnly` from the workflow list.

## Secondary Risk

WF05 uses a custom workflow id of length `15`, while most generated workflow IDs in this runtime are length `16`. API and DB accept the id, and the backend serves the SPA at `/workflow/WF05LockROV2A11`, so this is not proven to be the cause. It remains a secondary UI-router compatibility risk if the frontend applies stricter client-side assumptions than the backend/API.

## Safety

No workflow was executed, modified, imported/exported, activated, repaired, or patched. No env modification, restart, CLI execution, workflow run API, live API, order, cancel, reorder, Telegram send, or lock acquire/release was used.

