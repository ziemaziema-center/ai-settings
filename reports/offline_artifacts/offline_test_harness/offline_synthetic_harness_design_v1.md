# OFFLINE SYNTHETIC HARNESS DESIGN V1

## 1. Status

SPEC_ONLY

## 2. Purpose

Define the local-only synthetic test harness that validates contract-layer safety boundaries without any live/shadow/runtime/API/credential operation.

## 3. Allowed Inputs

- synthetic market snapshots generated locally
- local deterministic scenario flags
- offline contract boundary clauses

## 4. Forbidden Inputs

- live exchange/API responses
- credential data
- runtime scheduler/parser/fixture dependencies
- any order-submission payload

## 5. Conceptual State Model

Allowed states:

- NO_SIGNAL
- SIGNAL_CANDIDATE_CREATED
- RISK_FILTER_REJECTED
- PTRC_PRECHECK_ELIGIBLE
- NO_ORDER_SUBMISSION

Forbidden states:

- SUBMITTED
- ACK_RECEIVED
- OPEN
- FILLED
- PARTIAL
- LIVE_ORDER
- SHADOW_ORDER

Any forbidden state causes test failure.

## 6. Scenario Coverage

- normal_trend
- sideways_chop
- sudden_spike
- sudden_crash
- spread_widening
- stale_data
- duplicate_signal
- cooldown_active
- rejection_cluster
- rate_budget_exhausted
- heartbeat_missed
- clock_skew
- reconciliation_drift
- kill_active

## 7. Safety Dependency Coverage

Every synthetic decision must keep dependencies explicit:

- PTRC required
- IDEM required
- OSM required
- RECON required
- KILL required

## 8. Non-Authorization Boundary

All outputs are offline governance/test artifacts only. Signal quality or score never authorizes trading or runtime activation.

## 9. Expected Outputs

- `offline_backtest_result_v1.json`
- `offline_backtest_result_v1.md`
- local unit/static test results
- offline score report and manifest/QA artifacts

## 10. Stop Conditions

Stop if any of the following occurs:

- forbidden state appears
- non-authorization sentence missing
- dependency coverage missing
- any live/shadow/runtime/API/credential action is required

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
