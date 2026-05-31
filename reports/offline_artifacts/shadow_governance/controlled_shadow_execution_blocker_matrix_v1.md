# CONTROLLED SHADOW EXECUTION BLOCKER MATRIX V1

| blocker_id | status | required_evidence | responsible_gate | safe_next_action | forbidden_shortcut |
| --- | --- | --- | --- | --- | --- |
| CSEB-001_CREDENTIAL_USE_NOT_APPROVED | BLOCKED | credential gate approval artifact | CRED_GATE | keep credentials blocked and maintain checklist evidence | read/store credentials anyway |
| CSEB-002_UPBIT_API_USE_NOT_APPROVED | BLOCKED | explicit endpoint allow/deny approval record | API_GATE | keep all API calls disabled in scope phase | call API for convenience test |
| CSEB-003_SCHEDULER_NOT_APPROVED | BLOCKED | scheduler governance approval record | SCHED_GATE | keep scheduler inactive | activate scheduler for partial run |
| CSEB-004_RECORDER_RUNTIME_NOT_IMPLEMENTED_IN_APPROVED_EXEC_SCOPE | BLOCKED | approved runtime design + reviewed implementation package | REC_GATE | keep contract-only recorder | implement runtime outside approval |
| CSEB-005_N_DAY_SHADOW_NOT_STARTED | BLOCKED | signed execution kickoff record | SHADOW_START_GATE | prepare authorization packet template only | claim started without approval |
| CSEB-006_N_DAY_SHADOW_NOT_COMPLETED | BLOCKED | continuous N-day evidence logs and reviews | SHADOW_COMPLETE_GATE | define pass/fail criteria | claim completion from spec docs |
| CSEB-007_WF08_REVIEW_BLOCKED | BLOCKED | WF08 review artifact | WF08_GATE | keep WF08 blocked | bypass WF08 gate |
| CSEB-008_LIVE_AUTHORIZATION_BLOCKED | BLOCKED | signed live authorization packet | LIVE_GATE | keep live blocked | interpret shadow scope as live approval |
| CSEB-009_HUMAN_SHADOW_EXEC_AUTH_MISSING | BLOCKED | human approval packet for shadow execution | HUMAN_SHADOW_GATE | request human decision only | self-authorize execution |
| CSEB-010_SHADOW_KILL_ALERT_RECON_EVIDENCE_LINK_REQUIRED | BLOCKED | linked KILL/ALERT/RECON evidence set | SAFETY_EVID_GATE | attach required evidence links | start without evidence chain |
| CSEB-011_DAILY_REVIEW_OWNER_NOT_NAMED | BLOCKED | named daily review owner and backup | REVIEW_OWNER_GATE | assign owner before start | run without accountable owner |
| CSEB-012_ROLLBACK_STOP_PROCEDURE_NOT_APPROVED | BLOCKED | approved rollback/stop procedure | ROLLBACK_GATE | finalize and approve stop plan | defer rollback design until incident |

Shadow scope score measures scope, evidence, governance, and blocker completeness only; it does not authorize shadow execution, live trading, Upbit API use, credential use, runtime activation, scheduler activation, WF08, or production readiness.

This document does not authorize live trading, shadow mode execution, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

