# FULL AUTO LIVE TRADING GATE MATRIX V1

| Gate | Purpose | Dependencies | Required Evidence | Pass Criteria | Fail Behavior | Forbidden Shortcut | Current Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OFFLINE_GOVERNANCE_CONFIRMED | freeze contract governance | none | governance final verdict | verdict confirmed | stay spec-only | skip contract review | PASSED |
| OFFLINE_SYNTHETIC_TESTS_CONFIRMED | prove offline harness safety | gate 1 | 16/16 tests + score report | tests pass, forbidden states 0 | PASS_WITH_GAP/BLOCK | skip synthetic checks | PASSED |
| STRESS_TEST_GOVERNANCE_CONFIRMED | define stress controls | gate 2 | stress governance plan | scenarios/criteria complete | BLOCKED | run shadow before stress plan | NOT_STARTED |
| STRESS_TEST_HARNESS_IMPLEMENTED | implement stress harness later | gate 3 | implementation evidence | harness build complete | BLOCKED | use live API as shortcut | NOT_STARTED |
| STRESS_TEST_EXECUTED | execute stress simulation | gate 4 | stress execution report | all required scenarios pass | BLOCKED | partial scenario claim | NOT_STARTED |
| SHADOW_ENTRY_CRITERIA_CONFIRMED | define shadow gate | gate 5 | shadow criteria artifact | entry/exit rules complete | BLOCKED | treat docs as execution | NOT_STARTED |
| SHADOW_RUNTIME_STUB_IMPLEMENTED | future non-live stub runtime | gate 6 | stub design + tests | no exchange submission path | BLOCKED | direct live wiring | NOT_STARTED |
| SHADOW_MODE_EXECUTED_N_DAYS | continuity evidence | gate 7 | N-day logs | uninterrupted criteria met | BLOCKED | abbreviated day-count | NOT_STARTED |
| CREDENTIAL_GOVERNANCE_OPERATIONAL | key safety controls | gate 8 | credential checklist evidence | read+trade only, no withdraw | BLOCKED | plaintext/.env key usage | NOT_STARTED |
| DEPLOYMENT_GOVERNANCE_OPERATIONAL | deployment safety controls | gate 8 | hash/checklist evidence | hash match + peer review | BLOCKED | manual SSH deploy | NOT_STARTED |
| KILL_SWITCH_DRY_RUN_PASSED | fail-safe proof | gates 9-10 | dry-run incident evidence | kill trigger and sticky state proven | BLOCKED | no incident record | NOT_STARTED |
| RECONCILIATION_DRY_RUN_PASSED | intent/reality drift proof | gate 11 | dry-run recon report | drift handling proven | BLOCKED | bypass recon | NOT_STARTED |
| ALERT_SLA_DRY_RUN_PASSED | alert timeliness proof | gate 11 | SLA telemetry | actionable alert timing met | BLOCKED | async digest-only alert | NOT_STARTED |
| HUMAN_WF08_REVIEW | human governance gate | gates 1-13 | signed WF08 review record | explicit WF08 decision logged | BLOCKED | implied approval | NOT_STARTED |
| HUMAN_LIVE_AUTHORIZATION | final scoped authorization | gate 14 | live authorization packet | reversible scoped signed approval | BLOCKED | auto-enable live mode | NOT_STARTED |

Readiness score measures documentation, governance, and validation completeness only; it does not authorize trading, does not predict profit, and does not indicate runtime, shadow, live, or WF08 readiness.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
