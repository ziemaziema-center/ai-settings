# WF05 UI Render Repair Clone

Date: 2026-05-12

## Result

Overall status: `BLOCKED`

The approved repair create operation succeeded, but final UI-render confirmation remains blocked because Codex does not have an authenticated n8n editor session. The new workflow is structurally valid, inactive, and ready for a human-authenticated UI check.

## Repair

- Action taken: created one new inactive UI-render fixed clone.
- Repaired workflow name: `WF05_Reconciliation_ReadOnly_UI_RENDER_FIXED`
- Repaired workflow id: `qd1Hc9sv1i9DGXoy`
- Repaired editor URL: `https://n8n.mykindredai.com/workflow/qd1Hc9sv1i9DGXoy`
- Active: `false`
- Node count: `8`
- Connection source count: `7`

## Render Fix Applied

The previous generated-id clone still preserved the same internal node ids as the original WF05. The likely remaining UI-render issue was payload-level editor state caused by cloned internal node ids and flat inherited positions, not top-level workflow id alone.

The fixed clone was created from the read-only WF05 API export with:

- no top-level workflow `id` in the create payload;
- n8n-generated workflow id;
- fresh internal node ids for all eight nodes;
- normalized visible node positions;
- original node names, types, type versions, connections, settings, and pin data preserved.

## Original WF05

- Original workflow untouched: `true`
- Original workflow active: `false`
- Original node count: `8`
- Original connection source count: `7`

## Safety Validation

- Original WF05 execution count: `0`
- UI_RECOVERY execution count: `0`
- UI_RENDER_FIXED execution count: `0`
- WF03 active count: `0`
- WF04 active count: `0`
- Helper health: `PASS`
- `open_order_exists`: `false`
- `open_order_count`: `0`
- `duplicate_order_exists`: `false`
- Execution lock state: `unlocked`
- Upbit cron line present: `false`

## Safety Outcome

No WF05 execution, clone execution, workflow activation, cron enablement, live API call, live order, cancel, reorder, Telegram runtime send, lock acquire/release test, restart, or second repair clone was attempted.

## Next Safe Action

Human operator opens `https://n8n.mykindredai.com/workflow/qd1Hc9sv1i9DGXoy` in an authenticated n8n browser session and confirms all 8 nodes are visible and Active toggle is OFF; do not execute.
