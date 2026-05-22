# Light Execution System Design

Timestamp: 2026-05-14 14:23:42 KST

Mode: design-only, documentation-only, offline-only, non-production. No Upbit access, credentials use, API calls, workflow activation, live trading logic, executable order code, scheduler runtime, writer/runtime implementation, WF07/WF08 archive mutation, WF08 start, or tests occurred.

Reference boundary:

- Existing WF07/WF08 artifacts remain frozen, archived, specification-only, and non-production.
- This document defines a separate simplified practical design layer.
- This document does not inherit runtime authorization from the archived WF07/WF08 proof system.

## 1. Purpose

The light execution system is a practical, simpler automation path for future Upbit investment automation.

Primary intent:

- keep humans in the loop
- avoid autonomous trading
- avoid concurrency
- allow one-order-at-a-time operation only
- keep the first practical build small enough to audit manually
- preserve safety before convenience

The system should produce proposals, require explicit human approval, and only then allow a disabled-by-default executor to be considered in a future separately approved phase.

This design is not an implementation approval.

## 2. Core Rules

Trading rules:

- limit order only
- no market order
- no leverage
- no auto-retry trading
- no duplicate order
- no order if open order exists
- no execution unless KRW/asset condition is verified according to the final asset design
- no action if API, credential, exchange status, market status, or runtime status is uncertain

Operational rules:

- one proposal at a time
- one approval at a time
- one order at a time
- no autonomous loop
- no hidden retry
- no self-healing execution
- no escalation from alert to execution without human approval
- any uncertainty stops the path

Fail-safe default:

- uncertain state -> STOP
- ambiguous account/order state -> STOP
- missing log path -> STOP
- missing alert path -> STOP
- missing human approval -> STOP

## 3. Workflow Model

The future workflow should be n8n-compatible but simple.

### Read-Only Monitor

Responsibility:

- read market/account/order status only after future explicit API approval
- detect whether prerequisites are knowable
- never place, cancel, or modify orders
- emit a structured status snapshot

Boundary:

- read-only
- no mutation
- no trading action

### Proposal Generator

Responsibility:

- generate a single candidate limit-order proposal from verified inputs
- include market, side, limit price, amount/value, reasoning, expiry, and risk notes
- block proposal if required facts are missing

Boundary:

- proposal only
- no execution
- no credential ownership

### Human Approval Gate

Responsibility:

- require explicit operator approval for the exact proposal
- reject stale, modified, ambiguous, or duplicate approval
- preserve approval timestamp and operator identity/source

Boundary:

- no inferred approval
- no approval from cron
- no replayed approval from prior session

### Order Executor Disabled By Default

Responsibility:

- future one-shot execution path only if separately approved
- remain inactive until explicit execution approval exists
- enforce limit-only, one-order-at-a-time rules

Boundary:

- disabled by default
- no autonomous trigger
- no market order
- no retry loop
- no cancellation/reorder path in first build

### Journal Logger

Responsibility:

- record proposals, approvals, STOP events, alerts, and execution outcomes if execution is ever approved
- support local markdown/json or Google Sheets as a practical logging store
- preserve append-only behavior in practice, even if not research-grade proof

Boundary:

- logging cannot repair state
- logging cannot unlock execution
- logging failure stops the path

### Alert Path

Responsibility:

- notify operator on STOP, proposal-ready, approval-needed, execution-disabled, validation-failed, and review-required states
- Telegram approval/alert path is acceptable in a future approved implementation

Boundary:

- alert is not approval unless explicitly designed and confirmed
- alert failure stops the path

### Stop Fuse

Responsibility:

- provide a clear global STOP condition
- block proposal/execution when uncertain
- allow operator to leave the system in read-only mode

Boundary:

- stop fuse defaults to STOP
- no self-reset
- no automatic override

## 4. Minimum Validation Checklist

Before proposal:

- USD/KRW/pre-held asset condition verified depending final asset design
- market symbol verified
- market status checked
- API status checked if API access is ever separately approved
- prior execution state checked
- log write path confirmed
- alert path confirmed

