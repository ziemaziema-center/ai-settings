# AUTHENTICATED SHADOW REVIEW BLOCKER MATRIX V1

| blocker_id | status | required_evidence | responsible_gate | allowed_next_step | forbidden_shortcut |
| --- | --- | --- | --- | --- | --- |
| CRED_AUTH_MISSING | BLOCKED | explicit human credential authorization | CRED_GATE | credential governance review-only | any credential use without approval |
| CRED_STORAGE_NOT_VALIDATED | BLOCKED | operational storage validation record | CRED_GATE | storage checklist review | runtime credential injection |
| IP_ALLOWLIST_NOT_VALIDATED | BLOCKED | allowlist verification evidence | CRED_GATE | network policy review | private endpoint call |
| READ_ONLY_CRED_PROOF_MISSING | BLOCKED | read-only private endpoint proof plan | SHADOW_GATE | define proof protocol | private API execution |
| ORDER_HARD_BLOCK_RUNTIME_NOT_PROVEN | BLOCKED | runtime hard-block telemetry under auth scope | PTRC/OSM_GATE | offline contract test update | order endpoint invocation |
| SCHEDULER_NOT_AUTHORIZED | BLOCKED | explicit scheduler authorization | DEPLOY_GATE | manual-run continuation | scheduler activation |
| WF08_BLOCKED | BLOCKED | WF08 approval packet | WF08_GATE | pre-WF08 offline review | WF08 transition |
| LIVE_AUTH_BLOCKED | BLOCKED | live authorization packet | LIVE_GATE | remain offline/public-data | live trade/order |
| AUTH_DATA_SCOPE_NOT_APPROVED | BLOCKED | authenticated scope approval | SHADOW_GATE | scope review-only | auth scope expansion |
| ACCOUNT_PRIVATE_CLASS_NOT_APPROVED | BLOCKED | endpoint class approval | ENDPOINT_GATE | endpoint classification review | account/private calls |
| KILL_RECON_ALERT_NOT_PROVEN_AUTH | BLOCKED | authenticated-data resilience evidence | STRESS/RECON_GATE | offline test design | auth-run without fail-safe proof |
| AUTH_N_DAY_NOT_EXECUTED | BLOCKED | separately approved authenticated N-day evidence | SHADOW_GATE | stay in public-data mode | claim authenticated readiness |

?쏷his document does not authorize live trading, authenticated real shadow mode execution, Upbit private API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.??

This document does not authorize live trading, real shadow mode execution, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.


This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

