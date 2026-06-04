# UPBIT Contract Layer Offline Test Plan Governance - 2026-06-01

## [SECTION_1] CONTRACT_LAYER_TEST_OBJECTIVE
- Prove safety contracts before implementation.
- Prevent assumption-based execution.
- Define pass/fail criteria before code exists.
- Keep all future runtime/live/API work blocked.

## [SECTION_2] REQUIRED_TEST_CONTRACTS

### 1. PTRC
- Required future test categories:
  - pre-trade validation completeness
  - rejection logging integrity
  - escalation linkage to KILL path
  - order-shape policy enforcement
  - capital-threshold breach response
- Mandatory assertions:
  - every order intent must pass pre-trade validation
  - any failed check rejects order
  - rejection logs reason/check_id/raw_intent_hash
  - alert dependency exists
  - repeated rejection escalates to KILL evaluation
  - limit order only
  - market order hard rejected
  - no margin/leverage
  - capital threshold breach cancels outstanding orders and disables new entry
- Forbidden side effects:
  - no live order submission
  - no credential read/write
  - no parser execution
  - no scheduler activation
- Pass/fail criteria:
  - PASS only if all mandatory assertions are covered by offline tests and all forbidden side effects remain absent.

### 2. IDEM
- Required future test categories:
  - client_order_id generation and format
  - id persistence before network boundary
  - retry id consistency
  - duplicate suppression under ambiguous outcomes
  - exchange/client mapping integrity
- Mandatory assertions:
  - UUIDv4 client_order_id required
  - client_order_id persisted before network send
  - timeout/5xx/ambiguous response never creates duplicate
  - retry uses same client_order_id
  - exchange UUID maps 1:1 to client_order_id
- Forbidden side effects:
  - no duplicate live submission behavior
  - no hidden id mutation across retries
- Pass/fail criteria:
  - PASS only if duplicate suppression and 1:1 mapping proofs are complete in offline test evidence.

### 3. RECON
- Required future test categories:
  - drift detection
  - orphan cleanup policy
  - unresolved drift escalation
  - cold-start reconciliation
  - recovery reconciliation
- Mandatory assertions:
  - local intent and exchange reality drift detected
  - orphan exchange order is cancelled
  - unresolved drift triggers KILL
  - cold-start full reconciliation required
  - recovery full reconciliation required after disconnect
- Forbidden side effects:
  - no new entry while unresolved drift exists
- Pass/fail criteria:
  - PASS only if unresolved drift always blocks progression and routes to KILL evaluation.

### 4. KILL
- Required future test categories:
  - sticky latch semantics
  - order-entry disablement
  - open-order cancel behavior
  - human re-arm requirements
  - no auto-clear enforcement
- Mandatory assertions:
  - KILL is sticky
  - KILL disables new order entry
  - KILL cancels open orders
  - re-arm requires human approval, root cause, reconciliation, hash-chain verification
  - no auto-clear
- Forbidden side effects:
  - no autonomous re-enable path
- Pass/fail criteria:
  - PASS only if no test path can clear KILL without human re-arm evidence.

### 5. ALERT
- Required future test categories:
  - SLA timing
  - payload completeness
  - routing policy
  - anti-silent-failure guard
- Mandatory assertions:
  - actionable alert generated within 5 seconds for KILL/PTRC cluster/RECON drift
  - alert includes required fields
  - email-only/silent logging forbidden
- Forbidden side effects:
  - no silent critical failure path
- Pass/fail criteria:
  - PASS only if alert SLA and payload requirements are satisfied in offline instrumentation tests.

### 6. HEART
- Required future test categories:
  - stale-data gate
  - disconnect handling
  - clock-integrity checks
  - dead-man watchdog path
- Mandatory assertions:
  - stale market data blocks new orders
  - disconnect beyond grace triggers KILL
  - clock skew triggers STOP + alert
  - dead-man watchdog rule exists
- Forbidden side effects:
  - no order progression with stale heartbeat
- Pass/fail criteria:
  - PASS only if stale/disconnect/clock-skew paths always block progression.

### 7. BUDGET
- Required future test categories:
  - Remaining-Req accounting
  - local token bucket behavior
  - margin-to-limit policy
  - throttle escalation handling
- Mandatory assertions:
  - Remaining-Req tracked
  - local token bucket exists
  - safety margin below Upbit limit
  - 429 triggers backoff + alert
  - 418 triggers KILL + human escalation
- Forbidden side effects:
  - no aggressive retry storm on limit errors
- Pass/fail criteria:
  - PASS only if 429/418 responses enforce conservative control flow and escalation.

### 8. OSM
- Required future test categories:
  - state-transition observability
  - hash-chain integrity
  - LOST-state handling
  - transition logging completeness
- Mandatory assertions:
  - every state transition logged
  - hash-chain covers every transition
  - LOST state triggers KILL evaluation
  - no transition without log entry
- Forbidden side effects:
  - no invisible transition path
- Pass/fail criteria:
  - PASS only if log completeness and hash-chain continuity are verifiable offline.

## [SECTION_3] TEST_PLAN_BLOCKERS
- no implementation yet
- no runtime proof yet
- no authenticated shadow proof yet
- no stress execution yet
- no annual self-assessment approval yet
- no WF08
- no GATE_23

## [SECTION_4] FUTURE_GATE_MAPPING
- GATE_8 PTRC implementation static review
- GATE_10 IDEM implementation static review
- GATE_12 RECON implementation static review
- GATE_14 KILL implementation static review
- GATE_15 HEART+BUDGET+OSM implementation
- GATE_16 ALERT SLA instrumentation
- GATE_19 STRESS test
- GATE_20 SHADOW mode

## [SECTION_5] FORBIDDEN_CLAIMS
- ready for live: false (not ready for live)
- implementation complete: false (implementation not complete)
- runtime ready: false (runtime not ready)
- credential ready: false (credential not ready)
- WF08 ready: false (WF08 not ready)
- scheduler ready: false (scheduler not ready)

## Scope Safety Locks
- live_trading_authorization: false
- credential_authorization: false
- wf08_authorization: false
- scheduler_authorization: false
- upbit_api_access: false
- parser_execution: false
- fixture_creation: false
- implementation_created: false

This artifact is governance/test-planning only and does not authorize implementation, runtime wiring, shadow/live execution, parser execution, fixture creation, credentials, or Upbit API operations.
