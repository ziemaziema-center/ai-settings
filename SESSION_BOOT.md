# SESSION_BOOT

## 1. System Identity

This is:
- safety-first
- validation-first
- fail-safe investment automation

This is not:
- profit-chasing bot
- aggressive auto trader

Project identity:
- KB Investment Automation / Upbit crypto automation.
- Current milestone: SAFE LIMITED LIVE EXECUTION V1.
- Current final posture: CONTROLLED STOP STATE.

## 2. Current Live State

Current monitored state:
- `open_order_exists=true`
- `open_order_count=1`
- `market=KRW-BTC`
- `state=wait`
- `stale_wait=true`
- `remaining_volume=0.0001`
- `executed_volume=0`
- workflows inactive
- live fuse disabled/consumed
- no automation enabled

Interpretation:
- The existing order is still waiting.
- No second order is allowed.
- The stale-wait flag is report-only and must not trigger action.

## 3. Required First Reads

Future GPT/Claude/Codex sessions must read in this order before any runtime discussion:

1. `reports/upbit_v1_master_document_index_2026-05-11.md`
2. `reports/operational_snapshot_2026-05-11.md`
3. `reports/open_order_monitor_summary_2026-05-11.md`
4. `reports/KNOWN_FAILURES_2026-05-11.md`
5. `reports/VALIDATED_PATTERNS_2026-05-11.md`
6. `reports/pre_implementation_safety_gate_2026-05-11.md`

Baseline memory files remain relevant:
- `KNOWN_FAILURES.md`
- `VALIDATED_PATTERNS.md`
- `PATCH_HISTORY.md`
- `DAILY_EXECUTION_LOG.md`

## 4. Hard Rules

Do not:
- no second order
- no cancel
- no reorder
- no activation
- no cron
- no retry loops
- no hidden execution
- no runtime patch without safety gate
- no workflow/helper/runtime/configuration change under documentation-only scope
- no Telegram live send unless explicitly scoped and safety-gated
- no secret, JWT, Authorization header, raw balance, raw order payload, or full UUID logging

Do not touch:
- unrelated workflows
- `reel-service`
- Instagram/SNS workflows

## 5. Validation-First Rule

Before any runtime proposal, identify:
- risks
- blockers
- rollback
- runtime impact
- unrelated workflow risk

Also identify:
- files that would change
- workflows that would change
- forbidden endpoint exposure
- secrets exposure risk
- whether the pre-implementation safety gate permits the work

## 6. Stop Conditions

If any of the following are true:
- `open_order_exists=true`
- unknown state
- helper unavailable
- duplicate ambiguity
- restart ambiguity
- logging failure

Then:

STOP.

Additional STOP conditions:
- missing telemetry
- inconsistent telemetry
- workflow identity ambiguity
- active workflow uncertainty
- live fuse ambiguity
- emergency stop ambiguity
- any possible order/cancel/retry/activation side effect

## 7. Safe Development Order

1. read-only monitoring
2. reconciliation
3. persistent logging
4. Telegram readonly alerts
5. restart-safe persistence
6. controlled cancel lifecycle
7. limited automation

## 8. Final Principle

"When uncertain, remain stopped."
