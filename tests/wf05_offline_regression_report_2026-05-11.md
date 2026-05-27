# WF05 Offline Regression Report - 2026-05-11

## Summary
- timestamp_kst: 2026-05-27T13:14:17+09:00
- classifier_version: wf05-offline-classifier-2026-05-11-v1
- fixture_count: 12
- passed_count: 12
- failed_count: 0
- failed_case_ids: []
- safety_result: PASS
- next_action: Use this offline runner before any future WF05 patch.

## Offline Safety
- network_used: false
- secrets_loaded: false
- helper_called: false
- upbit_called: false
- n8n_called: false
- workflow_executed: false
- workflow_modified: false
- helper_modified: false

## Case Results
| Case ID | Expected | Actual | Result |
| --- | --- | --- | --- |
| wf05_wait | wait | wait | PASS |
| wf05_partial_fill | partial_fill | partial_fill | PASS |
| wf05_done_by_state | done | done | PASS |
| wf05_done_by_volume | done | done | PASS |
| wf05_cancel | cancel | cancel | PASS |
| wf05_missing_state | unknown_stop | unknown_stop | PASS |
| wf05_missing_volume | unknown_stop | unknown_stop | PASS |
| wf05_malformed_numeric | unknown_stop | unknown_stop | PASS |
| wf05_negative_volume | unknown_stop | unknown_stop | PASS |
| wf05_inconsistent_done | unknown_stop | unknown_stop | PASS |
| wf05_unsupported_state | unknown_stop | unknown_stop | PASS |
| wf05_helper_error | unknown_stop | unknown_stop | PASS |

## Final Rule
If any fixture fails, STOP before any WF05 runtime patch, live telemetry check, or workflow execution.
