# WF05 UI Accessibility Recovery Plan

Date: 2026-05-12

## Result

overall_status: `PASS`

This is a planning-only artifact. No workflow was executed, imported, duplicated, modified, activated, deleted, restored, or repaired.

## Current Facts

- `WF05_Reconciliation_ReadOnly` exists in n8n API/DB.
- Current workflow id: `WF05LockROV2A11`.
- Stored node count: `8`.
- Stored connection source count: `7`.
- Workflow JSON corruption: `false`.
- Runtime import artifact valid: `true`.
- Workflow active: `false`.
- Workflow archived: `false`.
- Exact workflow-name match count: `1`.
- UI access remains unreliable and redirects to `?new=true`.

## Analysis

### Likely UI Access Root Cause

The root cause remains UI-side route/session/editor handling, not stored workflow corruption. The strongest current risk is the custom workflow id:

```text
WF05LockROV2A11
```

It is accepted by API/DB, but differs from generated n8n runtime ids observed in this instance. The UI may apply stricter client-side assumptions or stale route handling and fall into new-workflow mode.

### Custom ID Risk

Risk level: `material`.

The id is usable for API/DB reads, but it is not proven safe for the n8n editor UI. Because the editor redirects to `?new=true`, WF05 should not be used for UI-driven validation until a UI-accessible clone with an n8n-generated id is created and verified.

## Option Assessment

### Option 1 - Export WF05 JSON and import as new workflow with n8n-generated ID

Recommendation: `SAFEST`

Rationale:
- Creates a normal n8n-generated id.
- Keeps original WF05 untouched.
- Can be imported inactive/manual-only.
- Gives a clean UI route to validate before any execution.

Required safeguards:
- Separate explicit approval required.
- Backup/export evidence before import.
- Remove top-level fixed `id` from import payload so n8n generates the id.
- Rename clone clearly, for example `WF05_Reconciliation_ReadOnly_UI_RECOVERY`.
- Preserve `active=false`.
- Preserve manual-trigger only.
- Confirm no schedule/cron nodes.
- Confirm no live order/cancel/reorder/Telegram/lock acquire-release paths.
- Confirm original WF05 remains inactive and untouched.
- Do not execute clone during import/visibility validation.

### Option 2 - Duplicate workflow via UI/API if safe

Recommendation: `NOT FIRST CHOICE`

Rationale:
- UI duplicate is impossible while the editor/list route is unreliable.
- API duplication may preserve problematic fields unless carefully normalized.
- Still requires mutation and separate approval.

### Option 3 - Restore runtime import artifact into new workflow with generated ID

Recommendation: `ACCEPTABLE VARIANT OF OPTION 1`

Rationale:
- The runtime import artifact is structurally valid and exactly matches runtime nodes/connections/settings.
- Must remove fixed id and import inactive under a new clear name.
- This is preferable if direct export is not needed or if export is unavailable.

### Option 4 - Leave WF05 as API-only and avoid runtime validation

Recommendation: `SAFE BUT BLOCKING`

Rationale:
- Avoids mutation entirely.
- Does not solve UI-assisted validation.
- Runtime validation remains blocked because the approved path depends on safe UI visibility.

## Recommended Recovery Plan

1. Planning gate:
   - keep original `WF05LockROV2A11` untouched;
   - require separate explicit approval for clone/import;
   - confirm WF05, WF03, WF04 inactive;
   - confirm cron disabled and no live approval exists.

2. Prepare clone payload:
   - use existing valid runtime import artifact or read-only API export as source;
   - remove top-level `id`;
   - rename clone to `WF05_Reconciliation_ReadOnly_UI_RECOVERY`;
   - preserve nodes, connections, settings, and inactive/manual-only design;
   - preserve no Telegram runtime send and no live/cancel/reorder paths.

3. Import clone under separate approval:
   - use only the already-running n8n API import/create workflow path or approved n8n UI import path;
   - do not activate;
   - do not execute;
   - record the generated workflow id.

4. Validate clone visibility read-only:
   - open `https://n8n.mykindredai.com/workflow/<generated_id>`;
   - confirm workflow name;
   - confirm nodes visible;
   - confirm Active toggle OFF;
   - confirm original WF05 remains untouched and inactive.

5. Future runtime validation gate:
   - only after clone visibility PASS, request separate explicit approval for one UI-driven clone execution;
   - original WF05 remains API/DB evidence only and is not used for UI runtime validation.

## Duplicate Runtime Risk

Duplicate runtime risk exists if both original WF05 and clone are kept as manual workflows. Mitigation:

- original remains inactive and untouched;
- clone remains inactive;
- no cron/schedule nodes;
- no activation;
- no execution until separate approval;
- clone name must include `UI_RECOVERY`;
- validation prompts must target generated clone id only after visibility PASS.

## Safety

No workflow execution, import, duplication, modification, activation, restart, API run endpoint, CLI execution, live order, cancel, reorder, Telegram send, or lock acquire/release was attempted.

