# Operational Snapshot - 2026-05-11

## 1. System Overview

Project: KB Investment Automation / Upbit crypto automation.

Current milestone: SAFE LIMITED LIVE EXECUTION V1.

Architecture:
- `upbit-helper`: FastAPI helper service that owns Upbit JWT signing and talks to Upbit private APIs.
- `n8n`: workflow orchestration layer. n8n workflows call helper telemetry endpoints and must not create Upbit JWTs directly.
- `reel-service`: unrelated SNS/Instagram service. It is not part of the Upbit trading path and must not be touched for KBIA Upbit work.
- Docker network: `kbia-internal`.
- n8n persistent volume: `n8n_data`.

Containers:
- `n8n`
- `upbit-helper`
- `reel-service`

Helper role:
- Owns Upbit auth/JWT signing.
- Returns sanitized telemetry only.
- Must not expose JWTs, Authorization headers, raw balances, raw order payloads, API secrets, or full order UUIDs.

Workflow role separation:
- WF03 `KBIA_03_WF_Upbit_PreCheck_Engine`: precheck, read-only private telemetry, duplicate lock, emergency stop, order-size checks, STOP handoff.
- WF04 `KBIA_04_WF_Upbit_Execution_Engine`: execution gate validation and disabled-by-default one-time manual live path through helper only.
- WF05: post-execution/finality concepts; not production-ready as a reconciliation engine.
- WF06: monitoring/failsafe concepts; Telegram runtime is not production-ready.

## 2. Verified Safe Components

Verified components:
- Helper health: PASS.
- Upbit auth: operational through helper.
- Accounts telemetry: operational and sanitized.
- Open-orders telemetry: operational and sanitized.
- Order-test telemetry: successful in prior validation.
- Duplicate lock: present/validated as a blocking layer.
- Dry-run isolation: WF04 default path remains dry-run blocked.
- Live fuse: one-time live attempt consumed and disabled.
- Workflow inactive state: WF03/WF04 inactive.
- Monitoring flow: read-only monitoring logs and summary report generated successfully.

Verified execution result:
- One-time live Upbit limit bid order was accepted.
- No duplicate live order was placed.
- No retry loop was used.
- No cancel, reorder, withdrawal, cron enablement, or workflow activation was used.

## 3. Current Live State

Current monitored order state:
- `open_order_exists=true`
- `open_order_count=1`
- `market=KRW-BTC`
- `state=wait`
- `stale_wait=true`
- `remaining_volume=0.0001`
- `executed_volume=0`
- `created_at=2026-05-10T12:46:37+09:00`

Current monitoring classification:
- `still_waiting_safe_stop`

Interpretation:
- The system must remain in STOP.
- No second order is allowed while the open order exists.
- The stale-wait flag is report-only and must not trigger action.

## 4. Hard Safety Rules

DO NOT:
- No cron.
- No activation.
- No retry.
- No cancel.
- No reorder.
- No second order.
- No auto loop.
- No workflow patch during monitoring-only work.
- No helper patch during monitoring-only work.
- No container restart during monitoring-only work.
- No Telegram live send unless explicitly scoped as a read-only alert validation task.
- No secret, JWT, Authorization header, raw balance, raw order payload, or full UUID logging.

If uncertain: STOP.
If incomplete: STOP.
If risk exists: STOP.

## 5. Not Yet Production Ready

The following are not production-ready:
- Reconciliation engine.
- Partial fill handling.
- Restart recovery.
- Telegram alert runtime.
- Persistent state recovery.
- Cancel lifecycle.
- Portfolio engine.

These must be designed and validated separately before any automation expansion.

## 6. Safe Next Phase Order

1. wait for order resolution
2. reconciliation engine
3. external persistent logging hardening
4. Telegram read-only alerts
5. fill-state validation
6. controlled cancel flow
7. only then limited automation

## 7. Final Status

System currently ends in:

CONTROLLED STOP STATE
