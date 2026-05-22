# V2 Helper Detail Endpoint Runtime Deployment

Date: 2026-05-11  
Mode: bounded helper runtime deployment  
Runtime scope: `upbit-helper` only  

## Result

Deployment result: PASS

The previously validated helper detail endpoint patch was deployed to the helper runtime and validated with read-only checks only.

## Deployment Scope

Allowed and performed:

- Copied the validated `upbit-helper/app/main.py` to the remote helper source.
- Rebuilt `upbit-helper:local`.
- Restarted only the `upbit-helper` container.
- Added helper-only append-only JSONL journal mount:

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
- no investment decision logic
- no unrelated Docker/network change

## Backup And Rollback

Local source backup:

```text
C:\Users\minho\Documents\02_work\03_AI\03_investment_automation\01_planning\backups\helper_detail_endpoint_20260511_205855
```

Remote source backup:

```text
/home/ubuntu/kbia_backups/upbit-helper-detail-20260511_211744
```

Remote rollback image:

```text
upbit-helper:rollback-20260511_211744
```

Rollback readiness: PASS

## Runtime Touched

Touched:

- `/home/ubuntu/upbit-helper/app/main.py`
- Docker image `upbit-helper:local`
- Docker container `upbit-helper`
- helper journal directory `/home/ubuntu/kbia-logs/upbit-helper/order-journal`

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

### New Detail Endpoint

Endpoint:

```text
POST /upbit/open-orders/detail-telemetry
```

Result:

- `success=true`
- `mode=read_only_detail_telemetry`
- `market=KRW-BTC`
- `open_order_exists=false`
- `open_order_count=0`
- `duplicate_order_exists=false`
- `new_order_created_detected=false`
- `classification=cancel`
- `blocked_reason=null`
- `next_safe_action=remain_stopped`
- `orders_count=1`
- `forbidden_endpoint_check=true`
- `secrets_leak_check=true`

Interpretation:

- No current open KRW-BTC order exists.
- The known resolved order is represented as `cancel`.
- The endpoint remained reconciliation-only and did not take action.

### Append-Only JSONL Journal

Journal write:

- `attempted=true`
- `success=true`
- `path_masked=order_journal_2026-05-11.jsonl`

Latest journal event:

- `market=KRW-BTC`
- `open_order_exists=false`
- `open_order_count=0`
- `duplicate_order_exists=false`
- `new_order_created_detected=false`
- `state=cancel`
- `remaining_volume=0.0001`
- `executed_volume=0`
- `classification=cancel`
- `blocked_reason=null`
- `next_safe_action=remain_stopped`

Journal secret scan: PASS

No JWT, Authorization header, API secret, raw balance, raw order payload, or full UUID was found in the validation journal.

### Mutation Path Scan

Runtime source scan for `open_orders_detail_telemetry`:

- detail endpoint function present: true
- calls `_upbit_post`: false
- allowed read paths present:
  - `/v1/orders/open`
  - `/v1/orders/closed`
- forbidden mutation terms in detail function: none
- scan result: PASS

### Workflow State

Target Upbit workflows checked after deployment:

- `KBIA_03_WF_Upbit_PreCheck_Engine`: inactive
- duplicate `KBIA_03_WF_Upbit_PreCheck_Engine`: inactive
- `KBIA_04_WF_Upbit_Execution_Engine`: inactive

Workflow inactive check: PASS  
Workflow patch performed: false  
Workflow activation changed: false  
Automation remains disabled: true

## Safety Telemetry

- helper runtime deployment: completed
- helper restart attempted: true
- workflow patch: false
- workflow activation changed: false
- cron enabled: false
- live order attempted: false
- cancel attempted: false
- reorder attempted: false
- retry loop added: false
- Telegram runtime send attempted: false
- live fuse reset attempted: false
- live execution authority added: false
- investment decision logic added: false

## Notes

An initial deployment command exited nonzero after the helper restart because the final `docker ps` formatting check was quoted incorrectly. Follow-up checks confirmed the helper container was running and `/health` passed. No rollback was required.

## Final Status

The helper detail endpoint is deployed and validated. The system remains in controlled STOP state with automation disabled.
