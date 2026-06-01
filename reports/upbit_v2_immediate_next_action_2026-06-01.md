# UPBIT V2 Immediate Next Action - 2026-06-01

NEXT_ACTION_ID
- V2_GATE7_PTRC_SPEC_SOURCE_BINDING_STATIC_REVIEW

SCOPE
- Perform one offline-only static source-binding review that verifies PTRC gate requirements (pre-trade mandatory checks, reject behavior, threshold breach semantics, no bypass) are traceable to V2 governance source and do not contradict preserved V1 STOP discipline. No runtime code, no parser, no fixtures, no API/credential/scheduler/WF08 operations.

INPUTS_REQUIRED
- reports/offline_artifacts/governance_sources/01_governance_v2_institutional_upgrade.md
- reports/offline_artifacts/governance_sources/02_reference_standards_and_sources.md
- reports/offline_artifacts/governance_sources/03_operational_runbook_v2.md
- reports/offline_artifacts/governance_sources/04_codex_continuation_prompt.md
- reports/upbit_v2_total_completion_reconciliation_2026-06-01.md

OUTPUT_ARTIFACT
- reports/upbit_v2_gate7_ptrc_source_binding_static_review_2026-06-01.md (markdown)

APPROVAL_GATE
- Human static reviewer approval; approval logged in reports and patch history with timestamp and artifact hash.

FORBIDDEN_SIDE_EFFECTS
- no live trading
- no Upbit API calls
- no credential creation/read
- no parser execution
- no fixture creation
- no WF08 transition
- no scheduler activation
- no runtime wiring

STOP_CONDITIONS
- required governance source missing
- contradictory clause that cannot be resolved offline
- wording implying live authorization
- any need for credential/API/runtime action
