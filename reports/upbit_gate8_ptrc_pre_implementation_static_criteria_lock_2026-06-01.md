# GATE_8_PTRC_PRE_IMPLEMENTATION_STATIC_CRITERIA_LOCK - Offline Static Governance Artifact (2026-06-01)
## Objective
- Lock static implementation criteria for future PTRC implementation without writing implementation code.
- Scope is offline governance/spec/static-review only.
## Static Criteria Lock
- PTRC implementation must preserve order-intent pre-trade validation completeness.
- PTRC implementation must preserve STOP + LOG + ALERT rejection behavior for failed checks.
- PTRC implementation must preserve limit-only order policy and hard reject market orders.
- PTRC implementation must preserve no margin/no leverage constraints.
- PTRC implementation must preserve capital-breach response: cancel outstanding + disable entry + human re-arm.
- No runtime trading code, no API calls, no credentials, no scheduler, no WF08 in this phase.
## Dependency Notes
- accepted_prior_gate: PASS_OFFLINE_TEST_PLAN_GOVERNANCE_FOR_CONTRACT_LAYER
- this_phase: GATE_8_PTRC_PRE_IMPLEMENTATION_STATIC_CRITERIA_LOCK
- next_action_candidate: GATE_9_IDEM_SPEC_SOURCE_BINDING_STATIC_REVIEW
## Scope Safety Locks
- implementation_created: false
- upbit_api_access: false
- credential_authorization: false
- wf08_authorization: false
- scheduler_authorization: false
- live_trading_authorization: false
- parser_execution: false
- fixture_creation: false
## Forbidden Claims (Negated Only)
- ready for live: false (not ready for live)
- implementation complete: false (implementation not complete)
- runtime ready: false (runtime not ready)
- credential ready: false (credential not ready)
- WF08 ready: false (WF08 not ready)
- scheduler ready: false (scheduler not ready)
This phase artifact does not authorize runtime implementation, order submission code, private endpoint execution, credential operations, scheduler activation, WF08 progression, shadow mode, or live mode.