Before approval:

- proposal fields complete
- limit price present and bounded
- amount/value present and bounded
- proposal not expired
- proposal matches latest read-only snapshot
- duplicate proposal not active

Before execution, if ever separately approved:

- human approval exists for exact proposal
- approval not expired
- approval not already consumed
- open order check confirms no open order exists
- duplicate order check confirms no duplicate order exists
- KRW/asset condition still valid
- market status still acceptable
- API status still acceptable
- previous execution state permits one-shot execution
- journal logger path available
- failure handling path available
- alert path available
- stop fuse not active

Any failed checklist item:

- STOP
- log
- alert
- require human review

## 5. Failure Handling

Failure handling sequence:

1. detect
2. stop
3. log
4. alert
5. require human review

Required failure behavior:

- no hidden retry
- no silent continuation
- no automatic repair
- no automatic re-approval
- no automatic order replacement
- no cancellation/reorder path unless separately designed and approved

Examples of STOP conditions:

- API uncertain
- credentials uncertain
- Upbit status uncertain
- market status uncertain
- open order exists
- duplicate order suspected
- KRW/asset condition unclear
- stale proposal
- stale approval
- missing log path
- failed alert path
- previous execution state unclear

Human review required:

- any ambiguous account/order state
- any mismatch between proposal and latest snapshot
- any mismatch between approval and proposal
- any suspected duplicate
- any unexpected response or missing confirmation

## 6. Architecture Boundary

Future simple n8n-compatible structure:

1. Manual Trigger or read-only scheduled monitor, depending future approval
2. Read-Only Status Snapshot
3. Proposal Generator
4. Validation Checklist
5. Human Approval Gate
6. Disabled-by-Default One-Shot Executor
7. Journal Logger
8. Alert Path
9. Stop Fuse

Acceptable practical storage:

- Google Sheets log
- local markdown log
- local JSON log
- append-only report folder

Acceptable practical approval channel:

- Telegram approval, if separately approved
- manual n8n form/input, if separately approved
- local approval artifact, if separately approved

Forbidden architecture behavior:

- no autonomous loop
- no self-healing execution
- no concurrent execution
- no hidden retry
- no auto-unlock
- no live order path without separate implementation approval
- no credential/API access without separate approval
- no workflow activation without separate approval

## 7. Comparison With Archived WF07/WF08

WF07/WF08 archived system:

- research-grade safety proof system
- frozen and archived
- specification-only
- focused on lock manager proof, durability proof, replay determinism, scheduler determinism, immutable lineage, and concurrency proof
- real writer forbidden
- WF08 blocked
- live path forbidden

LIGHT SYSTEM:

- practical human-approved execution system
- simpler by design
- one-order-at-a-time
- no concurrency
- no research-grade proof claim
- no autonomous trading
- designed for future operator-managed workflow construction

Key separation:

- WF07/WF08 archive does not authorize this light system.
- This light system does not mutate or supersede WF07/WF08 archive artifacts.
- This light system does not inherit runtime authorization from WF07/WF08.
- Any future light implementation requires separate explicit approval.
- Any future live execution requires separate explicit approval.

## 8. Final Recommendation

Build first:

- read-only monitor design and proposal generator design
- validation checklist schema
- operator-readable proposal summary
- append-only journal format
- alert-only STOP path

Must remain manual:

- approval
- final order decision
- stop fuse override
- review of ambiguous market/account/order state
- any decision after API/credential/status uncertainty

Must remain blocked:

- autonomous trading
- market orders
- leverage
- auto-retry trading
- duplicate order path
- order execution without open-order check
- order execution without KRW/asset condition verification
- order execution if API/credential/status is uncertain
- workflow activation
- live Upbit API access
- executable order code
- WF08 implementation

Final decision:

- DESIGN_ONLY
- IMPLEMENTATION_NOT_AUTHORIZED
- EXECUTION_NOT_AUTHORIZED
- WF07_ARCHIVE_PRESERVED
- WF08_BLOCKED
- LIVE_PATH_FORBIDDEN
