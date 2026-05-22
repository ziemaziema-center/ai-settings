# V2 Execution Lock Runtime Deployment

Date: 2026-05-11 KST

Mode: bounded execution-lock runtime deployment

Runtime scope: `upbit-helper` only

## Result

Deployment result: PASS

The previously validated V2 execution lock implementation was deployed to the helper runtime and validated with bounded helper-local checks only.

## Deployment Scope

Allowed and performed:

- Copied the validated local helper source to remote `/home/ubuntu/upbit-helper/app/main.py`.
- Rebuilt Docker image `upbit-helper:local`.
- Restarted only the `upbit-helper` container.
- Added helper-only execution lock host bind:

```text
/home/ubuntu/kbia-logs/upbit-helper:/home/ubuntu/kbia-logs/upbit-helper
```

- Preserved the existing order journal bind:

```text
/home/ubuntu/kbia-logs/upbit-helper/order-journal:/kbia-logs/order-journal
```

Not performed:

- no workflow patch
- no workflow activation
- no cron enablement
- no order placement
- no cancel
- no reorder
- no retry loop
- no Telegram runtime send
- no live fuse reset
- no autonomous unlock
- no live execution
- no investment decision logic

## Backup And Rollback

Local source backup:

```text
C:\Users\minho\Documents\02_work\03_AI\03_investment_automation\01_planning\backups\execution_lock_20260511_221304
```

Remote source backup:

```text
/home/ubuntu/kbia_backups/upbit-helper-execution-lock-20260511_223147
```

Remote rollback image:

```text
upbit-helper:rollback-execution-lock-20260511_223147
```

Rollback readiness: PASS

## Runtime Touched

Touched:

- `/home/ubuntu/upbit-helper/app/main.py`
- Docker image `upbit-helper:local`
- Docker container `upbit-helper`
- helper lock directories:
  - `/home/ubuntu/kbia-logs/upbit-helper/execution-locks`
  - `/home/ubuntu/kbia-logs/upbit-helper/execution-lock-journal`

Not touched:

- n8n workflow files
- n8n workflow activation state
- cron
- `reel-service`
- Instagram/SNS workflows
- Telegram runtime send path
- live fuse state

## Restart Status

Restart attempted: true

Restart scope: `upbit-helper` container only

Container status after restart: `upbit-helper` running

Helper health after restart: PASS

Health result:

```json
{"ok": true, "service": "upbit-helper"}
```

## Pre-Deploy Gate Checks

Read-only order state:

- `http_status=200`
- `success=true`
- `market=KRW-BTC`
- `open_order_count=0`
- `open_order_exists=false`

Workflow state:

- `KBIA_03_WF_Upbit_PreCheck_Engine`: inactive
- duplicate `KBIA_03_WF_Upbit_PreCheck_Engine`: inactive
- `KBIA_04_WF_Upbit_Execution_Engine`: inactive
- no active `WF05_Reconciliation_ReadOnly` runtime entry detected

Cron status:

- Upbit workflow cron disabled: true
- no Upbit workflow activation performed

Automation state:

- automation remains disabled: true

## Post-Deploy Validation

### Existing Endpoints

Accounts telemetry:

- `http_status=200`
- `success=true`
- `account_count=17`
- `currencies_present_count=17`
- `krw_balance_sufficient=true`
- `krw_available_band=5000-29999`
- `error_name=null`
- `error_message=null`

Open-orders telemetry:

- `http_status=200`
- `success=true`
- `market=KRW-BTC`
- `open_order_count=0`
- `open_order_exists=false`
- `error_name=null`
- `error_message=null`

Helper detail endpoint:

- `success=true`
- `mode=read_only_detail_telemetry`
- `market=KRW-BTC`
- `open_order_count=0`
- `open_order_exists=false`
- `classification=cancel`
- `blocked_reason=null`
- `next_safe_action=remain_stopped`
- `forbidden_endpoint_check=true`
- `secrets_leak_check=true`

### Execution Lock Runtime Validation

Endpoint reachability:

- `POST /execution-lock/status`: PASS
- `POST /execution-lock/acquire`: PASS
- `POST /execution-lock/release`: PASS

Lock behavior:

- initial status: `unlocked`
- acquire with no active lock: PASS
- second acquire while lock exists: blocked with `ACTIVE_LOCK_EXISTS`
- release with matching owner token: PASS
- stale lock detection: PASS, `stale_stop`, `human_review_required=true`
- stale lock cleanup by matching release: PASS
- final status: `unlocked`
- active lock file remaining: false

Lock journal:

- journal file: `execution_lock_2026-05-11.jsonl`
- line count before validation: `0`
- line count after validation: `7`
- append-only journal validation: PASS

Source scan:

- lock functions present: true
- `_upbit_get` in lock functions: false
- `_upbit_post` in lock functions: false
- forbidden mutation terms in lock functions: none
- scan result: PASS

## Workflow And Cron Verification

Post-deploy n8n database read-only scan confirmed:

- `KBIA_03_WF_Upbit_PreCheck_Engine`: inactive
- duplicate `KBIA_03_WF_Upbit_PreCheck_Engine`: inactive
- `KBIA_04_WF_Upbit_Execution_Engine`: inactive

Workflow patch performed: false

Workflow activation changed: false

Cron enabled for Upbit workflows: false

## Safety Telemetry

- execution lock runtime deployment: completed
- helper restart attempted: true
- helper modified: true, helper-only runtime deployment
- workflow patch: false
- workflow activation changed: false
- cron enabled: false
- live API order endpoint called: false
- live order attempted: false
- cancel attempted: false
- reorder attempted: false
- retry loop added: false
- Telegram runtime send attempted: false
- live fuse reset attempted: false
- autonomous unlock added: false
- live execution authority added: false
- investment decision logic added: false
- secrets leak scan: PASS

## Notes

The helper restart produced transient localhost connection resets while the container was starting. The deployment script waited until `/health` passed before reporting success.

The validation acquired and released test locks only through the execution-lock endpoints. It ended with `lock_state=unlocked` and no active lock file.

## Final Status

The execution lock endpoints are deployed and validated in `upbit-helper`. The system remains in controlled STOP state with automation disabled.
