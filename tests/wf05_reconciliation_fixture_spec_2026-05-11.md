# WF05 Reconciliation Fixture Specification - 2026-05-11

## Scope

This fixture suite validates `WF05_Reconciliation_ReadOnly` classification behavior offline.

No workflow execution, helper call, Upbit call, live telemetry call, order action, cancel action, restart, activation, cron, or Telegram send is allowed for this suite.

## Fixture File

- `tests/wf05_reconciliation_fixtures_2026-05-11.json`

## Safety Rules

- Offline JSON fixtures only.
- No raw balances.
- No JWT.
- No Authorization header.
- No API secret.
- No raw order payload.
- No full account identifiers.
- No full UUID.
- No live API call.
- No workflow/helper modification.

## Classification Rules Under Test

- `state=wait` and `executed_volume=0` and `remaining_volume>0` -> `wait`
- `state=wait` and `executed_volume>0` and `remaining_volume>0` -> `partial_fill`
- `state=done` and `executed_volume>0` and `remaining_volume=0` -> `done`
- `remaining_volume=0` and `executed_volume>0` -> `done`
- `state=cancel` -> `cancel`
- missing, inconsistent, malformed, unsupported, or failed telemetry -> `unknown_stop`

## Fixtures

| ID | Scenario | Expected |
| --- | --- | --- |
| `wf05_wait` | `state=wait`, no execution, remaining volume present | `wait` |
| `wf05_partial_fill` | `state=wait`, executed volume and remaining volume present | `partial_fill` |
| `wf05_done_by_state` | `state=done`, executed volume present, zero remaining volume | `done` |
| `wf05_done_by_volume` | zero remaining volume and executed volume present | `done` |
| `wf05_cancel` | `state=cancel` | `cancel` |
| `wf05_missing_state` | missing state | `unknown_stop` |
| `wf05_missing_volume` | missing remaining volume | `unknown_stop` |
| `wf05_malformed_numeric` | malformed remaining volume | `unknown_stop` |
| `wf05_negative_volume` | negative remaining volume | `unknown_stop` |
| `wf05_inconsistent_done` | `state=done` but executed volume is zero and remaining volume is nonzero | `unknown_stop` |
| `wf05_unsupported_state` | unsupported exchange state | `unknown_stop` |
| `wf05_helper_error` | helper success false | `unknown_stop` |

## Validation Performed

Validation required for this task:
- JSON syntax validation only.

Validation explicitly not performed:
- No workflow execution.
- No helper call.
- No Upbit call.
- No live telemetry call.

## Expected Safe Outcome

The fixture suite can be used later for offline classifier regression tests while the system remains stopped and the open order remains unresolved.
