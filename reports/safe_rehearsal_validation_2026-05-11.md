# Safe Rehearsal Validation Report - 2026-05-11

Timestamp: 2026-05-11 13:36:34 KST

## Result
- Overall status: BLOCKED
- Reason: helper transport-unavailable failure path does not currently produce a structured downstream safe log node; it would hard-stop, but not with the requested detect -> block -> log/report -> stop shape.
- No live order attempted.
- No cancel attempted.
- No workflow activation changed.
- No new order placed.

## Current Read-Only Telemetry
- Helper health: PASS (`ok=true`, `service=upbit-helper`)
- Accounts telemetry: PASS (`http_status=200`, `success=true`)
- Upbit KRW sufficiency check for 10000 KRW: checked safely, result `krw_balance_sufficient=false`, band `1-4999`
- Open-orders telemetry: PASS (`http_status=200`, `success=true`)
- Open order: `open_order_exists=true`, `open_order_count=1`, `market=KRW-BTC`
- Reconciliation lifecycle: `wait`
- Reconciliation fields captured safely:
  - `market=KRW-BTC`
  - `side=bid`
  - `ord_type=limit`
  - `state=wait`
  - `remaining_volume=0.0001`
  - `executed_volume=0`
  - `trades_count=0`
  - `created_at=2026-05-10T12:46:37+09:00`
  - `uuid_masked=78bbdeeb...fc40`

## Workflow State
- WF04 `DXyVeNk4mKgdLY7C`: inactive, manual trigger only.
- WF03 `PKTzRQZyxts0z1fH`: inactive, manual trigger only, duplicate lock key `KRW-BTC|bid|limit` present.
- WF03 `fHyU5g8iI6rrKDQE`: inactive, manual trigger only, appears to be an older inactive duplicate.
- WF04 live fuse: `consumed=true`, market `KRW-BTC`.
- Emergency stop static config: not explicitly set; workflow default path is safe STOP validation with open order and KRW insufficiency.

## Phase Results
| Phase | Result | Notes |
| --- | --- | --- |
| Phase 1 - Read-only health | PASS | helper/accounts/open-orders all returned safe telemetry; WF03/WF04 inactive; open order exists. |
| Phase 2 - Failure paths | BLOCKED | open order, duplicate lock, emergency stop, insufficient KRW, and malformed telemetry paths block and log; helper transport-unavailable hard-stops without structured safe log node. |
| Phase 3 - Restart recovery | BLOCKED_RESTART_TEST | n8n restart was not performed because it can affect unrelated active workflows; helper/n8n/reel-service were inspected read-only only. |
| Phase 4 - Reconciliation dry run | PASS | open order classified as `wait`; no cancel/reorder/modify action taken. |
| Phase 5 - External logging | PASS | this report and JSON log artifact were created additively. |
| Phase 6 - Telegram alerts | BLOCKED | WF06 text-only Telegram sendMessage exists and no buttons were found, but live Telegram was not called; report `TELEGRAM_ALERT_NOT_READY` for dry-run alert validation. |

## Failure Path Rehearsal
| Test | Result | Blocked reason |
| --- | --- | --- |
| `open_order_exists=true` | PASS | `OPEN_ORDER_EXISTS` |
| duplicate lock present | PASS | `DUPLICATE_LOCK_ACTIVE` |
| emergency stop true simulation | PASS | `SYSTEM_STOP_ACTIVE` |
| insufficient KRW simulation | PASS | `INSUFFICIENT_KRW` |
| helper unavailable transport simulation | BLOCKED | `BLOCKED_HELPER_TRANSPORT_ERROR_NO_STRUCTURED_LOG_NODE` |
| malformed/failed telemetry simulation | PASS | `ACCOUNT_VALIDATION_NOT_PASSED_OR_OPEN_ORDER_CHECK_FAILED` |

## Safety Checklist
- USD/KRW pre-held equivalent adapted for Upbit KRW balance: checked safely.
- Duplicate order prevention: checked.
- Market/time assumption: crypto is 24/7, automation remains inactive.
- Limit-only rule: checked.
- API status/helper health: checked.
- Previous execution state: checked.
- Logging path: checked.
- Failure handling path: checked, with helper transport logging blocker.
- Alert path: checked statically; live Telegram not called.
- `open_order_exists` handling: checked.
- Forbidden endpoints not used: checked for this run.
- Workflow activation not changed: checked.
- Retry loop absent: checked for WF03/WF04; WF06 explicitly marks `retry_allowed=false`.
- Secrets not exposed: checked.

## Blockers
- `open_order_exists=true`; no further order execution is allowed.
- KRW sufficiency for 10000 KRW is false in safe telemetry.
- Duplicate inactive WF03 workflow names exist in n8n; both are inactive, but this should be cleaned only under a separate explicit additive-safe maintenance prompt.
- Helper transport-unavailable path does not currently emit a structured downstream safe log payload.
- Telegram alert dry-run was not executed because live Telegram sends are not established as read-only in this scope.
- Restart recovery was not performed because restarting n8n could affect unrelated workflows and violates the current limited-scope safety posture.

## Notes
- No raw balances, Authorization headers, JWTs, API secrets, full account details, raw order payloads, or full UUIDs were logged.
- No order, cancel, reorder, withdrawal, cron enablement, workflow activation, retry loop, or Telegram trade approval button was used.
