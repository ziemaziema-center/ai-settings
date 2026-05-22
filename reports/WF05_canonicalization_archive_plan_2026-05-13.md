# WF05 Canonicalization And Archive Plan

Date: 2026-05-13

## Scope

Planning and metadata-safe canonicalization preparation only.

No workflow was executed, activated, renamed, deleted, archived, moved, patched, imported, exported, or modified.

## Canonical Workflow

- Canonical workflow: `WF05_Reconciliation_ReadOnly_UI_CLEANROOM`
- Canonical workflow id: `r0cmBJePnVLc9AED`
- Active state: `false`
- Node count: `8`
- Connection source count: `7`
- Connection edge count: `7`
- Connection schema: `list_of_lists`
- Latest execution reviewed: `8850`
- Latest execution status: `success`
- Latest execution mode: `manual`

## Canonical Reason

`WF05_Reconciliation_ReadOnly_UI_CLEANROOM` should be the canonical WF05 because it is the only WF05 variant that combines all required properties:

- inactive;
- UI-render repaired connection schema;
- 8 nodes and 7 connection sources/edges;
- successful read-only execution review;
- STOP-path reached;
- reconciliation classification `cancel`;
- lock state `unlocked`;
- no live execution, no activation, no cron, and no runtime mutation risk detected.

## Deprecated Candidates

### `WF05_Reconciliation_ReadOnly`

- Workflow id: `WF05LockROV2A11`
- Active: `false`
- Node count: `8`
- Connection source count: `7`
- Connection schema: `flat_list_of_edges`
- Classification: deprecated candidate.
- Reason: original runtime import uses the malformed connection schema that caused blank editor canvas behavior.

### `WF05_Reconciliation_ReadOnly_UI_RECOVERY`

- Workflow id: `OxJTKZQ0kJrICD5X`
- Active: `false`
- Node count: `8`
- Connection source count: `7`
- Connection schema: `flat_list_of_edges`
- Classification: deprecated candidate.
- Reason: generated-id recovery clone preserved the malformed connection schema.

### `WF05_Reconciliation_ReadOnly_UI_RENDER_FIXED`

- Workflow id: `qd1Hc9sv1i9DGXoy`
- Active: `false`
- Node count: `8`
- Connection source count: `7`
- Connection schema: `flat_list_of_edges`
- Classification: deprecated candidate.
- Reason: node-id/position repair clone preserved the malformed connection schema.

## Archive Strategy

Recommended future archive prefix:

```text
ARCHIVE_DO_NOT_RUN__WF05_DEPRECATED__2026-05-13__
```

Future archived names should be explicit and preserve lineage:

- `ARCHIVE_DO_NOT_RUN__WF05_DEPRECATED__2026-05-13__WF05_Reconciliation_ReadOnly`
- `ARCHIVE_DO_NOT_RUN__WF05_DEPRECATED__2026-05-13__WF05_Reconciliation_ReadOnly_UI_RECOVERY`
- `ARCHIVE_DO_NOT_RUN__WF05_DEPRECATED__2026-05-13__WF05_Reconciliation_ReadOnly_UI_RENDER_FIXED`

## Freeze Rules

Until a separate archive/rename approval is granted:

- Do not execute deprecated WF05 variants.
- Do not activate deprecated WF05 variants.
- Do not patch deprecated WF05 variants.
- Do not delete deprecated WF05 variants.
- Do not use deprecated WF05 variants for runtime validation.
- Keep all deprecated variants inactive.
- Treat `WF05_Reconciliation_ReadOnly_UI_CLEANROOM` as the only valid WF05 candidate for future read-only validation planning.

## Delete Decision

Delete now: `false`

No WF05 workflow should be deleted now. The deprecated variants are evidence-bearing artifacts for lineage, root-cause confirmation, and rollback comparison. Deletion should require a separate explicit approval and a pre-delete backup/export plan.

## Safety

- Any workflow executed by Codex: `false`
- Workflow modified: `false`
- Activation changed: `false`
- Restart attempted: `false`
- Live API called: `false`
- Live path allowed: `false`

## Next Safe Action

Prepare a separate approval-gated metadata-only archive/rename prompt for deprecated WF05 variants; do not execute or activate any WF05 workflow.
