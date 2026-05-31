# SHADOW RECORDER EXECUTION CONTRACT V1

## Purpose

Define future recorder execution behavior for controlled shadow runs under separate approval.

## Inputs

- signal events
- PTRC decision events
- IDEM events
- OSM intent events
- RECON events
- KILL events
- ALERT events

## Outputs

- local recorder event log only
- daily digest summary

## Hard Constraints

- no exchange submission
- no live order
- no shadow order against exchange
- no credential read
- no scheduler activation by default
- allowed only after separate human execution approval

## Behavior Rules

- recorder must stop on KILL
- recorder must flag unresolved RECON drift
- every hypothetical submission must be marked SHADOW_SUBMISSION_STUBBED_NOT_SENT

## Required Event States

- SHADOW_SIGNAL_OBSERVED
- SHADOW_PTRC_REJECTED
- SHADOW_PTRC_ELIGIBLE
- SHADOW_IDEM_PREPARED
- SHADOW_OSM_INTENT_PERSISTED
- SHADOW_SUBMISSION_STUBBED_NOT_SENT
- SHADOW_RECON_DRIFT_DETECTED
- SHADOW_KILL_TRIGGERED
- SHADOW_ALERT_REQUIRED
- SHADOW_HUMAN_REVIEW_REQUIRED

## Forbidden States

- SUBMITTED
- ACK_RECEIVED
- OPEN
- FILLED
- PARTIAL
- LIVE_ORDER
- EXCHANGE_CONNECTED
- CREDENTIAL_READ

## Final Contract Status

CONTRACT_ONLY_NOT_EXECUTED

Shadow scope score measures scope, evidence, governance, and blocker completeness only; it does not authorize shadow execution, live trading, Upbit API use, credential use, runtime activation, scheduler activation, WF08, or production readiness.

This document does not authorize live trading, shadow mode execution, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

This document does not authorize live trading, shadow mode, Upbit API access, credential use, scheduler activation, parser execution, fixture creation, WF08 transition, runtime wiring, implementation, or production-readiness claims.

