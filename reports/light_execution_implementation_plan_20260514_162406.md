# Light Execution Implementation Plan

Timestamp: 2026-05-14 16:24:06 KST

Mode: PLAN-ONLY, NON-PRODUCTION, IMPLEMENTATION-NOT-AUTHORIZED.

Reference design:

- `C:\Users\minho\Documents\02_work\03_AI\03_investment_automation\01_planning\reports\light_execution_system_design_20260514_142342.md`

Boundary statement:

- This document is a planning artifact only.
- It does not authorize workflow implementation, runtime creation, testing, Upbit access, credentials, API calls, live trading, or order attempts.
- WF07/WF08 archives remain isolated and unchanged.

## 1. Purpose

The light execution system implementation plan defines the smallest practical path toward a human-controlled Upbit automation workflow without starting implementation.

Purpose requirements:

- minimal practical automation
- human-in-loop only
- safety-first operation
- no autonomous trading
- no concurrency
- one-order-at-a-time execution model if execution is ever separately approved

Planning principles:

- read before write
- propose before approve
- approve before execute
- stop before uncertainty becomes action
- log every material state
- alert on any blocked or ambiguous state

## 2. Minimum System Components

Smallest acceptable future structure:

### Read-Only Market/Account Monitor

- collects market/account/order visibility only after separate API/credential approval
- verifies available KRW/pre-held asset state according to final asset design
- verifies open-order state
- emits a status snapshot only
- has no order capability

### Proposal Generator

- creates exactly one candidate proposal at a time
- includes market, side, limit price, amount/value, reason, expiry, and validation state
- blocks proposal creation if required status inputs are missing or uncertain
- has no execution capability

### Telegram Approval Gate

- delivers proposal summary to the operator
- requires explicit human confirmation for the exact proposal
- rejects stale, changed, duplicate, or ambiguous approvals
- never infers approval from alert delivery alone

### Disabled-by-Default Order Executor

- remains disabled until separate implementation and execution approval exists
- limit-order-only
- one-order-at-a-time only
- no market orders
- no retry loop
- no cancel/reorder path in the initial implementation

### Append-Only Journal Logger

- records monitor snapshots, proposals, approvals, STOP events, alerts, and any future execution outcomes
- acceptable backing formats: local markdown, local JSON, or Google Sheets if separately approved
- logging failure stops the path

### Stop Fuse / Kill Switch

- global STOP state defaults to active until explicitly configured otherwise in a future approved implementation
- blocks proposal and execution paths when active
- reset remains manual

### Alert Path

- sends proposal-ready, approval-required, STOP, validation-failed, and human-review-required alerts
- alert failure blocks progression

Explicitly rejected components:

- autonomous replay
- self-healing execution
- automatic retry trading
- autonomous scheduling chains
- concurrency runtime
- runtime lock manager
- market-order executor
- silent recovery engine

## 3. Implementation Phases

### Phase 0 - Planning Skeleton

Allowed future scope only after separate approval:

- create folder structure
- define report paths
- define log paths
- preserve WF07/WF08 archive separation
- define static config placeholders without credentials

Exit criteria:

- directories documented
- archive preservation confirmed
- no runtime or API capability exists

### Phase 1 - Read-Only Telemetry

Scope:

- read-only telemetry design
- account snapshot visibility
- open-order visibility
- market/status visibility
- no order capability

Exit criteria:

- monitor can produce operator-readable snapshots in a future approved read-only implementation
- unclear API/status/credential state maps to STOP
- no execution nodes or code exist

### Phase 2 - Proposal Generation Only

Scope:

- proposal generation from verified read-only snapshot
- Telegram proposal delivery if separately approved
- proposal expiry and summary fields
- no execution capability

Exit criteria:

- one proposal at a time
- limit-order-only proposal fields
- missing validation blocks proposal

### Phase 3 - Human Approval Gate

Scope:

- explicit confirmation path
- approval artifact or approval message linkage
- stale/duplicate/mismatch rejection
- executor still disabled

Exit criteria:

- approval cannot be inferred
- approval cannot be replayed silently
- approval does not execute anything by itself

### Phase 4 - Isolated Limit-Order Execution Path

Scope:

- future only after separate implementation, testing, and live execution approval
- isolated one-shot limit-order path
- one-order-at-a-time only
- hard stop fuse before execution
- no retry loop

Exit criteria:

- open order check passes immediately before execution
- duplicate order check passes immediately before execution
- API/status/account conditions pass immediately before execution
- journal and alert paths are available

### Phase 5 - Logging, Alerting, Manual Recovery

Scope:

- append-only logging
- alert escalation
- manual recovery only
- no self-healing execution

Exit criteria:

- all failures produce STOP/log/alert
- recovery decisions remain manual
- stop-fuse reset remains manual

## 4. Required Validation Checks

Mandatory checks:

- open order check
- duplicate order prevention
- limit-order-only enforcement
- market status validation
- API status validation
- previous execution state validation
- journal/log write validation
- alert-path validation
- stop-fuse validation
- human approval validation

Additional safety checks:

- KRW/pre-held asset condition validation according to final asset design
- proposal expiry validation
- exact proposal-to-approval match validation
- executor-disabled state validation before Phase 4
- no market-order field validation
- no leverage validation

Any failed validation:

`STOP`

Validation failures must log, alert, and require human review when ambiguous.

## 5. Failure Handling

Required flow:

1. detect
2. stop
3. log
4. alert
5. human review

Explicitly forbidden:

- hidden retry
- silent recovery
- autonomous repair
- hidden replay
- hidden reorder
- auto-cancel
- auto-replace
- auto-unlock
- self-healing execution

Failure classes:

- missing data -> STOP
- API/credential/status uncertainty -> STOP
- open order exists -> STOP
- duplicate suspected -> STOP
- approval mismatch -> STOP
- log failure -> STOP
- alert failure -> STOP
- unexpected runtime response in any future implementation -> STOP and human review

## 6. Safety Boundaries

Explicit boundaries:

- WF07/WF08 archives remain isolated
- no inheritance of runtime authorization from WF07/WF08 archive
- implementation requires separate approval
- testing requires separate approval
- live trading requires separate approval
- API access requires separate approval
- credential use requires separate approval
- workflow activation requires separate approval

The light execution path is a separate practical design layer, not a continuation of the WF07/WF08 proof system.

## 7. What Must Remain Manual

Must remain manual initially:

- API key management
- exchange funding
- first execution approval
- recovery decisions
- anomaly review
- stop-fuse reset
- approval of any workflow activation
- approval of any credential attachment
- approval of any live execution attempt

Manual decisions must not be inferred from prior approvals, alerts, logs, or proposal delivery.

## 8. Final Recommendation

Recommended build shape if future implementation is separately approved:

- smallest viable safe system
- minimal workflow count
- minimal runtime complexity
- approval-heavy operation initially
- read-only monitor first
- proposal generator second
- approval gate third
- executor last and disabled by default

Recommended minimal workflow count:

- one read-only monitor/proposal workflow
- one approval intake workflow if needed
- one disabled-by-default executor workflow only after separate approval

Must remain blocked:

- autonomous trading
- market orders
- leverage
- retry loops
- concurrency runtime
- scheduler runtime
- live execution without explicit approval
- WF08 implementation

Final decision:

- PLAN_ONLY
- IMPLEMENTATION_NOT_AUTHORIZED
- TESTING_NOT_AUTHORIZED
- EXECUTION_NOT_AUTHORIZED
- WF07_ARCHIVE_PRESERVED
- WF08_BLOCKED
- LIVE_PATH_FORBIDDEN
