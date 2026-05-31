# CONTROLLED N-DAY SHADOW SCOPE V1

## 1. Status

- status: SCOPE_DEFINED_ONLY
- execution_status: NOT_EXECUTED
- approval_status: HUMAN_DECISION_REQUIRED

## 2. Definition of Controlled N-day Shadow

Controlled N-day shadow means running decision, risk, idempotency, reconciliation, kill, and alert logic in observation mode for N continuous days while exchange submission remains stubbed and not sent.

## 3. Explicit Non-Authorization Boundary

- this scope definition is not shadow execution
- this scope definition is not live authorization
- no runtime activation is permitted by this document

## 4. Required Prior Evidence

- stress harness result (stress_harness_result_v1.md)
- local dry-run result (local_dry_run_result_v1.md)
- pre-live gate matrix with blocked live gates
- shadow entry review + blocker matrix + evidence checklist

## 5. What Shadow May Do

- observe candidate signal flow
- record PTRC/IDEM/OSM/RECON/KILL/ALERT decisions
- emit daily review digest artifacts
- mark hypothetical submissions as STUBBED_NOT_SENT only

## 6. What Shadow Must Never Do

- no Upbit API use
- no credentials
- no scheduler activation
- submit exchange order
- transition to WF08
- claim N-day completion without separately approved future run
- N-day completion cannot be claimed until a separately approved run executes continuously

## 7. Required Stubs

- submission stub that always emits SHADOW_SUBMISSION_STUBBED_NOT_SENT
- recorder stub that writes local-only audit records
- no transport stub may call exchange endpoints

## 8. Required Recorder Behavior

- local-only event recording
- deterministic state sequence recording
- unresolved RECON drift flagging
- immediate stop behavior on KILL

## 9. Daily Review Requirement

- daily digest must be produced
- daily human reviewer must be assigned before execution
- unresolved alerts/recon drift must be reviewed same day

## 10. Required Human Authorization Before Execution

- named human approver
- explicit N-day window
- allowed/blocked endpoint list
- credential policy and scheduler policy fields
- reversible approval record and rollback authority

## 11. STOP Conditions

- any attempt to enable scheduler
- any credential read request
- any Upbit API call proposal in execution path
- any detected forbidden state (SUBMITTED, LIVE_ORDER, EXCHANGE_CONNECTED)
- any unresolved RECON drift after review SLA

## 12. Final Safety Verdict

CONTROLLED_N_DAY_SHADOW_SCOPE_DEFINED_BUT_NOT_AUTHORIZED_FOR_EXECUTION

Shadow scope score measures scope, evidence, governance, and blocker completeness only; it does not authorize shadow execution, live trading, Upbit API use, credential use, runtime activation, scheduler activation, WF08, or production readiness.

This document does not authorize live trading, shadow mode execution, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.


