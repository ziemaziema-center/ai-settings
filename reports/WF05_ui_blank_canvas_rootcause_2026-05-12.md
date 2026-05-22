# WF05 Blank Canvas Root Cause

Date: 2026-05-12

## Result

Root cause confirmed for the WF05 workflow cluster:

`connections[source].main` was stored as a flat list of edge objects, while known-good n8n UI-rendering workflows store it as an array of output arrays.

Broken WF05 shape:

```json
{
  "main": [
    {
      "node": "Next Node",
      "type": "main",
      "index": 0
    }
  ]
}
```

Known-good UI-rendering shape:

```json
{
  "main": [
    [
      {
        "node": "Next Node",
        "type": "main",
        "index": 0
      }
    ]
  ]
}
```

## Evidence

- `KBIA_03_WF_Upbit_PreCheck_Engine`: all connection `main` values are `list_of_lists`.
- `KBIA_04_WF_Upbit_Execution_Engine`: all connection `main` values are `list_of_lists`.
- `WF05_Reconciliation_ReadOnly`: all connection `main` values are `flat_list_of_edges`.
- `WF05_Reconciliation_ReadOnly_UI_RECOVERY`: all connection `main` values are `flat_list_of_edges`.
- `WF05_Reconciliation_ReadOnly_UI_RENDER_FIXED`: all connection `main` values are `flat_list_of_edges`.
- `WF05_Reconciliation_ReadOnly_UI_CLEANROOM`: all connection `main` values are `list_of_lists`.

## Why Previous Repairs Failed

The previous repairs changed the top-level workflow id and internal node ids, but preserved the malformed connection shape. That left the editor-facing graph topology invalid even though API/DB node counts and connection source counts looked correct.

## Additional Observation

`My workflow` has `0` nodes and `0` connections. It is a genuinely blank workflow row, not the same WF05 payload defect.

## Safety

No workflow execution, activation, cron enablement, live API call, live order, cancel, reorder, Telegram runtime send, lock acquire/release test, restart, or destructive workflow action was used for diagnosis.
