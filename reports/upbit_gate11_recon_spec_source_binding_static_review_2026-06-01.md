# GATE_11_RECON_SPEC_SOURCE_BINDING_STATIC_REVIEW - Offline Static Governance Artifact (2026-06-01)
## Objective
- Bind RECON spec to V2 standards and offline test contracts without implementation code.
- Scope is offline governance/spec/static-review only.
## Static Criteria Lock
- RECON spec must detect local-intent versus exchange-state drift.
- RECON spec must require orphan exchange order cancellation path.
- RECON spec must route unresolved drift to KILL evaluation.
- RECON spec must require cold-start full reconciliation before progression.
- RECON spec must require full reconciliation after disconnect recovery.
- No runtime trading code, no API calls, no credentials, no scheduler, no WF08 in this phase.
## Dependency Notes
- accepted_prior_gate: PASS_OFFLINE_TEST_PLAN_GOVERNANCE_FOR_CONTRACT_LAYER
- this_phase: GATE_11_RECON_SPEC_SOURCE_BINDING_STATIC_REVIEW
- next_action_candidate: GATE_13_KILL_SPEC_SOURCE_BINDING_STATIC_REVIEW
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
