# WF05 Structure Integrity Diagnosis

Date: 2026-05-12

## Result

overall_status: `PASS`

WF05 exists in n8n runtime with intact stored structure. The workflow is not empty in the n8n API, not empty in the n8n SQLite `workflow_entity` row, not empty in `workflow_history`, and matches the saved runtime import artifact for nodes, connections, and settings.

The reported empty editor canvas does not match stored DB/API state. Direct Codex UI confirmation of the empty canvas was blocked because the available browser session redirected to n8n sign-in.

## Stored Runtime Structure

- workflow id: `WF05LockROV2A11`
- workflow name: `WF05_Reconciliation_ReadOnly`
- active: `false`
- archived: `false`
- trigger count: `0`
- stored node count: `8`
- stored connection source count: `7`
- stored connection edge group count: `7`
- nodes JSON present: `true`
- nodes JSON valid: `true`
- connections JSON present: `true`
- connections JSON valid: `true`
- workflow history row present: `true`
- shared workflow owner row present: `true`

Node names:
- `Manual Trigger`
- `Set Read-Only Reconciliation Request`
- `Get Helper Detail Telemetry From Helper`
- `Get Execution Lock Status From Helper`
- `Classify Reconciliation And Lock State`
- `Build Append-Only Lock Log Payload`
- `Read-Only Lock STOP Report`
- `Build Operator Lock Integration Summary`

## Canvas Coordinate Check

All stored node positions are valid and within normal canvas coordinates:

- x range: `200` to `1950`
- y range: `300` to `300`
- off-canvas suspected: `false`

This makes a true empty stored workflow or extreme off-canvas placement unlikely.

## Import Artifact Comparison

Runtime import artifact:

- `runtime_exports/WF05_Reconciliation_ReadOnly_runtime_import_2026-05-11.json`

Validation:

- artifact exists: `true`
- artifact JSON valid: `true`
- artifact node count: `8`
- artifact connection source count: `7`
- API nodes match artifact nodes exactly: `true`
- API connections match artifact connections exactly: `true`
- API settings match artifact settings: `true`

## Likely Root Cause

The likely root cause is UI-side, not stored workflow corruption:

- stale editor/browser state;
- canvas viewport/render issue;
- user opened a different/blank editor route;
- frontend failed to load/display the stored workflow;
- authenticated UI session state differs from the read-only API/DB view.

Because stored API/DB/history/artifact state is intact and node positions are normal, a partial import or corrupted workflow JSON is unlikely.

## Safety

No workflow was executed, modified, imported, restored, activated, or repaired. No restart, live API call, order, cancel, reorder, Telegram send, CLI execute, or workflow run API was used.

