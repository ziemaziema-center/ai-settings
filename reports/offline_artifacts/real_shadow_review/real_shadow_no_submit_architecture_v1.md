# REAL SHADOW NO-SUBMIT ARCHITECTURE V1

## Future Architecture

DATA_ACCESS_LAYER -> SIGNAL_OBSERVER -> PTRC_OBSERVER -> IDEM_STUB -> OSM_RECORDER -> RECON_OBSERVER -> KILL_OBSERVER -> ALERT_OBSERVER -> SHADOW_RECORDER

## Required Invariants

- no exchange submission
- no create order endpoint
- no live order
- no shadow order against exchange
- all hypothetical orders become STUBBED_NOT_SENT
- PERSISTED BEFORE SUBMITTED preserved by making SUBMITTED impossible
- KILL blocks recorder continuation
- RECON drift blocks new candidate observation
- ALERT required for critical synthetic/real-data anomalies
- scheduler disabled until separate approval

## Required Recorder Semantics

- recorder writes observational evidence only
- recorder state machine never emits mutation states
- recorder preserves causal sequence for daily review and audit

## Mandatory STOP Triggers

- any mutation-capable endpoint invocation request
- any state transition toward SUBMITTED, ACK_RECEIVED, OPEN, FILLED, PARTIAL
- unresolved critical RECON drift
- KILL active state

Real shadow review score measures review completeness, blocker clarity, and safety coverage only; it does not authorize real shadow execution, Upbit API access, credential use, scheduler activation, live trading, WF08, or production readiness.

This document does not authorize live trading, real shadow mode execution, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.
